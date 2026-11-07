"""Release-backed state transfers with staged downloads and verified upload sizes."""

from __future__ import annotations

import json
import os
import re
import shutil
import sqlite3
import subprocess
from contextlib import closing
from pathlib import Path
from tempfile import NamedTemporaryFile, TemporaryDirectory

from pydantic import ValidationError

from pipeline.models import Evidence

RELEASE_TAG = "data-latest"
ASSETS = ("gateway.sqlite", "evidence.jsonl")


class ReleaseError(RuntimeError):
    """A sanitised release diagnostic, safe to include in a failure issue."""


class StaleWorkingCopy(ReleaseError):
    """A previous or concurrent writer owns the working database."""


def preflight(state_dir: Path) -> None:
    """Preserve an existing working copy and explain its manual removal."""
    path = Path(state_dir) / "gateway.work.sqlite"
    if path.exists():
        quoted = str(path).replace("'", "''")
        raise StaleWorkingCopy(
            f"Working copy already exists: {path}. Ensure no pipeline is running and inspect it. "
            f"To discard it in PowerShell, run: Remove-Item -LiteralPath '{quoted}'"
        )


def replace_file(source: Path, destination: Path) -> None:
    """Copy and atomically replace one file, including across filesystem volumes."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile(dir=destination.parent, prefix=f".{destination.name}.", delete=False) as handle:
        temporary = Path(handle.name)
    try:
        shutil.copyfile(source, temporary)
        temporary.replace(destination)
    finally:
        temporary.unlink(missing_ok=True)


def replace_bundle(sources: list[tuple[Path, Path]], backup_dir: Path) -> None:
    """Restore the previous local bundle if a replacement raises an I/O error.

    Replacements are atomic per file. This handles ordinary errors, not process
    termination between files; the runbook describes recovery from interruption.
    """
    backups = []
    for index, (_, destination) in enumerate(sources):
        backup = backup_dir / f"backup-{index}"
        existed = destination.exists()
        if existed:
            shutil.copyfile(destination, backup)
        backups.append((destination, backup if existed else None))
    replaced = []
    try:
        for source, destination in sources:
            replace_file(source, destination)
            replaced.append(destination)
    except OSError:
        for destination, backup in reversed(backups):
            if destination in replaced:
                if backup is None:
                    destination.unlink(missing_ok=True)
                else:
                    replace_file(backup, destination)
        raise


def _gh(arguments: list[str]) -> subprocess.CompletedProcess[str]:
    executable = shutil.which("gh")
    if executable is None:
        raise ReleaseError("GitHub CLI gh was not found on PATH")
    timeout = 60
    if arguments[1] in {"download", "upload"}:
        try:
            timeout = int(os.environ.get("AI_HUB_RELEASE_TIMEOUT_SECONDS", "600"))
            if timeout <= 0:
                raise ValueError
        except ValueError:
            raise ReleaseError("AI_HUB_RELEASE_TIMEOUT_SECONDS must be a positive integer") from None
    try:
        return subprocess.run(
            [executable, *arguments], capture_output=True, text=True,
            encoding="utf-8", timeout=timeout, check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise ReleaseError(f"gh release {arguments[1]} failed: {type(exc).__name__}") from None


def _checked(arguments: list[str]) -> str:
    result = _gh(arguments)
    if result.returncode:
        raise ReleaseError(f"gh release {arguments[1]} failed (exit {result.returncode}); check authentication and Actions logs")
    return result.stdout


def _assets() -> dict[str, int] | None:
    result = _gh(["release", "view", RELEASE_TAG, "--json", "assets"])
    if result.returncode:
        # Authentication, permission, network and missing-asset errors are not a
        # first run. Tolerate case, spacing and a diagnostic suffix around gh's
        # "release not found" wording, but require its ordinary failure exit.
        if result.returncode == 1 and re.fullmatch(
            r"release[ \t]+not[ \t]+found(?:[.:][^\r\n]*)?",
            result.stderr.strip(), flags=re.IGNORECASE,
        ):
            return None
        raise ReleaseError(f"gh release view failed (exit {result.returncode}); not a missing release")
    try:
        entries = json.loads(result.stdout)["assets"]
        if not isinstance(entries, list):
            raise ValueError("Invalid assets")
        assets = {}
        for item in entries:
            name, size = item["name"], item["size"]
            if not isinstance(name, str) or type(size) is not int or size < 0 or name in assets:
                raise ValueError("Invalid asset metadata")
            assets[name] = size
        return assets
    except (KeyError, TypeError, ValueError):
        raise ReleaseError("gh release view returned invalid asset metadata") from None


def validate_bundle(state_dir: Path) -> str:
    """Require an intact promoted database and evidence from its last good run."""
    database, evidence = (Path(state_dir) / name for name in ASSETS)
    if not database.is_file() or not evidence.is_file():
        raise ReleaseError("A promoted gateway.sqlite and evidence.jsonl are both required")
    try:
        with closing(sqlite3.connect(database.resolve().as_uri() + "?mode=ro", uri=True)) as conn:
            if conn.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
                raise ValueError("Integrity check failed")
            if conn.execute("PRAGMA foreign_key_check").fetchone() is not None:
                raise ValueError("Foreign key check failed")
            row = conn.execute(
                "SELECT run_id, status, finished, gate_results_json FROM run_log ORDER BY rowid DESC LIMIT 1"
            ).fetchone()
        if row is None or row[1] != "succeeded" or row[2] is None:
            raise ValueError("No successful promotion")
        gates = json.loads(row[3])
        if not isinstance(gates, dict) or any(gates.get(name) is not True for name in ("gate_2", "gate_3")):
            raise ValueError("Missing passing gates")
        with evidence.open(encoding="utf-8") as handle:
            for line in handle:
                record = json.loads(line)
                if record["run_id"] != row[0]:
                    raise ValueError("Evidence belongs to a different run")
                Evidence.model_validate(record["evidence"])
        return row[0]
    except (sqlite3.Error, KeyError, TypeError, ValueError, ValidationError):
        raise ReleaseError("State bundle is invalid, ungated or has mismatched evidence") from None


def _verify_sizes(directory: Path, assets: dict[str, int]) -> None:
    for name in ASSETS:
        path = directory / name
        if name not in assets or not path.is_file() or path.stat().st_size != assets[name]:
            raise ReleaseError(f"Release asset missing or size mismatch: {name}")


def pull(state_dir: Path = Path("state")) -> bool:
    """Download both assets; an absent data-latest release is the first run."""
    state_dir = Path(state_dir)
    preflight(state_dir)
    assets = _assets()
    if assets is None:
        return False
    state_dir.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(prefix=".release-", dir=state_dir) as temporary:
        staged = Path(temporary)
        _checked([
            "release", "download", RELEASE_TAG, "--pattern", "gateway.sqlite",
            "--pattern", "evidence.jsonl", "--dir", str(staged),
        ])
        _verify_sizes(staged, assets)
        validate_bundle(staged)
        replace_bundle([(staged / name, state_dir / name) for name in ASSETS], staged)
    return True


def push(state_dir: Path = Path("state")) -> None:
    """Upload only a gated canonical bundle, then compare both remote sizes."""
    state_dir = Path(state_dir)
    preflight(state_dir)
    validate_bundle(state_dir)
    if _assets() is None:
        _checked([
            "release", "create", RELEASE_TAG, "--title", "Pipeline state",
            "--notes", "Latest gated AI Hub state and full evidence.", "--latest=false",
        ])
    _checked(["release", "upload", RELEASE_TAG, *(str(state_dir / name) for name in ASSETS), "--clobber"])
    assets = _assets()
    if assets is None:
        raise ReleaseError("Release disappeared after upload")
    _verify_sizes(state_dir, assets)

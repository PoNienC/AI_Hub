"""Release round trips through a real fake-gh process on PATH, without network."""

import json
import os
import shutil
import sqlite3
import subprocess
import sys
from contextlib import closing
from datetime import UTC, datetime
from pathlib import Path

import pytest

from pipeline import release
from pipeline.models import Evidence
from pipeline.store import StateStore

NOW = datetime(2026, 11, 7, tzinfo=UTC)


@pytest.fixture
def bundle(tmp_path, repo):
    directory = tmp_path / "local"
    with StateStore(directory) as store:
        store.upsert_repo(repo, observed_at=NOW)
        store.start_run("good", started_at=NOW, budgets={})
        store.finish_run("good", finished_at=NOW, status="succeeded", budgets={}, rows_in=1,
                         rows_out=1, gate_results={"gate_2": True, "gate_3": True})
        store.promote({"gate_2": True, "gate_3": True})
    item = Evidence(repo_id=repo.github_id, source="scorecard", status="absent", fetched_at=NOW)
    (directory / "evidence.jsonl").write_text(json.dumps({
        "run_id": "good", "evidence": item.model_dump(mode="json"),
    }) + "\n", encoding="utf-8")
    return directory


@pytest.fixture
def fake_gh(tmp_path, monkeypatch):
    root = tmp_path / "fake-gh"
    root.mkdir()
    (root / "remote").mkdir()
    (root / "mode.json").write_text("{}", encoding="utf-8")
    script = Path(__file__).parent / "fixtures/fake_gh.py"
    if os.name == "nt":
        executable = root / "gh.cmd"
        executable.write_text(f'@"{sys.executable}" "{script}" %*\n', encoding="utf-8")
    else:
        executable = root / "gh"
        executable.write_text(f'#!{sys.executable}\n' + script.read_text(encoding="utf-8"), encoding="utf-8")
        executable.chmod(0o755)
    monkeypatch.setenv("FAKE_GH_ROOT", str(root))
    monkeypatch.setenv("PATH", str(root) + os.pathsep + os.environ.get("PATH", ""))
    return root


def commands(root):
    return [json.loads(line) for line in (root / "commands.jsonl").read_text(encoding="utf-8").splitlines()]


def mode(root, **values):
    (root / "mode.json").write_text(json.dumps(values), encoding="utf-8")


def test_absent_release_is_first_run(fake_gh, tmp_path):
    target = tmp_path / "new-state"
    assert release.pull(target) is False
    assert not target.exists()
    assert commands(fake_gh) == [["release", "view", "data-latest", "--json", "assets"]]


@pytest.mark.parametrize("error", [
    "HTTP 401 Bad credentials", "HTTP 404 Not Found", "network unavailable",
    "release not foundry", "release not found\nHTTP 401 Bad credentials",
])
def test_other_errors_are_not_first_run(fake_gh, bundle, error):
    before = (bundle / "gateway.sqlite").read_bytes()
    mode(fake_gh, error=error)
    with pytest.raises(release.ReleaseError, match="not a missing release"):
        release.pull(bundle)
    assert (bundle / "gateway.sqlite").read_bytes() == before


@pytest.mark.parametrize("diagnostic", [
    "  RELEASE NOT FOUND\n", "release\t not  found", "release not found.",
    "release not found: data-latest",
])
def test_missing_release_diagnostic_variants(fake_gh, tmp_path, diagnostic):
    mode(fake_gh, error=diagnostic)
    assert release.pull(tmp_path / "new-state") is False


def test_missing_release_wording_with_other_exit_is_not_first_run(monkeypatch, tmp_path):
    monkeypatch.setattr(release.shutil, "which", lambda _: "gh")
    monkeypatch.setattr(release.subprocess, "run", lambda *args, **kwargs:
                        subprocess.CompletedProcess(args, 2, "", "release not found"))
    with pytest.raises(release.ReleaseError, match="not a missing release"):
        release.pull(tmp_path)


@pytest.mark.parametrize("configured,expected", [(None, 600), ("1200", 1200)])
def test_transfer_timeouts_leave_metadata_timeout_unchanged(
    fake_gh, bundle, tmp_path, monkeypatch, configured, expected,
):
    if configured is None:
        monkeypatch.delenv("AI_HUB_RELEASE_TIMEOUT_SECONDS", raising=False)
    else:
        monkeypatch.setenv("AI_HUB_RELEASE_TIMEOUT_SECONDS", configured)
    original = subprocess.run
    calls = []

    def recording_run(arguments, **kwargs):
        calls.append((arguments[2], kwargs["timeout"]))
        return original(arguments, **kwargs)

    monkeypatch.setattr(release.subprocess, "run", recording_run)
    release.push(bundle)
    assert release.pull(tmp_path / "downloaded") is True
    assert calls == [
        ("view", 60), ("create", 60), ("upload", expected), ("view", 60),
        ("view", 60), ("download", expected),
    ]


@pytest.mark.parametrize("configured", ["0", "-1", "invalid", "1.5", "inf"])
def test_invalid_transfer_timeout_prevents_upload(fake_gh, bundle, monkeypatch, configured):
    monkeypatch.setenv("AI_HUB_RELEASE_TIMEOUT_SECONDS", configured)
    with pytest.raises(release.ReleaseError, match="must be a positive integer"):
        release.push(bundle)
    assert all(command[1] != "upload" for command in commands(fake_gh))


def test_upload_then_download_exact_commands_and_bytes(fake_gh, bundle, tmp_path):
    release.push(bundle)
    recorded = commands(fake_gh)
    assert recorded == [
        ["release", "view", "data-latest", "--json", "assets"],
        ["release", "create", "data-latest", "--title", "Pipeline state", "--notes",
         "Latest gated AI Hub state and full evidence.", "--latest=false"],
        ["release", "upload", "data-latest", str(bundle / "gateway.sqlite"),
         str(bundle / "evidence.jsonl"), "--clobber"],
        ["release", "view", "data-latest", "--json", "assets"],
    ]
    target = tmp_path / "downloaded"
    assert release.pull(target) is True
    download = commands(fake_gh)[-1]
    assert download[:-1] == ["release", "download", "data-latest", "--pattern", "gateway.sqlite",
                            "--pattern", "evidence.jsonl", "--dir"]
    assert Path(download[-1]).parent == target
    for name in release.ASSETS:
        assert (target / name).read_bytes() == (bundle / name).read_bytes()
    release.push(target)
    assert len([args for args in commands(fake_gh) if args[1] == "create"]) == 1


@pytest.mark.parametrize("fault", ["size_delta", "download_fail", "missing_evidence", "invalid_metadata", "mismatch"])
def test_failed_pull_keeps_existing_bundle(fake_gh, bundle, fault):
    for name in release.ASSETS:
        shutil.copyfile(bundle / name, fake_gh / "remote" / name)
    (fake_gh / "exists").touch()
    before = {name: (bundle / name).read_bytes() for name in release.ASSETS}
    if fault == "missing_evidence":
        (fake_gh / "remote/evidence.jsonl").unlink()
    elif fault == "mismatch":
        path = fake_gh / "remote/evidence.jsonl"
        path.write_text(path.read_text(encoding="utf-8").replace('"good"', '"bad"'), encoding="utf-8")
    else:
        mode(fake_gh, **{fault: 1})
    with pytest.raises(release.ReleaseError):
        release.pull(bundle)
    assert {name: (bundle / name).read_bytes() for name in release.ASSETS} == before
    assert not list(bundle.glob(".release-*"))


@pytest.mark.parametrize("fault", ["size_delta", "upload_fail"])
def test_upload_errors_are_detected(fake_gh, bundle, fault):
    mode(fake_gh, **{fault: 1})
    with pytest.raises(release.ReleaseError):
        release.push(bundle)


@pytest.mark.parametrize("fault", ["missing", "ungated", "failed", "corrupt", "wrong_evidence"])
def test_push_rejects_unpromoted_or_invalid_bundle(fake_gh, bundle, fault):
    database = bundle / "gateway.sqlite"
    if fault == "missing":
        (bundle / "evidence.jsonl").unlink()
    elif fault == "corrupt":
        database.write_bytes(b"not sqlite")
    elif fault == "wrong_evidence":
        (bundle / "evidence.jsonl").write_text('{"run_id": "other"}\n', encoding="utf-8")
    else:
        with closing(sqlite3.connect(database)) as conn, conn:
            if fault == "ungated":
                conn.execute("UPDATE run_log SET gate_results_json = '{}' ")
            else:
                conn.execute("UPDATE run_log SET status = 'failed'")
    with pytest.raises(release.ReleaseError):
        release.push(bundle)
    assert not (fake_gh / "commands.jsonl").exists()


@pytest.mark.parametrize("operation", [release.pull, release.push])
def test_stale_copy_blocks_transfers(fake_gh, bundle, operation):
    stale = bundle / "gateway.work.sqlite"
    stale.write_bytes(b"keep for inspection")
    with pytest.raises(release.StaleWorkingCopy, match="Remove-Item -LiteralPath") as caught:
        operation(bundle)
    assert str(stale) in str(caught.value)
    assert stale.read_bytes() == b"keep for inspection"
    assert not (fake_gh / "commands.jsonl").exists()


def test_missing_gh_and_timeout(monkeypatch, tmp_path):
    monkeypatch.setattr(release.shutil, "which", lambda _: None)
    with pytest.raises(release.ReleaseError, match="PATH"):
        release.pull(tmp_path)
    monkeypatch.setattr(release.shutil, "which", lambda _: "gh")

    def timeout(*args, **kwargs):
        raise subprocess.TimeoutExpired("gh", 60)

    monkeypatch.setattr(release.subprocess, "run", timeout)
    with pytest.raises(release.ReleaseError, match="TimeoutExpired"):
        release.pull(tmp_path)


def test_bundle_replacement_restores_first_file_on_second_error(tmp_path, monkeypatch):
    pairs = []
    for index in range(2):
        source, destination = tmp_path / f"new-{index}", tmp_path / f"old-{index}"
        source.write_text("new", encoding="utf-8")
        destination.write_text("old", encoding="utf-8")
        pairs.append((source, destination))
    original = release.replace_file

    def fail_second(source, destination):
        if source == pairs[1][0]:
            raise OSError("disk full")
        original(source, destination)

    monkeypatch.setattr(release, "replace_file", fail_second)
    with pytest.raises(OSError):
        release.replace_bundle(pairs, tmp_path)
    assert [path.read_text(encoding="utf-8") for _, path in pairs] == ["old", "old"]

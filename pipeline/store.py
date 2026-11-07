"""SQLite working-copy storage with gated atomic promotion and rename history.

Only one writer may own gateway.work.sqlite in a state directory. A stale
working file is deliberately preserved and must be inspected or removed by its
owner before retrying. The canonical database is opened read-only for backup;
every mutation, including migrations, happens in the working copy.
"""

from __future__ import annotations

import json
import math
import sqlite3
from collections.abc import Mapping
from datetime import UTC, datetime, timedelta
from pathlib import Path
from types import TracebackType
from typing import Literal, Self

from pydantic import JsonValue

from pipeline.migrations import migrate
from pipeline.models import RepoRecord, Score, Snapshot


class PromotionError(RuntimeError):
    """A working database cannot replace the last successful state."""


def _timestamp(value: datetime) -> str:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("State timestamps must include a time zone")
    return value.astimezone(UTC).isoformat(timespec="microseconds")


class StateStore:
    """Own a disposable working copy; context exit rolls back unless promoted."""

    def __init__(self, state_dir: Path = Path("state")) -> None:
        self.state_dir = Path(state_dir)
        self.canonical_path = self.state_dir / "gateway.sqlite"
        self.work_path = self.state_dir / "gateway.work.sqlite"
        self._connection: sqlite3.Connection | None = None
        self._owns_work = False
        self.state_dir.mkdir(parents=True, exist_ok=True)
        # Exclusive creation prevents a second writer from deleting our copy.
        with self.work_path.open("xb"):
            self._owns_work = True
        try:
            self._connection = sqlite3.connect(self.work_path)
            if self.canonical_path.exists():
                source = sqlite3.connect(self.canonical_path.resolve().as_uri() + "?mode=ro", uri=True)
                try:
                    source.backup(self._connection)
                finally:
                    source.close()
            self._connection.execute("PRAGMA journal_mode = DELETE")
            self._connection.execute("PRAGMA foreign_keys = ON")
            self._connection.row_factory = sqlite3.Row
            migrate(self._connection)
        except BaseException:
            self.rollback()
            raise

    @property
    def connection(self) -> sqlite3.Connection:
        """Return the active working connection, never the canonical database."""
        if self._connection is None:
            raise RuntimeError("State store is closed")
        return self._connection

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self, exc_type: type[BaseException] | None, exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.rollback()

    def upsert_repo(self, repo: RepoRecord, *, observed_at: datetime) -> None:
        """Update by stable identifier, preserving first sighting and past names."""
        timestamp = _timestamp(observed_at)
        with self.connection:
            old = self.connection.execute(
                "SELECT full_name, renamed_from FROM repos WHERE github_id = ?", (repo.github_id,)
            ).fetchone()
            history = json.loads(old["renamed_from"]) if old else []
            if old and old["full_name"] != repo.full_name:
                history.append(old["full_name"])
            self.connection.execute("""
                INSERT INTO repos VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(github_id) DO UPDATE SET
                    full_name = excluded.full_name, renamed_from = excluded.renamed_from,
                    metadata_json = excluded.metadata_json, readme_sha = excluded.readme_sha,
                    last_seen = excluded.last_seen
                """, (repo.github_id, repo.full_name, json.dumps(history), repo.model_dump_json(),
                      repo.readme_sha, timestamp, timestamp))

    def get_repo(self, github_id: str) -> RepoRecord | None:
        """Read the latest validated metadata for a stable identifier."""
        row = self.connection.execute(
            "SELECT metadata_json FROM repos WHERE github_id = ?", (github_id,)
        ).fetchone()
        return RepoRecord.model_validate_json(row[0]) if row else None

    def rename_history(self, github_id: str) -> list[str]:
        """Return previous names in observation order."""
        row = self.connection.execute(
            "SELECT renamed_from FROM repos WHERE github_id = ?", (github_id,)
        ).fetchone()
        return json.loads(row[0]) if row else []

    def add_snapshot(self, snapshot: Snapshot) -> None:
        """Insert or replace this repo's observation for the same run."""
        with self.connection:
            self.connection.execute("""
                INSERT INTO snapshots VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(repo_id, run_id) DO UPDATE SET
                    observed_at = excluded.observed_at, stars = excluded.stars,
                    forks = excluded.forks, open_issues = excluded.open_issues,
                    pushed_at = excluded.pushed_at
                """, (snapshot.repo_id, snapshot.run_id, _timestamp(snapshot.observed_at),
                      snapshot.stars, snapshot.forks, snapshot.open_issues,
                      _timestamp(snapshot.pushed_at) if snapshot.pushed_at else None))

    def add_score(self, score: Score) -> None:
        """Store one result per repository, run and scoring version."""
        with self.connection:
            self.connection.execute("""
                INSERT INTO scores VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(repo_id, run_id, score_version) DO UPDATE SET
                    components_json = excluded.components_json,
                    coverage = excluded.coverage, total = excluded.total
                """, (score.repo_id, score.run_id, score.score_version,
                      json.dumps(score.components, allow_nan=False), score.coverage, score.total))

    def start_run(self, run_id: str, *, started_at: datetime, budgets: Mapping[str, JsonValue]) -> None:
        """Record the start and budget counters of a run in the working copy."""
        if not run_id:
            raise ValueError("run_id must not be empty")
        with self.connection:
            self.connection.execute(
                "INSERT INTO run_log (run_id, started, status, budgets_json) VALUES (?, ?, 'running', ?)",
                (run_id, _timestamp(started_at), json.dumps(dict(budgets), allow_nan=False)),
            )

    def finish_run(
        self, run_id: str, *, finished_at: datetime, status: Literal["succeeded", "failed"],
        budgets: Mapping[str, JsonValue], rows_in: int, rows_out: int,
        gate_results: Mapping[str, bool],
    ) -> None:
        """Persist completion, counts and gates; rollback discards failed-run logs."""
        if status not in {"succeeded", "failed"} or rows_in < 0 or rows_out < 0:
            raise ValueError("Invalid run status or row count")
        with self.connection:
            cursor = self.connection.execute("""
                UPDATE run_log SET finished = ?, status = ?, budgets_json = ?,
                    rows_in = ?, rows_out = ?, gate_results_json = ? WHERE run_id = ?
                """, (_timestamp(finished_at), status, json.dumps(dict(budgets), allow_nan=False),
                      rows_in, rows_out, json.dumps(dict(gate_results)), run_id))
            if cursor.rowcount != 1:
                raise KeyError(f"Unknown run: {run_id}")

    def velocity(self, repo_id: str, window_hours: float) -> float | None:
        """Return stars per elapsed hour within a window ending at the latest observation.

        Use the earliest and latest distinct timestamps inside that window.
        Fewer than two such observations gives None; falling counts are negative.
        """
        if not math.isfinite(window_hours) or window_hours <= 0:
            raise ValueError("window_hours must be finite and positive")
        latest = self.connection.execute(
            "SELECT observed_at, stars FROM snapshots WHERE repo_id = ? ORDER BY observed_at DESC LIMIT 1",
            (repo_id,),
        ).fetchone()
        if latest is None:
            return None
        end = datetime.fromisoformat(latest["observed_at"])
        start = _timestamp(end - timedelta(hours=window_hours))
        earliest = self.connection.execute("""
            SELECT observed_at, stars FROM snapshots
            WHERE repo_id = ? AND observed_at >= ? AND observed_at < ?
            ORDER BY observed_at LIMIT 1
            """, (repo_id, start, latest["observed_at"])).fetchone()
        if earliest is None:
            return None
        elapsed_hours = (end - datetime.fromisoformat(earliest["observed_at"])).total_seconds() / 3600
        return (latest["stars"] - earliest["stars"]) / elapsed_hours

    def promote(self, gate_results: Mapping[str, bool]) -> None:
        """Atomically replace canonical state only after explicit gates and integrity checks."""
        if not gate_results or any(result is not True for result in gate_results.values()):
            self.rollback()
            raise PromotionError("Promotion requires non-empty, passing gate results")
        connection = self.connection
        if connection.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
            self.rollback()
            raise PromotionError("SQLite integrity check failed")
        if connection.execute("PRAGMA foreign_key_check").fetchone() is not None:
            self.rollback()
            raise PromotionError("SQLite foreign key check failed")
        connection.commit()
        connection.close()
        self._connection = None
        self.work_path.replace(self.canonical_path)
        self._owns_work = False

    def rollback(self) -> None:
        """Close and discard only this instance's working file; safe to call twice."""
        if self._connection is not None:
            self._connection.close()
            self._connection = None
        if self._owns_work:
            self.work_path.unlink(missing_ok=True)
            self._owns_work = False

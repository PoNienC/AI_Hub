"""Exercise SQLite history, elapsed-time velocity and canonical-file safety."""

import json
import sqlite3
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

from pipeline.models import Snapshot
from pipeline.store import PromotionError, StateStore

START = datetime(2026, 11, 7, tzinfo=UTC)


def snapshot(repo, run_id="run_1", *, hours=0, stars=100):
    return Snapshot(repo_id=repo.github_id, run_id=run_id, observed_at=START + timedelta(hours=hours),
                    stars=stars, forks=repo.forks, open_issues=repo.open_issues, pushed_at=repo.pushed_at)


def seed_store(tmp_path, repo):
    with StateStore(tmp_path) as store:
        store.upsert_repo(repo, observed_at=START)
        store.add_snapshot(snapshot(repo))
        store.promote({"schema": True, "quality": True})
    return (tmp_path / "gateway.sqlite").read_bytes()


def test_fresh_schema_and_reopen(tmp_path, repo):
    seed_store(tmp_path, repo)
    assert not (tmp_path / "gateway.work.sqlite").exists()
    with StateStore(tmp_path) as store:
        assert store.connection.execute("SELECT version FROM schema_version").fetchone()[0] == 1
        assert store.get_repo(repo.github_id) == repo
        assert store.get_repo("missing") is None


def test_upsert_and_rename_keep_identity_and_history(tmp_path, repo):
    with StateStore(tmp_path) as store:
        store.upsert_repo(repo, observed_at=START)
        store.add_snapshot(snapshot(repo))
        store.upsert_repo(repo, observed_at=START + timedelta(hours=1))
        renamed = repo.model_copy(update={"full_name": "example/renamed", "readme_sha": "new-sha"})
        store.upsert_repo(renamed, observed_at=START + timedelta(hours=2))
        store.upsert_repo(renamed, observed_at=START + timedelta(hours=3))
        assert store.connection.execute("SELECT count(*) FROM repos").fetchone()[0] == 1
        assert store.get_repo(repo.github_id) == renamed
        assert store.rename_history(repo.github_id) == [repo.full_name]
        assert store.rename_history("missing") == []
        row = store.connection.execute("SELECT * FROM repos").fetchone()
        assert datetime.fromisoformat(row["first_seen"]) == START
        assert datetime.fromisoformat(row["last_seen"]) == START + timedelta(hours=3)
        assert row["readme_sha"] == "new-sha"
        assert store.connection.execute("SELECT repo_id FROM snapshots").fetchone()[0] == repo.github_id


@pytest.mark.parametrize("stars,expected", [(115, 2), (85, -2), (100, 0)])
def test_velocity_actual_elapsed_hours(tmp_path, repo, stars, expected):
    with StateStore(tmp_path) as store:
        store.upsert_repo(repo, observed_at=START)
        assert store.velocity(repo.github_id, 24) is None
        store.add_snapshot(snapshot(repo))
        assert store.velocity(repo.github_id, 24) is None
        store.add_snapshot(snapshot(repo, "run_2", hours=7.5, stars=stars))
        assert store.velocity(repo.github_id, 24) == pytest.approx(expected)
        assert store.velocity(repo.github_id, 7) is None


def test_window_boundary_duplicate_time_and_same_run(tmp_path, repo):
    with StateStore(tmp_path) as store:
        store.upsert_repo(repo, observed_at=START)
        store.add_snapshot(snapshot(repo))
        store.add_snapshot(snapshot(repo, "same_time"))
        assert store.velocity(repo.github_id, 24) is None
        store.add_snapshot(snapshot(repo, "run_2", hours=6, stars=106))
        store.add_snapshot(snapshot(repo, "run_2", hours=6, stars=112))
        assert store.velocity(repo.github_id, 6) == 2
        assert store.connection.execute("SELECT count(*) FROM snapshots").fetchone()[0] == 3


@pytest.mark.parametrize("window", [0, -1, float("nan"), float("inf")])
def test_invalid_velocity_window(tmp_path, window):
    with StateStore(tmp_path) as store, pytest.raises(ValueError, match="window_hours"):
        store.velocity("missing", window)


@pytest.mark.parametrize("gates", [{}, {"schema": False}, {"schema": True, "quality": False}, {"schema": 1}])
def test_failed_gates_preserve_canonical_bytes(tmp_path, repo, gates):
    original = seed_store(tmp_path, repo)
    with StateStore(tmp_path) as store:
        store.upsert_repo(repo.model_copy(update={"stars": 150}), observed_at=START)
        with pytest.raises(PromotionError):
            store.promote(gates)
    assert (tmp_path / "gateway.sqlite").read_bytes() == original
    assert not (tmp_path / "gateway.work.sqlite").exists()


def test_exception_and_explicit_rollback_preserve_canonical_bytes(tmp_path, repo):
    original = seed_store(tmp_path, repo)
    with pytest.raises(RuntimeError, match="run failed"), StateStore(tmp_path) as store:
        store.upsert_repo(repo.model_copy(update={"stars": 150}), observed_at=START)
        raise RuntimeError("run failed")
    with StateStore(tmp_path) as store:
        store.rollback()
        store.rollback()
        with pytest.raises(RuntimeError, match="closed"):
            store.get_repo(repo.github_id)
    assert (tmp_path / "gateway.sqlite").read_bytes() == original


def test_first_run_rollback_never_creates_canonical(tmp_path):
    with StateStore(tmp_path):
        pass
    assert not (tmp_path / "gateway.sqlite").exists()
    assert not (tmp_path / "gateway.work.sqlite").exists()


def test_successful_promotion_replaces_previous_state(tmp_path, repo):
    original = seed_store(tmp_path, repo)
    with StateStore(tmp_path) as store:
        store.upsert_repo(repo.model_copy(update={"stars": 150}), observed_at=START)
        store.promote({"quality": True})
    assert (tmp_path / "gateway.sqlite").read_bytes() != original
    with StateStore(tmp_path) as store:
        assert store.get_repo(repo.github_id).stars == 150


def test_second_writer_preserves_active_work(tmp_path, repo):
    with StateStore(tmp_path) as store:
        store.upsert_repo(repo, observed_at=START)
        before = store.work_path.read_bytes()
        with pytest.raises(FileExistsError):
            StateStore(tmp_path)
        assert store.work_path.read_bytes() == before


def test_unsupported_schema_does_not_touch_canonical(tmp_path, repo):
    seed_store(tmp_path, repo)
    connection = sqlite3.connect(tmp_path / "gateway.sqlite")
    with connection:
        connection.execute("UPDATE schema_version SET version = 999")
    connection.close()
    before = (tmp_path / "gateway.sqlite").read_bytes()
    with pytest.raises(ValueError, match="Unsupported state schema"):
        StateStore(tmp_path)
    assert (tmp_path / "gateway.sqlite").read_bytes() == before
    assert not (tmp_path / "gateway.work.sqlite").exists()


def test_failed_replace_preserves_canonical(tmp_path, repo, monkeypatch):
    original = seed_store(tmp_path, repo)

    def fail_replace(self, target):
        raise PermissionError("simulated file lock")

    with StateStore(tmp_path) as store:
        monkeypatch.setattr(Path, "replace", fail_replace)
        with pytest.raises(PermissionError, match="file lock"):
            store.promote({"schema": True})
    assert (tmp_path / "gateway.sqlite").read_bytes() == original
    assert not (tmp_path / "gateway.work.sqlite").exists()


def test_scores_and_run_log(tmp_path, repo, score):
    with StateStore(tmp_path) as store:
        store.upsert_repo(repo, observed_at=START)
        store.add_score(score)
        store.add_score(score.model_copy(update={"total": 80, "components": {"licence": 100}}))
        stored = store.connection.execute("SELECT * FROM scores").fetchall()
        assert len(stored) == 1 and stored[0]["total"] == 80
        assert json.loads(stored[0]["components_json"]) == {"licence": 100}
        store.start_run("run_1", started_at=START, budgets={"github": 0})
        store.finish_run("run_1", finished_at=START + timedelta(minutes=1), status="succeeded",
                         budgets={"github": 12}, rows_in=2, rows_out=1, gate_results={"schema": True})
        row = store.connection.execute("SELECT * FROM run_log").fetchone()
        assert row["status"] == "succeeded" and row["rows_out"] == 1
        assert json.loads(row["budgets_json"]) == {"github": 12}
        assert json.loads(row["gate_results_json"]) == {"schema": True}
        assert datetime.fromisoformat(row["finished"]) > datetime.fromisoformat(row["started"])


def test_run_log_and_timestamp_validation(tmp_path, repo):
    with StateStore(tmp_path) as store:
        with pytest.raises(ValueError, match="time zone"):
            store.upsert_repo(repo, observed_at=datetime(2026, 11, 7))
        with pytest.raises(ValueError, match="run_id"):
            store.start_run("", started_at=START, budgets={})
        kwargs = {"finished_at": START, "budgets": {}, "rows_in": 0, "rows_out": 0, "gate_results": {}}
        with pytest.raises(ValueError, match="status"):
            store.finish_run("unknown", status="bad", **kwargs)
        with pytest.raises(KeyError, match="Unknown run"):
            store.finish_run("unknown", status="failed", **kwargs)


def test_foreign_keys_are_enforced(tmp_path, repo):
    with StateStore(tmp_path) as store, pytest.raises(sqlite3.IntegrityError):
        store.add_snapshot(snapshot(repo))


def test_promotion_rejects_foreign_key_corruption(tmp_path, repo):
    original = seed_store(tmp_path, repo)
    with StateStore(tmp_path) as store:
        store.connection.execute("PRAGMA foreign_keys = OFF")
        store.add_snapshot(snapshot(repo.model_copy(update={"github_id": "missing"}), "bad"))
        with pytest.raises(PromotionError, match="foreign key"):
            store.promote({"schema": True})
    assert (tmp_path / "gateway.sqlite").read_bytes() == original

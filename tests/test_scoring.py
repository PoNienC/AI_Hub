"""Scoring policy tests independent of live services and wall-clock time."""

from datetime import UTC, datetime, timedelta

import pytest

from pipeline.models import Evidence
from pipeline.scoring import score_repo
from pipeline.store import StateStore

NOW = datetime(2026, 11, 7, tzinfo=UTC)


def evidence(repo, source, data=None, status="present"):
    return Evidence(repo_id=repo.github_id, source=source, status=status,
                    fetched_at=NOW, data={} if data is None else data)


@pytest.mark.parametrize("scorecard,count,contributors,age", [
    (0, 10000, 0, 1000), (10, 0, 100000, 0), (5, 2, 4, 20), (8.5, 1, 1, 365),
])
def test_bounds_and_fully_evaluated_weights(repo, scorecard, count, contributors, age):
    repo = repo.model_copy(update={
        "created_at": NOW - timedelta(days=2000), "licence_spdx": "MIT",
        "pushed_at": NOW - timedelta(days=age), "contributor_count": contributors,
        "release_published_at": NOW - timedelta(days=age),
    })
    result = score_repo(repo, [
        evidence(repo, "scorecard", {"score": scorecard}),
        evidence(repo, "deps_dev", {"advisories_status": "present", "advisory_count": count}),
        evidence(repo, "hacker_news", {"mention_count": count}),
    ], run_id="run", now=NOW, release_history=[repo.release_published_at - timedelta(days=30)])
    assert 0 <= result.score.total <= 100
    assert result.score.coverage == 1
    assert result.score.components["stars"] is None
    assert result.score.components["velocity"] is None
    assert result.details.failed_components == []


def test_weighted_mean_known_values(repo):
    repo = repo.model_copy(update={"licence_spdx": "MIT", "contributor_count": 2})
    result = score_repo(repo, [evidence(repo, "scorecard", {"score": 8})], run_id="run", now=NOW)
    assert result.score.coverage == pytest.approx(0.5)
    assert result.score.total == pytest.approx((0.25 * 80 + 0.15 * 100 + 0.10 * 20) / 0.5)


@pytest.mark.parametrize("status", ["absent", "unsupported", "failed"])
def test_missing_components_excluded_and_failures_flagged(repo, status):
    result = score_repo(repo, [
        evidence(repo, "scorecard", {"score": 8}),
        evidence(repo, "deps_dev", {"advisory_count": 0}, status),
        evidence(repo, "hacker_news", {"mention_count": 5}, status),
    ], run_id="run", now=NOW)
    assert result.score.total == 80 and result.score.coverage == 0.25
    assert result.details.failed_components == (["advisories", "hacker_news"] if status == "failed" else [])


def test_all_absent_null_and_present_zero_evaluated(repo):
    absent = score_repo(repo, [], run_id="run", now=NOW)
    assert absent.score.total is None and absent.score.coverage == 0
    zero = score_repo(repo, [evidence(repo, "scorecard", {"score": 0})], run_id="run", now=NOW)
    assert zero.score.total == 0 and zero.score.coverage == 0.25


def test_stars_and_velocity_cannot_change_scores(repo):
    evidence_list = [evidence(repo, "scorecard", {"score": 8})]
    low = score_repo(repo.model_copy(update={"stars": 0}), evidence_list,
                     run_id="run", now=NOW, velocity=-100)
    high = score_repo(repo.model_copy(update={"stars": 1000000}), evidence_list,
                      run_id="run", now=NOW, velocity=1000000)
    assert low.score == high.score
    assert low.details.velocity == -100 and high.details.stars == 1000000


@pytest.mark.parametrize("spdx,total,status,licence_class", [
    ("MIT", 100, "present", "permissive"),
    ("MPL-2.0", 80, "present", "weak_copyleft"),
    ("GPL-3.0-only", 60, "present", "strong_copyleft"),
    ("custom", None, "unsupported", "unknown"),
    ("MIT OR custom", None, "unsupported", "unknown"),
    ("NOASSERTION", None, "absent", "absent"),
    (None, None, "absent", "absent"),
])
def test_licence_classes(repo, spdx, total, status, licence_class):
    result = score_repo(repo.model_copy(update={"licence_spdx": spdx}), [], run_id="run", now=NOW)
    assert result.score.total == total
    assert result.details.component_statuses["licence"] == status
    assert result.details.licence_class == licence_class


def test_single_release_is_not_cadence(repo):
    repo = repo.model_copy(update={"release_published_at": NOW})
    result = score_repo(repo, [], run_id="run", now=NOW, release_history=[NOW, NOW])
    assert result.details.component_statuses["release_cadence"] == "unsupported"
    assert result.score.total is None
    actual = score_repo(repo, [], run_id="run", now=NOW, release_history=[NOW - timedelta(days=60)])
    assert actual.score.total == 50 and actual.score.coverage == 0.1


def test_stale_release_cannot_get_perfect_cadence(repo):
    repo = repo.model_copy(update={"release_published_at": NOW - timedelta(days=400)})
    result = score_repo(repo, [], run_id="run", now=NOW,
                        release_history=[NOW - timedelta(days=430)])
    assert result.score.components["release_cadence"] == 0


def test_future_dates_flagged(repo):
    future = NOW + timedelta(days=1)
    repo = repo.model_copy(update={"pushed_at": future, "release_published_at": future})
    item = evidence(repo, "scorecard", {"score": 10}).model_copy(update={"fetched_at": future})
    result = score_repo(repo, [item], run_id="run", now=NOW)
    assert set(result.details.failed_components) == {"scorecard", "maintenance", "release_cadence"}
    assert result.score.total is None


@pytest.mark.parametrize("source,data", [
    ("scorecard", {"score": 11}), ("scorecard", {"score": True}),
    ("scorecard", {}), ("hacker_news", {"mention_count": -1}),
    ("deps_dev", {"advisories_status": "present"}),
    ("deps_dev", {"advisories_status": "present", "advisory_count": "0"}),
    ("deps_dev", {"advisories_status": "invalid"}),
])
def test_malformed_present_component_fails(repo, source, data):
    result = score_repo(repo, [evidence(repo, source, data)], run_id="run", now=NOW)
    assert result.score.total is None and len(result.details.failed_components) == 1


def test_project_presence_never_means_zero_advisories(repo):
    result = score_repo(repo, [evidence(repo, "deps_dev", {"project": {"projectKey": {"id": "x"}}})],
                        run_id="run", now=NOW)
    assert result.details.component_statuses["advisories"] == "unsupported"
    assert result.score.total is None and result.score.coverage == 0


def test_identity_and_duplicate_source_rejected(repo):
    item = evidence(repo, "scorecard", {"score": 8})
    with pytest.raises(ValueError, match="Duplicate"):
        score_repo(repo, [item, item], run_id="run", now=NOW)
    with pytest.raises(ValueError, match="different repository"):
        score_repo(repo, [item.model_copy(update={"repo_id": "another"})], run_id="run", now=NOW)


@pytest.mark.parametrize("velocity", [float("nan"), float("inf"), True])
def test_invalid_velocity_rejected(repo, velocity):
    with pytest.raises(ValueError, match="Velocity"):
        score_repo(repo, [], run_id="run", now=NOW, velocity=velocity)


def test_b1_store_accepts_score_unchanged(repo, tmp_path):
    result = score_repo(repo, [evidence(repo, "scorecard", {"score": 8})], run_id="run", now=NOW)
    with StateStore(tmp_path) as store:
        store.upsert_repo(repo, observed_at=NOW)
        store.start_run("run", started_at=NOW, budgets={})
        store.add_score(result.score)
        row = store.connection.execute("SELECT total, coverage FROM scores").fetchone()
        assert tuple(row) == (80, 0.25)

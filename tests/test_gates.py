"""Offline publication gates and rollback regression checks."""

import json
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

from pipeline.budgets import BudgetExceeded
from pipeline.export import build_listings, write_listings
from pipeline.failure import RunFailure, abort_run
from pipeline.gates import GateFailure, check_gates, gate_2, gate_3, gate_5
from pipeline.scoring import score_repo
from pipeline.site.builder import build
from pipeline.store import StateStore

NOW = datetime(2026, 11, 7, 12, tzinfo=UTC)


@pytest.fixture
def publication(repo, tmp_path):
    labels = tmp_path / "labels.csv"
    labels.write_text("full_name,topic,level\n", encoding="utf-8")
    repo = repo.model_copy(update={"licence_spdx": "MIT"})
    result = score_repo(repo, [], run_id="gate_run", now=NOW)
    return build_listings([repo], [result], run_id="gate_run", generated_at=NOW, labels_path=labels)


def test_gate_2_validates_published_listing(publication, tmp_path):
    path = write_listings(publication, tmp_path / "listings.json")
    assert gate_2(path).listings[0].coverage == publication.listings[0].score.coverage
    assert check_gates(path, now=NOW) == {"gate_2": True, "gate_3": True}


@pytest.mark.parametrize("field,value", [
    ("topic", "invented"), ("level", "expert"), ("coverage", 0.99),
    ("tested", "passed"), ("tested", None), ("score", None),
])
def test_gate_2_rejects_bad_rows(publication, tmp_path, field, value):
    data = publication.model_dump(mode="json")
    data["listings"][0][field] = value
    path = tmp_path / "listings.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(GateFailure, match="gate_2"):
        gate_2(path)


@pytest.mark.parametrize("missing", ["coverage", "score", "tested", "licence_class"])
def test_gate_2_rejects_missing_required_fields(publication, tmp_path, missing):
    data = publication.model_dump(mode="json")
    row = data["scoring_details"]["R_1"] if missing == "licence_class" else data["listings"][0]
    del row[missing]
    path = tmp_path / "listings.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(GateFailure, match="gate_2"):
        gate_2(path)


@pytest.mark.parametrize("content", [None, "{invalid json}", "[]"])
def test_gate_2_unreadable_or_invalid_file(tmp_path, content):
    path = tmp_path / "listings.json"
    if content is not None:
        path.write_text(content, encoding="utf-8")
    with pytest.raises(GateFailure, match="gate_2"):
        gate_2(path)


@pytest.mark.parametrize("age,passes", [
    (timedelta(0), True), (timedelta(hours=7), True),
    (timedelta(hours=7, microseconds=1), False), (timedelta(seconds=-1), False),
])
def test_freshness(publication, age, passes):
    publication.generated_at = NOW - age
    if passes:
        gate_3(publication, now=NOW)
    else:
        with pytest.raises(GateFailure, match="freshness"):
            gate_3(publication, now=NOW)


@pytest.mark.parametrize("count,previous,passes", [
    (0, None, True), (0, 0, True), (9, 10, True), (8, 10, False),
    (1, 2, False), (10, 10, True), (11, 10, True),
])
def test_count_rule(publication, count, previous, passes):
    publication.listings *= count
    if passes:
        gate_3(publication, now=NOW, previous_count=previous)
    else:
        with pytest.raises(GateFailure, match="count"):
            gate_3(publication, now=NOW, previous_count=previous)


@pytest.mark.parametrize("previous", [-1, 1.5, True])
def test_invalid_count_baseline(publication, previous):
    with pytest.raises(ValueError, match="previous_count"):
        gate_3(publication, now=NOW, previous_count=previous)


@pytest.mark.parametrize("rule", ["score", "licence", "tested", "labels"])
@pytest.mark.parametrize("passes", [True, False])
def test_row_quality_rules(publication, rule, passes):
    row = publication.listings[0]
    if rule == "labels":
        row.topic = "coding_agent" if passes else None
        row.level = "beginner" if passes else None
    elif not passes and rule == "score":
        row.score.total = None
    elif not passes and rule == "licence":
        publication.scoring_details[row.repo.github_id].licence_class = None
    elif not passes:
        row.tested = "passed"
    if passes:
        gate_3(publication, now=NOW, require_labels=rule == "labels")
    else:
        with pytest.raises(GateFailure, match=rule):
            gate_3(publication, now=NOW, require_labels=rule == "labels")


def test_default_label_switch(publication, monkeypatch):
    gate_3(publication, now=NOW)
    monkeypatch.setattr("pipeline.gates.REQUIRE_LABELS", True)
    with pytest.raises(GateFailure, match="labels"):
        gate_3(publication, now=NOW)


@pytest.mark.parametrize("error,step", [
    (GateFailure("gate_2", "schema", "invalid row"), "gate_2"),
    (GateFailure("gate_3", "count", "too few rows"), "gate_3"),
    (BudgetExceeded("github_points", 2500, 2501), "budget.github_points"),
    (ValueError("secret payload"), "export"),
])
def test_abort_preserves_canonical_and_uses_one_record(tmp_path, repo, error, step):
    with StateStore(tmp_path) as store:
        store.upsert_repo(repo, observed_at=NOW)
        store.promote({"seed": True})
    before = (tmp_path / "gateway.sqlite").read_bytes()
    with StateStore(tmp_path) as store:
        store.upsert_repo(repo.model_copy(update={"stars": 999}), observed_at=NOW)
        failure = abort_run(
            error, store=store, stage="export", run_id="failed_run", started=NOW,
            finished=NOW + timedelta(seconds=1), rows_in=10, rows_out=8,
            previous_count=10, log_path="state/logs/failed_run.log",
        )
    assert (tmp_path / "gateway.sqlite").read_bytes() == before
    assert not (tmp_path / "gateway.work.sqlite").exists()
    restored = RunFailure.model_validate_json(failure.model_dump_json())
    assert restored.issue_body == failure.issue_body
    assert restored.failed_step == step
    assert step in failure.issue_title
    assert "Rows in: 10" in failure.issue_body
    assert "Rows out: 8" in failure.issue_body
    assert "state/logs/failed_run.log" in failure.issue_body
    assert "secret payload" not in failure.issue_body


@pytest.fixture
def site(tmp_path):
    return build(Path(__file__).parent / "fixtures/listings_sample.json", tmp_path / "dist")


def test_gate_5_clean_site(site):
    assert gate_5(site) is None


@pytest.mark.parametrize("fault,rule,page", [
    ("link", "links", "topics/coding_agent.html"),
    ("size", "size", "repos/oversize.html"),
    ("topics", "topics", "index.html"),
    ("index", "index", "index.html"),
])
def test_gate_5_rejects_site_and_names_page(site, fault, rule, page):
    path = site / page
    if fault == "link":
        path.write_text('<a href="../missing.html">broken</a>', encoding="utf-8")
    elif fault == "size":
        path.write_text("x" * 200_001, encoding="utf-8")
    elif fault == "topics":
        path.write_text("<h1>No topics</h1>", encoding="utf-8")
    else:
        path.unlink()
    with pytest.raises(GateFailure) as caught:
        gate_5(site)
    assert (caught.value.gate, caught.value.rule) == ("gate_5", rule)
    assert page in str(caught.value)


@pytest.mark.parametrize("reference", [
    "../Index.html", "../Topics/pending.html", "../topics/Pending.html",
    "../Topics/", "../topics/index.HTML", "../topics/%50ending.html",
    "/TOPICS/pending.html",
])
def test_gate_5_rejects_case_mismatches_on_every_platform(site, reference):
    (site / "topics/index.html").write_text("<h1>Topics</h1>", encoding="utf-8")
    (site / "repos/case.html").write_text(f'<a href="{reference}">link</a>', encoding="utf-8")
    with pytest.raises(GateFailure) as caught:
        gate_5(site)
    assert (caught.value.gate, caught.value.rule) == ("gate_5", "links")
    assert "repos/case.html" in str(caught.value)
    assert reference in str(caught.value)


def test_gate_5_requires_exact_index_name(site):
    # Use an intermediate name so the rename also changes case on Windows.
    (site / "index.html").rename(site / "temporary.html")
    (site / "temporary.html").rename(site / "Index.html")
    with pytest.raises(GateFailure, match="missing index page"):
        gate_5(site)

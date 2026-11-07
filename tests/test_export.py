"""CSV joins, ranking, export validation and offline adapter-to-listing flow."""

import json
from datetime import UTC, datetime, timedelta
from pathlib import Path

import httpx
import pytest
from pydantic import ValidationError

from pipeline.budgets import Budget
from pipeline.export import (
    Listings, PublishedListing, build_listings, load_provisional_labels, write_listings,
)
from pipeline.http import HttpClient
from pipeline.models import Evidence, Listing
from pipeline.scoring import score_repo
from pipeline.sources import deps_dev, hacker_news, hugging_face, scorecard

NOW = datetime(2026, 11, 7, tzinfo=UTC)


@pytest.fixture
def labels_path(tmp_path):
    path = tmp_path / "labels.csv"
    path.write_text("full_name,topic,level,confidence\nEXAMPLE/agent,coding_agent,beginner,high\n", encoding="utf-8")
    return path


def score(repo, value=8, *, run_id="run"):
    item = Evidence(repo_id=repo.github_id, source="scorecard", status="present",
                    fetched_at=NOW, data={"score": value})
    return score_repo(repo, [item], run_id=run_id, now=NOW, velocity=-2)


def document(repos, results, labels_path):
    return build_listings(repos, results, run_id="run", generated_at=NOW, labels_path=labels_path)


def test_csv_join_is_provisional_regardless_of_confidence(repo, labels_path):
    unknown = repo.model_copy(update={"github_id": "R_2", "full_name": "unknown/agent"})
    output = document([repo, unknown], [score(repo), score(unknown)], labels_path)
    labelled, pending = output.listings
    assert (labelled.topic, labelled.level, labelled.label_status) == ("coding_agent", "beginner", "provisional")
    assert (pending.topic, pending.level, pending.label_status) == (None, None, "pending")
    assert all(row.tested == "untested" for row in output.listings)
    assert all(row.unevaluated_checks == ["fake_stars", "typosquat", "sandbox_test"] for row in output.listings)


def test_real_provisional_csv_validates():
    labels = load_provisional_labels()
    assert len(labels) == 100
    assert labels["arize-ai/phoenix"].topic == "evals_observability"


def test_ordering_differs_from_stars_and_ties_use_recency(repo, labels_path):
    # Both pushes are older than a year, giving identical maintenance components.
    newer = repo.model_copy(update={"stars": 1, "pushed_at": NOW - timedelta(days=400)})
    older = repo.model_copy(update={"github_id": "R_2", "full_name": "a/older", "stars": 10000,
                                   "pushed_at": NOW - timedelta(days=500)})
    poor = repo.model_copy(update={"github_id": "R_3", "full_name": "a/poor", "stars": 1000000})
    repos = [poor, older, newer]
    output = document(repos, [score(poor, 1), score(older), score(newer)], labels_path)
    assert [row.repo.github_id for row in output.listings] == ["R_1", "R_2", "R_3"]
    assert [row.repo.stars for row in output.listings] == [1, 10000, 1000000]
    assert output.listings[0].score.total == output.listings[1].score.total


def test_remaining_ties_are_deterministic_and_zero_is_listed(repo, labels_path):
    missing_push = repo.model_copy(update={"github_id": "R_2", "full_name": "aaa/no-push"})
    with_push = repo.model_copy(update={"pushed_at": NOW - timedelta(days=400)})
    results = [score(with_push, 0), score(missing_push, 0)]
    forward = document([missing_push, with_push], results, labels_path)
    reverse = document([with_push, missing_push], reversed(results), labels_path)
    assert forward == reverse
    assert [row.repo.github_id for row in forward.listings] == ["R_1", "R_2"]
    assert all(row.score.total == 0 for row in forward.listings)


def test_all_absent_excluded_but_diagnostics_retained(repo, labels_path):
    result = score_repo(repo, [], run_id="run", now=NOW)
    output = document([repo], [result], labels_path)
    assert output.listings == []
    assert output.scoring_details[repo.github_id].licence_class == "absent"
    assert Listings.model_validate_json(output.model_dump_json()) == output


def test_json_validity_metadata_and_b1_listing_compatibility(repo, labels_path, tmp_path):
    output = document([repo], [score(repo)], labels_path)
    path = write_listings(output, tmp_path / "site/src/data/listings.json",
                          evidence_path=tmp_path / "state/evidence.jsonl")
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["run_id"] == "run" and payload["score_version"] == "v0"
    assert payload["generated_at"] == "2026-11-07T00:00:00Z"
    assert payload["scoring_details"][repo.github_id]["velocity"] == -2
    assert Listings.model_validate(payload) == output
    row = payload["listings"][0]
    assert row["coverage"] == row["score"]["coverage"] == 0.25
    assert PublishedListing.model_validate(row) == output.listings[0]
    assert Listing.model_validate({key: value for key, value in row.items() if key != "coverage"})


def test_default_output_location(repo, labels_path, tmp_path, monkeypatch):
    output = document([repo], [score(repo)], labels_path)
    monkeypatch.chdir(tmp_path)
    assert write_listings(output) == Path("site/src/data/listings.json")
    assert Path("site/src/data/listings.json").is_file()
    assert Path("site/src/data/listings.evidence.jsonl").is_file()
    assert not Path("state/evidence.jsonl").exists()


def test_dry_output_preserves_production_evidence(repo, labels_path, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    legacy_evidence = Path("state/evidence.jsonl")
    legacy_evidence.parent.mkdir()
    legacy_evidence.write_bytes(b"previous production evidence")
    output = document([repo], [score(repo)], labels_path)
    path = write_listings(output)
    evidence_path = Path("site/src/data/listings.evidence.jsonl")
    previous_listing = path.read_bytes()
    previous_evidence = evidence_path.read_bytes()

    dry_output = build_listings(
        [repo], [score(repo, 1, run_id="dry-run")], run_id="dry-run",
        generated_at=NOW, labels_path=labels_path,
    )
    dry_path = Path("site/src/data/listings.dry.json")
    assert write_listings(dry_output, dry_path) == dry_path
    assert Listings.model_validate_json(dry_path.read_text(encoding="utf-8")) == dry_output
    dry_evidence = json.loads(Path("site/src/data/listings.dry.evidence.jsonl").read_text(encoding="utf-8"))
    assert dry_evidence["run_id"] == "dry-run"
    assert Evidence.model_validate(dry_evidence["evidence"]) == dry_output.scoring_details[repo.github_id].evidence[0]
    assert path.read_bytes() == previous_listing
    assert evidence_path.read_bytes() == previous_evidence
    assert legacy_evidence.read_bytes() == b"previous production evidence"


@pytest.mark.parametrize("csv_text", [
    "full_name,topic\nexample/agent,coding_agent\n",
    "full_name,topic,level\nexample/agent,unknown,beginner\n",
    "full_name,topic,level\nexample/agent,coding_agent,expert\n",
    "full_name,topic,level\nexample/agent,,beginner\n",
    "full_name,topic,level\ninvalid,coding_agent,beginner\n",
    "full_name,topic,level\nexample/agent,coding_agent,beginner\nExample/Agent,coding_agent,beginner\n",
])
def test_invalid_csv_fails_instead_of_inventing_labels(csv_text, labels_path):
    labels_path.write_text(csv_text, encoding="utf-8")
    with pytest.raises(ValueError):
        load_provisional_labels(labels_path)


def test_missing_csv_is_configuration_error(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_provisional_labels(tmp_path / "missing.csv")


@pytest.mark.parametrize("mode", ["duplicate_score", "duplicate_repo", "missing", "orphan", "wrong_run"])
def test_join_integrity(repo, labels_path, mode):
    result = score(repo)
    repos, results = [repo], [result]
    if mode == "duplicate_score":
        results.append(result)
    elif mode == "duplicate_repo":
        repos.append(repo)
    elif mode == "missing":
        results = []
    elif mode == "orphan":
        repos = []
    else:
        results = [score(repo, run_id="other")]
    with pytest.raises(ValueError):
        document(repos, results, labels_path)


@pytest.mark.parametrize("mode", [
    "repo_id", "run_id", "null_score", "coverage", "label", "tested", "duplicate",
    "details", "stars", "statuses", "failure_flags", "evidence", "version",
    "row_coverage", "missing_coverage",
])
def test_export_schema_rejects_inconsistent_rows(repo, labels_path, mode):
    data = document([repo], [score(repo)], labels_path).model_dump(mode="json")
    row = data["listings"][0]
    details = data["scoring_details"][repo.github_id]
    if mode in {"repo_id", "run_id"}:
        row["score"][mode] = "other"
    elif mode == "null_score":
        row["score"]["total"] = None
    elif mode == "coverage":
        row["coverage"] = 0
        row["score"]["coverage"] = 0
    elif mode == "row_coverage":
        row["coverage"] = 0.7
    elif mode == "missing_coverage":
        del row["coverage"]
    elif mode == "label":
        row["topic"] = "invalid"
    elif mode == "tested":
        row["tested"] = "tested"
    elif mode == "duplicate":
        data["listings"].append(row)
    elif mode == "details":
        data["scoring_details"] = {}
    elif mode == "stars":
        details["stars"] = 999
    elif mode == "statuses":
        details["component_statuses"]["scorecard"] = "absent"
    elif mode == "failure_flags":
        details["failed_components"] = ["scorecard"]
    elif mode == "evidence":
        details["evidence"][0]["repo_id"] = "other"
    else:
        data["score_version"] = "v999"
    match = "Published listings require evaluated scores" if mode == "coverage" else None
    with pytest.raises(ValidationError, match=match):
        Listings.model_validate(data)


def test_validation_failure_preserves_existing_output(repo, labels_path, tmp_path):
    output = document([repo], [score(repo)], labels_path)
    path = tmp_path / "listings.json"
    path.write_bytes(b"previous good export")
    output.listings[0].level = "invalid"
    with pytest.raises(ValidationError):
        write_listings(output, path, evidence_path=tmp_path / "evidence.jsonl")
    assert path.read_bytes() == b"previous good export"
    assert not (tmp_path / "evidence.jsonl").exists()


def test_replace_failure_preserves_output_and_removes_temp(repo, labels_path, tmp_path, monkeypatch):
    output = document([repo], [score(repo)], labels_path)
    path = tmp_path / "listings.json"
    path.write_bytes(b"previous good export")

    original_replace = Path.replace

    def fail_replace(self, target):
        if target == path:
            raise OSError("simulated replacement failure")
        return original_replace(self, target)

    monkeypatch.setattr(Path, "replace", fail_replace)
    with pytest.raises(OSError, match="simulated"):
        write_listings(output, path, evidence_path=tmp_path / "evidence.jsonl")
    assert path.read_bytes() == b"previous good export"
    assert list(tmp_path.glob(".listings.json.*.tmp")) == []


def test_adapters_to_scoring_to_export_offline(repo, load_fixture, labels_path, tmp_path):
    fixtures = load_fixture("enrichment_responses.json")
    by_host = {"api.deps.dev": "deps_dev", "api.scorecard.dev": "scorecard",
               "huggingface.co": "hugging_face", "hn.algolia.com": "hacker_news"}

    def handler(request):
        payload = fixtures[by_host[request.url.host]]["present"]["body"]
        return httpx.Response(200, json=payload)

    budget = Budget()
    with httpx.Client(transport=httpx.MockTransport(handler)) as client:
        http = HttpClient(budget, client=client, retries=0)
        evidence = [adapter.fetch(repo, http, fetched_at=NOW)
                    for adapter in [deps_dev, scorecard, hugging_face, hacker_news]]
    result = score_repo(repo, evidence, run_id="run", now=NOW)
    assert result.score.coverage == pytest.approx(0.3)
    assert result.score.total == pytest.approx((78 * 0.25 + 40 * 0.05) / 0.3)
    assert result.details.component_statuses["advisories"] == "unsupported"
    output = document([repo], [result], labels_path)
    evidence_path = tmp_path / "state/evidence.jsonl"
    path = write_listings(output, tmp_path / "listings.json", evidence_path=evidence_path)
    restored = Listings.model_validate_json(path.read_text(encoding="utf-8"))
    summaries = {item.source: item for item in restored.scoring_details[repo.github_id].evidence}
    assert summaries["scorecard"].data == {"score": 7.8, "date": "2026-11-01"}
    assert summaries["deps_dev"].data == {"advisory_count": None, "advisories_status": "unsupported"}
    assert summaries["hacker_news"].data["mention_count"] == 2
    assert summaries["hacker_news"].data["top_item"]["id"] == "1002"
    assert summaries["hugging_face"].data["link_count"] == 2
    records = [json.loads(line) for line in evidence_path.read_text(encoding="utf-8").splitlines()]
    assert [Evidence.model_validate(record["evidence"]) for record in records] == evidence
    assert all(record["run_id"] == "run" and record["score_version"] == "v0" for record in records)
    assert all(budget.http_calls[name] == 1 for name in by_host.values())


@pytest.mark.parametrize("status", ["present", "absent", "unsupported", "failed"])
def test_site_row_size_is_bounded_and_full_evidence_is_retained(
    repo, load_fixture, labels_path, tmp_path, status,
):
    repo = repo.model_copy(update={"licence_spdx": "MIT"})
    fixtures = load_fixture("enrichment_responses.json")
    large_text = "診斷 evidence " * 10000
    items = [
        Evidence(repo_id=repo.github_id, source="scorecard", status=status, fetched_at=NOW,
                 data=fixtures["scorecard"]["present"]["body"] | {"checks": [large_text] * 10}),
        Evidence(repo_id=repo.github_id, source="deps_dev", status=status, fetched_at=NOW,
                 data={"project": {"readme": large_text}, "advisories_status": "unsupported",
                       "advisory_count": None}),
        Evidence(repo_id=repo.github_id, source="hacker_news", status=status, fetched_at=NOW,
                 data={"mention_count": 2, "top_item": {"id": "1002", "title": large_text,
                       "discussion_url": "https://news.ycombinator.com/item?id=1002",
                       "unexpected": large_text}}),
        Evidence(repo_id=repo.github_id, source="hugging_face", status=status, fetched_at=NOW,
                 detail=large_text, data={"link_status": "present", "search_truncated": False,
                       "links": [{"type": "model", "id": f"example/model{i}",
                                  "url": f"https://huggingface.co/example/model{i}",
                                  "readme": large_text} for i in range(100)]}),
        Evidence(repo_id=repo.github_id, source="future_source", status=status, fetched_at=NOW,
                 data={"unknown_payload": large_text}),
    ]
    result = score_repo(repo, items, run_id="run", now=NOW)
    output = document([repo], [result], labels_path)
    before = output.model_dump()
    evidence_path = tmp_path / "state/evidence.jsonl"
    path = write_listings(output, tmp_path / "site/src/data/listings.json", evidence_path=evidence_path)
    payload = json.loads(path.read_text(encoding="utf-8"))
    for row in payload["listings"]:
        details = payload["scoring_details"][row["repo"]["github_id"]]
        serialised = json.dumps({"listing": row, "scoring_details": details}, ensure_ascii=False, indent=2)
        assert len(serialised.encode("utf-8")) < 8 * 1024
    summaries = payload["scoring_details"][repo.github_id]["evidence"]
    assert all(item["status"] == status for item in summaries)
    hub = next(item["data"] for item in summaries if item["source"] == "hugging_face")
    assert len(hub["links"]) == 3 and hub["link_count"] == 100 and hub["links_truncated"]
    assert large_text not in path.read_text(encoding="utf-8")
    records = [json.loads(line) for line in evidence_path.read_text(encoding="utf-8").splitlines()]
    assert [Evidence.model_validate(record["evidence"]) for record in records] == items
    assert output.model_dump() == before
    Listings.model_validate(payload)


def test_excluded_repository_full_evidence_is_saved(repo, labels_path, tmp_path):
    item = Evidence(repo_id=repo.github_id, source="scorecard", status="failed",
                    fetched_at=NOW, detail="HTTP 503")
    output = document([repo], [score_repo(repo, [item], run_id="run", now=NOW)], labels_path)
    evidence_path = tmp_path / "state/evidence.jsonl"
    path = write_listings(output, tmp_path / "listings.json", evidence_path=evidence_path)
    assert json.loads(path.read_text(encoding="utf-8"))["listings"] == []
    record = json.loads(evidence_path.read_text(encoding="utf-8"))
    assert Evidence.model_validate(record["evidence"]) == item
    output.scoring_details[repo.github_id].evidence = []
    write_listings(output, path, evidence_path=evidence_path)
    assert evidence_path.read_text(encoding="utf-8") == ""


def test_evidence_write_failure_preserves_site(repo, labels_path, tmp_path):
    output = document([repo], [score(repo)], labels_path)
    path = tmp_path / "listings.json"
    path.write_bytes(b"previous good export")
    blocked = tmp_path / "blocked"
    blocked.write_text("file, not a directory", encoding="utf-8")
    with pytest.raises(OSError):
        write_listings(output, path, evidence_path=blocked / "evidence.jsonl")
    assert path.read_bytes() == b"previous good export"
    with pytest.raises(ValueError, match="separate paths"):
        write_listings(output, path, evidence_path=path)
    assert path.read_bytes() == b"previous good export"

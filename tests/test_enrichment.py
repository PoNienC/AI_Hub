"""Offline enrichment contracts, conservative evidence and per-attempt budgets."""

from datetime import UTC, datetime, timedelta

import httpx
import pytest

from pipeline.budgets import Budget, BudgetExceeded
from pipeline.http import HttpClient
from pipeline.sources import deps_dev, hacker_news, hugging_face, scorecard
from pipeline.sources._enrichment import links_repo

ADAPTERS = [deps_dev, scorecard, hugging_face, hacker_news]
NOW = datetime(2026, 11, 7, tzinfo=UTC)


def call(adapter, repo, payload, status=200, *, retries=0, limit=10):
    source = adapter.__name__.rsplit(".", 1)[1]
    requests = []

    def handler(request):
        requests.append(request)
        return httpx.Response(status, json=payload)

    budget = Budget(http_call_limits={source: limit})
    with httpx.Client(transport=httpx.MockTransport(handler)) as client:
        http = HttpClient(budget, client=client, retries=retries, sleep=lambda _: None)
        result = adapter.fetch(repo, http, fetched_at=NOW)
    assert budget.http_calls[source] == len(requests)
    return result, requests


@pytest.mark.parametrize("adapter", ADAPTERS)
@pytest.mark.parametrize("status", ["present", "absent", "failed"])
def test_adapter_status_and_one_call(adapter, status, repo, load_fixture):
    source = adapter.__name__.rsplit(".", 1)[1]
    fixture = load_fixture("enrichment_responses.json")[source][status]
    evidence, requests = call(adapter, repo, fixture["body"], fixture["status_code"])
    assert evidence.status == status
    assert evidence.source == source and evidence.repo_id == repo.github_id
    assert evidence.fetched_at == NOW
    assert len(requests) == 1


@pytest.mark.parametrize("adapter", ADAPTERS)
def test_transport_failure_and_retry_accounting(adapter, repo):
    source = adapter.__name__.rsplit(".", 1)[1]
    budget = Budget(http_call_limits={source: 3})

    def handler(request):
        raise httpx.ConnectError("private diagnostic must not escape", request=request)

    with httpx.Client(transport=httpx.MockTransport(handler)) as client:
        evidence = adapter.fetch(repo, HttpClient(budget, client=client, sleep=lambda _: None))
    assert evidence.status == "failed" and "private diagnostic" not in evidence.detail
    assert budget.http_calls[source] == 3


@pytest.mark.parametrize("adapter", ADAPTERS)
def test_exhaustion_propagates_before_request(adapter, repo):
    with pytest.raises(BudgetExceeded):
        call(adapter, repo, {}, limit=0)


@pytest.mark.parametrize("adapter", ADAPTERS)
def test_retries_are_real_calls_and_can_exhaust_budget(adapter, repo):
    evidence, requests = call(adapter, repo, {}, 503, retries=2)
    assert evidence.status == "failed" and len(requests) == 3
    with pytest.raises(BudgetExceeded):
        call(adapter, repo, {}, 503, retries=2, limit=1)


@pytest.mark.parametrize("adapter", ADAPTERS)
@pytest.mark.parametrize("payload", [{}, [], None])
def test_malformed_success_fails(adapter, payload, repo):
    evidence, _ = call(adapter, repo, payload)
    assert evidence.status == "failed" and evidence.data == {}


@pytest.mark.parametrize("adapter", ADAPTERS)
def test_invalid_json_and_non_success_do_not_leak_body(adapter, repo):
    source = adapter.__name__.rsplit(".", 1)[1]
    for status in [200, 301, 403, 429]:
        with httpx.Client(transport=httpx.MockTransport(lambda _: httpx.Response(status, text="secret"))) as client:
            evidence = adapter.fetch(repo, HttpClient(Budget(), client=client, retries=0))
        assert evidence.source == source and evidence.status == "failed"
        assert "secret" not in evidence.model_dump_json()


@pytest.mark.parametrize("adapter", ADAPTERS)
def test_unsupported_host_needs_no_call(adapter, repo):
    other = repo.model_copy(update={"html_url": "https://gitlab.com/example/agent"})
    evidence, requests = call(adapter, other, {})
    assert evidence.status == "unsupported" and requests == []


@pytest.mark.parametrize("adapter", ADAPTERS)
def test_naive_time_rejected(adapter, repo):
    with HttpClient(Budget()) as http, pytest.raises(ValueError, match="time zone"):
        adapter.fetch(repo, http, fetched_at=NOW.replace(tzinfo=None))


@pytest.mark.parametrize("adapter,expected", [
    (deps_dev, "absent"), (scorecard, "absent"),
    (hugging_face, "failed"), (hacker_news, "failed"),
])
def test_not_found_depends_on_endpoint(adapter, expected, repo):
    evidence, requests = call(adapter, repo, {"message": "Not found"}, 404)
    assert evidence.status == expected and evidence.detail == "HTTP 404"
    assert evidence.data == {} and len(requests) == 1


@pytest.mark.parametrize("identifier,expected", [
    ("github.com/example/agent-fork", "failed"),
    ("github.com/other/agent", "failed"),
    ("github.com/EXAMPLE/Agent.git", "present"),
])
def test_deps_dev_requires_matching_repository(identifier, expected, repo, load_fixture):
    payload = load_fixture("enrichment_responses.json")["deps_dev"]["present"]["body"]
    payload["projectKey"]["id"] = identifier
    evidence, _ = call(deps_dev, repo, payload)
    assert evidence.status == expected
    if expected == "failed":
        assert evidence.detail == "Mismatched repository" and evidence.data == {}


def test_hn_null_url_is_skipped(repo, load_fixture):
    payload = load_fixture("enrichment_responses.json")["hacker_news"]["present"]["body"]
    null_hit = next(hit for hit in payload["hits"] if hit["url"] is None)
    evidence, _ = call(hacker_news, repo, payload)
    assert evidence.status == "present" and evidence.data["mention_count"] == 2
    assert evidence.data["top_item"]["id"] == "1002"
    evidence, _ = call(hacker_news, repo, {"nbHits": 1, "hits": [null_hit]})
    assert evidence.status == "absent" and evidence.data["mention_count"] == 0


@pytest.mark.parametrize("field,value", [
    ("objectID", None), ("created_at_i", "yesterday"),
    ("points", -1), ("title", None), ("url", 123),
])
def test_hn_invalid_story_still_fails(field, value, repo, load_fixture):
    payload = load_fixture("enrichment_responses.json")["hacker_news"]["present"]["body"]
    hit = next(hit for hit in payload["hits"] if hit["url"] is None)
    hit[field] = value
    evidence, _ = call(hacker_news, repo, payload)
    assert evidence.status == "failed" and evidence.data == {}


def test_endpoint_mapping_and_source_payloads(repo, load_fixture):
    fixtures = load_fixture("enrichment_responses.json")
    evidence, requests = call(deps_dev, repo, fixtures["deps_dev"]["present"]["body"])
    assert requests[0].url.raw_path == b"/v3/projects/github.com%2Fexample%2Fagent"
    assert evidence.data["advisories_status"] == "unsupported"
    assert evidence.data["advisory_count"] is None
    evidence, requests = call(scorecard, repo, fixtures["scorecard"]["present"]["body"])
    assert str(requests[0].url) == "https://api.scorecard.dev/projects/github.com/example/agent"
    assert evidence.data["score"] == 7.8
    evidence, requests = call(hugging_face, repo, fixtures["hugging_face"]["present"]["body"])
    assert requests[0].url.params["q"] == '"https://github.com/example/agent"'
    assert {link["type"] for link in evidence.data["links"]} == {"model", "space"}
    assert evidence.data["links"][1]["url"] == "https://huggingface.co/spaces/example/demo"
    evidence, requests = call(hacker_news, repo, fixtures["hacker_news"]["present"]["body"])
    assert evidence.data["mention_count"] == 2
    assert evidence.data["top_item"]["id"] == "1002"
    assert requests[0].url.params["numericFilters"] == (
        f"created_at_i>={int((NOW - timedelta(days=30)).timestamp())},created_at_i<={int(NOW.timestamp())}"
    )


@pytest.mark.parametrize("value", [-1, 11, True, "7.8"])
def test_scorecard_rejects_invalid_scores(value, repo, load_fixture):
    payload = load_fixture("enrichment_responses.json")["scorecard"]["present"]["body"]
    payload["score"] = value
    assert call(scorecard, repo, payload)[0].status == "failed"


@pytest.mark.parametrize("url,expected", [
    ("https://github.com/EXAMPLE/Agent.git", True),
    ("https://github.com/example/agent?tab=readme", True),
    ("https://github.com/example/agent-fork", False),
    ("https://github.com.evil.test/example/agent", False),
    ("https://evil.test/github.com/example/agent", False),
    ("https://github.com/example", False),
    ("https://[", False),
])
def test_repository_url_identity(url, expected, repo):
    assert links_repo(url, repo) is expected


@pytest.mark.parametrize("kind,readme,url", [
    ("dataset", True, "https://github.com/example/agent"),
    ("space", False, "https://github.com/example/agent"),
    ("model", True, "https://github.com/example/agent-fork"),
    ("space", True, "https://github.com.evil.test/example/agent"),
])
def test_hub_requires_card_link_not_name_match(kind, readme, url, repo):
    payload = {"estimatedTotalHits": 1, "hits": [{
        "name": "example/agent", "type": kind, "isReadmeFile": readme,
        "formatted": {"fileContent": [{"text": url}]},
    }]}
    evidence, _ = call(hugging_face, repo, payload)
    assert evidence.status == "absent" and evidence.data["links"] == []


@pytest.mark.parametrize("adapter,payload", [
    (hugging_face, {"estimatedTotalHits": 0, "hits": []}),
    (hacker_news, {"nbHits": 0, "hits": []}),
])
def test_empty_search_is_absent(adapter, payload, repo):
    assert call(adapter, repo, payload)[0].status == "absent"


@pytest.mark.parametrize("adapter,payload", [
    (hugging_face, {"estimatedTotalHits": 1000, "hits": []}),
    (hacker_news, {"nbHits": 1001, "hits": []}),
    (hacker_news, {"nbHits": 0, "hits": [], "exhaustiveNbHits": False}),
])
def test_incomplete_search_fails(adapter, payload, repo):
    assert call(adapter, repo, payload)[0].status == "failed"


def test_hn_filters_dates_urls_and_duplicate_ids(repo, load_fixture):
    payload = load_fixture("enrichment_responses.json")["hacker_news"]["present"]["body"]
    hit = payload["hits"][0]
    payload["hits"] = [
        hit, hit.copy(),
        dict(hit, objectID="2000", created_at_i=int((NOW - timedelta(days=31)).timestamp())),
        dict(hit, objectID="2001", created_at_i=int((NOW + timedelta(days=1)).timestamp())),
        dict(hit, objectID="2002", url="https://github.com/example/agent-fork"),
    ]
    payload["nbHits"] = len(payload["hits"])
    evidence, _ = call(hacker_news, repo, payload)
    assert evidence.data["mention_count"] == 1
    assert evidence.data["top_item"]["id"] == hit["objectID"]

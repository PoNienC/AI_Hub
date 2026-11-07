"""Validate GitHub pagination, field mapping, failures and budgets offline."""

import json
import logging
from datetime import UTC, datetime

import httpx
import pytest

from pipeline.budgets import Budget, BudgetExceeded
from pipeline.config import NICHE_DEFAULT, QUERIES, Settings
from pipeline.http import HttpRequestError
from pipeline.sources.github import (
    GitHubRateLimitError,
    GitHubResponseError,
    GitHubSource,
    GraphQLError,
)

TOKEN = "fixture-secret-token"


def settings(**overrides):
    return Settings(github_token=TOKEN, query_names=["mcp"], **overrides)


def test_two_pages_deduplicate_and_map_fields(load_fixture):
    requests = []

    def handler(request):
        requests.append(request)
        assert request.headers["Authorization"] == f"Bearer {TOKEN}"
        return httpx.Response(200, json=load_fixture(f"github_page_{len(requests)}.json"))

    with httpx.Client(transport=httpx.MockTransport(handler)) as client, GitHubSource(settings(), client=client) as source:
        records = source.search()
        assert [record.github_id for record in records] == ["R_1", "R_2", "R_3"]
        assert records[1].full_name == "example/tool-renamed"
        assert source.budget.github_points == 5
        assert source.budget.http_calls["github"] == 2
        assert source.budget.github_unmeasured_calls == 0
        assert source.rate_limit_remaining == 4995
    payloads = [json.loads(request.content) for request in requests]
    assert payloads[0]["variables"] == {"query": QUERIES["mcp"], "first": 100, "after": None}
    assert payloads[1]["variables"]["after"] == "cursor_1"
    assert payloads[1]["variables"]["first"] == 98
    record = records[0]
    assert record.stars == 120 and record.forks == 7 and record.open_issues == 4
    assert record.licence_spdx == "MIT" and record.language == "Python"
    assert record.topics == ["ai-agents", "mcp"]
    assert record.release_tag == "v1.2.0"
    assert record.release_published_at == datetime(2026, 11, 1, 12, tzinfo=UTC)
    assert record.created_at == datetime(2025, 1, 1, tzinfo=UTC)
    assert record.pushed_at == datetime(2026, 11, 6, 10, tzinfo=UTC)
    assert record.readme_sha == "1" * 40
    assert record.contributor_count == 12 and record.contributor_source == "mentionable_users"
    assert record.query_tags == ["mcp"]
    assert records[1].readme_sha is None and records[1].licence_spdx is None
    assert records[1].release_tag is None and records[1].pushed_at is None


def test_cap_and_cross_query_deduplication(load_fixture):
    requests = []

    def handler(request):
        requests.append(json.loads(request.content)["variables"])
        return httpx.Response(200, json=load_fixture("github_page_1.json"))

    with httpx.Client(transport=httpx.MockTransport(handler)) as client, GitHubSource(settings(), client=client) as source:
        records = source.search({"mcp": QUERIES["mcp"], "agents": QUERIES["agents"]}, per_query_cap=2)
    assert len(records) == 2 and len(requests) == 2
    assert all(record.query_tags == ["mcp", "agents"] for record in records)
    assert all(request["first"] == 2 and request["after"] is None for request in requests)


@pytest.mark.parametrize("all_queries", [False, True])
def test_niche_and_all_queries_escape(load_fixture, all_queries):
    requests = []

    def handler(request):
        requests.append(json.loads(request.content)["variables"]["query"])
        return httpx.Response(200, json=load_fixture("github_empty.json"))

    with httpx.Client(transport=httpx.MockTransport(handler)) as client, GitHubSource(Settings(github_token=TOKEN), client=client) as source:
        assert source.search(all_queries=all_queries) == []
    names = QUERIES if all_queries else NICHE_DEFAULT
    assert requests == [QUERIES[name] for name in names]


def test_partial_error_is_typed_charged_and_does_not_leak_token(load_fixture, caplog):
    payload = load_fixture("github_partial_error.json")
    payload["errors"][0]["message"] += TOKEN
    caplog.set_level(logging.DEBUG)
    with httpx.Client(transport=httpx.MockTransport(lambda _: httpx.Response(200, json=payload))) as client:
        with GitHubSource(settings(), client=client) as source, pytest.raises(GraphQLError, match="mcp") as caught:
            source.search()
        assert source.budget.github_points == 2
        assert source.budget.http_calls["github"] == 1
    assert TOKEN not in caplog.text and TOKEN not in str(caught.value)


def test_reported_cost_aborts_on_crossing_call(load_fixture):
    calls = []

    def handler(request):
        calls.append(request)
        payload = load_fixture("github_page_1.json")
        payload["data"]["rateLimit"]["cost"] = 2499 if len(calls) == 1 else 2
        return httpx.Response(200, json=payload)

    with httpx.Client(transport=httpx.MockTransport(handler)) as client, GitHubSource(settings(), client=client) as source:
        with pytest.raises(BudgetExceeded, match="2501 > 2500"):
            source.search()
        assert source.budget.github_points == 2501
        assert source.budget.http_calls["github"] == len(calls) == 2
        with pytest.raises(BudgetExceeded):
            source.search()
        assert len(calls) == 2


def test_exact_threshold_prevents_another_network_call(load_fixture):
    calls = []

    def handler(request):
        calls.append(request)
        payload = load_fixture("github_page_1.json")
        payload["data"]["rateLimit"]["cost"] = 2500
        return httpx.Response(200, json=payload)

    with httpx.Client(transport=httpx.MockTransport(handler)) as client, GitHubSource(settings(), client=client) as source:
        with pytest.raises(BudgetExceeded):
            source.search()
        assert source.budget.github_points == 2500
        assert len(calls) == 1


def test_remote_limit_exhaustion(load_fixture):
    payload = load_fixture("github_empty.json")
    payload["data"]["rateLimit"]["remaining"] = 0
    with httpx.Client(transport=httpx.MockTransport(lambda _: httpx.Response(200, json=payload))) as client:
        with GitHubSource(settings(), client=client) as source, pytest.raises(GitHubRateLimitError):
            source.search()
        with pytest.raises(GitHubRateLimitError):
            source.search()
        assert source.budget.http_calls["github"] == 1


@pytest.mark.parametrize("payload", [[], {}, {"data": {"rateLimit": {"cost": -1, "remaining": 2}}},
                                     {"data": {"rateLimit": {"cost": True, "remaining": 2}}}])
def test_invalid_response_shapes(payload):
    with (
        httpx.Client(transport=httpx.MockTransport(lambda _: httpx.Response(200, json=payload))) as client,
        GitHubSource(settings(), client=client) as source,
        pytest.raises(GitHubResponseError),
    ):
        source.search()


@pytest.mark.parametrize("damage", ["missing_id", "null_node", "bad_page", "empty_page", "no_cursor"])
def test_malformed_repository_or_pagination(load_fixture, damage):
    payload = load_fixture("github_page_1.json")
    page = payload["data"]["search"]
    if damage == "missing_id":
        del page["nodes"][0]["id"]
    elif damage == "null_node":
        page["nodes"][0] = None
    elif damage == "bad_page":
        page["pageInfo"]["hasNextPage"] = "true"
    elif damage == "empty_page":
        page["nodes"] = []
    else:
        page["pageInfo"]["endCursor"] = None
    with (
        httpx.Client(transport=httpx.MockTransport(lambda _: httpx.Response(200, json=payload))) as client,
        GitHubSource(settings(), client=client) as source,
        pytest.raises(GitHubResponseError, match="mcp"),
    ):
        source.search()


def test_repeated_cursor_aborts(load_fixture):
    with httpx.Client(transport=httpx.MockTransport(lambda _: httpx.Response(200, json=load_fixture("github_page_1.json")))) as client:
        with GitHubSource(settings(), client=client) as source, pytest.raises(GitHubResponseError):
            source.search()
        assert source.budget.http_calls["github"] == 2


def test_retry_response_costs_are_counted(load_fixture, caplog):
    calls = []
    caplog.set_level(logging.DEBUG)

    def handler(request):
        calls.append(request)
        payload = load_fixture("github_empty.json")
        return httpx.Response(503 if len(calls) == 1 else 200, json=payload)

    with (
        httpx.Client(transport=httpx.MockTransport(handler)) as client,
        GitHubSource(settings(), client=client, sleep=lambda _: None) as source,
    ):
        assert source.search() == []
        assert source.budget.github_points == 2 and source.budget.http_calls["github"] == 2
    assert TOKEN not in caplog.text


def test_lost_response_reservation_is_visible_and_aborts(load_fixture):
    calls = []

    def handler(request):
        calls.append(request)
        if len(calls) == 1:
            raise httpx.ReadTimeout(TOKEN)
        return httpx.Response(200, json=load_fixture("github_empty.json"))

    with (
        httpx.Client(transport=httpx.MockTransport(handler)) as client,
        GitHubSource(settings(), client=client, sleep=lambda _: None) as source,
    ):
        with pytest.raises(GitHubResponseError, match="unmeasured"):
            source.search()
        assert source.budget.github_points == 2
        assert source.budget.github_unmeasured_calls == 1


@pytest.mark.parametrize("status", [200, 401, 503])
def test_invalid_json_and_http_failures(status):
    with httpx.Client(transport=httpx.MockTransport(lambda _: httpx.Response(status, text="invalid JSON"))) as client:
        expected = GitHubResponseError if status == 200 else HttpRequestError
        with GitHubSource(settings(http_retries=0), client=client) as source, pytest.raises(expected):
            source.search()


def test_default_does_not_call_rest(load_fixture):
    def handler(request):
        assert request.method == "POST"
        return httpx.Response(200, json=load_fixture("github_page_1.json"))

    with httpx.Client(transport=httpx.MockTransport(handler)) as client, GitHubSource(settings(), client=client) as source:
        assert len(source.search(per_query_cap=2)) == 2


@pytest.mark.parametrize("mode,expected", [("last", 37), ("one", 1), ("empty", 0), ("no_content", 0)])
def test_opt_in_contributor_fallback(load_fixture, mode, expected):
    requests = []

    def handler(request):
        requests.append(request)
        if request.method == "POST":
            payload = load_fixture("github_page_1.json")
            payload["data"]["search"]["nodes"] = payload["data"]["search"]["nodes"][:1]
            return httpx.Response(200, json=payload)
        assert request.url.params["per_page"] == "1" and request.url.params["anon"] == "true"
        assert request.url.path == "/repos/example/agent/contributors"
        if mode == "no_content":
            return httpx.Response(204)
        headers = {"Link": '<https://api.github.com/repos/example/agent/contributors?per_page=1&anon=true&page=37>; rel="last"'} if mode == "last" else {}
        return httpx.Response(200, json=[] if mode == "empty" else load_fixture("github_contributors.json"), headers=headers)

    with (
        httpx.Client(transport=httpx.MockTransport(handler)) as client,
        GitHubSource(settings(contributor_fallback=True), client=client) as source,
    ):
        record = source.search(per_query_cap=1)[0]
        assert record.contributor_count == expected and record.contributor_source == "rest_contributors"
        assert source.budget.github_points == 3 and len(requests) == 2


@pytest.mark.parametrize("link", [
    '<https://evil.test/next?page=2&per_page=1>; rel="last"',
    '<https://api.github.com/repos/example/agent/contributors?page=2&per_page=100>; rel="last"',
    '<https://api.github.com/repos/example/agent/contributors?page=2&per_page=1>; rel="next"',
])
def test_invalid_contributor_links_fail_closed(load_fixture, link):
    def handler(request):
        return httpx.Response(200, json=load_fixture("github_contributors.json"), headers={"Link": link})

    with (
        httpx.Client(transport=httpx.MockTransport(handler)) as client,
        GitHubSource(settings(), client=client) as source,
        pytest.raises(GitHubResponseError),
    ):
        source._rest_contributors("example/agent")


def test_rest_failure_and_budget_guard():
    with httpx.Client(transport=httpx.MockTransport(lambda _: httpx.Response(404))) as client:
        with GitHubSource(settings(), client=client) as source, pytest.raises(HttpRequestError):
            source._rest_contributors("example/agent")
        with GitHubSource(settings(), client=client, budget=Budget(github_point_limit=0)) as source:
            with pytest.raises(BudgetExceeded):
                source._rest_contributors("example/agent")
            assert source.budget.http_calls["github"] == 0


@pytest.mark.parametrize("cap", [0, 1001, 1.5, True])
def test_invalid_cap(cap):
    with (
        httpx.Client(transport=httpx.MockTransport(lambda _: httpx.Response(200))) as client,
        GitHubSource(settings(), client=client) as source,
        pytest.raises(ValueError),
    ):
        source.search(per_query_cap=cap)


def test_missing_token():
    with pytest.raises(ValueError, match="GH_TOKEN"):
        GitHubSource(Settings())

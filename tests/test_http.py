"""Test timeout, retry and accounting behaviour using only MockTransport."""

from datetime import UTC, datetime, timedelta
from email.utils import format_datetime

import httpx
import pytest

from pipeline.budgets import Budget, BudgetExceeded
from pipeline.http import HttpClient, HttpRequestError


def test_retries_count_attempts_and_apply_timeout():
    calls, sleeps = [], []

    def handler(request):
        calls.append(request)
        if len(calls) == 1:
            raise httpx.ConnectError("sensitive transport detail")
        return httpx.Response(503 if len(calls) == 2 else 200)

    budget = Budget()
    with httpx.Client(transport=httpx.MockTransport(handler)) as client:
        with HttpClient(budget, client=client, sleep=sleeps.append, timeout_seconds=7) as http:
            assert http.request("GET", "https://example.test", source="scorecard").status_code == 200
        assert not client.is_closed
    assert budget.http_calls["scorecard"] == 3
    assert sleeps == [1, 2]
    assert calls[0].extensions["timeout"] == dict.fromkeys(["connect", "read", "write", "pool"], 7)


def test_exhausted_transport_error_is_sanitised():
    def handler(request):
        raise httpx.ReadTimeout("secret-token")

    budget = Budget()
    with httpx.Client(transport=httpx.MockTransport(handler)) as client:
        http = HttpClient(budget, client=client, sleep=lambda _: None)
        with pytest.raises(HttpRequestError) as caught:
            http.request("GET", "https://example.test", source="scorecard")
    assert "secret-token" not in str(caught.value)
    assert budget.http_calls["scorecard"] == 3


def test_budget_stops_before_retry():
    budget = Budget(http_call_limits={"scorecard": 1})
    calls = []

    def handler(request):
        calls.append(request)
        return httpx.Response(503)

    with httpx.Client(transport=httpx.MockTransport(handler)) as client:
        http = HttpClient(budget, client=client, sleep=lambda _: None)
        with pytest.raises(BudgetExceeded):
            http.request("GET", "https://example.test", source="scorecard")
    assert len(calls) == 1


@pytest.mark.parametrize("status", [404, 401, 302, 503])
def test_non_retryable_post_and_status_responses(status):
    budget = Budget()
    with httpx.Client(transport=httpx.MockTransport(lambda _: httpx.Response(status))) as client:
        http = HttpClient(budget, client=client)
        assert http.request("POST", "https://example.test", source="github").status_code == status
    assert budget.http_calls["github"] == 1


def test_retryable_post_response_hooks_and_retry_after():
    seen, sleeps = [], []
    budget = Budget()
    with httpx.Client(transport=httpx.MockTransport(lambda _: httpx.Response(429, headers={"Retry-After": "3"}))) as client:
        http = HttpClient(budget, client=client, retries=1, sleep=sleeps.append)
        response = http.request("POST", "https://example.test", source="github", retryable=True,
                                before_attempt=budget.charge_github, on_response=lambda r: seen.append(r.status_code))
    assert response.status_code == 429
    assert seen == [429, 429] and sleeps == [3]
    assert budget.github_points == budget.http_calls["github"] == 2


@pytest.mark.parametrize("retry_after", ["invalid", "nan", "-2"])
def test_invalid_retry_after_uses_backoff(retry_after):
    sleeps = []
    with httpx.Client(transport=httpx.MockTransport(lambda _: httpx.Response(503, headers={"Retry-After": retry_after}))) as client:
        http = HttpClient(Budget(), client=client, retries=1, sleep=sleeps.append)
        http.request("GET", "https://example.test", source="github")
    assert sleeps == [1]


def test_retry_after_http_date():
    sleeps = []
    date = format_datetime(datetime.now(UTC) + timedelta(seconds=20), usegmt=True)
    with httpx.Client(transport=httpx.MockTransport(lambda _: httpx.Response(503, headers={"Retry-After": date}))) as client:
        http = HttpClient(Budget(), client=client, retries=1, sleep=sleeps.append)
        http.request("GET", "https://example.test", source="github")
    assert 1 <= sleeps[0] <= 20


def test_long_retry_after_aborts_without_sleeping():
    sleeps = []
    with httpx.Client(transport=httpx.MockTransport(lambda _: httpx.Response(429, headers={"Retry-After": "120"}))) as client:
        http = HttpClient(Budget(), client=client, sleep=sleeps.append)
        with pytest.raises(HttpRequestError, match="60-second"):
            http.request("GET", "https://example.test", source="github")
    assert sleeps == []


@pytest.mark.parametrize("options", [{"retries": -1}, {"retries": True}, {"timeout_seconds": 0}])
def test_invalid_options(options):
    with pytest.raises(ValueError):
        HttpClient(Budget(), **options)


def test_owned_client_is_closed():
    with HttpClient(Budget()) as http:
        assert not http._client.is_closed
    assert http._client.is_closed

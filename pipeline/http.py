"""Injectable HTTP client with bounded retries and per-attempt budget hooks."""

from __future__ import annotations

import logging
import math
import time
from collections.abc import Callable, Mapping
from datetime import UTC, datetime
from email.utils import parsedate_to_datetime
from types import TracebackType
from typing import Self

import httpx
from pydantic import JsonValue

from pipeline.budgets import Budget

LOG = logging.getLogger(__name__)
RETRY_STATUSES = {429, 500, 502, 503, 504}


class HttpRequestError(RuntimeError):
    """A request failed; diagnostics deliberately omit URLs, headers and bodies."""

    def __init__(self, source: str, reason: str) -> None:
        self.source = source
        super().__init__(f"{source} request failed: {reason}")


def _retry_delay(response: httpx.Response | None, attempt: int) -> float:
    delay = min(2**attempt, 30)
    if response is None or "Retry-After" not in response.headers:
        return delay
    value = response.headers["Retry-After"]
    try:
        seconds = float(value)
    except ValueError:
        try:
            seconds = (parsedate_to_datetime(value) - datetime.now(UTC)).total_seconds()
        except (TypeError, ValueError, OverflowError):
            return delay
    if not math.isfinite(seconds):
        return delay
    return max(delay, seconds)


class HttpClient:
    """Retry read operations, using an injected httpx client for offline tests."""

    def __init__(
        self, budget: Budget, *, client: httpx.Client | None = None,
        timeout_seconds: float = 30, retries: int = 2,
        sleep: Callable[[float], None] = time.sleep,
    ) -> None:
        if not math.isfinite(timeout_seconds) or timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be finite and positive")
        if type(retries) is not int or retries < 0:
            raise ValueError("retries must be a non-negative integer")
        self.budget = budget
        self.timeout_seconds = timeout_seconds
        self.retries = retries
        self._sleep = sleep
        self._owns_client = client is None
        self._client = httpx.Client(timeout=timeout_seconds) if client is None else client

    def request(
        self, method: str, url: str, *, source: str,
        headers: Mapping[str, str] | None = None, params: Mapping[str, str | int] | None = None,
        json: JsonValue = None, retryable: bool = False,
        before_attempt: Callable[[], None] | None = None,
        on_response: Callable[[httpx.Response], None] | None = None,
    ) -> httpx.Response:
        """Count each attempt; opt in to retries for read-only GraphQL POSTs.

        Return final HTTP responses, including 404, for source-specific evidence
        handling. Transport errors raise a sanitised exception. Redirects are
        disabled so they cannot bypass accounting or forward credentials.
        """
        attempts = self.retries + 1 if retryable or method.upper() in {"GET", "HEAD", "OPTIONS"} else 1
        for attempt in range(attempts):
            self.budget.check_http(source)
            if before_attempt is not None:
                before_attempt()
            self.budget.charge_http(source)
            response = None
            try:
                response = self._client.request(
                    method, url, headers=headers, params=params, json=json,
                    timeout=self.timeout_seconds, follow_redirects=False,
                )
            except httpx.TransportError:
                if attempt + 1 == attempts:
                    raise HttpRequestError(source, "transport error after retries") from None
            if response is not None:
                if on_response is not None:
                    on_response(response)
                if response.status_code not in RETRY_STATUSES or attempt + 1 == attempts:
                    return response
            delay = _retry_delay(response, attempt)
            if response is not None:
                response.close()
            if delay > 60:
                raise HttpRequestError(source, "Retry-After exceeds the 60-second retry allowance")
            LOG.warning("Retrying %s request after attempt %d in %.1f seconds", source, attempt + 1, delay)
            self._sleep(delay)
        raise AssertionError("Request loop must return or raise")

    def close(self) -> None:
        """Close only a client created here; injected clients belong to their caller."""
        if self._owns_client:
            self._client.close()

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self, exc_type: type[BaseException] | None, exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.close()

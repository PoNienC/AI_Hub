"""Run-level GitHub point and per-source HTTP attempt accounting."""

from __future__ import annotations

from collections.abc import Mapping

from pydantic import JsonValue

from pipeline.config import HTTP_CALL_LIMITS, Settings


class BudgetExceeded(RuntimeError):
    """A request or reported cost would exceed a configured run budget."""

    def __init__(self, resource: str, limit: int, attempted: int) -> None:
        self.resource = resource
        self.limit = limit
        self.attempted = attempted
        super().__init__(f"{resource} budget exceeded: {attempted} > {limit}")


def _non_negative_integer(value: int) -> None:
    if type(value) is not int or value < 0:
        raise ValueError("Budget values must be non-negative integers")


class Budget:
    """Count all HTTP attempts, including retries, and reconcile GraphQL costs.

    GraphQL cost is only known after a response. Reserve its minimum one point
    before sending, then record the reported cost, raising immediately on an
    overrun. A lost response retains that reservation and is explicitly counted
    as unmeasured; it must not be mistaken for an exact billed total.
    """

    def __init__(
        self, github_point_limit: int = 2500, http_call_limits: Mapping[str, int] | None = None,
    ) -> None:
        _non_negative_integer(github_point_limit)
        self.github_point_limit = github_point_limit
        self.http_call_limits = dict(HTTP_CALL_LIMITS if http_call_limits is None else http_call_limits)
        for limit in self.http_call_limits.values():
            _non_negative_integer(limit)
        self.reset()

    @classmethod
    def from_settings(cls, settings: Settings) -> Budget:
        """Build counters from a run's configured limits."""
        return cls(settings.github_point_limit, settings.http_call_limits)

    def reset(self) -> None:
        """Clear all counters for a new run, preserving configured limits."""
        self.github_points = 0
        self.github_unmeasured_calls = 0
        self.http_calls = dict.fromkeys(self.http_call_limits, 0)

    def check_github(self, points: int = 1) -> None:
        """Reject a known charge before sending a request."""
        _non_negative_integer(points)
        attempted = self.github_points + points
        if attempted > self.github_point_limit:
            raise BudgetExceeded("github_points", self.github_point_limit, attempted)

    def charge_github(self, points: int = 1) -> None:
        """Charge a known cost, such as one REST GET, before the request."""
        self.check_github(points)
        self.github_points += points

    def reserve_graphql(self) -> None:
        """Reserve the minimum cost of one GraphQL attempt."""
        self.charge_github(1)
        self.github_unmeasured_calls += 1

    def record_graphql_cost(self, cost: int) -> None:
        """Replace one reservation with actual cost, retaining any billed overrun."""
        _non_negative_integer(cost)
        if self.github_unmeasured_calls == 0:
            raise ValueError("GraphQL cost requires an outstanding reservation")
        self.github_unmeasured_calls -= 1
        self.github_points += cost - 1
        self.check_github(0)

    def check_http(self, source: str) -> None:
        """Reject an unknown source or an exhausted HTTP allowance."""
        if source not in self.http_call_limits:
            raise ValueError(f"No HTTP budget configured for source: {source}")
        attempted = self.http_calls[source] + 1
        if attempted > self.http_call_limits[source]:
            raise BudgetExceeded(f"http_calls.{source}", self.http_call_limits[source], attempted)

    def charge_http(self, source: str) -> None:
        """Count a single HTTP attempt before sending it."""
        self.check_http(source)
        self.http_calls[source] += 1

    def snapshot(self) -> dict[str, JsonValue]:
        """Return serialisable counters suitable for the state store's run log."""
        return {
            "github_points": self.github_points,
            "github_point_limit": self.github_point_limit,
            "github_unmeasured_calls": self.github_unmeasured_calls,
            "http_calls": dict(self.http_calls),
            "http_call_limits": dict(self.http_call_limits),
        }

"""Check exact thresholds, actual GraphQL costs and independent HTTP budgets."""

import pytest

from pipeline.budgets import Budget, BudgetExceeded
from pipeline.config import Settings


def test_threshold_and_refused_charge():
    budget = Budget()
    budget.charge_github(2499)
    budget.charge_github()
    assert budget.github_points == 2500
    with pytest.raises(BudgetExceeded, match="2501 > 2500") as caught:
        budget.charge_github()
    assert caught.value.resource == "github_points"
    assert budget.github_points == 2500


def test_reported_cost_overrun_is_recorded_and_aborts():
    budget = Budget()
    budget.reserve_graphql()
    with pytest.raises(BudgetExceeded):
        budget.record_graphql_cost(2501)
    assert budget.github_points == 2501
    assert budget.github_unmeasured_calls == 0
    with pytest.raises(BudgetExceeded):
        budget.reserve_graphql()


def test_zero_cost_refunds_reservation():
    budget = Budget()
    budget.reserve_graphql()
    budget.record_graphql_cost(0)
    assert budget.github_points == 0
    with pytest.raises(ValueError, match="reservation"):
        budget.record_graphql_cost(1)


def test_http_threshold_and_independent_sources():
    budget = Budget(http_call_limits={"github": 1, "scorecard": 2})
    budget.charge_http("github")
    with pytest.raises(BudgetExceeded, match="http_calls.github"):
        budget.charge_http("github")
    budget.charge_http("scorecard")
    assert budget.http_calls == {"github": 1, "scorecard": 1}
    with pytest.raises(ValueError, match="No HTTP budget"):
        budget.charge_http("unknown")


def test_reset_settings_and_snapshot_are_independent():
    settings = Settings(github_point_limit=10, http_call_limits={"github": 3})
    budget = Budget.from_settings(settings)
    budget.reserve_graphql()
    budget.charge_http("github")
    snapshot = budget.snapshot()
    assert snapshot["github_unmeasured_calls"] == 1
    assert snapshot["github_point_limit"] == 10
    snapshot["http_calls"]["github"] = 99
    assert budget.http_calls["github"] == 1
    budget.reset()
    assert budget.github_points == budget.github_unmeasured_calls == 0
    assert all(count == 0 for count in budget.http_calls.values())
    assert budget.github_point_limit == 10


@pytest.mark.parametrize("invalid", [-1, 1.5, True])
def test_invalid_budget_values(invalid):
    with pytest.raises(ValueError):
        Budget(github_point_limit=invalid)
    with pytest.raises(ValueError):
        Budget(http_call_limits={"github": invalid})
    with pytest.raises(ValueError):
        Budget().charge_github(invalid)

"""Check configuration parity, defaults and explicit environment overrides."""

import pytest
from pydantic import ValidationError

from pipeline.config import (
    NICHE_DEFAULT,
    QUERIES,
    SCORE_VERSION,
    SCORE_WEIGHTS_V0,
    Settings,
)
from scripts.pull_candidate_repos import QUERIES as ORIGINAL_QUERIES


def test_queries_match_original():
    assert QUERIES == ORIGINAL_QUERIES


def test_niche_and_all_queries():
    assert NICHE_DEFAULT == ["coding_agent", "claude_code", "mcp", "mcp_server", "ai_agents", "agents"]
    settings = Settings.from_env({})
    assert list(settings.selected_queries()) == NICHE_DEFAULT
    assert settings.selected_queries(all_queries=True) == QUERIES
    assert Settings(all_queries=True).selected_queries() == QUERIES
    assert settings.github_point_limit == 2500
    assert settings.per_query_cap == 100
    settings.query_names.clear()
    assert Settings().query_names == NICHE_DEFAULT


def test_environment_overrides(monkeypatch):
    monkeypatch.setenv("AI_HUB_PER_QUERY_CAP", "42")
    assert Settings.from_env().per_query_cap == 42
    settings = Settings.from_env({
        "GH_TOKEN": "secret-token", "GITHUB_TOKEN": "ignored-token",
        "AI_HUB_STATE_DIR": "custom_state", "AI_HUB_QUERY_NAMES": "mcp, agents,mcp",
        "AI_HUB_GITHUB_POINT_LIMIT": "1200", "AI_HUB_ALL_QUERIES": "true",
        "AI_HUB_HTTP_CALL_LIMITS": '{"scorecard": 50}',
        "AI_HUB_HTTP_TIMEOUT_SECONDS": "12.5", "AI_HUB_HTTP_RETRIES": "1",
        "AI_HUB_CONTRIBUTOR_FALLBACK": "true",
    })
    assert settings.github_token.get_secret_value() == "secret-token"
    assert "secret-token" not in repr(settings)
    assert "secret-token" not in settings.model_dump_json()
    assert settings.state_dir.name == "custom_state"
    assert settings.query_names == ["mcp", "agents"]
    assert settings.selected_queries() == QUERIES
    assert settings.github_point_limit == 1200
    assert settings.http_call_limits["scorecard"] == 50
    assert settings.http_call_limits["github"] == 1000
    assert settings.http_timeout_seconds == 12.5
    assert settings.http_retries == 1
    assert settings.contributor_fallback
    assert Settings.from_env({"GITHUB_TOKEN": "fallback"}).github_token.get_secret_value() == "fallback"


@pytest.mark.parametrize("overrides", [
    {"query_names": ["typo"]}, {"query_names": []}, {"github_point_limit": -1},
    {"http_call_limits": {"scorecard": -1}}, {"http_call_limits": {"typo": 10}},
    {"http_timeout_seconds": 0}, {"per_query_cap": 1001},
])
def test_invalid_settings(overrides):
    with pytest.raises(ValidationError):
        Settings(**overrides)


def test_weights_are_versioned_and_ignore_popularity():
    assert SCORE_VERSION == "v0"
    assert sum(SCORE_WEIGHTS_V0.values()) == pytest.approx(1)
    assert SCORE_WEIGHTS_V0["stars"] == SCORE_WEIGHTS_V0["velocity"] == 0

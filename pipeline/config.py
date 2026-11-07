"""Environment-backed pipeline settings, query selection and versioned weights."""

from __future__ import annotations

import json
import os
from collections.abc import Mapping
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field, SecretStr, field_validator

QUERIES: dict[str, str] = {
    "llm": "topic:llm stars:>3000",
    "ai_agents": "topic:ai-agents stars:>1000",
    "agents": "topic:agents stars:>2000",
    "mcp": "topic:mcp stars:>500",
    "mcp_server": "topic:mcp-server stars:>300",
    "claude_code": "claude-code in:name,description,topics stars:>300",
    "rag": "topic:rag stars:>1000",
    "generative_ai": "topic:generative-ai stars:>2000",
    "local_inference": "topic:llama stars:>2000",
    "coding_agent": "coding agent in:description stars:>1000",
    "computer_use": "topic:browser-automation topic:ai stars:>500",
    "voice": "topic:text-to-speech stars:>2000",
    "image_video": "topic:stable-diffusion stars:>3000",
    "evals": "topic:llm-evaluation stars:>300",
    "fine_tuning": "topic:fine-tuning stars:>1000",
    "new_2026": "created:>2026-01-01 stars:>1500 ai OR llm OR agent in:name,description,topics",
    "new_h2_2025": "created:2025-07-01..2025-12-31 stars:>3000 ai OR llm OR agent in:name,description,topics",
}
NICHE_DEFAULT = ["coding_agent", "claude_code", "mcp", "mcp_server", "ai_agents", "agents"]
SCORE_VERSION = "v0"
# Relative weights; raw popularity never contributes to the trust score.
SCORE_WEIGHTS_V0: dict[str, float] = {
    "scorecard": 0.25,
    "advisories": 0.20,
    "licence": 0.15,
    "maintenance": 0.15,
    "release_cadence": 0.10,
    "contributors": 0.10,
    "hacker_news": 0.05,
    "stars": 0.0,
    "velocity": 0.0,
}
HTTP_CALL_LIMITS = dict.fromkeys(
    ["github", "deps_dev", "scorecard", "hugging_face", "hacker_news"], 1000
)


class Settings(BaseModel):
    """Run settings; use ``from_env`` to load explicit environment overrides."""

    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)

    github_token: SecretStr | None = Field(default=None, repr=False)
    state_dir: Path = Path("state")
    query_names: list[str] = Field(default_factory=lambda: NICHE_DEFAULT.copy())
    all_queries: bool = False
    per_query_cap: int = Field(default=100, ge=1, le=1000)
    github_point_limit: int = Field(default=2500, ge=0)
    http_call_limits: dict[str, int] = Field(default_factory=HTTP_CALL_LIMITS.copy)
    http_timeout_seconds: float = Field(default=30, gt=0)
    http_retries: int = Field(default=2, ge=0)
    contributor_fallback: bool = False

    @field_validator("query_names")
    @classmethod
    def known_queries(cls, value: list[str]) -> list[str]:
        """Reject misspelt or empty query selections before making requests."""
        if not value or any(name not in QUERIES for name in value):
            raise ValueError("query_names must contain recognised query names")
        return list(dict.fromkeys(value))

    @field_validator("http_call_limits", mode="before")
    @classmethod
    def parse_limits(cls, value: object) -> object:
        """Parse environment JSON within the settings validation boundary."""
        if isinstance(value, str):
            try:
                return json.loads(value)
            except json.JSONDecodeError as exc:
                raise ValueError("http_call_limits must be a valid JSON object") from exc
        return value

    @field_validator("http_call_limits")
    @classmethod
    def valid_limits(cls, value: dict[str, int]) -> dict[str, int]:
        """Merge per-source overrides and reject invalid budgets."""
        if any(name not in HTTP_CALL_LIMITS or limit < 0 for name, limit in value.items()):
            raise ValueError("HTTP limits require recognised sources and non-negative limits")
        return HTTP_CALL_LIMITS | value

    @classmethod
    def from_env(cls, environ: Mapping[str, str] | None = None) -> Settings:
        """Load GH_TOKEN (or GITHUB_TOKEN) and AI_HUB_* overrides.

        QUERY_NAMES is comma-separated; HTTP_CALL_LIMITS is a JSON object.
        Other suffixes match the upper-case field names.
        """
        env = os.environ if environ is None else environ
        values: dict[str, object] = {}
        token = env.get("GH_TOKEN") or env.get("GITHUB_TOKEN")
        if token:
            values["github_token"] = token
        for name in cls.model_fields:
            key = f"AI_HUB_{name.upper()}"
            if name == "github_token" or key not in env:
                continue
            raw = env[key]
            if name == "query_names":
                values[name] = [part.strip() for part in raw.split(",")]
            else:
                values[name] = raw
        return cls.model_validate(values)

    def selected_queries(self, *, all_queries: bool = False) -> dict[str, str]:
        """Select the niche, or every query for the later CLI's --all-queries flag."""
        names = QUERIES if all_queries or self.all_queries else self.query_names
        return {name: QUERIES[name] for name in names}

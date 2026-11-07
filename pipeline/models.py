"""Validated records shared by ingestion, state storage and later export tasks."""

from __future__ import annotations

from typing import Annotated, Literal, Self

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, HttpUrl, JsonValue, model_validator

Level = Literal["beginner", "intermediate", "advanced", "not_runnable"]
Topic = Literal[
    "agent_framework", "app_builder_ui", "browser_computer_use", "coding_agent",
    "evals_observability", "fine_tuning_training", "image_video_gen",
    "learning_resource_or_list", "local_inference", "mcp_server_or_skill",
    "model_weights_or_research", "other", "rag_knowledge", "voice_realtime",
]
EvidenceStatus = Literal["present", "absent", "unsupported", "failed"]
LabelStatus = Literal["reviewed", "provisional", "pending"]
TestStatus = Literal["untested"]
ScoreVersion = Literal["v0"]
UnevaluatedCheck = Literal["fake_stars", "typosquat", "sandbox_test"]
ContributorSource = Literal["mentionable_users", "rest_contributors"]
NonNegativeInt = Annotated[int, Field(ge=0)]
Percentage = Annotated[float, Field(ge=0, le=100)]
Identifier = Annotated[str, Field(min_length=1)]


class Record(BaseModel):
    """Reject unexpected fields and non-finite values at data boundaries."""

    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)


class RepoRecord(Record):
    """Repository metadata keyed by GitHub's stable GraphQL node identifier."""

    github_id: Identifier
    full_name: str = Field(pattern=r"^[^/\s]+/[^/\s]+$")
    html_url: HttpUrl
    description: str | None = None
    language: str | None = None
    stars: NonNegativeInt = 0
    forks: NonNegativeInt = 0
    open_issues: NonNegativeInt = 0
    created_at: AwareDatetime
    pushed_at: AwareDatetime | None = None
    licence_spdx: str | None = None
    topics: list[str] = Field(default_factory=list)
    release_tag: str | None = None
    release_published_at: AwareDatetime | None = None
    contributor_count: NonNegativeInt | None = None
    contributor_source: ContributorSource | None = None
    readme_sha: str | None = None
    query_tags: list[str] = Field(default_factory=list)


class Snapshot(Record):
    """Counts observed in one run; timestamps always include a time zone."""

    repo_id: Identifier
    run_id: Identifier
    observed_at: AwareDatetime
    stars: NonNegativeInt
    forks: NonNegativeInt
    open_issues: NonNegativeInt
    pushed_at: AwareDatetime | None = None


class Evidence(Record):
    """An observation whose absence is distinct from an unsupported or failed check."""

    repo_id: Identifier
    source: Identifier
    status: EvidenceStatus
    fetched_at: AwareDatetime
    data: dict[str, JsonValue] = Field(default_factory=dict)
    detail: str | None = None


class Score(Record):
    """Versioned scoring result, including the fraction of evaluated weight."""

    repo_id: Identifier
    run_id: Identifier
    score_version: ScoreVersion
    components: dict[str, Percentage | None] = Field(default_factory=dict)
    coverage: float = Field(ge=0, le=1)
    total: Percentage | None


class Listing(Record):
    """Publication contract with explicit provisional labels and test status."""

    repo: RepoRecord
    score: Score
    level: Level | None = None
    topic: Topic | None = None
    label_status: LabelStatus = "pending"
    tested: TestStatus
    score_version: ScoreVersion
    unevaluated_checks: list[UnevaluatedCheck] = Field(
        default_factory=lambda: ["fake_stars", "typosquat", "sandbox_test"]
    )

    @model_validator(mode="after")
    def matching_score_version(self) -> Self:
        """Require the published version to match the embedded score's version."""
        if self.score_version != self.score.score_version:
            raise ValueError("listing score_version must match score.score_version")
        return self

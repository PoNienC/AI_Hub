"""Versioned evidence-weighted scores with explicit coverage and failure flags.

See docs/scoring.md for the v0 policy. Raw stars and velocity are retained as
diagnostics only. Missing evidence never receives a fabricated positive score.
"""

from __future__ import annotations

import math
from collections.abc import Iterable, Sequence
from datetime import datetime
from typing import Literal, Self

from pydantic import Field, model_validator

from pipeline.config import SCORE_VERSION, SCORE_WEIGHTS_V0
from pipeline.models import Evidence, EvidenceStatus, NonNegativeInt, Record, RepoRecord, Score
from pipeline.sources._enrichment import utc_time

Component = Literal[
    "scorecard", "advisories", "licence", "maintenance", "release_cadence",
    "contributors", "hacker_news",
]
LicenceClass = Literal["permissive", "weak_copyleft", "strong_copyleft", "unknown", "absent"]
PERMISSIVE = {
    "MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "ISC", "0BSD", "Unlicense",
    "CC0-1.0", "Zlib", "BSL-1.0",
}
WEAK_COPYLEFT = {
    "MPL-2.0", "EPL-1.0", "EPL-2.0", "LGPL-2.0", "LGPL-2.1", "LGPL-3.0",
}
STRONG_COPYLEFT = {"GPL-2.0", "GPL-3.0", "AGPL-3.0"}


class ScoreDetails(Record):
    """Persist diagnostics separately so B1 Score/Listing contracts stay intact."""

    component_statuses: dict[Component, EvidenceStatus]
    failed_components: list[Component] = Field(default_factory=list)
    licence_class: LicenceClass
    stars: NonNegativeInt
    velocity: float | None = None
    evidence: list[Evidence] = Field(default_factory=list)

    @model_validator(mode="after")
    def matching_failures(self) -> Self:
        """Require a complete status map and truthful failure flags."""
        expected = {name for name, weight in SCORE_WEIGHTS_V0.items() if weight > 0}
        if set(self.component_statuses) != expected:
            raise ValueError("Component statuses must cover every weighted component")
        failures = {key for key, value in self.component_statuses.items() if value == "failed"}
        if set(self.failed_components) != failures or len(self.failed_components) != len(failures):
            raise ValueError("Failure flags must match component statuses")
        return self


class ScoringResult(Record):
    """A B1-compatible score and its separately serialisable evidence details."""

    score: Score
    details: ScoreDetails


def _number(value: object, *, integer: bool = False) -> float:
    if type(value) not in ({int} if integer else {int, float}):
        raise ValueError("Expected a numeric observation")
    if value < 0 or not math.isfinite(value):
        raise ValueError("Observation must be finite and non-negative")
    return float(value)


def _external(component: str, evidence: Evidence | None) -> tuple[float | None, EvidenceStatus]:
    if evidence is None:
        return None, "absent"
    if evidence.status != "present":
        return None, evidence.status
    data = evidence.data
    try:
        if component == "scorecard":
            value = _number(data["score"])
            if value > 10:
                raise ValueError("Scorecard is out of range")
            return value * 10, "present"
        if component == "advisories":
            # The project adapter explicitly marks this unsupported. Only
            # separately supplied, evaluated package evidence can score here.
            status = data.get("advisories_status", "unsupported")
            if status in {"absent", "unsupported", "failed"}:
                return None, status
            if status != "present":
                raise ValueError("Unknown advisory status")
            return 100 / (1 + _number(data["advisory_count"], integer=True)), "present"
        count = _number(data["mention_count"], integer=True)
        return min(100, count * 20), "present"
    except (KeyError, TypeError, ValueError, OverflowError):
        return None, "failed"


def _licence(spdx: str | None) -> tuple[float | None, EvidenceStatus, LicenceClass]:
    if not spdx or spdx in {"NOASSERTION", "NONE"}:
        return None, "absent", "absent"
    if spdx in PERMISSIVE:
        return 100, "present", "permissive"
    copyleft_id = spdx.removesuffix("-only").removesuffix("-or-later")
    if copyleft_id in WEAK_COPYLEFT:
        return 80, "present", "weak_copyleft"
    if copyleft_id in STRONG_COPYLEFT:
        return 60, "present", "strong_copyleft"
    return None, "unsupported", "unknown"


def _freshness(value: datetime | None, now: datetime) -> tuple[float | None, EvidenceStatus]:
    if value is None:
        return None, "absent"
    age = (now - utc_time(value)).total_seconds() / 86400
    if age < 0:
        return None, "failed"
    return max(0, 100 * (1 - age / 365)), "present"


def _cadence(
    repo: RepoRecord, history: Sequence[datetime] | None, now: datetime,
) -> tuple[float | None, EvidenceStatus]:
    dates = {utc_time(date) for date in (() if history is None else history)}
    if repo.release_published_at is not None:
        dates.add(utc_time(repo.release_published_at))
    if not dates:
        return None, "absent"
    if any(date > now or date < repo.created_at for date in dates):
        return None, "failed"
    if len(dates) < 2:
        return None, "unsupported"
    ordered = sorted(dates)
    mean_days = (ordered[-1] - ordered[0]).total_seconds() / 86400 / (len(ordered) - 1)
    freshness, _ = _freshness(ordered[-1], now)
    return min(freshness, 100 * min(1, 30 / mean_days)), "present"


def score_repo(
    repo: RepoRecord, evidence: Iterable[Evidence], *, run_id: str,
    now: datetime | None = None, velocity: float | None = None,
    release_history: Sequence[datetime] | None = None,
) -> ScoringResult:
    """Score one repository, excluding unevaluated weight from the denominator.

    Duplicate sources or another repository's evidence are input errors. Future
    observations are failed components. Release cadence needs two distinct
    release dates; a lone latestRelease is not evidence of a release interval.
    Store ``result.score`` with StateStore.add_score; export retains ``details``.
    """
    observed = utc_time(now)
    if velocity is not None and (type(velocity) not in {int, float} or not math.isfinite(velocity)):
        raise ValueError("Velocity must be finite or None")
    sources = {}
    for item in evidence:
        if item.repo_id != repo.github_id:
            raise ValueError("Evidence belongs to a different repository")
        if item.source in sources:
            raise ValueError(f"Duplicate evidence source: {item.source}")
        sources[item.source] = item
    components = dict.fromkeys(SCORE_WEIGHTS_V0)
    statuses = {}
    for component, source in [("scorecard", "scorecard"), ("advisories", "deps_dev"), ("hacker_news", "hacker_news")]:
        item = sources.get(source)
        if item is not None and item.fetched_at > observed:
            components[component], statuses[component] = None, "failed"
        else:
            components[component], statuses[component] = _external(component, item)
    components["licence"], statuses["licence"], licence_class = _licence(repo.licence_spdx)
    components["maintenance"], statuses["maintenance"] = _freshness(repo.pushed_at, observed)
    components["release_cadence"], statuses["release_cadence"] = _cadence(repo, release_history, observed)
    if repo.contributor_count is None:
        statuses["contributors"] = "absent"
    else:
        components["contributors"] = min(100, repo.contributor_count * 10)
        statuses["contributors"] = "present"
    evaluated = math.fsum(SCORE_WEIGHTS_V0[key] for key, value in components.items() if value is not None)
    possible = math.fsum(SCORE_WEIGHTS_V0.values())
    weighted = math.fsum(SCORE_WEIGHTS_V0[key] * value for key, value in components.items() if value is not None)
    score = Score(
        repo_id=repo.github_id, run_id=run_id, score_version=SCORE_VERSION,
        components=components, coverage=min(1, evaluated / possible),
        total=min(100, max(0, weighted / evaluated)) if evaluated else None,
    )
    return ScoringResult(score=score, details=ScoreDetails(
        component_statuses=statuses,
        failed_components=[key for key, value in statuses.items() if value == "failed"],
        licence_class=licence_class, stars=repo.stars, velocity=velocity,
        evidence=list(sources.values()),
    ))

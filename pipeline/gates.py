"""Publication schema and data-quality gates, evaluated before promotion."""

from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path

from pydantic import ValidationError

from pipeline.export import Listings
from pipeline.site.links import SiteCheckError, check
from pipeline.sources._enrichment import utc_time

REQUIRE_LABELS = False


class GateFailure(RuntimeError):
    """A named publication gate rejected an artefact without exposing its data."""

    def __init__(self, gate: str, rule: str, reason: str) -> None:
        self.gate = gate
        self.rule = rule
        super().__init__(f"{gate} ({rule}): {reason}")


def gate_2(path: Path) -> Listings:
    """Validate the exported envelope and PublishedListing rows, including coverage."""
    try:
        return Listings.model_validate_json(Path(path).read_bytes())
    except (OSError, ValidationError) as exc:
        # Pydantic's full error includes input values; do not copy them into issues.
        raise GateFailure("gate_2", "schema", f"Invalid listings file: {type(exc).__name__}") from None


def gate_3(
    listings: Listings, *, previous_count: int | None = None,
    now: datetime | None = None, require_labels: bool | None = None,
) -> None:
    """Require fresh, complete rows and at least 90 per cent of the last good count.

    The first run has no count baseline. Missing labels are allowed until request
    2. B1 supports only ``untested``: dated sandbox results and other statuses
    must be introduced together by request 3, never inferred here.
    """
    if previous_count is not None and (type(previous_count) is not int or previous_count < 0):
        raise ValueError("previous_count must be a non-negative integer or None")
    age = utc_time(now) - listings.generated_at
    if not timedelta(0) <= age <= timedelta(hours=7):
        raise GateFailure("gate_3", "freshness", "generated_at must be within the past 7 hours")
    if previous_count is not None and len(listings.listings) * 10 < previous_count * 9:
        raise GateFailure("gate_3", "count", "Listed count is below 90 per cent of the previous successful run")
    labels_required = REQUIRE_LABELS if require_labels is None else require_labels
    for row in listings.listings:
        if row.score is None or row.score.total is None:
            raise GateFailure("gate_3", "score", "Every listing requires an evaluated score")
        details = listings.scoring_details.get(row.repo.github_id)
        if details is None or details.licence_class not in {
            "permissive", "weak_copyleft", "strong_copyleft", "unknown", "absent",
        }:
            raise GateFailure("gate_3", "licence", "Every listing requires an explicit licence status")
        if row.tested != "untested":
            raise GateFailure("gate_3", "tested", "Only untested is supported without dated sandbox results")
        if labels_required and (row.topic is None or row.level is None):
            raise GateFailure("gate_3", "labels", "Every listing requires both topic and level")


def check_gates(
    path: Path, *, previous_count: int | None = None, now: datetime | None = None,
    require_labels: bool | None = None,
) -> dict[str, bool]:
    """Read the actual output file and return promotion gates only when both pass."""
    listings = gate_2(path)
    gate_3(listings, previous_count=previous_count, now=now, require_labels=require_labels)
    return {"gate_2": True, "gate_3": True}


def gate_5(dist: Path) -> None:
    """Reject broken site links, oversize pages or an index without a topic."""
    try:
        check(dist)
    except SiteCheckError as exc:
        raise GateFailure("gate_5", exc.rule, str(exc)) from None
    except OSError as exc:
        raise GateFailure("gate_5", "site", f"Cannot inspect site: {type(exc).__name__}") from None

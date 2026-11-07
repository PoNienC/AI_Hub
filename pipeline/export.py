"""Validated, deterministic listing export with provisional CSV labels."""

from __future__ import annotations

import csv
import json
from collections.abc import Iterable
from datetime import datetime
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Self

from pydantic import AwareDatetime, Field, JsonValue, model_validator

from pipeline.config import SCORE_VERSION
from pipeline.models import Evidence, Identifier, Level, Listing, Record, RepoRecord, ScoreVersion, Topic
from pipeline.scoring import ScoreDetails, ScoringResult
from pipeline.sources._enrichment import utc_time

DEFAULT_LABELS_PATH = Path("data/labelled_repos_for_review.csv")
DEFAULT_OUTPUT_PATH = Path("site/src/data/listings.json")
DEFAULT_EVIDENCE_PATH = Path("state/evidence.jsonl")
SUMMARY_LINK_LIMIT = 3
SUMMARY_TEXT_LIMIT = 256


class ProvisionalLabel(Record):
    """An unreviewed label; CSV confidence is not human approval."""

    topic: Topic
    level: Level


class PublishedListing(Listing):
    """Extend the B1 publication contract with visible evaluated coverage."""

    coverage: float = Field(ge=0, le=1)

    @model_validator(mode="after")
    def matching_coverage(self) -> Self:
        """Prevent the displayed fraction from diverging from the score."""
        if self.coverage != self.score.coverage:
            raise ValueError("Listing coverage must match score.coverage")
        return self


class Listings(Record):
    """Publication envelope; exported rows extend B1 Listing with coverage.

    Details are keyed by GitHub ID, including diagnostics for excluded null
    scores. They preserve failed checks, licence status and raw velocity without
    altering B1 models or the SQLite schema.
    """

    generated_at: AwareDatetime
    score_version: ScoreVersion
    run_id: Identifier
    listings: list[PublishedListing]
    scoring_details: dict[str, ScoreDetails]

    @model_validator(mode="after")
    def consistent_rows(self) -> Self:
        """Reject mismatched identities, run metadata, null scores or duplicates."""
        seen = set()
        for listing in self.listings:
            repo_id = listing.repo.github_id
            if repo_id in seen or listing.score.repo_id != repo_id:
                raise ValueError("Duplicate or mismatched repository identity")
            seen.add(repo_id)
            if listing.score.run_id != self.run_id or listing.score_version != self.score_version:
                raise ValueError("Listing run/version must match the envelope")
            if listing.score.total is None or listing.score.coverage == 0:
                raise ValueError("Published listings require evaluated scores")
            if repo_id not in self.scoring_details:
                raise ValueError("Every listing requires scoring details")
            if self.scoring_details[repo_id].stars != listing.repo.stars:
                raise ValueError("Scoring details must match repository stars")
            statuses = self.scoring_details[repo_id].component_statuses
            for name, status in statuses.items():
                if (listing.score.components.get(name) is not None) != (status == "present"):
                    raise ValueError("Component values must match evidence statuses")
            if listing.label_status == "pending" and (listing.topic is not None or listing.level is not None):
                raise ValueError("Pending labels must have null topic and level")
            if listing.label_status != "pending" and (listing.topic is None or listing.level is None):
                raise ValueError("Assigned labels require both topic and level")
        for repo_id, details in self.scoring_details.items():
            if any(item.repo_id != repo_id for item in details.evidence):
                raise ValueError("Evidence belongs to a different repository")
        return self


def load_provisional_labels(path: Path = DEFAULT_LABELS_PATH) -> dict[str, ProvisionalLabel]:
    """Read case-insensitive GitHub names; reject invalid or duplicate CSV rows."""
    labels = {}
    with Path(path).open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not {"full_name", "topic", "level"}.issubset(reader.fieldnames or []):
            raise ValueError("Label CSV requires full_name, topic and level columns")
        for line, row in enumerate(reader, start=2):
            name = (row.get("full_name") or "").strip().casefold()
            if len(name.split("/")) != 2 or not all(name.split("/")) or any(c.isspace() for c in name):
                raise ValueError(f"Invalid full_name in label CSV at line {line}")
            if name in labels:
                raise ValueError(f"Duplicate label CSV repository at line {line}")
            labels[name] = ProvisionalLabel(topic=row.get("topic"), level=row.get("level"))
    return labels


def build_listings(
    repos: Iterable[RepoRecord], results: Iterable[ScoringResult], *, run_id: str,
    generated_at: datetime | None = None, labels_path: Path = DEFAULT_LABELS_PATH,
) -> Listings:
    """Join by stable ID, apply provisional labels and sort by score then push time."""
    labels = load_provisional_labels(labels_path)
    by_id = {}
    for result in results:
        score = result.score
        if score.repo_id in by_id:
            raise ValueError("Duplicate score for repository")
        if score.run_id != run_id or score.score_version != SCORE_VERSION:
            raise ValueError("Score run/version does not match export")
        by_id[score.repo_id] = result
    rows = []
    seen = set()
    for repo in repos:
        if repo.github_id in seen:
            raise ValueError("Duplicate repository")
        seen.add(repo.github_id)
        if repo.github_id not in by_id:
            raise ValueError(f"Missing score for repository: {repo.github_id}")
        result = by_id[repo.github_id]
        if result.score.total is None:
            continue
        label = labels.get(repo.full_name.casefold())
        rows.append(PublishedListing(
            repo=repo, score=result.score, topic=label.topic if label else None,
            coverage=result.score.coverage,
            level=label.level if label else None, label_status="provisional" if label else "pending",
            tested="untested", score_version=SCORE_VERSION,
            unevaluated_checks=["fake_stars", "typosquat", "sandbox_test"],
        ))
    if set(by_id) != seen:
        raise ValueError("Score has no corresponding repository")
    rows.sort(key=lambda row: (
        -row.score.total,
        -(row.repo.pushed_at.timestamp() if row.repo.pushed_at else float("-inf")),
        row.repo.full_name.casefold(), row.repo.github_id,
    ))
    return Listings(
        generated_at=utc_time(generated_at), score_version=SCORE_VERSION, run_id=run_id,
        listings=rows, scoring_details={repo_id: by_id[repo_id].details for repo_id in sorted(by_id)},
    )


def _summary_fields(data: dict[str, JsonValue], names: tuple[str, ...]) -> dict[str, JsonValue]:
    """Keep selected scalars; omit nested payloads and overlong source text."""
    return {
        name: value for name in names if name in data
        if (value := data[name]) is None or type(value) in {bool, int, float}
        or (isinstance(value, str) and len(value) <= SUMMARY_TEXT_LIMIT)
    }


def _summarise_evidence(item: Evidence) -> Evidence:
    """Retain bounded source diagnostics without shipping full adapter payloads."""
    data = item.data
    summary = {}
    if item.source == "scorecard":
        summary = _summary_fields(data, ("score", "date"))
    elif item.source == "deps_dev":
        summary = _summary_fields(data, ("advisories_status", "advisory_count"))
    elif item.source == "hacker_news":
        summary = _summary_fields(data, ("mention_count", "window_start", "window_end"))
        top = data.get("top_item")
        if isinstance(top, dict):
            summary["top_item"] = _summary_fields(
                top, ("id", "title", "url", "discussion_url", "points", "created_at_i"),
            )
        elif top is None:
            summary["top_item"] = None
    elif item.source == "hugging_face":
        summary = _summary_fields(data, ("link_status", "search_truncated"))
        links = data.get("links")
        if isinstance(links, list):
            summary["link_count"] = len(links)
            summary["links_truncated"] = len(links) > SUMMARY_LINK_LIMIT
            summary["links"] = [
                _summary_fields(link, ("type", "id", "url"))
                for link in links[:SUMMARY_LINK_LIMIT] if isinstance(link, dict)
            ]
    return item.model_copy(update={
        "data": summary,
        "detail": item.detail[:SUMMARY_TEXT_LIMIT] if item.detail is not None else None,
    })


def _write_atomic(path: Path, chunks: Iterable[str]) -> Path:
    """Replace one artefact only after all chunks have been written successfully."""
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with NamedTemporaryFile(mode="w", encoding="utf-8", newline="\n", dir=destination.parent,
                                prefix=f".{destination.name}.", suffix=".tmp", delete=False) as handle:
            temporary = Path(handle.name)
            handle.writelines(chunks)
        temporary.replace(destination)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    return destination


def write_listings(
    listings: Listings, path: Path = DEFAULT_OUTPUT_PATH, *,
    evidence_path: Path = DEFAULT_EVIDENCE_PATH,
) -> Path:
    """Write full local evidence first, then atomically replace compact site JSON.

    Both files are validated before writing and replaced individually. Evidence
    is a diagnostic snapshot, tagged with run ID; it is not canonical state.
    Pass a separate evidence_path as well as path for an isolated dry run.
    """
    if Path(path).resolve() == Path(evidence_path).resolve():
        raise ValueError("Listings and full evidence require separate paths")
    validated = Listings.model_validate_json(listings.model_dump_json())
    compact = validated.model_copy(update={"scoring_details": {
        repo_id: details.model_copy(update={
            "evidence": [_summarise_evidence(item) for item in details.evidence],
        }) for repo_id, details in validated.scoring_details.items()
    }})
    payload = Listings.model_validate_json(compact.model_dump_json()).model_dump_json(indent=2) + "\n"
    _write_atomic(evidence_path, (
        json.dumps({
            "run_id": validated.run_id, "score_version": validated.score_version,
            "generated_at": validated.generated_at.isoformat(),
            "evidence": item.model_dump(mode="json"),
        }, ensure_ascii=False, allow_nan=False) + "\n"
        for repo_id in sorted(validated.scoring_details)
        for item in validated.scoring_details[repo_id].evidence
    ))
    return _write_atomic(path, [payload])

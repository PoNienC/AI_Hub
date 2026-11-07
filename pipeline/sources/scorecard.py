"""Read published OpenSSF Scorecard results; no scan is run by this adapter.

Reference: https://api.scorecard.dev/
"""

import math
from datetime import datetime
from urllib.parse import quote

from pipeline.http import HttpClient
from pipeline.models import Evidence, RepoRecord
from pipeline.sources._enrichment import failed, fetch_json, links_repo


def fetch(repo: RepoRecord, http: HttpClient, *, fetched_at: datetime | None = None) -> Evidence:
    """Return the published 0–10 aggregate and its upstream observation date."""
    path = "/".join(quote(part, safe="") for part in repo.full_name.split("/"))
    evidence = fetch_json(
        repo, http, source="scorecard", url=f"https://api.scorecard.dev/projects/github.com/{path}",
        fetched_at=fetched_at,
    )
    if evidence.status != "present":
        return evidence
    try:
        score = evidence.data["score"]
        if type(score) not in {int, float} or not math.isfinite(score) or not 0 <= score <= 10:
            raise ValueError("Invalid score")
        if not links_repo("https://" + evidence.data["repo"]["name"], repo):
            raise ValueError("Mismatched repository")
        observed = evidence.data["date"]
        if not isinstance(observed, str):
            raise ValueError("Invalid date")
        datetime.fromisoformat(observed)
    except (KeyError, TypeError, ValueError):
        return failed(evidence, "Malformed Scorecard result")
    return evidence

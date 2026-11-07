"""Fetch deps.dev project evidence using its percent-encoded GitHub identifier.

GetProject does not expose package-version advisories. Its presence must never
be interpreted as zero vulnerabilities. Advisory coverage remains unsupported
until a future package/version resolution stage supplies that evidence.
Reference: https://docs.deps.dev/api/v3/#getproject
"""

from datetime import datetime
from urllib.parse import quote

from pipeline.http import HttpClient
from pipeline.models import Evidence, RepoRecord
from pipeline.sources._enrichment import failed, fetch_json


def fetch(repo: RepoRecord, http: HttpClient, *, fetched_at: datetime | None = None) -> Evidence:
    """Return project evidence without inferring package advisories or ecosystem."""
    project_id = f"github.com/{repo.full_name}"
    evidence = fetch_json(
        repo, http, source="deps_dev",
        url=f"https://api.deps.dev/v3/projects/{quote(project_id, safe='')}",
        fetched_at=fetched_at,
    )
    if evidence.status != "present":
        return evidence
    try:
        identifier = evidence.data["projectKey"]["id"]
        if not isinstance(identifier, str) or not identifier.startswith("github.com/"):
            raise ValueError("Invalid project identifier")
    except (KeyError, TypeError, ValueError):
        return failed(evidence, "Malformed deps.dev project")
    return evidence.model_copy(update={
        "data": {"project": evidence.data, "advisory_count": None, "advisories_status": "unsupported"},
        "detail": "Project endpoint does not evaluate package-version advisories",
    })

"""Shared evidence boundaries for the four read-only enrichment adapters."""

from __future__ import annotations

import re
from collections.abc import Mapping, Set
from datetime import UTC, datetime
from urllib.parse import urlsplit

from pipeline.http import HttpClient, HttpRequestError
from pipeline.models import Evidence, RepoRecord

URL_PATTERN = re.compile(r"https?://[^\s<>\[\]()\"'\\]+", re.IGNORECASE)


def utc_time(value: datetime | None = None) -> datetime:
    """Return an aware UTC observation time, rejecting naive caller timestamps."""
    value = datetime.now(UTC) if value is None else value
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("Observation time must include a time zone")
    return value.astimezone(UTC)


def links_repo(url: str, repo: RepoRecord) -> bool:
    """Match a GitHub repository or a path inside it, never a name prefix."""
    try:
        parsed = urlsplit(url)
        if parsed.scheme not in {"http", "https"} or parsed.netloc.lower() != "github.com":
            return False
        parts = parsed.path.strip("/").split("/")
        if len(parts) < 2:
            return False
        name = parts[1].removesuffix(".git")
        return f"{parts[0]}/{name}".casefold() == repo.full_name.casefold()
    except ValueError:
        return False


def failed(evidence: Evidence, detail: str) -> Evidence:
    """Discard unvalidated payloads and retain a sanitised failure reason."""
    return evidence.model_copy(update={"status": "failed", "data": {}, "detail": detail})


def fetch_json(
    repo: RepoRecord, http: HttpClient, *, source: str, url: str,
    fetched_at: datetime | None = None, params: Mapping[str, str | int] | None = None,
    absent_statuses: Set[int] = frozenset({404}),
) -> Evidence:
    """Map HTTP outcomes to evidence; budget exhaustion deliberately propagates.

    One lookup is made for a supported repository. HttpClient charges each
    actual attempt, including retries. An unsupported host makes no request;
    a GitHub repository's programming language does not establish its ecosystem.
    Search endpoints pass an empty absent_statuses set: only an empty successful
    response establishes absence there, whereas an HTTP 404 means failure.
    """
    evidence = Evidence(
        repo_id=repo.github_id, source=source, status="unsupported", fetched_at=utc_time(fetched_at),
    )
    if not links_repo(str(repo.html_url), repo):
        return evidence.model_copy(update={"detail": "Only GitHub repositories are supported"})
    try:
        response = http.request("GET", url, source=source, params=params)
    except HttpRequestError:
        return failed(evidence, "Network request failed after bounded retries")
    try:
        if response.status_code in absent_statuses:
            return evidence.model_copy(update={
                "status": "absent", "detail": f"HTTP {response.status_code}",
            })
        if response.status_code != 200:
            return failed(evidence, f"HTTP {response.status_code}")
        try:
            payload = response.json()
            if not isinstance(payload, dict):
                raise ValueError("Expected JSON object")
            return Evidence(
                repo_id=repo.github_id, source=source, status="present",
                fetched_at=evidence.fetched_at, data=payload,
            )
        except ValueError:
            return failed(evidence, "Invalid JSON object")
    finally:
        response.close()

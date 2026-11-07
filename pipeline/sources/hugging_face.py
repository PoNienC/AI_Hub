"""Record links from model/Space cards, never a compatibility or run-test claim.

Use one bounded combined full-text lookup (100 hits), rather than name searches
that do not search card bodies. The Hub also indexes datasets and Space code;
only model/Space README hits containing the exact GitHub repository qualify.
No match in a truncated response is failed/incomplete, not proof of absence.
The full-text JSON shape is an observed web API contract, not a versioned SDK
guarantee; schema changes fail closed. Reference: https://huggingface.co/docs/hub/search
"""

from datetime import datetime
from urllib.parse import quote

from pipeline.http import HttpClient
from pipeline.models import Evidence, RepoRecord
from pipeline.sources._enrichment import URL_PATTERN, failed, fetch_json, links_repo

SEARCH_LIMIT = 100


def fetch(repo: RepoRecord, http: HttpClient, *, fetched_at: datetime | None = None) -> Evidence:
    """Return confirmed card links from a single combined model/Space search."""
    evidence = fetch_json(
        repo, http, source="hugging_face", url="https://huggingface.co/api/search/full-text",
        params={"q": f'"https://github.com/{repo.full_name}"', "limit": SEARCH_LIMIT},
        fetched_at=fetched_at,
    )
    if evidence.status != "present":
        return evidence
    try:
        hits, total = evidence.data["hits"], evidence.data["estimatedTotalHits"]
        if not isinstance(hits, list) or type(total) is not int or total < len(hits):
            raise ValueError("Invalid search hits")
        links = {}
        for hit in hits:
            if not isinstance(hit, dict):
                raise ValueError("Invalid hit")
            if hit["type"] not in {"model", "space"} or hit["isReadmeFile"] is not True:
                continue
            name = hit["name"]
            if not isinstance(name, str) or len(name.split("/")) != 2:
                raise ValueError("Invalid Hub identifier")
            fragments = hit["formatted"]["fileContent"]
            if not isinstance(fragments, list):
                raise ValueError("Invalid card text")
            content = "".join(fragment["text"] for fragment in fragments)
            if any(links_repo(url.rstrip(".,;!"), repo) for url in URL_PATTERN.findall(content)):
                prefix = "spaces/" if hit["type"] == "space" else ""
                url = "https://huggingface.co/" + prefix + quote(name, safe="/")
                links[url] = {"type": hit["type"], "id": name, "url": url}
        truncated = total > len(hits)
    except (KeyError, TypeError, ValueError):
        return failed(evidence, "Malformed Hugging Face full-text results")
    if truncated and not links:
        return failed(evidence, "Search truncated before any repository card link was confirmed")
    return evidence.model_copy(update={
        "status": "present" if links else "absent",
        "data": {"link_status": "present" if links else "absent",
                 "links": list(links.values()), "search_truncated": truncated},
        "detail": "Card links only; no execution or compatibility check",
    })

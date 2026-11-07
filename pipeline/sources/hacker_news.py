"""Count exact repository story URLs in a bounded 30-day Algolia search.

This is a discussion signal, not a security or quality judgement. Search is
limited to 1,000 candidates in one request; an incomplete result is failed so
neither a partial count nor an uncertain top item can affect ranking.
Reference: https://hn.algolia.com/api
"""

from datetime import datetime, timedelta

from pipeline.http import HttpClient
from pipeline.models import Evidence, RepoRecord
from pipeline.sources._enrichment import failed, fetch_json, links_repo, utc_time

SEARCH_LIMIT = 1000


def fetch(repo: RepoRecord, http: HttpClient, *, fetched_at: datetime | None = None) -> Evidence:
    """Return mention count and highest-point story within the last 30 days."""
    end = utc_time(fetched_at)
    start = end - timedelta(days=30)
    evidence = fetch_json(
        repo, http, source="hacker_news", url="https://hn.algolia.com/api/v1/search",
        params={"query": f"https://github.com/{repo.full_name}", "tags": "story",
                "restrictSearchableAttributes": "url", "typoTolerance": "false",
                "numericFilters": f"created_at_i>={int(start.timestamp())},created_at_i<={int(end.timestamp())}",
                "hitsPerPage": SEARCH_LIMIT, "page": 0},
        fetched_at=end,
    )
    if evidence.status != "present":
        return evidence
    try:
        hits, count = evidence.data["hits"], evidence.data["nbHits"]
        if not isinstance(hits, list) or type(count) is not int or count != len(hits):
            raise ValueError("Incomplete search")
        if evidence.data.get("exhaustiveNbHits", True) is not True:
            raise ValueError("Approximate count")
        matched = {}
        for hit in hits:
            identifier, created, points = hit["objectID"], hit["created_at_i"], hit["points"]
            if (not isinstance(identifier, str) or not identifier.isdigit()
                    or type(created) is not int or type(points) is not int or points < 0
                    or not isinstance(hit["url"], str) or not isinstance(hit["title"], str)):
                raise ValueError("Invalid story")
            if (int(start.timestamp()) <= created <= int(end.timestamp())
                    and links_repo(hit["url"], repo)):
                matched[identifier] = {
                    "id": identifier, "title": hit["title"], "url": hit["url"],
                    "discussion_url": f"https://news.ycombinator.com/item?id={identifier}",
                    "points": points, "created_at_i": created,
                }
        top = max(matched.values(), key=lambda item: (item["points"], item["created_at_i"], item["id"]), default=None)
    except (KeyError, TypeError, ValueError):
        return failed(evidence, "Malformed or incomplete Hacker News results")
    return evidence.model_copy(update={
        "status": "present" if matched else "absent",
        "data": {"mention_count": len(matched), "top_item": top,
                 "window_start": start.isoformat(), "window_end": end.isoformat()},
    })

"""Pull candidate AI repositories from the GitHub search API for the phase 0 labelling set.

Data layer: data_ingestion. No spatial data; no CRS applies.
Writes data/candidate_repos.csv (relative to the project root). Needs an authenticated `gh` CLI.
"""
from __future__ import annotations

import csv
import json
import logging
import subprocess
import time
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
LOG = logging.getLogger("pull_candidate_repos")

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
FIELDS = [
    "query_tag", "full_name", "stars", "forks", "language", "license", "created_at",
    "pushed_at", "open_issues", "topics", "description", "html_url",
]


def search(query: str, per_page: int = 100) -> list[dict]:
    """Run one GitHub repository search sorted by stars and return raw items."""
    cmd = [
        "gh", "api", "-X", "GET", "search/repositories",
        "-f", f"q={query}", "-f", "sort=stars", "-f", "order=desc", "-f", f"per_page={per_page}",
    ]
    out = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", check=True).stdout
    return json.loads(out).get("items", [])


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    out_path = root / "data" / "candidate_repos.csv"
    seen: set[str] = set()
    rows: list[dict] = []
    for tag, query in QUERIES.items():
        try:
            items = search(query)
        except subprocess.CalledProcessError as exc:
            LOG.error("query %s failed: %s", tag, exc.stderr[:200])
            continue
        LOG.info("%s: %d items", tag, len(items))
        for it in items:
            name = it["full_name"]
            if name in seen:
                continue
            seen.add(name)
            rows.append({
                "query_tag": tag,
                "full_name": name,
                "stars": it["stargazers_count"],
                "forks": it["forks_count"],
                "language": it.get("language") or "",
                "license": (it.get("license") or {}).get("spdx_id", "") or "",
                "created_at": it["created_at"][:10],
                "pushed_at": it["pushed_at"][:10],
                "open_issues": it["open_issues_count"],
                "topics": ";".join(it.get("topics", [])),
                "description": (it.get("description") or "").replace("\n", " ")[:300],
                "html_url": it["html_url"],
            })
        time.sleep(2.5)  # search API allows 30 requests a minute
    with out_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    LOG.info("wrote %d unique repos to %s", len(rows), out_path)


if __name__ == "__main__":
    main()

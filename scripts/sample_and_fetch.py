"""Sample 100 candidate repos across topic and star band, fetch README and root listing, compute run-readiness signals.

Data layer: data_ingestion. No spatial data; no CRS applies.
Reads data/candidate_repos.csv; writes data/labelling_set.csv and data/readmes/<owner>__<repo>.md. Needs `gh`.
"""
from __future__ import annotations

import base64
import csv
import json
import logging
import random
import re
import subprocess
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
LOG = logging.getLogger("sample_and_fetch")
random.seed(20261107)

ROOT = Path(__file__).resolve().parent.parent
README_DIR = ROOT / "data" / "readmes"
DEPLOY_BADGES = ("vercel.com/new", "render.com/deploy", "railway.app/new", "railway.com/new",
                 "heroku.com/deploy", "deploy.cloud.run", "replit.com/github", "colab.research.google.com",
                 "huggingface.co/spaces", "codespaces/new", "open.vscode.dev", "deploy with vercel",
                 "deploy on railway", "netlify.com/start")


def gh_json(path: str) -> dict | list | None:
    """Call the GitHub REST API through gh and return parsed JSON, or None on error."""
    res = subprocess.run(["gh", "api", path], capture_output=True, text=True, encoding="utf-8", errors="replace", check=False)
    if res.returncode != 0:
        return None
    return json.loads(res.stdout)


def sample(rows: list[dict], per_tag: int = 6) -> list[dict]:
    """Take the top three and three lower-half repos per query tag; dedupe; trim to 100."""
    by_tag: dict[str, list[dict]] = {}
    for r in rows:
        by_tag.setdefault(r["query_tag"], []).append(r)
    chosen: list[dict] = []
    seen: set[str] = set()
    for items in by_tag.values():
        items.sort(key=lambda r: -int(r["stars"]))
        top = items[:3]
        lower = items[len(items) // 2:] or items
        pick = top + random.sample(lower, min(3, len(lower)))
        for r in pick:
            if r["full_name"] not in seen:
                seen.add(r["full_name"])
                chosen.append(r)
    random.shuffle(chosen)
    return chosen[:100]


def signals(readme: str, root_files: set[str]) -> dict:
    """Mechanical run-readiness signals from README text and root file names."""
    low = readme.lower()
    lower_files = {f.lower() for f in root_files}
    return {
        "has_dockerfile": int(any(f.startswith("dockerfile") or f == "docker-compose.yml" or f == "docker-compose.yaml" or f == "compose.yaml" for f in lower_files)),
        "has_devcontainer": int(".devcontainer" in lower_files),
        "has_deploy_badge": int(any(b in low for b in DEPLOY_BADGES)),
        "has_quickstart": int(bool(re.search(r"#+\s*(quick\s*start|quickstart|getting started|installation|install|usage)", low))),
        "needs_api_key": int(bool(re.search(r"api[_ -]?key|openai_api|anthropic_api|export \w+_key", low))),
        "has_pip_or_npm": int(bool(re.search(r"\bpip install\b|\bnpm (install|i)\b|\bnpx\b|\buvx?\b|\bbrew install\b|\bcargo install\b", low))),
        "has_lockfile": int(any(f in lower_files for f in ("package-lock.json", "pnpm-lock.yaml", "yarn.lock", "uv.lock", "poetry.lock", "pipfile.lock", "cargo.lock", "requirements.txt", "pyproject.toml"))),
        "has_ci": int(".github" in lower_files),
        "has_license_file": int(any(f.startswith("license") for f in lower_files)),
        "readme_words": len(readme.split()),
    }


def main() -> None:
    README_DIR.mkdir(parents=True, exist_ok=True)
    rows = list(csv.DictReader((ROOT / "data" / "candidate_repos.csv").open(encoding="utf-8")))
    chosen = sample(rows)
    out_rows: list[dict] = []
    for i, r in enumerate(chosen, 1):
        name = r["full_name"]
        readme_json = gh_json(f"repos/{name}/readme")
        readme = ""
        if isinstance(readme_json, dict) and readme_json.get("content"):
            readme = base64.b64decode(readme_json["content"]).decode("utf-8", errors="replace")
        (README_DIR / (name.replace("/", "__") + ".md")).write_text(readme, encoding="utf-8")
        tree = gh_json(f"repos/{name}/contents")
        root_files = {t["name"] for t in tree} if isinstance(tree, list) else set()
        out_rows.append({**r, **signals(readme, root_files), "readme_fetched": int(bool(readme)), "root_listed": int(bool(root_files))})
        if i % 20 == 0:
            LOG.info("%d/%d fetched", i, len(chosen))
    out_path = ROOT / "data" / "labelling_set.csv"
    with out_path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(out_rows[0].keys()))
        w.writeheader()
        w.writerows(out_rows)
    LOG.info("wrote %d repos to %s", len(out_rows), out_path)


if __name__ == "__main__":
    main()

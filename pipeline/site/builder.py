"""Render an escaped, portable static site and publish only complete builds."""

from __future__ import annotations

import json
import re
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import get_args
from urllib.parse import urlsplit

from jinja2 import Environment, PackageLoader, StrictUndefined, select_autoescape
from markdown_it import MarkdownIt

from pipeline.export import DEFAULT_OUTPUT_PATH, Listings
from pipeline.models import Level, Topic

DEFAULT_DIST = Path("site/dist")
SCORING_PATH = Path(__file__).resolve().parents[2] / "docs/scoring.md"
TOPICS = (*get_args(Topic), "pending")


def github_url(value: str) -> bool:
    """Allow only HTTPS GitHub URLs without credentials, ports or backslashes."""
    parsed = urlsplit(value)
    return (
        parsed.scheme == "https" and parsed.netloc == "github.com"
        and parsed.path.startswith("/") and "\\" not in value
        and not any(character.isspace() for character in value)
    )


def _scoring_html(path: Path) -> str:
    renderer = MarkdownIt("commonmark", {"html": False}).enable("table")
    tokens = renderer.parse(path.read_text(encoding="utf-8"))
    for token in tokens:
        for child in token.children or []:
            if child.type == "link_open" and not github_url(child.attrGet("href") or ""):
                # Keep the reference text without shipping dead relative links or
                # outbound destinations outside the site's GitHub-only policy.
                child.attrs.pop("href", None)
            elif child.type == "image":
                child.type, child.tag = "text", ""
                child.content = child.content or "Image omitted"
                child.children = None
    return renderer.renderer.render(tokens, renderer.options, {})


@contextmanager
def replace_directory(source: Path, destination: Path) -> Iterator[None]:
    """Swap a complete sibling tree; restore the previous tree on an ordinary error.

    Directory renames are atomic individually. Replacing a non-empty directory
    requires two renames on Windows, so process termination between them is not
    a filesystem transaction. The previous tree is retained until the caller exits.
    """
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(prefix=f".{destination.name}-previous-", dir=destination.parent) as temporary:
        backup = Path(temporary) / "site"
        existed = destination.exists()
        if existed:
            destination.replace(backup)
        try:
            source.replace(destination)
            yield
        except BaseException:
            if destination.exists():
                destination.replace(source)
            if existed:
                backup.replace(destination)
            raise


def build(
    input_path: Path = DEFAULT_OUTPUT_PATH, output_path: Path = DEFAULT_DIST, *,
    scoring_path: Path = SCORING_PATH,
) -> Path:
    """Build from Listings alone, preserving row order and replacing only on success."""
    document = Listings.model_validate_json(Path(input_path).read_bytes())
    output_path = Path(output_path)
    if output_path.resolve() in Path(input_path).resolve().parents:
        raise ValueError("Site output must not contain its input listings")
    groups = {topic: [] for topic in TOPICS}
    for row in document.listings:
        # GraphQL IDs, unlike names, survive repository renames. Reject unsafe
        # path segments without altering the shared publication schema.
        if not re.fullmatch(r"[A-Za-z0-9_-]+={0,2}", row.repo.github_id):
            raise ValueError("Repository ID is not a safe site route")
        if not github_url(str(row.repo.html_url)):
            raise ValueError("Repository URL must use https://github.com/")
        groups[row.topic or "pending"].append(row)
    environment = Environment(
        loader=PackageLoader("pipeline.site", "templates"),
        autoescape=select_autoescape(("html",)), undefined=StrictUndefined,
    )
    common = {"document": document, "levels": get_args(Level)}
    policy = _scoring_html(Path(scoring_path))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(prefix=f".{output_path.name}-build-", dir=output_path.parent) as temporary:
        staged = Path(temporary) / "site"
        staged.mkdir()

        def render(name: str, route: str, **context: object) -> None:
            path = staged / route
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(environment.get_template(name).render(
                **common, root="../" if "/" in route else "", **context,
            ), encoding="utf-8")

        render("index.html", "index.html", groups=groups, title="AI Hub")
        for topic, rows in groups.items():
            render("topic.html", f"topics/{topic}.html", topic=topic, rows=rows, title=topic)
        for row in document.listings:
            render("repo.html", f"repos/{row.repo.github_id}.html", row=row,
                   details=document.scoring_details[row.repo.github_id], title=row.repo.full_name)
        render("how_we_grade.html", "how_we_grade.html", policy=policy, title="How we grade")
        (staged / "status.json").write_text(json.dumps({
            "generated_at": document.generated_at.isoformat(), "run_id": document.run_id,
            "score_version": document.score_version, "listing_count": len(document.listings),
            "checks": [{"name": "listings_schema", "status": "passed"}],
        }, indent=2) + "\n", encoding="utf-8")
        with replace_directory(staged, output_path):
            pass
    return output_path

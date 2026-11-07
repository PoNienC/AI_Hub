"""Offline site gate for local links, HTML size and topic navigation."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from posixpath import normpath
from urllib.parse import unquote, urlsplit

from pipeline.site.builder import github_url, policy_url

MAX_HTML_BYTES = 200_000


class SiteCheckError(ValueError):
    """A site page failed a named, locally verifiable publication rule."""

    def __init__(self, rule: str, page: str, reason: str) -> None:
        self.rule = rule
        super().__init__(f"{page}: {reason}")


class _Links(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.references: list[str] = []
        self.has_base = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.has_base |= tag == "base"
        self.references.extend(value for name, value in attrs if name in {"href", "src"} and value is not None)


def check(dist: Path) -> None:
    """Require every internal href/src to resolve inside dist without network access.

    Fragments and query strings are allowed. Directory links resolve to their
    index.html; root-relative links resolve against the generated site root.
    """
    root = Path(dist).resolve()
    paths = sorted(root.rglob("*"))
    exact_files = {path.relative_to(root).as_posix() for path in paths if path.is_file()}
    if "index.html" not in exact_files:
        raise SiteCheckError("index", "index.html", "missing index page")
    has_topic = False
    for page in paths:
        if page.suffix.lower() != ".html":
            continue
        name = page.relative_to(root).as_posix()
        if not page.resolve().is_relative_to(root):
            raise SiteCheckError("links", name, "page escapes the site directory")
        try:
            if page.stat().st_size > MAX_HTML_BYTES:
                raise SiteCheckError("size", name, f"HTML exceeds {MAX_HTML_BYTES:,} bytes")
            parser = _Links()
            parser.feed(page.read_text(encoding="utf-8"))
        except (OSError, UnicodeError) as exc:
            raise SiteCheckError("html", name, f"cannot read HTML ({type(exc).__name__})") from None
        if parser.has_base:
            raise SiteCheckError("links", name, "base URLs are not supported")
        for reference in parser.references:
            try:
                url = urlsplit(reference)
            except ValueError:
                raise SiteCheckError("links", name, "malformed URL") from None
            if url.scheme or url.netloc:
                allowed = policy_url(reference) if name == "how_we_grade.html" else github_url(reference)
                if not allowed:
                    raise SiteCheckError("links", name, "outbound link is outside the page's allow-list")
                continue
            path = unquote(url.path)
            if "\\" in path or "\x00" in path:
                raise SiteCheckError("links", name, "invalid internal path")
            requested = ((root / path.lstrip("/")) if path.startswith("/") else
                         (page.parent / path) if path else page)
            target = requested.resolve()
            if target.is_dir():
                requested /= "index.html"
                target = (target / "index.html").resolve()
            if not target.is_relative_to(root) or not target.is_file():
                raise SiteCheckError("links", name, f"unresolved internal link: {reference}")
            # Check the spelling before resolve() canonicalises Windows paths.
            # Comparing the full relative name also catches directory case.
            if normpath(requested.relative_to(root).as_posix()) not in exact_files:
                raise SiteCheckError("links", name, f"internal link case mismatch: {reference}")
            if page == root / "index.html" and target.is_relative_to(root / "topics") and target.suffix == ".html":
                has_topic = True
    if not has_topic:
        raise SiteCheckError("topics", "index.html", "index must link to at least one topic")

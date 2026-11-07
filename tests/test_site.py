"""Offline rendering contracts, hostile inputs and publication retention."""

import json
import re
from html import unescape
from pathlib import Path

import pytest
from jinja2 import TemplateError

from pipeline.export import Listings
from pipeline.site import builder
from pipeline.site.links import SiteCheckError, check

SAMPLE = Path(__file__).parent / "fixtures/listings_sample.json"


@pytest.fixture
def sample():
    return Listings.model_validate_json(SAMPLE.read_bytes())


@pytest.fixture
def built(tmp_path):
    return builder.build(SAMPLE, tmp_path / "dist")


def save(document, tmp_path):
    path = tmp_path / "listings.json"
    path.write_text(document.model_dump_json(), encoding="utf-8")
    return path


def test_build_structure_and_status(built, sample):
    assert len(sample.listings) >= 20
    expected = {"index.html", "how_we_grade.html", "status.json"}
    expected |= {f"topics/{topic}.html" for topic in builder.TOPICS}
    expected |= {f"repos/{row.repo.github_id}.html" for row in sample.listings}
    assert {path.relative_to(built).as_posix() for path in built.rglob("*") if path.is_file()} == expected
    status = json.loads((built / "status.json").read_text(encoding="utf-8"))
    assert status == {
        "generated_at": sample.generated_at.isoformat(), "run_id": sample.run_id,
        "score_version": sample.score_version, "listing_count": len(sample.listings),
        "checks": [{"name": "listings_schema", "status": "passed"}],
    }
    assert "Date.now()" in (built / "index.html").read_text(encoding="utf-8")


@pytest.mark.parametrize("field", [
    "score", "coverage", "components", "licence", "push", "release", "label",
    "label_status", "tested", "github",
])
def test_repository_fields(built, sample, field):
    row = sample.listings[0]
    details = sample.scoring_details[row.repo.github_id]
    html = unescape((built / f"repos/{row.repo.github_id}.html").read_text(encoding="utf-8"))
    expected = {
        "score": ["Score", f"{row.score.total:.1f}/100"],
        "coverage": ["Coverage", f"{row.coverage * 100:.0f}%"],
        "components": ["Evaluated components and status", *details.component_statuses.values()],
        "licence": ["Licence class", details.licence_class, row.repo.licence_spdx or "unknown"],
        "push": ["Last push", row.repo.pushed_at.isoformat() if row.repo.pushed_at else "unknown"],
        "release": ["Latest release", row.repo.release_tag or "unknown",
                    row.repo.release_published_at.isoformat() if row.repo.release_published_at else "unknown"],
        "label": ["Label", row.topic or "pending", row.level or "pending"],
        "label_status": ["Label status", row.label_status],
        "tested": ["Tested status", row.tested],
        "github": [f'href="{row.repo.html_url}"', "View on GitHub"],
    }
    assert all(value in html for value in expected[field])
    if field == "components":
        for name, status in details.component_statuses.items():
            value = f"{row.score.components[name]:.1f}" if status == "present" else "Not evaluated"
            assert f"<th>{name.replace('_', ' ')}</th><td>{value}</td><td>{status}</td>" in html


def test_hostile_repository_text_escaped(sample, tmp_path):
    hostile = '<img src=x onerror="alert(1)"><script>alert(2)</script>&'
    row = sample.listings[0]
    row.repo.description = hostile
    row.repo.release_tag = hostile
    row.repo.licence_spdx = hostile
    built = builder.build(save(sample, tmp_path), tmp_path / "dist")
    html = (built / f"repos/{row.repo.github_id}.html").read_text(encoding="utf-8")
    assert hostile not in html
    assert "<img" not in html
    assert "&lt;img src=x onerror=&#34;alert(1)&#34;&gt;" in html
    assert "&lt;script&gt;alert(2)&lt;/script&gt;" in html


def test_order_and_top_ten_are_export_order(sample, tmp_path):
    sample.listings.reverse()
    for row in sample.listings:
        row.topic, row.level, row.label_status = "coding_agent", "beginner", "provisional"
    built = builder.build(save(sample, tmp_path), tmp_path / "dist")
    expected = [row.repo.github_id for row in sample.listings]
    index = (built / "index.html").read_text(encoding="utf-8")
    topic = (built / "topics/coding_agent.html").read_text(encoding="utf-8")
    assert re.findall(r'href="repos/([^"]+)\.html"', index) == expected[:10]
    assert re.findall(r'href="../repos/([^"]+)\.html"', topic) == expected


def test_empty_topic_and_pending_labels(sample, tmp_path):
    for row in sample.listings:
        row.topic, row.level, row.label_status = None, None, "pending"
    built = builder.build(save(sample, tmp_path), tmp_path / "dist")
    assert "No entries" in (built / "topics/coding_agent.html").read_text(encoding="utf-8")
    assert sample.listings[0].repo.github_id in (built / "topics/pending.html").read_text(encoding="utf-8")


def test_markdown_links_stripped_and_html_disabled(tmp_path):
    policy = tmp_path / "scoring.md"
    policy.write_text('[local](runbook.md) [external](https://example.org/) '
                      '[GitHub](https://github.com/owner/repo)\n\n'
                      '<script>alert(1)</script>\n\n![image](https://example.org/x.png)', encoding="utf-8")
    built = builder.build(SAMPLE, tmp_path / "dist", scoring_path=policy)
    html = (built / "how_we_grade.html").read_text(encoding="utf-8")
    assert 'href="runbook.md"' not in html
    assert "https://example.org" not in html
    assert 'href="https://github.com/owner/repo"' in html
    assert "<script>alert(1)</script>" not in html
    assert "&lt;script&gt;" in html
    assert "<img" not in html


@pytest.mark.parametrize("fault", ["render", "rename", "validation"])
def test_failed_build_retains_previous_dist(tmp_path, monkeypatch, fault):
    output = tmp_path / "dist"
    output.mkdir()
    (output / "old.html").write_text("previous site", encoding="utf-8")
    input_path = SAMPLE
    if fault == "render":
        original = builder.Environment.get_template

        def fail(self, name, *args, **kwargs):
            if name == "repo.html":
                raise TemplateError("render failed")
            return original(self, name, *args, **kwargs)

        monkeypatch.setattr(builder.Environment, "get_template", fail)
    elif fault == "rename":
        original = Path.replace

        def fail(self, destination):
            if self.name == "site" and "-build-" in self.parent.name:
                raise PermissionError("destination locked")
            return original(self, destination)

        monkeypatch.setattr(Path, "replace", fail)
    else:
        input_path = tmp_path / "invalid.json"
        input_path.write_text("{}", encoding="utf-8")
    with pytest.raises((TemplateError, OSError, ValueError)):
        builder.build(input_path, output)
    assert {path.name: path.read_text() for path in output.iterdir()} == {"old.html": "previous site"}
    assert not list(tmp_path.glob(".dist-*"))


def test_success_replaces_old_tree(tmp_path):
    output = tmp_path / "dist"
    output.mkdir()
    (output / "obsolete.html").write_text("old", encoding="utf-8")
    builder.build(SAMPLE, output)
    assert not (output / "obsolete.html").exists()
    assert (output / "index.html").is_file()


@pytest.mark.parametrize("url", ["https://evil.example/x", "https://github.com.evil.example/x",
                                 "https://github.com@evil.example/x", "http://github.com/x"])
def test_non_github_outbound_links_rejected(sample, tmp_path, url):
    payload = json.loads(sample.model_dump_json())
    payload["listings"][0]["repo"]["html_url"] = url
    path = tmp_path / "listings.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(ValueError, match="Repository URL"):
        builder.build(path, tmp_path / "dist")


def test_unsafe_id_rejected(sample, tmp_path):
    payload = json.loads(sample.model_dump_json())
    row = payload["listings"][0]
    old_id, new_id = row["repo"]["github_id"], "../escape"
    row["repo"]["github_id"] = row["score"]["repo_id"] = new_id
    details = payload["scoring_details"].pop(old_id)
    for evidence in details["evidence"]:
        evidence["repo_id"] = new_id
    payload["scoring_details"][new_id] = details
    path = tmp_path / "listings.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(ValueError, match="safe site route"):
        builder.build(path, tmp_path / "dist")


@pytest.mark.parametrize("reference", [
    "../index.html#top", "../status.json?view=1", "#heading", "", "/index.html",
    "../topics/", "../topics/space%20name.html", "https://github.com/owner/repo",
])
def test_internal_links_fragments_queries_and_github(built, reference):
    (built / "topics/index.html").write_text("<h1>Topics</h1>", encoding="utf-8")
    (built / "topics/space name.html").write_text("<h1>Space</h1>", encoding="utf-8")
    (built / "repos/link.html").write_text(f'<a href="{reference}">link</a>', encoding="utf-8")
    check(built)


@pytest.mark.parametrize("markup", [
    '<img src="missing.png">', '<a href="../../outside.html">escape</a>',
    '<a href="%2e%2e/%2e%2e/outside.html">encoded escape</a>',
    '<a href="javascript:alert(1)">script</a>', '<a href="//github.com/owner/repo">relative scheme</a>',
    '<a href="https://example.org/">external</a>', '<base href="https://github.com/">',
    '<a href="..%5Cindex.html">backslash</a>', '<a href="%00">nul</a>',
    '<a href="https://[broken">invalid</a>',
])
def test_links_reject_missing_or_unsafe_targets(built, markup):
    (built.parent / "outside.html").write_text("outside", encoding="utf-8")
    (built / "repos/link.html").write_text(markup, encoding="utf-8")
    with pytest.raises(SiteCheckError, match="repos/link.html"):
        check(built)


def test_page_size_limit_is_bytes_and_inclusive(built):
    path = built / "repos/size.html"
    path.write_text("é" * 100_000, encoding="utf-8")
    check(built)
    with path.open("a", encoding="utf-8") as handle:
        handle.write("x")
    with pytest.raises(SiteCheckError, match="size.html"):
        check(built)

"""Offline rendering contracts, hostile inputs and publication retention."""

import json
import re
from datetime import datetime
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
        "push": ["Last push", builder.display_date(row.repo.pushed_at)],
        "release": ["Latest release", row.repo.release_tag or "unknown",
                    builder.display_date(row.repo.release_published_at)],
        "label": ["Label", builder.topic_name(row.topic) if row.topic else "level not yet labelled",
                  row.level.replace("_", " ") if row.level else "level not yet labelled"],
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


def test_large_topic_pagination_preserves_every_row(sample, tmp_path):
    template = sample.listings[0]
    details = sample.scoring_details[template.repo.github_id]
    sample.listings, sample.scoring_details = [], {}
    for number in range(1500):
        row = template.model_copy(deep=True)
        repo_id = f"repo_{number}"
        row.repo.github_id = row.score.repo_id = repo_id
        row.repo.full_name = f"owner/repo_{number}"
        row.topic, row.level, row.label_status = None, None, "pending"
        sample.listings.append(row)
        cloned_details = details.model_copy(deep=True)
        for evidence in cloned_details.evidence:
            evidence.repo_id = repo_id
        sample.scoring_details[repo_id] = cloned_details
    built = builder.build(save(sample, tmp_path), tmp_path / "dist")
    routes = ["pending.html", *(f"pending_{page}.html" for page in range(2, 9))]
    observed = []
    for page, route in enumerate(routes):
        path = built / "topics" / route
        html = path.read_text(encoding="utf-8")
        ids = re.findall(r'href="../repos/([^"]+)\.html"', html)
        assert len(ids) == (100 if page == 7 else 200)
        observed.extend(ids)
        assert f'<ol start="{page * 200 + 1}">' in html
        assert path.stat().st_size <= 200_000
        assert ('rel="prev"' in html) == (page > 0)
        assert ('rel="next"' in html) == (page < 7)
        if page:
            assert f'href="{routes[page - 1]}" rel="prev"' in html
        if page < 7:
            assert f'href="{routes[page + 1]}" rel="next"' in html
    assert observed == [row.repo.github_id for row in sample.listings]
    check(built)


def test_backup_cleanup_failure_logs_without_failing_publication(tmp_path, monkeypatch, caplog):
    output, staged = tmp_path / "dist", tmp_path / "staged"
    output.mkdir()
    staged.mkdir()
    (output / "old.html").write_text("old", encoding="utf-8")
    (staged / "index.html").write_text("new", encoding="utf-8")

    def locked_cleanup(cls, name, ignore_errors=False, repeated=False):
        if not ignore_errors:
            raise PermissionError("previous site locked")

    monkeypatch.setattr(builder.TemporaryDirectory, "_rmtree", classmethod(locked_cleanup))
    with builder.replace_directory(staged, output):
        pass
    assert (output / "index.html").read_text(encoding="utf-8") == "new"
    assert "previous site clean-up incomplete" in caplog.text
    assert len(list(tmp_path.glob(".dist-previous-*/site/old.html"))) == 1


@pytest.mark.parametrize("host", sorted(builder.POLICY_HOSTS))
def test_policy_references_are_preserved_and_pass_gate(tmp_path, host):
    policy = tmp_path / "scoring.md"
    policy.write_text(f'[reference](https://{host}/docs#section)', encoding="utf-8")
    built = builder.build(SAMPLE, tmp_path / "dist", scoring_path=policy)
    html = (built / "how_we_grade.html").read_text(encoding="utf-8")
    assert f'href="https://{host}/docs#section"' in html
    check(built)
    (built / "repos/external.html").write_text(f'<a href="https://{host}/">ref</a>', encoding="utf-8")
    with pytest.raises(SiteCheckError, match="repos/external.html"):
        check(built)


@pytest.mark.parametrize("url", [
    "http://docs.deps.dev/", "https://docs.deps.dev.evil.example/",
    "https://docs.deps.dev@evil.example/", "https://docs.deps.dev:443/",
    "https://evil.example/", "https://docs.deps.dev/with space",
    "https://docs.deps.dev/\\escape",
])
def test_policy_disallows_unapproved_urls(built, url):
    assert not builder.policy_url(url)
    (built / "how_we_grade.html").write_text(f'<a href="{url}">ref</a>', encoding="utf-8")
    with pytest.raises(SiteCheckError, match="how_we_grade.html"):
        check(built)


def test_index_only_nonempty_topics_in_export_order_pending_last(sample, tmp_path):
    for index, row in enumerate(sample.listings):
        row.topic, row.level, row.label_status = None, None, "pending"
        if index in (1, 2):
            row.topic = "rag_knowledge" if index == 1 else "mcp_server_or_skill"
            row.level, row.label_status = "beginner", "provisional"
    built = builder.build(save(sample, tmp_path), tmp_path / "dist")
    html = (built / "index.html").read_text(encoding="utf-8")
    assert re.findall(r'<section data-topic="([^"]+)"', html) == [
        "rag_knowledge", "mcp_server_or_skill", "pending",
    ]
    assert "MCP server or skill" in html and "RAG knowledge" in html
    assert "beginner (provisional)" in html
    assert "level not yet labelled" in html
    assert "pending · pending" not in html
    assert "pending · pending" not in (built / "topics/pending.html").read_text(encoding="utf-8")
    assert "<title>AI Hub</title>" in html
    assert "<title>MCP server or skill · AI Hub</title>" in (
        built / "topics/mcp_server_or_skill.html"
    ).read_text(encoding="utf-8")


def test_index_retains_top_ten_per_selected_level(sample, tmp_path):
    for index, row in enumerate(sample.listings):
        row.topic, row.label_status = "coding_agent", "provisional"
        row.level = "beginner" if index < 12 else "advanced"
    built = builder.build(save(sample, tmp_path), tmp_path / "dist")
    html = (built / "index.html").read_text(encoding="utf-8")
    rows = re.findall(r'<li data-views="([^"]+)"( hidden)?><a href="repos/([^"]+)\.html"', html)
    assert [repo_id for _, hidden, repo_id in rows if not hidden] == [
        row.repo.github_id for row in sample.listings[:10]
    ]
    for level, expected in (("beginner", sample.listings[:10]), ("advanced", sample.listings[12:22])):
        assert [repo_id for views, _, repo_id in rows if level in views.split()] == [
            row.repo.github_id for row in expected
        ]
    assert all("intermediate" not in views.split() for views, _, _ in rows)


def test_empty_index_has_one_empty_state(sample, tmp_path):
    sample.listings = []
    built = builder.build(save(sample, tmp_path), tmp_path / "dist")
    html = (built / "index.html").read_text(encoding="utf-8")
    assert '<section data-topic=' not in html
    assert '<p id="empty">No entries for this level.</p>' in html
    assert html.count("No entries") == 1


def test_display_dates_use_english_utc_and_status_keeps_iso(sample, tmp_path):
    timestamp = datetime.fromisoformat("2026-11-07T00:15:32.123456+02:00")
    sample.generated_at = timestamp
    row = sample.listings[0]
    row.repo.pushed_at = row.repo.release_published_at = timestamp
    built = builder.build(save(sample, tmp_path), tmp_path / "dist")
    html = (built / f"repos/{row.repo.github_id}.html").read_text(encoding="utf-8")
    assert "<dd>06 Nov 2026</dd>" in html
    assert " · 06 Nov 2026</dd>" in html
    assert ">06 Nov 2026 22:15 UTC</time>" in html
    assert f'datetime="{timestamp.isoformat()}"' in html
    assert json.loads((built / "status.json").read_text(encoding="utf-8"))["generated_at"] == timestamp.isoformat()
    assert builder.display_date(None) == "unknown"

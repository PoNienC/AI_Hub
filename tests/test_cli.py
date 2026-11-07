"""Offline CLI integration: ordering, failure history and publication isolation."""

import copy
import json
import logging
import sqlite3
from contextlib import closing
from datetime import UTC, datetime
from pathlib import Path

import httpx
import pytest

from pipeline import cli, release
from pipeline.config import NICHE_DEFAULT, QUERIES, Settings
from pipeline.export import Listings
from pipeline.failure import RunFailure
from pipeline.gates import GateFailure
from pipeline.store import StateStore

NOW = datetime(2026, 11, 7, 12, tzinfo=UTC)


@pytest.fixture
def setup(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    labels = tmp_path / "data/labelled_repos_for_review.csv"
    labels.parent.mkdir()
    labels.write_text("full_name,topic,level\n", encoding="utf-8")
    settings = Settings(github_token="offline-secret", http_retries=0)
    monkeypatch.setattr(cli.Settings, "from_env", lambda: settings)
    return settings


@pytest.fixture
def offline(load_fixture):
    requests = []
    base = load_fixture("github_page_1.json")
    enrichments = load_fixture("enrichment_responses.json")

    def handler(request):
        requests.append(request)
        if request.url.host == "api.github.com":
            payload = copy.deepcopy(base)
            first = json.loads(request.content)["variables"]["first"]
            node = base["data"]["search"]["nodes"][0]
            nodes = []
            for index in range(min(first, 5)):
                item = copy.deepcopy(node)
                item.update(id=f"R_{index}", nameWithOwner=f"example/repo{index}",
                            url=f"https://github.com/example/repo{index}")
                nodes.append(item)
            payload["data"]["search"]["nodes"] = nodes
            payload["data"]["search"]["pageInfo"] = {"hasNextPage": False, "endCursor": None}
            return httpx.Response(200, json=payload)
        source = {
            "api.deps.dev": "deps_dev", "api.scorecard.dev": "scorecard",
            "huggingface.co": "hugging_face", "hn.algolia.com": "hacker_news",
        }[request.url.host]
        response = enrichments[source]["absent"]
        return httpx.Response(response["status_code"], json=response["body"])

    with httpx.Client(transport=httpx.MockTransport(handler)) as client:
        yield client, requests


def seed_state(settings, repo, count=5):
    with StateStore(settings.state_dir) as store:
        store.upsert_repo(repo, observed_at=NOW)
        store.start_run("previous", started_at=NOW, budgets={})
        store.finish_run("previous", finished_at=NOW, status="succeeded", budgets={},
                         rows_in=count, rows_out=count, gate_results={"gate_2": True, "gate_3": True})
        store.promote({"gate_2": True, "gate_3": True})
    (settings.state_dir / "evidence.jsonl").write_bytes(b"previous evidence")
    output = Path("site/src/data/listings.json")
    output.parent.mkdir(parents=True)
    output.write_bytes(b"previous listings")
    index = Path("site/dist/index.html")
    index.parent.mkdir(parents=True)
    index.write_bytes(b"previous site")
    return [settings.state_dir / "gateway.sqlite", settings.state_dir / "evidence.jsonl", output, index]


def failures(settings):
    return [RunFailure.model_validate_json(line) for line in
            (settings.state_dir / "failures.jsonl").read_text(encoding="utf-8").splitlines()]


@pytest.mark.parametrize("existing", [True, False])
def test_dry_run_offline_limit_five_preserves_production(setup, offline, repo, monkeypatch, existing):
    paths = seed_state(setup, repo) if existing else [Path("state/gateway.sqlite"), Path("state/evidence.jsonl"), Path("site/src/data/listings.json")]
    before = [path.read_bytes() if path.exists() else None for path in paths]
    monkeypatch.setattr(release, "pull", lambda *_: pytest.fail("dry run pulled"))
    monkeypatch.setattr(release, "push", lambda *_: pytest.fail("dry run uploaded"))
    monkeypatch.setattr(StateStore, "promote", lambda *_: pytest.fail("dry run promoted"))
    client, requests = offline
    assert cli.main(["run", "--dry-run", "--limit", "5"], client=client) == 0
    assert [path.read_bytes() if path.exists() else None for path in paths] == before
    output = Path("site/src/data/listings.dry.json")
    document = Listings.model_validate_json(output.read_bytes())
    assert len(document.listings) == 5
    dist = Path("site/dist.dry")
    assert len(list((dist / "repos").glob("*.html"))) == 5
    assert (dist / "index.html").is_file()
    assert Path("site/dist").exists() is existing
    status = json.loads((dist / "status.json").read_text(encoding="utf-8"))
    assert status["run_id"] == document.run_id
    assert {check["name"] for check in status["checks"]} == {"listings_schema", "gate_2", "gate_3", "gate_5"}
    lines = output.with_suffix(".evidence.jsonl").read_text(encoding="utf-8").splitlines()
    assert len(lines) == 20
    assert {json.loads(line)["run_id"] for line in lines} == {document.run_id}
    assert not list(Path("state").glob(".run-*"))
    assert not Path("state/gateway.work.sqlite").exists()
    assert len(requests) == len(NICHE_DEFAULT) + 20


def test_real_run_order_and_success_log(setup, offline, monkeypatch):
    events = []
    monkeypatch.setattr(release, "pull", lambda *_: events.append("pull"))
    for owner, name, event in [
        (cli.GitHubSource, "search", "ingest"), (cli, "score_repo", "score"),
        (cli, "write_listings", "export"), (cli, "check_gates", "gates"),
        (cli, "build_site", "site"), (cli, "gate_5", "gate_5"),
        (StateStore, "promote", "promote"),
    ]:
        original = getattr(owner, name)

        def wrapper(*args, _original=original, _event=event, **kwargs):
            events.append(_event)
            return _original(*args, **kwargs)

        monkeypatch.setattr(owner, name, wrapper)
    for adapter in cli.ADAPTERS:
        original = adapter.fetch

        def enrich(*args, _original=original, **kwargs):
            events.append("enrich")
            return _original(*args, **kwargs)

        monkeypatch.setattr(adapter, "fetch", enrich)

    def pushed(directory):
        events.append("push")
        assert release.validate_bundle(directory)
        assert Path("site/src/data/listings.json").exists()

    monkeypatch.setattr(release, "push", pushed)
    assert cli.main(["run", "--limit", "1"], client=offline[0]) == 0
    assert events == ["pull", "ingest", *(["enrich"] * 4), "score", "export", "site", "gates", "gate_5", "promote", "push"]
    with closing(sqlite3.connect(setup.state_dir / "gateway.sqlite")) as conn:
        status, rows_in, rows_out, gates = conn.execute(
            "SELECT status, rows_in, rows_out, gate_results_json FROM run_log"
        ).fetchone()
        assert (status, rows_in, rows_out) == ("succeeded", 1, 1)
        assert json.loads(gates) == {"gate_2": True, "gate_3": True, "gate_5": True}
        assert conn.execute("SELECT COUNT(*) FROM snapshots").fetchone()[0] == 1
        assert conn.execute("SELECT COUNT(*) FROM scores").fetchone()[0] == 1
    assert cli.main(["gates"]) == 0


@pytest.mark.parametrize("fault", ["gate_2", "gate_3", "gate_5", "github_budget", "http_budget", "export"])
def test_failure_rolls_back_and_appends_once(setup, offline, repo, monkeypatch, fault):
    paths = seed_state(setup, repo)
    before = [path.read_bytes() for path in paths]
    monkeypatch.setattr(release, "push", lambda *_: pytest.fail("failed run uploaded"))
    if fault == "gate_5":
        original = cli.build_site

        def broken(*args, **kwargs):
            dist = original(*args, **kwargs)
            (dist / "broken.html").write_text('<a href="missing.html">broken</a>', encoding="utf-8")
            return dist

        monkeypatch.setattr(cli, "build_site", broken)
    elif fault.startswith("gate_"):
        def rejected(*args, **kwargs):
            raise GateFailure(fault, "fixture", "rejected")
        monkeypatch.setattr(cli, "check_gates", rejected)
    elif fault == "github_budget":
        setup.github_point_limit = 0
    elif fault == "http_budget":
        setup.http_call_limits["deps_dev"] = 0
    else:
        Path("data/labelled_repos_for_review.csv").unlink()
    for attempt in range(2):
        assert cli.main(["run", "--no-release", "--limit", "5"], client=offline[0]) == 1
        recorded = failures(setup)
        assert len(recorded) == attempt + 1
        assert [path.read_bytes() for path in paths] == before
        latest = recorded[-1]
        assert latest.finished >= latest.started
        assert Path(latest.log_path).is_file()
        assert (setup.state_dir / "failure-title.txt").read_text(encoding="utf-8").strip() == latest.issue_title
        assert (setup.state_dir / "failure-body.md").read_text(encoding="utf-8") == latest.issue_body
        assert "offline-secret" not in latest.model_dump_json()
        if fault == "gate_5":
            assert latest.failed_step == "gate_5"
            assert "broken.html" in latest.reason
    assert recorded[0].run_id != recorded[1].run_id
    assert not Path("state/gateway.work.sqlite").exists()


@pytest.mark.parametrize("transfer", [False, True])
def test_count_uses_previous_success_and_catches_drop(setup, offline, repo, monkeypatch, transfer):
    paths = seed_state(setup, repo, count=6)
    before = [path.read_bytes() for path in paths]
    pulls = []
    monkeypatch.setattr(release, "pull", lambda directory: pulls.append(directory) or False)
    monkeypatch.setattr(release, "push", lambda *_: pytest.fail("failed run uploaded"))
    failure = cli.run_pipeline(setup, transfer=transfer, client=offline[0], limit=5)
    assert failure.failed_step == "gate_3"
    assert (failure.previous_count, failure.rows_in, failure.rows_out) == (6, 5, 5)
    assert pulls == ([setup.state_dir] if transfer else [])
    assert [path.read_bytes() for path in paths] == before


def test_baseline_failure_has_its_own_stage(setup, offline, monkeypatch):
    monkeypatch.setattr(release, "pull", lambda *_: False)

    def fail(*args):
        raise sqlite3.DatabaseError("baseline cannot be read")

    monkeypatch.setattr(cli, "previous_count", fail)
    failure = cli.run_pipeline(setup, client=offline[0], limit=1)
    assert failure.failed_step == "baseline"
    assert not offline[1]


def test_stale_copy_preflight_preserves_file_and_names_removal(setup, offline, monkeypatch, caplog):
    setup.state_dir.mkdir()
    path = setup.state_dir / "gateway.work.sqlite"
    path.write_bytes(b"preserve")
    monkeypatch.setattr(release, "pull", lambda *_: pytest.fail("preflight must precede pull"))
    assert cli.main(["run"], client=offline[0]) == 1
    assert path.read_bytes() == b"preserve"
    assert str(path) in caplog.text
    assert f"Remove-Item -LiteralPath '{path}'" in caplog.text
    assert failures(setup)[0].failed_step == "preflight"
    assert not offline[1]


def test_all_queries_and_no_release(setup, offline, monkeypatch):
    monkeypatch.setattr(release, "pull", lambda *_: pytest.fail("transfer disabled"))
    monkeypatch.setattr(release, "push", lambda *_: pytest.fail("transfer disabled"))
    assert cli.main(["run", "--no-release", "--all-queries", "--limit", "1"], client=offline[0]) == 0
    queries = [json.loads(request.content)["variables"]["query"] for request in offline[1]
               if request.url.host == "api.github.com"]
    assert queries == list(QUERIES.values())


def test_push_failure_records_failure_but_keeps_gated_local_bundle(setup, offline, monkeypatch):
    monkeypatch.setattr(release, "pull", lambda *_: False)

    def fail(*args):
        raise release.ReleaseError("Upload failed; retry release push")

    monkeypatch.setattr(release, "push", fail)
    failure = cli.run_pipeline(setup, client=offline[0], limit=1)
    assert failure.failed_step == "release.push"
    assert release.validate_bundle(setup.state_dir)
    assert len(failures(setup)) == 1


def test_output_io_failure_restores_local_database_and_evidence(setup, offline, repo, monkeypatch):
    paths = seed_state(setup, repo)
    before = [path.read_bytes() for path in paths]
    original = release.replace_file

    def fail_output(source, destination):
        if destination == Path("site/src/data/listings.json"):
            raise PermissionError("output locked")
        original(source, destination)

    monkeypatch.setattr(release, "replace_file", fail_output)
    failure = cli.run_pipeline(setup, transfer=False, client=offline[0], limit=5)
    assert failure.failed_step == "promote"
    assert [path.read_bytes() for path in paths] == before


@pytest.mark.parametrize("command", [["release", "pull"], ["release", "push"]])
def test_standalone_command_errors_have_issue_files(setup, monkeypatch, command):
    def fail(*args):
        raise release.ReleaseError("Transfer failed")
    monkeypatch.setattr(release, "pull", fail)
    monkeypatch.setattr(release, "push", fail)
    assert cli.main(command) == 1
    assert len(failures(setup)) == 1


@pytest.mark.parametrize("command", [["run"], ["release", "pull"], ["release", "push"]])
def test_exception_details_reach_only_diagnostic_file(setup, offline, monkeypatch, caplog, command):
    detail = "diagnostic detail for the operator"

    def fail(*args, **kwargs):
        raise ValueError(detail)

    caplog.set_level(logging.DEBUG)
    if command == ["run"]:
        monkeypatch.setattr(release, "pull", lambda *_: False)
        monkeypatch.setattr(cli.GitHubSource, "search", fail)
    else:
        monkeypatch.setattr(release, command[1], fail)
    assert cli.main(command, client=offline[0]) == 1
    failure = failures(setup)[0]
    diagnostic = Path(failure.log_path).read_text(encoding="utf-8")
    assert "Traceback (most recent call last):" in diagnostic
    assert f"ValueError: {detail}" in diagnostic
    assert "DEBUG" in diagnostic
    assert detail not in caplog.text
    assert detail not in failure.model_dump_json()
    assert detail not in (setup.state_dir / "failure-body.md").read_text(encoding="utf-8")


@pytest.mark.parametrize("existing", [False, True])
@pytest.mark.parametrize("fault", ["schema", "settings"])
def test_failed_gates_command_is_read_only(setup, repo, tmp_path, monkeypatch, existing, fault):
    if existing:
        seed_state(setup, repo)
        for name in ("failures.jsonl", "failure-title.txt", "failure-body.md"):
            (setup.state_dir / name).write_text("previous failure", encoding="utf-8")
    if fault == "settings":
        def fail():
            raise ValueError("invalid settings")
        monkeypatch.setattr(cli.Settings, "from_env", fail)
    before = {path: path.read_bytes() for path in tmp_path.rglob("*") if path.is_file()}
    assert cli.main(["gates", "--path", "missing.json"]) == 1
    assert {path: path.read_bytes() for path in tmp_path.rglob("*") if path.is_file()} == before
    assert setup.state_dir.exists() is existing


@pytest.mark.parametrize("action", ["pull", "push"])
def test_standalone_release_success(setup, monkeypatch, action):
    called = []
    monkeypatch.setattr(release, action, lambda directory: called.append(directory) or True)
    assert cli.main(["release", action]) == 0
    assert called == [setup.state_dir]


def test_invalid_settings_do_not_leak_secret(setup, monkeypatch, caplog):
    def invalid():
        return Settings(github_token="offline-secret", per_query_cap=-1)
    monkeypatch.setattr(cli.Settings, "from_env", invalid)
    assert cli.main(["run"]) == 1
    assert "offline-secret" not in caplog.text
    assert "Invalid settings" in failures(setup)[0].reason


@pytest.mark.parametrize("value", ["0", "-1", "bad"])
def test_invalid_limit_exits_two(setup, value):
    with pytest.raises(SystemExit) as caught:
        cli.main(["run", "--limit", value])
    assert caught.value.code == 2


@pytest.mark.parametrize("defaults", [False, True])
def test_site_build_needs_no_settings_or_credentials(tmp_path, monkeypatch, defaults):
    sample = Path(__file__).parent / "fixtures/listings_sample.json"
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(cli.Settings, "from_env", lambda: pytest.fail("site build loaded settings"))
    monkeypatch.delenv("GH_TOKEN", raising=False)
    if defaults:
        source = Path("site/src/data/listings.json")
        source.parent.mkdir(parents=True)
        source.write_bytes(sample.read_bytes())
        args, output = ["site", "build"], Path("site/dist")
    else:
        output = tmp_path / "preview"
        args = ["site", "build", "--input", str(sample), "--output", str(output)]
    assert cli.main(args) == 0
    assert (output / "index.html").is_file()
    assert not Path("state").exists()


def test_failed_site_build_returns_one_and_retains_site(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    output = Path("site/dist")
    output.mkdir(parents=True)
    (output / "index.html").write_bytes(b"previous")
    assert cli.main(["site", "build", "--input", "missing.json"]) == 1
    assert (output / "index.html").read_bytes() == b"previous"
    assert not Path("state").exists()


def test_site_swap_failure_rolls_back_without_promotion(setup, offline, repo, monkeypatch):
    paths = seed_state(setup, repo)
    before = [path.read_bytes() for path in paths]
    original = Path.replace

    def locked(self, destination):
        if self.name == "site" and self.parent.name.startswith(".pipeline-site-"):
            raise PermissionError("site locked")
        return original(self, destination)

    monkeypatch.setattr(Path, "replace", locked)
    monkeypatch.setattr(StateStore, "promote", lambda *_: pytest.fail("site swap failed before promotion"))
    failure = cli.run_pipeline(setup, transfer=False, client=offline[0], limit=5)
    assert failure.failed_step == "promote"
    assert [path.read_bytes() for path in paths] == before
    assert not list(Path("site").glob(".*-site-*"))

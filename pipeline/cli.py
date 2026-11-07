"""Command-line orchestration of bounded ingestion, gates and release transfers."""

from __future__ import annotations

import argparse
import json
import logging
import os
import shutil
import sqlite3
from collections.abc import Callable, Sequence
from contextlib import ExitStack, closing
from datetime import UTC, datetime
from pathlib import Path
from tempfile import TemporaryDirectory
from uuid import uuid4

import httpx
from jinja2 import TemplateError
from pydantic import ValidationError

from pipeline import release
from pipeline.budgets import Budget, BudgetExceeded
from pipeline.config import Settings
from pipeline.export import DEFAULT_LABELS_PATH, DEFAULT_OUTPUT_PATH, build_listings, write_listings
from pipeline.failure import RunFailure, abort_run
from pipeline.gates import GateFailure, check_gates, gate_2, gate_5
from pipeline.http import HttpClient, HttpRequestError
from pipeline.models import Snapshot
from pipeline.scoring import score_repo
from pipeline.site.builder import DEFAULT_DIST, build as build_site, replace_directory
from pipeline.sources import deps_dev, hacker_news, hugging_face, scorecard
from pipeline.sources.github import GitHubResponseError, GitHubSource
from pipeline.store import PromotionError, StateStore

LOG = logging.getLogger("pipeline.cli")
ADAPTERS = (deps_dev, scorecard, hugging_face, hacker_news)
EXPECTED_ERRORS = (
    OSError, ValueError, sqlite3.Error, BudgetExceeded, GateFailure,
    HttpRequestError, GitHubResponseError, PromotionError, release.ReleaseError, TemplateError,
)


def _now() -> datetime:
    return datetime.now(UTC)


def previous_count(database: Path, *, exclude_run_id: str = "") -> int | None:
    """Read the latest successful baseline without creating or mutating state."""
    if not database.exists():
        return None
    with closing(sqlite3.connect(database.resolve().as_uri() + "?mode=ro", uri=True)) as conn:
        row = conn.execute(
            "SELECT rows_out FROM run_log WHERE status = 'succeeded' AND run_id != ? "
            "ORDER BY rowid DESC LIMIT 1", (exclude_run_id,),
        ).fetchone()
    return row[0] if row else None


def record_failure(failure: RunFailure, state_dir: Path) -> None:
    """Append one failed run and render the workflow's issue files from that record."""
    state_dir.mkdir(parents=True, exist_ok=True)
    with (state_dir / "failures.jsonl").open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(failure.model_dump_json() + "\n")
        handle.flush()
        os.fsync(handle.fileno())
    (state_dir / "failure-title.txt").write_text(failure.issue_title + "\n", encoding="utf-8")
    (state_dir / "failure-body.md").write_text(failure.issue_body, encoding="utf-8")


def _log_exception(log_path: Path, run_id: str, error: Exception) -> None:
    """Append a diagnostic traceback directly to a file, never to console handlers."""
    log_path.parent.mkdir(parents=True, exist_ok=True)
    handler = logging.FileHandler(log_path, encoding="utf-8")
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s"))
    try:
        record = LOG.makeRecord(
            LOG.name, logging.DEBUG, __file__, 0, "Run %s failed", (run_id,),
            (type(error), error, error.__traceback__),
        )
        handler.handle(record)
    finally:
        handler.close()


def _publish(store: StateStore, staged: Path, output: Path, gates: dict[str, bool]) -> None:
    """Promote state and publish gated files, restoring local files on I/O failure."""
    canonical = store.canonical_path
    backup = staged / "previous.sqlite"
    existed = canonical.exists()
    if existed:
        shutil.copyfile(canonical, backup)
    store.promote(gates)
    try:
        release.replace_bundle([
            (staged / "evidence.jsonl", store.state_dir / "evidence.jsonl"),
            (staged / "listings.json", output),
        ], staged)
    except OSError:
        if existed:
            release.replace_file(backup, canonical)
        else:
            canonical.unlink(missing_ok=True)
        raise


def run_pipeline(
    settings: Settings, *, limit: int | None = None, dry_run: bool = False,
    all_queries: bool = False, transfer: bool = True, client: httpx.Client | None = None,
    labels_path: Path = DEFAULT_LABELS_PATH, output_path: Path = DEFAULT_OUTPUT_PATH,
    clock: Callable[[], datetime] = _now,
) -> RunFailure | None:
    """Run the pipeline; injected HTTP clients make complete offline tests possible.

    A limit caps unique repositories enriched and bounds each search query. Dry
    runs copy local history into temporary state, never contact gh and write only
    listings.dry.json, its sibling evidence and site/dist.dry. Successful run_log is finalised
    before promotion because B1 closes the store on promotion. Transfer failures
    after promotion are recorded separately and leave the local gated bundle.
    """
    if limit is not None and (type(limit) is not int or limit <= 0):
        raise ValueError("limit must be a positive integer")
    run_id, started = uuid4().hex, clock()
    state_dir = settings.state_dir
    log_path = state_dir / "logs" / f"{run_id}.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    handler = logging.FileHandler(log_path, encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s"))
    pipeline_logger = logging.getLogger("pipeline")
    old_level = pipeline_logger.level
    pipeline_logger.setLevel(logging.INFO)
    pipeline_logger.addHandler(handler)
    budget = Budget.from_settings(settings)
    store = None
    stage, rows_in, rows_out, baseline = "preflight", 0, 0, None
    try:
        release.preflight(state_dir)
        if transfer and not dry_run:
            stage = "release.pull"
            release.pull(state_dir)
        stage = "baseline"
        baseline = previous_count(state_dir / "gateway.sqlite")
        with TemporaryDirectory(prefix=".run-", dir=state_dir) as temporary, ExitStack() as site_stack:
            staged = Path(temporary)
            working_dir = staged / "state" if dry_run else state_dir
            if dry_run:
                working_dir.mkdir()
                if (state_dir / "gateway.sqlite").exists():
                    shutil.copyfile(state_dir / "gateway.sqlite", working_dir / "gateway.sqlite")
            stage = "store"
            with StateStore(working_dir) as store:
                store.start_run(run_id, started_at=started, budgets=budget.snapshot())
                stage = "ingest"
                LOG.info("Run %s: ingest", run_id)
                with GitHubSource(settings, budget=budget, client=client) as source:
                    repos = source.search(
                        all_queries=all_queries,
                        per_query_cap=min(settings.per_query_cap, limit) if limit else None,
                    )
                repos = repos[:limit] if limit is not None else repos
                rows_in = len(repos)
                observed = clock()
                for repo in repos:
                    store.upsert_repo(repo, observed_at=observed)
                    store.add_snapshot(Snapshot(
                        repo_id=repo.github_id, run_id=run_id, observed_at=observed,
                        stars=repo.stars, forks=repo.forks, open_issues=repo.open_issues,
                        pushed_at=repo.pushed_at,
                    ))
                stage = "enrich"
                LOG.info("Run %s: enrich %d repositories", run_id, rows_in)
                evidence = {}
                with HttpClient(budget, client=client, timeout_seconds=settings.http_timeout_seconds,
                                retries=settings.http_retries) as http:
                    for repo in repos:
                        evidence[repo.github_id] = [adapter.fetch(repo, http, fetched_at=clock()) for adapter in ADAPTERS]
                stage = "score"
                scored_at = clock()
                results = [score_repo(
                    repo, evidence[repo.github_id], run_id=run_id, now=scored_at,
                    velocity=store.velocity(repo.github_id, window_hours=168),
                ) for repo in repos]
                for result in results:
                    store.add_score(result.score)
                stage = "export"
                document = build_listings(repos, results, run_id=run_id, generated_at=clock(), labels_path=labels_path)
                rows_out = len(document.listings)
                path = write_listings(document, staged / "listings.json", evidence_path=staged / "evidence.jsonl")
                stage = "site.build"
                site_output = DEFAULT_DIST.with_name("dist.dry") if dry_run else DEFAULT_DIST
                site_output.parent.mkdir(parents=True, exist_ok=True)
                site_temporary = site_stack.enter_context(TemporaryDirectory(
                    prefix=".pipeline-site-", dir=site_output.parent,
                ))
                site_staged = build_site(path, Path(site_temporary) / "site")
                stage = "gates"
                gates = check_gates(path, previous_count=baseline, now=clock())
                gate_5(site_staged)
                gates["gate_5"] = True
                status_path = site_staged / "status.json"
                status = json.loads(status_path.read_text(encoding="utf-8"))
                status["checks"].extend({"name": name, "status": "passed"} for name in gates)
                status_path.write_text(json.dumps(status, indent=2) + "\n", encoding="utf-8")
                LOG.info("Run %s: gates passed; rows_in=%d rows_out=%d budgets=%s", run_id, rows_in, rows_out, budget.snapshot())
                stage = "publish.dry" if dry_run else "promote"
                with replace_directory(site_staged, site_output):
                    if dry_run:
                        output = output_path.with_name(output_path.stem + ".dry.json")
                        release.replace_bundle([
                            (path, output),
                            (staged / "evidence.jsonl", output.with_suffix(".evidence.jsonl")),
                        ], staged)
                    else:
                        store.finish_run(
                            run_id, finished_at=clock(), status="succeeded", budgets=budget.snapshot(),
                            rows_in=rows_in, rows_out=rows_out, gate_results=gates,
                        )
                        _publish(store, staged, output_path, gates)
            if transfer and not dry_run:
                stage = "release.push"
                release.push(state_dir)
        LOG.info("Run %s completed%s", run_id, " (dry run)" if dry_run else "")
        return None
    except EXPECTED_ERRORS as exc:
        failure = abort_run(
            exc, store=store, stage=stage, run_id=run_id, started=started, finished=clock(),
            rows_in=rows_in, rows_out=rows_out, previous_count=baseline,
            log_path=str(log_path), budgets=budget.snapshot(),
        )
        if isinstance(exc, (release.ReleaseError, GitHubResponseError, HttpRequestError)):
            failure.reason = str(exc)
        _log_exception(log_path, run_id, exc)
        LOG.error("%s\n%s", failure.issue_title, failure.issue_body)
        record_failure(failure, state_dir)
        return failure
    finally:
        pipeline_logger.removeHandler(handler)
        pipeline_logger.setLevel(old_level)
        handler.close()


def _positive(value: str) -> int:
    number = int(value)
    if number <= 0:
        raise argparse.ArgumentTypeError("limit must be positive")
    return number


def main(argv: Sequence[str] | None = None, *, client: httpx.Client | None = None) -> int:
    """Expose run, gates, release and site commands; return 1 on operational failure."""
    parser = argparse.ArgumentParser(prog="pipeline")
    commands = parser.add_subparsers(dest="command", required=True)
    run = commands.add_parser("run", help="Ingest, gate and publish repository data")
    run.add_argument("--limit", type=_positive)
    run.add_argument("--dry-run", action="store_true")
    run.add_argument("--all-queries", action="store_true")
    run.add_argument("--no-release", action="store_true", help="Use local state; transfer explicitly in CI")
    gates = commands.add_parser("gates", help="Validate an existing export against the previous good count")
    gates.add_argument("--path", type=Path, default=DEFAULT_OUTPUT_PATH)
    releases = commands.add_parser("release", help="Transfer the promoted state and evidence")
    releases.add_argument("action", choices=("pull", "push"))
    site = commands.add_parser("site", help="Build static pages without credentials")
    site_commands = site.add_subparsers(dest="action", required=True)
    site_build = site_commands.add_parser("build", help="Render the validated listings")
    site_build.add_argument("--input", type=Path, default=DEFAULT_OUTPUT_PATH)
    site_build.add_argument("--output", type=Path, default=DEFAULT_DIST)
    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    started = _now()
    settings = None
    try:
        if args.command == "site":
            build_site(args.input, args.output)
            LOG.info("Site built: %s", args.output)
            return 0
        settings = Settings.from_env()
        if args.command == "run":
            return int(run_pipeline(
                settings, limit=args.limit, dry_run=args.dry_run, all_queries=args.all_queries,
                transfer=not args.no_release, client=client,
            ) is not None)
        if args.command == "gates":
            document = gate_2(args.path)
            baseline = previous_count(settings.state_dir / "gateway.sqlite", exclude_run_id=document.run_id)
            check_gates(args.path, previous_count=baseline)
            gate_5(DEFAULT_DIST.with_name("dist.dry") if args.path.stem.endswith(".dry") else DEFAULT_DIST)
            LOG.info("Gates 2, 3 and 5 passed")
        elif args.action == "pull":
            LOG.info("Release %s", "downloaded" if release.pull(settings.state_dir) else "absent; first run")
        else:
            release.push(settings.state_dir)
            LOG.info("Release upload verified")
        return 0
    except EXPECTED_ERRORS as exc:
        if args.command == "site":
            LOG.error("Site build failed: %s", type(exc).__name__)
            return 1
        state_dir = settings.state_dir if settings is not None else Path("state")
        run_id = uuid4().hex
        log_path = state_dir / "logs" / f"{run_id}.log"
        failure = abort_run(
            exc, store=None, stage=f"release.{args.action}" if args.command == "release" else args.command,
            run_id=run_id, started=started, finished=_now(), rows_in=0, rows_out=0,
            log_path=(os.environ.get("PIPELINE_LOG_URL", "Actions or terminal command output")
                      if args.command == "gates" else str(log_path)),
        )
        if isinstance(exc, release.ReleaseError):
            failure.reason = str(exc)
        if isinstance(exc, ValidationError):
            failure.reason = "Invalid settings; check AI_HUB_* values"
        if args.command != "gates":
            _log_exception(log_path, run_id, exc)
            record_failure(failure, state_dir)
        LOG.error("%s\n%s", failure.issue_title, failure.issue_body)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

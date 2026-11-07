# Approved plan — T001_ingestion_pipeline: ingestion pipeline and state store

Source: hybrid (Gate 1 option C, 07 November 2026). Claude's nine-task split carrying Codex's contracts: provisional labels with `label_status`, niche selection in config, state-store safety, evidence semantics, versioned weights, workflow hardening. User's words: "C Hybrid (Recommended)"; "Yes, all three (Recommended)".

Standing rules for every task: Python 3.13, uv, `pipeline/` package; type hints on public functions; module docstring per file; pathlib; logging not print; British English; no network in unit tests (recorded JSON fixtures under `tests/fixtures/`); `uv run pytest --cov=pipeline --cov-fail-under=80` and `uv run ruff check .` are the project checks; never rank by raw stars; nothing marked tested without a dated sandbox result (all `untested` in T001).

## T01 — Package skeleton, models and config
- Objective: `pyproject.toml` (uv, ruff, pytest, pytest-cov, httpx, pydantic 2), `.python-version`, `pipeline/__init__.py`, `pipeline/config.py` (settings from env with defaults; `QUERIES` copied verbatim from `scripts/pull_candidate_repos.py`; `NICHE_DEFAULT = ["coding_agent", "claude_code", "mcp", "mcp_server", "ai_agents", "agents"]`; `--all-queries` escape; budgets: GitHub 2,500 points, HTTP calls per source; `SCORE_WEIGHTS_V0` with a `SCORE_VERSION = "v0"`), `pipeline/models.py` (pydantic: `RepoRecord`, `Snapshot`, `Evidence` with `status` in {present, absent, unsupported, failed}, `Score`, `Listing` with `level`, `topic`, `label_status` in {reviewed, provisional, pending}, `tested` fixed to `untested`, `score_version`, `unevaluated_checks`), `tests/conftest.py` with fixture loader.
- Depends on: none.
- Likely files: pyproject.toml, .python-version, pipeline/__init__.py, pipeline/config.py, pipeline/models.py, tests/conftest.py, tests/test_config.py, tests/test_models.py, .gitignore (add `.coverage`, `htmlcov/`).
- Acceptance: `uv sync --frozen` works; `QUERIES` equals the script's dict (test imports both); niche default is the six queries; every model rejects unknown enum values; `Listing` requires `score_version` and `tested`.
- Tests: test_config (queries equal, niche default, env override), test_models (one parametrised test over every enum field rejecting a bad value).
- Risk: low.

## T02 — State store with safe promotion
- Objective: `pipeline/store.py`: SQLite schema `schema_version`, `repos` (github id as stable key, full_name, renamed_from, metadata JSON, readme_sha, first_seen, last_seen), `snapshots` (repo id, run id, observed_at, stars, forks, open_issues, pushed_at; unique per repo and run), `scores` (repo id, run id, score_version, components JSON, coverage, total), `run_log` (run id, started, finished, status, budgets JSON, rows in and out, gate results JSON). Open on a working copy (`state/gateway.work.sqlite`); `promote()` replaces `state/gateway.sqlite` only after gates pass; `rollback()` discards the copy. `velocity(repo_id, window_hours)` from actual elapsed time between snapshots; `None` when fewer than two snapshots. Rename handling by github id.
- Depends on: T01.
- Likely files: pipeline/store.py, pipeline/migrations.py, tests/test_store.py.
- Acceptance: fresh database migrates to version 1; upsert twice leaves one row; rename keeps history; velocity None on first snapshot and correct on two; a failed run leaves `gateway.sqlite` byte-identical; falling star counts give negative velocity, not an error.
- Tests: test_store covering each acceptance line, on a temp directory.
- Risk: medium.

## T03 — GitHub GraphQL source and budget accounting
- Objective: `pipeline/http.py` (httpx client with retries, timeouts, injected for tests), `pipeline/budgets.py` (`Budget` counters, `BudgetExceeded`), `pipeline/sources/github.py`: search per query with cursor pagination to a per-query cap (default 100), dedupe by id; repo node fields: stargazerCount, forkCount, pushedAt, createdAt, licenseInfo, repositoryTopics, latest release (tag, publishedAt), `mentionableUsers.totalCount` as contributor proxy, README `object(expression:"HEAD:README.md")` oid; read `rateLimit { cost remaining }` and charge the budget; partial GraphQL errors raise a typed error naming the query. Document in the module docstring that contributor coverage is a proxy and the REST `contributors?per_page=1&anon=true` Link-header count is the fallback (implemented behind a flag, default off).
- Depends on: T01.
- Likely files: pipeline/http.py, pipeline/budgets.py, pipeline/sources/__init__.py, pipeline/sources/github.py, tests/fixtures/github_*.json, tests/test_github.py, tests/test_budgets.py.
- Acceptance: two-page fixture yields deduped records; a partial-error fixture raises; the budget aborts on the call that would exceed 2,500 points; no token logged.
- Tests: test_github (pagination, dedupe, partial error, field mapping), test_budgets (threshold, reset).
- Risk: high.

## T04 — Enrichment adapters
- Objective: `pipeline/sources/deps_dev.py` (project endpoint by `github.com/owner/repo`), `pipeline/sources/scorecard.py` (`api.scorecard.dev/projects/github.com/owner/repo`), `pipeline/sources/hugging_face.py` (search models and Spaces whose card links the repo URL; record link status only), `pipeline/sources/hacker_news.py` (Firebase or Algolia search of the repo URL, bounded to 30 days, count and top item). Every adapter returns `Evidence` with status present, absent (404), unsupported (ecosystem not covered) or failed (network or 5xx) and `fetched_at`; never raises on 404.
- Depends on: T01.
- Likely files: pipeline/sources/deps_dev.py, pipeline/sources/scorecard.py, pipeline/sources/hugging_face.py, pipeline/sources/hacker_news.py, tests/fixtures/*.json, tests/test_enrichment.py.
- Acceptance: for every adapter, a present, an absent and a failed fixture map to the right status (one parametrised test across all four adapters); each adapter counts one HTTP call per repo in the budget.
- Tests: test_enrichment parametrised over adapters and statuses.
- Risk: medium.

## T05 — Scoring and export
- Objective: `pipeline/scoring.py`: total 0 to 100 from weighted components (Scorecard score, deps.dev advisories, licence class, maintenance recency from pushed_at, release cadence, contributor proxy, HN mentions), weights from `SCORE_WEIGHTS_V0`; an absent or unsupported component is excluded and lowers `coverage`, a failed component is excluded and flagged; stars and velocity are stored but carry weight 0; `unevaluated_checks = ["fake_stars", "typosquat", "sandbox_test"]`. `pipeline/export.py`: builds `Listing` rows (topic and level from `data/labelled_repos_for_review.csv` where present with `label_status = provisional`, else null and `pending`), sorts by total score then recency, writes `site/src/data/listings.json` with `generated_at`, `score_version`, `run_id`.
- Depends on: T02, T03, T04.
- Likely files: pipeline/scoring.py, pipeline/export.py, docs/scoring.md, tests/test_scoring.py, tests/test_export.py.
- Acceptance: score bounded 0 to 100; ordering by score differs from ordering by stars on the fixture set; a repo with every component absent scores null with coverage 0 and is excluded from listings; JSON validates against `Listings`.
- Tests: test_scoring (bounds, star independence, coverage), test_export (CSV join, label_status, JSON validity).
- Risk: high.

## T06 — Gates 2 and 3 and the abort rule
- Objective: `pipeline/gates.py`: gate 2 (every listing validates; unknown topic or level fails), gate 3 (`generated_at` within 7 hours of now; listed count at least 90 per cent of the previous successful run, skipped on first run; every listing has score, licence status and `tested`; label rule behind `REQUIRE_LABELS = False` until request 2; no `tested` other than `untested` without a dated sandbox result). `Budget` overrun or any gate failure returns a `RunFailure` with an issue title and body text (gate name, counts, log path) for the workflow to post; the store is rolled back, not promoted.
- Depends on: T05.
- Likely files: pipeline/gates.py, pipeline/failure.py, tests/test_gates.py.
- Acceptance: each gate has a passing and a failing test; the first-run case passes the count rule; failure text names the gate; a failed run never promotes.
- Tests: test_gates parametrised over every gate rule, pass and fail.
- Risk: low.

## T07 — Release round trip and CLI
- Objective: `pipeline/release.py`: `pull()` downloads asset `data-latest` with `gh release download --pattern gateway.sqlite` into `state/` (absent release means first run), `push()` uploads with `gh release upload --clobber` only after promotion, verifies size after upload. `pipeline/cli.py` (`pipeline run [--limit N] [--dry-run] [--all-queries]`, `pipeline gates`, `pipeline release pull|push`); `--dry-run` writes to a temp state and `site/src/data/listings.dry.json`, never promotes or uploads. Orchestration order: pull, ingest, enrich, score, export, gates, promote, push, run_log.
- Depends on: T02, T06.
- Likely files: pipeline/release.py, pipeline/cli.py, tests/test_release.py, tests/test_cli.py.
- Acceptance: a fake `gh` on PATH records the exact commands; a missing release is treated as first run; upload is skipped when gates fail; `pipeline run --dry-run --limit 5` completes offline against fixtures via an injected client.
- Tests: test_release (fake gh), test_cli (dry run, order, exit codes).
- Risk: medium.

## T08 — Workflow, runbook and docs
- Objective: `.github/workflows/refresh.yml`: `schedule: cron "17 */6 * * *"`, `workflow_dispatch`, `concurrency: refresh` (cancel-in-progress false), `permissions: contents: write, issues: write`, `astral-sh/setup-uv`, `uv sync --frozen`, `pipeline release pull`, `pipeline run`, `pipeline release push`, on failure `gh issue create --label pipeline-failure` with the failure text; secrets read only from `secrets.GH_TOKEN`. `docs/runbook.md` with the first four entries from `docs/phase1_architecture_and_operations.md` section 5 (rate limit or schema change, BigQuery quota marked "from request 4", labeller drift marked "from request 2", sandbox timeout marked "from request 3") plus how to run locally and how to roll back. `docs/scoring.md` (weights v0, evidence semantics, unevaluated checks). `README.md` (what, how to run, layout).
- Depends on: T07.
- Likely files: .github/workflows/refresh.yml, .github/dependabot.yml, docs/runbook.md, docs/scoring.md, README.md, tests/test_workflow.py.
- Acceptance: YAML parses and the cron string equals `17 */6 * * *`; `actionlint` passes if installed (else note); runbook has four entries each with symptom, cause, fix; README commands match `cli.py`.
- Tests: test_workflow (YAML parse, cron, permissions, concurrency present).
- Risk: low.

## T09 — Dry run against 50 repos
- Objective: with the real network and `gh` auth, run `uv run pipeline run --dry-run --limit 50`; record wall time, GitHub points used, HTTP calls per source, listings count, coverage distribution and any adapter failures in `TASK_HANDOVER.md`; fix nothing beyond configuration unless the run fails, in which case report.
- Depends on: T08.
- Likely files: .ai/tasks/T001_ingestion_pipeline/TASK_HANDOVER.md (no source files expected).
- Acceptance: completes in under 10 minutes; `listings.dry.json` validates; no promotion, no upload.
- Tests: the run itself plus `uv run pytest` green and `ruff check` clean on the final tree.
- Risk: medium (network).

## Implementation order
T01, T02, T03, T04 (T03 and T04 independent of each other), T05, T06, T07, T08, T09.

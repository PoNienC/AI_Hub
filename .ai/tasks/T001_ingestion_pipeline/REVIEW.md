# Hand-off review — T001_ingestion_pipeline: ingestion pipeline and state store

- Date: 07 November 2026 · branch `dual_dev/T001_ingestion_pipeline` (stacked on `dual_dev_setup`)
- Hand-off commit: `4f743c1` (request started at `4a66f25`)
- Push: only after every audit below is complete. Fixes come as new commits on top; nothing you review is amended or rebased. No remote exists yet.
- Close-out: I will ask you before closing out.

## In short

- **Built:** the whole request 1 pipeline: config and models, SQLite state store with safe promotion, GitHub GraphQL source with budgets, four enrichment adapters, versioned trust score and validated export, gates 2 and 3 with the abort rule, release round trip and CLI, six-hourly workflow, runbook, README; proven by a live 50-repo dry run in 111 seconds.
- **Tests:** 454 passed, coverage 98.44 per cent, `ruff check .` clean, on `4f743c1`.
- **Audits:** all 4 complete (B1, B2 with a round-2 re-check, B3, B4); no BLOCKER or HIGH open.
- **Look at first:** `TASK_HANDOVER.md` section T09 attempt 2 (what the live run found), then `docs/runbook.md` and `README.md`.

## What was built

| Task | Title | Executor | Commit | What it does (one line) |
|---|---|---|---|---|
| T01 | Package skeleton, models and config | Codex | 501f79e | uv project, pydantic models, settings, verbatim queries, six-query niche default, weights v0 |
| T02 | State store with safe promotion | Codex | 501f79e | SQLite schema v1, working copy, promote only after gates, velocity from snapshots, renames by id |
| T03 | GitHub GraphQL source and budgets | Codex | 501f79e, 898b859 | paginated search, budget accounting, page 25 with resource-limit halving (live fix) |
| T04 | Enrichment adapters | Codex | 4c87086 | deps.dev, Scorecard, Hugging Face, Hacker News with present/absent/unsupported/failed |
| T05 | Scoring and export | Codex | 4c87086 | trust score 0 to 100 (stars weight 0), coverage per row, compact evidence in listings.json, full evidence to state |
| T06 | Gates 2 and 3 and abort rule | Codex | 400f780 | schema and data-quality gates, failure record and issue text, rollback on failure |
| T07 | Release round trip and CLI | Codex | 400f780 | `pipeline run | gates | release`, dry run isolation, gh release pull/push, failures.jsonl, stale-copy pre-flight |
| T08 | Workflow, runbook and docs | Codex | 400f780 | refresh.yml (cron 17 */6, dispatch, concurrency, permissions, issue on failure), Dependabot, runbook, README |
| T09 | Dry run against 50 repos | Claude | 4f743c1 | live run: 50 in, 50 out, 111 s, 12 GitHub points, all adapters answered, gates passed |

Audit fix commits: 9793c48 (B1), 6653b63 and b6fcae5 (B2), a6f4dea (B3), 898b859 (T03 from the T09 finding).

## How to try it

1. `uv sync --frozen`, then set `GH_TOKEN` (for example from `gh auth token`).
2. `uv run pipeline run --dry-run --limit 10` writes `site/src/data/listings.dry.json` in about 30 seconds; nothing is promoted or uploaded.
3. `uv run pytest --cov=pipeline --cov-fail-under=80` and `uv run ruff check .` are the project checks.
4. Read `docs/runbook.md` for the failure paths and `docs/scoring.md` for the weights.

## Audits

| Scope | Tasks | Reviewer (model, effort) | Status | Findings B/H/M/L/N | Fix commit |
|---|---|---|---|---|---|
| B1 | T01-T03 | Claude subagent (session model) | complete | 0/0/2/2/3 | 9793c48 |
| B2 r1 | T04-T05 | Claude subagent (session model) | complete (you approved A) | 0/1/3/4/1 | 6653b63 |
| B2 r2 | T04-T05 | Claude subagent (session model) | complete, HIGH verified fixed | 0/0/0/3/2 | b6fcae5 |
| B3 | T06-T08 | Claude subagent (session model) | complete | 0/0/3/3/4 | a6f4dea |
| T09 finding | T03 | Claude (coordinator, live run) | complete, verified by dry run attempt 2 | 0/0/1/0/0 | 898b859 |
| B4 | T09 | Codex (gpt-6-astra, xhigh) | complete | 0/0/0/2/0 | this commit (record wording); fixture capture deferred to request 2 |

Status: running · awaiting your review · fixing · re-check running · complete.

## Known limits to carry forward

- Scorecard covers 2 of the 50 niche repos; scores saturate near 100 with three evaluated components. Weights v0 are to be rebalanced in request 4 (recorded in DECISIONS.md).
- Labels: 5 provisional, 45 pending until request 2; all rows `untested` until request 3.
- The release round trip and the scheduled workflow are unit-tested with a fake `gh` and verified pins, but not exercised live: no remote exists yet. First live step after the remote: a manual `pipeline release pull`, then one `workflow_dispatch`.
- Untracked and outside this request: `docs/ai_hub_platform_*` (the flowchart and report you asked for) and `.claude/launch.json`. They can be committed separately.

## Your review notes

Send notes in chat; please do not edit repo files until completion (fixes land here, each one announced). A change you ask for becomes a new task.

| # | Your note | Became task, or "no action" | Status |
|---|---|---|---|

## Changes since the hand-off

~~~text
 .ai/tasks/T001_ingestion_pipeline/AUDIT_LOG.md     |  16 +++
 .ai/tasks/T001_ingestion_pipeline/REVIEW.md        | 128 +++++++++++++++++++++
 .ai/tasks/T001_ingestion_pipeline/TASKS.md         |   8 +-
 .ai/tasks/T001_ingestion_pipeline/TASK_HANDOVER.md |   2 +-
 .../codex/B4_audit_r1_brief.md                     |  54 +++++++++
 .../codex/B4_audit_r1_out.md                       |  36 ++++++
 6 files changed, 239 insertions(+), 5 deletions(-)
~~~

- ad0a891 — B4 audit fixes (T09): record wording (F2); fixture capture deferred to request 2 (F1). No source change.
- close-out commit — STATE.md, DECISIONS.md, this section.

## Detail

### Files changed

~~~text
 .github/dependabot.yml                    |  10 +
 .github/workflows/refresh.yml             |  80 +++++
 .gitignore                                |   8 +
 .python-version                           |   1 +
 README.md                                 |  76 +++++
 docs/runbook.md                           | 225 +++++++++++++
 docs/scoring.md                           | 178 +++++++++++
 pipeline/__init__.py                      |   1 +
 pipeline/budgets.py                       | 105 ++++++
 pipeline/cli.py                           | 290 +++++++++++++++++
 pipeline/config.py                        | 120 +++++++
 pipeline/export.py                        | 244 ++++++++++++++
 pipeline/failure.py                       |  69 ++++
 pipeline/gates.py                         |  73 +++++
 pipeline/http.py                          | 121 +++++++
 pipeline/migrations.py                    |  68 ++++
 pipeline/models.py                        | 109 +++++++
 pipeline/release.py                       | 208 ++++++++++++
 pipeline/scoring.py                       | 190 +++++++++++
 pipeline/sources/__init__.py              |   1 +
 pipeline/sources/_enrichment.py           |  84 +++++
 pipeline/sources/deps_dev.py              |  38 +++
 pipeline/sources/github.py                | 284 +++++++++++++++++
 pipeline/sources/hacker_news.py           |  63 ++++
 pipeline/sources/hugging_face.py          |  61 ++++
 pipeline/sources/scorecard.py             |  36 +++
 pipeline/store.py                         | 216 +++++++++++++
 pyproject.toml                            |  35 ++
 scripts/sample_and_fetch.py               |   4 +-
 tests/conftest.py                         |  34 ++
 tests/fixtures/enrichment_responses.json  |  29 ++
 tests/fixtures/fake_gh.py                 |  46 +++
 tests/fixtures/github_contributors.json   |   1 +
 tests/fixtures/github_empty.json          |   6 +
 tests/fixtures/github_mixed_errors.json   |  10 +
 tests/fixtures/github_page_1.json         |  28 ++
 tests/fixtures/github_page_2.json         |  26 ++
 tests/fixtures/github_partial_error.json  |   7 +
 tests/fixtures/github_resource_limit.json |  23 ++
 tests/test_budgets.py                     |  74 +++++
 tests/test_cli.py                         | 329 +++++++++++++++++++
 tests/test_config.py                      |  89 ++++++
 tests/test_enrichment.py                  | 234 ++++++++++++++
 tests/test_export.py                      | 353 +++++++++++++++++++++
 tests/test_gates.py                       | 152 +++++++++
 tests/test_github.py                      | 508 ++++++++++++++++++++++++++++++
 tests/test_http.py                        | 117 +++++++
 tests/test_models.py                      |  83 +++++
 tests/test_release.py                     | 244 ++++++++++++++
 tests/test_scoring.py                     | 204 ++++++++++++
 tests/test_store.py                       | 207 ++++++++++++
 tests/test_workflow.py                    |  68 ++++
 uv.lock                                   | 469 +++++++++++++++++++++++++++
 53 files changed, 6337 insertions(+), 2 deletions(-)
~~~

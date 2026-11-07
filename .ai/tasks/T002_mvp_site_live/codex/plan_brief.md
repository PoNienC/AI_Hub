# Codex brief — independent plan (PLANNING ONLY)

Fresh task. You are a peer planner in a dual-agent workflow (see `AGENTS.md`).
Another agent is planning the same request separately. Do not assume its
approach is correct, and do not look for it.

## Rules

- Produce an independent implementation plan only.
- Do not modify, create or delete any file. Do not attempt implementation.
- Do not read `.ai/tasks/T002_mvp_site_live/PLAN_A.md` or any plan under `.ai/tasks/` other
  than this request's `REQUEST.md`.

## Read first

**Everything you need is pasted at the end of this brief** — the repo
tree, `AGENTS.md`, `.ai/PROJECT.md`, `.ai/STATE.md`, `.ai/DECISIONS.md` and
the relevant source and tests in full — and the request is in
`.ai/tasks/T002_mvp_site_live/REQUEST.md`. Plan from that text. Run a command only if a
file you truly need is missing from the pack, then read only that file;
do not explore the repository folder by folder. Say "not in the pack"
rather than guessing.



## Output — your final message, Markdown, exactly these sections

# Plan B (Codex) — T002 MVP site and live schedule
## Objective
## Assumptions
## Proposed architecture
## Numbered tasks
For each task: number, title, objective, depends on, likely files, tests,
risk (low / medium / high).
## Implementation order
## Test strategy
## Risks
## Alternatives considered
## Rollback
## Open questions for the user

Be specific to this repository: cite real file paths, functions and tests
from the pack. Keep the whole plan under about 900 words. British English.
No preamble.

## Context pack (pasted)

# Context pack — C:\Users\po.nienchen\repos\AI_Hub

Branch: `dual_dev/T001_ingestion_pipeline` · last commit: d73a1d2 2026-11-07 Reorder phase 1 requests: MVP site before the quality layers · built 2026-11-07 21:39

Everything a planner needs is pasted below. Paths are relative to the repo root.

## Repository tree (124 tracked files)

Files per top-level folder:
~~~~
   39  .ai/
   23  tests/
   20  pipeline/
   12  docs/
    9  research_notes/
    7  (root)
    7  data/
    2  .github/
    2  reports/
    2  scripts/
    1  .claude/
~~~~

All paths:
~~~~
.ai/DECISIONS.md
.ai/PROJECT.md
.ai/STATE.md
.ai/tasks/.gitkeep
.ai/tasks/T001_ingestion_pipeline/ALLOCATION.md
.ai/tasks/T001_ingestion_pipeline/AUDIT_LOG.md
.ai/tasks/T001_ingestion_pipeline/COMPARISON.md
.ai/tasks/T001_ingestion_pipeline/PLAN_A.md
.ai/tasks/T001_ingestion_pipeline/PLAN_APPROVED.md
.ai/tasks/T001_ingestion_pipeline/PLAN_B.md
.ai/tasks/T001_ingestion_pipeline/REQUEST.md
.ai/tasks/T001_ingestion_pipeline/REVIEW.md
.ai/tasks/T001_ingestion_pipeline/TASKS.md
.ai/tasks/T001_ingestion_pipeline/TASK_HANDOVER.md
.ai/tasks/T001_ingestion_pipeline/codex/B1_exec_brief.md
.ai/tasks/T001_ingestion_pipeline/codex/B1_exec_out.md
.ai/tasks/T001_ingestion_pipeline/codex/B1_fix_r1_brief.md
.ai/tasks/T001_ingestion_pipeline/codex/B1_fix_r1_out.md
.ai/tasks/T001_ingestion_pipeline/codex/B2_exec_brief.md
.ai/tasks/T001_ingestion_pipeline/codex/B2_exec_out.md
.ai/tasks/T001_ingestion_pipeline/codex/B2_fix_r1_brief.md
.ai/tasks/T001_ingestion_pipeline/codex/B2_fix_r1_out.md
.ai/tasks/T001_ingestion_pipeline/codex/B2_fix_r2_brief.md
.ai/tasks/T001_ingestion_pipeline/codex/B2_fix_r2_out.md
.ai/tasks/T001_ingestion_pipeline/codex/B3_exec_brief.md
.ai/tasks/T001_ingestion_pipeline/codex/B3_exec_out.md
.ai/tasks/T001_ingestion_pipeline/codex/B3_fix_r1_brief.md
.ai/tasks/T001_ingestion_pipeline/codex/B3_fix_r1_out.md
.ai/tasks/T001_ingestion_pipeline/codex/B4_audit_r1_brief.md
.ai/tasks/T001_ingestion_pipeline/codex/B4_audit_r1_out.md
.ai/tasks/T001_ingestion_pipeline/codex/T09_fix_r1_brief.md
.ai/tasks/T001_ingestion_pipeline/codex/T09_fix_r1_out.md
.ai/tasks/T001_ingestion_pipeline/codex/plan_brief.md
.ai/tasks/T001_ingestion_pipeline/codex/plan_out.md
.ai/tasks/T001_ingestion_pipeline/context_pack.md
.ai/tasks/T001_ingestion_pipeline/subagent/B1_audit_r1_out.md
.ai/tasks/T001_ingestion_pipeline/subagent/B2_audit_r1_out.md
.ai/tasks/T001_ingestion_pipeline/subagent/B2_audit_r2_out.md
.ai/tasks/T001_ingestion_pipeline/subagent/B3_audit_r1_out.md
.claude/launch.json
.github/dependabot.yml
.github/workflows/refresh.yml
.gitignore
.python-version
AGENTS.md
CLAUDE.md
README.md
data/candidate_repos.csv
data/labelled_repos_for_review.csv
data/labelling_set.csv
data/labelling_set_part_a.csv
data/labelling_set_part_b.csv
data/labels_part_a.csv
data/labels_part_b.csv
docs/ai_hub_platform_flow.html
docs/ai_hub_platform_flow.json
docs/ai_hub_platform_flow.png
docs/ai_hub_platform_flow.svg
docs/ai_hub_platform_structure.html
docs/ai_hub_platform_structure.md
docs/build_platform_report.py
docs/dual_dev_requests.md
docs/phase1_architecture_and_operations.md
docs/platform_report_body.html
docs/runbook.md
docs/scoring.md
pipeline/__init__.py
pipeline/budgets.py
pipeline/cli.py
pipeline/config.py
pipeline/export.py
pipeline/failure.py
pipeline/gates.py
pipeline/http.py
pipeline/migrations.py
pipeline/models.py
pipeline/release.py
pipeline/scoring.py
pipeline/sources/__init__.py
pipeline/sources/_enrichment.py
pipeline/sources/deps_dev.py
pipeline/sources/github.py
pipeline/sources/hacker_news.py
pipeline/sources/hugging_face.py
pipeline/sources/scorecard.py
pipeline/store.py
pyproject.toml
reports/AI repo gateway competitor landscape.md
reports/ambition_brief_261107_ai_repo_gateway.md
research_notes/AI repo gateway competitor landscape/ai_topic_trends_and_business_models.md
research_notes/AI repo gateway competitor landscape/beginner_gateways_and_demand.md
research_notes/AI repo gateway competitor landscape/closest_competitors_verified.md
research_notes/AI repo gateway competitor landscape/dev_news_and_social.md
research_notes/AI repo gateway competitor landscape/github_trending_tools.md
research_notes/AI repo gateway competitor landscape/hugging_face_and_ai_hubs.md
research_notes/AI repo gateway competitor landscape/own_data_100_repo_labelling.md
research_notes/AI repo gateway competitor landscape/skills_mcp_registries.md
research_notes/AI repo gateway competitor landscape/trust_quality_signals_and_data.md
scripts/pull_candidate_repos.py
scripts/sample_and_fetch.py
tests/conftest.py
tests/fixtures/enrichment_responses.json
tests/fixtures/fake_gh.py
tests/fixtures/github_contributors.json
tests/fixtures/github_empty.json
tests/fixtures/github_mixed_errors.json
tests/fixtures/github_page_1.json
tests/fixtures/github_page_2.json
tests/fixtures/github_partial_error.json
tests/fixtures/github_resource_limit.json
tests/test_budgets.py
tests/test_cli.py
tests/test_config.py
tests/test_enrichment.py
tests/test_export.py
tests/test_gates.py
tests/test_github.py
tests/test_http.py
tests/test_models.py
tests/test_release.py
tests/test_scoring.py
tests/test_store.py
tests/test_workflow.py
uv.lock
~~~~

## Key documents

### AGENTS.md

~~~~
# Dual-agent development contract

This project uses Claude Code and OpenAI Codex as cooperating development
agents. This section is the operating contract for both.

## Authority

The user is the final authority for architecture, plan selection, execution
allocation and acceptance of significant changes.

- Claude Code is the default workflow coordinator and default executor.
- Claude is NOT automatically the preferred planner.
- Codex is a peer planner, optional executor and reciprocal reviewer.

## Mandatory workflow (substantial requests only)

The user starts it with `/dual_dev <request>` in Claude Code. Small edits
skip it.

1. Claude and Codex each produce an independent plan.
2. Neither agent sees the other's plan until both are complete.
3. Claude presents both plans and a neutral comparison to the user.
4. No implementation before the user approves Claude's plan, Codex's plan
   or a hybrid (Gate 1).
5. Claude then asks how execution is allocated (Gate 2). Default: Claude
   executes all tasks. The user may assign any subset to Codex.
6. Every executed task is reviewed by the other agent. An agent is never
   the sole reviewer of its own work.

## Planning

Both plans cover: objective; assumptions; architecture; numbered tasks;
dependencies; implementation order; testing; risks; alternatives
considered; rollback where relevant.

Planning never modifies project files. Codex plans in a read-only sandbox.

## Reciprocal audit

- Claude executes → Codex reviews (read-only) → Claude evaluates each
  finding → Claude fixes accepted findings.
- Codex executes → Claude reviews → Codex evaluates each finding → Codex
  fixes accepted findings.
- Reviewers never silently modify the executor's implementation.
- Audit review (chosen at Gate 2): `auto` — the executor fixes what it
  accepts; `ask` — nothing is fixed until the user approves the proposed
  resolutions; `ask_high` — the user is asked only when there is a
  BLOCKER or HIGH finding. The user's decision on a finding overrides the
  executor's; a finding the user approved for fixing is fixed, not
  rejected — if it cannot be fixed, the executor stops and explains why.
- Hand-off before audits finish: audits run in the background (Claude's
  as a read-only subagent) and review committed ranges only. The user
  gets the result to review as soon as the last task is committed; audit
  fixes arrive as new commits on top; nothing is pushed until every
  audit is complete.

Severity: BLOCKER, HIGH, MEDIUM, LOW, NOTE.
Resolution: ACCEPTED, PARTIALLY_ACCEPTED, REJECTED, DEFERRED — always with
a reason.

Re-review limits: BLOCKER/HIGH → one re-review of the fix commit;
MEDIUM → fix plus tests is enough; LOW/NOTE → no second audit. A BLOCKER
or HIGH found by the re-review goes to the user — there is no automatic
third round.

## Task boundaries and Git

Branch names, commit format and push cadence follow this project's own
rules, recorded in `.ai/PROJECT.md` under "Git conventions". Where the
project has none: branch `dual_dev/T###_slug`, commit `T## <task title>`,
no push without approval.

Always:

- One request = one branch. The user picks the audit mode at Gate 2:
  `per_task` (audit after every task), `per_block` (audit once per run
  of consecutive tasks by the same executor) or `end` (audit everything
  after all tasks). Work is committed per task (or per Codex block) and
  the audit reviews the commit range; audit fixes get their own commit.
- Never push while any audit or re-check is still open.
- Push only the request branch, and only with the user's approval. If the
  project requires a push every session, offer it when work pauses with
  every audit complete.
- Never push to or merge into the main branch, and never open a pull
  request, without the user's explicit approval.
- The two agents never edit the same working tree at the same time.
  The one exception: while Codex executes, Claude may update its `.ai/`
  bookkeeping files (Codex never edits `.ai/`), but commits nothing
  until Codex has finished.
- No AI-agent credit lines in commit messages.

## Shared state (in the repository, not in agent memory)

- `.ai/PROJECT.md` — what the project is, stack, layout, how to test, Git
  conventions.
- `.ai/STATE.md` — current shared state; updated at the end of each request.
- `.ai/DECISIONS.md` — material architectural decisions, newest first.
- `.ai/tasks/T###_slug/` — one folder per request: `REQUEST.md`,
  `PLAN_A.md` (Claude), `PLAN_B.md` (Codex), `COMPARISON.md`,
  `PLAN_APPROVED.md`, `TASKS.md`, `TASK_HANDOVER.md`, `AUDIT_LOG.md`,
  `REVIEW.md` (the hand-off review), `codex/` (briefs and raw Codex
  output) and `subagent/` (reports of Claude's audit subagent).

Git history remains the authoritative implementation history. A root
`HANDOVER.md`, if present, is a personal note and not part of this contract.

## Rules for Codex when called by this workflow

- Follow the brief you are given; it states your role (planner, auditor or
  executor) and your limits.
- As planner or auditor: read only; never modify files.
- As executor: change only what the assigned task needs; run the relevant
  tests; do not stage or commit; do not edit `.ai/` files — put your
  handover in your final message instead.
- British English in code comments, documentation and messages.

~~~~

### .ai/PROJECT.md

~~~~
# AI_Hub — project facts for both agents

## Purpose
A gateway that groups trending AI GitHub repositories, agent skills and MCP servers by user skill level and topic for vibe coders, with sandbox run tests and security screening. Phase 0 (research and gap test) done 07 November 2026; phase 1 (build) approved the same day. Source: `reports/AI repo gateway competitor landscape.md`, `docs/phase1_architecture_and_operations.md`.

## Stack and versions
- Python 3.13.13 (installed); package manager uv (to be added in request 1). Source: `scripts/*.py`, `docs/phase1_architecture_and_operations.md` section 1.
- Front end: Astro static site with Tailwind, Cloudflare Pages (request 5). Not yet present.
- GitHub CLI `gh` authenticated; Codex CLI 0.160.1 logged in (07 November 2026).
- Data: SQLite state store `state/gateway.sqlite` kept as a GitHub Release asset, never committed (planned). CSVs under `data/` are committed; `data/readmes/` is ignored and re-fetchable.

## Top-level layout (07 November 2026)
- `data/` — phase 0 CSVs (965 candidate repos; 100-repo labelled review set) and ignored READMEs.
- `docs/` — `phase1_architecture_and_operations.md` (target architecture, update schedule, six test gates, deploy, runbook outline) and `dual_dev_requests.md` (five requests to run in order).
- `reports/` — phase 0 report and the ambition brief.
- `research_notes/` — nine research notes with URLs on every claim.
- `scripts/` — `pull_candidate_repos.py`, `sample_and_fetch.py` (need `gh`).
- Planned by the requests: `pipeline/`, `tests/`, `site/`, `.github/workflows/`, `state/` (ignored).

## Setup steps
- `gh auth login` (public read is enough). Python 3.13. Request 1 adds uv; install with `uv sync --frozen` into a worktree-local `.venv` (Codex's sandbox convention, noted in the init probe on 07 November 2026).

## Test and lint commands
- TBC until request 1: planned `uv run pytest` (coverage 80 per cent or better), `ruff check .`, pydantic schema gate on `site/src/data/*.json`. Source: `docs/phase1_architecture_and_operations.md` section 3.

## Coding conventions
- From the user's global rules (`~/.claude/rules/python.md`): type hints on public functions; module docstring per file; pathlib not os.path; logging not print; no bare `except Exception` unless re-raised; British English in docstrings, comments and user strings.
- Names snake_case with underscores (files, folders, branches). The word "claude" never appears in any name, branch, commit or identifier. No AI credit lines in commits.
- Never rank by raw stars; never mark anything "tested" without a dated sandbox run. Source: `docs/phase1_architecture_and_operations.md`.

## Key documents
- `docs/phase1_architecture_and_operations.md` — the target for every request.
- `docs/dual_dev_requests.md` — the five requests, in order.
- `reports/AI repo gateway competitor landscape.md` — why the project exists.
- `data/labelled_repos_for_review.csv` — becomes `data/gold_labels.csv` after Po's review (due before request 2).

## Git conventions (used by /dual_dev)
- Main branch: `main` (created 07 November 2026, no commits yet at setup time). Source: `git init -b main`.
- Request branch pattern: `dual_dev/T001_slug` (default; no project pattern existed).
- Commit format: `T01 <task title>` (default). Setup commit: `Set up dual-agent workflow (AGENTS.md contract, .ai shared state)`.
- Push policy: no push without the user's explicit approval. Commit only what the user ordered or approved (user's global rules).
- Pull requests: not yet required (solo project, no remote). When a remote exists, request branches merge to `main` through a pull request reviewed by the user.
- GitHub account for this remote: `PoNienC` (personal; decided by Po, 07 November 2026). The GitHub CLI also holds `PoNienChenPP` (work); switch with `gh auth switch -u PoNienC` only after telling the user. Remote `origin` = https://github.com/PoNienC/AI_Hub (private, created 07 November 2026).
- Codex execution on this machine (PRIORPLAP180): available (07 November 2026). Read probe: exit 0, write to repo blocked. Write probe in a throwaway repo: exit 0, file created. Model default gpt-6-astra.

~~~~

### .ai/STATE.md

~~~~
# State — 07 November 2026 (close-out of T001)

- Branch: `dual_dev/T001_ingestion_pipeline`, stacked on `dual_dev_setup`; `main` still has no commits.
- Remote: https://github.com/PoNienC/AI_Hub (private, created 07 November 2026, HTTPS, credentials via `gh auth setup-git`). `dual_dev_setup` pushed and is the default branch for now. `dual_dev/T001_ingestion_pipeline` pushed on 07 November 2026 after Po granted the `workflow` scope to the PoNienC token. Scheduled workflows run only from the default branch, which is `dual_dev_setup` without the workflow file, so nothing runs on GitHub until the request branch is merged or made default. Pushing from this PC needs `gh auth switch -u PoNienC` first (HTTPS credentials come from the active gh account); switch back to PoNienChenPP afterwards.
- Extra commit after close-out on the request branch: a98beda "Add platform structure flowchart and report" (docs and launch.json, outside the request).
- Last commit: T001 close-out (see `git log -1`). Hand-off commit `4f743c1`.
- Request T001 (ingestion pipeline and state store): COMPLETE. Nine tasks, four audit scopes closed, no BLOCKER or HIGH open. 454 tests, coverage 98.44 per cent, ruff clean. Live dry run: 50 repos in 111 s.
- Codex totals for T001: 765,096 tokens; weekly limit 28 per cent used (resets Wednesday 11 November 10:05).
- Work in flight: none. Next: request 2 = MVP site and live schedule (Po, 07 November 2026: "MVP next"); labeller is now request 3, sandbox 4, trust layer and weights v1 5, Astro and Cloudflare 6. See `docs/dual_dev_requests.md`.
- Untracked, outside T001: `docs/ai_hub_platform_*` (flowchart and report), `docs/build_platform_report.py`, `docs/platform_report_body.html`, `.claude/launch.json`. Commit separately when Po says so.

## Owner actions pending
1. Review `data/labelled_repos_for_review.csv` into `data/gold_labels.csv` — due before request 3 (the labeller); can run in parallel with request 2.
2. Create the GitHub remote under PoNienC, push the branches on approval, then run `pipeline release pull` once by hand and one `workflow_dispatch` before enabling the schedule (runbook).
3. Before request 4: Google Cloud service account for BigQuery. Before request 5: domain, Cloudflare account, four secrets.

## Carry-forwards into later requests
- Request 3: labeller; gate 2 validates `pipeline.export.Listings`; capture one sanitised live response per adapter as fixtures (B2 F8, B4 F1); gold labels keyed by github_id.
- Request 5: rebalance weights v0 (advisories and release cadence unevaluated, max coverage 0.70; scores saturate near 100 with three components); Scorecard covers 2 of 50 niche repos, so run the Scorecard CLI or lower its weight; deps.dev package resolution; GH Archive fake-star check needs the Google key.
- Request 4: sandbox tests; `tested` is `untested` everywhere until then.

## Known issues
- `PYTEST_DEBUG_TEMPROOT=_build/pytest` is for Codex's sandbox only; on Po's shell it fails with PermissionError because the folder belongs to the sandbox user. Run pytest without it.
- Release round trip and workflow are unit-tested with a fake `gh` and verified action pins, not yet exercised live (no remote).

## Sources
- `.ai/tasks/T001_ingestion_pipeline/` (REVIEW.md, TASKS.md, AUDIT_LOG.md, TASK_HANDOVER.md); root `HANDOVER.md` (personal) for the owner-action dates.

~~~~

### .ai/DECISIONS.md

~~~~
# Decisions

Format: date · decision · context · alternatives · consequences

- 07 November 2026 · Phase 1 is built through the dual_dev workflow (Claude plans and audits, Codex executes) · Po's instruction after phase 0 · single-agent build · every build item is one `/dual_dev` request; see `docs/dual_dev_requests.md`.
- 07 November 2026 · First niche is the coding-agent stack (coding agents, skills and rules packs, MCP servers) · phase 0 gap table and growth evidence, `reports/AI repo gateway competitor landscape.md` · all ten topics at once · ingestion and sandbox tests scoped to the niche first.
- 07 November 2026 · Rank by a trust score, never by raw stars · own data: Spearman 0.08 between stars and run-readiness on 100 repos; fake-star literature · star velocity ranking · scoring defined in `docs/phase1_architecture_and_operations.md` section 1.
- 07 November 2026 · No "tested" badge without a dated sandbox run · every competitor's "verified" meant paid placement or publisher identity · README-signal proxies · nightly sandbox job, request 3.
- 07 November 2026 · Batch pipeline plus static site, no servers · solo maintainer, free tiers · API back end · GitHub Actions every 6 hours, Cloudflare Pages.
- 07 November 2026 · GitHub account `PoNienC` for this project · personal project · work account `PoNienChenPP` · recorded in `.ai/PROJECT.md`.
- 07 November 2026 · Failed pipeline runs are recorded in an append-only failure log outside the promoted SQLite database · B1 audit finding F5: rollback deletes the working copy, so run_log cannot hold failures · promote a run-log-only change · T07 implements the log; T06 failure text and T08 runbook read from it.
- 07 November 2026 · Scoring weights v0 keep the advisories and release-cadence components even though they cannot be evaluated yet (max coverage 0.70); `coverage` is shown on every listing row; deps.dev package resolution and any weight rebalance happen in request 4 with one score-version change · B2 audit finding F2, approved by Po · rebalance now · listings carry coverage so the gap is visible.
- 07 November 2026 · GitHub GraphQL page size defaults to 25 with adaptive halving on RESOURCE_LIMITS_EXCEEDED (floor 5) · T09 live dry run: 50-node pages with `mentionableUsers` exceed GitHub's resource limit · drop the contributor proxy field · fewer repos per call (12 points for 50 repos is still far under budget).
- 07 November 2026 · Live-response fixtures for the four adapters are captured in request 2, not T001 · B4 audit F1; needs network capture plus test wiring · capture now without tests · request 2 brief carries it.
- 07 November 2026 · Request 2 is a GitHub-hosted MVP site (Jinja2, GitHub Pages, built-in token) before the quality layers · Po wants to see and use the product before scaling · keep labeller first · labeller 3, sandbox 4, trust and weights v1 5, Astro and Cloudflare 6.

~~~~

### README.md

~~~~
# AI Hub

AI Hub builds a gateway for discovering AI repositories, agent skills and MCP
servers by topic and user skill level. This first pipeline ingests GitHub
metadata, records independent evidence, calculates a versioned score and exports
validated listings. Scores reflect evaluated evidence and visible coverage;
raw stars never affect ranking. All entries remain `untested`, and CSV labels
are provisional until human review and the later labelling workflow.

## Run

Use Python 3.13, uv and GitHub CLI from the repository root. Follow the
[local environment and token setup](docs/runbook.md#run-locally), then:

```powershell
uv sync --frozen
uv run pipeline run --dry-run --limit 5
uv run pipeline gates --path site/src/data/listings.dry.json
```

Dry runs use live source APIs, temporary state and separate
`listings.dry.json` / `listings.dry.evidence.jsonl` outputs. The production command
pulls state, ingests, enriches, scores, exports, gates, promotes and uploads:

```powershell
uv run pipeline run
```

For explicitly managed transfers (also used in CI):

```powershell
uv run pipeline release pull
uv run pipeline run --no-release
uv run pipeline release push
uv run pipeline gates
```

`--limit N` caps enriched repositories; `--all-queries` expands beyond the default
six-query niche. Both are optional flags on `pipeline run`. Configure paths,
budgets and source options through `AI_HUB_*` environment variables. The default
canonical state is `state/gateway.sqlite`; the `data-latest` release carries that
database and `evidence.jsonl`. Full evidence stays outside the production site
data. Gate or budget failures retain the last good files and append diagnostics
to `state/failures.jsonl`.

## Checks

After creating `_build/pytest` and setting `PYTEST_DEBUG_TEMPROOT` as described
in the runbook:

```powershell
uv run pytest --cov=pipeline --cov-fail-under=80
uv run ruff check .
```

Tests use local fixtures and injected clients, including a fake `gh` executable;
they never call live APIs. No separate type-check command is configured.

## Layout

| Path | Purpose |
|---|---|
| `pipeline/` | Sources, budgets, state store, scoring, export, gates and CLI |
| `tests/` | Offline unit and integration tests, recorded JSON and fake CLI fixtures |
| `data/` | Candidate repositories and provisional label CSVs |
| `state/` | Ignored SQLite state, full evidence and run/failure diagnostics |
| `site/src/data/` | Generated listings; the frontend is a later request |
| `.github/workflows/refresh.yml` | Six-hourly/manual gated refresh and failure reporting |
| `.github/dependabot.yml` | Weekly uv and GitHub Actions dependency updates |
| `docs/` | Architecture, scoring policy and operational runbook |
| `.ai/` | Shared dual-agent plans and handovers |

Read the [scoring policy](docs/scoring.md) for weights, evidence limits and
unevaluated checks, and the [runbook](docs/runbook.md) for setup, failures and
rollback. Labelling, sandbox runs, the trust layer and static-site deployment
arrive in subsequent requests.

~~~~

### CLAUDE.md

~~~~
# AI_Hub

@AGENTS.md

~~~~

## Relevant files in full (11)

### pipeline/cli.py (291 lines)

~~~~
"""Command-line orchestration of bounded ingestion, gates and release transfers."""

from __future__ import annotations

import argparse
import logging
import os
import shutil
import sqlite3
from collections.abc import Callable, Sequence
from contextlib import closing
from datetime import UTC, datetime
from pathlib import Path
from tempfile import TemporaryDirectory
from uuid import uuid4

import httpx
from pydantic import ValidationError

from pipeline import release
from pipeline.budgets import Budget, BudgetExceeded
from pipeline.config import Settings
from pipeline.export import DEFAULT_LABELS_PATH, DEFAULT_OUTPUT_PATH, build_listings, write_listings
from pipeline.failure import RunFailure, abort_run
from pipeline.gates import GateFailure, check_gates, gate_2
from pipeline.http import HttpClient, HttpRequestError
from pipeline.models import Snapshot
from pipeline.scoring import score_repo
from pipeline.sources import deps_dev, hacker_news, hugging_face, scorecard
from pipeline.sources.github import GitHubResponseError, GitHubSource
from pipeline.store import PromotionError, StateStore

LOG = logging.getLogger("pipeline.cli")
ADAPTERS = (deps_dev, scorecard, hugging_face, hacker_news)
EXPECTED_ERRORS = (
    OSError, ValueError, sqlite3.Error, BudgetExceeded, GateFailure,
    HttpRequestError, GitHubResponseError, PromotionError, release.ReleaseError,
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
    listings.dry.json and its sibling evidence. Successful run_log is finalised
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
        with TemporaryDirectory(prefix=".run-", dir=state_dir) as temporary:
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
                stage = "gates"
                gates = check_gates(path, previous_count=baseline, now=clock())
                LOG.info("Run %s: gates passed; rows_in=%d rows_out=%d budgets=%s", run_id, rows_in, rows_out, budget.snapshot())
                if dry_run:
                    output = output_path.with_name(output_path.stem + ".dry.json")
                    release.replace_bundle([
                        (path, output),
                        (staged / "evidence.jsonl", output.with_suffix(".evidence.jsonl")),
                    ], staged)
                else:
                    stage = "promote"
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
    """Expose run, gates and release commands; return 1 on an operational failure."""
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
    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    started = _now()
    settings = None
    try:
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
            LOG.info("Gates 2 and 3 passed")
        elif args.action == "pull":
            LOG.info("Release %s", "downloaded" if release.pull(settings.state_dir) else "absent; first run")
        else:
            release.push(settings.state_dir)
            LOG.info("Release upload verified")
        return 0
    except EXPECTED_ERRORS as exc:
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

~~~~

### pipeline/export.py (245 lines)

~~~~
"""Validated, deterministic listing export with provisional CSV labels."""

from __future__ import annotations

import csv
import json
from collections.abc import Iterable
from datetime import datetime
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Self

from pydantic import AwareDatetime, Field, JsonValue, model_validator

from pipeline.config import SCORE_VERSION
from pipeline.models import Evidence, Identifier, Level, Listing, Record, RepoRecord, ScoreVersion, Topic
from pipeline.scoring import ScoreDetails, ScoringResult
from pipeline.sources._enrichment import utc_time

DEFAULT_LABELS_PATH = Path("data/labelled_repos_for_review.csv")
DEFAULT_OUTPUT_PATH = Path("site/src/data/listings.json")
SUMMARY_LINK_LIMIT = 3
SUMMARY_TEXT_LIMIT = 256


class ProvisionalLabel(Record):
    """An unreviewed label; CSV confidence is not human approval."""

    topic: Topic
    level: Level


class PublishedListing(Listing):
    """Extend the B1 publication contract with visible evaluated coverage."""

    coverage: float = Field(ge=0, le=1)

    @model_validator(mode="after")
    def matching_coverage(self) -> Self:
        """Prevent the displayed fraction from diverging from the score."""
        if self.coverage != self.score.coverage:
            raise ValueError("Listing coverage must match score.coverage")
        return self


class Listings(Record):
    """Publication envelope; exported rows extend B1 Listing with coverage.

    Details are keyed by GitHub ID, including diagnostics for excluded null
    scores. They preserve failed checks, licence status and raw velocity without
    altering B1 models or the SQLite schema.
    """

    generated_at: AwareDatetime
    score_version: ScoreVersion
    run_id: Identifier
    listings: list[PublishedListing]
    scoring_details: dict[str, ScoreDetails]

    @model_validator(mode="after")
    def consistent_rows(self) -> Self:
        """Reject mismatched identities, run metadata, null scores or duplicates."""
        seen = set()
        for listing in self.listings:
            repo_id = listing.repo.github_id
            if repo_id in seen or listing.score.repo_id != repo_id:
                raise ValueError("Duplicate or mismatched repository identity")
            seen.add(repo_id)
            if listing.score.run_id != self.run_id or listing.score_version != self.score_version:
                raise ValueError("Listing run/version must match the envelope")
            if listing.score.total is None or listing.score.coverage == 0:
                raise ValueError("Published listings require evaluated scores")
            if repo_id not in self.scoring_details:
                raise ValueError("Every listing requires scoring details")
            if self.scoring_details[repo_id].stars != listing.repo.stars:
                raise ValueError("Scoring details must match repository stars")
            statuses = self.scoring_details[repo_id].component_statuses
            for name, status in statuses.items():
                if (listing.score.components.get(name) is not None) != (status == "present"):
                    raise ValueError("Component values must match evidence statuses")
            if listing.label_status == "pending" and (listing.topic is not None or listing.level is not None):
                raise ValueError("Pending labels must have null topic and level")
            if listing.label_status != "pending" and (listing.topic is None or listing.level is None):
                raise ValueError("Assigned labels require both topic and level")
        for repo_id, details in self.scoring_details.items():
            if any(item.repo_id != repo_id for item in details.evidence):
                raise ValueError("Evidence belongs to a different repository")
        return self


def load_provisional_labels(path: Path = DEFAULT_LABELS_PATH) -> dict[str, ProvisionalLabel]:
    """Read case-insensitive GitHub names; reject invalid or duplicate CSV rows."""
    labels = {}
    with Path(path).open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not {"full_name", "topic", "level"}.issubset(reader.fieldnames or []):
            raise ValueError("Label CSV requires full_name, topic and level columns")
        for line, row in enumerate(reader, start=2):
            name = (row.get("full_name") or "").strip().casefold()
            if len(name.split("/")) != 2 or not all(name.split("/")) or any(c.isspace() for c in name):
                raise ValueError(f"Invalid full_name in label CSV at line {line}")
            if name in labels:
                raise ValueError(f"Duplicate label CSV repository at line {line}")
            labels[name] = ProvisionalLabel(topic=row.get("topic"), level=row.get("level"))
    return labels


def build_listings(
    repos: Iterable[RepoRecord], results: Iterable[ScoringResult], *, run_id: str,
    generated_at: datetime | None = None, labels_path: Path = DEFAULT_LABELS_PATH,
) -> Listings:
    """Join by stable ID, apply provisional labels and sort by score then push time."""
    labels = load_provisional_labels(labels_path)
    by_id = {}
    for result in results:
        score = result.score
        if score.repo_id in by_id:
            raise ValueError("Duplicate score for repository")
        if score.run_id != run_id or score.score_version != SCORE_VERSION:
            raise ValueError("Score run/version does not match export")
        by_id[score.repo_id] = result
    rows = []
    seen = set()
    for repo in repos:
        if repo.github_id in seen:
            raise ValueError("Duplicate repository")
        seen.add(repo.github_id)
        if repo.github_id not in by_id:
            raise ValueError(f"Missing score for repository: {repo.github_id}")
        result = by_id[repo.github_id]
        if result.score.total is None:
            continue
        label = labels.get(repo.full_name.casefold())
        rows.append(PublishedListing(
            repo=repo, score=result.score, topic=label.topic if label else None,
            coverage=result.score.coverage,
            level=label.level if label else None, label_status="provisional" if label else "pending",
            tested="untested", score_version=SCORE_VERSION,
            unevaluated_checks=["fake_stars", "typosquat", "sandbox_test"],
        ))
    if set(by_id) != seen:
        raise ValueError("Score has no corresponding repository")
    rows.sort(key=lambda row: (
        -row.score.total,
        -(row.repo.pushed_at.timestamp() if row.repo.pushed_at else float("-inf")),
        row.repo.full_name.casefold(), row.repo.github_id,
    ))
    return Listings(
        generated_at=utc_time(generated_at), score_version=SCORE_VERSION, run_id=run_id,
        listings=rows, scoring_details={repo_id: by_id[repo_id].details for repo_id in sorted(by_id)},
    )


def _summary_fields(data: dict[str, JsonValue], names: tuple[str, ...]) -> dict[str, JsonValue]:
    """Keep selected scalars; omit nested payloads and overlong source text."""
    return {
        name: value for name in names if name in data
        if (value := data[name]) is None or type(value) in {bool, int, float}
        or (isinstance(value, str) and len(value) <= SUMMARY_TEXT_LIMIT)
    }


def _summarise_evidence(item: Evidence) -> Evidence:
    """Retain bounded source diagnostics without shipping full adapter payloads."""
    data = item.data
    summary = {}
    if item.source == "scorecard":
        summary = _summary_fields(data, ("score", "date"))
    elif item.source == "deps_dev":
        summary = _summary_fields(data, ("advisories_status", "advisory_count"))
    elif item.source == "hacker_news":
        summary = _summary_fields(data, ("mention_count", "window_start", "window_end"))
        top = data.get("top_item")
        if isinstance(top, dict):
            summary["top_item"] = _summary_fields(
                top, ("id", "title", "url", "discussion_url", "points", "created_at_i"),
            )
        elif top is None:
            summary["top_item"] = None
    elif item.source == "hugging_face":
        summary = _summary_fields(data, ("link_status", "search_truncated"))
        links = data.get("links")
        if isinstance(links, list):
            summary["link_count"] = len(links)
            summary["links_truncated"] = len(links) > SUMMARY_LINK_LIMIT
            summary["links"] = [
                _summary_fields(link, ("type", "id", "url"))
                for link in links[:SUMMARY_LINK_LIMIT] if isinstance(link, dict)
            ]
    return item.model_copy(update={
        "data": summary,
        "detail": item.detail[:SUMMARY_TEXT_LIMIT] if item.detail is not None else None,
    })


def _write_atomic(path: Path, chunks: Iterable[str]) -> Path:
    """Replace one artefact only after all chunks have been written successfully."""
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with NamedTemporaryFile(mode="w", encoding="utf-8", newline="\n", dir=destination.parent,
                                prefix=f".{destination.name}.", suffix=".tmp", delete=False) as handle:
            temporary = Path(handle.name)
            handle.writelines(chunks)
        temporary.replace(destination)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    return destination


def write_listings(
    listings: Listings, path: Path = DEFAULT_OUTPUT_PATH, *,
    evidence_path: Path | None = None,
) -> Path:
    """Write full local evidence first, then atomically replace compact site JSON.

    Both files are validated before writing and replaced individually. Evidence
    is a diagnostic snapshot, tagged with run ID; it is not canonical state.
    Evidence defaults to a sibling <stem>.evidence.jsonl derived from path,
    keeping dry-run output separate unless evidence_path is explicitly shared.
    """
    path = Path(path)
    evidence_path = path.with_suffix(".evidence.jsonl") if evidence_path is None else Path(evidence_path)
    if path.resolve() == evidence_path.resolve():
        raise ValueError("Listings and full evidence require separate paths")
    validated = Listings.model_validate_json(listings.model_dump_json())
    compact = validated.model_copy(update={"scoring_details": {
        repo_id: details.model_copy(update={
            "evidence": [_summarise_evidence(item) for item in details.evidence],
        }) for repo_id, details in validated.scoring_details.items()
    }})
    payload = Listings.model_validate_json(compact.model_dump_json()).model_dump_json(indent=2) + "\n"
    _write_atomic(evidence_path, (
        json.dumps({
            "run_id": validated.run_id, "score_version": validated.score_version,
            "generated_at": validated.generated_at.isoformat(),
            "evidence": item.model_dump(mode="json"),
        }, ensure_ascii=False, allow_nan=False) + "\n"
        for repo_id in sorted(validated.scoring_details)
        for item in validated.scoring_details[repo_id].evidence
    ))
    return _write_atomic(path, [payload])

~~~~

### pipeline/gates.py (74 lines)

~~~~
"""Publication schema and data-quality gates, evaluated before promotion."""

from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path

from pydantic import ValidationError

from pipeline.export import Listings
from pipeline.sources._enrichment import utc_time

REQUIRE_LABELS = False


class GateFailure(RuntimeError):
    """A named publication gate rejected an artefact without exposing its data."""

    def __init__(self, gate: str, rule: str, reason: str) -> None:
        self.gate = gate
        self.rule = rule
        super().__init__(f"{gate} ({rule}): {reason}")


def gate_2(path: Path) -> Listings:
    """Validate the exported envelope and PublishedListing rows, including coverage."""
    try:
        return Listings.model_validate_json(Path(path).read_bytes())
    except (OSError, ValidationError) as exc:
        # Pydantic's full error includes input values; do not copy them into issues.
        raise GateFailure("gate_2", "schema", f"Invalid listings file: {type(exc).__name__}") from None


def gate_3(
    listings: Listings, *, previous_count: int | None = None,
    now: datetime | None = None, require_labels: bool | None = None,
) -> None:
    """Require fresh, complete rows and at least 90 per cent of the last good count.

    The first run has no count baseline. Missing labels are allowed until request
    2. B1 supports only ``untested``: dated sandbox results and other statuses
    must be introduced together by request 3, never inferred here.
    """
    if previous_count is not None and (type(previous_count) is not int or previous_count < 0):
        raise ValueError("previous_count must be a non-negative integer or None")
    age = utc_time(now) - listings.generated_at
    if not timedelta(0) <= age <= timedelta(hours=7):
        raise GateFailure("gate_3", "freshness", "generated_at must be within the past 7 hours")
    if previous_count is not None and len(listings.listings) * 10 < previous_count * 9:
        raise GateFailure("gate_3", "count", "Listed count is below 90 per cent of the previous successful run")
    labels_required = REQUIRE_LABELS if require_labels is None else require_labels
    for row in listings.listings:
        if row.score is None or row.score.total is None:
            raise GateFailure("gate_3", "score", "Every listing requires an evaluated score")
        details = listings.scoring_details.get(row.repo.github_id)
        if details is None or details.licence_class not in {
            "permissive", "weak_copyleft", "strong_copyleft", "unknown", "absent",
        }:
            raise GateFailure("gate_3", "licence", "Every listing requires an explicit licence status")
        if row.tested != "untested":
            raise GateFailure("gate_3", "tested", "Only untested is supported without dated sandbox results")
        if labels_required and (row.topic is None or row.level is None):
            raise GateFailure("gate_3", "labels", "Every listing requires both topic and level")


def check_gates(
    path: Path, *, previous_count: int | None = None, now: datetime | None = None,
    require_labels: bool | None = None,
) -> dict[str, bool]:
    """Read the actual output file and return promotion gates only when both pass."""
    listings = gate_2(path)
    gate_3(listings, previous_count=previous_count, now=now, require_labels=require_labels)
    return {"gate_2": True, "gate_3": True}

~~~~

### pipeline/failure.py (70 lines)

~~~~
"""One failure record shared by rollback, the append-only log and issue text."""

from __future__ import annotations

from datetime import datetime

from pydantic import AwareDatetime, Field, JsonValue

from pipeline.budgets import BudgetExceeded
from pipeline.gates import GateFailure
from pipeline.models import Identifier, NonNegativeInt, Record
from pipeline.store import StateStore


class RunFailure(Record):
    """A failed run retained outside the promoted database."""

    run_id: Identifier
    started: AwareDatetime
    finished: AwareDatetime
    failed_step: Identifier
    reason: str
    rows_in: NonNegativeInt
    rows_out: NonNegativeInt
    previous_count: NonNegativeInt | None = None
    log_path: str
    budgets: dict[str, JsonValue] = Field(default_factory=dict)

    @property
    def issue_title(self) -> str:
        """Name the gate, budget or execution stage that stopped the run."""
        return f"Pipeline failure: {self.failed_step}"

    @property
    def issue_body(self) -> str:
        """Render diagnostics from exactly the record appended to failures.jsonl."""
        previous = "first run" if self.previous_count is None else str(self.previous_count)
        return (
            f"Run: {self.run_id}\nStarted: {self.started.isoformat()}\n"
            f"Finished: {self.finished.isoformat()}\nFailing gate, budget or stage: {self.failed_step}\n"
            f"Reason: {self.reason}\nRows in: {self.rows_in}\nRows out: {self.rows_out}\n"
            f"Previous successful count: {previous}\nLog: {self.log_path}\n"
        )


def abort_run(
    error: Exception, *, store: StateStore | None, stage: str, run_id: str,
    started: datetime, finished: datetime, rows_in: int, rows_out: int,
    log_path: str, previous_count: int | None = None,
    budgets: dict[str, JsonValue] | None = None,
) -> RunFailure:
    """Discard this run's working copy and return its single diagnostic record.

    Gate and budget errors are deliberately sanitised by their producers. Other
    exceptions retain their type only, avoiding credentials or source payloads.
    """
    if store is not None:
        store.rollback()
    failed_step = stage
    reason = type(error).__name__
    if isinstance(error, GateFailure):
        failed_step, reason = error.gate, str(error)
    elif isinstance(error, BudgetExceeded):
        failed_step, reason = f"budget.{error.resource}", str(error)
    return RunFailure(
        run_id=run_id, started=started, finished=finished, failed_step=failed_step,
        reason=reason, rows_in=rows_in, rows_out=rows_out, previous_count=previous_count,
        log_path=log_path, budgets={} if budgets is None else budgets,
    )

~~~~

### .github/workflows/refresh.yml (81 lines)

~~~~
name: Refresh repository data

"on":
  schedule:
    - cron: "17 */6 * * *"
  workflow_dispatch:

concurrency:
  group: refresh
  cancel-in-progress: false

permissions:
  contents: write
  issues: write

jobs:
  refresh:
    runs-on: ubuntu-latest
    timeout-minutes: 45
    env:
      GH_TOKEN: ${{ secrets.GH_TOKEN }}
      GH_REPO: ${{ github.repository }}
      UV_CACHE_DIR: ${{ github.workspace }}/_build/uv-cache
      UV_PYTHON_INSTALL_DIR: ${{ github.workspace }}/_build/uv-python
      UV_PROJECT_ENVIRONMENT: ${{ github.workspace }}/.venv
      UV_FROZEN: "true"
      PYTEST_DEBUG_TEMPROOT: ${{ github.workspace }}/_build/pytest
      PIPELINE_LOG_URL: ${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}
    steps:
      - name: Check out source
        uses: actions/checkout@d23441a48e516b6c34aea4fa41551a30e30af803 # v6
        with:
          token: ${{ secrets.GH_TOKEN }}
          persist-credentials: false
      - name: Set up uv
        uses: astral-sh/setup-uv@37802adc94f370d6bfd71619e3f0bf239e1f3b78 # v7
        with:
          version: "0.11.19"
          enable-cache: true
      - name: Install locked dependencies
        run: uv sync --frozen
      - name: Run unit tests
        run: |
          mkdir -p "$PYTEST_DEBUG_TEMPROOT"
          uv run pytest --cov=pipeline --cov-fail-under=80
      - name: Lint
        run: uv run ruff check .
      - name: Pull last successful state
        run: uv run pipeline release pull
      - name: Ingest, gate and promote
        run: uv run pipeline run --no-release
      - name: Upload and verify promoted state
        run: uv run pipeline release push
      - name: Report failure
        if: failure()
        shell: bash
        run: |
          mkdir -p state
          if [ ! -s state/failure-title.txt ] || [ ! -s state/failure-body.md ]; then
            printf '%s\n' 'Pipeline failure: workflow setup or checks' > state/failure-title.txt
            printf '%s\n' 'The workflow failed before a pipeline failure record was available. See the Actions log for the failing step; row counts are unavailable.' > state/failure-body.md
          fi
          printf '\nActions log: %s\n' "$PIPELINE_LOG_URL" >> state/failure-body.md
          gh label create pipeline-failure --color B60205 --description 'Pipeline refresh failure' --force
          gh issue create --label pipeline-failure --title "$(cat state/failure-title.txt)" --body-file state/failure-body.md
      - name: Retain state and diagnostics
        if: always()
        uses: actions/upload-artifact@b7c566a772e6b6bfb58ed0dc250532a479d7789f # v6
        with:
          name: refresh-${{ github.run_id }}-${{ github.run_attempt }}
          retention-days: 14
          if-no-files-found: ignore
          path: |
            state/gateway.sqlite
            state/evidence.jsonl
            state/failures.jsonl
            state/failure-title.txt
            state/failure-body.md
            state/logs/
            site/src/data/listings.json

~~~~

### tests/test_workflow.py (69 lines)

~~~~
"""Parse workflow YAML and enforce the approved schedule and publication boundary."""

import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def workflow():
    return yaml.safe_load((ROOT / ".github/workflows/refresh.yml").read_text(encoding="utf-8"))


def test_yaml_schedule_dispatch_permissions_and_concurrency():
    document = workflow()
    assert document["on"]["schedule"] == [{"cron": "17 */6 * * *"}]
    assert "workflow_dispatch" in document["on"]
    assert set(document["on"]) == {"schedule", "workflow_dispatch"}
    assert document["permissions"] == {"contents": "write", "issues": "write"}
    assert document["concurrency"] == {"group": "refresh", "cancel-in-progress": False}
    assert document["jobs"]["refresh"]["env"]["GH_REPO"] == "${{ github.repository }}"


def test_workflow_checks_then_one_release_round_trip():
    steps = workflow()["jobs"]["refresh"]["steps"]
    commands = [step["run"] for step in steps if "run" in step]
    ordered = ["uv sync --frozen", "uv run pytest --cov=pipeline --cov-fail-under=80",
               "uv run ruff check .", "uv run pipeline release pull",
               "uv run pipeline run --no-release", "uv run pipeline release push"]
    positions = [next(index for index, command in enumerate(commands) if value in command)
                 for value in ordered]
    assert positions == sorted(set(positions))
    for value in ordered[-3:]:
        step = next(step for step in steps if step.get("run") == value)
        assert "if" not in step and not step.get("continue-on-error", False)


def test_actions_pinned_and_only_approved_secret_used():
    text = (ROOT / ".github/workflows/refresh.yml").read_text(encoding="utf-8")
    assert set(re.findall(r"secrets\.([A-Za-z_][A-Za-z_0-9]*)", text)) == {"GH_TOKEN"}
    steps = workflow()["jobs"]["refresh"]["steps"]
    actions = [step for step in steps if "uses" in step]
    assert all(re.fullmatch(r"[\w-]+/[\w-]+@[0-9a-f]{40}", step["uses"]) for step in actions)
    assert any(step["uses"].startswith("astral-sh/setup-uv@") for step in actions)
    checkout = next(step for step in actions if step["uses"].startswith("actions/checkout@"))
    assert checkout["with"]["persist-credentials"] is False


def test_failure_reporting_and_diagnostic_retention():
    job = workflow()["jobs"]["refresh"]
    assert 0 < job["timeout-minutes"] <= 60
    report = next(step for step in job["steps"] if step.get("if") == "failure()")
    assert "gh issue create --label pipeline-failure" in report["run"]
    assert "--body-file state/failure-body.md" in report["run"]
    assert "state/failure-title.txt" in report["run"]
    assert "PIPELINE_LOG_URL" in report["run"]
    artefact = next(step for step in job["steps"] if step.get("uses", "").startswith("actions/upload-artifact@"))
    assert artefact["if"] == "always()"
    for path in ("state/gateway.sqlite", "state/evidence.jsonl", "state/failures.jsonl", "state/logs/"):
        assert path in artefact["with"]["path"].splitlines()


def test_dependabot_parses_and_checks_weekly():
    document = yaml.safe_load((ROOT / ".github/dependabot.yml").read_text(encoding="utf-8"))
    assert document["version"] == 2
    assert {item["package-ecosystem"] for item in document["updates"]} == {"uv", "github-actions"}
    assert all(item["schedule"]["interval"] == "weekly" for item in document["updates"])

~~~~

### README.md (77 lines)

~~~~
# AI Hub

AI Hub builds a gateway for discovering AI repositories, agent skills and MCP
servers by topic and user skill level. This first pipeline ingests GitHub
metadata, records independent evidence, calculates a versioned score and exports
validated listings. Scores reflect evaluated evidence and visible coverage;
raw stars never affect ranking. All entries remain `untested`, and CSV labels
are provisional until human review and the later labelling workflow.

## Run

Use Python 3.13, uv and GitHub CLI from the repository root. Follow the
[local environment and token setup](docs/runbook.md#run-locally), then:

```powershell
uv sync --frozen
uv run pipeline run --dry-run --limit 5
uv run pipeline gates --path site/src/data/listings.dry.json
```

Dry runs use live source APIs, temporary state and separate
`listings.dry.json` / `listings.dry.evidence.jsonl` outputs. The production command
pulls state, ingests, enriches, scores, exports, gates, promotes and uploads:

```powershell
uv run pipeline run
```

For explicitly managed transfers (also used in CI):

```powershell
uv run pipeline release pull
uv run pipeline run --no-release
uv run pipeline release push
uv run pipeline gates
```

`--limit N` caps enriched repositories; `--all-queries` expands beyond the default
six-query niche. Both are optional flags on `pipeline run`. Configure paths,
budgets and source options through `AI_HUB_*` environment variables. The default
canonical state is `state/gateway.sqlite`; the `data-latest` release carries that
database and `evidence.jsonl`. Full evidence stays outside the production site
data. Gate or budget failures retain the last good files and append diagnostics
to `state/failures.jsonl`.

## Checks

After creating `_build/pytest` and setting `PYTEST_DEBUG_TEMPROOT` as described
in the runbook:

```powershell
uv run pytest --cov=pipeline --cov-fail-under=80
uv run ruff check .
```

Tests use local fixtures and injected clients, including a fake `gh` executable;
they never call live APIs. No separate type-check command is configured.

## Layout

| Path | Purpose |
|---|---|
| `pipeline/` | Sources, budgets, state store, scoring, export, gates and CLI |
| `tests/` | Offline unit and integration tests, recorded JSON and fake CLI fixtures |
| `data/` | Candidate repositories and provisional label CSVs |
| `state/` | Ignored SQLite state, full evidence and run/failure diagnostics |
| `site/src/data/` | Generated listings; the frontend is a later request |
| `.github/workflows/refresh.yml` | Six-hourly/manual gated refresh and failure reporting |
| `.github/dependabot.yml` | Weekly uv and GitHub Actions dependency updates |
| `docs/` | Architecture, scoring policy and operational runbook |
| `.ai/` | Shared dual-agent plans and handovers |

Read the [scoring policy](docs/scoring.md) for weights, evidence limits and
unevaluated checks, and the [runbook](docs/runbook.md) for setup, failures and
rollback. Labelling, sandbox runs, the trust layer and static-site deployment
arrive in subsequent requests.

~~~~

### docs/scoring.md (179 lines)

~~~~
# Scoring policy v0

The score is a 0–100 weighted mean of evaluated components, using
`SCORE_WEIGHTS_V0` and `SCORE_VERSION` in `pipeline/config.py`. It is a triage
signal for repository discovery. It does not certify security, suitability or
successful execution. Policy changes require a new score version.

| Component | Weight | v0 normalisation to 0–100 |
|---|---:|---|
| Scorecard | 25% | Published 0–10 aggregate multiplied by 10 |
| Advisories | 20% | `100 / (1 + advisory_count)` for explicitly evaluated package evidence |
| Licence | 15% | Recognised permissive: 100; weak copyleft: 80; strong copyleft: 60 |
| Maintenance | 15% | `max(0, 100 * (1 - days_since_push / 365))` |
| Release cadence | 10% | Lower of release freshness and `100 * min(1, 30 / mean_interval_days)` |
| Contributors | 10% | `min(100, contributor_count * 10)` |
| Hacker News | 5% | `min(100, mention_count * 20)` within the observed 30-day window |
| Stars | 0% | Stored in repository metadata and diagnostics; never used for ranking |
| Star velocity | 0% | Retained in diagnostics in stars/hour; never used for ranking |

`total = sum(weight * component) / evaluated_weight` and
`coverage = evaluated_weight / all_positive_weight`. Coverage is a fraction
between 0 and 1, independent of the normalised total. For example, Scorecard 8/10
on its own produces total 80 and coverage 0.25. Do not present that result as
fully evaluated. A low evaluated value, including zero, still counts as coverage.
Each listing row exposes `coverage` directly, equal to `score.coverage`.
No evaluated components produces `total: null`, `coverage: 0`; that repository
is excluded from the listing rows but its diagnostics remain in the export.

## Evidence semantics and limits

- `present`: the requested observation was obtained and validated.
- `absent`: HTTP 404 from the deps.dev or Scorecard project lookup, no confirmed
  search matches in a complete bounded result, or missing GitHub metadata. Its
  weight is excluded. A 404 from Hugging Face or Hacker News search is `failed`.
- `unsupported`: this host, field or classification cannot be evaluated by the
  current source. Its weight is excluded.
- `failed`: network failure, an HTTP error other than a project-lookup 404, invalid response, incomplete
  search, future observation or malformed scoring input. Its weight is excluded
  and `failed_components` names affected scoring components. Raw source evidence
  remains available, including failures in unweighted Hugging Face checks.

Each adapter exposes `fetch(repo, http, *, fetched_at=None) -> Evidence`. Supply
the shared B1 `HttpClient` and `Budget`. Each supported repository makes one
lookup per adapter, plus any bounded retries. Every actual attempt is charged;
`BudgetExceeded` propagates and must abort the run. Unsupported hosts need no
request. Do not infer an ecosystem from a repository's primary language.

The [deps.dev project endpoint](https://docs.deps.dev/api/v3/#getproject) returns
project metadata, not package-version advisories. The adapter reports project
presence separately from `advisories_status: unsupported` and
`advisory_count: null`. Neither a known project nor a missing response means
zero vulnerabilities. The scoring contract accepts a future, separately verified
package assessment only when `advisories_status` is explicitly `present` and
`advisory_count` is a non-negative integer. Package resolution and such assessment
are not implemented by these tasks; ordinary T04 output leaves this 20% unevaluated.

B1 provides one `latestRelease`. That cannot establish cadence. The scorer
accepts optional `release_history` timestamps, deduplicates them and includes the
latest release. At least two distinct release dates are required; one date means
`unsupported`, none means `absent`. Mean interval is elapsed days from first to
last divided by interval count. Release freshness uses the maintenance formula
above with the latest release date. Future dates or dates preceding repository
creation fail the component. These tasks do not fetch release history, so B1
alone leaves this 10% unevaluated too.
With the current adapters and no release history, maximum coverage is 0.70.
Weights and score version remain unchanged; package resolution and any weight
rebalance are deferred to request 4 (the trust layer).

Licence classes are an explicit discovery policy, not a legal assessment.
Recognised permissive identifiers are MIT, Apache-2.0, BSD-2-Clause,
BSD-3-Clause, ISC, 0BSD, Unlicense, CC0-1.0, Zlib and BSL-1.0. Weak copyleft
includes MPL-2.0, EPL-1.0/2.0 and LGPL-2.0/2.1/3.0. Strong copyleft includes
GPL-2.0/3.0 and AGPL-3.0. The classifier recognises GitHub's unsuffixed
identifiers and normalises a trailing `-only` or `-or-later` for copyleft lookup;
for example, GPL-3.0, GPL-3.0-only and GPL-3.0-or-later all score 60.
Unrecognised identifiers/expressions are unsupported; null, empty, NONE and
NOASSERTION are absent. No terms are inferred from unknown identifiers.

The default contributor count is GitHub's `mentionableUsers` proxy, not a count
of proven contributors. The B1 opt-in REST fallback retains its provenance in
`RepoRecord.contributor_source`.

[Hugging Face full-text search](https://huggingface.co/docs/hub/search) searches
multiple content types. One combined query inspects at most 100 candidates;
only model/Space README text containing an exact repository URL qualifies.
The observed JSON web API is not a versioned guarantee. Schema drift fails
closed. Dataset hits, Space source-code hits, name-only matches and repository
prefix collisions do not establish a card link. Truncation with no confirmed
link fails; a confirmed link can be present with `search_truncated: true`.
Links are unweighted and assert neither functionality nor compatibility.

[HN Algolia search](https://hn.algolia.com/api) counts distinct story IDs with
URLs pointing to the repository or a path within it, within the inclusive
30-day UTC interval. It does not count arbitrary comments or articles that
mention the repository elsewhere. The highest-point qualifying story is the
top item (recency then ID break ties). At most 1,000 candidates are inspected;
incomplete/approximate results fail instead of supplying partial counts. Empty
searches are absent, not an evaluated zero for the scoring denominator. Stories
with `url: null` are skipped; malformed structural story fields still fail.

## Integration and export

```python
result = score_repo(repo, evidence, run_id=run_id, now=observed_at,
                    velocity=store.velocity(repo.github_id, window_hours=168))
store.add_score(result.score)
document = build_listings(repos, results, run_id=run_id, generated_at=observed_at)
write_listings(document)
```

`score_repo` returns `ScoringResult(score, details)`; `score` is the unchanged
B1 `Score`. The `details` object preserves component statuses, failed components,
licence class, raw stars/velocity and full source evidence in memory. B1 SQLite
stores scores and snapshots; diagnostics persist in the export artefacts below,
not in new database columns. B1 public signatures and migrations are unchanged.

`pipeline.export.Listings` validates the envelope: `generated_at`,
`score_version`, `run_id`, `listings` (`PublishedListing`, extending B1 `Listing`
with required row-level `coverage`) and `scoring_details`
(diagnostics keyed by GitHub ID). Identity, run/version, failure flags and
component-status consistency and matching row/score coverage are checked. CSV labels are joined case-insensitively
by current GitHub `full_name` from `data/labelled_repos_for_review.csv`.
Matching rows are always `provisional`, regardless of confidence. Missing rows
have null topic/level and `pending`. Invalid categories, duplicate names,
missing columns or a missing CSV fail export; no labels are silently invented.
This provisional name-based join does not follow renames: a renamed repository
loses its provisional label and becomes `pending` until the CSV is updated.
Gold labels in request 2 will be keyed by the stable `github_id`.

Rows sort by descending total then descending push time, with unknown push
times last. Name and stable ID break remaining ties. Raw stars and velocity
never break ties. All rows explicitly have `tested: untested` and
`unevaluated_checks: ["fake_stars", "typosquat", "sandbox_test"]`.

`write_listings` validates before replacing `site/src/data/listings.json`. Its
`scoring_details.evidence` contains compact per-source summaries: source,
repository ID, status, fetched time and a bounded detail, plus Scorecard score/date,
deps.dev advisory status/count, HN count/window/top item, or Hugging Face link
status/count and up to three links. Summaries select scalar fields, omit source
strings over 256 characters and truncate the diagnostic detail to 256 characters.
`links_truncated` flags the link-list limit; `search_truncated` retains the
upstream search limit flag. Unknown sources retain their status and detail only.
Full Scorecard checks, deps.dev project payloads and other raw fields are omitted
from the site file. Tests bound each representative row plus its diagnostics to
less than 8 KiB, even with large source payloads.

Full evidence, including excluded repositories and unevaluated sources, is
written first to a sibling `<stem>.evidence.jsonl` derived from the listings
`path` when `evidence_path` is omitted. The default destinations are
`site/src/data/listings.json` and `site/src/data/listings.evidence.jsonl`.
Each line has `run_id`, `score_version`,
`generated_at` and the original `evidence` object. This is the latest export's
diagnostic snapshot, replaced rather than appended, separate from the compact
site JSON. Pass an explicit `evidence_path=Path("state/evidence.jsonl")` to keep
production evidence outside the site tree and covered by the `state/` Git
ignore rule. The two files are replaced atomically individually, not as a transaction.
If the site replacement fails after evidence succeeds, the evidence run ID may
be newer than the site envelope. In-memory scoring results remain unmodified.

Passing `path=Path("site/src/data/listings.dry.json")` without `evidence_path`
writes `site/src/data/listings.dry.evidence.jsonl`, leaving production listings
and evidence, including `state/evidence.jsonl`, untouched. If overriding
`evidence_path`, use a separate dry-run destination such as
`Path("state/evidence.dry.jsonl")`. No canonical state is promoted, release
uploaded or site deployed by scoring/export.

## CLI publication and release retention

`pipeline run` stages the export and validates the on-disk `Listings` envelope
with gates 2 and 3 before replacing production files. The CLI explicitly routes
full production evidence to `state/evidence.jsonl` and uploads it alongside
`state/gateway.sqlite` on the `data-latest` release. It never relies on
`write_listings`' default sibling evidence path for production publication.
`pipeline run --dry-run` uses temporary state and writes only
`site/src/data/listings.dry.json` and `listings.dry.evidence.jsonl` as data
outputs, with no promotion or release transfer. Run diagnostics remain in
`state/`. See the [runbook](runbook.md) for gates, failure history, publication
ordering and recovery from interrupted multi-file updates.

~~~~

### pyproject.toml (36 lines)

~~~~
[build-system]
requires = ["setuptools>=75"]
build-backend = "setuptools.build_meta"

[project]
name = "ai-hub-pipeline"
version = "0.1.0"
description = "Repository ingestion and evidence for the AI Hub gateway"
requires-python = ">=3.13"
dependencies = ["httpx>=0.28,<1", "pydantic>=2.10,<3"]

[project.scripts]
pipeline = "pipeline.cli:main"

[dependency-groups]
dev = [
    "pytest>=8,<10",
    "pytest-cov>=6,<8",
    "pyyaml>=6,<7",
    "ruff>=0.9,<1",
]

[tool.setuptools.packages.find]
include = ["pipeline*"]

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["."]

[tool.ruff]
target-version = "py313"
line-length = 100

[tool.ruff.lint]
select = ["E4", "E7", "E9", "F"]

~~~~

### docs/phase1_architecture_and_operations.md (83 lines)

~~~~
# Phase 1 — architecture, updates, testing, deployment and maintenance

Written 07 November 2026 for the AI_Hub gateway. Decisions here are the default for every dual_dev request; a request may refine them, never silently drop them.

## In short
- One batch pipeline, no servers: GitHub Actions runs every 6 hours, rebuilds the data and the static site, and deploys only if every test gate passes.
- Back end = Python 3.13 pipeline (ingest, score, label, test, publish JSON). Front end = Astro static site on Cloudflare Pages reading that JSON.
- Nothing is called "tested" without a dated sandbox run; nothing ranks by raw stars.
- Maintenance is designed in: failed runs open a GitHub issue, the site shows its data age, the last good site stays up on failure.
- Po's label review (about one hour) is due before request 2 starts; Claude will say when.

## 1. Architecture

**Answer: three layers, all rebuilt by one scheduled job; the only moving part at run time is a static site.**

| Layer | Choice | Why |
|---|---|---|
| Ingestion | Python 3.13, `httpx`, GitHub GraphQL API, GH Archive (BigQuery free tier) for star velocity, deps.dev and OpenSSF Scorecard APIs, Hugging Face Hub API, Hacker News Firebase API | All free tier; fit a six-hourly refresh of a few thousand repos |
| State store | One SQLite file (`state/gateway.sqlite`) kept as a GitHub Release asset `data-latest` between runs, never committed | History without git bloat; trivially inspectable |
| Scoring | Trust score = Scorecard + deps.dev + licence + maintenance (last push, release cadence) + fake-star check (lockstep account clustering over GH Archive) + clone and typosquat check | Replaces stars as the ranking signal |
| Labelling | Claude API (`claude-sonnet-5-5`), README plus repo tree, run-requirement ladder (beginner / intermediate / advanced / not_runnable), cached by README hash | Cheap; only re-labels when the README changes |
| Sandbox test | Separate Actions job: clean Docker container, follow the README quickstart, 20-minute cap, records pass or fail, time to first run, date | Produces the "works first try" badge; weekly for listed repos, on first listing for new ones |
| Publish | Pipeline writes `site/src/data/*.json` (listings, topics, levels, digest) | Front end never calls an API |
| Front end | Astro static site, Tailwind, deployed to Cloudflare Pages; pages: home (ten per topic), topic, level filter, repo detail (first command, reason to trust, dated test result), weekly digest, "how we grade" | Zero servers, free hosting, fast |
| Digest | Weekly Markdown and RSS generated by the pipeline every Monday 07:00 UK | Distribution earns the audience; newsletter tooling comes later |

Repository layout (created by the requests): `pipeline/` (Python package), `tests/`, `site/` (Astro), `.github/workflows/`, `state/` (git-ignored), `docs/`, `.ai/` (dual_dev memory).

## 2. Regular updates

**Answer: every 6 hours automatically; weekly digest on Mondays; zero manual steps.**

- `refresh.yml`: cron `17 */6 * * *`. Steps: download `data-latest`, ingest, score, label changed READMEs, run gates, build site, deploy, upload new `data-latest`.
- `sandbox.yml`: nightly at 02:00 UK; tests new listings and re-tests every listed repo weekly. Writes results into the state store.
- `digest.yml`: Mondays 07:00 UK; writes `site/src/data/digest.json` and RSS, then triggers `refresh.yml`.
- Budgets per run: GitHub REST and GraphQL under 2,500 points; BigQuery under 5 GB scanned; Claude API under 200k tokens. The run aborts, not degrades, when a budget is crossed, and opens an issue.

## 3. Testing before deploy

**Answer: six gates in CI; deploy runs only when all six pass; a failed run leaves the previous site live.**

1. Unit tests (`pytest`, coverage on scoring and labelling logic at 80 per cent or better).
2. Schema gate: every output JSON validated with pydantic models; unknown level or topic values fail the run.
3. Data quality gate: data age under 7 hours; listed-repo count at least 90 per cent of the previous run; no listed repo without a level, topic, trust score and licence; no "tested" badge without a dated sandbox result.
4. Labeller gate: agreement with the gold set (`data/gold_labels.csv`, Po-reviewed) at 85 per cent or better on level, 90 per cent on topic; measured every run on the gold rows.
5. Site gate: Astro build succeeds; Playwright smoke test opens home, one topic, one repo page and the digest; internal link check passes.
6. Security gate: `pip-audit` and `npm audit` on the pipeline and site; dependency updates via Dependabot weekly.

Pull requests run gates 1, 2, 5 and 6 on a sample dataset in under five minutes. The full gates run on the schedule and on merge to `main`.

## 4. Deployment

**Answer: Cloudflare Pages from the Actions job, production on `main`, preview per pull request.**

- Secrets in GitHub Actions: `GH_TOKEN` (fine-grained, read-only public repos), `ANTHROPIC_API_KEY`, `CLOUDFLARE_API_TOKEN`, `GCP_SA_KEY` (BigQuery read-only). Never in the repo.
- Rollback: redeploy the previous Pages build from the Cloudflare dashboard, or re-run the last green Actions run.
- Domain: decided by Po before the first public release; until then the `*.pages.dev` address.

## 5. Maintenance and fixing problems

**Answer: the pipeline reports its own failures; a runbook in `docs/runbook.md` covers each known failure with the fix.**

- Alerts: any failed scheduled run opens a GitHub issue labelled `pipeline-failure` with the log link and the failing gate, and emails Po. A second failure in a row pins a red "data is stale" banner on the site via a `status.json` file.
- Observability: each run writes `state/run_log.jsonl` (duration, API points used, tokens used, rows in and out, gate results). The site footer shows "data as of" and the last gate results.
- Runbook entries, written with the first request and extended on every incident:
  - GitHub API rate limit or schema change: run aborts; check the GraphQL error, adjust the query, re-run.
  - BigQuery quota exceeded: reduce the GH Archive window to 7 days; re-run.
  - Claude API error or labeller drift (gate 4 fails): the run keeps the previous labels and deploys; open an issue; review the disagreeing rows with Po.
  - Sandbox test times out for many repos: check the runner image; mark results "untested" rather than "failed".
  - Site build or smoke test fails: the previous site stays live; fix on a branch; preview deploy; merge.
  - A listed repo reported as malicious: `pipeline/blocklist.yml` entry, immediate manual re-run, removal within 24 hours, a note in the digest.
  - Secrets expire: rotate in GitHub settings; nothing else changes.
- Dependencies: Dependabot weekly; Python pinned with `uv.lock`; Node pinned with `pnpm-lock.yaml`.
- Monthly check by Po (15 minutes): read the month's issues, the run log summary and the labeller agreement trend.

## 6. What Po must do, and when

Order changed 07 November 2026: request 2 is the MVP site on GitHub Pages (Jinja2, built-in token, no external accounts); labeller, sandbox, trust layer and the Astro site follow as requests 3 to 6. The owner steps below keep their triggers, now tied to those numbers.
- Now: run `/dual_dev_init` in this folder (it will ask before `git init`), then paste request 1 from `docs/dual_dev_requests.md`.
- After request 1 is committed and before request 2 starts: review `data/labelled_repos_for_review.csv` into `data/gold_labels.csv` (about one hour). Claude will say when.
- Before request 5: choose the domain name and create the Cloudflare account; add the four secrets to GitHub.
- Before public launch: recruit ten vibe coders for the task test (Reddit or Discord).

~~~~

### .ai/tasks/T002_mvp_site_live/REQUEST.md (18 lines)

~~~~
# Request T002_mvp_site_live

Date: 07 November 2026 · Codex model: default (gpt-6-astra) · effort: xhigh on every step · Codex tokens so far: 0

## Request (verbatim)
Build the MVP front end and make the pipeline live on GitHub, per docs/phase1_architecture_and_operations.md sections 2 to 5 with one change: the MVP site is generated by Python with Jinja2, not Astro (Astro comes in request 6). Add `pipeline/site/` and a `pipeline site build` command that reads `site/src/data/listings.json` and writes `site/dist/`: `index.html` (every topic with its top ten by trust score, a level filter with small inline JavaScript, data age and run id in the footer), one page per topic, one page per repo (score, coverage, evaluated components, licence class, last push, latest release, label with its status, tested status, GitHub link), `how_we_grade.html` rendered from docs/scoring.md, and `status.json`. Light gate 5: build succeeds, every internal link resolves, no page over 200 KB; add it to the gates. Workflow: extend `.github/workflows/refresh.yml` to build the site after a passing run and deploy to GitHub Pages (`actions/upload-pages-artifact`, `actions/deploy-pages`, permissions `pages: write` and `id-token: write`), using the built-in `GITHUB_TOKEN` for GraphQL and the release asset so no secret is needed; verify both work with that token and document any limit. Add a `README.md` section "Live site". Acceptance: `uv run pytest` green at 80 per cent coverage or better; `pipeline run --dry-run --limit 20` then `pipeline site build` produces `site/dist/` with an index and at least 20 repo pages, links valid; workflow YAML test extended. Merging to `main`, making it default and the first live dispatch are owner steps at close-out.

## Confirmed constraints
- Po's decision 07 November 2026: MVP before the quality layers; see .ai/DECISIONS.md.
- Jinja2 site generator for the MVP (Astro deferred to request 6). GitHub Pages hosting. Built-in GITHUB_TOKEN; no new secrets.
- Labels stay provisional or pending (labeller is request 3); `tested` stays `untested` (sandbox is request 4). The site must show these honestly.
- Owner steps at close-out, not in this request: merge to `main`, make it the default branch, first `workflow_dispatch`, enable Pages.
- User rules: British English, type hints, pathlib, logging not print, snake_case, no "claude" in names, no AI credit lines.

## Starting point
- Branch: dual_dev/T001_ingestion_pipeline (closed-out request 1, pushed). The request branch stacks on it; its pull request will include T001 unless T001 merges first.
- Commit: d73a1d2.

~~~~

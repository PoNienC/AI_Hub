# Context pack — C:\Users\po.nienchen\repos\AI_Hub

Branch: `dual_dev_setup` · last commit: 4a66f25 2026-11-07 Add phase 0 research, data and phase 1 plan · built 2026-11-07 11:12

Everything a planner needs is pasted below. Paths are relative to the repo root.

## Repository tree (29 tracked files)

Files per top-level folder:
~~~~
    9  research_notes/
    7  data/
    4  .ai/
    3  (root)
    2  docs/
    2  reports/
    2  scripts/
~~~~

All paths:
~~~~
.ai/DECISIONS.md
.ai/PROJECT.md
.ai/STATE.md
.ai/tasks/.gitkeep
.gitignore
AGENTS.md
CLAUDE.md
data/candidate_repos.csv
data/labelled_repos_for_review.csv
data/labelling_set.csv
data/labelling_set_part_a.csv
data/labelling_set_part_b.csv
data/labels_part_a.csv
data/labels_part_b.csv
docs/dual_dev_requests.md
docs/phase1_architecture_and_operations.md
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
- GitHub account for this remote: `PoNienC` (personal; decided by Po, 07 November 2026). The GitHub CLI also holds `PoNienChenPP` (work); switch with `gh auth switch -u PoNienC` only after telling the user. No remote configured yet.
- Codex execution on this machine (PRIORPLAP180): available (07 November 2026). Read probe: exit 0, write to repo blocked. Write probe in a throwaway repo: exit 0, file created. Model default gpt-6-astra.

~~~~

### .ai/STATE.md

~~~~
# State — 07 November 2026

- Branch: `dual_dev_setup` (stacked on an unborn `main`; no commits yet).
- Last commit: none.
- Work in flight: dual_dev setup (this branch). Phase 1 request 1 (ingestion pipeline) is next, from `docs/dual_dev_requests.md`.
- Other branches touching AGENTS.md or CLAUDE.md: none (fresh repository).
- Codex probes passed 07 November 2026 (read: 95 s, 12,387 tokens; write: 7,819 tokens; weekly limit 21 per cent used).
- Known issues: labels in `data/labelled_repos_for_review.csv` are unreviewed LLM candidates; no repo has been executed; `data/readmes/` is ignored and must be re-fetched with `scripts/sample_and_fetch.py`.
- Owner actions pending: review the 100 labels into `data/gold_labels.csv` before request 2; domain, Cloudflare account and four GitHub secrets before request 5.

## Sources
- Repository contents on 07 November 2026; `docs/phase1_architecture_and_operations.md` section 6.
- Root `HANDOVER.md` (personal, ignored): the approval of phase 1 and the niche on 07 November 2026, and the pending-actions list.

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

~~~~

### CLAUDE.md

~~~~
# AI_Hub

@AGENTS.md

~~~~

## Relevant files in full (7)

### docs/phase1_architecture_and_operations.md (81 lines)

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
- Now: run `/dual_dev_init` in this folder (it will ask before `git init`), then paste request 1 from `docs/dual_dev_requests.md`.
- After request 1 is committed and before request 2 starts: review `data/labelled_repos_for_review.csv` into `data/gold_labels.csv` (about one hour). Claude will say when.
- Before request 5: choose the domain name and create the Cloudflare account; add the four secrets to GitHub.
- Before public launch: recruit ten vibe coders for the task test (Reddit or Discord).

~~~~

### docs/dual_dev_requests.md (24 lines)

~~~~
# dual_dev requests for phase 1 — paste one at a time

Each request is under 250 words and points at `docs/phase1_architecture_and_operations.md` as the target. Run them in order; each one should end committed on its own branch with the test gates green before the next starts.

## Request 1 — ingestion pipeline and state store

/dual_dev Build the ingestion pipeline described in docs/phase1_architecture_and_operations.md sections 1 and 2. Python 3.13 package `pipeline/` with uv. Sources: GitHub GraphQL (repo metadata, releases, contributors for repos matching the topic queries in scripts/pull_candidate_repos.py), GH Archive WatchEvents over the last 30 days through BigQuery for star velocity, deps.dev and OpenSSF Scorecard for trust inputs, Hugging Face Hub API for model and Space links, Hacker News Firebase for mentions. State: one SQLite file `state/gateway.sqlite` with tables for repos, snapshots, scores and run_log, uploaded as the GitHub Release asset `data-latest` at the end of each run and downloaded at the start. Scoring: a trust score as defined in section 1, no raw-star ranking. Output: `site/src/data/listings.json` validated with pydantic. Workflow `.github/workflows/refresh.yml` on cron `17 */6 * * *` with budgets and the abort rule from section 2, and gates 1, 2 and 3 from section 3. Write `docs/runbook.md` with the first four runbook entries from section 5. Acceptance: `uv run pytest` green with coverage at 80 per cent or better; a dry run against 50 repos completes in under 10 minutes and produces a valid listings.json; the workflow passes on a manual dispatch. British English, type hints, pathlib, logging not print.

## Request 2 — labeller and gold-set gate

/dual_dev Add the skill-level and topic labeller from docs/phase1_architecture_and_operations.md section 1, as `pipeline/labelling/`. Input: README and top-level tree per repo from the state store. Model: Claude API `claude-sonnet-5-5`, one call per repo, cached by README hash in the SQLite store so unchanged READMEs are never re-labelled. Labels: topic from the fixed list in data/labelled_repos_for_review.csv; level from the run-requirement ladder (beginner, intermediate, advanced, not_runnable) with a one-line reason and an "afternoon line" under 20 words; confidence high, medium or low. Gate 4: compute agreement against `data/gold_labels.csv` on every run; fail the run below 85 per cent on level or 90 per cent on topic, keeping the previous labels live. Add a `pipeline labels --report` command that prints the disagreeing rows for review. Acceptance: pytest green; agreement on the gold set reported in the run log; token use per full relabel under 200k; a budget abort opens a GitHub issue. No API key in the repo.

## Request 3 — sandbox install tests

/dual_dev Add the sandbox test job from docs/phase1_architecture_and_operations.md sections 1 and 2. Workflow `.github/workflows/sandbox.yml` nightly at 02:00 UK: for each newly listed repo and each listed repo not tested in 7 days, start a clean `python:3.13` or `node:22` Docker container chosen from the repo language, execute the README quickstart commands extracted by `pipeline/sandbox/extract.py` (install step and first run command), 20-minute cap, no network secrets. Record pass or fail, time to first run, log tail and date in the state store, and expose `tested` (pass, fail, untested) with the date in listings.json. The "works first try" badge appears only on a dated pass. Start with the 30 highest-scoring coding-agent-stack repos. Acceptance: pytest green for the extractor on the 100 READMEs in data/readmes; the workflow runs end to end on five repos in manual dispatch; a timeout records "untested", not "fail"; runbook entry added.

## Request 4 — trust layer and blocklist

/dual_dev Complete the trust layer from docs/phase1_architecture_and_operations.md section 1: fake-star check (lockstep clustering of low-activity accounts over GH Archive WatchEvents, flag when more than 20 per cent of 30-day stars come from such clusters), clone and typosquat check (name similarity against the top 500 listed repos plus star ratio under 1 per cent), licence classification (permissive, copyleft, none), maintenance score (last push, release cadence, open issue ratio), and `pipeline/blocklist.yml` with an immediate removal path. Add gate 6 (`pip-audit`, `npm audit`, Dependabot config). Expose a "reason to trust" sentence per repo in listings.json built from these signals. Acceptance: pytest green including a synthetic fake-star fixture that is flagged and a genuine fixture that is not; a blocklisted repo disappears from listings.json on the next run; runbook entry for a malicious-listing report.

## Request 5 — static site, digest and deploy

/dual_dev Build the front end from docs/phase1_architecture_and_operations.md sections 1, 3 and 4: Astro static site in `site/` with Tailwind, reading `site/src/data/*.json`. Pages: home (ten per topic, level filter), topic, repo detail (first command to run, reason to trust, dated test result, level and reason), weekly digest, "how we grade", status footer with data age and last gate results. Weekly digest generator `pipeline/digest/` on `digest.yml` Mondays 07:00 UK writing digest.json and RSS. Gate 5: Astro build, Playwright smoke on four pages, internal link check. Deploy to Cloudflare Pages from `refresh.yml` only after all gates pass; preview deploys on pull requests; `status.json` banner when two runs fail in a row. Acceptance: all six gates green on a manual dispatch; Lighthouse performance 90 or better on home and a repo page; site works at phone width; no external script except Cloudflare analytics.

~~~~

### scripts/pull_candidate_repos.py (94 lines)

~~~~
"""Pull candidate AI repositories from the GitHub search API for the phase 0 labelling set.

Data layer: data_ingestion. No spatial data; no CRS applies.
Writes data/candidate_repos.csv (relative to the project root). Needs an authenticated `gh` CLI.
"""
from __future__ import annotations

import csv
import json
import logging
import subprocess
import time
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
LOG = logging.getLogger("pull_candidate_repos")

QUERIES: dict[str, str] = {
    "llm": "topic:llm stars:>3000",
    "ai_agents": "topic:ai-agents stars:>1000",
    "agents": "topic:agents stars:>2000",
    "mcp": "topic:mcp stars:>500",
    "mcp_server": "topic:mcp-server stars:>300",
    "claude_code": "claude-code in:name,description,topics stars:>300",
    "rag": "topic:rag stars:>1000",
    "generative_ai": "topic:generative-ai stars:>2000",
    "local_inference": "topic:llama stars:>2000",
    "coding_agent": "coding agent in:description stars:>1000",
    "computer_use": "topic:browser-automation topic:ai stars:>500",
    "voice": "topic:text-to-speech stars:>2000",
    "image_video": "topic:stable-diffusion stars:>3000",
    "evals": "topic:llm-evaluation stars:>300",
    "fine_tuning": "topic:fine-tuning stars:>1000",
    "new_2026": "created:>2026-01-01 stars:>1500 ai OR llm OR agent in:name,description,topics",
    "new_h2_2025": "created:2025-07-01..2025-12-31 stars:>3000 ai OR llm OR agent in:name,description,topics",
}
FIELDS = [
    "query_tag", "full_name", "stars", "forks", "language", "license", "created_at",
    "pushed_at", "open_issues", "topics", "description", "html_url",
]


def search(query: str, per_page: int = 100) -> list[dict]:
    """Run one GitHub repository search sorted by stars and return raw items."""
    cmd = [
        "gh", "api", "-X", "GET", "search/repositories",
        "-f", f"q={query}", "-f", "sort=stars", "-f", "order=desc", "-f", f"per_page={per_page}",
    ]
    out = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", check=True).stdout
    return json.loads(out).get("items", [])


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    out_path = root / "data" / "candidate_repos.csv"
    seen: set[str] = set()
    rows: list[dict] = []
    for tag, query in QUERIES.items():
        try:
            items = search(query)
        except subprocess.CalledProcessError as exc:
            LOG.error("query %s failed: %s", tag, exc.stderr[:200])
            continue
        LOG.info("%s: %d items", tag, len(items))
        for it in items:
            name = it["full_name"]
            if name in seen:
                continue
            seen.add(name)
            rows.append({
                "query_tag": tag,
                "full_name": name,
                "stars": it["stargazers_count"],
                "forks": it["forks_count"],
                "language": it.get("language") or "",
                "license": (it.get("license") or {}).get("spdx_id", "") or "",
                "created_at": it["created_at"][:10],
                "pushed_at": it["pushed_at"][:10],
                "open_issues": it["open_issues_count"],
                "topics": ";".join(it.get("topics", [])),
                "description": (it.get("description") or "").replace("\n", " ")[:300],
                "html_url": it["html_url"],
            })
        time.sleep(2.5)  # search API allows 30 requests a minute
    with out_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    LOG.info("wrote %d unique repos to %s", len(rows), out_path)


if __name__ == "__main__":
    main()

~~~~

### scripts/sample_and_fetch.py (102 lines)

~~~~
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
    res = subprocess.run(["gh", "api", path], capture_output=True, text=True, encoding="utf-8", errors="replace")
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
    for tag, items in by_tag.items():
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

~~~~

### .ai/PROJECT.md (45 lines)

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
- GitHub account for this remote: `PoNienC` (personal; decided by Po, 07 November 2026). The GitHub CLI also holds `PoNienChenPP` (work); switch with `gh auth switch -u PoNienC` only after telling the user. No remote configured yet.
- Codex execution on this machine (PRIORPLAP180): available (07 November 2026). Read probe: exit 0, write to repo blocked. Write probe in a throwaway repo: exit 0, file created. Model default gpt-6-astra.

~~~~

### .gitignore (19 lines)

~~~~
# Pipeline state and large re-fetchable data
state/
data/readmes/

# Codex run logs (large)
.ai/tasks/*/codex/*.log

# Personal note, never committed
/HANDOVER.md

# Environments and caches
.venv/
node_modules/
__pycache__/
*.pyc
.env
.env.*
site/dist/

~~~~

### .ai/DECISIONS.md (11 lines)

~~~~
# Decisions

Format: date · decision · context · alternatives · consequences

- 07 November 2026 · Phase 1 is built through the dual_dev workflow (Claude plans and audits, Codex executes) · Po's instruction after phase 0 · single-agent build · every build item is one `/dual_dev` request; see `docs/dual_dev_requests.md`.
- 07 November 2026 · First niche is the coding-agent stack (coding agents, skills and rules packs, MCP servers) · phase 0 gap table and growth evidence, `reports/AI repo gateway competitor landscape.md` · all ten topics at once · ingestion and sandbox tests scoped to the niche first.
- 07 November 2026 · Rank by a trust score, never by raw stars · own data: Spearman 0.08 between stars and run-readiness on 100 repos; fake-star literature · star velocity ranking · scoring defined in `docs/phase1_architecture_and_operations.md` section 1.
- 07 November 2026 · No "tested" badge without a dated sandbox run · every competitor's "verified" meant paid placement or publisher identity · README-signal proxies · nightly sandbox job, request 3.
- 07 November 2026 · Batch pipeline plus static site, no servers · solo maintainer, free tiers · API back end · GitHub Actions every 6 hours, Cloudflare Pages.
- 07 November 2026 · GitHub account `PoNienC` for this project · personal project · work account `PoNienChenPP` · recorded in `.ai/PROJECT.md`.

~~~~

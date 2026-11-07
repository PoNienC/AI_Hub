# Gate 1 — plan choice: T001_ingestion_pipeline ingestion pipeline and state store

- Date: 07 November 2026
- Codex: model gpt-6-astra, effort xhigh
- Full plans: [PLAN_A.md](PLAN_A.md) (Claude) · [PLAN_B.md](PLAN_B.md) (Codex)
- Decision: **C Hybrid**, 07 November 2026. User: "C Hybrid (Recommended)"; hybrid details: "Yes, all three (Recommended)" (provisional labels with label_status, versioned weights v0, six coding-agent-stack queries as default scope).

## Decision needed

Choose one: **A** Claude's plan · **B** Codex's plan · **C** Hybrid (below) · **D** Revise both.

Recommendation: **C** — Claude's nine finer tasks (better for audits and allocation) carrying Codex's five robustness contracts, which Claude's plan missed.

## In short

- **Both deliver:** the same package shape (config, sources, SQLite store, scoring, pydantic export, gates, CLI, workflow, runbook), the same six-hourly cron, velocity from own snapshots, no BigQuery.
- **Biggest difference:** Codex found a real conflict in the request: gate 3 demands a level and topic on every listed repo, but the labeller only arrives in request 2. Claude's plan did not see it.
- **Why the recommendation:** Codex's contracts make the pipeline safe to run unattended; Claude's task split keeps each audit scope small and lets two tasks run in parallel.

## Key differences

### 1. Labels before the labeller exists

Codex spotted that T001 cannot satisfy "no listed repo without a level and topic". Hybrid: listings carry provisional labels from `data/labelled_repos_for_review.csv` where present, else null with `label_status: pending`; gate 3's label rule is switched on in request 2. Codex better.

### 2. Which repos are in scope

Codex asks which query subset defines the niche; Claude lifted all 17 queries. Hybrid: config selects a niche (coding-agent stack = coding_agent, claude_code, mcp, mcp_server, ai_agents, agents queries) with a flag for the full set. Codex better.

### 3. State store safety

Codex adds schema versioning, a working copy, transactional writes, keeping the previous database and output on any failure, and rename handling. Claude's store was a plain upsert. Codex better.

### 4. Evidence semantics in scoring

Codex keeps "unavailable" distinct from "negative" evidence, versions the weights, and marks request-4 checks as unevaluated in the output. Claude had a first-cut score only. Codex better.

### 5. Task granularity

Claude: nine tasks, two independent (GitHub source and enrichment adapters), release and CLI separate from the workflow. Codex: seven larger tasks, three rated high risk. Claude better for block audits and a possible Codex execution split.

### 6. Contributor data via GraphQL

Codex flags that GraphQL contributor coverage is uncertain and asks for a documented REST fallback. Claude assumed `mentionableUsers`. Codex better.

### 7. Workflow hardening

Codex adds concurrency protection, frozen installs and a split between read and write credentials. Claude had the cron, dispatch and issue creation. Hybrid takes both.

## Recommended hybrid (option C)

1. Package skeleton, pydantic models, config with niche selection, budgets and versioned weights v0 — source: A + B — depends on: —
2. State store: schema version, transactions, working copy and previous-run retention, snapshots, velocity, rename handling — source: B — depends on: 1
3. GitHub GraphQL source: pagination, dedupe, partial-error handling, budget accounting, contributor coverage check with documented REST fallback — source: A + B — depends on: 1
4. Enrichment adapters: deps.dev, Scorecard, Hugging Face, Hacker News, each distinguishing unsupported, absent and failed — source: A + B — depends on: 1
5. Scoring (versioned, star-independent, unevaluated checks marked) and export with provisional labels and label_status — source: B — depends on: 2, 3, 4
6. Gates 2 and 3 (T001 variant: label rule off) and budget abort with issue text — source: A + B — depends on: 5
7. Release round trip with recoverable promotion, and the CLI orchestration with `--dry-run` and `--limit` — source: A + B — depends on: 2, 6
8. Workflow (cron, dispatch, concurrency, frozen install, permissions split, issue on failure), `docs/runbook.md` first four entries, `docs/scoring.md`, README — source: A + B — depends on: 7
9. Dry run against 50 repos, timed, recorded in the handover — source: A — depends on: 8

## Open questions for you

- Labels in T001: provisional from the review CSV with `label_status`, as in the hybrid? (Recommended yes.)
- Scoring weights: ship versioned v0 with unevaluated checks shown, tune in request 4? (Recommended yes.)
- Niche: the six coding-agent-stack queries as the default scope? (Recommended yes.)

## Risks only one plan found

| Risk | Found by | Severity | Mitigation |
|---|---|---|---|
| Gate 3 unsatisfiable before request 2 (labels) | Codex | High | provisional labels and label_status; rule switched on in request 2 |
| State replaced by a bad run | Codex | High | working copy, keep previous on failure |
| GraphQL contributor coverage wrong | Codex | Medium | coverage check, REST fallback documented |
| Velocity null on first run fails gate 3 | Claude | Medium | gate allows null velocity when no prior snapshot |
| Release upload untestable live without a remote | Claude | Low | fake `gh` in tests; owner creates remote |

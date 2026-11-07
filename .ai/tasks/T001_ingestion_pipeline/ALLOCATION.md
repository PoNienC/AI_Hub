# Gate 2 — execution split: T001_ingestion_pipeline ingestion pipeline and state store

- Date: 07 November 2026
- Approved plan: [PLAN_APPROVED.md](PLAN_APPROVED.md) · Gate 1 record: [COMPARISON.md](COMPARISON.md)
- Codex execution on this machine: available, 07 November 2026 (from `.ai/PROJECT.md`)
- Codex: model gpt-6-astra, effort xhigh · [what the options mean](C:\Users\po.nienchen\.claude\skills\dual_dev\templates\gate2_standing_options.md)
- Decision: **B split as proposed**, per_block with overlap on, audit review ask_high, xhigh gpt-6-astra. 07 November 2026. User: "B Split as proposed (Recommended)"; "per_block, overlap on (Recommended)"; "ask_high (Recommended)"; "xhigh, gpt-6-astra (Recommended)".

## In short

- **Split:** B — Codex executes T01 to T08 (the whole coded pipeline, independent of the live network), Claude executes T09 (the real-network dry run, which needs this machine's `gh` login) and audits every Codex block. This is the "Claude plans and audits, Codex executes" model Po chose on 07 November 2026.
- **Audit mode:** per_block with overlap on — 4 audit points (B1, B2, B3 by Claude's audit subagent; B4 by Codex); 3 Codex execute calls plus 1 Codex audit, plus correction calls as needed. Overlap buys little here because every block depends on the one before, so blocks run one after another.
- **Audit review:** ask_high — two tasks are high risk (T03, T05); you are stopped only for a BLOCKER or HIGH finding; expected stops for you: 0 to 2.
- **Effort and model:** standing table, xhigh on every step, gpt-6-astra. Watch point: three xhigh execute calls could move the weekly limit from 23 per cent towards 60 per cent; if any limit passes 80 per cent the workflow stops and asks before the next call.

## Proposed split

| Task | Title | Executor | Reviewer | Block | Depends on | Risk | Why this executor |
|---|---|---|---|---|---|---|---|
| T01 | Package skeleton, models and config | Codex | Claude subagent | B1 | — | low | self-contained, fixture-tested |
| T02 | State store with safe promotion | Codex | Claude subagent | B1 | T01 | medium | pure SQLite logic, interface fixed by T01 models |
| T03 | GitHub GraphQL source and budgets | Codex | Claude subagent | B1 | T01 | high | fixture-tested; closes B1 as a high-risk task |
| T04 | Enrichment adapters | Codex | Claude subagent | B2 | T01 | medium | four independent adapters, one parametrised test |
| T05 | Scoring and export | Codex | Claude subagent | B2 | T02, T03, T04 | high | contract fully specified in the plan; closes B2 |
| T06 | Gates 2 and 3 and abort rule | Codex | Claude subagent | B3 | T05 | low | rule table in the plan |
| T07 | Release round trip and CLI | Codex | Claude subagent | B3 | T02, T06 | medium | fake `gh` keeps it offline |
| T08 | Workflow, runbook and docs | Codex | Claude subagent | B3 | T07 | low | documentation and YAML; executor changes next |
| T09 | Dry run against 50 repos | Claude | Codex | B4 | T08 | medium | needs the real network and this machine's `gh` auth |

## Blocks and audit points

| Block | Tasks | Executor | Reviewer | Closes because | Overlap with next block? |
|---|---|---|---|---|---|
| B1 | T01-T03 | Codex | Claude subagent | high-risk task T03 | no — B2 depends on T01 and T03 |
| B2 | T04-T05 | Codex | Claude subagent | high-risk task T05 | no — B3 depends on T05 |
| B3 | T06-T08 | Codex | Claude subagent | executor changes next | no — B4 depends on T08 |
| B4 | T09 | Claude | Codex | last task | — |

## Order of work

1. B1: one Codex execute call for T01-T03 → Claude checks the diff, runs tests and ruff, commits → subagent audits B1 (about 15 to 20 minutes) → fixes by Codex if any → commit.
2. B2: Codex execute T04-T05 → same cycle.
3. B3: Codex execute T06-T08 → same cycle.
4. B4: Claude runs T09 (dry run), records results, commits → Codex audits B4 in the background.
5. Hand-off: full test suite, `REVIEW.md`; you review while the last audit finishes → fixes → your go-ahead → completion → push question.

## Git plan

- Branch: `dual_dev/T001_ingestion_pipeline` (stacked on `dual_dev_setup`) · commit format: `T01-T03 <short title>` for a Codex block, `T09 <title>`, `B1 audit fixes (T01-T03)` · push policy: no push without approval; no remote exists yet.

## Cost so far

- Codex calls: 1 (planning) · tokens: 21,405 · plan limit: 23% used, resets Wednesday 11 November 10:05

## Risks of the split

- Codex writes every interface (models, store, sources) in B1; a weak `models.py` propagates to B2 and B3. Mitigation: B1 is audited before B2 starts (no overlap).
- Codex's sandbox may block `uv sync` network access for dependency download; if so Claude installs the environment before the B1 call and reports it.
- T09 is the only task touching the real network; if the dry run exposes a source bug, the fix becomes a new Codex correction call, not a Claude edit.

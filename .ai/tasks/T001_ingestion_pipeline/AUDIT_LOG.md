# Audit log — T001_ingestion_pipeline: ingestion pipeline and state store

Audit mode: per_block (overlap on) · Audit review: ask_high.

- One section per audit scope and round. Each opens with "In short", then
  one titled line per finding, then the full table.
- Findings in the table are copied verbatim from the reviewer; the executor
  proposes a resolution for each, with a reason.
- Under `ask` (or `ask_high` with a BLOCKER/HIGH) nothing is fixed until you
  fill "Your decision"; your decision wins.
- Round 2 (re-check of a BLOCKER/HIGH fix) is the last automatic round; a
  BLOCKER or HIGH it finds always comes to you.
- Raw reviewer output: `codex/` (Codex) and `subagent/` (Claude's audit subagent).

## B1 (T01-T03) — round 1 · executor: Codex · reviewer: Claude subagent (dual_dev_auditor, session model) · 07 November 2026

Range: `ac9cffe..501f79e` (base `ac9cffe`, end `501f79e`)
Review: ask_high · no BLOCKER or HIGH → auto (no stop for the user) · closed 07 November 2026, fixes in `9793c48` (Codex resolutions: F1 ACCEPTED, F2 PARTIALLY_ACCEPTED docstring, F3 ACCEPTED, F4 ACCEPTED, F5 DEFERRED, F6 DEFERRED, F7 PARTIALLY_ACCEPTED a and c) · raw report: subagent/B1_audit_r1_out.md

**In short:** PASS_WITH_FINDINGS · findings B/H/M/L/N: 0/0/2/2/3 · needs you: no

- **F1 (MEDIUM, T03) Retries abort on real GitHub error bodies** → ACCEPTED: settle the reservation with a fixed estimate on answered non-success responses; keep the abort for transport errors; add a 502-HTML-then-200 test.
- **F2 (MEDIUM, T03) API version 2026-03-10 undocumented** → PARTIALLY_ACCEPTED: Claude verified live on 07 November 2026 that REST (`rate_limit`) and GraphQL both accept `X-GitHub-Api-Version: 2026-03-10` (HTTP 200). Keep the value; add the verification date and a fallback note to the module docstring.
- **F3 (LOW, T01) Ruff rules not pinned** → ACCEPTED: pin `[tool.ruff.lint] select` and `line-length` in pyproject.toml; ruff must stay clean.
- **F4 (LOW, T01) Listing.score_version can diverge** → ACCEPTED: after-validator plus one mismatch test.
- **F5 (NOTE, cross-task) Failed runs leave no run_log trace** → DEFERRED to T07: append-only failure log outside the promoted database; recorded in DECISIONS.md and the B3 brief.
- **F6 (NOTE, cross-task) Stale working copy blocks runs** → DEFERRED to T07 and T08: CLI pre-flight message and runbook entry; in the B3 brief.
- **F7 (NOTE, T01) Config and test-isolation rough edges** → ACCEPTED (a) and (c); (b) left as the plan's parity test requires the import.

| ID | Task | Severity | Finding | Proposed resolution | Reason | Planned fix | Your decision | Outcome |
|---|---|---|---|---|---|---|---|---|
| F1 | T03 | MEDIUM | GraphQL retries abort the run in every realistic failure case (reservation never settled when the error body has no rateLimit) | ACCEPTED | real 5xx bodies lack `data.rateLimit`; retries are dead code | estimate cost on answered non-success responses, log it, keep abort for transport errors; new test | — (auto) | fixed in `9793c48` |
| F2 | T03 | MEDIUM | `X-GitHub-Api-Version: 2026-03-10` not a documented version | PARTIALLY_ACCEPTED | verified live 07 Nov 2026: accepted by REST and GraphQL | docstring: verification date, fallback to 2022-11-28 if rejected | — (auto) | fixed in `9793c48` |
| F3 | T01 | LOW | Ruff rule selection not pinned | ACCEPTED | CI and local must agree | `[tool.ruff.lint] select`, `line-length` | — (auto) | fixed in `9793c48` |
| F4 | T01 | LOW | Listing.score_version can disagree with score.score_version | ACCEPTED | publication contract | after-validator and test | — (auto) | fixed in `9793c48` |
| F5 | T02→T07 | NOTE | failed runs leave no trace in run_log | DEFERRED | design choice belongs to T07 | append-only failure log; B3 brief | — (auto) | deferred |
| F6 | T02→T07/T08 | NOTE | stale working copy blocks every later run | DEFERRED | CLI and runbook belong to T07/T08 | pre-flight message; runbook entry; B3 brief | — (auto) | deferred |
| F7 | T01 | NOTE | config and test-isolation rough edges | ACCEPTED (a, c) | cheap now | ValueError wrap; explicit mapping in test | — (auto) | fixed in `9793c48` |


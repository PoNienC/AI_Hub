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


## B2 (T04-T05) — round 1 · executor: Codex · reviewer: Claude subagent (dual_dev_auditor, session model) · 07 November 2026

Range: `9793c48..4c87086` (base `9793c48`, end `4c87086`)
Review: ask_high · HIGH present → reviewed by the user 07 November 2026: "A Approve as proposed" (every proposed resolution stands) · Codex resolutions: F1 ACCEPTED, F2 PARTIALLY_ACCEPTED (coverage on row), F3 ACCEPTED, F4 ACCEPTED, F5 ACCEPTED, F6 ACCEPTED, F7 ACCEPTED, F8 DEFERRED to T09, F9 PARTIALLY_ACCEPTED · fixes in `6653b63` · round 2 re-check of the fix commit running · raw report: subagent/B2_audit_r1_out.md

**In short:** PASS_WITH_FINDINGS · findings B/H/M/L/N: 0/1/3/4/1 · needs you: yes (one HIGH)

- **F1 (HIGH, T05) Copyleft licences never recognised** → ACCEPTED: GitHub emits `GPL-3.0`, `AGPL-3.0`, `LGPL-2.1` without `-only`/`-or-later`; normalise the id and test against the real values in data/candidate_repos.csv; fix docs/scoring.md.
- **F2 (MEDIUM, cross-task) Advisories weight is dead by construction** → PARTIALLY_ACCEPTED: expose `coverage` on each listing row now and record the decision; full deps.dev package resolution and any weight rebalance go to request 4 (trust layer), where the fake-star and typosquat components also land and the score version changes once.
- **F3 (MEDIUM, T05) Raw adapter payloads in listings.json** → ACCEPTED: compact per-source summary in listings.json; full evidence to `state/evidence.jsonl` (not shipped); per-row size-bound test.
- **F4 (MEDIUM, T04) Null HN url fails the component** → ACCEPTED: skip the hit; fixture with `url: null`.
- **F5 (LOW, T04) 404 from search endpoints reported as absent** → ACCEPTED: `absent_statuses` argument; search adapters map 404 to failed.
- **F6 (LOW, T04) deps.dev identity check weaker** → ACCEPTED: same `links_repo` check as Scorecard.
- **F7 (LOW, T05) Labels join by name only** → ACCEPTED (documentation only): note in docs/scoring.md; keyed by github_id when gold labels arrive (request 2).
- **F8 (LOW, T04) Live API shapes unverified** → DEFERRED to T09: record one real response per adapter as a fixture.
- **F9 (NOTE) Lint intent and test hygiene** → PARTIALLY_ACCEPTED: close the client with `with`; E501 left off.

| ID | Task | Severity | Finding | Proposed resolution | Reason | Planned fix | Your decision | Outcome |
|---|---|---|---|---|---|---|---|---|
| F1 | T05 | HIGH | copyleft SPDX ids from GitHub (`GPL-3.0`, `AGPL-3.0`, `LGPL-2.1`) never match; copyleft repos lose the licence weight | ACCEPTED | ranking bias on about 9% of repos; proven by own CSVs | normalise suffixes and add GitHub ids; parametrised test over real licence values; docs fix | approve | fixed in `6653b63` |
| F2 | T04/T05 | MEDIUM | advisories component always unsupported; max coverage 0.70; not visible on the row | PARTIALLY_ACCEPTED | design limit of deps.dev project endpoint; weight change belongs with request 4 | add `coverage` to the listing row; DECISIONS entry; request 4 resolves packages or rebalances | approve (partial: coverage on the row; rest to request 4) | fixed in `6653b63` |
| F3 | T05 | MEDIUM | full adapter payloads serialised into the site JSON | ACCEPTED | multi-megabyte site file | compact summary in listings.json; full evidence to state/evidence.jsonl; size test | approve | fixed in `6653b63` |
| F4 | T04 | MEDIUM | HN hit with null url raises and fails the component | ACCEPTED | benign input | skip null-url hits; fixture | approve | fixed in `6653b63` |
| F5 | T04 | LOW | 404 from HF or HN search mapped to absent | ACCEPTED | silent signal loss | `absent_statuses` parameter | approve | fixed in `6653b63` |
| F6 | T04 | LOW | deps.dev project identity not verified | ACCEPTED | parity with Scorecard | `links_repo` check | approve | fixed in `6653b63` |
| F7 | T05 | LOW | provisional labels join by full_name only | ACCEPTED (docs) | gold labels not yet available | note in docs/scoring.md | approve (docs) | fixed in `6653b63` |
| F8 | T04 | LOW | live API shapes unverified | DEFERRED | only T09 can confirm | record real fixtures in T09 | approve (defer to T09) | fixed in `6653b63` |
| F9 | cross | NOTE | line-length advisory; unclosed client in a test | PARTIALLY_ACCEPTED | cosmetic | `with` on the client | approve (partial) | fixed in `6653b63` |


## B2 (T04-T05) — round 2 (re-check of the fix commit) · executor: Codex · reviewer: Claude subagent (dual_dev_auditor, session model) · 07 November 2026

Range: `4c87086..6653b63` (base `4c87086`, end `6653b63`) · raw report: subagent/B2_audit_r2_out.md
Review: ask_high · no BLOCKER or HIGH → auto · closed 07 November 2026, fixes in `b6fcae5` (F1, F2, F5 ACCEPTED; F3, F4 DEFERRED to B3) · the last automatic round; the LOW fixes below get no further audit

**In short:** PASS_WITH_FINDINGS · round-1 HIGH resolved and verified · findings B/H/M/L/N: 0/0/0/3/2 · needs you: no

- **F1 (LOW, T05) Zero-coverage envelope rule no longer tested** → ACCEPTED: set both row and score coverage to 0 in the test mode.
- **F2 (LOW, T05→T07) Dry-run evidence can overwrite the real file** → ACCEPTED: derive the evidence path from the listings path; T07 brief names both paths.
- **F3 (LOW, T05→T07/T08) Full evidence lost on the CI runner** → DEFERRED to T07: upload `evidence.jsonl` alongside the SQLite asset; in the B3 brief.
- **F4 (NOTE, T05→T06) Exported rows are `PublishedListing`, not `Listing`** → DEFERRED to T06: gate 2 validates `pipeline.export.Listings`; in the B3 brief.
- **F5 (NOTE, T05) Licence canary fails with a bare KeyError** → ACCEPTED: `pytest.fail` with a clear message.

| ID | Task | Severity | Finding | Proposed resolution | Reason | Planned fix | Your decision | Outcome |
|---|---|---|---|---|---|---|---|---|
| F1 | T05 | LOW | coverage test mode no longer reaches the envelope rule | ACCEPTED | lost regression guard | set row and score coverage to 0 | — (auto) | fixed in `b6fcae5` |
| F2 | T05→T07 | LOW | default evidence path shared by dry and real runs | ACCEPTED | silent overwrite | derive from listings path | — (auto) | fixed in `b6fcae5` |
| F3 | T05→T07/T08 | LOW | evidence.jsonl discarded on the Actions runner | DEFERRED | belongs to the release round trip | T07 uploads it with the SQLite asset | — (auto) | deferred |
| F4 | T05→T06 | NOTE | gate 2 must validate PublishedListing | DEFERRED | T06 not written yet | in the B3 brief | — (auto) | deferred |
| F5 | T05 | NOTE | licence canary raises KeyError | ACCEPTED | clearer failure | pytest.fail message | — (auto) | fixed in `b6fcae5` |

## B3 (T06-T08) — round 1 · executor: Codex · reviewer: Claude subagent (dual_dev_auditor, session model) · 07 November 2026

Range: `b6fcae5..400f780` (base `b6fcae5`, end `400f780`) · raw report: subagent/B3_audit_r1_out.md
Review: ask_high · no BLOCKER or HIGH → auto · closed 07 November 2026, fixes in `a6f4dea` (Codex: F1, F2, F4, F5, F7, F8, F9 ACCEPTED; F6 PARTIALLY_ACCEPTED; F3 resolved by verification; F10 retained as documented)

**In short:** PASS_WITH_FINDINGS · findings B/H/M/L/N: 0/0/3/3/4 · needs you: no

- **F1 (MEDIUM, T07) 60 s timeout on asset transfers** → ACCEPTED: configurable transfer timeout (default 600 s), 60 s kept for view/create; test.
- **F2 (MEDIUM, T07) Unexpected errors logged by type name only** → ACCEPTED: traceback to the file handler only; issue text unchanged; test.
- **F3 (MEDIUM, T08) Action SHAs and uv version unverified** → RESOLVED BY VERIFICATION (Claude, 07 November 2026, live `gh api`): checkout v6 = d23441a4…, setup-uv v7 = 37802adc…, upload-artifact v6 = b7c566a7…, all match; uv release 0.11.19 exists. No code change; recorded in the handover.
- **F4 (LOW, T07) Upload-skipped-on-failure test is vacuous** → ACCEPTED: one gate-failure case with transfer on.
- **F5 (LOW, T07) Dry-run outputs not git-ignored** → ACCEPTED: ignore `site/src/data/*.dry.*` and `*.evidence.jsonl`; runbook line.
- **F6 (LOW, T07) First-run detection on exact stderr string** → PARTIALLY_ACCEPTED: wording confirmed live on gh 2.92.0 ("release not found"); add a tolerant match and record the version in the runbook; first-run `release pull` tried manually before enabling the schedule.
- **F7 (NOTE, T07) Stale stage label** → ACCEPTED: `stage = "baseline"`.
- **F8 (NOTE, T07) `pipeline gates` writes failure records** → ACCEPTED: skip `record_failure` for the read-only command.
- **F9 (NOTE, T08) No GH_REPO in job env** → ACCEPTED: add it.
- **F10 (NOTE, T07) run_log before promote** → ACCEPTED AS DOCUMENTED: plan line consciously superseded; no change.

| ID | Task | Severity | Finding | Proposed resolution | Reason | Planned fix | Your decision | Outcome |
|---|---|---|---|---|---|---|---|---|
| F1 | T07 | MEDIUM | fixed 60 s timeout on gh download and upload | ACCEPTED | asset growth would self-inflict an outage | `AI_HUB_RELEASE_TIMEOUT_SECONDS` default 600 for transfers; test | — (auto) | fixed in `a6f4dea` |
| F2 | T07 | MEDIUM | unexpected errors recorded by class name only | ACCEPTED | runbook points at a log that has nothing | traceback to file handler at DEBUG; test | — (auto) | fixed in `a6f4dea` |
| F3 | T08 | MEDIUM | action SHAs and uv version unverified | RESOLVED | verified live by Claude | none | — (auto) | verified, no change |
| F4 | T07 | LOW | upload-skipped acceptance untested | ACCEPTED | explicit acceptance line | gate-failure case with transfer=True | — (auto) | fixed in `a6f4dea` |
| F5 | T07 | LOW | dry-run outputs under site/ not ignored | ACCEPTED | full payloads could be committed | .gitignore lines; runbook | — (auto) | fixed in `a6f4dea` |
| F6 | T07 | LOW | exact stderr match for first run | PARTIALLY_ACCEPTED | wording confirmed on gh 2.92.0 | tolerant match; version noted in runbook | — (auto) | fixed in `a6f4dea` |
| F7 | T07 | NOTE | stale stage label during baseline read | ACCEPTED | cheap | `stage = "baseline"` | — (auto) | fixed in `a6f4dea` |
| F8 | T07 | NOTE | `gates` command records failures | ACCEPTED | avoids confusing local state | skip record_failure | — (auto) | fixed in `a6f4dea` |
| F9 | T08 | NOTE | no GH_REPO env | ACCEPTED | removes checkout dependency | add env | — (auto) | fixed in `a6f4dea` |
| F10 | T07 | NOTE | order deviates from plan, documented | ACCEPTED AS DOCUMENTED | sound | none | — (auto) | no change |


## T09 dry-run findings (live network) · found by: Claude (coordinator, executing T09) · scope: T03 (B1, Codex) · 07 November 2026

Run `2ebf7d36` (dry run, limit 50) failed at ingest within 7 s. Review: ask_high · no BLOCKER or HIGH → auto · executor Codex fixes.

**In short:** one MEDIUM live-API finding in T03; unit tests could not surface it.

- **F1 (MEDIUM, T03) GitHub GraphQL returns RESOURCE_LIMITS_EXCEEDED for 50-node pages** → ACCEPTED: default page size 25; on a RESOURCE_LIMITS_EXCEEDED error halve the page and retry (floor 5) before failing closed; tests with a fixture error of that type.

Evidence (Claude probes, 07 November 2026, token-authenticated, header 2026-03-10): queries `coding_agent` and `mcp` with the full field set: first=50 → 50 to 51 errors of type RESOURCE_LIMITS_EXCEEDED (paths under `mentionableUsers`, `latestRelease`, `id`), cost 2; first=25 → 0 errors, cost 1; first=10 → 0 errors. first=50 without `mentionableUsers` → 0 errors. `repositoryTopics(first: 20)` alone does not help. Query `claude_code` at first=50 → 0 errors (smaller repos). The pipeline raised `GraphQLError("GraphQL returned errors; partial data discarded")`, which is the intended fail-closed path; the page size is the defect.

| ID | Task | Severity | Finding | Proposed resolution | Reason | Planned fix | Your decision | Outcome |
|---|---|---|---|---|---|---|---|---|
| F1 | T03 | MEDIUM | 50-node GraphQL pages exceed GitHub's resource limit with `mentionableUsers` | ACCEPTED | every real run of the niche would fail at ingest | default page 25 (`AI_HUB_GITHUB_PAGE_SIZE`), adaptive halving on RESOURCE_LIMITS_EXCEEDED, tests | — (auto) | fixed in `898b859`; dry run attempt 2 passed |

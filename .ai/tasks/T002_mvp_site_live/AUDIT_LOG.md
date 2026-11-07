# Audit log — T002_mvp_site_live: MVP site and live schedule

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

Range: `d73a1d2..abc99df` (base `d73a1d2`, end `abc99df`) · raw report: subagent/B1_audit_r1_out.md
Review: ask_high · no BLOCKER or HIGH → auto (no stop for the user)

**In short:** PASS_WITH_FINDINGS · findings B/H/M/L/N: 0/1/3/3/0 (plus coordinator C1-C4 below) · needs you: no

- **F1 (MEDIUM, T02/T03) CI rebuild discards the gate record in status.json** → ACCEPTED: remove the "Build published site" step; keep the independent `pipeline gates` check before upload; align README, runbook and architecture doc; tests updated.
- **F2 (LOW, T01) Topic pages unbounded against the 200 KB gate** → ACCEPTED: 200 rows per topic page with next/previous links; test at about 1,500 rows.
- **F3 (LOW, T01) Backup clean-up can fail a published run on Windows; temp dirs not ignored** → ACCEPTED: `ignore_cleanup_errors=True` with a logged warning; `site/.*/` ignored.
- **F4 (LOW, T03) Architecture doc targets rewritten** → ACCEPTED: restore the target statements, add "Current (request 2):" notes.
- **F5 (NOTE, T03) README CI step list** → ACCEPTED: follows F1.
- **F6 (NOTE, T01) Packaging and rendering notes** → PARTIALLY_ACCEPTED: (c) display-name map for topics ("MCP server or skill", "RAG knowledge"); (b) allow-list docs.deps.dev, huggingface.co, hn.algolia.com, scorecard.dev on the policy page and in gate 5; (a) document the editable-install assumption.
- **F7 (NOTE, T02) Case-insensitive path check on Windows** → ACCEPTED: exact-name comparison.

| ID | Task | Severity | Finding | Proposed resolution | Reason | Planned fix | Your decision | Outcome |
|---|---|---|---|---|---|---|---|---|
| F1 | T02/T03 | MEDIUM | CI rebuilds the site after promotion; deployed status.json loses gate records | ACCEPTED | named deliverable misreported on the live site | drop the rebuild step; docs and tests aligned | — (auto) | pending |
| F2 | T01 | LOW | topic pages unbounded vs 200 KB gate | ACCEPTED | self-inflicted outage at scale | paginate at 200 rows; large-row test | — (auto) | pending |
| F3 | T01 | LOW | Windows clean-up error after swap; temp dirs not ignored | ACCEPTED | T04 runs on Windows with a preview server | ignore_cleanup_errors; .gitignore | — (auto) | pending |
| F4 | T03 | LOW | architecture doc targets replaced | ACCEPTED | document is the target for every request | restore targets with current notes | — (auto) | pending |
| F5 | T03 | NOTE | README CI steps inconsistent | ACCEPTED | follows F1 | align | — (auto) | pending |
| F6 | T01 | NOTE | packaging, stripped reference links, topic capitalisation | PARTIALLY_ACCEPTED | cosmetic and policy | display names; host allow-list; docstring note | — (auto) | pending |
| F7 | T02 | NOTE | case-insensitive path check on Windows | ACCEPTED | cheap | exact-name comparison | — (auto) | pending |
| C1 | T01 | MEDIUM | index lists eleven empty topics | ACCEPTED | MVP reads as empty | only topics with entries; Pending last | — (auto) | pending |
| C2 | T01 | LOW | "pending · pending" rows | ACCEPTED | clarity | "level not yet labelled" once | — (auto) | pending |
| C3 | T01 | LOW | duplicated page title | ACCEPTED | polish | index title = site name | — (auto) | pending |
| C4 | T01 | LOW | raw ISO timestamps | ACCEPTED | readability | DD Mon YYYY in templates | — (auto) | pending |


Coordinator observations from a local build (Claude, 07 November 2026, `pipeline site build --input site/src/data/listings.dry.json --output site/dist.dry`, 68 files, 321 KB, viewed in the browser). To be fixed by Codex in the B1 corrections round together with the audit findings; IDs C1 to C4 so they do not clash with the auditor's F numbers.

- **C1 (MEDIUM, T01) Index lists every vocabulary topic, eleven of them empty** → fix: render only topics that have entries at the selected level, in exported order; keep the "Pending" group last; an empty whole page shows one "no entries" line.
- **C2 (LOW, T01) Pending rows read "pending · pending"** → fix: when the label is pending show "level not yet labelled" once; when provisional show "<level> (provisional)".
- **C3 (LOW, T01) Page title duplicates the site name ("AI Hub · AI Hub")** → fix: index title is the site name alone; other pages "<page> · AI Hub".
- **C4 (LOW, T01) Timestamps shown as raw ISO strings with microseconds** → fix: render dates as `DD Mon YYYY` (and `HH:MM UTC` for generated_at) in the templates; keep ISO in `status.json`.

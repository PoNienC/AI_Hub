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

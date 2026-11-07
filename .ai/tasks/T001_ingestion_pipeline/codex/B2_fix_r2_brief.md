# Codex brief — execute T04, T05

Fresh task. You are the executor for T04, T05 in a dual-agent workflow
(see `AGENTS.md`). Claude Code will review your work afterwards.

## Rules

- Implement ONLY T04, T05, in this order, as specified. No unrelated
  changes and no refactors outside their scope.
- Finish each task and run its tests before starting the next one. If a
  task cannot be completed, stop there and report why — do not start the
  tasks after it.
- Do not stage, commit, branch, push or rewrite Git history.
- Do not edit files under `.ai/`. Put your handover in your final message.
- Run the relevant tests and report results honestly. For Python, prefer
  the project's own interpreter (for example `.venv\Scripts\python -m pytest`).
  If the sandbox blocks a command, report the exact command and error.
  Also run the lint and type checks `.ai/PROJECT.md` names — only those,
  no other check or formatter.
- Follow the project's conventions. British English in comments,
  documentation and messages.

## Tasks

Read `.ai/tasks/T001_ingestion_pipeline/PLAN_APPROVED.md`, sections T04, T05: objective,
dependencies, likely files, acceptance criteria and tests. Also read
`AGENTS.md` and `.ai/PROJECT.md`.

Corrections round 2 (small). Claude's round-2 findings for T04, T05 are in `.ai/tasks/T001_ingestion_pipeline/AUDIT_LOG.md` under B2 round 2 (full report: `.ai/tasks/T001_ingestion_pipeline/subagent/B2_audit_r2_out.md`). Evaluate each one independently, mark it ACCEPTED, PARTIALLY_ACCEPTED, REJECTED or DEFERRED with a reason, fix only what you accept, then re-run the tests and the project's checks. In scope: F1 (test mode `coverage` sets both `row["coverage"]` and `row["score"]["coverage"]` to 0 so the envelope rule is exercised), F2 (default `evidence_path` derived from the listings `path`, for example a sibling `<stem>.evidence.jsonl`, so a dry run never overwrites `state/evidence.jsonl`; update docs/scoring.md), F5 (`pytest.fail` with a clear message for an unclassified CSV licence). F3 and F4 are deferred to T06/T07: no change. Environment notes: the worktree-local `.venv` exists; set `PYTEST_DEBUG_TEMPROOT` to `_build/pytest` before pytest. The project checks are `uv run pytest --cov=pipeline --cov-fail-under=80` and `uv run ruff check .`.

## Output — your final message, Markdown

# Codex handover — T04, T05
One section per task:
## T<nn> — <title>
### Summary
### Files changed
### Tests and checks run
One line per command — the task's tests, then the lint and type checks
`.ai/PROJECT.md` names: command and result (pass / fail counts), or the
exact error if the sandbox blocked it.
### Finding resolutions
Corrections round only. For each finding: F<n>, ACCEPTED /
PARTIALLY_ACCEPTED / REJECTED / DEFERRED, one-line reason, what you changed.
### Known gaps and risks

No preamble.

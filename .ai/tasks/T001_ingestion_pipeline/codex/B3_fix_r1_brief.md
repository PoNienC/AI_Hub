# Codex brief — execute T06, T07, T08

Fresh task. You are the executor for T06, T07, T08 in a dual-agent workflow
(see `AGENTS.md`). Claude Code will review your work afterwards.

## Rules

- Implement ONLY T06, T07, T08, in this order, as specified. No unrelated
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

Read `.ai/tasks/T001_ingestion_pipeline/PLAN_APPROVED.md`, sections T06, T07, T08: objective,
dependencies, likely files, acceptance criteria and tests. Also read
`AGENTS.md` and `.ai/PROJECT.md`.

Corrections round 1. Claude's findings for T06, T07, T08 are in `.ai/tasks/T001_ingestion_pipeline/AUDIT_LOG.md` under B3 round 1 (full report: `.ai/tasks/T001_ingestion_pipeline/subagent/B3_audit_r1_out.md`). Evaluate each one independently, mark it ACCEPTED, PARTIALLY_ACCEPTED, REJECTED or DEFERRED with a reason, fix only what you accept, then re-run the tests and the project's checks. Facts verified live by Claude on 07 November 2026 that you should rely on: the three action SHA pins match tags v6, v7 and v6; uv 0.11.19 exists (F3: no change needed); `gh` 2.92.0 prints exactly `release not found` for a missing release (F6: keep that wording, add a tolerant match, note the version in the runbook). In scope: F1, F2, F4, F5, F6, F7, F8, F9. F3 and F10: no change. Environment notes: the worktree-local `.venv` exists; set `PYTEST_DEBUG_TEMPROOT` to `_build/pytest` before pytest. The project checks are `uv run pytest --cov=pipeline --cov-fail-under=80` and `uv run ruff check .`.

## Output — your final message, Markdown

# Codex handover — T06, T07, T08
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

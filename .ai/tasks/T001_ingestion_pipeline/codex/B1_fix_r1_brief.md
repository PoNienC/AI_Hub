# Codex brief — execute T01, T02, T03

Fresh task. You are the executor for T01, T02, T03 in a dual-agent workflow
(see `AGENTS.md`). Claude Code will review your work afterwards.

## Rules

- Implement ONLY T01, T02, T03, in this order, as specified. No unrelated
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

Read `.ai/tasks/T001_ingestion_pipeline/PLAN_APPROVED.md`, sections T01, T02, T03: objective,
dependencies, likely files, acceptance criteria and tests. Also read
`AGENTS.md` and `.ai/PROJECT.md`.

Corrections round 1. Claude's findings for T01, T02, T03 are in `.ai/tasks/T001_ingestion_pipeline/AUDIT_LOG.md` under B1 round 1 (full report: `.ai/tasks/T001_ingestion_pipeline/subagent/B1_audit_r1_out.md`). Evaluate each one independently, mark it ACCEPTED, PARTIALLY_ACCEPTED, REJECTED or DEFERRED with a reason, fix only what you accept, then re-run the tests and the project's checks. F5 and F6 are already deferred to T07 and T08: do not implement them now. For F2, note that Claude verified live on 07 November 2026 that GitHub REST and GraphQL accept the 2026-03-10 header, so a docstring note is enough. Environment notes: the worktree-local `.venv` exists; set `PYTEST_DEBUG_TEMPROOT` to `_build/pytest` before pytest, as before. The project checks are `uv run pytest --cov=pipeline --cov-fail-under=80` and `uv run ruff check .`; after pinning ruff rules (F3), ruff must pass on the whole repository including `scripts/`.

## Output — your final message, Markdown

# Codex handover — T01, T02, T03
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

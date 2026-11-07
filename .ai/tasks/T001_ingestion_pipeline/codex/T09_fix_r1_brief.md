# Codex brief — execute T03

Fresh task. You are the executor for T03 in a dual-agent workflow
(see `AGENTS.md`). Claude Code will review your work afterwards.

## Rules

- Implement ONLY T03, in this order, as specified. No unrelated
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

Read `.ai/tasks/T001_ingestion_pipeline/PLAN_APPROVED.md`, sections T03: objective,
dependencies, likely files, acceptance criteria and tests. Also read
`AGENTS.md` and `.ai/PROJECT.md`.

Corrections from the T09 live dry run. Claude's finding for T03 is in `.ai/tasks/T001_ingestion_pipeline/AUDIT_LOG.md` under "T09 dry-run findings" with the probe evidence. Evaluate it, mark ACCEPTED, PARTIALLY_ACCEPTED, REJECTED or DEFERRED with a reason, fix what you accept, then re-run the tests and the project's checks. Scope: in `pipeline/sources/github.py` (and `pipeline/config.py` for the setting) make the GraphQL page size a setting `AI_HUB_GITHUB_PAGE_SIZE` with default 25 (the per-query cap and `--limit` still bound the total); when a response carries only errors of type `RESOURCE_LIMITS_EXCEEDED`, discard that page, halve the page size (floor 5) and retry the same cursor, logging the reduction; any other GraphQL error keeps the current fail-closed behaviour; charge the budget for every attempt as today. Add fixtures and tests: a RESOURCE_LIMITS_EXCEEDED page followed by a clean smaller page succeeds; a mixed-error page still fails; the floor is respected. Update the module docstring and `docs/runbook.md` (entry: GitHub resource limit). Keep public signatures used by `pipeline/cli.py` unchanged. Environment notes: the worktree-local `.venv` exists; set `PYTEST_DEBUG_TEMPROOT` to `_build/pytest` before pytest. The project checks are `uv run pytest --cov=pipeline --cov-fail-under=80` and `uv run ruff check .`.

## Output — your final message, Markdown

# Codex handover — T03
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

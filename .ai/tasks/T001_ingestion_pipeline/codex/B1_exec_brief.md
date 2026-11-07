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

Environment notes: use `uv` (installed) to create a worktree-local `.venv` with `uv sync` after writing `pyproject.toml`; if dependency download is blocked by the sandbox, say so exactly and continue writing code and tests so Claude can install and run them. Python 3.13 is `python` on PATH. Also install dev dependencies pytest, pytest-cov, ruff, respx or a plain httpx MockTransport for fixtures. The project checks are `uv run pytest --cov=pipeline --cov-fail-under=80` and `uv run ruff check .`.

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

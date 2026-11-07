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

Environment notes: the worktree-local `.venv` already exists (`uv sync --frozen` keeps it current); set `PYTEST_DEBUG_TEMPROOT` to `_build/pytest` before running pytest, as in B1. Build on the B1 interfaces in `pipeline/models.py`, `pipeline/store.py`, `pipeline/http.py`, `pipeline/budgets.py` and `pipeline/sources/github.py` without changing their public signatures; if a signature must change, say so in the handover. The project checks are `uv run pytest --cov=pipeline --cov-fail-under=80` and `uv run ruff check .`. The provisional labels CSV is `data/labelled_repos_for_review.csv` (columns include full_name, topic, level, confidence).

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

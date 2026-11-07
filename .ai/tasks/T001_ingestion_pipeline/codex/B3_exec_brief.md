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

Carried obligations from the B1 audit (see `.ai/tasks/T001_ingestion_pipeline/AUDIT_LOG.md`, B1 round 1, F5 and F6, and `.ai/DECISIONS.md`): (1) in T07, failed runs are recorded in an append-only failure log outside the promoted database (`state/failures.jsonl`, one JSON line per failed run with run id, started, finished, failing gate or budget, counts, log path); T06's failure text is built from the same record; (2) in T07, `pipeline run` pre-flights a stale `state/gateway.work.sqlite` and exits with a clear message naming the file and the exact removal command instead of a traceback; in T08 the runbook gains a 'stale working copy' entry. Environment notes: the worktree-local `.venv` exists; set `PYTEST_DEBUG_TEMPROOT` to `_build/pytest` before pytest. Keep B1 and B2 public signatures unchanged unless the handover says otherwise. The project checks are `uv run pytest --cov=pipeline --cov-fail-under=80` and `uv run ruff check .`. For the workflow YAML test, parse with PyYAML (add it as a dev dependency) if not already present.

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

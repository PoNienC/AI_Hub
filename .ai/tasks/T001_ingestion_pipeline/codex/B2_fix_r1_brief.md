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

Corrections round 1. Claude's findings for T04, T05 are in `.ai/tasks/T001_ingestion_pipeline/AUDIT_LOG.md` under B2 round 1 (full report: `.ai/tasks/T001_ingestion_pipeline/subagent/B2_audit_r1_out.md`). The user has approved these findings for fixing. Fix each one; if one cannot be fixed, stop and explain why — do not reject it. Approved scope:
- F1 (HIGH): normalise SPDX ids so GitHub's `GPL-2.0`, `GPL-3.0`, `LGPL-2.1`, `LGPL-3.0`, `AGPL-3.0` (and `-only` / `-or-later` variants) classify as copyleft; add a parametrised test over the distinct `license` values in `data/candidate_repos.csv`; correct `docs/scoring.md`.
- F2 (partial): add `coverage` to each listing row in `listings.json` (model and export); do NOT change weights or the score version; do NOT add deps.dev package resolution.
- F3: compact per-source evidence summary in `listings.json`; write full evidence to `state/evidence.jsonl` (git-ignored, not shipped); add a per-row serialised size-bound test.
- F4: a Hacker News hit with `url: null` is skipped, not a failure; fixture added.
- F5: `fetch_json` takes `absent_statuses` (default {404}); the Hugging Face and Hacker News search adapters pass an empty set so 404 becomes `failed`.
- F6: deps.dev adapter verifies the returned project links the requested repo, as Scorecard does.
- F7: document in `docs/scoring.md` that provisional labels join by full_name and that gold labels will be keyed by github_id.
- F9: close the owned `httpx.Client` in `tests/test_enrichment.py` with `with`; leave E501 unselected.
- F8 is deferred to T09: no change.
Environment notes: the worktree-local `.venv` exists; set `PYTEST_DEBUG_TEMPROOT` to `_build/pytest` before pytest. Keep B1 public signatures unchanged. The project checks are `uv run pytest --cov=pipeline --cov-fail-under=80` and `uv run ruff check .`.

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

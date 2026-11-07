# Codex handover — T06, T07, T08

## T06 — Gates 2 and 3 and the abort rule

### Summary

Revalidated T06 before starting T07. No corrections required.

### Files changed

None.

### Tests and checks run

All pytest runs used `PYTEST_DEBUG_TEMPROOT=_build/pytest`. uv used frozen dependencies and worktree-local environment/cache paths. No type-check command is specified.

- `.venv\Scripts\python.exe -m pytest tests/test_gates.py` — 41 passed, 0 failed.
- `uv run pytest --cov=pipeline --cov-fail-under=80` — 412 passed, 0 failed; 98.39% coverage.
- `uv run ruff check .` — passed.

### Finding resolutions

No B3 round-1 findings assigned to T06.

### Known gaps and risks

None identified.

## T07 — Release round trip and CLI

### Summary

Implemented the accepted release, diagnostic and CLI corrections, with regression tests and runbook updates.

### Files changed

- [pipeline/release.py](C:/Users/po.nienchen/repos/AI_Hub/pipeline/release.py), [pipeline/cli.py](C:/Users/po.nienchen/repos/AI_Hub/pipeline/cli.py)
- [tests/test_release.py](C:/Users/po.nienchen/repos/AI_Hub/tests/test_release.py), [tests/test_cli.py](C:/Users/po.nienchen/repos/AI_Hub/tests/test_cli.py)
- [.gitignore](C:/Users/po.nienchen/repos/AI_Hub/.gitignore), [docs/runbook.md](C:/Users/po.nienchen/repos/AI_Hub/docs/runbook.md)

### Tests and checks run

- `.venv\Scripts\python.exe -m pytest tests/test_release.py tests/test_cli.py` — 65 passed, 0 failed.
- `git check-ignore site/src/data/listings.dry.json site/src/data/listings.dry.evidence.jsonl site/src/data/listings.evidence.jsonl` — all three paths ignored.
- `uv run pytest --cov=pipeline --cov-fail-under=80` — 434 passed, 0 failed; 98.42% coverage.
- `uv run ruff check .` — passed.

### Finding resolutions

- **F1 — ACCEPTED:** Transfers need longer timeouts; added `AI_HUB_RELEASE_TIMEOUT_SECONDS`, default 600 seconds, retaining 60 seconds for metadata/create calls.
- **F2 — ACCEPTED:** Type-only diagnostics hinder investigation; added DEBUG tracebacks directly to diagnostic files, preserving sanitised console and issue output.
- **F4 — ACCEPTED:** Existing upload protection test was vacuous; added a real count-gate failure with transfers enabled, asserting no upload and unchanged production files.
- **F5 — ACCEPTED:** Dry-run payloads should remain untracked; added both ignore patterns and runbook guidance.
- **F6 — PARTIALLY_ACCEPTED:** Confirmed wording remains valid; retained it with tolerant matching, fail-closed tests, gh 2.92.0 documentation and manual first-run instructions.
- **F7 — ACCEPTED:** Baseline errors had the wrong stage; added `baseline` and regression coverage.
- **F8 — ACCEPTED:** Gate inspection should be read-only; failures now leave logs, failure history and issue files untouched.
- **F10 — ACCEPTED:** Existing documented ordering is justified because promotion closes the store; retained it unchanged.

### Known gaps and risks

Release transfers were tested offline with fake `gh`. Live first-run validation remains an operational step documented in the runbook.

## T08 — Workflow, runbook and docs

### Summary

Added explicit repository resolution to the workflow. All edits remain unstaged; Git history, `.ai/` and unrelated files were untouched.

### Files changed

- [.github/workflows/refresh.yml](C:/Users/po.nienchen/repos/AI_Hub/.github/workflows/refresh.yml)
- [tests/test_workflow.py](C:/Users/po.nienchen/repos/AI_Hub/tests/test_workflow.py)

### Tests and checks run

- `.venv\Scripts\python.exe -m pytest tests/test_workflow.py` — 5 passed, 0 failed.
- `uv run pytest --cov=pipeline --cov-fail-under=80` — 434 passed, 0 failed; 98.42% coverage.
- `uv run ruff check .` — passed.

### Finding resolutions

- **F3 — ACCEPTED, resolved by verification:** Relied on Claude’s 7 November verification of checkout v6, setup-uv v7, upload-artifact v6 and uv 0.11.19; no changes.
- **F9 — ACCEPTED:** Explicit repository selection removes checkout-remote dependence; added `GH_REPO: ${{ github.repository }}` and an assertion.

### Known gaps and risks

Live Actions execution was not performed. Actionlint was not run under the instruction limiting checks to the specified project commands.
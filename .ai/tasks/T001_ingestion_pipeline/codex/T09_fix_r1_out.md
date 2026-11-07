# Codex handover — T03

## T03 — GitHub GraphQL source and budget accounting

### Summary

Added `AI_HUB_GITHUB_PAGE_SIZE`, default 25, validated from 5–100. Resource-limit-only responses now discard partial data, halve the requested page size to a floor of 5, log the reduction and retry the same cursor.

Other GraphQL errors remain fail-closed. Budget accounting, total caps and public signatures are preserved.

### Files changed

- [pipeline/config.py](/C:/Users/po.nienchen/repos/AI_Hub/pipeline/config.py)
- [pipeline/sources/github.py](/C:/Users/po.nienchen/repos/AI_Hub/pipeline/sources/github.py)
- [tests/test_config.py](/C:/Users/po.nienchen/repos/AI_Hub/tests/test_config.py)
- [tests/test_github.py](/C:/Users/po.nienchen/repos/AI_Hub/tests/test_github.py)
- [tests/fixtures/github_resource_limit.json](/C:/Users/po.nienchen/repos/AI_Hub/tests/fixtures/github_resource_limit.json)
- [tests/fixtures/github_mixed_errors.json](/C:/Users/po.nienchen/repos/AI_Hub/tests/fixtures/github_mixed_errors.json)
- [docs/runbook.md](/C:/Users/po.nienchen/repos/AI_Hub/docs/runbook.md)

### Tests and checks run

Used the worktree `.venv`, `PYTEST_DEBUG_TEMPROOT=_build/pytest` and frozen uv settings.

- `.venv\Scripts\python -m pytest tests/test_github.py tests/test_config.py tests/test_budgets.py` — **PASS: 88 passed, 0 failed**.
- `uv run pytest --cov=pipeline --cov-fail-under=80` — **PASS: 454 passed, 0 failed; 98.44% coverage**.
- `uv run ruff check .` — **PASS: no issues**.

No separate type-check command is specified.

### Finding resolutions

- **F1 — ACCEPTED:** live probes demonstrated oversized-page failures; implemented configurable sizing, bounded retries, regression fixtures/tests and documentation.

### Known gaps and risks

The live T09 dry run has not been repeated; Claude’s review remains pending. No Git mutations or `.ai/` edits were made.
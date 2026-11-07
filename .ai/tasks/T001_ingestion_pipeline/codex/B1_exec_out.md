# Codex handover — T01, T02, T03

## T01 — Package skeleton, models and config

### Summary

Implemented the package, validated models, environment settings, exact query dictionary, niche selection and versioned weights. Created the local `.venv` and dependency lock.

All uv commands used worktree-local paths: `.venv`, `_build/uv-cache` and `_build/uv-python`.

### Files changed

- `pyproject.toml`, `uv.lock`, `.python-version`, `.gitignore`
- `pipeline/__init__.py`, `pipeline/config.py`, `pipeline/models.py`
- `tests/conftest.py`, `tests/test_config.py`, `tests/test_models.py`

### Tests and checks run

- `uv sync --python python` — PASS; installed runtime and development dependencies.
- `uv sync --frozen` — PASS.
- `uv run pytest tests/test_config.py tests/test_models.py --cov=pipeline --cov-fail-under=80` — PASS: 33 passed, 100% coverage.
- `uv run pytest --cov=pipeline --cov-fail-under=80` — PASS at T01 completion: 33 passed, 100% coverage.
- `uv run ruff check .` — FAIL: two existing findings; no remaining findings in new files.

No type-check command is specified in `.ai/PROJECT.md`.

### Known gaps and risks

The existing Ruff findings remain unchanged to respect scope: `PLW1510` at [sample_and_fetch.py:31](C:/Users/po.nienchen/repos/AI_Hub/scripts/sample_and_fetch.py:31) and `PERF102` at line 44.

Per-source HTTP limits default to 1,000 calls and are configurable. CLI wiring belongs to T07. `.ai/CODEX_APP_PROMPT.md` was absent.

## T02 — State store with safe promotion

### Summary

Implemented schema version 1, working-copy isolation, rename history, snapshots, scores, run logs and elapsed-hour velocity. Promotion requires passing gates and SQLite integrity checks. Tests verify byte-identical canonical state after failures.

### Files changed

- `pipeline/store.py`
- `pipeline/migrations.py`
- `tests/test_store.py`

### Tests and checks run

- `uv run pytest tests/test_store.py` — initially 24 setup errors from the sandbox restriction below; rerun PASS: 24 passed.
- `uv run pytest --cov=pipeline --cov-fail-under=80` — initially 33 passed, 24 setup errors; rerun PASS: 57 passed, 99.22% coverage.
- `uv run ruff check .` — FAIL: the same two existing script findings; none in new files.

Exact sandbox error:

```text
PermissionError: [WinError 5] Access is denied: 'C:\Users\po.nienchen\AppData\Local\Temp\pytest-of-ponien.chen'
```

Successful reruns set `PYTEST_DEBUG_TEMPROOT` to the worktree’s `_build/pytest`; T03 used the same setting.

### Known gaps and risks

An interrupted process can leave `gateway.work.sqlite`; the store refuses to overwrite it. Failed-run database logs are discarded with rollback, so later orchestration must retain failure diagnostics separately.

## T03 — GitHub GraphQL source and budget accounting

### Summary

Implemented paginated search, ID-based deduplication, field mapping, typed partial-error failures, retry/timeout handling and per-attempt budgets. Contributor counts explicitly identify the proxy; the REST fallback is implemented and disabled by default.

Unknown GraphQL costs cause an abort. Tests verify token exclusion from logs and error messages.

### Files changed

- `pipeline/http.py`, `pipeline/budgets.py`
- `pipeline/sources/__init__.py`, `pipeline/sources/github.py`
- `tests/test_github.py`, `tests/test_budgets.py`, `tests/test_http.py`
- `tests/fixtures/github_page_1.json`
- `tests/fixtures/github_page_2.json`
- `tests/fixtures/github_partial_error.json`
- `tests/fixtures/github_empty.json`
- `tests/fixtures/github_contributors.json`

### Tests and checks run

- `uv run pytest tests/test_github.py tests/test_budgets.py tests/test_http.py` — PASS: 62 passed.
- `uv run pytest --cov=pipeline --cov-fail-under=80` — PASS: **119 passed, 99.23% coverage**.
- `uv run ruff check .` — FAIL: the same two existing script findings; none in new files.

### Known gaps and risks

Validation used synthetic offline fixtures; no live ingestion run was performed.

Actual GraphQL cost is reported after execution. A response crossing the budget is therefore charged and immediately aborts; subsequent calls are blocked. [GitHub rate-limit documentation](https://docs.github.com/en/graphql/overview/rate-limits-and-query-limits-for-the-graphql-api).

T01–T03 were completed and tested sequentially. No staging, commits, branching, pushes, history changes or `.ai/` edits were made.
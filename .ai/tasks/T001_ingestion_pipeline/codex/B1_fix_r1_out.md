# Codex handover — T01, T02, T03

## T01 — Package skeleton, models and config

### Summary

Pinned Ruff rules, enforced matching listing/score versions, and corrected configuration validation and test isolation.

### Files changed

- [pyproject.toml](C:/Users/po.nienchen/repos/AI_Hub/pyproject.toml)
- [pipeline/config.py](C:/Users/po.nienchen/repos/AI_Hub/pipeline/config.py)
- [pipeline/models.py](C:/Users/po.nienchen/repos/AI_Hub/pipeline/models.py)
- [tests/test_config.py](C:/Users/po.nienchen/repos/AI_Hub/tests/test_config.py)
- [tests/test_models.py](C:/Users/po.nienchen/repos/AI_Hub/tests/test_models.py)

### Tests and checks run

All pytest runs used `PYTEST_DEBUG_TEMPROOT=_build/pytest`. uv used the worktree’s `.venv`, cache/Python paths under `_build/`, and frozen dependencies. No type-check command is specified.

- `.\.venv\Scripts\python.exe -m pytest tests/test_config.py tests/test_models.py` — PASS: 38 passed, 0 failed.
- `uv run pytest --cov=pipeline --cov-fail-under=80` — PASS after T01: 124 passed, 0 failed; 99.25% coverage.
- `uv run ruff check .` — PASS across the repository, including `scripts/`.

### Finding resolutions

- **F3 — ACCEPTED:** Pinned `E4`, `E7`, `E9`, `F` and line length 100 to make lint configuration explicit.
- **F4 — ACCEPTED:** Added an after-validator and mismatch regression test.
- **F7 — PARTIALLY_ACCEPTED:** Fixed (a) malformed JSON raising inconsistent errors and (c) environment-dependent tests; retained (b) the script import required by the parity test.

### Known gaps and risks

The required script import still configures root logging. `uv.lock` is unchanged.

## T02 — State store with safe promotion

### Summary

Reviewed both findings and verified existing behaviour. No implementation changes were required.

### Files changed

None.

### Tests and checks run

- `.\.venv\Scripts\python.exe -m pytest tests/test_store.py` — PASS: 24 passed, 0 failed.
- `uv run pytest --cov=pipeline --cov-fail-under=80` — PASS in shared final run: 132 passed, 0 failed; 99.26% coverage.
- `uv run ruff check .` — PASS in shared final run.

### Finding resolutions

- **F5 — DEFERRED:** Durable failure logging belongs to T07, as instructed; no changes.
- **F6 — DEFERRED:** Stale-copy diagnostics and recovery documentation belong to T07/T08, as instructed; no changes.

### Known gaps and risks

Rollback still discards failed-run database logs. Stale working copies still require manual recovery until the deferred work is completed.

## T03 — GitHub GraphQL source and budget accounting

### Summary

Repaired retry accounting for answered HTTP errors without `rateLimit`, preserving the abort when transport failures leave unknown costs. Documented the verified API header and fallback.

No staging, commits, branching, pushing, history changes or `.ai/` edits were performed.

### Files changed

- [pipeline/sources/github.py](C:/Users/po.nienchen/repos/AI_Hub/pipeline/sources/github.py)
- [pipeline/budgets.py](C:/Users/po.nienchen/repos/AI_Hub/pipeline/budgets.py)
- [tests/test_github.py](C:/Users/po.nienchen/repos/AI_Hub/tests/test_github.py)

### Tests and checks run

- `.\.venv\Scripts\python.exe -m pytest tests/test_github.py tests/test_budgets.py tests/test_http.py` — PASS: 70 passed, 0 failed.
- `uv run pytest --cov=pipeline --cov-fail-under=80` — PASS: 132 passed, 0 failed; 99.26% coverage.
- `uv run ruff check .` — PASS across the whole repository.

### Finding resolutions

- **F1 — ACCEPTED:** Settle answered errors using a logged four-point estimate; added recovery, budget-boundary, token-redaction and mixed transport/HTTP failure coverage.
- **F2 — PARTIALLY_ACCEPTED:** Retained `2026-03-10`; documented the supplied 07 November 2026 verification and `2022-11-28` fallback.

### Known gaps and risks

The four-point charge is an estimate tied to the current query; revisit it if the query or [GitHub’s cost formula](https://docs.github.com/en/graphql/overview/rate-limits-and-query-limits-for-the-graphql-api) changes. Tests were offline; live API verification was not repeated.
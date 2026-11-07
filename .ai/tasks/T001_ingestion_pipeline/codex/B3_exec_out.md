# Codex handover — T06, T07, T08

## T06 — Gates 2 and 3 and the abort rule

### Summary

Implemented schema and data-quality gates, rollback, and a shared `RunFailure` record for failure logs and issue text. Gate 2 validates `pipeline.export.Listings`, including published coverage.

### Files changed

- [pipeline/gates.py](C:/Users/po.nienchen/repos/AI_Hub/pipeline/gates.py)
- [pipeline/failure.py](C:/Users/po.nienchen/repos/AI_Hub/pipeline/failure.py)
- [tests/test_gates.py](C:/Users/po.nienchen/repos/AI_Hub/tests/test_gates.py)

### Tests and checks run

All pytest commands used `PYTEST_DEBUG_TEMPROOT=_build/pytest`. uv used the worktree’s `.venv` and `_build` directories.

- `.\.venv\Scripts\python -m pytest tests/test_gates.py -q` — **41 passed**.
- `uv run pytest --cov=pipeline --cov-fail-under=80` — **364 passed; 98.47% coverage**.
- `uv run ruff check .` — **passed**.

### Known gaps and risks

Labels remain optional. Only `untested` is supported until dated sandbox results are introduced.

## T07 — Release round trip and CLI

### Summary

Implemented CLI orchestration, both release assets, upload-size verification, append-only failure records, stale-copy preflight and isolated dry runs. Added `--no-release` for explicitly managed workflow transfers.

B1/B2 public signatures remain unchanged.

### Files changed

- [pipeline/cli.py](C:/Users/po.nienchen/repos/AI_Hub/pipeline/cli.py)
- [pipeline/release.py](C:/Users/po.nienchen/repos/AI_Hub/pipeline/release.py)
- [tests/test_cli.py](C:/Users/po.nienchen/repos/AI_Hub/tests/test_cli.py)
- [tests/test_release.py](C:/Users/po.nienchen/repos/AI_Hub/tests/test_release.py)
- [tests/fixtures/fake_gh.py](C:/Users/po.nienchen/repos/AI_Hub/tests/fixtures/fake_gh.py)
- [pyproject.toml](C:/Users/po.nienchen/repos/AI_Hub/pyproject.toml)

### Tests and checks run

- `.\.venv\Scripts\python -m pytest tests/test_release.py tests/test_cli.py -q` — **43 passed**, including rerun after fixing two test connection warnings.
- `uv run pytest --cov=pipeline --cov-fail-under=80` — **407 passed; 98.39% coverage**.
- `uv run ruff check .` — **passed**.
- `uv sync --frozen` — **passed**.
- `uv run pipeline --help` — **passed**.

### Known gaps and risks

The successful SQLite run log is finalised immediately before promotion because promotion closes the B1 store. Subsequent upload failures are recorded separately.

Local bundle replacement handles ordinary I/O failures but is not atomic across process termination. Remote replacement is also non-atomic: [`gh --clobber` deletes existing assets before uploading replacements](https://cli.github.com/manual/gh_release_upload). Recovery is documented.

## T08 — Workflow, runbook and docs

### Summary

Added the scheduled/manual workflow, pinned actions, failure reporting, retained diagnostic artefacts, weekly dependency updates, operational documentation and PyYAML workflow tests.

### Files changed

- [.github/workflows/refresh.yml](C:/Users/po.nienchen/repos/AI_Hub/.github/workflows/refresh.yml)
- [.github/dependabot.yml](C:/Users/po.nienchen/repos/AI_Hub/.github/dependabot.yml)
- [docs/runbook.md](C:/Users/po.nienchen/repos/AI_Hub/docs/runbook.md)
- [docs/scoring.md](C:/Users/po.nienchen/repos/AI_Hub/docs/scoring.md)
- [README.md](C:/Users/po.nienchen/repos/AI_Hub/README.md)
- [tests/test_workflow.py](C:/Users/po.nienchen/repos/AI_Hub/tests/test_workflow.py)
- [pyproject.toml](C:/Users/po.nienchen/repos/AI_Hub/pyproject.toml)
- [uv.lock](C:/Users/po.nienchen/repos/AI_Hub/uv.lock)

### Tests and checks run

- `.\.venv\Scripts\python -m pytest tests/test_workflow.py -q` — **5 passed**.
- `uv run pytest --cov=pipeline --cov-fail-under=80` — **412 passed; 98.39% coverage; no warnings**.
- `uv run ruff check .` — **passed**.
- `uv sync --frozen` — **passed**, including PyYAML 6.0.3.
- `actionlint .github/workflows/refresh.yml` — **not run: actionlint is not installed**.

No separate type-check command is configured.

### Known gaps and risks

Live Actions execution and real API/release validation remain untested; T09 was not started. Failure history on ephemeral runners is retained through per-run artefacts.

No staging, commits, branching, pushes or `.ai/` edits were performed. Existing unrelated changes were preserved.
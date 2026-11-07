# Codex handover — T04, T05

## T04 — Enrichment adapters

### Summary

Verified the existing implementation before starting T05. No round-2 corrections required.

### Files changed

None.

### Tests and checks run

- `.venv\Scripts\python -m pytest tests/test_enrichment.py` — PASS: 83 passed, 0 failed.
- `uv run ruff check .` — PASS on the final tree.

`PYTEST_DEBUG_TEMPROOT` was set to `_build/pytest`. No type check is specified.

### Finding resolutions

No round-2 findings require T04 changes.

### Known gaps and risks

Live API verification remains deferred to T09.

## T05 — Scoring and export

### Summary

Implemented F1, F2 and F5. Default evidence filenames now follow the listings path, with regression coverage confirming dry exports preserve production files.

### Files changed

- [pipeline/export.py](C:/Users/po.nienchen/repos/AI_Hub/pipeline/export.py)
- [tests/test_export.py](C:/Users/po.nienchen/repos/AI_Hub/tests/test_export.py)
- [tests/test_scoring.py](C:/Users/po.nienchen/repos/AI_Hub/tests/test_scoring.py)
- [docs/scoring.md](C:/Users/po.nienchen/repos/AI_Hub/docs/scoring.md)

### Tests and checks run

- `.venv\Scripts\python -m pytest tests/test_scoring.py tests/test_export.py` — PASS: 108 passed, 0 failed.
- `uv run pytest --cov=pipeline --cov-fail-under=80` — PASS: 323 passed, 0 failed; coverage **98.36%**.
- `uv run ruff check .` — PASS.

Pytest used `_build/pytest`. uv used worktree-local paths with synchronisation disabled. No type check is specified.

### Finding resolutions

- **F1 — ACCEPTED:** Set both coverage fields to zero and assert the envelope’s evaluated-score error.
- **F2 — ACCEPTED:** Derive omitted `evidence_path` from the listings path; document destinations and test dry-run isolation.
- **F3 — DEFERRED:** Evidence upload belongs to T07; no change.
- **F4 — DEFERRED:** Export-model validation belongs to T06; no change.
- **F5 — ACCEPTED:** Unknown CSV licences now trigger `pytest.fail` with the unclassified identifier.

### Known gaps and risks

Explicit `evidence_path` overrides still require separate production and dry-run destinations. F3 and F4 remain outstanding.

No `.ai/` files were edited, and no staging, commits, branches or history changes were made.
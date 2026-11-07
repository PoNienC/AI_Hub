# Codex handover — T04, T05

## T04 — Enrichment adapters

### Summary

Implemented four adapters with timestamped evidence, conservative status mapping, bounded searches and HTTP budget accounting. Budget exhaustion propagates. B1 public signatures remain unchanged.

### Files changed

- `pipeline/sources/_enrichment.py`
- `pipeline/sources/deps_dev.py`
- `pipeline/sources/scorecard.py`
- `pipeline/sources/hugging_face.py`
- `pipeline/sources/hacker_news.py`
- `tests/fixtures/enrichment_responses.json`
- `tests/test_enrichment.py`

### Tests and checks run

All pytest commands used `PYTEST_DEBUG_TEMPROOT=_build/pytest`.

- `.venv\Scripts\python -m pytest tests/test_enrichment.py -q` — PASS: 70 passed.
- `uv run pytest --cov=pipeline --cov-fail-under=80` — PASS: 202 passed; 98.28% coverage.
- `uv run ruff check .` — PASS.
- Type checks — none configured.

### Known gaps and risks

- [deps.dev project responses](https://docs.deps.dev/api/v3/#getproject) do not expose package-version advisories; advisory coverage remains unsupported.
- Hugging Face uses an observed full-text API contract; schema changes fail closed.
- Tests are offline fixtures; production validation remains for T09.

## T05 — Scoring and export

### Summary

Implemented versioned weighted scoring, coverage and failure diagnostics, provisional CSV labels, deterministic ranking and validated atomic JSON export. Stars and velocity have zero ranking weight; null scores are excluded.

B1 models and database interfaces remain unchanged. `score_repo()` returns `ScoringResult`; pass its `.score` to `StateStore.add_score()`. Export validation uses `pipeline.export.Listings`.

### Files changed

- `pipeline/scoring.py`
- `pipeline/export.py`
- [docs/scoring.md](/C:/Users/po.nienchen/repos/AI_Hub/docs/scoring.md)
- `tests/test_scoring.py`
- `tests/test_export.py`

### Tests and checks run

- `.venv\Scripts\python -m pytest tests/test_scoring.py tests/test_export.py -q` — PASS: 68 passed.
- `uv run pytest --cov=pipeline --cov-fail-under=80` — PASS: 270 passed; 98.38% coverage.
- `uv run ruff check .` — PASS.
- Type checks — none configured.

### Known gaps and risks

- Release cadence requires two distinct release dates. B1 supplies only the latest release; optional history is supported but not fetched.
- Without advisory assessment or release history, maximum evaluated coverage is 70%.
- New diagnostics persist in exported JSON, not additional SQLite columns.
- The v0 scoring formulas and licence classifications are documented for review.

No staging, commits, branching, pushes or `.ai/` edits were performed. Existing `.ai/` modifications were left untouched.
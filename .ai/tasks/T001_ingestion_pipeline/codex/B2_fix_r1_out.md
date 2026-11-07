# Codex handover — T04, T05

## T04 — Enrichment adapters

### Summary

Completed the approved adapter corrections before starting T05. B1 public signatures remain unchanged.

### Files changed

- [pipeline/sources/_enrichment.py](C:/Users/po.nienchen/repos/AI_Hub/pipeline/sources/_enrichment.py)
- [pipeline/sources/deps_dev.py](C:/Users/po.nienchen/repos/AI_Hub/pipeline/sources/deps_dev.py)
- [pipeline/sources/hacker_news.py](C:/Users/po.nienchen/repos/AI_Hub/pipeline/sources/hacker_news.py)
- [pipeline/sources/hugging_face.py](C:/Users/po.nienchen/repos/AI_Hub/pipeline/sources/hugging_face.py)
- [tests/test_enrichment.py](C:/Users/po.nienchen/repos/AI_Hub/tests/test_enrichment.py)
- [tests/fixtures/enrichment_responses.json](C:/Users/po.nienchen/repos/AI_Hub/tests/fixtures/enrichment_responses.json)

### Tests and checks run

Both tasks used `PYTEST_DEBUG_TEMPROOT=_build/pytest`. uv used the existing worktree `.venv`, synchronisation disabled, and cache/Python directories under `_build`.

- `.venv\Scripts\python.exe -m pytest tests/test_enrichment.py` — **83 passed, 0 failed**.
- `uv run pytest --cov=pipeline --cov-fail-under=80` — **283 passed, 0 failed; 98.49% coverage**.
- `uv run ruff check .` — **passed**.
- Type checks — none specified; none run.

### Finding resolutions

- **F4 — ACCEPTED:** Null HN URLs are skipped; added fixture and regression coverage while retaining structural validation.
- **F5 — ACCEPTED:** Added `absent_statuses`, defaulting to `{404}`; HF and HN pass an empty set.
- **F6 — ACCEPTED:** deps.dev verifies repository identity using `links_repo`; mismatches fail.
- **F8 — DEFERRED:** Live-response verification remains assigned to T09; no change.
- **F9 — PARTIALLY_ACCEPTED:** Closed the owned client through a context manager; E501 remains unselected.

### Known gaps and risks

Live API response shapes remain unverified pending T09.

## T05 — Scoring and export

### Summary

Corrected copyleft classification, exposed coverage through `PublishedListing`, and separated compact site summaries from full local evidence. Weights and score version remain unchanged.

### Files changed

- [pipeline/scoring.py](C:/Users/po.nienchen/repos/AI_Hub/pipeline/scoring.py)
- [pipeline/export.py](C:/Users/po.nienchen/repos/AI_Hub/pipeline/export.py)
- [docs/scoring.md](C:/Users/po.nienchen/repos/AI_Hub/docs/scoring.md)
- [tests/test_scoring.py](C:/Users/po.nienchen/repos/AI_Hub/tests/test_scoring.py)
- [tests/test_export.py](C:/Users/po.nienchen/repos/AI_Hub/tests/test_export.py)

### Tests and checks run

- `.venv\Scripts\python.exe -m pytest tests/test_scoring.py tests/test_export.py` — **107 passed, 0 failed**.
- `uv run pytest --cov=pipeline --cov-fail-under=80` — **322 passed, 0 failed; 98.36% coverage**.
- `uv run ruff check .` — **passed**.
- Type checks — none specified; none run.

### Finding resolutions

- **F1 — ACCEPTED:** Normalised copyleft suffixes; tested all 13 distinct candidate CSV licence values and 18 copyleft variants; corrected documentation.
- **F2 — PARTIALLY_ACCEPTED:** Added validated row-level coverage through an export model extending B1 `Listing`; no weight, version or package-resolution changes.
- **F3 — ACCEPTED:** Added bounded source summaries and full `state/evidence.jsonl` output; verified lossless evidence retention and representative rows plus diagnostics below 8 KiB. Existing `state/` ignore rule applies.
- **F7 — ACCEPTED:** Documented the provisional `full_name` join, rename limitation and future `github_id` gold-label key.

### Known gaps and risks

- Current adapters without release history still permit maximum coverage of 0.70.
- Evidence and site files are replaced atomically individually; they are not a transaction. Evidence carries its run ID.
- Isolated dry runs must pass both `path` and `evidence_path`.
- No `.ai/` edits, Git staging, commits, branches or pushes were performed. Pre-existing changes were preserved.
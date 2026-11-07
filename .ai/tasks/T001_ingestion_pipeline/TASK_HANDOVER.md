# Task handover — T001_ingestion_pipeline

One section per task or block, appended as work lands.

## B1 (T01-T03) — executor Codex, 07 November 2026

### Codex handover (verbatim)

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

### Coordinator checks (Claude, after the Codex run)
- `git status`: 24 new files under pipeline/, tests/, pyproject.toml, uv.lock, .python-version; .gitignore gained cache and _build lines. No unexpected changes.
- `uv run pytest --cov=pipeline --cov-fail-under=80`: 119 passed, coverage 99.23%.
- `uv run ruff check .`: 2 findings, both in scripts/sample_and_fetch.py (phase 0 script, not Codex's scope); fixed by Claude in a separate commit before the block commit; now clean.
- Codex run: 1,163 s, 106,774 tokens, weekly limit 24% used.

### B1 corrections round 1 — executor Codex, 07 November 2026

#### Codex handover (verbatim)

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

#### Coordinator checks (Claude)
- `uv run pytest --cov=pipeline --cov-fail-under=80`: 132 passed, coverage 99.26%.
- `uv run ruff check .`: clean (rules now pinned in pyproject.toml).
- Codex run: 430 s, 68,067 tokens, weekly limit 24% used.

## B2 (T04-T05) — executor Codex, 07 November 2026

### Codex handover (verbatim)

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

### Coordinator checks (Claude)
- `git status`: 12 new files (four adapters plus shared helper, scoring, export, docs/scoring.md, fixtures, three test modules). No unexpected changes.
- `uv run pytest --cov=pipeline --cov-fail-under=80`: 270 passed, coverage 98.38%.
- `uv run ruff check .`: clean.
- Codex run: 761 s, 95,138 tokens, weekly limit 25% used.

### B2 corrections round 1 — executor Codex, 07 November 2026

#### Codex handover (verbatim)

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

#### Coordinator checks (Claude)
- `uv run pytest --cov=pipeline --cov-fail-under=80`: 322 passed, coverage 98.36%.
- `uv run ruff check .`: clean.
- Codex run: 563 s, 77,024 tokens, weekly limit 25% used.
- Untracked docs files (platform flowchart and report, .claude/launch.json) are not part of this request and were not staged.

### B2 corrections round 2 — executor Codex, 07 November 2026

#### Codex handover (verbatim)

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

#### Coordinator checks (Claude)
- `uv run pytest --cov=pipeline --cov-fail-under=80`: 323 passed, coverage 98.36%.
- `uv run ruff check .`: clean.
- Codex run: 309 s, 49,405 tokens, weekly limit 26% used.

## B3 (T06-T08) — executor Codex, 07 November 2026

### Codex handover (verbatim)

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

### Coordinator checks (Claude)
- `git status`: new gates.py, failure.py, cli.py, release.py, four test modules, fake_gh fixture, .github/workflows/refresh.yml, .github/dependabot.yml, README.md, docs/runbook.md; pyproject.toml, uv.lock and docs/scoring.md modified. No unexpected changes to source.
- `uv run pytest --cov=pipeline --cov-fail-under=80`: 412 passed, coverage 98.39%.
- `uv run ruff check .`: clean. `uv run pipeline --help`: prints usage.
- `actionlint` not installed on this machine; the workflow test parses the YAML, cron, permissions and concurrency instead.
- Codex run: 1,161 s, 124,220 tokens, weekly limit 27% used.

### B3 audit F3 verification (Claude, 07 November 2026, live gh api)
- actions/checkout v6 → d23441a48e516b6c34aea4fa41551a30e30af803 (matches the pin)
- astral-sh/setup-uv v7 → 37802adc94f370d6bfd71619e3f0bf239e1f3b78 (matches)
- actions/upload-artifact v6 → b7c566a772e6b6bfb58ed0dc250532a479d7789f (matches)
- astral-sh/uv release 0.11.19 exists; gh 2.92.0 (2026-04-28) prints `release not found` for a missing release.

### B3 corrections round 1 — executor Codex, 07 November 2026

#### Codex handover (verbatim)

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

#### Coordinator checks (Claude)
- `uv run pytest --cov=pipeline --cov-fail-under=80`: 434 passed, coverage 98.42%.
- `uv run ruff check .`: clean.
- Codex run: 516 s, 68,078 tokens, weekly limit 28% used.

## T09 — dry run against 50 repos (Claude), attempt 1, 07 November 2026
- Command: `uv run pipeline run --dry-run --limit 50` with GH_TOKEN from `gh auth token`.
- Result: exit 1 after 7 s at stage ingest: `GitHub query 'coding_agent': GraphQL returned errors; partial data discarded`.
- Diagnosis: GitHub GraphQL RESOURCE_LIMITS_EXCEEDED on 50-node pages with the full field set; pages of 25 succeed (probe table in AUDIT_LOG.md, T09 section). Fix sent to Codex as a T03 correction; dry run to be repeated after it.

### T03 correction from the T09 finding — executor Codex, 07 November 2026

#### Codex handover (verbatim)

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

#### Coordinator checks (Claude)
- `uv run pytest --cov=pipeline --cov-fail-under=80`: 454 passed, coverage 98.44%.
- `uv run ruff check .`: clean.
- Codex run: 407 s, 57,811 tokens, weekly limit 28% used.

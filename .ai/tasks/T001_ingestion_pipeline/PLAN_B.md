# Plan B (Codex) — T001 ingestion pipeline and state store

Author: Codex, model gpt-6-astra, effort xhigh, 115s

## Objective

Build a reproducible Python 3.13 ingestion pipeline that preserves repository history, calculates explainable trust scores, validates listings and safely persists successful runs. Deliver offline verification and a timed 50-repository dry run; defer live workflow acceptance until a remote exists.

## Assumptions

- `.ai/tasks/T001_ingestion_pipeline/REQUEST.md` overrides the older request: use six-hourly star snapshots; no BigQuery or Google Cloud credentials.
- `.ai/DECISIONS.md` limits initial coverage to the coding-agent stack.
- No spatial data, CRS or GPU processing applies.
- The supplied tree contains no package configuration or tests. CSV contents, including the topic vocabulary, are **not in the pack**.
- Score weights and valid bootstrap labels need agreement: request 2 supplies labelling, while T001 already requires levels and topics.

## Proposed architecture

Use `pipeline/` with configuration, source adapters, SQLite persistence, scoring, validation and a CLI orchestrator. Inject HTTP clients and clocks for deterministic tests.

The four required tables contain:

- `repos`: stable GitHub identity, current metadata, README/hash, root listing and source/label provenance.
- `snapshots`: timestamped star counts and maintenance observations, unique per repository/run.
- `scores`: versioned component evidence, coverage and aggregate score.
- `run_log`: status, timings, budgets, row counts and gate outcomes.

Calculate star velocity from actual elapsed observation time; the first snapshot has no velocity. Neither stars nor velocity contributes to ranking.

Keep unavailable evidence distinct from negative evidence. Persist source timestamps and explicit collection bounds. Use a working database copy, transactional writes and integrity checks. Validate staged JSON before promotion; retain the previous successful database and output on failure.

## Numbered tasks

1. **Establish package and data contracts**  
   **Objective:** Configure Python 3.13, uv, CLI, typed settings and pydantic models; settle scoring, topic vocabulary and bootstrap-label policy.  
   **Depends on:** Approved plan and dependency-file changes.  
   **Likely files:** `pyproject.toml`, `uv.lock`, `.python-version`, `pipeline/config.py`, `pipeline/models.py`, `.gitignore`.  
   **Tests:** Proposed `tests/test_models.py`, `tests/test_config.py`; invalid enums, timestamps and missing configuration.  
   **Risk:** medium.

2. **Implement durable state and snapshots**  
   **Objective:** Add schema versioning, idempotent upserts, transactions, snapshot velocity, recoverable backups and successful-run baselines. Preserve history across repository renames.  
   **Depends on:** 1.  
   **Likely files:** `pipeline/store.py`, `pipeline/migrations/`, `pipeline/snapshots.py`.  
   **Tests:** Proposed `tests/test_store.py`, `tests/test_snapshots.py`; interrupted writes, duplicate runs, renames, first observations and falling star counts.  
   **Risk:** medium.

3. **Build GitHub ingestion and budget accounting**  
   **Objective:** Preserve query strings from `scripts/pull_candidate_repos.py::QUERIES`, with explicit niche selection, pagination and deduplication. Fetch metadata, releases, contributor evidence, README and root files. Verify GraphQL contributor coverage; document any necessary REST fallback. Replace `search()`/`main()` error-and-continue behaviour with explicit failure handling.  
   **Depends on:** 1–2.  
   **Likely files:** `pipeline/sources/github.py`, `pipeline/http.py`, `pipeline/budgets.py`, `pipeline/queries.py`.  
   **Tests:** Proposed `tests/test_github.py`, `tests/test_budgets.py`; pagination, partial GraphQL errors, retry limits and budget exhaustion.  
   **Risk:** high.

4. **Add enrichment adapters**  
   **Objective:** Collect deps.dev and Scorecard evidence, verified Hugging Face model/Space links and bounded Hacker News Firebase mentions. Distinguish unsupported projects, absent evidence and service failures; record coverage rather than imply exhaustive discovery.  
   **Depends on:** 3.  
   **Likely files:** `pipeline/sources/{deps_dev,scorecard,hugging_face,hacker_news}.py`.  
   **Tests:** Proposed `tests/test_enrichment.py`; fixture responses, ambiguous repository associations, missing records, caching and pagination.  
   **Risk:** medium.

5. **Implement scoring, export and gates**  
   **Objective:** Calculate a documented, versioned score from available trust inputs. Mark request-4 fraud/typosquat checks unevaluated. Export validated listings with label provenance, explicit licence status and `untested` status. Enforce freshness below seven hours, count retention of at least 90%, required fields and dated test evidence.  
   **Depends on:** 2–4 and agreed label policy.  
   **Likely files:** `pipeline/scoring.py`, `pipeline/export.py`, `pipeline/gates.py`, `site/src/data/listings.json`.  
   **Tests:** Proposed `tests/test_scoring.py`, `tests/test_gates.py`; missing evidence, score bounds, star-independent ordering, stale sources and first-run baseline.  
   **Risk:** high.

6. **Orchestrate refresh and release persistence**  
   **Objective:** Add cron `17 */6 * * *`, manual dispatch, concurrency protection, frozen installs, gates and recoverable `data-latest` download/upload. Separate public-read credentials from release/issue write permissions. Budget aborts must preserve previous outputs and report failure.  
   **Depends on:** 5.  
   **Likely files:** `pipeline/cli.py`, `pipeline/release_store.py`, `.github/workflows/refresh.yml`.  
   **Tests:** Proposed `tests/test_refresh.py`, `tests/test_release_store.py`; absent/corrupt assets, failed uploads and failure reporting.  
   **Risk:** high.

7. **Document and demonstrate acceptance**  
   **Objective:** Document operation and the first four required runbook entries, marking future BigQuery/labeller/sandbox procedures accordingly. Run an isolated, non-publishing 50-repository dry run.  
   **Depends on:** 6.  
   **Likely files:** `README.md`, `docs/runbook.md`, `tests/test_pipeline.py`.  
   **Tests:** Full suite, coverage report, schema validation and recorded runtime below ten minutes.  
   **Risk:** medium.

## Implementation order

After Gates 1 and 2: 1 → 2 → 3 → 4 → 5 → 6 → 7. Use `dual_dev/T001_ingestion_pipeline`; reciprocal reviews follow the selected audit cadence.

## Test strategy

Require `uv run pytest` with at least 80% pipeline coverage and Ruff checks. Mock services for repeatable failure tests. Enforce GitHub usage below 2,500, including retries; BigQuery and model-token usage remain zero. Keep `.venv` and uv caches worktree-local. Live manual dispatch remains outstanding until the owner creates the remote.

## Risks

Unreviewed labels cannot silently satisfy publication requirements. Undefined weights can overstate trust. API coverage, search limits and sparse snapshots constrain completeness. Release replacement needs recoverable promotion. `.ai/STATE.md` is stale against the request’s commit information.

## Alternatives considered

Retain phase-0 scripts as research utilities; do not reuse `sample_and_fetch.py::gh_json()` error suppression. Defer BigQuery, automated labels and full fraud detection. SQLite suits the batch workload better than introducing a database service.

## Rollback

Revert task commits and restore the last verified release asset and matching JSON. Back up databases before migrations; never replace valid state following failed gates.

## Open questions for the user

- Approve a reviewed 50-repository bootstrap label set, or explicitly provisional labels for T001?
- Approve versioned initial scoring weights with incomplete trust checks exposed?
- Which coding-agent query subset should define initial discovery?
# Plan A (Claude Code) — T001 ingestion pipeline and state store

Author: Claude Code

## Objective
A `pipeline/` Python 3.13 package, managed by uv, that ingests repo metadata and trust inputs for the topic queries, keeps history in `state/gateway.sqlite`, computes a trust score, writes a validated `site/src/data/listings.json`, and runs every six hours from `.github/workflows/refresh.yml` behind gates 1 to 3, with `docs/runbook.md`.

## Assumptions
- No BigQuery in this request; star velocity = difference between consecutive snapshots in the state store (24 h and 7 d windows once history exists; null before).
- No remote yet, so the release upload and download are implemented behind a `GH_RELEASE_ENABLED` flag and covered by unit tests with a fake `gh`; the live workflow dispatch is the owner's step once the remote exists.
- Topic queries are lifted verbatim from `scripts/pull_candidate_repos.py` into `pipeline/config.py`.
- Trust score weights are a first cut, documented in `docs/scoring.md`, to be tuned in request 4.

## Proposed architecture
`pipeline/` = `config.py` (queries, budgets, weights) · `sources/` (`github_graphql.py`, `deps_dev.py`, `scorecard.py`, `huggingface.py`, `hackernews.py`, each a pure fetcher returning typed dataclasses, `httpx` client injected) · `store.py` (SQLite schema and upserts: `repos`, `snapshots`, `scores`, `run_log`) · `scoring.py` (trust score 0 to 100) · `publish.py` (pydantic models `Listing`, `Listings`; writes JSON) · `gates.py` (gate 2 schema, gate 3 data quality) · `budget.py` (counters and `BudgetExceeded`) · `release.py` (download and upload `data-latest` via `gh release`) · `cli.py` (`pipeline run --limit N --dry-run`, `pipeline gates`, `pipeline release pull|push`). Tests under `tests/` with recorded JSON fixtures; no network in tests.

## Numbered tasks
1. **Package skeleton and config** — `pyproject.toml` (uv, ruff, pytest, coverage 80), `pipeline/__init__.py`, `config.py` with queries, budgets, weights; `tests/conftest.py`. Depends: none. Files: pyproject.toml, pipeline/config.py. Tests: config loads; queries equal the script's. Risk low.
2. **State store** — `store.py`: schema migration, upserts, snapshot insert, run_log write, velocity query. Depends: 1. Tests: in-memory SQLite round trip; velocity from two snapshots. Risk low.
3. **GitHub GraphQL source** — search by query with pagination, repo node (stars, forks, pushedAt, releases(last 1), mentionableUsers count, licence, topics, README hash), rate-limit cost accounting into `budget.py`. Depends: 1. Tests: fixture responses; budget abort. Risk medium.
4. **Trust input sources** — deps.dev, Scorecard, Hugging Face Hub, Hacker News Algolia or Firebase; each tolerant of 404. Depends: 1. Tests: fixtures per source. Risk low.
5. **Scoring and publish** — `scoring.py` weights (Scorecard, deps.dev advisories, licence class, maintenance recency, release cadence, velocity, HN mentions), `publish.py` pydantic models and writer. Depends: 2, 3, 4. Tests: score bounds, no-star-rank property, JSON validates. Risk medium.
6. **Gates and budgets** — `gates.py` gate 2 and gate 3 checks against the previous run; `budget.py` abort rule; GitHub issue body text on abort. Depends: 5. Tests: each gate failing and passing. Risk low.
7. **Release round trip and CLI** — `release.py` using `gh release download|upload --clobber`; `cli.py` orchestration with `--dry-run` and `--limit`. Depends: 2, 6. Tests: fake `gh` on PATH. Risk medium.
8. **Workflow, runbook, docs** — `refresh.yml` (cron `17 */6 * * *`, `workflow_dispatch`, uv setup, `pipeline release pull`, `pipeline run`, gates, release push, `gh issue create` on failure), `docs/runbook.md` first four entries, `docs/scoring.md`. Depends: 7. Tests: `actionlint` if available, else YAML parse. Risk low.
9. **Dry run against 50 repos** — real network, `pipeline run --limit 50 --dry-run`, record time and token-free cost in `TASK_HANDOVER.md`. Depends: 8. Risk medium (network).

## Implementation order
1, 2, 3, 4 (3 and 4 independent), 5, 6, 7, 8, 9.

## Test strategy
pytest with recorded fixtures only; `uv run pytest --cov=pipeline --cov-fail-under=80`; `ruff check`; a property test that sorting listings by trust score differs from sorting by stars on the fixture set; one dry run with network as the acceptance check.

## Risks
GraphQL search cost higher than budgeted for 17 queries (mitigate: 100 per query, `--limit`); Scorecard missing for most small repos (score tolerates null); release upload untestable live without a remote; velocity null on the first run (gate 3 must allow it).

## Alternatives considered
Parquet instead of SQLite (rejected: no history queries); committing state to git (rejected: bloat); REST instead of GraphQL (rejected: 5 to 10 times the calls).

## Rollback
Delete the request branch; `state/` is ignored; no remote changes.

## Open questions for the user
None blocking. Trust score weights to confirm at request 4.

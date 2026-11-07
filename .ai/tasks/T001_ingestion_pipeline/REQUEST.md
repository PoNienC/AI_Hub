# Request T001_ingestion_pipeline

Date: 07 November 2026 · Codex model: default (gpt-6-astra) · effort: xhigh on every step · Codex tokens so far: 21,405 (plan)

## Request (verbatim)
Build the ingestion pipeline described in docs/phase1_architecture_and_operations.md sections 1 and 2. Python 3.13 package pipeline/ with uv. Sources: GitHub GraphQL (repo metadata, releases, contributors for repos matching the topic queries in scripts/pull_candidate_repos.py), deps.dev and OpenSSF Scorecard for trust inputs, Hugging Face Hub API for model and Space links, Hacker News Firebase for mentions. BigQuery and GH Archive are optional in this request: star velocity comes from the pipeline's own six-hourly star snapshots until a Google Cloud key exists (request 4). State: one SQLite file state/gateway.sqlite with tables for repos, snapshots, scores and run_log, uploaded as the GitHub Release asset data-latest at the end of each run and downloaded at the start. Scoring: a trust score as defined in section 1, no raw-star ranking. Output: site/src/data/listings.json validated with pydantic. Workflow .github/workflows/refresh.yml on cron 17 */6 * * * with budgets and the abort rule from section 2, and gates 1, 2 and 3 from section 3. Write docs/runbook.md with the first four runbook entries from section 5. Acceptance: uv run pytest green with coverage at 80 per cent or better; a dry run against 50 repos completes in under 10 minutes and produces a valid listings.json; the workflow passes on a manual dispatch. British English, type hints, pathlib, logging not print.

## Confirmed constraints
- Target document: docs/phase1_architecture_and_operations.md (sections 1, 2, 3, 5).
- No BigQuery or Google Cloud key in this request; star velocity from own snapshots.
- No remote repository exists yet: the GitHub Release upload and the workflow dispatch can be implemented and unit-tested, but only exercised live once a remote exists (owner action).
- User rules: British English, type hints, pathlib, logging not print, snake_case names, no "claude" in names, no AI credit lines in commits.

## Starting point
- Branch: dual_dev_setup (unmerged setup branch; the request branch stacks on it, so its pull request will include the setup commits unless setup merges first).
- Commit: 4a66f25 "Add phase 0 research, data and phase 1 plan".

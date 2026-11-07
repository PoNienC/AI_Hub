# How the AI_Hub gateway works — from trending repo to a running starter

V1 · 07 November 2026 · PNC · audience: Po. HTML twin: `docs/ai_hub_platform_structure.html` (swim-lane flowchart inside; editable source `docs/ai_hub_platform_flow.json`).

## In short
- One scheduled pipeline, one state file, one static site. No servers.
- Every six hours: pull state, ingest, enrich, score, label, export, six gates, promote, deploy.
- Stars never decide the ranking. A trust score and a dated sandbox test do.
- Po's only recurring job is a 15-minute monthly check; failures open their own GitHub issue.
- Decision needed: none in this document; it describes the approved phase 1 plan.

## Definitions
- MCP — Model Context Protocol; MCP servers are one of the three listing types.
- Scorecard — OpenSSF Scorecard, a free weekly security score per repository.
- Gate — an automatic check; the site deploys only when all six pass.
- SQLite — the single state file `gateway.sqlite`, kept as a GitHub release asset.
- Astro — the static site builder; pages are served by Cloudflare Pages.

## Timeline
- 07 November 2026: phase 0 done (research, gap table, 100-repo sample).
- 07 November 2026: request 1 in progress (ingestion, store, scoring built; gates, CLI, workflow next).
- Next: request 2 labeller, request 3 sandbox tests, request 4 trust layer, request 5 site and deploy.

## The workflow (swim lanes, top to bottom)
Lanes: Scheduler (GitHub Actions) · Pipeline (Python) · Data (state and outputs) · Site and reader (Astro on Cloudflare Pages) · Po (maintainer).

1. Scheduler starts a run every 6 hours (cron 17 */6) or on a manual dispatch.
2. Pipeline pulls the last `gateway.sqlite` from the release asset `data-latest`.
3. Ingest from GitHub GraphQL: six coding-agent-stack queries; metadata, latest release, README hash. A blocklisted repo is excluded on the next run.
4. Enrich each repo: deps.dev, OpenSSF Scorecard, Hugging Face links, Hacker News mentions.
5. Trust score 0 to 100 from licence, maintenance, Scorecard and mentions; stars and velocity carry zero weight.
6. Label level and topic with the Claude API, cached by README hash; must agree with Po's `gold_labels.csv` at 85 per cent, otherwise the previous labels stay (request 2).
7. Nightly at 02:00 the sandbox job installs each new or week-old listing in a clean container; only a dated pass gives the "works first try" badge (request 3).
8. Export `listings.json` (ten per topic, level filter, pydantic-validated) plus `evidence.jsonl` that the site never ships.
9. Six gates: unit tests, schema, data quality, label agreement, site smoke test, security audit.
10. Gates fail: keep the last good site, write `failures.jsonl`, open a GitHub issue, email Po. Po fixes from the runbook.
11. Gates pass: promote the state file, upload `data-latest`, build the Astro site, deploy to Cloudflare Pages.
12. Mondays 07:00: weekly digest and RSS.
13. The reader picks a level and a topic and gets the first command to run and the reason to trust it.
14. Po: monthly 15-minute check of issues, run log and label agreement trend.

## Stages, inputs and outputs
| Stage | Tool | In | Out | Status |
|---|---|---|---|---|
| Pull state | gh release download | data-latest | working copy of the database | built |
| Ingest | GitHub GraphQL | query list | repos, snapshots | built |
| Enrich and score | deps.dev, Scorecard, HF, HN | repo list | score with coverage and version | built; weights v0 to be confirmed |
| Label | Claude API | README, tree | level, topic, label_status | to set up (request 2); gold labels needed |
| Sandbox test | nightly Docker job | new and week-old listings | tested pass, fail, untested with date | to set up (request 3) |
| Export and gates | pydantic, pytest, Playwright | scored, labelled repos | listings.json or failures.jsonl | export built; gates in progress |
| Promote, deploy, digest | GitHub release, Cloudflare Pages, RSS | listings.json | live site, data-latest | to set up (request 5) |

## What runs when
| When | Job | What happens | If it fails |
|---|---|---|---|
| Every 6 hours | refresh.yml | the full run above | last good site stays; issue; email |
| Nightly 02:00 | sandbox.yml | install tests | recorded as untested |
| Monday 07:00 | digest.yml | digest and RSS, then a refresh | digest skipped |
| Two failures in a row | status.json | red "data is stale" banner | Po follows the runbook |
| Monthly, 15 min | Po | issues, run log, agreement trend | — |

## Targets
- 6 h refresh · 6 gates before any deploy · 85 per cent label agreement · 0 manual steps a week.

## Gaps and what we need
- Data: `gold_labels.csv` from Po's review (before request 2); Google Cloud key for GH Archive (before request 4).
- To be confirmed: scoring weights v0 and the advisories component (request 4); domain name.
- To set up: requests 2 to 5; Cloudflare account and four GitHub secrets.

## Dry run (last)
- Task T09 after block B3: `pipeline run --dry-run --limit 50` on the real network; under 10 minutes; no promotion, no upload; one real response per adapter recorded as a test fixture.

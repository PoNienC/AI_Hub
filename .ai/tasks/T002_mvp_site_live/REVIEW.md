# Hand-off review — T002_mvp_site_live: MVP site and live schedule

- Date: 07 November 2026 · branch `dual_dev/T002_mvp_site_live` (stacked on `dual_dev/T001_ingestion_pipeline`)
- Hand-off commit: `8ad1ba6` (request started at `d73a1d2`)
- Push: only after every audit below is complete. Fixes come as new commits on top; nothing you review is amended or rebased. Pushes need the PoNienC gh account.
- Close-out: automatic once every audit is closed, unless you send review notes (approved at the gate).

## In short

- **Built:** the MVP front end: a Jinja2 site generator inside the pipeline (index by topic with a level filter, paginated topic pages, one page per repo by GitHub id, "how we grade", status.json), light gate 5 wired into `pipeline run`, and `refresh.yml` deploying to GitHub Pages with the built-in token; README "Live site" and runbook entries; proven by a live 20-repo dry run and a browser check.
- **Tests:** 535 passed, coverage 98.34 per cent, `ruff check .` clean, on the final tree.
- **Audits:** both complete (B1: 11 findings resolved; B2: one LOW record correction). No BLOCKER or HIGH open.
- **Look at first:** http://localhost:8766/index.html (the `site_preview` launch entry serves `site/dist.dry/`), then `README.md` "Live site" for the go-live steps.

## What was built

| Task | Title | Executor | Commit | What it does (one line) |
|---|---|---|---|---|
| T01 | Site generator, templates, dependencies | Codex | abc99df | `pipeline/site/builder.py`, templates plus a label partial, staged build and atomic swap, id routes, status.json |
| T02 | Light gate 5, CLI and wiring | Codex | abc99df | `pipeline site build`; gate 5 (links, size, case-exact paths, host allow-list) before promotion; dry run to `site/dist.dry/` |
| T03 | Workflow, Pages deploy, docs | Codex | abc99df | built-in token; `pipeline gates` check then Pages artefact upload and `deploy` job; README, runbook, architecture targets restored |
| T04 | Local acceptance run | Claude | 8ad1ba6 | 20-repo live dry run in 51 s, 37 pages, gates 2/3/5 pass, browser check, pins verified |

Audit fix commit: 1eee812 (B1).

## How to try it

1. `uv sync --frozen`; set `GH_TOKEN` from `gh auth token`.
2. `uv run pipeline run --dry-run --limit 20`, then `uv run pipeline site build --input site/src/data/listings.dry.json --output site/dist.dry`.
3. Serve `site/dist.dry/` (the `site_preview` launch entry, or `python -m http.server 8766 --directory site/dist.dry`) and open index.html.
4. `uv run pytest --cov=pipeline --cov-fail-under=80` and `uv run ruff check .`.

## Audits

| Scope | Tasks | Reviewer (model, effort) | Status | Findings B/H/M/L/N | Fix commit |
|---|---|---|---|---|---|
| B1 | T01-T03 | Claude subagent (session model) plus coordinator browser check | complete | 0/0/2/6/3 (F1-F7, C1-C4) | 1eee812 |
| B2 | T04 | Codex (gpt-6-astra, xhigh) | complete | 0/0/0/1/0 | close-out commit (record wording) |

Status: running · awaiting your review · fixing · re-check running · complete.

## Go-live steps for you (after close-out, each asked separately)

1. Merge `dual_dev_setup`, `dual_dev/T001_ingestion_pipeline` and `dual_dev/T002_mvp_site_live` into `main` (fast-forward) and make `main` the default branch.
2. Make the repository public (free-plan Pages), then Settings, Pages, Source "GitHub Actions".
3. Run `refresh.yml` once by hand (workflow_dispatch): the first run creates the `data-latest` release and deploys https://ponienc.github.io/AI_Hub/.
4. From then on the schedule runs every 6 hours; failures open an issue.

## Your review notes

Send notes in chat; please do not edit repo files until completion (fixes land here, each one announced). A change you ask for becomes a new task.

| # | Your note | Became task, or "no action" | Status |
|---|---|---|---|

## Changes since the hand-off

- close-out commit — B2 audit logged, size record corrected (F1), STATE.md and DECISIONS.md updated. No source change since the hand-off.

## Detail

### Files changed

~~~text
 .claude/launch.json                        |    6 +
 .github/workflows/refresh.yml              |   28 +-
 .gitignore                                 |    2 +
 README.md                                  |   54 +-
 docs/phase1_architecture_and_operations.md |   46 +-
 docs/runbook.md                            |  101 +-
 docs/scoring.md                            |   26 +-
 pipeline/cli.py                            |   70 +-
 pipeline/gates.py                          |   11 +
 pipeline/site/__init__.py                  |    1 +
 pipeline/site/builder.py                   |  198 +
 pipeline/site/links.py                     |   89 +
 pipeline/site/templates/base.html          |   36 +
 pipeline/site/templates/how_we_grade.html  |    5 +
 pipeline/site/templates/index.html         |   25 +
 pipeline/site/templates/label.html         |    5 +
 pipeline/site/templates/repo.html          |   23 +
 pipeline/site/templates/topic.html         |   14 +
 pyproject.toml                             |    6 +-
 tests/fixtures/listings_sample.json        | 6359 ++++++++++++++++++++++++++++
 tests/test_cli.py                          |   86 +-
 tests/test_gates.py                        |   58 +-
 tests/test_site.py                         |  373 ++
 tests/test_workflow.py                     |   49 +-
 uv.lock                                    |  593 +++
 25 files changed, 8176 insertions(+), 88 deletions(-)
~~~

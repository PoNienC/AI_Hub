# Approved plan — T002_mvp_site_live: MVP site and live schedule

Source: hybrid (Claude's four-task shape with Codex's staged output, id routes, status fields, dependency audit and the Pages eligibility question). User's instructions (07 November 2026): "C Hybrid (Recommended)"; preset "Confirm (Recommended)"; close-out "Yes, automatic (Recommended)"; visibility "Make public at go-live (Recommended)".

Standing rules for every task: Python 3.13, uv, `pipeline/` package; type hints on public functions; module docstring per file; pathlib; logging not print; British English; no network in unit tests; `uv run pytest --cov=pipeline --cov-fail-under=80` and `uv run ruff check .` are the project checks; the site never sorts by stars; labels and `tested` are shown as the data says (`provisional`, `pending`, `untested`) with a one-line note; every repo text is HTML-escaped and outbound links are `https://github.com/...` only.

## T01 — Site generator, templates, dependencies
- Objective: `pipeline/site/` with `builder.py` (load `pipeline.export.Listings` from a JSON path; group by topic preserving the exported order, top ten per topic for the index; routes by `github_id`: `repos/<github_id>.html`, `topics/<topic>.html`, `index.html`, `how_we_grade.html`, `status.json`; build into a temporary directory next to the target, then replace the target atomically; never read the state store), Jinja2 templates packaged under `pipeline/site/templates/` (`base.html` with a small CSS block, `index.html` with the level filter as a few lines of inline JavaScript that only toggles visibility, `topic.html`, `repo.html` with score, coverage, evaluated components with status, licence class, last push, latest release, label with status, tested status, GitHub link, `how_we_grade.html` rendered from `docs/scoring.md` with relative links resolved or stripped), `status.json` (`generated_at`, `run_id`, `score_version`, `listing_count`, `checks` list; data age computed in the browser). Dependencies: `jinja2`, `markdown-it-py`; add `pip-audit` to dev dependencies and a `uv run pip-audit` line to the runbook's checks.
- Depends on: none.
- Likely files: pipeline/site/__init__.py, pipeline/site/builder.py, pipeline/site/templates/*.html, pyproject.toml, uv.lock, tests/test_site.py, tests/fixtures/listings_sample.json (20 or more sanitised rows from the dry run).
- Acceptance: build from the fixture produces index, one page per topic, one page per repo, how_we_grade, status.json; every field named above appears on a repo page (one parametrised test over the field list); hostile description text is escaped; an empty topic renders a "no entries" state; the previous `dist` survives a failed build.
- Tests: test_site (structure, fields, escaping, ordering equals exported order, empty topic, failed-build retention).
- Risk: medium.

## T02 — Light gate 5, CLI and wiring
- Objective: `pipeline/site/links.py` with `check(dist)`: every internal `href`/`src` resolves to a file in `dist` (fragments allowed), no HTML page over 200,000 bytes, index has at least one topic; registered as `gate_5` in `pipeline/gates.py`. `pipeline site build [--input PATH] [--output PATH]` in `pipeline/cli.py` (defaults `site/src/data/listings.json` → `site/dist/`; no credentials needed). `pipeline run` builds the site after export and runs gate 5 before promotion; a dry run writes to `site/dist.dry/` (git-ignored) from the dry listings. Gate 5 failure follows the existing failure path (rollback, failures.jsonl, issue text).
- Depends on: T01.
- Likely files: pipeline/site/links.py, pipeline/gates.py, pipeline/cli.py, .gitignore, tests/test_gates.py, tests/test_cli.py, tests/test_site.py.
- Acceptance: a broken link and an oversize page each fail gate 5 with a message naming the page; a clean build passes; `pipeline run --dry-run --limit 5` offline (injected client) produces `site/dist.dry/` and never touches `site/dist/`; a gate 5 failure in a real run rolls back and records the failure.
- Tests: test_gates (gate 5 pass and fail cases), test_cli (dry run builds to dist.dry; failure path), test_site (links).
- Risk: medium.

## T03 — Workflow, Pages deploy, docs
- Objective: extend `.github/workflows/refresh.yml`: `GH_TOKEN: ${{ github.token }}` and `GH_REPO` (drop `secrets.GH_TOKEN`); after `release push`, upload `site/dist/` with `actions/upload-pages-artifact`, then a `deploy` job with `actions/deploy-pages`, `environment: github-pages`, permissions `pages: write` and `id-token: write` on that job only; pin both actions by SHA with the tag in a comment (Claude verifies the pins live at audit); failure issue step unchanged. `README.md` "Live site" section: URL pattern `https://ponienc.github.io/AI_Hub/`, local preview command, owner go-live steps (merge to main, make default, enable Pages with source "GitHub Actions", repo visibility note, first dispatch). `docs/runbook.md`: built-in token limits (GraphQL points shared per repository, release asset on this repo only), Pages visibility rule, site rollback (re-run the last green deploy). Correct obsolete request-number and Astro references in `docs/phase1_architecture_and_operations.md` and `docs/scoring.md`. `tests/test_workflow.py` extended: no `secrets.` reference, deploy job present with its permissions and environment, site build step after release push, pins shaped as SHAs.
- Depends on: T02.
- Likely files: .github/workflows/refresh.yml, README.md, docs/runbook.md, docs/phase1_architecture_and_operations.md, docs/scoring.md, tests/test_workflow.py.
- Acceptance: YAML parses; the test assertions above pass; README commands match `cli.py`; runbook has the three new entries.
- Tests: test_workflow.
- Risk: medium.

## T04 — Local acceptance run
- Objective: with the real network, `uv run pipeline run --dry-run --limit 20`, then `uv run pipeline site build --input site/src/data/listings.dry.json --output site/dist.dry`; open the index in the browser pane; record page count, sizes, gate 5 result and any rendering defect in `TASK_HANDOVER.md`; verify the two new action pins against their tags with `gh api`; fix nothing beyond configuration (defects go back to Codex as corrections).
- Depends on: T03.
- Likely files: .ai/tasks/T002_mvp_site_live/TASK_HANDOVER.md.
- Acceptance: at least 20 repo pages, index present, gate 5 passes, under 5 minutes; pins verified.
- Tests: the run itself, plus the full suite and ruff on the final tree.
- Risk: low.

## Implementation order
T01, T02, T03 (one Codex block), then T04 (Claude).

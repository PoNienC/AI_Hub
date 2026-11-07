# Claude audit — T01, T02, T03 (round 1)

Reviewer: Claude audit subagent (dual_dev_auditor, session model), 07 November 2026. Range `d73a1d2..abc99df`. Saved verbatim by the coordinator; snapshot paths shortened to repo-relative.

## Verdict
PASS_WITH_FINDINGS — no blocker; one MEDIUM cross-task finding (the CI rebuild step discards the run's gate records from the deployed `status.json`), the rest LOW or NOTE.
- T01 Site generator, templates, dependencies: PASS_WITH_FINDINGS (acceptance met; LOW/NOTE items on page-size headroom, Windows clean-up and packaging assumptions).
- T02 Light gate 5, CLI and wiring: PASS (acceptance met; NOTE on case-sensitivity).
- T03 Workflow, Pages deploy, docs: PASS_WITH_FINDINGS (acceptance met; MEDIUM on the extra rebuild step, LOW on documentation scope).

## Findings

### F1 [MEDIUM] (cross-task T02/T03) CI rebuilds the site after promotion, so the deployed `status.json` never records gates 2, 3 and 5
- Where: `.github/workflows/refresh.yml:54-57`; `pipeline/cli.py:190-204` and `:273-276`; `pipeline/site/builder.py:121-124`; `docs/runbook.md:117`
- Problem: `uv run pipeline run --no-release` already builds `site/dist/`, runs gate 5 and writes `status.json` with `checks` = listings_schema, gate_2, gate_3, gate_5. The workflow then runs `uv run pipeline site build`, which rebuilds `site/dist/` from the same `listings.json` and writes a fresh `status.json` whose `checks` contains only `listings_schema`. That rebuilt tree is what `upload-pages-artifact` publishes. The runbook documents the behaviour without noting that CI deploys a standalone build. The approved plan for T03 asked only to "upload `site/dist/`" after `release push`; the rebuild and the second `pipeline gates` step were added by the executor and are redundant with the gated build inside `pipeline run`.
- Why it matters: the `checks` list is a named deliverable of T01's `status.json` and the architecture doc promises it "lists completed checks". On the live site that list will be misleadingly short, invisible to tests. Also a failure of the extra step occurs after `release push`.
- Suggested fix: drop the "Build published site" step (keep "Check published site and data" if an independent re-verification before upload is wanted), update `tests/test_workflow.py` accordingly, and correct `README.md:30-37`, `docs/runbook.md:62-66` and `docs/phase1_architecture_and_operations.md:34` to match.

### F2 [LOW] (T01) Topic pages are unbounded while gate 5 caps every page at 200,000 bytes
- Where: `pipeline/site/templates/topic.html:4-6`; `pipeline/site/builder.py:115-116`; `pipeline/site/links.py:11`
- Problem: the index is capped at ten rows per topic, but each topic page lists every row. Until request 3 almost every repository is `pending`, so `topics/pending.html` grows with the whole listing; roughly 145 bytes per row crosses 200,000 bytes at about 1,350 rows. The default niche yields at most 600 repositories; `--all-queries` allows up to 1,700.
- Why it matters: when the limit is crossed, gate 5 blocks publication of the whole site until code changes.
- Suggested fix: paginate or cap topic pages (for example 200 rows per page with "next" links), or add a test at about 1,500 rows and document the ceiling.

### F3 [LOW] (T01) Backup clean-up after a successful swap can turn a published run into a recorded failure; temporary site directories are not git-ignored
- Where: `pipeline/site/builder.py:52-75`; `pipeline/cli.py:206-219`; `.gitignore:20-21`
- Problem: `replace_directory` keeps the old tree inside a `TemporaryDirectory`; its `__exit__` deletes the old tree after the swap. If any old file is held open on Windows (for example by the `http.server` preview the README recommends), `rmtree` raises `PermissionError` after the new site is in place and, in `run_pipeline`, after promotion; `abort_run` then records a failed run and `release.push` is skipped. A killed build leaves `site/.pipeline-site-*` or `site/.dist-build-*` directories that `.gitignore` does not cover.
- Suggested fix: `TemporaryDirectory(ignore_cleanup_errors=True)` or best-effort deletion with a warning; add `site/.*/` to `.gitignore`.

### F4 [LOW] (T03) Architecture document rewritten beyond "correct obsolete request-number and Astro references"
- Where: `docs/phase1_architecture_and_operations.md:49`, `:55`, `:64`, `:74`
- Problem: target statements were replaced with current-state statements (pull-request sample check, the four-secret list, "emails Po", the stale banner, Node lockfile). `.ai/PROJECT.md` names this document "the target for every request".
- Suggested fix: restore the target statements and add a short "Current (request 2):" note where the MVP differs.

### F5 [NOTE] (T03) README CI command split omits `pipeline site build` while the runbook and workflow include it
- Where: `README.md:30-37` versus `docs/runbook.md:62-66` and `.github/workflows/refresh.yml:48-57`
- Suggested fix: align with whichever step list survives F1.

### F6 [NOTE] (T01) Packaging and rendering assumptions worth recording
- Where: `pipeline/site/builder.py:21` (`SCORING_PATH`), `:36-49` (`_scoring_html`); `templates/index.html:9`, `topic.html:3`
- Problem: (a) `SCORING_PATH` resolves relative to the source checkout; (b) `_scoring_html` strips every non-GitHub absolute link so "How we grade" loses its deps.dev, Hugging Face and HN references; (c) `capitalize` produces "Mcp server or skill" and "Rag knowledge".
- Suggested fix: document (a); allow-list the reference hosts on the policy page and in gate 5 if wanted; a display-name map or title case for topics.

### F7 [NOTE] (T02) Gate 5 path checks are case-insensitive on Windows, case-sensitive on GitHub Pages
- Where: `pipeline/site/links.py:70-74`
- Suggested fix: compare `target.name` against `target.parent.iterdir()` names, or leave as is given the Linux gate in CI.

## Checked
- Brief, `PLAN_APPROVED.md` (T01–T04), `TASK_HANDOVER.md`, `AGENTS.md`, `.ai/PROJECT.md`. Diff read in full except the fixture body and `uv.lock`.
- Source read in full: `pipeline/cli.py`, `pipeline/gates.py`, `pipeline/export.py`, `pipeline/models.py`, `pipeline/config.py`, `pipeline/site/builder.py`, `pipeline/site/links.py`, all five templates, `.github/workflows/refresh.yml`, `pyproject.toml`, `.gitignore`; `pipeline/failure.py` (grep); `tests/test_cli.py`, `tests/test_gates.py`, `tests/test_site.py`, `tests/test_workflow.py`.
- T01 acceptance: structure, parametrised field test, hostile text escaped (autoescape on, raw HTML off in markdown-it), empty-topic state, export order and top ten preserved, previous `dist` survives failures; builder never reads SQLite; routes keyed by `github_id` with a safe-segment regex and GitHub-only `html_url` check; `status.json` carries the five fields; `jinja2 3.1.6`, `markdown-it-py 4.2.0`, dev `pip-audit 2.10.1` in `uv.lock`; fixture 50 rows, 5 provisional, no token-like strings.
- T02 acceptance: broken link and oversize page fail naming the page; clean build passes; offline dry run writes `site/dist.dry/` and leaves `site/dist/` untouched; gate 5 failure rolls back with `failed_step == "gate_5"`; swap failure before promotion; `site build` needs no settings; run order export → site build → gates 2/3 → gate 5 → promote; link checker rejects unsafe schemes and traversal; no import cycle.
- T03 acceptance: no `secrets.`; `GH_TOKEN: ${{ github.token }}` and `GH_REPO`; top-level permissions contents/issues write only; `deploy` job with `pages: write`, `id-token: write`, `environment: github-pages`, `needs: refresh`; both new actions pinned by SHA with tag comments; failure issue step unchanged; README "Live site" with URL, preview commands, four owner steps, visibility note; runbook has the three new entries; token-limit figures consistent with 1,000 points/hour per repository.
- Cross-task: index links every topic page; `pipeline gates --path *.dry.json` selects `site/dist.dry/`; recorded results (509 passed, 98.30 per cent, ruff clean) consistent.
- Scope: within the tasks' likely files, except the extent of the architecture-document rewrite (F4).

## Limits
- Could not run tests, ruff, `pip-audit` or `uv lock --check`.
- Could not verify the two action pins live; the coordinator has.
- Could not render the site; filter, CSS and age script reviewed by reading only.
- F2 size estimate is arithmetic, not a measurement.

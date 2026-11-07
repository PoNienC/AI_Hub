# Plan B (Codex) — T002 MVP site and live schedule

Author: Codex, model gpt-6-astra, effort xhigh, 128s

## Objective

Build a Jinja2 MVP from the existing validated listings, add publication checks, and prepare GitHub Pages deployment and six-hourly refresh. Preserve honest scoring, provisional labels and `untested` status. Leave merging, default-branch changes, Pages activation and first dispatch to the owner.

## Assumptions

- T002 stacks on `d73a1d2`, using `dual_dev/T002_mvp_site_live`.
- The request supersedes older Astro, Cloudflare and request-number references.
- Keep `REQUIRE_LABELS = False`; weights v0 and ingestion behaviour remain unchanged.
- Gate 1 must explicitly approve dependency and lockfile changes.
- GitHub account plan, Pages eligibility and actual token capabilities are **not in the pack**; live verification remains pending until an authorised Actions run.

## Proposed architecture

Add `pipeline/site/` with a builder, packaged Jinja2 templates and small static assets. Consume `pipeline.export.Listings` through `gate_2()`, preserving exported ranking rather than sorting by stars.

Generate relative links suitable for a GitHub project site. Use stable GitHub IDs for repository routes and a shared route map for topics, repositories and navigation. Escape repository text, restrict outbound URL schemes and avoid inserting untrusted HTML through JavaScript.

Build into a temporary directory; validate before replacing `site/dist/`. Keep site publication separate from `run_pipeline()` and its database promotion.

`status.json` contains generation time, run ID, score version, listing count and checks actually completed. Browser-side age calculation shows stale data even when failed refreshes leave the previous site online; it must not claim knowledge of consecutive failures.

## Numbered tasks

1. **Define build inputs and dependencies**  
   **Objective:** Specify routes, status fields and CLI options; add Jinja2, a Markdown renderer and Python dependency auditing. Package templates correctly.  
   **Depends on:** Gate 1 approval.  
   **Likely files:** `pyproject.toml`, `uv.lock`, new `pipeline/site/__init__.py`.  
   **Tests:** Locked installation; packaged template discovery.  
   **Risk:** low.

2. **Render the MVP pages**  
   **Objective:** Build every topic’s top ten, complete topic pages, repository details, level filtering and grading documentation. Include all requested evidence fields, pending/provisional labels and `untested`. Render `docs/scoring.md`; explicitly resolve its relative documentation links. Provide empty-topic and no-match states.  
   **Depends on:** 1.  
   **Likely files:** New `pipeline/site/builder.py`, templates and assets.  
   **Tests:** Representative fixtures cover ranking, every requested field, missing metadata, empty topics and hostile text.  
   **Risk:** medium.

3. **Integrate CLI and light gate 5**  
   **Objective:** Extend `pipeline.cli.main()` with `site build --input --output`, defaulting to the requested paths and requiring no API credentials. Add `gate_5()` for internal links, fragments, assets and a 200,000-byte maximum per HTML page. Publish output only after validation. Keep existing gates 2/3 promotion semantics.  
   **Depends on:** 2.  
   **Likely files:** `pipeline/cli.py`, `pipeline/gates.py`, `pipeline/site/builder.py`.  
   **Tests:** Broken links, oversized pages, unsafe paths and failed replacement preserve the previous build.  
   **Risk:** medium.

4. **Establish offline acceptance coverage**  
   **Objective:** Exercise JSON-to-site generation and CLI behaviour without network calls, using at least 20 listings. Confirm score ordering, topic limits, project-path navigation, accessible filtering and stale-age behaviour.  
   **Depends on:** 3.  
   **Likely files:** New `tests/test_site.py`, fixtures; `tests/test_cli.py`, `tests/test_gates.py`.  
   **Tests:** Existing suite plus builder integration tests; browser smoke check for filtering and layout.  
   **Risk:** low.

5. **Prepare gated GitHub Pages deployment**  
   **Objective:** Replace the custom secret with the built-in token. Order refresh as tests, lint/audit, release pull, ingestion, site build/gate, verified release push, Pages artefact upload, deployment. Scope deployment permissions and use the `github-pages` environment. Preserve concurrency, failure issues and diagnostics; pin new actions.  
   **Depends on:** 4.  
   **Likely files:** `.github/workflows/refresh.yml`, `tests/test_workflow.py`.  
   **Tests:** Extend existing schedule, ordering, permissions, token and action-pin assertions; ensure failures block deployment.  
   **Risk:** high.

6. **Document and demonstrate readiness**  
   **Objective:** Add “Live site”, local preview, rollout and rollback instructions; correct obsolete request references. Run the bounded live dry run and build its explicit output. Document token rate limits and private-repository hosting constraints once verified; distinguish offline checks from pending live proof.  
   **Depends on:** 5.  
   **Likely files:** `README.md`, `docs/runbook.md`, `docs/phase1_architecture_and_operations.md`, `docs/scoring.md`.  
   **Tests:** Assert at least 20 repository pages and a passing gate 5.  
   **Risk:** medium.

## Implementation order

Approve plan and dependencies, then allocate execution and audit modes at Gate 2. Execute 1–6 sequentially. Commit per task or approved executor block; reciprocal audits review committed ranges. No push with outstanding audits, and no push or PR without approval.

## Test strategy

Run `uv run pytest --cov=pipeline --cov-fail-under=80`, Ruff and Python dependency auditing. Preserve offline tests. Perform the live acceptance smoke separately:

`pipeline run --dry-run --limit 20`

`pipeline site build --input site/src/data/listings.dry.json`

Fail acceptance clearly if fewer than 20 repositories survive export.

## Risks

- Built-in token search permissions and available quota need runtime proof.
- Private-repository Pages availability and site visibility require confirmation.
- Release publication and Pages deployment cannot be one atomic transaction.
- High v0 scores can mislead without prominent coverage and evaluation limits.

## Alternatives considered

- Astro: deferred explicitly.
- Browser-fetched JSON: unnecessary; rendered HTML supports browsing without JavaScript.
- Automatic dry-file fallback: rejected because it could publish unintended data.

## Rollback

Before deployment, failed builds retain the previous distribution. Failed refreshes leave the existing site live. Retain successful Pages artefacts for redeployment without rerunning ingestion. Restore release state separately using the existing recovery procedure when necessary.

## Open questions for the user

- Approve the explicit `--input` acceptance command? Dry runs do not write production `listings.json`.
- Can live token verification be completed during the owner’s first dispatch?
- Confirm intended site visibility and Pages eligibility for this private repository.
# State — 07 November 2026 (close-out of T002)

- Branch: `dual_dev/T002_mvp_site_live`, stacked on `dual_dev/T001_ingestion_pipeline` (both requests closed out). `main` still has no commits.
- Remote: https://github.com/PoNienC/AI_Hub (private). Pushed: `dual_dev_setup`, `dual_dev/T001_ingestion_pipeline` (up to 3d044bc). NOT yet pushed: the request-reorder commit d73a1d2 on the T001 branch and the whole T002 branch. Pushes need `gh auth switch -u PoNienC` first, then switch back to PoNienChenPP.
- Request T001 (ingestion pipeline): COMPLETE. Request T002 (MVP site and live schedule): COMPLETE. 535 tests, coverage 98.34 per cent, ruff clean. Live 20-repo dry run plus site build verified in the browser.
- Codex totals: T001 765,096 tokens; T002 327,251 tokens; weekly limit 34 per cent used (resets Wednesday 11 November 10:05).
- Work in flight: none. Next: go-live steps (owner), then request 3 (labeller and gold-set gate) from `docs/dual_dev_requests.md`.
- Local preview: `.claude/launch.json` entries `docs_static` (port 8765, docs) and `site_preview` (port 8766, site/dist.dry).

## Go-live steps for Po (each asked separately by Claude)
1. Push the T001 reorder commit and the T002 branch (PoNienC account).
2. Merge `dual_dev_setup` → T001 → T002 into `main` (fast-forward) and make `main` the default branch on GitHub.
3. Make the repository public (GitHub Pages on the free plan), then Settings → Pages → Source "GitHub Actions".
4. Run `refresh.yml` once by hand (workflow_dispatch): first run creates the `data-latest` release and deploys https://ponienc.github.io/AI_Hub/. Then the 6-hourly schedule is live; failures open issues.

## Owner actions pending after go-live
- Review `data/labelled_repos_for_review.csv` into `data/gold_labels.csv` (before request 3, about one hour).
- Google Cloud key (before request 5); Cloudflare account and domain (before request 6).

## Carry-forwards into later requests
- Request 3: labeller; gate 2 validates `pipeline.export.Listings`; capture one sanitised live response per adapter as fixtures; gold labels keyed by github_id; switch `REQUIRE_LABELS` on.
- Request 4: sandbox tests; `tested` is `untested` everywhere until then.
- Request 5: weights v1 (scores saturate near 100 with three components; Scorecard covers few niche repos); deps.dev package resolution; GH Archive fake-star check.
- Request 6: Astro front end replaces the Jinja2 MVP; Cloudflare Pages and a domain.

## Known issues
- `PYTEST_DEBUG_TEMPROOT=_build/pytest` is for Codex's sandbox only; run pytest without it on Po's shell.
- The first live `pipeline release pull` and Pages deploy are exercised only at go-live; the runbook describes what to expect.

## Sources
- `.ai/tasks/T001_ingestion_pipeline/` and `.ai/tasks/T002_mvp_site_live/` (REVIEW.md, TASKS.md, AUDIT_LOG.md, TASK_HANDOVER.md); root `HANDOVER.md` (personal) for the owner-action dates.

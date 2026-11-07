# State — 07 November 2026 (close-out of T001)

- Branch: `dual_dev/T001_ingestion_pipeline`, stacked on `dual_dev_setup`; `main` still has no commits.
- Remote: https://github.com/PoNienC/AI_Hub (private, created 07 November 2026, HTTPS, credentials via `gh auth setup-git`). `dual_dev_setup` pushed and is the default branch for now. `dual_dev/T001_ingestion_pipeline` pushed on 07 November 2026 after Po granted the `workflow` scope to the PoNienC token. Scheduled workflows run only from the default branch, which is `dual_dev_setup` without the workflow file, so nothing runs on GitHub until the request branch is merged or made default. Pushing from this PC needs `gh auth switch -u PoNienC` first (HTTPS credentials come from the active gh account); switch back to PoNienChenPP afterwards.
- Extra commit after close-out on the request branch: a98beda "Add platform structure flowchart and report" (docs and launch.json, outside the request).
- Last commit: T001 close-out (see `git log -1`). Hand-off commit `4f743c1`.
- Request T001 (ingestion pipeline and state store): COMPLETE. Nine tasks, four audit scopes closed, no BLOCKER or HIGH open. 454 tests, coverage 98.44 per cent, ruff clean. Live dry run: 50 repos in 111 s.
- Codex totals for T001: 765,096 tokens; weekly limit 28 per cent used (resets Wednesday 11 November 10:05).
- Work in flight: none. Next: request 2 (labeller and gold-set gate) from `docs/dual_dev_requests.md`.
- Untracked, outside T001: `docs/ai_hub_platform_*` (flowchart and report), `docs/build_platform_report.py`, `docs/platform_report_body.html`, `.claude/launch.json`. Commit separately when Po says so.

## Owner actions pending
1. Review `data/labelled_repos_for_review.csv` into `data/gold_labels.csv` — due now, before request 2 starts (about one hour).
2. Create the GitHub remote under PoNienC, push the branches on approval, then run `pipeline release pull` once by hand and one `workflow_dispatch` before enabling the schedule (runbook).
3. Before request 4: Google Cloud service account for BigQuery. Before request 5: domain, Cloudflare account, four secrets.

## Carry-forwards into later requests
- Request 2: labeller; gate 2 validates `pipeline.export.Listings`; capture one sanitised live response per adapter as fixtures (B2 F8, B4 F1); gold labels keyed by github_id.
- Request 4: rebalance weights v0 (advisories and release cadence unevaluated, max coverage 0.70; scores saturate near 100 with three components); Scorecard covers 2 of 50 niche repos, so run the Scorecard CLI or lower its weight; deps.dev package resolution; GH Archive fake-star check needs the Google key.
- Request 3: sandbox tests; `tested` is `untested` everywhere until then.

## Known issues
- `PYTEST_DEBUG_TEMPROOT=_build/pytest` is for Codex's sandbox only; on Po's shell it fails with PermissionError because the folder belongs to the sandbox user. Run pytest without it.
- Release round trip and workflow are unit-tested with a fake `gh` and verified action pins, not yet exercised live (no remote).

## Sources
- `.ai/tasks/T001_ingestion_pipeline/` (REVIEW.md, TASKS.md, AUDIT_LOG.md, TASK_HANDOVER.md); root `HANDOVER.md` (personal) for the owner-action dates.

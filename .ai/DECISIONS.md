# Decisions

Format: date · decision · context · alternatives · consequences

- 07 November 2026 · Phase 1 is built through the dual_dev workflow (Claude plans and audits, Codex executes) · Po's instruction after phase 0 · single-agent build · every build item is one `/dual_dev` request; see `docs/dual_dev_requests.md`.
- 07 November 2026 · First niche is the coding-agent stack (coding agents, skills and rules packs, MCP servers) · phase 0 gap table and growth evidence, `reports/AI repo gateway competitor landscape.md` · all ten topics at once · ingestion and sandbox tests scoped to the niche first.
- 07 November 2026 · Rank by a trust score, never by raw stars · own data: Spearman 0.08 between stars and run-readiness on 100 repos; fake-star literature · star velocity ranking · scoring defined in `docs/phase1_architecture_and_operations.md` section 1.
- 07 November 2026 · No "tested" badge without a dated sandbox run · every competitor's "verified" meant paid placement or publisher identity · README-signal proxies · nightly sandbox job, request 3.
- 07 November 2026 · Batch pipeline plus static site, no servers · solo maintainer, free tiers · API back end · GitHub Actions every 6 hours, Cloudflare Pages.
- 07 November 2026 · GitHub account `PoNienC` for this project · personal project · work account `PoNienChenPP` · recorded in `.ai/PROJECT.md`.
- 07 November 2026 · Failed pipeline runs are recorded in an append-only failure log outside the promoted SQLite database · B1 audit finding F5: rollback deletes the working copy, so run_log cannot hold failures · promote a run-log-only change · T07 implements the log; T06 failure text and T08 runbook read from it.
- 07 November 2026 · Scoring weights v0 keep the advisories and release-cadence components even though they cannot be evaluated yet (max coverage 0.70); `coverage` is shown on every listing row; deps.dev package resolution and any weight rebalance happen in request 4 with one score-version change · B2 audit finding F2, approved by Po · rebalance now · listings carry coverage so the gap is visible.
- 07 November 2026 · GitHub GraphQL page size defaults to 25 with adaptive halving on RESOURCE_LIMITS_EXCEEDED (floor 5) · T09 live dry run: 50-node pages with `mentionableUsers` exceed GitHub's resource limit · drop the contributor proxy field · fewer repos per call (12 points for 50 repos is still far under budget).
- 07 November 2026 · Live-response fixtures for the four adapters are captured in request 2, not T001 · B4 audit F1; needs network capture plus test wiring · capture now without tests · request 2 brief carries it.
- 07 November 2026 · Request 2 is a GitHub-hosted MVP site (Jinja2, GitHub Pages, built-in token) before the quality layers · Po wants to see and use the product before scaling · keep labeller first · labeller 3, sandbox 4, trust and weights v1 5, Astro and Cloudflare 6.

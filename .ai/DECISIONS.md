# Decisions

Format: date · decision · context · alternatives · consequences

- 07 November 2026 · Phase 1 is built through the dual_dev workflow (Claude plans and audits, Codex executes) · Po's instruction after phase 0 · single-agent build · every build item is one `/dual_dev` request; see `docs/dual_dev_requests.md`.
- 07 November 2026 · First niche is the coding-agent stack (coding agents, skills and rules packs, MCP servers) · phase 0 gap table and growth evidence, `reports/AI repo gateway competitor landscape.md` · all ten topics at once · ingestion and sandbox tests scoped to the niche first.
- 07 November 2026 · Rank by a trust score, never by raw stars · own data: Spearman 0.08 between stars and run-readiness on 100 repos; fake-star literature · star velocity ranking · scoring defined in `docs/phase1_architecture_and_operations.md` section 1.
- 07 November 2026 · No "tested" badge without a dated sandbox run · every competitor's "verified" meant paid placement or publisher identity · README-signal proxies · nightly sandbox job, request 3.
- 07 November 2026 · Batch pipeline plus static site, no servers · solo maintainer, free tiers · API back end · GitHub Actions every 6 hours, Cloudflare Pages.
- 07 November 2026 · GitHub account `PoNienC` for this project · personal project · work account `PoNienChenPP` · recorded in `.ai/PROJECT.md`.

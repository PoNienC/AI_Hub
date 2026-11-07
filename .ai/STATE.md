# State — 07 November 2026

- Branch: `dual_dev_setup` (stacked on an unborn `main`; no commits yet).
- Last commit: none.
- Work in flight: dual_dev setup (this branch). Phase 1 request 1 (ingestion pipeline) is next, from `docs/dual_dev_requests.md`.
- Other branches touching AGENTS.md or CLAUDE.md: none (fresh repository).
- Codex probes passed 07 November 2026 (read: 95 s, 12,387 tokens; write: 7,819 tokens; weekly limit 21 per cent used).
- Known issues: labels in `data/labelled_repos_for_review.csv` are unreviewed LLM candidates; no repo has been executed; `data/readmes/` is ignored and must be re-fetched with `scripts/sample_and_fetch.py`.
- Owner actions pending: review the 100 labels into `data/gold_labels.csv` before request 2; domain, Cloudflare account and four GitHub secrets before request 5.

## Sources
- Repository contents on 07 November 2026; `docs/phase1_architecture_and_operations.md` section 6.
- Root `HANDOVER.md` (personal, ignored): the approval of phase 1 and the niche on 07 November 2026, and the pending-actions list.

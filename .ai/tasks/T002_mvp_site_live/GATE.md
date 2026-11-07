# Gate — plan and execution in one stop: T002_mvp_site_live MVP site and live schedule

- Date: 07 November 2026 · Codex: model gpt-6-astra, effort xhigh · [what the options mean](C:\Users\po.nienchen\.claude\skills\dual_dev\templates\gate2_standing_options.md)
- Plans: [PLAN_A.md](PLAN_A.md) (Claude) · [PLAN_B.md](PLAN_B.md) (Codex) · provisional [PLAN_APPROVED.md](PLAN_APPROVED.md)
- Decisions (07 November 2026): plan **C Hybrid** ("C Hybrid (Recommended)") · preset confirmed ("Confirm (Recommended)": Codex T01-T03 one block, Claude T04 and audits, per_block with overlap, ask_high, xhigh) · close-out **automatic** ("Yes, automatic (Recommended)") · visibility: make the repo public at go-live ("Make public at go-live (Recommended)")

## In short

- **Both deliver:** a Jinja2 generator under `pipeline/site/`, a `pipeline site build` command, a light gate 5 (links, page size), `refresh.yml` extended to deploy to GitHub Pages with the built-in token, README and runbook updates, and a local 20-repo acceptance run.
- **Biggest difference:** Codex builds into a staging folder and replaces `site/dist/` only after validation, routes repo pages by stable GitHub id, and flags that GitHub Pages on a private repository needs a paid plan. Claude's plan is leaner but missed all three. Codex better.
- **Recommendation:** **C hybrid** — Claude's four-task shape with Codex's staging, id routes, status fields and the Pages eligibility question folded in.
- **Preset:** Codex executes T01 to T03 as one block, Claude executes T04 (the local acceptance run, needs the network and this machine's token) and audits the block; `per_block` with overlap; review `ask_high`; standing effort xhigh.
- **Close-out:** automatic once every audit is closed, when no BLOCKER or HIGH stands, the tests and checks pass and you send no review notes. Merge, default-branch change and the first live dispatch stay separate owner approvals.

## Key differences

1. **Safe replacement of the built site** — Codex stages and validates before replacing `site/dist/`; Claude wrote straight to it. Codex better; taken.
2. **Repo page routes** — Codex keys them by GitHub id (rename-safe); Claude by name. Codex better; taken.
3. **Private repo and Pages** — only Codex raised that Pages on a private repo needs GitHub Pro; the account plan could not be read by API. Decision for you below.
4. **Where gate 5 runs** — Codex keeps site publication outside `run_pipeline()`; Claude runs gate 5 inside the run so one failure path and one issue cover everything. Claude's taken: a site that fails to build blocks promotion and deploy, matching "six gates before any deploy".
5. **Task count** — Codex six tasks (separate dependency and doc tasks); Claude four. Four kept, with Codex's doc corrections and dependency audit folded into T01 and T03.
6. **Status.json honesty** — Codex: browser-side data age, no claim about consecutive failures. Taken.

## Recommended tasks

| # | Title | Source | Depends on | Risk |
|---|---|---|---|---|
| T01 | Site generator, templates, dependencies, id routes, staged output, status.json | both | — | medium |
| T02 | Light gate 5, `site build` CLI, gate wired into `pipeline run`, atomic replace, tests | both | T01 | medium |
| T03 | Workflow with Pages deploy on the built-in token, verified pins, README "Live site", runbook (token limits, visibility, go-live, rollback), doc reference fixes | both | T02 | medium |
| T04 | Local acceptance: dry run 20 repos, site build, open in the browser, record counts | A | T03 | low |

## Open questions for you

- **Repository visibility for Pages.** GitHub Pages on a private repository needs GitHub Pro or better; on a free account the repo must be public. The site is meant to be public anyway and the code holds no secrets. Recommendation: make `PoNienC/AI_Hub` public at go-live (an owner step at close-out). Alternatives: pay for Pro, or host the MVP on Cloudflare Pages now (brings request 6's account forward).
- Site name and tagline default to "AI_Hub" and "trusted starting points for coding agents"; say if you want others.

## Cost so far

- Codex calls: 1 · tokens: 31,576 · plan limit: 30% used, resets Wednesday 11 November 10:05

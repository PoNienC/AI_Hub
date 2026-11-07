# Tasks — T002_mvp_site_live: MVP site and live schedule

- Branch: `dual_dev/T002_mvp_site_live` · push policy: no push without approval; pushes need the PoNienC gh account active
- Commit format: `T01 <task title> · block: T01-T03 <short title> · fixes: B1 audit fixes (T01-T03)`
- Plan source: hybrid (combined gate, GATE.md)
- Codex: model gpt-6-astra, effort xhigh
- Audit mode: per_block (per_task | per_block | end) · overlap: on (on | off; n/a for per_task and end)
- Audit review: ask_high (auto | ask | ask_high)
- Allocation approved by the user: 07 November 2026
- Hand-off: `8ad1ba6`, 07 November 2026 — see REVIEW.md <!-- pending | `<commit>`, DD Month YYYY — see REVIEW.md -->
- Close-out: done 07 November 2026 (automatic, approved at the combined gate; no review notes received) <!-- ask | automatic (approved at the combined gate) -->
- Running now: none <!-- B2 done; 22:37 → codex/B2_audit_r1_out.md <!-- T04 done; 22:31 <!-- B1 closed; 22:14 → codex/B1_fix_r1_out.md <!-- B1_audit_r1 done; 22:04 → subagent/B1_audit_r1_out.md <!-- B1_exec done; 21:44 → codex/B1_exec_out.md <!-- every background job: step, started HH:MM, output file — e.g. "B1_audit_r1 (Codex) 14:05 → codex/B1_audit_r1_out.md" -->
- Codex tokens so far: 327,251

| Task | Title | Executor | Reviewer | Block | Depends on | Risk | Status | Commit | Audit fix |
|---|---|---|---|---|---|---|---|---|---|
| T01 | Site generator, templates, dependencies | Codex | Claude subagent | B1 | — | medium | Complete | abc99df | 1eee812 |
| T02 | Light gate 5, CLI and wiring | Codex | Claude subagent | B1 | T01 | medium | Complete | abc99df | 1eee812 |
| T03 | Workflow, Pages deploy, docs | Codex | Claude subagent | B1 | T02 | medium | Complete | abc99df | 1eee812 |
| T04 | Local acceptance run | Claude | Codex | B2 | T03 | low | Complete | 8ad1ba6 | record wording, close-out |

Status values: Pending · In progress · Done, audit pending · In audit · Awaiting your review · Corrections · Complete · Blocked
Blocks: consecutive tasks with the same executor, closed after a High-risk task or six tasks (`per_block`); in `end`, each run of consecutive same-executor tasks is one audit point, all audited at the hand-off; each task is its own block in `per_task`.

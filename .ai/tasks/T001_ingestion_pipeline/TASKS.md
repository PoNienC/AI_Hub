# Tasks — T001_ingestion_pipeline: ingestion pipeline and state store

- Branch: `dual_dev/T001_ingestion_pipeline` · push policy: no push without approval (no remote yet)
- Commit format: `T01 <task title> · block: T01-T03 <short title> · fixes: B1 audit fixes (T01-T03)`
- Plan source: hybrid (Gate 1 option C, COMPARISON.md)
- Codex: model gpt-6-astra, effort xhigh
- Audit mode: per_block (per_task | per_block | end) · overlap: on (on | off; n/a for per_task and end)
- Audit review: ask_high (auto | ask | ask_high)
- Allocation approved by the user: 07 November 2026
- Hand-off: pending <!-- pending | `<commit>`, DD Month YYYY — see REVIEW.md -->
- Close-out: ask <!-- ask | automatic (approved at the combined gate) -->
- Running now: T09_fix_r1 (Codex, T03 correction) 16:57 → codex/T09_fix_r1_out.md <!-- T09 dry run failed at ingest, see AUDIT_LOG; 16:53 <!-- B3 closed; 16:44 → codex/B3_fix_r1_out.md <!-- B3_audit_r1 done; 16:32 → subagent/B3_audit_r1_out.md <!-- B3_exec done; 16:11 → codex/B3_exec_out.md <!-- B2 closed; 16:05 → codex/B2_fix_r2_out.md <!-- B2_audit_r2 done; 15:59 → subagent/B2_audit_r2_out.md <!-- B2_fix_r1 done; 15:48 → codex/B2_fix_r1_out.md <!-- B2_audit_r1 done, approved; 12:21 → subagent/B2_audit_r1_out.md <!-- B2_exec done 12:07 → codex/B2_exec_out.md <!-- B1_fix_r1 done 11:59 → codex/B1_fix_r1_out.md <!-- B1_audit_r1 done 11:50 → subagent/B1_audit_r1_out.md <!-- was: B1_exec (Codex) 11:28 → codex/B1_exec_out.md --> <!-- every background job: step, started HH:MM, output file — e.g. "B1_audit_r1 (Codex) 14:05 → codex/B1_audit_r1_out.md" -->
- Codex tokens so far: 667,922

| Task | Title | Executor | Reviewer | Block | Depends on | Risk | Status | Commit | Audit fix |
|---|---|---|---|---|---|---|---|---|---|
|  Package skeleton, models and config | Codex | Claude subagent | B1 | — | low | Pending | Done, audit pending | pending |
|  State store with safe promotion | Codex | Claude subagent | B1 | T01 | medium | Pending | Done, audit pending | pending |
|  GitHub GraphQL source and budgets | Codex | Claude subagent | B1 | T01 | high | Pending | Done, audit pending | pending |
| T04 | Enrichment adapters | Codex | Claude subagent | B2 | T01 | medium | Complete | 4c87086 | 6653b63, b6fcae5 |
| T05 | Scoring and export | Codex | Claude subagent | B2 | T02, T03, T04 | high | Complete | 4c87086 | 6653b63, b6fcae5 |
| T06 | Gates 2 and 3 and abort rule | Codex | Claude subagent | B3 | T05 | low | Complete | 400f780 | a6f4dea |
| T07 | Release round trip and CLI | Codex | Claude subagent | B3 | T02, T06 | medium | Complete | 400f780 | a6f4dea |
| T08 | Workflow, runbook and docs | Codex | Claude subagent | B3 | T07 | low | Complete | 400f780 | a6f4dea |
| T09 | Dry run against 50 repos | Claude | Codex | B4 | T08 | medium | Blocked on T03 fix | — | — |

Status values: Pending · In progress · Done, audit pending · In audit · Awaiting your review · Corrections · Complete · Blocked
Blocks: consecutive tasks with the same executor, closed after a High-risk task or six tasks (`per_block`); in `end`, each run of consecutive same-executor tasks is one audit point, all audited at the hand-off; each task is its own block in `per_task`.

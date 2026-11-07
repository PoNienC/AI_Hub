# Codex brief — read-only audit of T09 (round 1)

Fresh task. You are the reviewer in a dual-agent workflow (see `AGENTS.md`).
Claude Code executed T09. Review them independently and critically.

## Rules

- Read only. Do not modify, create or delete any file. Do not fix anything.
- Review only these changes: range `898b859..4f743c1` (one or more
  commits). The commits, file list and full
  diff are **pasted at the end of this brief** — start there. Run git or
  open files only for extra context, reading them as they are at the end
  of the range (`git show <end>:<path>`); the working tree may already hold
  later work.
- Treat changes under `.ai/` as context, not as code to review.
- Do not run tests: other work may be under way in the working tree, so
  results would not reflect this range. The executor's recorded test
  results (in the handover) are authoritative; a missing test or a
  doubtful result is a finding.

## Context

- Task specs and acceptance criteria: `.ai/tasks/T001_ingestion_pipeline/PLAN_APPROVED.md`, sections T09.
- Executor's handover: `.ai/tasks/T001_ingestion_pipeline/TASK_HANDOVER.md`, sections T09.
- Check each task against its own acceptance criteria, and check that the
  tasks fit together.
- Project conventions: `AGENTS.md`, `.ai/PROJECT.md`.

T09 is a run, not code: Claude executed `uv run pipeline run --dry-run --limit 50` against the live network and recorded the result in `TASK_HANDOVER.md` (section T09, attempts 1 and 2) and `AUDIT_LOG.md` (section "T09 dry-run findings"). Audit the record against the evidence on disk, which you may read: `state/t09_dryrun_attempt2.out` (full run output), `state/logs/*.log`, `site/src/data/listings.dry.json` and `site/src/data/listings.dry.evidence.jsonl`. Check: the acceptance criteria in PLAN_APPROVED.md T09 (under 10 minutes, valid listings, no promotion, no upload); that every number in the handover matches the files; that the scoring observations are fair; and whether the T03 correction (commit 898b859, page size and resource-limit retry) is the right fix for the failure in attempt 1. Do not run the pipeline.

## Check

Correctness against the acceptance criteria; bugs and edge cases; tests
(present, meaningful, passing); error handling; security; performance;
consistency with existing code; scope creep (changes outside the task).

## Output — your final message, Markdown

# Codex audit — T09 (round 1)
## Verdict
PASS, PASS_WITH_FINDINGS or FAIL — one line, plus one line per task.
## Findings
One block per finding, most severe first:
### F<n> [BLOCKER | HIGH | MEDIUM | LOW | NOTE] (T<nn>) short title
- Task: the task ID the finding belongs to (or "cross-task")
- Where: `path:line`
- Problem:
- Why it matters:
- Suggested fix:
Write "None" if there are no findings.
## Checked
What you verified and how (files read, git commands run).

British English. No preamble.

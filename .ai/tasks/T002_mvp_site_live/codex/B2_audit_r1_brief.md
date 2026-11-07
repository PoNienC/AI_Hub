# Codex brief — read-only audit of T04 (round 1)

Fresh task. You are the reviewer in a dual-agent workflow (see `AGENTS.md`).
Claude Code executed T04. Review them independently and critically.

## Rules

- Read only. Do not modify, create or delete any file. Do not fix anything.
- Review only these changes: range `c05608b..8ad1ba6` (one or more
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

- Task specs and acceptance criteria: `.ai/tasks/T002_mvp_site_live/PLAN_APPROVED.md`, sections T04.
- Executor's handover: `.ai/tasks/T002_mvp_site_live/TASK_HANDOVER.md`, sections T04.
- Check each task against its own acceptance criteria, and check that the
  tasks fit together.
- Project conventions: `AGENTS.md`, `.ai/PROJECT.md`.

T04 is a run, not code: Claude executed the 20-repo live dry run, the standalone site build and a browser check, and recorded them in TASK_HANDOVER.md (section T04). Audit the record against the evidence on disk, which you may read: state/t04_dryrun.out, state/logs/*.log, site/src/data/listings.dry.json, site/dist.dry/ (37 HTML files, status.json). Check the T04 acceptance criteria in PLAN_APPROVED.md, that every number in the record matches the files, and whether the built pages honour the standing rules (no star ordering, honest label and tested wording, escaped text, GitHub-only outbound links apart from the allow-listed reference hosts). Do not run the pipeline.

## Check

Correctness against the acceptance criteria; bugs and edge cases; tests
(present, meaningful, passing); error handling; security; performance;
consistency with existing code; scope creep (changes outside the task).

## Output — your final message, Markdown

# Codex audit — T04 (round 1)
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

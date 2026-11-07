# Codex audit — T09 (round 1)

## Verdict

PASS_WITH_FINDINGS — the dry-run acceptance criteria are met; two LOW findings remain.

T09: PASS_WITH_FINDINGS — successful execution, valid gated output, no promotion or upload; reporting precision and deferred fixtures need attention.

## Findings

### F1 [LOW] (T09) Deferred live-response fixtures remain outstanding

- Task: T09, carrying B2/T04 finding F8.
- Where: `.ai/tasks/T001_ingestion_pipeline/TASK_HANDOVER.md:685`; `.ai/tasks/T001_ingestion_pipeline/AUDIT_LOG.md:67`; `tests/test_enrichment.py:37`
- Problem: F8 explicitly deferred recording real adapter responses as fixtures to T09. The reviewed revision still uses synthetic `example/agent` responses. The ignored evidence JSONL records live results, but Hugging Face and Hacker News entries contain transformed outputs rather than replayable upstream responses.
- Why it matters: The successful live observation cannot provide the promised offline regression coverage for actual API shapes.
- Suggested fix: Preserve one sanitised raw response per adapter, including capture metadata, and exercise these through the existing offline adapter tests. Keep F8 outstanding until this is done.

### F2 [LOW] (T09) Saturation count uses inconsistent rounding

- Task: T09.
- Where: `.ai/tasks/T001_ingestion_pipeline/TASK_HANDOVER.md:694`
- Problem: “8 rows at 100.0” does not match the stated precision. No stored total equals 100; **11** round to 100.0 at one decimal place. Eight round to **100.00 at two decimal places**. The maximum is 99.99979943070419.
- Why it matters: Score compression is a fair observation, but the reported saturation count is not reproducible without an explicit rounding rule.
- Suggested fix: State either “11 scores round to 100.0” or “8 scores round to 100.00”, distinguishing rounding from exact saturation.

## Checked

- Read committed context using `git show 4f743c1:<path>`: conventions, approved plan, handover, audit log, decisions, relevant pipeline code and tests. `git diff --name-only 898b859 4f743c1` confirms only three `.ai/` records changed.
- Read `state/t09_dryrun_attempt2.out`, both run logs and both dry-run artefacts. Attempt 2’s logged processing interval is **109.099 seconds**, consistent with the reported **111-second wall time** and comfortably below ten minutes.
- Recalculated **50 unique listings**, **200 evidence records**, **193,503 listing bytes** and **261,717 evidence bytes**. Run identifiers and evidence associations agree.
- Confirmed **12 GraphQL calls**, **12 points**, **zero unmeasured calls**, and **50 calls per enrichment source**. Present/absent counts match: deps.dev **40/10**, Scorecard **2/48**, Hugging Face **15/35**, Hacker News **7/43**; no failures.
- Confirmed coverage **0.25/0.40/0.70** minimum/median/maximum; score median **99.552396…**, minimum **35.793195…**; **39 rows** evaluate only licence, maintenance and contributors. Top-ten overlap with star ordering is **two**. Labels match the committed CSV: **five provisional**, **45 pending**, all **untested**.
- Verified recorded gates passed and inspected their validation path. Production artefacts are absent; committed dry-run control flow bypasses promotion and release transfers.
- The T03 correction is appropriate for the recorded resource-limit failure. Inspected bounded reductions, cursor preservation, partial-data rejection, budget accounting and regression tests. The live rerun confirms the smaller default works; it did not exercise adaptive reductions.
- Accepted the handover’s recorded **454 passing tests**, **98.44% coverage** and clean Ruff result for the unchanged source tree. No tests or pipeline were run, and no files were modified.
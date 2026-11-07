# Codex audit — T04 (round 1)

## Verdict

PASS_WITH_FINDINGS — acceptance criteria are supported; one recorded size is inaccurate.

T04: PASS_WITH_FINDINGS — 20 repository pages, index, gate pass, timing and action pins verified; correct the size record.

## Findings

### F1 [LOW] (T04) Recorded site size does not match the artefacts

- Task: T04
- Where: `.ai/tasks/T002_mvp_site_live/TASK_HANDOVER.md:206`
- Problem: The handover reports **185 KB**. The 37 HTML files total **118,180 bytes**; including `status.json`, the directory totals **118,434 bytes** (115.66 KiB). The largest page is `how_we_grade.html`, at **16,090 bytes**.
- Why it matters: Recording sizes is an explicit T04 deliverable. The recorded total cannot be reconciled with the supplied artefacts, although all pages remain comfortably below the size limit.
- Suggested fix: Correct the total and specify whether it includes `status.json`, using explicit bytes or KiB.

## Checked

- Read the approved plan, handover, project conventions and relevant implementation using `git show 8ad1ba6:<path>`. Git diff/stat confirmed that the reviewed range changes only `.ai/` records.
- Matched `state/t04_dryrun.out`, the corresponding run log, listings and page metadata to run `a2a38755c6774cad98dbe14e2630b7f0`. Confirmed 20 inputs/outputs, six GitHub points and 20 calls per enrichment source.
- The log spans **49.654 seconds**, consistent with the reported 51-second command duration including overhead. The standalone build’s approximately two-second duration is recorded in the handover.
- Inspected all **37 HTML pages and `status.json`**: 20 repository pages, 15 topic pages, index and grading page. Internal links resolve with exact casing; outbound destinations satisfy the GitHub/reference-host allow-list.
- Compared pages against listings: topic order preserves exported ranking; index selections match the top ten per topic; labels, coverage, component statuses and `untested` wording agree with the data. Special-character text is escaped.
- Confirmed the pipeline log records passing gates. The standalone rebuild leaves only `listings_schema` in `status.json`, consistent with the committed builder.
- Independently matched both workflow SHAs through the official release pages: [upload-pages-artifact v3.0.1](https://github.com/actions/upload-pages-artifact/releases/tag/v3.0.1) and [deploy-pages v4.0.5](https://github.com/actions/deploy-pages/releases/tag/v4.0.5).
- Relied on the authoritative recorded **535 passing tests, 98.34% coverage and clean ruff** for unchanged application code. The separate `REVIEW.md` referenced by T04 is absent at this commit. Browser acceptance was assessed from the handover and generated markup.
- No files modified; no tests, pipeline, build or gate commands run.
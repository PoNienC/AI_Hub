# Codex handover — T01, T02, T03

## T01 — Site generator, templates, dependencies

### Summary

Added 200-row topic pagination, corrected index filtering and presentation, preserved approved policy links, and made backup clean-up failures non-fatal.

### Files changed

- [builder.py](C:/Users/po.nienchen/repos/AI_Hub/pipeline/site/builder.py), [links.py](C:/Users/po.nienchen/repos/AI_Hub/pipeline/site/links.py), [.gitignore](C:/Users/po.nienchen/repos/AI_Hub/.gitignore), [test_site.py](C:/Users/po.nienchen/repos/AI_Hub/tests/test_site.py).
- Templates: `base.html`, `index.html`, `repo.html`, `topic.html`; added `label.html`.

### Tests and checks run

All pytest runs used `PYTEST_DEBUG_TEMPROOT=_build/pytest`. uv used the worktree `.venv`, frozen dependencies and cache/Python directories under `_build`.

- `.venv\Scripts\python -m pytest tests/test_site.py` — 61 passed, 0 failed.
- `uv run pytest --cov=pipeline --cov-fail-under=80` — 527 passed, 0 failed; 98.33% coverage.
- `uv run ruff check .` — passed, 0 findings.

No type-check command configured.

### Finding resolutions

- **F2 — ACCEPTED:** Unbounded topics could block publication; added pagination and a 1,500-row regression test.
- **F3 — ACCEPTED:** Backup deletion could fail after publication; enabled tolerant clean-up, logged retained backups and ignored temporary site directories.
- **F6 — PARTIALLY_ACCEPTED:** Added acronym-aware names and all five requested HTTPS reference hosts in the renderer and gate 5; documented the editable-install assumption without changing packaging.
- **C1 — ACCEPTED:** Empty topics obscured useful entries; index now shows populated topics for the selected level, preserves exported order, puts Pending last and provides one empty state.
- **C2 — ACCEPTED:** Repeated pending labels were unclear; rows now show “level not yet labelled” or “level (provisional)”.
- **C3 — ACCEPTED:** Removed the duplicated index title.
- **C4 — ACCEPTED:** Added English UTC display dates; retained ISO timestamps in `status.json`.

### Known gaps and risks

Locked backups can remain on disk with a warning. Browser acceptance remains for T04.

## T02 — Light gate 5, CLI and wiring

### Summary

Made internal link checks case-sensitive across platforms and verified that independent gate checks preserve recorded build status.

### Files changed

[links.py](C:/Users/po.nienchen/repos/AI_Hub/pipeline/site/links.py), [test_gates.py](C:/Users/po.nienchen/repos/AI_Hub/tests/test_gates.py), [test_cli.py](C:/Users/po.nienchen/repos/AI_Hub/tests/test_cli.py).

### Tests and checks run

- `.venv\Scripts\python -m pytest tests/test_gates.py tests/test_cli.py tests/test_site.py` — 150 passed, 0 failed.
- `uv run pytest --cov=pipeline --cov-fail-under=80` — 535 passed, 0 failed; 98.34% coverage.
- `uv run ruff check .` — passed, 0 findings.

No type-check command configured.

### Finding resolutions

- **F1 — ACCEPTED:** Added integration assertions that completed checks survive `pipeline gates`; the redundant workflow rebuild is removed in T03.
- **F7 — ACCEPTED:** Windows could hide broken Pages links; gate 5 now compares exact filenames and directory casing, with regression coverage.

### Known gaps and risks

No outstanding T02 correction identified. Tests used offline clients.

## T03 — Workflow, Pages deploy, docs

### Summary

Removed the redundant rebuild while retaining independent gates before Pages upload. Aligned documentation and restored architecture targets with explicit current-state notes.

### Files changed

[refresh.yml](C:/Users/po.nienchen/repos/AI_Hub/.github/workflows/refresh.yml), [test_workflow.py](C:/Users/po.nienchen/repos/AI_Hub/tests/test_workflow.py), [README.md](C:/Users/po.nienchen/repos/AI_Hub/README.md), [runbook.md](C:/Users/po.nienchen/repos/AI_Hub/docs/runbook.md), [phase1_architecture_and_operations.md](C:/Users/po.nienchen/repos/AI_Hub/docs/phase1_architecture_and_operations.md).

### Tests and checks run

- `.venv\Scripts\python -m pytest tests/test_workflow.py` — 7 passed, 0 failed.
- `uv run pytest --cov=pipeline --cov-fail-under=80` — 535 passed, 0 failed; 98.34% coverage.
- `uv run ruff check .` — passed, 0 findings.

No type-check command configured. No test or check was blocked.

### Finding resolutions

- **F1 — ACCEPTED:** Rebuilding discarded recorded gates; removed that step and retained `pipeline gates` before upload.
- **F4 — ACCEPTED:** Current implementation details had replaced targets; restored targets with “Current (request 2)” notes.
- **F5 — ACCEPTED:** Aligned README, runbook and architecture descriptions with the corrected workflow.

### Known gaps and risks

Live deployment and T04 acceptance remain outstanding. No staging, commits, branching, pushes or `.ai/` edits were performed.
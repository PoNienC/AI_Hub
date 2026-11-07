# Task handover — T002_mvp_site_live

One section per task or block, appended as work lands.

## B1 (T01-T03) — executor Codex, 07 November 2026

### Codex handover (verbatim)

## T01 — Site generator, templates, dependencies

### Summary

Implemented the static builder, packaged templates, stable ID routes, topic grouping, top-ten index, level filter, grading page and status metadata. Repository text is escaped; export order is preserved. Added dependencies, updated `uv.lock` and synchronised the worktree-local `.venv`.

### Files changed

- `pipeline/site/__init__.py`, `pipeline/site/builder.py`
- `pipeline/site/templates/{base,index,topic,repo,how_we_grade}.html`
- `pyproject.toml`, `uv.lock`
- `tests/test_site.py`, `tests/fixtures/listings_sample.json` — 50 dry-run rows
- `docs/runbook.md`

### Tests and checks run

- `.venv/Scripts/python -m pytest tests/test_site.py -q` — **24 passed**
- `uv run pytest --cov=pipeline --cov-fail-under=80` — **478 passed; 98.39% coverage**
- `uv run ruff check .` — **passed**

No type-check command is configured. Pytest used `PYTEST_DEBUG_TEMPROOT=_build/pytest`.

### Known gaps and risks

Windows requires two directory renames to replace an existing tree. Ordinary failures restore the previous site; abrupt termination between renames is not atomic. `pip-audit` was added to the runbook but not run.

## T02 — Light gate 5, CLI and wiring

### Summary

Added internal-link, HTML-size and topic-navigation checks; credential-free `pipeline site build`; and site generation before promotion. Dry runs produce `site/dist.dry/`. Gate failures retain production files and generate existing failure records and issue text.

Existing public signatures and command arguments remain unchanged.

### Files changed

- `pipeline/site/links.py`
- `pipeline/gates.py`, `pipeline/cli.py`
- `.gitignore`
- `tests/test_gates.py`, `tests/test_cli.py`, `tests/test_site.py`

### Tests and checks run

- `.venv/Scripts/python -m pytest tests/test_gates.py tests/test_cli.py tests/test_site.py -q` — **124 passed**
- `uv run pytest --cov=pipeline --cov-fail-under=80` — **507 passed; 98.30% coverage**
- `uv run ruff check .` — **passed**

No type-check command is configured. Pytest used `PYTEST_DEBUG_TEMPROOT=_build/pytest`.

### Known gaps and risks

Standalone `site build` validates and renders the export; freshness and gate 5 are checked separately. Pipeline runs perform all three gates before promotion.

## T03 — Workflow, Pages deploy, docs

### Summary

Switched CI to the built-in token. Added build/check/upload after release push and a dependent Pages deploy job with job-scoped Pages/OIDC permissions. The failure issue step is unchanged.

Documented preview, owner go-live steps, token limits, visibility and rollback. Corrected obsolete request numbers and frontend references.

Intended action pins:

- `upload-pages-artifact` [v3.0.1](https://github.com/actions/upload-pages-artifact/releases/tag/v3.0.1): `56afc609e74202658d3ffba0e8f6dda462b719fa`
- `deploy-pages` [v4.0.5](https://github.com/actions/deploy-pages/releases/tag/v4.0.5): `d6db90164ac5ed86f2b6aed7e0febac5b3c0c03e`

### Files changed

- `.github/workflows/refresh.yml`
- `README.md`
- `docs/runbook.md`, `docs/scoring.md`, `docs/phase1_architecture_and_operations.md`
- `tests/test_workflow.py`

### Tests and checks run

- `.venv/Scripts/python -m pytest tests/test_workflow.py -q` — **7 passed**
- `uv run pytest --cov=pipeline --cov-fail-under=80` — **509 passed; 98.30% coverage**
- `uv run ruff check .` — **passed**

No type-check command is configured. Pytest used `PYTEST_DEBUG_TEMPROOT=_build/pytest`.

### Known gaps and risks

T04’s live run, browser acceptance and independent pin verification remain with Claude. Deployment and built-in-token API access have not been exercised in GitHub Actions. Deploy-job failures appear in Actions but cannot trigger the earlier refresh-job issue step.

No files were staged or committed; no branch, push, history or `.ai/` changes were made.

### Coordinator checks (Claude)
- `git status`: new pipeline/site/ (builder, links, templates), tests/test_site.py, tests/fixtures/listings_sample.json; modified cli.py, gates.py, refresh.yml, README, runbook, scoring, architecture doc, pyproject, uv.lock, .gitignore, three test modules. No unexpected changes.
- `uv run pytest --cov=pipeline --cov-fail-under=80`: 509 passed, coverage 98.30%.
- `uv run ruff check .`: clean.
- Pins: actions/deploy-pages d6db9016… = tag v4 (verified live earlier); actions/upload-pages-artifact 56afc609… checked against tag v3.0.1 → 56afc609e74202658d3ffba0e8f6dda462b719fa.
- Codex run: 1,040 s, 110,800 tokens, weekly limit 31% used.

### B1 corrections round 1 — executor Codex, 07 November 2026

#### Codex handover (verbatim)

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

#### Coordinator checks (Claude)
- `uv run pytest --cov=pipeline --cov-fail-under=80`: 535 passed, coverage 98.34%.
- `uv run ruff check .`: clean.
- Codex run: 860 s, 93,193 tokens, weekly limit 33% used.

## T04 — Local acceptance run (Claude), 07 November 2026

### Summary
- `uv run pipeline run --dry-run --limit 20` with the real network: exit 0, 51 s, 20 in / 20 out, 6 GitHub points, 20 calls per enrichment source, gates passed; the run itself built `site/dist.dry/` with gates 2, 3 and 5 recorded.
- `uv run pipeline site build --input site/src/data/listings.dry.json --output site/dist.dry` rebuilt it standalone: 37 HTML pages (index, how_we_grade, 15 topic pages, 20 repo pages), 118,180 bytes of HTML (118,434 bytes with status.json; `du -sh` had reported 185K of allocated disk), largest page how_we_grade.html at 16,090 bytes. `uv run pipeline gates --path site/src/data/listings.dry.json`: gates 2, 3 and 5 passed.
- Browser check (http://localhost:8766/index.html, the `site_preview` launch entry): only populated topics shown ("Coding agent" with two provisional-beginner rows, "Pending" last); rows read "beginner (provisional)" or "level not yet labelled"; title "AI Hub"; repo links route by GitHub id; level filter present. No rendering defect seen.
- Pins verified live with `gh api`: actions/upload-pages-artifact 56afc609e74202658d3ffba0e8f6dda462b719fa = v3.0.1; actions/deploy-pages d6db90164ac5ed86f2b6aed7e0febac5b3c0c03e = v4 (v4.0.5).

### Acceptance
- At least 20 repo pages: 20. Index present. Gate 5 passed. Under 5 minutes: 51 s run plus about 2 s build. Pins verified.
- Full suite and ruff on the final tree: run at hand-off, see REVIEW.md.

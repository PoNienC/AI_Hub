# Codex handover — T01, T02, T03

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
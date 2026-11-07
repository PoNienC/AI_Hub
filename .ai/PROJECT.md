# AI_Hub — project facts for both agents

## Purpose
A gateway that groups trending AI GitHub repositories, agent skills and MCP servers by user skill level and topic for vibe coders, with sandbox run tests and security screening. Phase 0 (research and gap test) done 07 November 2026; phase 1 (build) approved the same day. Source: `reports/AI repo gateway competitor landscape.md`, `docs/phase1_architecture_and_operations.md`.

## Stack and versions
- Python 3.13.13 (installed); package manager uv (to be added in request 1). Source: `scripts/*.py`, `docs/phase1_architecture_and_operations.md` section 1.
- Front end: Astro static site with Tailwind, Cloudflare Pages (request 5). Not yet present.
- GitHub CLI `gh` authenticated; Codex CLI 0.160.1 logged in (07 November 2026).
- Data: SQLite state store `state/gateway.sqlite` kept as a GitHub Release asset, never committed (planned). CSVs under `data/` are committed; `data/readmes/` is ignored and re-fetchable.

## Top-level layout (07 November 2026)
- `data/` — phase 0 CSVs (965 candidate repos; 100-repo labelled review set) and ignored READMEs.
- `docs/` — `phase1_architecture_and_operations.md` (target architecture, update schedule, six test gates, deploy, runbook outline) and `dual_dev_requests.md` (five requests to run in order).
- `reports/` — phase 0 report and the ambition brief.
- `research_notes/` — nine research notes with URLs on every claim.
- `scripts/` — `pull_candidate_repos.py`, `sample_and_fetch.py` (need `gh`).
- Planned by the requests: `pipeline/`, `tests/`, `site/`, `.github/workflows/`, `state/` (ignored).

## Setup steps
- `gh auth login` (public read is enough). Python 3.13. Request 1 adds uv; install with `uv sync --frozen` into a worktree-local `.venv` (Codex's sandbox convention, noted in the init probe on 07 November 2026).

## Test and lint commands
- TBC until request 1: planned `uv run pytest` (coverage 80 per cent or better), `ruff check .`, pydantic schema gate on `site/src/data/*.json`. Source: `docs/phase1_architecture_and_operations.md` section 3.

## Coding conventions
- From the user's global rules (`~/.claude/rules/python.md`): type hints on public functions; module docstring per file; pathlib not os.path; logging not print; no bare `except Exception` unless re-raised; British English in docstrings, comments and user strings.
- Names snake_case with underscores (files, folders, branches). The word "claude" never appears in any name, branch, commit or identifier. No AI credit lines in commits.
- Never rank by raw stars; never mark anything "tested" without a dated sandbox run. Source: `docs/phase1_architecture_and_operations.md`.

## Key documents
- `docs/phase1_architecture_and_operations.md` — the target for every request.
- `docs/dual_dev_requests.md` — the five requests, in order.
- `reports/AI repo gateway competitor landscape.md` — why the project exists.
- `data/labelled_repos_for_review.csv` — becomes `data/gold_labels.csv` after Po's review (due before request 2).

## Git conventions (used by /dual_dev)
- Main branch: `main` (created 07 November 2026, no commits yet at setup time). Source: `git init -b main`.
- Request branch pattern: `dual_dev/T001_slug` (default; no project pattern existed).
- Commit format: `T01 <task title>` (default). Setup commit: `Set up dual-agent workflow (AGENTS.md contract, .ai shared state)`.
- Push policy: no push without the user's explicit approval. Commit only what the user ordered or approved (user's global rules).
- Pull requests: not yet required (solo project, no remote). When a remote exists, request branches merge to `main` through a pull request reviewed by the user.
- GitHub account for this remote: `PoNienC` (personal; decided by Po, 07 November 2026). The GitHub CLI also holds `PoNienChenPP` (work); switch with `gh auth switch -u PoNienC` only after telling the user. Remote `origin` = https://github.com/PoNienC/AI_Hub (private, created 07 November 2026).
- Codex execution on this machine (PRIORPLAP180): available (07 November 2026). Read probe: exit 0, write to repo blocked. Write probe in a throwaway repo: exit 0, file created. Model default gpt-6-astra.

# AI Hub

AI Hub builds a gateway for discovering AI repositories, agent skills and MCP
servers by topic and user skill level. This first pipeline ingests GitHub
metadata, records independent evidence, calculates a versioned score and exports
validated listings. Scores reflect evaluated evidence and visible coverage;
raw stars never affect ranking. All entries remain `untested`, and CSV labels
are provisional until human review and the later labelling workflow.

## Run

Use Python 3.13, uv and GitHub CLI from the repository root. Follow the
[local environment and token setup](docs/runbook.md#run-locally), then:

```powershell
uv sync --frozen
uv run pipeline run --dry-run --limit 5
uv run pipeline gates --path site/src/data/listings.dry.json
```

Dry runs use live source APIs, temporary state and separate
`listings.dry.json` / `listings.dry.evidence.jsonl` outputs. The production command
pulls state, ingests, enriches, scores, exports, gates, promotes and uploads:

```powershell
uv run pipeline run
```

For explicitly managed transfers (also used in CI):

```powershell
uv run pipeline release pull
uv run pipeline run --no-release
uv run pipeline release push
uv run pipeline gates
```

`--limit N` caps enriched repositories; `--all-queries` expands beyond the default
six-query niche. Both are optional flags on `pipeline run`. Configure paths,
budgets and source options through `AI_HUB_*` environment variables. The default
canonical state is `state/gateway.sqlite`; the `data-latest` release carries that
database and `evidence.jsonl`. Full evidence stays outside the production site
data. Gate or budget failures retain the last good files and append diagnostics
to `state/failures.jsonl`.

## Checks

After creating `_build/pytest` and setting `PYTEST_DEBUG_TEMPROOT` as described
in the runbook:

```powershell
uv run pytest --cov=pipeline --cov-fail-under=80
uv run ruff check .
```

Tests use local fixtures and injected clients, including a fake `gh` executable;
they never call live APIs. No separate type-check command is configured.

## Layout

| Path | Purpose |
|---|---|
| `pipeline/` | Sources, budgets, state store, scoring, export, gates and CLI |
| `tests/` | Offline unit and integration tests, recorded JSON and fake CLI fixtures |
| `data/` | Candidate repositories and provisional label CSVs |
| `state/` | Ignored SQLite state, full evidence and run/failure diagnostics |
| `site/src/data/` | Generated listings; the frontend is a later request |
| `.github/workflows/refresh.yml` | Six-hourly/manual gated refresh and failure reporting |
| `.github/dependabot.yml` | Weekly uv and GitHub Actions dependency updates |
| `docs/` | Architecture, scoring policy and operational runbook |
| `.ai/` | Shared dual-agent plans and handovers |

Read the [scoring policy](docs/scoring.md) for weights, evidence limits and
unevaluated checks, and the [runbook](docs/runbook.md) for setup, failures and
rollback. Labelling, sandbox runs, the trust layer and static-site deployment
arrive in subsequent requests.

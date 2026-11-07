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
`listings.dry.json` / `listings.dry.evidence.jsonl` outputs, with static pages in
`site/dist.dry/`. The production command pulls state, ingests, enriches, scores,
exports, builds the site, gates, promotes and uploads:

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

## Live site

The production URL after go-live is [AI Hub](https://ponienc.github.io/AI_Hub/).
The current site uses Jinja2 templates and a small level filter; repository
routes use stable GitHub IDs. Data age is calculated in the browser. Labels and
test statuses remain explicit, and scores preserve the exported order.

Preview the bundled 50-row sample locally without credentials or source APIs:

```powershell
uv run pipeline site build --input tests/fixtures/listings_sample.json --output site/dist.dry
uv run python -m http.server 8000 --bind 127.0.0.1 --directory site/dist.dry
```

Open `http://127.0.0.1:8000/`. To preview a live dry run, substitute
`site/src/data/listings.dry.json` for the sample input. The default
`uv run pipeline site build` reads `site/src/data/listings.json` and replaces
`site/dist/`; it needs an existing export but no credentials or state store.

Owner go-live steps, after review:

1. Merge the approved request branch into `main` and make `main` the default
   branch, so the scheduled workflow can run there.
2. Make the repository public at go-live, as agreed. GitHub Free requires a
   public repository for Pages; private-repository Pages requires an eligible
   paid plan. A private repository alone does not make the website private.
   See the [Pages visibility entry](docs/runbook.md#pages-visibility).
3. In **Settings → Pages → Build and deployment**, select **GitHub Actions**
   as the source. Check that the `github-pages` environment permits `main`.
4. In **Actions → Refresh repository data → Run workflow**, select `main` for
   the first dispatch. Confirm both `refresh` and `deploy` succeed and open the
   production URL. The existing six-hour schedule then refreshes it.

CI uses the built-in token; no personal token secret is needed. The Pages
upload follows the verified release push and an independent `pipeline gates`
check. It uploads the site already built by `pipeline run`, preserving the
completed checks in `status.json`. Only the deploy job receives Pages/OIDC
write permissions and deploys from `main`.

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
| `pipeline/site/` | Static site builder, packaged templates and light gate 5 |
| `site/src/data/` | Generated listings consumed by the static builder |
| `site/dist/`, `site/dist.dry/` | Ignored production and preview pages |
| `.github/workflows/refresh.yml` | Six-hourly/manual gated refresh, failure reporting and Pages deploy |
| `.github/dependabot.yml` | Weekly uv and GitHub Actions dependency updates |
| `docs/` | Architecture, scoring policy and operational runbook |
| `.ai/` | Shared dual-agent plans and handovers |

Read the [scoring policy](docs/scoring.md) for weights, evidence limits and
unevaluated checks, and the [runbook](docs/runbook.md) for setup, failures and
rollback. Labelling, sandbox runs, the trust layer and a richer frontend arrive
in subsequent requests.

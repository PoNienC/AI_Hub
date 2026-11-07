# Pipeline runbook

The refresh workflow runs at 00:17, 06:17, 12:17 and 18:17 UTC, or through
`workflow_dispatch`. Concurrency group `refresh` queues runs without cancelling
the active writer. Run only one local writer against each state directory too.

## Run locally

Use Python 3.13, uv and GitHub CLI (`gh`) from the repository root. Install into
the worktree's `.venv`; keep uv's cache and managed Python under `_build`.
PowerShell setup:

```powershell
$env:UV_CACHE_DIR = Join-Path $PWD '_build/uv-cache'
$env:UV_PYTHON_INSTALL_DIR = Join-Path $PWD '_build/uv-python'
$env:UV_PROJECT_ENVIRONMENT = Join-Path $PWD '.venv'
$env:UV_FROZEN = 'true'
$env:PYTEST_DEBUG_TEMPROOT = Join-Path $PWD '_build/pytest'
New-Item -ItemType Directory -Path $env:PYTEST_DEBUG_TEMPROOT -Force | Out-Null
uv sync --frozen
```

Export `GH_TOKEN` securely into the shell; never put its value in a command
example, committed file or issue. The GraphQL source needs it even if `gh` is
already authenticated. A local token needs public metadata access and, for
release transfers, contents write access to this repository. On GitHub Actions,
`GH_TOKEN` is supplied by `${{ github.token }}` and `GH_REPO` by
`${{ github.repository }}`. No personal token secret is read by the workflow.
The refresh job has contents/issue write permissions; Pages and OIDC write
permissions are granted only to the deploy job.

```powershell
uv run pytest --cov=pipeline --cov-fail-under=80
uv run ruff check .
uv run pip-audit
uv run pipeline run --dry-run --limit 5
uv run pipeline gates --path site/src/data/listings.dry.json
```

The dry-run command still calls source APIs and uses their budgets. It skips
release transfers, copies any existing local history into temporary state, and
discards that state afterwards. Its data outputs are
`site/src/data/listings.dry.json` and
`site/src/data/listings.dry.evidence.jsonl`, with the generated site in
`site/dist.dry/`; all are ignored by Git, as are other
`site/src/data/*.evidence.jsonl` files. It never changes `site/dist/`, production listings,
`state/gateway.sqlite` or `state/evidence.jsonl`. Logs and failure records are
still retained under `state/`. Unit tests inject fixture clients and need no
network. A limited dry run against a larger local baseline can fail the 90%
count gate; use a separate `AI_HUB_STATE_DIR` for a fresh sample baseline.

Production, including the release round trip:

```powershell
uv run pipeline run
uv run pipeline gates
```

The equivalent split used in CI is:

```powershell
uv run pipeline release pull
uv run pipeline run --no-release
uv run pipeline release push
uv run pipeline gates
```

`--no-release` publishes locally and skips both transfers, preventing duplicate
pulls/uploads in the workflow. `--all-queries` selects all configured searches;
the default is the six-query coding-agent niche. `--limit N` caps the number of
unique repositories enriched and bounds each query's search cap to N (or the
configured per-query cap if smaller). It does not guarantee N unique results.
`Settings` accepts `AI_HUB_*` overrides, including `AI_HUB_STATE_DIR`,
`AI_HUB_GITHUB_POINT_LIMIT` and JSON `AI_HUB_HTTP_CALL_LIMITS`.

## State, gates and failure records

`data-latest` is the release tag; its assets are `gateway.sqlite` and
`evidence.jsonl`. An absent release starts fresh; authentication errors, network
errors, missing assets, invalid SQLite and mismatched evidence fail the transfer.
The absent-release diagnostic `release not found` was verified with gh 2.92.0 on
7 November 2026; matching also tolerates case, spacing and a punctuation-led
suffix. Before enabling the schedule, manually run `uv run pipeline release pull`
once in the intended repository to confirm first-run detection and authentication.
Downloads are staged under `state/` and validated before replacing local files.
The first push creates the release; later pushes replace the two assets and
verify their reported sizes. The repository must allow mutable release assets.
Uploads and downloads allow 600 seconds per command by default; set
`AI_HUB_RELEASE_TIMEOUT_SECONDS` to a positive integer to change this limit.
Metadata and release-creation commands retain their 60-second timeout.

The run stages compact listings, full evidence and the generated site, evaluates
gates 2 and 3 on the exported file and gate 5 on the staged site, then promotes.
Gate 5 requires every internal href/src to resolve to a file inside the site,
HTML pages no larger than 200,000 bytes and at least one topic link on the index.
The builder loads only listings and the scoring policy, never SQLite. It builds
beside its destination and swaps the complete directory, restoring the previous
site if an ordinary publication error occurs. Directory renames are individually
atomic; replacing an existing tree on Windows requires two renames, so abrupt
process termination between them is not a filesystem transaction.
Gate 2 uses `pipeline.export.Listings` and
its `PublishedListing` rows, including coverage. Gate 3 requires a non-future
timestamp no older than seven hours, at least 90% of the previous successful
count (no count baseline on the first run), score, licence status and `untested`.
Explicit `unknown`/`absent` licence status is allowed; no licence is invented.
`REQUIRE_LABELS` stays false until request 3. No sandbox result exists yet.

`pipeline site build [--input PATH] [--output PATH]` renders an existing export
without settings, credentials or network access; defaults are
`site/src/data/listings.json` and `site/dist/`. It validates the schema but does
not certify freshness or run gate 5. `pipeline gates` checks production data and
`site/dist/`; a `--path` ending in `.dry.json` checks `site/dist.dry/` instead.
For a custom preview directory, call `pipeline.gates.gate_5(Path(...))` directly.
CI uploads the site already built and gated by `pipeline run`. After release
push, an independent `pipeline gates` check re-verifies it before the Pages
upload without rebuilding or changing `status.json`.
`status.json` identifies the export run and lists completed checks;
standalone builds record schema validation only, while `pipeline run` also
records gates 2, 3 and 5. The browser calculates age from `generated_at`.

The successful `run_log` row is finalised in the working SQLite copy immediately
before promotion: the B1 store closes on promotion. It records local gated
success, budgets, timestamps and counts. Upload happens afterwards. An upload
failure therefore leaves a valid local promoted bundle and adds a failure record;
retry `pipeline release push` to upload it without re-ingesting or pulling over it.

Each failed pipeline run appends one JSON line to `state/failures.jsonl`, outside
the rolled-back database: run ID, started/finished times, failing gate/budget or
stage, reason, row counts, previous count, budgets and log path. The CLI renders
`state/failure-title.txt` and `state/failure-body.md` from that same record. The
workflow adds its Actions log URL and opens a `pipeline-failure` issue. A failure
before the CLI can start uses a workflow diagnostic with unavailable row counts.
These text files describe the latest failure; the JSONL history is append-only.
Detailed logs are `state/logs/<run_id>.log`. Pipeline and standalone release
failures append a DEBUG traceback to that file only; console output, failure
records and issue text retain sanitised diagnostics. The `pipeline gates`
command is read-only, including on failure: it reports to the console without
writing logs, failure history or issue files. Unexpected process termination
may prevent any failure record from being written.

CI retains state, full evidence, listings and diagnostics in a
`refresh-<run_id>-<attempt>` Actions artefact for 14 days, on success or failure.
Failure history is local to each runner/worktree; download the run artefacts to
retain history across ephemeral runners. Full evidence also travels with the
release and never belongs in the site JSON. The Pages artefact contains only
`site/dist/` and is retained for 14 days. Deployment depends on the refresh job
succeeding and runs only on `main`. Build and refresh failures use the existing
failure issue step; deployment-job failures are visible in the Actions run and
`github-pages` environment and do not execute that earlier issue step.

### Built-in token limits

The built-in token's GraphQL allowance is normally 1,000 points per hour per
repository, shared by workflows using that repository's token (enterprise
resources have a higher allowance). This remote limit is separate from the
pipeline's 2,500-point per-run ceiling; the ceiling does not grant additional
GitHub capacity. Inspect remaining allowance, reduce the search/limit or wait
for reset when it is exhausted. See [GitHub's GraphQL limits](https://docs.github.com/en/graphql/overview/rate-limits-and-query-limits-for-the-graphql-api).

The token is scoped to this repository. `GH_REPO` selects this repository's
`data-latest` release; the token cannot write release assets in an unrelated
repository. See [GITHUB_TOKEN scope](https://docs.github.com/en/actions/concepts/security/github_token).

### Pages visibility

GitHub Free supports Pages from public repositories. Private repositories need
an eligible paid plan; private source does not by itself restrict access to the
published site. The agreed go-live route is to make `PoNienC/AI_Hub` public,
choose **GitHub Actions** as the Pages source, and dispatch from the default
`main` branch. These are owner actions, not performed by this implementation.
See [Pages availability](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages)
and [Pages access control](https://docs.github.com/en/pages/getting-started-with-github-pages/changing-the-visibility-of-your-github-pages-site).

### Site rollback

Pause competing refreshes, select the last green workflow run in Actions, and
re-run its **deploy job only** while its `github-pages` artefact remains available
(14-day retention). This reuses the retained site without re-ingesting or
changing the release state. Re-running all jobs performs a fresh ingestion and
is not an exact site rollback. If the artefact has expired, recover `site/dist/`
from a retained green diagnostic artefact or rebuild that run's matching listings
and code, then arrange a reviewed deployment. Do not redeploy mismatched runs.

## Incident entries

### GitHub API rate limit or schema change

- **Symptom:** ingestion aborts, a budget or GitHub query is named in the failure
  record, or gate 2 rejects the exported schema.
- **Cause:** exhausted remote allowance, per-run GitHub/HTTP budget, changed API
  response fields or invalid source data.
- **Fix:** inspect the named query/gate and run log, plus recorded budget counters.
  Wait for the remote allowance to reset or reduce `--limit` / per-query caps.
  For schema drift, reproduce with a sanitised fixture, correct the adapter/query,
  run the project checks and retry. Do not bypass gates or silently increase the
  budget. A failed run must leave the previous good production files intact.

### GitHub resource limit

- **Symptom:** ingestion logs `RESOURCE_LIMITS_EXCEEDED` and page-size reductions,
  or aborts with a GitHub query resource-limit error even though points remain.
- **Cause:** large GraphQL pages with expensive fields such as `mentionableUsers`
  exceed GitHub's per-query resources. The 7 November 2026 probes failed at 50
  nodes and succeeded at 25 for the affected queries.
- **Fix:** use `AI_HUB_GITHUB_PAGE_SIZE` (default 25, allowed range 5–100) to set
  the initial page size. A response containing only `RESOURCE_LIMITS_EXCEEDED`
  errors is discarded, the requested size is halved (rounded down, floor 5),
  and the same cursor is retried. Each reduction is logged and retained for the
  rest of that query; every attempt consumes HTTP and GraphQL budget. The
  per-query cap and `--limit` still bound totals and may request fewer than five
  remaining nodes. A resource error at five or fewer nodes, a mixed-error page
  or any other GraphQL error fails closed. If failures persist at the floor,
  inspect the named query and reproduce with a sanitised fixture before changing
  its fields; run the project checks and retry. Do not bypass errors or budgets.

### BigQuery quota exceeded — from request 5

- **Symptom:** the future GH Archive job reports a scanned-byte or quota error.
- **Cause:** the selected archive window exceeds its allowance.
- **Fix:** reduce the GH Archive window to seven days and retry within budget.
  BigQuery is not called by the current pipeline; this entry becomes operational
  when request 5 adds it.

### Labeller API error or drift — from request 3

- **Symptom:** the future labeller fails or gate 4 agreement drops below its
  approved gold-set thresholds.
- **Cause:** API failure, changed model behaviour or a prompt/label mismatch.
- **Fix:** inspect the disagreeing rows with Po and the API diagnostics. Preserve
  the last approved labels, correct the cause and rerun the approved labeller
  gate. The current CSV labels are provisional and gate 4 is not implemented.
  Any future degraded-publishing policy must be explicit in request 3.

### Sandbox timeout — from request 4

- **Symptom:** future sandbox runs time out for many repositories.
- **Cause:** an unsuitable runner image, infrastructure failure or the time cap.
- **Fix:** inspect the runner image and time limits, correct the environment and
  retry. Keep affected entries `untested` until there is a dated sandbox result;
  infrastructure timeouts must not become a fabricated functional failure. The
  current pipeline does not execute repository code.

### Stale working copy

- **Symptom:** `pipeline run` exits with `Working copy already exists`, naming
  `state/gateway.work.sqlite` and a removal command, without a traceback.
- **Cause:** an interrupted process left its working database behind, or another
  local pipeline is still running.
- **Fix:** confirm that no writer is running. Inspect or copy the working file
  if diagnostics are needed. To discard the default working copy in PowerShell:
  `Remove-Item -LiteralPath 'state/gateway.work.sqlite'`. On Linux use
  `rm -- state/gateway.work.sqlite`. For a custom state directory use the exact
  path printed by the CLI. Remove only the working copy; retain the canonical
  database. Retry the run. Never remove another live process's working copy.

### Interrupted publication or release upload

- **Symptom:** a local publication error, missing/size-mismatched release asset,
  or database/evidence run-ID mismatch after interruption.
- **Cause:** process termination, disk/permission problems or an interrupted
  upload. Local files are atomic individually; a bundle is not one filesystem
  transaction. Ordinary replacement errors restore earlier local files, but a
  killed process can interrupt that restoration.
- **Fix:** preserve the failed run's artefact. If its local bundle is complete
  and gated, retry `uv run pipeline release push`; do not pull first. Otherwise
  restore a matching good database/evidence pair as below. Inspect failed checks
  before running again. GitHub CLI
  [`--clobber` deletes the old asset before uploading its replacement](https://cli.github.com/manual/gh_release_upload),
  so remote replacement is not atomic and a failed upload may lose an old asset.

## Roll back

Stop active refresh/local writers before restoring. Download a previous green
run's retained Actions artefact into a separate directory. Preserve the current
bundle for diagnosis. Restore its matching `state/gateway.sqlite`,
`state/evidence.jsonl` and `site/src/data/listings.json` into this worktree; never
mix runs. Do not restore `gateway.work.sqlite`. Run
`uv run pipeline release push` to replace the release with the restored gated
pair, without re-ingestion or a preceding pull. It verifies integrity, recorded
gates, evidence run IDs and both uploaded sizes.

`uv run pipeline gates` can check a recently restored listing, but an export
older than seven hours correctly fails freshness. Restoring historical state
does not make it fresh: run a normal refresh after resolving the incident.
Re-running all jobs of a green workflow performs a new ingestion, not an exact rollback.
Keep a good artefact beyond the 14-day retention window if longer rollback
history is required. Restore the matching `site/dist/` for a local site rollback;
for the deployed site, follow [Site rollback](#site-rollback).

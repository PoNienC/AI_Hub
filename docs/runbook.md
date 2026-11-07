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
already authenticated. On GitHub Actions the only secret read is `GH_TOKEN`.
It must have read access to public repository metadata and contents write /
issues write access to this repository for releases and failure issues. Workflow
`permissions` do not grant additional privileges to a personal token.

```powershell
uv run pytest --cov=pipeline --cov-fail-under=80
uv run ruff check .
uv run pipeline run --dry-run --limit 5
uv run pipeline gates --path site/src/data/listings.dry.json
```

The dry-run command still calls source APIs and uses their budgets. It skips
release transfers, copies any existing local history into temporary state, and
discards that state afterwards. Its only data outputs are
`site/src/data/listings.dry.json` and
`site/src/data/listings.dry.evidence.jsonl`; it never changes production listings,
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
Downloads are staged under `state/` and validated before replacing local files.
The first push creates the release; later pushes replace the two assets and
verify their reported sizes. The repository must allow mutable release assets.

The run stages compact listings and full evidence, evaluates gates 2 and 3 on
the exported file, then promotes. Gate 2 uses `pipeline.export.Listings` and
its `PublishedListing` rows, including coverage. Gate 3 requires a non-future
timestamp no older than seven hours, at least 90% of the previous successful
count (no count baseline on the first run), score, licence status and `untested`.
Explicit `unknown`/`absent` licence status is allowed; no licence is invented.
`REQUIRE_LABELS` stays false until request 2. No sandbox result exists yet.

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
Detailed logs are `state/logs/<run_id>.log`. Unexpected process termination may
prevent any failure record from being written.

CI retains state, full evidence, listings and diagnostics in a
`refresh-<run_id>-<attempt>` Actions artefact for 14 days, on success or failure.
Failure history is local to each runner/worktree; download the run artefacts to
retain history across ephemeral runners. Full evidence also travels with the
release and never belongs in the site JSON. There is no site deploy in this
request; site and later gates arrive in subsequent requests.

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

### BigQuery quota exceeded — from request 4

- **Symptom:** the future GH Archive job reports a scanned-byte or quota error.
- **Cause:** the selected archive window exceeds its allowance.
- **Fix:** reduce the GH Archive window to seven days and retry within budget.
  BigQuery is not called by the current pipeline; this entry becomes operational
  when request 4 adds it.

### Labeller API error or drift — from request 2

- **Symptom:** the future labeller fails or gate 4 agreement drops below its
  approved gold-set thresholds.
- **Cause:** API failure, changed model behaviour or a prompt/label mismatch.
- **Fix:** inspect the disagreeing rows with Po and the API diagnostics. Preserve
  the last approved labels, correct the cause and rerun the approved labeller
  gate. The current CSV labels are provisional and gate 4 is not implemented.
  Any future degraded-publishing policy must be explicit in request 2.

### Sandbox timeout — from request 3

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
Re-running a green workflow performs a new ingestion, not an exact rollback.
Keep a good artefact beyond the 14-day retention window if longer rollback
history is required. Frontend rollback through Cloudflare belongs to request 5.

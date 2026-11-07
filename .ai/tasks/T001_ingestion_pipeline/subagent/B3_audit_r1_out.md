# Claude audit — T06, T07, T08 (round 1)

Reviewer: Claude audit subagent (dual_dev_auditor, session model), 07 November 2026. Range `b6fcae5..400f780`. Saved verbatim by the coordinator.

## Verdict

PASS_WITH_FINDINGS — no blocker; two MEDIUM operational risks in T07, one MEDIUM verification gap in T08, the rest LOW/NOTE.

- T06 (gates 2 and 3, abort rule): PASS — every acceptance line is met and tested.
- T07 (release round trip and CLI): PASS_WITH_FINDINGS — correct by reading and well tested offline; a fixed 60 s `gh` timeout and type-name-only diagnostics for unexpected errors are operational weaknesses; one acceptance test is vacuous.
- T08 (workflow, runbook, docs): PASS_WITH_FINDINGS — YAML, cron, permissions, concurrency, runbook entries and README commands all check out; the three action SHA pins and the uv version cannot be verified offline and will hard-fail the workflow if wrong.

## Findings

### F1 [MEDIUM] (T07) Fixed 60 s timeout on every `gh` call, including asset upload and download
- Where: `pipeline/release.py:80-90` (`_gh`, `timeout=60`), used by `pull()` at `:170-174` and `push()` at `:190`
- Problem: `subprocess.run(..., timeout=60)` applies to `gh release download` and `gh release upload` as well as to the cheap `view`. `evidence.jsonl` carries full adapter payloads for every repository and `gateway.sqlite` grows with every six-hourly snapshot; neither size is bounded. A `TimeoutExpired` kills `gh` mid-transfer. On upload `--clobber` deletes the old asset first (`docs/runbook.md:176-177`), so a timed-out upload leaves the release with no asset, and every later `pull` fails with "Release asset missing" until someone re-pushes by hand.
- Why it matters: a self-inflicted outage that grows more likely as the dataset grows, with no code path to recover automatically.
- Suggested fix: give transfer commands a much larger, configurable timeout (for example `AI_HUB_RELEASE_TIMEOUT_SECONDS`, default 600) and keep 60 s only for `view`/`create`; alternatively drop `timeout` for transfers and rely on the job's `timeout-minutes: 45`. Add a test asserting the transfer timeout differs from the metadata timeout.

### F2 [MEDIUM] (T07) Unexpected errors are recorded by type name only, and no traceback or message reaches the run log
- Where: `pipeline/failure.py:60` (`reason = type(error).__name__`); `pipeline/cli.py:191-201` (the `except EXPECTED_ERRORS` block logs only `issue_title`/`issue_body`, never `exc_info`); `pipeline/cli.py:250-263` likewise for standalone commands
- Problem: for `OSError`, `ValueError`, `sqlite3.Error` and `PromotionError` the only diagnostic anywhere — issue, `failures.jsonl` and `state/logs/<run_id>.log` — is the class name. Example: running without `GH_TOKEN` raises `ValueError("GH_TOKEN or GITHUB_TOKEN is required ...")` and the operator sees "Reason: ValueError". The runbook promises "Detailed logs are `state/logs/<run_id>.log`" but that file holds only the INFO stage lines plus the same sanitised text.
- Why it matters: the sanitisation is right for the GitHub issue, but the local log is the place the runbook sends people to diagnose, and it carries nothing extra.
- Suggested fix: in both `except` blocks write the traceback to the file handler only (for example `LOG.debug("Run %s failed", run_id, exc_info=exc)` with the handler at DEBUG, or a dedicated logger attached only to the file handler) and keep the issue text as it is. Add a test asserting the log file contains the exception class and message for a `ValueError` fault.

### F3 [MEDIUM] (T08) Action SHA pins and the uv version are unverifiable offline and are a single point of failure
- Where: `.github/workflows/refresh.yml:30` (`actions/checkout@d23441a4...  # v6`), `:35` (`astral-sh/setup-uv@37802adc...  # v7`), `:37` (`version: "0.11.19"`), `:67` (`actions/upload-artifact@b7c566a7...  # v6`)
- Problem: Codex executed without network, and none of the three 40-character SHAs or the uv release number can be checked from the snapshot. The workflow test only checks the shape of the pin, so a fabricated or mistyped SHA passes the suite and fails the real job at step one.
- Why it matters: the deliverable's acceptance is "the workflow runs"; a bad pin makes every scheduled run fail before the pipeline starts.
- Suggested fix: before the first `workflow_dispatch`, verify each SHA resolves to the stated tag (`gh api repos/actions/checkout/git/ref/tags/v6` etc.) and that `uv 0.11.19` exists; record the verification in the handover. Optionally relax `version:` to a floor so drift cannot break the job.

### F4 [LOW] (T07) The "upload is skipped when gates fail" acceptance is not actually tested
- Where: `tests/test_cli.py:150-166`: `release.push` is monkeypatched to `pytest.fail`, but every invocation uses `--no-release`, so `push` is unreachable regardless of the fault. Lines 180 and 221 also pass `transfer=False`.
- Problem: the guard is vacuous; the code is correct by structure (`pipeline/cli.py:170-188`), so this is a test-strength finding.
- Suggested fix: parametrise one gate-failure case with `transfer=True`, `release.pull` patched to return `False` and `release.push` patched to `pytest.fail("failed run uploaded")`.

### F5 [LOW] (T07) Dry-run outputs land under `site/src/data/` which is not ignored by Git
- Where: `pipeline/cli.py:174-178` writes `site/src/data/listings.dry.json` and `listings.dry.evidence.jsonl`; `.gitignore` ignores `state/` but nothing under `site/`
- Problem: the dry-run evidence file contains full third-party payloads. After T09's dry run both files sit untracked and one careless `git add -A` commits them.
- Suggested fix: add `site/src/data/*.dry.*` and `site/src/data/*.evidence.jsonl` to `.gitignore` (or route dry-run evidence to `state/`), and mention it in the runbook's dry-run paragraph.

### F6 [LOW] (T07) First-run detection depends on an exact `gh` stderr string
- Where: `pipeline/release.py:105` (`result.stderr.strip().lower() == "release not found"`)
- Problem: correct for current `gh` but brittle across versions and locales; any other wording raises. Fail-closed, but the first real `release pull` is the only thing that exercises it.
- Suggested fix: keep the fail-closed default, but also accept the exit code plus a `startswith`/regex match, and note in the runbook that a first-run `release pull` should be tried manually once before enabling the schedule. Record the `gh --version` the check was validated against.

### F7 [NOTE] (T07) Stage label is stale while the baseline is read
- Where: `pipeline/cli.py:120-123`: `stage = "release.pull"` is set before `release.pull`, and `previous_count(...)` runs under that label; `stage = "store"` only follows at line 131.
- Suggested fix: set `stage = "baseline"` before the `previous_count` call.

### F8 [NOTE] (T07) Standalone `pipeline gates` failures overwrite the latest issue files and append to run history
- Where: `pipeline/cli.py:239-243` and `:250-263` (`record_failure` is called for the `gates` command as well)
- Suggested fix: either document it in the runbook or skip `record_failure` for the read-only `gates` command.

### F9 [NOTE] (T08) `gh` repository resolution in Actions relies on the checkout's remote
- Where: `.github/workflows/refresh.yml:21` sets `GH_TOKEN` only; no `GH_REPO`
- Suggested fix: add `GH_REPO: ${{ github.repository }}` to the job `env`.

### F10 [NOTE] (T07) Orchestration order deviates from the approved plan (run_log before promote and push)
- Where: `pipeline/cli.py:180-188`; documented in `docs/runbook.md:87-91` and the handover
- Problem: PLAN_APPROVED T07 lists "promote, push, run_log"; the implementation finalises `run_log` before promotion because `StateStore.promote()` closes the connection. The consequence is handled by a separate failure record and a retry path. Sound and documented; record as consciously superseded.

## Checked

- Diff: `changes.diff` in full (1,891 lines, 16 files).
- Specs and context: `PLAN_APPROVED.md` (T06–T08 and standing rules), `TASK_HANDOVER.md` B3 section and coordinator checks, `AGENTS.md`, `.ai/PROJECT.md`.
- Supporting source: `pipeline/store.py`, `pipeline/export.py`, `pipeline/scoring.py`, `pipeline/models.py`, `pipeline/config.py`, `pipeline/budgets.py`, `pipeline/http.py`, `pipeline/sources/github.py`, `pipeline/sources/_enrichment.py`, `pipeline/migrations.py`, `pyproject.toml`, `.gitignore`.
- T06 acceptance: gate 2 pass/fail including unknown topic/level; gate 3 freshness boundary at exactly 7 h and negative age; count rule including first run; score/licence/tested/labels pass and fail; `REQUIRE_LABELS` default switch; abort preserves canonical byte-for-byte and the record names the gate and counts. Verified `len*10 < previous*9` matches "at least 90 per cent".
- T07 acceptance: fake `gh` records exact argv; absent release is first run while 401/404/network are not; pull failures keep the existing bundle; push rejects ungated/corrupt/mismatched bundles; stale working copy blocks both transfers and names the removal command; dry run with `--limit 5` completes offline, validates against `Listings`, never pulls/pushes/promotes and leaves production files byte-identical; real-run order `pull → ingest → enrich×4 → score → export → gates → promote → push`; exit codes 0/1/2; secret absent from failure records and logs; push failure after promotion keeps a valid local bundle; output I/O failure restores database, evidence and listings.
- Publication safety path by reading: `_publish` backs up canonical before `promote` and restores on `OSError`; `replace_bundle` restores earlier files in reverse; `StateStore.__exit__` rollback is idempotent after promotion.
- Secret hygiene: every string that reaches `RunFailure.reason` is fixed text or sanitised counters; `gh` stderr is never copied into messages.
- T08 acceptance: cron, dispatch, concurrency, permissions, `uv sync --frozen`, pull → run → push order, failure step with `gh issue create --label pipeline-failure`, only `secrets.GH_TOKEN` referenced. Runbook has the four required incident entries plus run-locally and roll-back sections. README commands match `cli.py`.
- Conventions: module docstrings, type hints, pathlib, logging not print (the only `print` is the fake `gh` fixture), no bare `except Exception`, British spelling.
- Scope: within the three tasks; no edits to B1/B2 public signatures.

## Limits

- Could not run anything (read-only brief): test results taken from the coordinator's record (412 passed, 98.39 % coverage, ruff clean).
- No network: the three action SHAs, the uv version, the Dependabot `uv` ecosystem name, the exact `gh` "release not found" wording and the `gh release create --latest=false` flag are plausible but unverified (F3, F6).
- `actionlint` was not run by anyone.
- Live behaviour of the release round trip is untested until the first scheduled run; T09's dry run skips transfers.
- Windows-only observation: the `.cmd` fake-`gh` wrapper depends on `PATHEXT` containing `.CMD`; default, not a finding.

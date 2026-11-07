# Claude audit — T01, T02, T03 (round 1)

Reviewer: Claude audit subagent (dual_dev_auditor, session model), 07 November 2026. Saved verbatim by the coordinator.

## Verdict
PASS_WITH_FINDINGS — no blockers; two MEDIUM findings on T03 that unit tests cannot surface and the T09 dry run would hit.
- T01 — PASS (one LOW, two NOTEs).
- T02 — PASS (two NOTEs, both already flagged by Codex, carried forward as cross-task obligations).
- T03 — PASS_WITH_FINDINGS (two MEDIUM: GraphQL retries are self-defeating in realistic failure cases; unrecognised `X-GitHub-Api-Version` value).

## Findings

### F1 [MEDIUM] (T03) GraphQL retries abort the run in every realistic failure case
- Task: T03
- Where: `pipeline/sources/github.py:110-135` (`_account_response`), `:159-164` (`retryable=True`, `before_attempt=self.budget.reserve_graphql`); `pipeline/http.py:367-393`; test `tests/test_github.py:188-203`.
- Problem: every GraphQL attempt reserves one point and increments `github_unmeasured_calls` (`budgets.py:130-133`). The reservation is only reconciled when the response body contains `data.rateLimit` (`github.py:119-127`). A retried 429/502/503 from GitHub in practice carries either an HTML body or `{"message": ...}` with no `data` block, so `_account_response` returns at `:116` or falls through with `rate is None` and the reservation stays unmeasured. The retry then succeeds, and `:134-135` raises `GitHubResponseError("earlier GraphQL cost is unmeasured; run aborted")`. Transport errors behave the same way (tested as intended at `test_github.py:206-222`). The only test exercising a retried status (`test_retry_response_costs_are_counted`) feeds a 503 whose body is a full, valid GraphQL payload with `rateLimit`, which real GitHub error responses do not provide, so the test masks the behaviour.
- Why it matters: `retryable=True`, the back-off, and the `Retry-After` handling in `http.py` are effectively dead code for the GitHub source: one transient 502 on a six-hourly run aborts the run (and, from T06 onwards, opens a failure issue) even though the data path would have recovered. It also contradicts the plan's intent of "httpx client with retries". The fail-closed accounting rationale is sound for lost responses, but it is applied to responses GitHub did receive and answered.
- Suggested fix: on a non-success response without `rateLimit`, settle the reservation with a conservative fixed upper bound for one search page (for this query shape GitHub's formula gives roughly 3-4 points: `1 + (100 + 100 + 100) / 100`), decrement `github_unmeasured_calls`, and log that the cost was estimated; keep the abort for genuine lost responses (transport errors) or make it configurable. Add a test with a 502 HTML body followed by a 200 that expects the run to succeed with the estimated cost. At minimum, document in the module docstring that retries will almost always abort the run and remove the misleading fixture.

### F2 [MEDIUM] (T03) `X-GitHub-Api-Version: 2026-03-10` is not a documented API version
- Task: T03
- Where: `pipeline/sources/github.py:106`; the same header dict is sent on the REST fallback at `:195-198`.
- Problem: GitHub's REST API versioning documentation lists `2022-11-28` as the supported calendar version and states that a request naming an unsupported version is rejected with HTTP 400. I know of no `2026-03-10` version (knowledge to June 2026) and could not check online. If the value is invalid, the opt-in contributor fallback fails on every repository with `HttpRequestError("contributors HTTP 400")` (`:201-202`), discarding the whole search result. Whether the GraphQL endpoint also validates the header is not documented; if it does, the main search path fails too and T09's dry run will be the first place anyone sees it.
- Why it matters: a hard-coded header value that cannot be checked offline and, in the REST case, is documented to produce a 400. Tests pass because MockTransport ignores headers.
- Suggested fix: use `2022-11-28` (the documented version) or omit the header; if a later version is intended, cite the GitHub changelog entry in the module docstring so the next reviewer can verify it.

### F3 [LOW] (T01) Ruff rule selection is not pinned, so the lint check depends on the machine
- Task: T01
- Where: `pyproject.toml:22-23`; handover `TASK_HANDOVER.md:35`.
- Problem: `[tool.ruff]` sets only `target-version`. Ruff's default selection is `E4, E7, E9, F`; it does not include `PLW1510` or `PERF102`, yet the handover reports both from `uv run ruff check .`. Those rules can only have fired from a user- or machine-level Ruff configuration, so the "project check" named in the plan's standing rules is not reproducible from the repository alone.
- Why it matters: T08's workflow runs `ruff check .` on a clean runner, which will apply different rules from the developer machines; new findings (or their absence) will not match local results. Line lengths above 88 characters throughout the new files (for example `tests/test_github.py:35`) would also fail if a future config enables `E501`.
- Suggested fix: add `[tool.ruff.lint] select = [...]` (and `line-length` if the longer lines are intended) to `pyproject.toml` so local and CI runs agree; re-run `uv run ruff check .` under that pinned config.

### F4 [LOW] (T01) `Listing.score_version` can disagree with `Listing.score.score_version`
- Task: T01
- Where: `pipeline/models.py:581-587`.
- Problem: `Listing` carries its own required `score_version` and also embeds `score: Score`, which has a `score_version` of its own. No validator ties the two together, so a listing can publish `score_version="v0"` with a score computed under a different version once a `v1` exists.
- Why it matters: the plan makes `score_version` part of the publication contract (T05 writes it into `listings.json`; T06 gate 2 validates it). With a single Literal value today this cannot diverge, but the duplication will silently allow it on the first weight change.
- Suggested fix: a `model_validator(mode="after")` on `Listing` asserting `self.score_version == self.score.score_version`, or derive the field from `score` instead of requiring it separately. One test for the mismatch.

### F5 [NOTE] (cross-task) Failed runs leave no trace in `run_log`
- Task: cross-task (T02 → T06/T07)
- Where: `pipeline/store.py:148-163` (`finish_run` accepts `status="failed"`), `:209-216` (`rollback` deletes the working copy); schema `pipeline/migrations.py:451-460` (`status IN ('running','succeeded','failed')`).
- Problem: the only database a failed run can write to is the working copy, which `rollback()` deletes; `finish_run(..., status="failed")` therefore never persists. The `run_log.status = 'failed'` value and T06's "counts, log path" failure text have no durable source. Codex flagged this in the handover (`TASK_HANDOVER.md:67`).
- Why it matters: T06's abort rule and T08's runbook assume failure diagnostics exist; T07's orchestration order ("promote, push, run_log") must be designed around this now or the failure path will be rediscovered late.
- Suggested fix: record the decision in `.ai/DECISIONS.md` or the T06/T07 brief: either write failed-run entries to a separate append-only log (file or small table outside the promoted database) or allow `promote()` of a run-log-only change. No change required in T02 itself.

### F6 [NOTE] (cross-task) A stale working copy blocks every later run until removed by hand
- Task: cross-task (T02 → T07/T08)
- Where: `pipeline/store.py:46-48` (`open("xb")`), module docstring `:3-6`; test `tests/test_store.py:128-134`.
- Problem: exclusive creation is the right protection against two writers, but after a crash or a killed process the leftover `state/gateway.work.sqlite` makes every subsequent `StateStore()` raise `FileExistsError`. On a fresh GitHub Actions checkout this cannot occur; locally and on any persistent runner it will. Codex noted the gap (`TASK_HANDOVER.md:67`).
- Why it matters: the T08 runbook needs a documented recovery step, and T07's CLI needs to translate `FileExistsError` into a clear message rather than a traceback.
- Suggested fix: carry into the T07 and T08 briefs: a `pipeline run` pre-flight that reports the stale file with the exact path and the command to remove it; runbook entry "stale working copy".

### F7 [NOTE] (T01) Minor configuration and test-isolation rough edges
- Task: T01
- Where: `pipeline/config.py:273`; `tests/test_config.py:13` with `scripts/pull_candidate_repos.py:15`; `tests/test_config.py:33-34`.
- Problem: (a) a malformed `AI_HUB_HTTP_CALL_LIMITS` raises `json.JSONDecodeError`, not `ValidationError` like every other bad setting, so T07's CLI will need two exception paths. (b) `test_config.py` imports the phase 0 script, which calls `logging.basicConfig(level=INFO)` at import and installs a root handler for the whole pytest session. (c) `test_environment_overrides` calls `Settings.from_env()` against the real `os.environ`, so a developer with `AI_HUB_QUERY_NAMES` or similar exported would see an unrelated failure.
- Why it matters: small, but each is a future debugging cost; none affects acceptance.
- Suggested fix: wrap `json.loads` and re-raise as `ValueError` with a clear message (pydantic will turn it into a `ValidationError` if the parse moves into a validator); pass an explicit mapping in the test instead of `monkeypatch.setenv`; leave the script import as is (it is what the plan's parity test asks for).

## Checked
- Read in full: `changes.diff` (file list and the diffs for `.gitignore`, `.python-version`, `pipeline/__init__.py`, `budgets.py`, `config.py`, `http.py`, `migrations.py`, `models.py`, `sources/__init__.py`, first 70 lines of `sources/github.py`); from the snapshot: `pipeline/sources/github.py` (lines 70-234), `pipeline/store.py`, `pyproject.toml`, `tests/conftest.py`, `tests/test_config.py`, `tests/test_models.py`, `tests/test_store.py`, `tests/test_budgets.py`, `tests/test_http.py`, `tests/test_github.py`, all five fixtures under `tests/fixtures/`, `scripts/pull_candidate_repos.py`, `.gitignore`, `PLAN_APPROVED.md`, `TASK_HANDOVER.md`, `AGENTS.md`, `.ai/PROJECT.md`; `uv.lock` package names and versions only (httpx 0.28.1, pydantic 2.14.3, pytest 9.2.0, pytest-cov 7.1.0, ruff 0.17.4 — all within the `pyproject.toml` ranges).
- T01 acceptance: `QUERIES` in `config.py:183-201` compared line by line against `pull_candidate_repos.py:18-36` — identical, and `test_config.py:16-17` imports both. `NICHE_DEFAULT` is the six names in the plan's order (`config.py:202`). Every model uses `extra="forbid"` and `allow_inf_nan=False` (`models.py:518`); the enum test (`test_models.py:28-40`) is derived from `model_fields` so it covers every Literal field including the list field; `Listing` requires `tested` and `score_version` (`models.py:586-587`, tested at `test_models.py:52-57`). Weights sum to 1 with stars and velocity at 0 (`config.py:205-215`). `SecretStr` with `repr=False` keeps the token out of `repr` and `model_dump_json` (`test_config.py:44-45`).
- T02 acceptance: schema v1 contains every table and column named in the plan (`migrations.py:21-61`), with `snapshots` unique per repo and run via the composite primary key; migration runs atomically inside `BEGIN IMMEDIATE` with rollback on failure. Working copy at `state/gateway.work.sqlite`, canonical opened read-only via URI for `backup()` (`store.py:50-56`); `promote()` requires non-empty all-`True` gates, `integrity_check` and `foreign_key_check` before `Path.replace` (`store.py:191-207`); `__exit__` always rolls back (`:75-79`). Velocity uses the actual elapsed hours between the earliest in-window and the latest snapshot, `None` with fewer than two, negative on falling counts (`store.py:165-189`; `test_store.py:57-66` covers +2, -2, 0). Rename history keyed by `github_id` (`store.py:81-98`; `test_store.py:38-55`). Byte-identical canonical after failed gates, exceptions, explicit rollback, failed replace and foreign-key corruption (`test_store.py:87-161, 200-207`). Timestamps normalised to UTC ISO so string comparison in SQL orders correctly (`store.py:30-33`).
- T03 acceptance: two-page fixture dedupes R_2 and maps every requested field (`test_github.py:27-59` against `github_page_1.json`/`github_page_2.json`); partial-error fixture raises `GraphQLError` naming the query and still records the reported cost (`github.py:126-129`, `test_github.py:90-99`); budget aborts on the crossing call and blocks the next network call (`budgets.py:118-142`, `test_github.py:102-134`); token absent from `caplog` at DEBUG and from exception text (`test_github.py:99, 203`), transport errors sanitised (`http.py:379-381`), redirects disabled (`http.py:377`). GraphQL query text contains every field the plan lists (`github.py:39-58`). REST fallback is off by default (`config.py:235`), uses `per_page=1&anon=true` and the `rel="last"` page count, and validates the Link URL host and path (`github.py:193-221`). Module docstring states the proxy and fallback (`github.py:1-22`).
- Cross-task fit: `Budget.snapshot()` returns a JSON-safe dict consumed by `StateStore.start_run`/`finish_run`; `HTTP_CALL_LIMITS` keys match the four T04 adapters plus GitHub; `SCORE_WEIGHTS_V0` keys match the T05 component list; `RepoRecord` round-trips through `upsert_repo`/`get_repo` (`test_store.py:34`).
- Handover test counts reconciled by hand: T01 33 tests (11 config + 22 models), T02 24, T03 62 (37 github + 8 budgets + 17 http) = 119, matching "119 passed". Coverage 99.23 per cent is plausible given the one `AssertionError` guard at `http.py:394` and a few defensive branches.
- Scope: all 25 changed files fall under the three tasks' likely-files lists or are necessary support (`uv.lock`, `tests/test_http.py`, cache entries in `.gitignore`). No `.ai/` or script edits by Codex. British English throughout (licence, serialisable, sanitised).

## Limits
- Could not run `uv sync --frozen`, pytest, coverage or ruff (read-only brief); test and coverage results are taken from the handover and cross-checked only by counting test cases.
- Could not verify online whether GitHub accepts `X-GitHub-Api-Version: 2026-03-10` (F2) or how the GraphQL endpoint treats that header; the finding rests on GitHub's documented REST behaviour as of my knowledge cut-off.
- `uv.lock` was checked for package names and versions only, not hashes or the full dependency graph.
- The `Topic` Literal values in `models.py:498-503` were not cross-checked against `docs/phase1_architecture_and_operations.md` (not named in the T01 specification); the T05/T06 reviewer should confirm they match the labelled CSV's topic vocabulary.
- Behaviour of `Path.replace` over an open canonical database on Windows was reasoned about from the code and the monkeypatched test only; not exercised.

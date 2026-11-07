# Claude audit — T04, T05 (round 1)

Reviewer: Claude audit subagent (dual_dev_auditor, session model), 07 November 2026. Saved verbatim by the coordinator. Snapshot root for every path: scratchpad `dd_T001_B2_audit_r1\snap` (deleted after saving).

## Verdict
PASS_WITH_FINDINGS — one HIGH correctness bug in the licence classifier, otherwise both tasks meet their acceptance criteria with offline tests that cover them.
- T04 (enrichment adapters): PASS_WITH_FINDINGS — all acceptance lines met; one robustness bug in the Hacker News parser (F4) and several unverified live-API assumptions that T09 must confirm.
- T05 (scoring and export): PASS_WITH_FINDINGS — all acceptance lines met; the licence component never recognises GitHub's copyleft SPDX identifiers (F1), and the advisories component is permanently unevaluated by design (F2).

## Findings

### F1 [HIGH] (T05) Copyleft licence identifiers never match what GitHub emits
- Task: T05
- Where: `pipeline/scoring.py:29-37` (`WEAK_COPYLEFT`, `STRONG_COPYLEFT`), `pipeline/scoring.py:103-112` (`_licence`), `docs/scoring.md:68-69`; evidence `pipeline/sources/github.py:55,93`, `data/labelled_repos_for_review.csv:10,15,20,21,29,46,63,86,97,100`, `data/candidate_repos.csv` (88 of 965 rows)
- Problem: the classifier only lists `GPL-2.0-only`, `GPL-3.0-or-later`, `LGPL-2.1-only`, `AGPL-3.0-only` and so on. GitHub's `licenseInfo.spdxId` (B1 maps it unchanged at `github.py:93`) uses the older identifiers `GPL-3.0`, `GPL-2.0`, `LGPL-2.1`, `LGPL-3.0`, `AGPL-3.0`. The project's own GitHub-sourced CSVs prove it: every copyleft row in `data/labelled_repos_for_review.csv` and `data/candidate_repos.csv` reads `AGPL-3.0`, `GPL-3.0` or `LGPL-3.0`; none has a `-only`/`-or-later` suffix. So every copyleft repository falls through to `return None, "unsupported", "unknown"` (`scoring.py:112`). The test `test_licence_classes` (`tests/test_scoring.py:75-88`) uses `GPL-3.0-only`, which GitHub never returns, so it passes without exercising the real input.
- Why it matters: roughly 9 per cent of the candidate set (88/965) loses the 15 per cent licence weight, their coverage drops, and the export labels a clearly licensed repository `licence_class: unknown`. Permissive repos are unaffected, so copyleft repos are systematically ranked on fewer components than their peers — a ranking bias, not a neutral gap. `docs/scoring.md:68-69` documents the wrong identifiers as the policy.
- Suggested fix: include GitHub's identifiers (`GPL-2.0`, `GPL-3.0`, `LGPL-2.1`, `LGPL-3.0`, `AGPL-3.0`, and `LGPL-2.0`/`MPL-2.0`/`EPL-*` as already listed) or normalise by stripping a `-only`/`-or-later` suffix before set lookup; add a parametrised test fed with the distinct `license` values from `data/candidate_repos.csv`; correct `docs/scoring.md`.

### F2 [MEDIUM] (cross-task) The advisories component can never be evaluated; 20 per cent of the weight is dead by construction
- Task: cross-task (T04 adapter, T05 weights)
- Where: `pipeline/sources/deps_dev.py:34` (hard-coded `"advisories_status": "unsupported"`), `pipeline/scoring.py:88-96`, `docs/scoring.md:47-54`, `.ai/tasks/T001_ingestion_pipeline/PLAN_APPROVED.md:40` ("deps.dev advisories")
- Problem: the approved plan names "deps.dev advisories" as a scored component. The adapter calls only the project endpoint, which (as Codex correctly notes) does not carry package-version advisories, and always returns `unsupported`. Combined with release cadence (no history fetched, `scoring.py:124-139`), the maximum attainable coverage is 0.70, which the handover acknowledges (`TASK_HANDOVER.md:263-264`). The deps.dev call therefore costs one HTTP request per repo and yields nothing the scorer uses; the project payload also duplicates the Scorecard that the research note says GetProject already embeds (`research_notes/.../trust_quality_signals_and_data.md:70`).
- Why it matters: this is a documented design decision, not a hidden bug, but it is a deviation from the approved plan that the user has not yet accepted. Until it is, every published total silently divides by at most 0.70 of the weight and the 30 per cent "missing" is invisible on the listing row (only in `scoring_details`).
- Suggested fix: record the decision explicitly (AUDIT_LOG/DECISIONS) and either (a) add a follow-up task to resolve packages via deps.dev `GetProjectPackageVersions` → `GetVersion.advisoryKeys`, or (b) rebalance `SCORE_WEIGHTS_V0` so unimplemented components do not carry weight, bumping `SCORE_VERSION` per the policy in `docs/scoring.md:5`. Either way, consider whether the deps.dev call is worth its budget before T09.

### F3 [MEDIUM] (T05) The site data file embeds every raw adapter payload
- Task: T05
- Where: `pipeline/scoring.py:192` (`evidence=list(sources.values())`), `pipeline/export.py:42` (`scoring_details: dict[str, ScoreDetails]`), `pipeline/sources/scorecard.py:36` (returns the full Scorecard body including `checks`), `pipeline/sources/deps_dev.py:34` (embeds the whole project object under `"project"`)
- Problem: `write_listings` serialises `ScoreDetails.evidence` — the complete `Evidence.data` for every adapter — into `site/src/data/listings.json`. A Scorecard result with its `checks[].details` arrays is typically 10–20 KB; deps.dev projects add more. For the niche default (six queries × 100 cap, up to ~600 repos) that is a multi-megabyte JSON file whose consumer is a browser-side static site.
- Why it matters: page weight and build time for the Astro site (request 5), and the Scorecard check details are of no use to the listing UI. Diagnostics belong in a separate artefact or should be trimmed.
- Suggested fix: keep `scoring_details` but reduce `evidence` to a compact per-source summary (status, detail, `score`/`date`, `mention_count`/`top_item`, `link_status`/`links`), or write full evidence to a sibling file (e.g. `site/src/data/evidence.json` or under `state/`) that the site does not ship. Add a test asserting an upper bound on per-row serialised size.

### F4 [MEDIUM] (T04) A single Hacker News story with a null URL fails the whole component
- Task: T04
- Where: `pipeline/sources/hacker_news.py:40-44`
- Problem: the loop raises `ValueError("Invalid story")` when `hit["url"]` is not a string. HN stories legitimately have `url: null` (Ask HN / Show HN text posts). The adapter relies on `restrictSearchableAttributes=url` (`hacker_news.py:25`) to keep such hits out, but that parameter is not among those listed in the HN Algolia API reference and its behaviour here is unverified. If even one text-only story matches (for example on `story_text`), every mention for that repo is discarded as `failed` instead of that hit being skipped. The existing test (`tests/test_enrichment.py:176-188`) covers out-of-window and wrong-URL hits but not a null URL.
- Why it matters: a 5 per cent component flips from evaluated to `failed` on a benign input, and `failed_components` would then report a false alarm.
- Suggested fix: treat `url` of `None` as "does not link the repository" and `continue`; keep hard failure for structural fields (`objectID`, `created_at_i`, `points`, `title`). Add a fixture hit with `"url": null`.

### F5 [LOW] (T04) HTTP 404 from the two search endpoints is reported as `absent`
- Task: T04
- Where: `pipeline/sources/_enrichment.py:64-65`, used by `pipeline/sources/hugging_face.py:23-27` and `pipeline/sources/hacker_news.py:22-29`
- Problem: for deps.dev and Scorecard a 404 genuinely means "no record for this repo". For `huggingface.co/api/search/full-text` and `hn.algolia.com/api/v1/search` an empty result is a 200 with no hits; a 404 means the endpoint has moved or been removed. The shared helper maps it to `absent`, so an endpoint change would appear as "no HN mentions / no HF links" for every repository with no `failed` flag anywhere. The fixtures encode this synthetic case (`tests/fixtures/enrichment_responses.json:19,27`).
- Why it matters: silent degradation of a signal; the plan's generic "absent (404)" wording was followed, so this is a design refinement rather than a defect.
- Suggested fix: let `fetch_json` take an `absent_statuses` argument (default `{404}`) and pass an empty set from the two search adapters so 404 becomes `failed`; or at minimum `LOG.warning` on 404 from search endpoints.

### F6 [LOW] (T04) deps.dev adapter does not check the returned project is the requested repository
- Task: T04
- Where: `pipeline/sources/deps_dev.py:28-30` versus `pipeline/sources/scorecard.py:28`
- Problem: Scorecard verifies `links_repo("https://" + data["repo"]["name"], repo)`; deps.dev only checks `projectKey.id` starts with `github.com/`. A redirected or aliased project (renames are common) would be accepted as this repo's evidence.
- Why it matters: low today because the payload is unweighted, but it is the one adapter whose identity check is weaker than its sibling's.
- Suggested fix: `links_repo("https://" + identifier, repo)` with the same `failed(..., "Mismatched repository")` outcome.

### F7 [LOW] (T05) Provisional labels join on the current `full_name`, so a renamed repo loses its label
- Task: T05
- Where: `pipeline/export.py:117`, `pipeline/export.py:19` (`DEFAULT_LABELS_PATH`)
- Problem: B1 tracks renames by GitHub ID (`renamed_from` in `pipeline/store.py`), but the CSV has no ID column and the join is by name only. A repository renamed after labelling reverts to `pending`. Separately, `PROJECT.md:35` says this CSV "becomes `data/gold_labels.csv` after Po's review", so the default path is already known to be temporary.
- Why it matters: label loss is silent; T06 gate 2 would not notice.
- Suggested fix: document the limitation in `docs/scoring.md` now; when gold labels arrive (request 2), key them by `github_id` or also match `renamed_from`.

### F8 [LOW] (T04) Live API assumptions are unverified and only T09 can confirm them
- Task: T04
- Where: `pipeline/sources/hugging_face.py:7-8,24-25` (undocumented `/api/search/full-text`, `estimatedTotalHits`, `formatted.fileContent`), `pipeline/sources/hacker_news.py:24-27` (`restrictSearchableAttributes`, `typoTolerance`, `hitsPerPage=1000`), `pipeline/sources/scorecard.py:30-33` (`date` parses with `fromisoformat`), `pipeline/http.py:90` (`follow_redirects=False`, so any 301 becomes `failed`)
- Problem: all four adapters fail closed on schema drift, which is the right default, but none of these shapes is confirmed by a recorded live response; the fixtures were written by hand. The phase 0 research explicitly left "exact Algolia HN limits" and "api.scorecard.dev endpoint reference" unresolved (`research_notes/.../trust_quality_signals_and_data.md:87,152`).
- Why it matters: if any assumption is wrong the first real run yields 100 per cent `failed` for that source. Harmless for ranking (weight excluded) but it would mislead the coverage figures and waste the HTTP budget.
- Suggested fix: in T09, record one real response per adapter under `tests/fixtures/` (sanitised) and switch the parametrised test to those; note the T09 check in the handover.

### F9 [NOTE] (cross-task) Lint intent and small test hygiene
- Task: cross-task
- Where: `pyproject.toml:24,27` (`line-length = 100` but `select` omits `E501`); over-length lines at `pipeline/export.py:65,67` and `pipeline/scoring.py:166`; `tests/test_enrichment.py:100` (`HttpClient(Budget())` creates an owned `httpx.Client` that is never closed); `tests/test_export.py:48-51` (`test_real_provisional_csv_validates` assumes the working directory is the repo root)
- Problem: cosmetic. Ruff passes because E501 is not selected, so the configured line length is advisory only. The unclosed client only emits a `ResourceWarning`. The CWD assumption holds for `uv run pytest` from the root.
- Why it matters: none today; recorded so the B1 lint decision is not mistaken for enforcement.
- Suggested fix: optional — add `E501` to `select` or drop `line-length`; wrap the client in `with`.

## Checked
- Read the full `changes.diff` (12 files, 1,337 insertions, all new files; no modifications to B1 code, no `.ai/` changes in the range, no scope creep — every file is in the plan's "likely files" or is the shared helper `_enrichment.py`).
- T04 acceptance, line by line: parametrised present/absent/failed test across all four adapters (`tests/test_enrichment.py:33-43`) — present; one HTTP call per repo asserted both by request count and `budget.http_calls` (`test_enrichment.py:30,43`) — present; never raises on 404 (`_enrichment.py:64`) — confirmed; `fetched_at` always set and tz-aware (`_enrichment.py:16-21,55`) — confirmed; unsupported host makes no request (`_enrichment.py:57-58`, test `:91-95`) — confirmed; retries are charged per attempt and `BudgetExceeded` propagates (`pipeline/http.py:80-85`, tests `:46-71`) — confirmed.
- T05 acceptance: total bounded 0–100 (`scoring.py:185-186`, test `test_bounds_and_fully_evaluated_weights`); ordering by score differs from ordering by stars (`tests/test_export.py:54-63`); all-absent → `total None`, `coverage 0`, excluded from rows but kept in `scoring_details` (`export.py:115-116`, test `:78-83`); JSON validates against `Listings` on round trip (`test_export.py:86-94,202-224`); CSV join and `label_status` (`export.py:117-123`, test `:38-45`); `unevaluated_checks` fixed list (`export.py:122`); sort by total then push time with deterministic tie-breaks (`export.py:126-130`, tests `:54-75`); envelope carries `generated_at`, `score_version`, `run_id` (`export.py:131-134`).
- Arithmetic: hand-checked the weighted mean and coverage for `test_weighted_mean_known_values` and `test_adapters_to_scoring_to_export_offline` ((78×0.25 + 40×0.05)/0.30); confirmed `_cadence` cannot divide by zero (distinct dates ⇒ positive span), `_freshness` handles `None` and future dates, and `ScoreDetails.matching_failures` requires exactly the seven positive-weight components (`pipeline/config.py:34-44`).
- Cross-task fit: `score_repo` returns `Score` unchanged for `StateStore.add_score` (`store.py:127`), `velocity(repo_id, window_hours) -> float | None` (`store.py:165`) matches the `velocity: float | None` parameter; `Listing` model untouched (`pipeline/models.py:90-109`); `Evidence.data` is `dict[str, JsonValue]` so the nested HN/HF/deps.dev payloads serialise.
- Licence bug evidence: `pipeline/sources/github.py:55,93` (`licenseInfo { spdxId }` passed straight through), B1 fixtures `tests/fixtures/github_page_1.json:9`, `github_page_2.json:17`, and the GitHub-sourced `license` column in `data/labelled_repos_for_review.csv` (10 copyleft rows, all un-suffixed) and `data/candidate_repos.csv` (88 of 965 rows match `,(A?GPL|LGPL)-x.y,`; other values seen: `MIT`, `Apache-2.0`, `NOASSERTION`, `BSD-2/3-Clause`, `MPL-2.0`, `Unlicense`, `CC0-1.0`, `CC-BY-4.0`).
- Real CSV header (`data/labelled_repos_for_review.csv:1`) contains `full_name`, `topic`, `level`, `confidence` — matches `load_provisional_labels` and the test that loads 100 rows.
- Conventions (`AGENTS.md`, `.ai/PROJECT.md`, `pyproject.toml`): module docstrings present on all seven new modules; type hints on public functions; `pathlib` used; no `print`; no bare `except Exception`; British English in docstrings and docs; no secrets sent to third-party hosts (adapters pass no headers); redirects disabled.
- Handover test results (`TASK_HANDOVER.md:227-228,256-257,272-273`): 270 passed, 98.38 per cent coverage, ruff clean — consistent with the tests I read; no test is missing against the acceptance lists.

## Limits
- I could not run anything (read-only brief). Test pass/fail and coverage figures are taken from the coordinator's handover.
- I could not query the live deps.dev, Scorecard, Hugging Face or HN Algolia APIs, so F4/F5/F8 rest on my knowledge of those APIs and on the project's own research notes; the HN `restrictSearchableAttributes`/`typoTolerance` behaviour and the HF full-text JSON shape are unverified either way.
- The GitHub SPDX identifier claim in F1 is inferred from the GraphQL field name and the GitHub-sourced CSVs in `data/`, not from a live GraphQL call; the CSVs were produced by the phase 0 REST script, whose `license.spdx_id` uses the same GitHub licence catalogue as GraphQL's `licenseInfo.spdxId`.
- Export size in F3 is an estimate (typical Scorecard payload size × expected repo count), not a measurement.

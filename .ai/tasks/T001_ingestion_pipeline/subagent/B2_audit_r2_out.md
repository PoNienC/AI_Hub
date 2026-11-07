# Claude audit — T04, T05 (round 2)

Reviewer: Claude audit subagent (dual_dev_auditor, session model), 07 November 2026. Re-check of the fix commit `4c87086..6653b63`. Saved verbatim by the coordinator; snapshot paths shortened to repo-relative.

## Verdict
PASS_WITH_FINDINGS — the HIGH finding (F1, copyleft licences) is resolved and verified; the other round-1 fixes are in place with no regressions found; remaining findings are LOW and NOTE only, none needs a third round.
- T04 (enrichment adapters): PASS — null-URL skip, `absent_statuses`, deps.dev identity check and client closing are correct and tested.
- T05 (scoring and export): PASS_WITH_FINDINGS — licence fix correct against the real CSV; row coverage and compact/full evidence split work; three LOW test/design points below.

## Findings

### F1 [LOW] (T05) The "coverage" schema test no longer exercises the envelope's zero-coverage rule
- Where: `tests/test_export.py:161-162` (mode `"coverage"` sets only `row["score"]["coverage"] = 0`); `pipeline/export.py:39-44` (`PublishedListing.matching_coverage`); `pipeline/export.py:72-73` (envelope rule `listing.score.coverage == 0`).
- Problem: since this commit a listing row carries its own `coverage` (0.25 in the fixture). Setting only `score.coverage` to 0 now trips the new row-level validator (`0.25 != 0`) during field validation, so `Listings.consistent_rows` never runs. The test still passes, but it now proves the row/score mismatch rule (already covered by `row_coverage`), not the envelope's "Published listings require evaluated scores" coverage branch. That branch is now exercised by no test.
- Why it matters: the regression guard for "a zero-coverage row must never be published" has silently been lost.
- Suggested fix: in mode `"coverage"` set both `row["coverage"] = 0` and `row["score"]["coverage"] = 0`, so the row validator passes and the envelope rule is the one that rejects.

### F2 [LOW] (cross-task) Default `evidence_path` is shared by dry runs and real runs
- Where: `pipeline/export.py:22` (`DEFAULT_EVIDENCE_PATH = Path("state/evidence.jsonl")`), `pipeline/export.py:214-217`; `docs/scoring.md:156`; plan T07 (`--dry-run` writes `listings.dry.json`).
- Problem: a caller that passes a dry-run `path` but forgets `evidence_path` silently replaces the production `state/evidence.jsonl` with dry-run evidence. The isolation relies on documentation, not on the API.
- Why it matters: the full-evidence snapshot is the only place raw adapter payloads survive; a dry run overwriting it loses the last real run's diagnostics with no error.
- Suggested fix: derive the default from `path` (for example `path.with_suffix(".evidence.jsonl")` or a sibling name under the same parent), or make `evidence_path` required when `path` is not the default. At minimum, T07's brief should name both paths explicitly for `--dry-run`.

### F3 [LOW] (cross-task) Full evidence is written to an ephemeral location in the scheduled workflow
- Where: `pipeline/export.py:233-241`; `.gitignore:2` (`state/` ignored); plan T07 (only `gateway.sqlite` is pulled and pushed); plan T08 (GitHub Actions runner).
- Problem: in the scheduled run `state/` lives on a throwaway Actions runner; the release round trip uploads only `gateway.sqlite`. So in production the full evidence is written and then discarded; "retained" holds only for local runs.
- Why it matters: when a listing's score is questioned after a scheduled run, only the compact summary is left. A consequence of the approved fix, not a defect in it, but T07/T08 need to know.
- Suggested fix: have T07 upload `evidence.jsonl` alongside the SQLite asset (or as a workflow artefact in T08), or state in `docs/scoring.md` that full evidence is local-only until then.

### F4 [NOTE] (T05) B1 `Listing` no longer validates an exported row
- Where: `pipeline/models.py:27-30` (`Record` has `extra="forbid"`), `pipeline/models.py:90` (`Listing`); `pipeline/export.py:34-37` (`PublishedListing` adds `coverage`); `tests/test_export.py:100`.
- Problem: an exported row carries `coverage`, which `Listing` rejects as an extra field. T06 gate 2 ("every listing validates") must validate against `PublishedListing`/`Listings`, not `Listing`.
- Suggested fix: none required now; record in T06's brief that the row model is `pipeline.export.PublishedListing`.

### F5 [NOTE] (T05) Candidate-licence test depends on a data file at import time
- Where: `tests/test_scoring.py:14-17` (module-level read of `data/candidate_repos.csv`), `tests/test_scoring.py:97-114` (`expected[spdx]` lookup).
- Problem: a new licence value in the CSV surfaces as a bare `KeyError` rather than a message saying the classifier policy needs a decision. The canary behaviour is desirable; the failure mode is opaque.
- Suggested fix: `pytest.fail(f"Unclassified licence in candidate CSV: {spdx!r}")` when `spdx not in expected`; keep the module-level read.

## Checked
- Read the brief and the full `changes.diff`; confirmed the file list (11 files) matches the hunks and every hunk maps to a round-1 finding (F1–F7, F9); no scope creep.
- Round-1 F1 (HIGH) resolved: `pipeline/scoring.py:29-32,104-108` — sets now hold GitHub's unsuffixed ids and `_licence` strips `-only`/`-or-later` before copyleft lookup. Verified against `data/candidate_repos.csv`: 965 data rows; all `license` values within the 13-value set used by `test_actual_candidate_licences`; 0 rows carry `-only`, `-or-later`, `OTHER` or `NONE`; 92 rows (9.5 per cent) are GPL-3.0/AGPL-3.0/LGPL-3.0/MPL-2.0. Tests `tests/test_scoring.py:97-134` cover all 13 CSV values and 18 copyleft variants.
- F2 (row coverage): `pipeline/export.py:34-44,135-141`; round-trip and rejection modes at `tests/test_export.py:88-100,148-186`.
- F3 (compact summaries + full evidence): walked `_summary_fields`, `_summarise_evidence`, `_write_atomic`, `write_listings` (`pipeline/export.py:155-242`); size test (`test_export.py:253-296`) uses >256-character multi-byte text in every position; same-path guard and evidence-directory failure covered at `test_export.py:313-324`.
- F4 (HN null url): `pipeline/sources/hacker_news.py:40-48`; fixture hit 1003 with `url: null`; tests at `tests/test_enrichment.py:127-146`.
- F5 (`absent_statuses`): `pipeline/sources/_enrichment.py:44-72`; HF and HN pass `set()`; 404 mapping per endpoint tested at `test_enrichment.py:103-110`. Docs updated at `docs/scoring.md:32-38`.
- F6 (deps.dev identity): `pipeline/sources/deps_dev.py:28-34`; tests at `test_enrichment.py:113-124`.
- F9 (client closed): `pipeline/http.py:109-121` provides `close`/`__enter__`/`__exit__`; `test_enrichment.py:98-100` uses `with`.
- F7 (docs): `docs/scoring.md` read in full; statements match the code.
- Test counts reconcile: 270 → 283 → 322. Handover reports 322 passed, 98.36 per cent coverage, ruff clean.
- Conventions: British English; type hints; pathlib; no prints; ruff selection unchanged.

## Limits
- Could not run tests, ruff or Python; floating-point assertions and the 8 KiB bound rest on the coordinator's reported run plus reading.
- Could not verify live GitHub `licenseInfo.spdxId` output; the CSV from the phase 0 pull was the ground truth.
- `frozenset` default and Windows `Path.replace` overwrite semantics were checked by reading only.

# Scoring policy v0

The score is a 0–100 weighted mean of evaluated components, using
`SCORE_WEIGHTS_V0` and `SCORE_VERSION` in `pipeline/config.py`. It is a triage
signal for repository discovery. It does not certify security, suitability or
successful execution. Policy changes require a new score version.

| Component | Weight | v0 normalisation to 0–100 |
|---|---:|---|
| Scorecard | 25% | Published 0–10 aggregate multiplied by 10 |
| Advisories | 20% | `100 / (1 + advisory_count)` for explicitly evaluated package evidence |
| Licence | 15% | Recognised permissive: 100; weak copyleft: 80; strong copyleft: 60 |
| Maintenance | 15% | `max(0, 100 * (1 - days_since_push / 365))` |
| Release cadence | 10% | Lower of release freshness and `100 * min(1, 30 / mean_interval_days)` |
| Contributors | 10% | `min(100, contributor_count * 10)` |
| Hacker News | 5% | `min(100, mention_count * 20)` within the observed 30-day window |
| Stars | 0% | Stored in repository metadata and diagnostics; never used for ranking |
| Star velocity | 0% | Retained in diagnostics in stars/hour; never used for ranking |

`total = sum(weight * component) / evaluated_weight` and
`coverage = evaluated_weight / all_positive_weight`. Coverage is a fraction
between 0 and 1, independent of the normalised total. For example, Scorecard 8/10
on its own produces total 80 and coverage 0.25. Do not present that result as
fully evaluated. A low evaluated value, including zero, still counts as coverage.
No evaluated components produces `total: null`, `coverage: 0`; that repository
is excluded from the listing rows but its diagnostics remain in the export.

## Evidence semantics and limits

- `present`: the requested observation was obtained and validated.
- `absent`: HTTP 404, no confirmed search matches in a complete bounded result,
  or missing GitHub metadata. Its weight is excluded.
- `unsupported`: this host, field or classification cannot be evaluated by the
  current source. Its weight is excluded.
- `failed`: network failure, a non-404 HTTP error, invalid response, incomplete
  search, future observation or malformed scoring input. Its weight is excluded
  and `failed_components` names affected scoring components. Raw source evidence
  remains available, including failures in unweighted Hugging Face checks.

Each adapter exposes `fetch(repo, http, *, fetched_at=None) -> Evidence`. Supply
the shared B1 `HttpClient` and `Budget`. Each supported repository makes one
lookup per adapter, plus any bounded retries. Every actual attempt is charged;
`BudgetExceeded` propagates and must abort the run. Unsupported hosts need no
request. Do not infer an ecosystem from a repository's primary language.

The [deps.dev project endpoint](https://docs.deps.dev/api/v3/#getproject) returns
project metadata, not package-version advisories. The adapter reports project
presence separately from `advisories_status: unsupported` and
`advisory_count: null`. Neither a known project nor a missing response means
zero vulnerabilities. The scoring contract accepts a future, separately verified
package assessment only when `advisories_status` is explicitly `present` and
`advisory_count` is a non-negative integer. Package resolution and such assessment
are not implemented by these tasks; ordinary T04 output leaves this 20% unevaluated.

B1 provides one `latestRelease`. That cannot establish cadence. The scorer
accepts optional `release_history` timestamps, deduplicates them and includes the
latest release. At least two distinct release dates are required; one date means
`unsupported`, none means `absent`. Mean interval is elapsed days from first to
last divided by interval count. Release freshness uses the maintenance formula
above with the latest release date. Future dates or dates preceding repository
creation fail the component. These tasks do not fetch release history, so B1
alone leaves this 10% unevaluated too.

Licence classes are an explicit discovery policy, not a legal assessment.
Recognised permissive identifiers are MIT, Apache-2.0, BSD-2-Clause,
BSD-3-Clause, ISC, 0BSD, Unlicense, CC0-1.0, Zlib and BSL-1.0. Weak copyleft
includes MPL-2.0, EPL-1.0/2.0 and LGPL-2.0/2.1/3.0 (`-only` or `-or-later`).
Strong copyleft includes GPL-2.0/3.0 and AGPL-3.0 (`-only` or `-or-later`).
Unrecognised identifiers/expressions are unsupported; null, empty, NONE and
NOASSERTION are absent. No terms are inferred from unknown identifiers.

The default contributor count is GitHub's `mentionableUsers` proxy, not a count
of proven contributors. The B1 opt-in REST fallback retains its provenance in
`RepoRecord.contributor_source`.

[Hugging Face full-text search](https://huggingface.co/docs/hub/search) searches
multiple content types. One combined query inspects at most 100 candidates;
only model/Space README text containing an exact repository URL qualifies.
The observed JSON web API is not a versioned guarantee. Schema drift fails
closed. Dataset hits, Space source-code hits, name-only matches and repository
prefix collisions do not establish a card link. Truncation with no confirmed
link fails; a confirmed link can be present with `search_truncated: true`.
Links are unweighted and assert neither functionality nor compatibility.

[HN Algolia search](https://hn.algolia.com/api) counts distinct story IDs with
URLs pointing to the repository or a path within it, within the inclusive
30-day UTC interval. It does not count arbitrary comments or articles that
mention the repository elsewhere. The highest-point qualifying story is the
top item (recency then ID break ties). At most 1,000 candidates are inspected;
incomplete/approximate results fail instead of supplying partial counts. Empty
searches are absent, not an evaluated zero for the scoring denominator.

## Integration and export

```python
result = score_repo(repo, evidence, run_id=run_id, now=observed_at,
                    velocity=store.velocity(repo.github_id, window_hours=168))
store.add_score(result.score)
document = build_listings(repos, results, run_id=run_id, generated_at=observed_at)
write_listings(document)
```

`score_repo` returns `ScoringResult(score, details)`; `score` is the unchanged
B1 `Score`. The `details` object preserves component statuses, failed components,
licence class, raw stars/velocity and source evidence. B1 SQLite stores scores
and snapshots; these new diagnostics persist in exported JSON, not in new
database columns. There are no changes to B1 public signatures or migrations.

`pipeline.export.Listings` validates the envelope: `generated_at`,
`score_version`, `run_id`, `listings` (B1 `Listing` rows) and `scoring_details`
(diagnostics keyed by GitHub ID). Identity, run/version, failure flags and
component-status consistency are checked. CSV labels are joined case-insensitively
by current GitHub `full_name` from `data/labelled_repos_for_review.csv`.
Matching rows are always `provisional`, regardless of confidence. Missing rows
have null topic/level and `pending`. Invalid categories, duplicate names,
missing columns or a missing CSV fail export; no labels are silently invented.

Rows sort by descending total then descending push time, with unknown push
times last. Name and stable ID break remaining ties. Raw stars and velocity
never break ties. All rows explicitly have `tested: untested` and
`unevaluated_checks: ["fake_stars", "typosquat", "sandbox_test"]`.

`write_listings` validates before atomically replacing
`site/src/data/listings.json`; pass a different path for a dry run. No canonical
state is promoted, release uploaded or site deployed by scoring/export.

# Curated layer — Task 4.2 verification

Completed 2026-10-21. No raw, staging, provenance, manifest, governing-document, acquisition or ingestion file was modified. No data was downloaded, no dependencies installed, and no commit or push occurred. Milestone 5 was not started.

## Structure and decisions

The curated artifact is `data/local/ttc_curated.sqlite3` (Git-ignored), separate from `data/local/ttc.sqlite3`. This is the same SQLite engine, not a second storage engine. Staging is attached with URI `mode=ro` for the build and stays byte-for-byte unchanged. This avoids changing the storage foundation schema or its exact-schema validation and keeps subsequent staging ingestion compatible.

Three materialized tables are defined in `sql/curated_schema.sql`:

- `curated_metadata`: rules version, exact canonical selection, cleaning-specification hash and implementation hash.
- `curated_selection`: one explicitly selected snapshot per supplied mode/resource, including snapshot ID, resource ID, raw checksum and staged receipt count.
- `curated_records`: one row per selected `(snapshot_id, record_ordinal)`, retaining all eleven original strings plus parsed fields, statuses, quality flags and analysis-specific eligibility. Its local foreign key points to curated_selection. Cross-file staging lineage is verified explicitly because SQLite foreign keys do not span attached databases.

`sql/build_curated.sql` implements the transformation as a single INSERT/CTE SELECT with a window count for duplicate groups. Python registers narrowly scoped deterministic date/time/number validation functions during the build because permissive casts are not the contract. All record shaping, flags, group sizes and eligibility expressions are SQL. Consumers can read the materialized tables with ordinary SQLite; no UDF installation is needed after building. Materialization also allows validation before atomic publication.

Snapshot selection comes only from `config/curated_snapshots.json`: original Subway/Bus/Streetcar/LRT snapshot IDs 1/2/3/4, each checked against its exact resource ID and checksum. No MAX(timestamp), inferred latest version or automatic inclusion of other snapshots is used. The explicit scope begins 2025-01-01 with no imposed end date; observed coverage is not extended or zero-filled. The builder also accepts an explicitly configured subset for controlled offline tests; the delivered configuration selects all four modes.

A temporary output database is built transactionally, reconciled, closed and atomically replaces only an owned curated artifact after validation. Staging cannot be used as the output path. Unrelated existing output databases are rejected. A failed build leaves the previous curated artifact intact. Output content contains no wall-clock build timestamp, so unchanged selected inputs, rules and implementation produce identical bytes.

## Deliberately unresolved semantics

- No version-pinned code dictionary is preserved in the project. Under Task 4.1, nonblank codes therefore have `code_status=not_evaluated`, blank codes have missing status, descriptions stay NULL and description_eligible is false. Do not interpret these statuses as known-unmapped or reuse Task 4.1 hypothetical description counts as implemented output. Raw-code frequency eligibility is retained.
- Original Day is preserved. Derived weekday is calendar-based on parsed source Date; conflicts are flags, not corrections. `weekday_exploratory_eligible` supports explicitly provisional date-derived checks, and `weekday_conflict_excluded_eligible` supports the documented sensitivity excluding conflicts. A missing reported Day does not itself establish a conflict; the sensitivity is still exploratory. `validated_weekday_eligible` is always false pending calendar/service-day clarification.
- Line/Station/Bound/Vehicle are not normalized or mapped. Canonical route eligibility remains false; raw nonblank labels remain eligible as reported labels. Non-cardinal direction, slash-containing Line, 22-character Station and Vehicle text 0 are review-candidate flags, not declarations of error.
- Min Gap raw text is preserved, with a separately parsed gap_value and `gap_semantic_status=unresolved`. Gap<Delay is a flag only. Gap is never added to delay.
- Exact finite numeric values are stored as SQLite INTEGER where possible, otherwise REAL only if `Decimal.from_float` proves exact representation. A finite value such as 0.1 that cannot be represented without rounding fails the whole build with a clear message; it is not excluded, clamped or rounded. Current integer inputs are all representable. Extending numeric representation requires a separately justified change; no new semantic exclusion rule was introduced.
- Blanks/invalid date, time or duration text yield NULL derived values and distinct statuses, never numeric zero. Parsed negative delays stay negative and are ineligible only for valid-delay-minute sums. Long-duration thresholds >60/>120/>1440 are flags, not exclusions. Duplicate candidates remain records.

## Eligibility contract

There is no global clean-record filter. `incident_count_eligible` counts source records regardless of code, time, route or duration usability; `scope_eligible` additionally requires a parsed Date in the configured period. Delay-minute eligibility requires valid finite nonnegative delay, including zero. Hour eligibility requires valid HH:MM. Raw Line/Code eligibility requires a nonblank source value. Corresponding scoped flags combine each field-specific condition with scope_eligible. Description/canonical-route/validated-weekday eligibility is withheld as described above. Consumers must choose the metric-specific and scoped flags they require; missing categories remain separately accountable rather than disappear from totals.

## Executed commands

```sh
python3 -m unittest discover -s tests -v
python3 scripts/build_curated.py --selection config/curated_snapshots.json --report reports/curated_verification.json
python3 scripts/build_curated.py --selection config/curated_snapshots.json --report reports/curated_repeat_verification.json
python3 /tmp/ttc_verify_curated_independent.py
```

An initial test run exposed a missing URI-enable flag on the SQLite connection; it was corrected before successful builds. The final suite passes all **38 tests** (11 new curated tests and 27 existing tests). Tests cover strict calendar/time/numeric parsing, zero/blank preservation, invalid and negative values, weekday conflicts, duplicate retention, exact raw strings, separate eligibility, scoped eligibility without row deletion, wrong-checksum rejection, version isolation, deterministic rebuilds, read-only staging compatibility, safe output paths and refusal to round unrepresentable decimals. All tests are offline and use temporary fixtures.

## Actual database reconciliation

| Mode | Selected staged = curated rows | Eligible incident / delay / hour rows | Named raw Line eligible | Nonblank raw Code eligible | Description eligible |
|---|---:|---:|---:|---:|---:|
| Subway | 45,475 | 45,475 / 45,475 / 45,475 | 45,298 | 45,475 | 0 |
| Bus | 102,257 | 102,257 / 102,257 / 102,257 | 101,016 | 102,257 | 0 |
| Streetcar | 23,703 | 23,703 / 23,703 / 23,703 | 23,351 | 23,702 | 0 |
| LRT | 4,569 | 4,569 / 4,569 / 4,569 | 4,562 | 4,569 | 0 |

All current rows also pass the configured date scope. These are source-record eligibility counts, not independent verification of real-world incidents or reporting completeness.

| Mode | Zero delays retained | Weekday conflicts flagged | Duplicate-candidate rows retained | Blank Line / Bound / Code | >60 / >120 minute flags |
|---|---:|---:|---:|---|---|
| Subway | 29,669 | 63 | 132 | 177 / 15860 / 0 | 110 / 41 |
| Bus | 12,974 | 130 | 595 | 1241 / 21327 / 0 | 4209 / 2220 |
| Streetcar | 5,279 | 42 | 36 | 352 / 5327 / 1 | 1188 / 365 |
| LRT | 1,908 | 420 | 7 | 7 / 773 / 0 | 110 / 46 |

Total: **176,004 staged = 176,004 curated rows**, with 49,830 zeros, 655 weekday conflicts and all 770 duplicate-candidate records retained. No current date/time/delay is invalid or missing; no negative delay occurs. All 176,003 nonblank codes remain not_evaluated; one blank Streetcar Code remains missing. There are zero >1440-minute delay flags. The numeric delay sum is 2,740,515, equal to the selected source sum; this is reconciliation, not a service-reliability finding.

Builder checks compare all eleven original strings and source row keys using staging joins, verify no missing/extra/unselected rows, reconcile each selection with its receipt count, and check integrity/foreign keys in both databases. The independent read-only audit traversed every joined source/curated row (1,936,044 original string values), separately checked actual parsed dates/times, numeric equality, English calendar weekdays and core eligibility, and recomputed duplicate-group sizes from staged non-ID fields. It did not substitute historical profile numbers for actual database results.

Both databases passed integrity checks (`ok`) and foreign-key checks (zero violations). All prior files, including the **entire staging database**, raw files and provenance, match pre-task hashes. No original source or existing record was rewritten.

Two executed builds returned identical verification reports and artifact bytes. Curated SHA-256: `70e25ed9fd6ba4c6516f957e0fcfa0b825b5d4337ab7cb8203729fdf19bb5f31`. Staging SHA-256 remains `dec4388766ce094eb4616d2b61829b65bdb00ceeaa05827cf71d7aa01aba6f21`. SQL consumers can read the artifact without loading Python parser functions.

## Files created

- `config/curated_snapshots.json` — explicit selected resource/snapshot/checksum set and scope.
- `sql/curated_schema.sql`, `sql/build_curated.sql` — materialized curated definitions and SQL transformation.
- `scripts/build_curated.py` — strict parsing helpers, guarded build and reconciliation.
- `tests/test_curated_layer.py` — deterministic offline tests.
- `reports/curated_verification.json`, `reports/curated_repeat_verification.json` — actual executed build results.
- `reports/curated_layer_verification.md` — this structure/verification/limitations report.
- `data/local/ttc_curated.sqlite3` — ignored, reproducible materialized artifact.

No pre-existing project file was modified. Operational definitions, code dictionaries, source-calendar authority, LRT reporting completeness, physical vehicle/route identity and historical revision practices remain unresolved. The curated layer preserves and exposes these limitations; it does not resolve them. Stop after Task 4.2 for review.

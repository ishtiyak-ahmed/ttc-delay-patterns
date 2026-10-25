# Core analytical SQL

Run from the repository root with Python's standard library:

```sh
python3 scripts/run_core_analysis.py --output results/core_analysis
python3 -m unittest discover -s tests -v
```

The output directory must not already exist. For a repeat run, choose another directory and compare artifacts. The executor opens the curated and staging databases read-only, checks the explicitly pinned `config/curated_snapshots.json` against both curated selection structures and staging snapshot identities, checks lineage, executes every `.sql` file here twice, reconciles compatible aggregations, then exports. No database objects or records are created or changed. Each query is also independently executable against the curated database without Python UDFs.

## Measures and dimensions

- `recorded_incidents`: COUNT of scope-eligible, incident-count-eligible source rows. Not DISTINCT `_id`, deduplicated events, or independently verified disruptions.
- `duration_eligible_incidents`: count with `scoped_delay_minutes_eligible=1`. Zero durations qualify; invalid/missing/negative durations do not. All other scoped incidents remain in the incident count and in `duration_ineligible_incidents`.
- `recorded_delay_minutes`: SUM of eligible durations. An all-unavailable group has NULL, never zero.
- `average_recorded_minutes`: eligible SUM / eligible count. Includes zero-minute incidents; unavailable/negative values are excluded only from duration measures.
- `median_recorded_minutes`: middle eligible duration, averaging the two middle durations for even counts. SQL window ordering is deterministic, including source-row keys for ties. Never average subgroup medians to obtain an overall median.
- `zero_minute_incidents` and `positive_minute_incidents`: disjoint eligible-duration partitions. `zero_minute_share` = zero / duration-eligible count, NULL if that denominator is zero. It is not a service failure probability.
- `observed_dates`: DISTINCT parsed dates with records in the group. Distinct-date counts, medians, averages and shares are not additive. Sum counts/minutes only across compatible, nonoverlapping groups.

All outputs keep `source_mode`. Exact nonblank `line_raw` and `code_raw` values are grouped separately within each mode. Rankings use RANK, so ties share a rank. There are no canonical mappings or inferred code descriptions. Monthly and hourly outputs include zero counts/shares as well as frequency and duration measures. `weekday_hour` has two **alternative** exploratory variants: all date-derived weekdays, and conflict-excluded sensitivity. Never sum these variants together. Neither is source-validated weekday behaviour; no source day/time semantics have been resolved by these queries.

`eligibility_audit` includes all selected records, scope exclusions, unallocated hours, duration issues, and named-label/code exclusions including their recorded minutes. `coverage` and `dates_without_records` show observed bounds and internal gaps, without constructing zero-incident periods. There is no scheduled-trip, passenger, operating-day or service-volume denominator.

## Export contract

Each query exports an ordered UTF-8 CSV. `results.json` is the authoritative typed representation: SQL NULL is JSON null; CSV empty cells mean SQL NULL. CSV consumers should import raw labels as text, preserving their exact representation. A header is written even for an empty result. `manifest.json` records query/tool hashes, curated artifact checksum, explicit snapshots/scope, result columns/counts, export checksums and verification results. Fixed inputs and code produce identical bytes; no wall-clock timestamp is inserted. Exports are aggregates and cannot alone recover row lineage; the pinned curated artifact retains `(snapshot_id, record_ordinal)` back to staging and immutable raw snapshots.

# Monthly temporal evidence — Task 5.3

```sh
python3 scripts/run_temporal_analysis.py --output results/temporal_persistence
python3 -m unittest discover -s tests -v
```

Choose a new output directory for a rerun; exports refuse overwrite. The two standalone SQL queries read the existing curated artifact, requiring no UDFs or database writes. The Python executor reuses the core executor for explicit snapshot/receipt/lineage/integrity checks and compatible totals, then executes each monthly query twice and independently accumulates headline values from actual curated rows. Original core outputs are not regenerated or replaced.

Grain: mode × parsed calendar month × exact eligible raw Code or Line. `category_eligible=0, category_raw=NULL` is an explicit ineligible/missing category bucket, not a made-up raw label. It is included for reconciliation and has no named-category rank. All original raw values remain recoverable in curated/staging data. Nonblank labels, including unusual labels, are not normalized. Named category ranks use RANK with ties and exclude the missing bucket. A category with no eligible minutes has NULL minute rank.

`recorded_incidents` counts incident-count-eligible, scope-eligible source rows. `duration_eligible_incidents` requires the scoped numeric-duration flag. `duration_ineligible_incidents` retains the difference. Zero-minute records contribute to counts and eligible denominators, with zero minutes. Missing/invalid/negative durations contribute no eligible minutes; an all-unavailable group's SUM is NULL. Positive-duration thresholds >60 and >120 follow the existing descriptive flags and are nested subsets, never additive to each other. Duplicate-candidate values are diagnostic subsets, not records removed from primary measures.

Incident share divides category records by **all** scoped mode-month records, including missing categories. Minute share divides eligible category minutes by **all** scoped mode-month eligible minutes, including missing categories; it is NULL if the numerator is unavailable or the denominator is unavailable/zero. These shares describe composition, not service-exposure rates. Repeated `mode_month_*` columns are denominator metadata; do not sum them across categories. Likewise, do not sum distinct-date counts across overlapping categories or average shares across months.

Coverage columns show first/last recorded category dates, category observed-date counts, corresponding mode-month counts/bounds and calendar month length. A full observed-date month is not proof of complete reporting. No missing category-month rows are fabricated. Absence means no selected records allocated to that label/month, not no delay/service or nonoperation. Raw-label availability is not verified scheduled-service exposure. LRT December 2025 is partial and January 2026 lacks one observed date; EC has no selected records before February 2026. Expose these differences rather than comparing equal-length service histories.

The code and line profiles are separate marginal aggregations: do not join them on mode/month in a way that multiplies totals or apply unsupported joint line-and-code filters. Use existing grain-specific median/coverage exports where applicable; monthly group medians are not implemented here. CSV empty cells represent SQL NULL, with typed JSON as the authoritative representation. The manifest pins all snapshot identities, source hashes, SQL/tooling hashes, export hashes, independent headline partitions and reconciliation results.

Persistence is evaluated descriptively in `reports/temporal_persistence_evidence.md` using exact month counts and ranges. No inferential significance, causal explanation or reliability score is produced.

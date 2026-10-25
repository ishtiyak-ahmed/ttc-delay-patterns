# Temporal persistence and final analytical evidence — Task 5.3

## Decision and narrative

The strongest story is now supported across months: **frequency and recorded duration reveal different patterns of recorded TTC disruption, and select different investigation priorities.** Lead with Bus’s persistent duration concentration and its overlap with raw code MFDV; explain Subway’s persistent zero-minute composition; then show that monthly line leadership can change despite an overall ranking. These remain descriptive source-record findings, not verified causes, exposure-adjusted reliability or passenger impact.

This companion updates the provisional evidence in `analytical_viability_review.md` without duplicating or rewriting that historical review. It follows the current working question supplied in Task 5.3. No governing document, source data or pipeline architecture was changed.

## 1. Independent headline verification

The executor iterated actual curated values in `(snapshot_id, record_ordinal)` order, independently of the existing aggregate exports. Filters: `incident_count_eligible=1 AND scope_eligible=1`; scope is parsed Date >= 2025-01-01 with no configured upper limit. Duration tests additionally require `scoped_delay_minutes_eligible=1`. MFDV uses exact `source_mode='bus' AND code_raw='MFDV'`, without dictionary descriptions or incident deduplication. Subway zero share uses eligible duration records. The Bus record denominators below include all scoped Bus records; currently every duration qualifies, so incident and duration-eligible denominators coincide.

| Claim | Exact numerator / denominator | Recomputed result |
| --- | --- | --- |
| Bus >60-minute record share | 4,209 / 102,257 | 4.12% |
| Bus >60-minute recorded-minute share | 853,656 / 2,163,102 | 39.46% |
| Bus MFDV record share | 7,288 / 102,257 | 7.13% |
| Bus MFDV recorded-minute share | 871,387 / 2,163,102 | 40.28% |
| Subway zero-minute share | 29,669 / 45,475 | 65.24% |

All three headline findings match; no correction is necessary. Counts are source records, not DISTINCT `_id` or verified unique real-world events. Zero records remain countable; missing/invalid/negative durations remain countable incidents but cannot contribute eligible minutes. An all-unavailable duration group has NULL minutes, not zero. Current selected data have no missing/invalid/negative durations, so there are no such duration exclusions in these headline denominators.

Explicit original snapshot selection (full checksums in the unchanged `config/curated_snapshots.json` and copied into `results/temporal_persistence/manifest.json`):

| Mode | Snapshot | Resource ID | Selected records |
| --- | --- | --- | --- |
| subway | 1 | 0b6e5c52-e993-46d6-8d74-8602ee224457 | 45,475 |
| bus | 2 | b5725365-9252-4bfe-b6f4-cda7ddf74341 | 102,257 |
| streetcar | 3 | cf2fdd12-6f0e-4644-aae7-0bbfc31df031 | 23,703 |
| lrt | 4 | 9a800c92-0362-4cee-8232-7374596b6a43 | 4,569 |

Curated artifact SHA-256: `70e25ed9fd6ba4c6516f957e0fcfa0b825b5d4337ab7cb8203729fdf19bb5f31`. Selection is checked against curated metadata, curated_selection and staging resource/checksum identities, not inferred from ingestion timestamps. All 176,004 selected records trace to staging.

### Bus overlap: one disjoint partition, no double-counting

Independent audit source: `headline_audit()` in `scripts/run_temporal_analysis.py`; machine-readable result: manifest `headlines.bus_disjoint_partitions`. The code query also reproduces the MFDV >60 subset by summing its monthly over60 fields.

| Disjoint Bus group | Records | Eligible recorded minutes |
| --- | --- | --- |
| other__not_over60 | 94,535 | 1,215,228 |
| MFDV__over60 | 3,775 | 777,169 |
| MFDV__not_over60 | 3,513 | 94,218 |
| other__over60 | 434 | 76,487 |

The intersection is **3,775 records and 777,169 minutes**: 89.69% of >60-minute Bus records and 91.04% of that group’s recorded minutes. MFDV and the long-duration group are substantially overlapping views, not independent populations or two additive impacts. Their union is **7,722 records and 947,874 minutes**, calculated by adding the three qualifying disjoint groups once. The four partition rows sum to exactly 102,257 records and 2,163,102 minutes. The `not_over60` labels include all other duration states in principle; current durations are all valid.

## 2. Persistence criteria and coverage

The following terminology describes the selected snapshots only. It is not a hypothesis test, confidence interval or forecast:

- **Persistent across observed months:** state the precise property and require it to hold in every evaluated month. Presence, leading rank and a majority share are different properties. We report exact `k/N`, share/rank ranges and exceptions rather than assign an unqualified “persistent” label to a category. Leading means RANK=1, retaining ties. A majority means >50% by definition, not a chosen risk threshold. Where leadership is frequent but not universal, report `k/N` explicitly without pretending universal persistence.
- **Concentrated in a limited period:** name the actual interval and property (for example leadership confined to one phase), with month counts and exceptions. Presence outside that phase prevents calling the category itself absent or isolated. No universal 70%/80% persistence cutoff is imposed; a phase-specific rank pattern does not demonstrate a structural or reporting change.
- **Inconclusive because of insufficient/uneven coverage:** withhold a common-exposure or stable full-span comparison if the categories start at different times or observed-date coverage differs materially. Show the full-span and common-calendar-window results without treating the latter as matched service exposure. Do not fabricate absent category-month records as zero-delay service.

Subway, Bus and Streetcar each have records on all calendar dates in all 20 months, January 2025–August 2026. This is an observed-date check, not proof of complete reporting. LRT has nine observed months: December 2025 has 25/31 dates, January 2026 has 30/31 (2026-01-23 absent), and February–August have all mode-level dates. Show those two coverage-limited months separately; seven months meet the full calendar-date observation check. Category-date coverage can still differ within those seven months. No analysis converts calendar days or observed dates into an assumed service-exposure denominator.

## 3. Monthly raw-code evidence

Source: `sql/analysis/persistence/monthly_codes.sql` → `results/temporal_persistence/monthly_codes.csv` and typed `results.json`. Shares use all mode-month records/minutes, including the missing-code bucket. Named-category ranks exclude that bucket.

| Mode | Raw Code | Months present | Count rank 1 | Minute rank 1 | Monthly mode-minute share range |
| --- | --- | --- | --- | --- | --- |
| bus | MFDV | 20/20 | 2/20 | 20/20 | 29.05%–50.33% |
| bus | EFO | 20/20 | 15/20 | 0/20 | 2.25%–17.42% |
| subway | MUIS | 20/20 | 1/20 | 0/20 | 0.00%–0.78% |
| subway | SUDP | 20/20 | 16/20 | 13/20 | 5.73%–17.13% |
| streetcar | MTDV | 20/20 | 9/20 | 19/20 | 14.68%–33.53% |
| lrt | EXO | 9/9 | 2/9 | 0/9 | 4.86%–12.97% |
| lrt | PXSW | 9/9 | 0/9 | 4/9 | 8.21%–29.26% |

- **Bus MFDV:** recorded-minute leader in **20/20** months, with 29.05%–50.33% of monthly Bus minutes. Its count rank varies 1–5; monthly record share 5.88%–9.17%. The duration-heavy profile is persistent, not generated by one isolated month. Summed across codes, >60-minute Bus records account for 2.82%–5.74% of monthly records but 27.73%–49.37% of monthly minutes, reinforcing the distributional distinction without adding the overlapping populations.
- **Bus EFO:** count leader in **15/20** months, precisely January 2025–March 2026; never count leader in April–August 2026 (ranks 5, 6, 6, 9, 5). It remains present in all months. The prior overall “most frequent” result is correct, but a claim of persistent monthly leadership is weakened. Whether recording practices, source categories or underlying activity changed is unresolved.
- **Subway MUIS:** present and count-ranked 1–3 in **20/20** months, but never a minute leader. Its zero share is 97.79%–100% every month; monthly minute share never exceeds 0.78%. Separately, Subway’s overall zero share is 59.67%–72.75% in all 20 months. The zero-heavy count composition is persistent; no claim of zero passenger impact follows.
- **Subway SUDP:** count leader in 16/20 and minute leader in 13/20, with minute rank always 1–3. **Streetcar MTDV:** minute leader in 19/20 (February 2025 rank 2), versus count leader in 9/20. These are recurring, explicitly non-universal leadership patterns within their own modes, not shared causes.
- **LRT EXO/PXSW:** present 9/9; PXSW leads minutes in 4/9 months, EXO in none. Both have varying ranks and a shorter, uneven beginning. Treat them as supporting exploration, not as evidence of stable mode-wide code leadership.

Bus duplicate-candidate rows contribute 8,358 minutes (0.39% of total Bus minutes); all remain in the primary measures. Records >120 minutes contribute 676,994 minutes (31.30% of Bus minutes), nested within the >60 group. Duration concentration is therefore intrinsically sensitive to long recorded values and their source definition. These diagnostics neither validate their operational meaning nor justify trimming them. No deduplicated or capped estimate has been substituted.

## 4. Monthly raw-route/line evidence

Source: `sql/analysis/persistence/monthly_lines.sql` → `results/temporal_persistence/monthly_lines.csv` and typed `results.json`. Labels remain exact, mode-scoped reported strings.

| Mode | Raw Line | Months present | Count rank 1 | Minute rank 1 | Minute rank range when present |
| --- | --- | --- | --- | --- | --- |
| bus | 52 LAWRENCE WEST | 20/20 | 6/20 | 2/20 | 1–16 |
| subway | YU | 20/20 | 20/20 | 17/20 | 1–2 |
| subway | BD | 20/20 | 0/20 | 3/20 | 1–2 |
| streetcar | 504 KING | 20/20 | 9/20 | 11/20 | 1–4 |
| streetcar | 501 QUEEN | 20/20 | 9/20 | 6/20 | 1–5 |
| lrt | EC | 7/9 | 7/9 | 6/9 | 1–2 |
| lrt | FW | 9/9 | 2/9 | 3/9 | 1–2 |

- **Subway YU** leads record counts in 20/20 months and recorded minutes in 17/20. **BD** leads minutes in March 2025, March 2026 and April 2026, while YU remains the count leader. Monthly count and minute leadership therefore differ in exactly 3/20 observed months. This is a defensible route/line example of metric choice, without asserting that either line is less reliable.
- **Bus 52 LAWRENCE WEST** is first overall in both counts and minutes, but leads monthly counts in only 6/20 and minutes in 2/20. Minute rank spans 1–16; July 2026 count rank is 13 and minute rank 16. It appears in all months, so the weakened claim is stable leadership, not recorded presence. A single overall ranking hides that variation.
- **Streetcar 504 KING** leads counts in 9/20 and minutes in 11/20; **501 QUEEN** leads counts in 9/20 and minutes in 6/20. Both appear 20/20. This supports recurring activity with variable leadership, rather than one universally dominant label.
- **LRT’s aggregate EC/FW rank reversal is weakened substantially by coverage.** EC first appears in February 2026 (21/28 observed category dates); FW has records from December 2025 onward. EC leads counts in all seven common observed months and minutes in six. Across February–August alone, EC has 2,743 records/19,256 minutes versus FW’s 1,072/10,869. The full-span near-tie (19,256 vs 19,324 minutes) combines unequal histories, so it should not be a main comparative finding. Even the common calendar window is not matched reporting/service exposure: FW has fewer observed dates in several months, and February EC begins partway through the month. The source does not establish service start dates or absence of service from missing records.

## 5. Final evidence matrix and editorial recommendation

The strongest final set has three main findings, with two supporting investigations. Code and duration views of the same Bus records form one connected finding, not two independent headline effects.

| Place | Precise claim and numerical support | Temporal evidence / SQL and export | Visual | Interpretation and limitation |
| --- | --- | --- | --- | --- |
| Main 1 | Bus duration concentration overlaps MFDV: >60 = 4,209 records/853,656 min; MFDV = 7,288/871,387; intersection 3,775/777,169. | MFDV minute rank 1 in 20/20; monthly share 29.05%–50.33%. monthly_codes.sql / monthly_codes.csv; manifest.headlines. | Aligned monthly code shares plus record-share/minute-share duration bars; overlap annotation. | Investigate recording definitions and long-duration profile. Unknown code meaning, extreme-value semantics and overlapping records preclude cause or passenger-impact claims. |
| Main 2 | Subway 29,669/45,475 = 65.24% zero minutes; MUIS 4,217/4,263 = 98.92%. | Subway zeros exceed half in 20/20 months; MUIS zero share 97.79%–100%. monthly_codes.csv + existing core monthly.csv/mode_summary.csv. | Monthly zero/positive composition with separate total count and minute panels. | Counts describe a wider reporting population than positive durations. Zero is not missing and does not prove no impact. |
| Main 3 | Subway YU count leader in 20/20; BD minute leader in three months despite lower count ranking. | BD minute leadership in 2025-03, 2026-03, 2026-04. monthly_lines.sql / monthly_lines.csv. | Monthly paired count/minute share panels for exact YU/BD labels. | Shows priorities differ within one mode across months; raw totals lack service-exposure denominators. |
| Support / temporal qualification | EFO count leader in first 15 months, none of final five; MFDV minute leader throughout. | EFO present 20/20, count ranks 5/6/6/9/5 in Apr–Aug 2026. monthly_codes.csv. | Monthly category rank or share timeline annotated with observed interval. | Motivates checking recording/category context, not asserting an intervention, causal shift or statistically established break. |
| Supporting dashboard / caution | Bus 52 label first overall but monthly minute leader only 2/20; LRT full-span near-tie has unequal histories. | Bus minute ranks 1–16; LRT EC/FW common-window totals 19,256 vs 10,869. monthly_lines.csv. | Raw-label month profiles with date-coverage columns; LRT visibly separate. | Weakens static leader and LRT rank-reversal stories. No canonical mapping or reliability ranking. |

The main report can now move from a broad catalogue of “when/where/how” rankings to an evidence chain: **define what a record measures → show persistent frequency/duration differences → demonstrate why period and label selection matter → identify bounded investigation priorities**. Engineering then explains why these results can be traced and reproduced. Do not require all modes to supply equally strong headlines. No additional source or architectural change is necessary for this narrative. Power BI preparation may follow review, with filters restricted to the export grain; separate code and line aggregates do not support arbitrary joint filtering, recombined medians or additive distinct-date counts.

## 6. Reconciliation, tests and files

Executed commands:

```sh
python3 -m unittest discover -s tests -v
python3 scripts/run_temporal_analysis.py --output results/temporal_persistence
python3 scripts/run_temporal_analysis.py --output /tmp/ttc53-repeat-export
```

An earlier development export was moved to `/tmp/ttc53-development-export` before the final export. Original Task 5.1 exports were never overwritten. Additional inline Python independently checked export/query checksums, compared complete final export bytes, reconciled Bus overlap subsets to the monthly code query, recomputed report arithmetic and compared all pre-existing project file hashes. No network, ingestion, transformation, database mutation, commit or push occurred.

- **49 tests pass**, including six new offline tests: category shares with missing/invalid values; all-unknown and zero-minute denominators; ties, partial coverage and duplicate retention; version isolation/wrong selection; disjoint Bus overlap; deterministic exports and overwrite refusal. Tests use disposable fixtures only.
- Both profiles cover the same **69 mode-months** as existing monthly outputs. Category partitions include every selected incident: 176,004; eligible minutes sum to 2,740,515; zeros sum to 49,830 in each separate profile. They are alternative aggregations and must never be added together.
- Monthly counts/minutes/eligible counts/ineligible counts/zeros/duplicate candidates reconcile to actual recomputed core queries. Full-period eligible category counts/minutes reconcile to existing raw-code/raw-line queries. All 1,777 missing-line records and the one missing-code record remain in explicit buckets; raw-label rankings exclude only those ineligible buckets.
- Original Task 5.1 export values also reconcile; valid staging lineage count is 176,004. SQLite integrity is `ok`, foreign-key violations zero. Explicit selected snapshot identities match. Both queries run twice internally; two final exports are byte-identical.
- All 83 pre-existing project files remain unchanged, including raw snapshots, provenance, staging/curated SQLite files, governing documents and prior analytical outputs. Verification details and original-data hashes are in `reports/temporal_persistence_verification.json`; machine-readable headline partitions, query/selection/output hashes and reconciliation checks are in the new export manifest.

Created: `sql/analysis/persistence/monthly_codes.sql`, `monthly_lines.sql`, `README.md`; `scripts/run_temporal_analysis.py`; `tests/test_temporal_analysis.py`; two CSVs plus `results.json`/`manifest.json` under `results/temporal_persistence/`; this report; `reports/temporal_persistence_verification.json`. No pre-existing file was modified. The six new fixture tests do not alter real TTC datasets. No next milestone or Power BI implementation has started.

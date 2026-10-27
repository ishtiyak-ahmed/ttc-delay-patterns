# Final Power BI data contract — Milestone 5

**TTC Delay Patterns: Why Incident Frequency and Recorded Duration Tell Different Stories.** Contract `milestone5-v1`, prepared 2026-10-21. This is a verified data/model handoff, not an implemented Power BI report. The narrative emphasizes recorded-minute concentration, differences in frequency/duration rankings, and monthly persistence or variation. Engineering provides the reproducible evidence behind those claims.

## 1. Export audit and minimum change

Task 5.1 monthly measures and Task 5.3 monthly raw-code/raw-line profiles already supply the analytical measures and persistence evidence. Their original CSVs remain valid research outputs. Importing them all unchanged into one model would duplicate populations and expose repeated mode-month denominators, precomputed shares/ranks, overlapping date counts and incompatible medians. They must not be appended as extra incidents.

The final bundle projects the existing monthly/code/line outputs, extracts dimensions, removes repeated denominators and derived measures, and adds only one new analytical SQL query: `sql/power_bi/monthly_duration.sql`. Its disjoint monthly duration-band × literal Bus-MFDV partition supports both time-filterable duration distribution and the overlap disclosure. There is no separate overlapping MFDV/long-duration population to append.

Not imported: overall mode/raw-code/raw-line summaries (derivable from monthly facts); stored monthly ranks/shares/averages; hourly and provisional weekday profiles (outside the final narrative); overall duration summaries (replaced by their monthly partition); grouped medians (cannot combine across filters). Coverage/eligibility context and gap dates are reused in the final bundle. These source exports remain unchanged, with checksums pinned by the new manifest.

## 2. Final inventory and grain

Load only the ten CSVs in `results/power_bi/`. `results.json` is their typed equivalent for audit, and `manifest.json` provides column order, row counts, input/output hashes, explicit snapshot selection and executed verification. Do not load JSON as additional facts.

| CSV / model table | Unique grain / key | Actual rows | Role |
|---|---|---:|---|
| `dim_mode.csv` / DimMode | `source_mode` | 4 | Mode, selected snapshot provenance and full-snapshot context |
| `dim_month.csv` / DimMonth | `month_start` | 20 | Month-level date dimension; January 2025–August 2026 |
| `dim_code.csv` / DimCode | `code_key` | 479 | Exact mode-scoped Code, including one missing bucket |
| `dim_line.csv` / DimLine | `line_key` | 909 | Exact mode-scoped Line, including four missing buckets |
| `dim_duration_band.csv` / DimDurationBand | `duration_band` | 8 | Disjoint duration categories and sort/subset flags |
| `fact_month.csv` / FactMonth | `(source_mode, month_start)` | 69 | Overview KPIs, monthly totals, coverage and quality counts |
| `fact_code.csv` / FactCode | `(source_mode, month_start, code_key)` | 4,851 | Code concentration and monthly persistence |
| `fact_line.csv` / FactLine | `(source_mode, month_start, line_key)` | 5,592 | Raw-line concentration and monthly persistence |
| `fact_duration.csv` / FactDuration | `(source_mode, month_start, duration_band, is_bus_mfdv)` | 615 | Distribution, zeros, long-duration concentration and Bus overlap |
| `reporting_gaps.csv` / ReportingGaps | `(source_mode, calendar_date)` | 1 | Internal dates with no selected records, not zero-incident fact rows |

Every primary key is unique and every intended relationship has been checked. Missing category buckets count as records but have no canonical label or inferred code description. All three category/duration facts individually reconcile to FactMonth. They are alternative marginal partitions of the same population, never additive to each other.

### Types and column definitions

Import UTF-8 CSV with explicit types; do not rely on automatic detection. All keys, hashes, resource IDs and raw labels are **Text** (retain leading zeros and whitespace). Date fields are ISO dates parsed as **Date** with an explicit ISO-compatible locale. `month_start` is a period key, not an incident date. `month_label` is Text; year/month numbers, counts, ranks of sort order and 0/1 flags are Whole Number. Minute sums are nullable Decimal Number (current values are exact integers; future source fractions must still satisfy the existing lossless curated numeric contract). CSV empty cells represent SQL NULL; never replace missing minutes with 0. No raw CSV values are cleaned here.

| Fields | Definition / aggregation contract |
|---|---|
| `source_mode` | Exact `bus`, `lrt`, `streetcar`, `subway` logical source; shared filter key. Never interpret summed cross-mode records as a reliability comparison. |
| `month_start`; DimMonth `month_label`, `year`, `month_number` | First of parsed calendar month; label `YYYY-MM`, calendar year and month number. Monthly granularity only. |
| `recorded_incidents` | Count of source rows with incident-count and scope eligibility. Includes zero-minute rows, unknown categories and duplicate candidates. Not unique verified disruptions or DISTINCT `_id`. Additive within one fact across disjoint rows. |
| `duration_eligible_incidents`, `duration_ineligible_incidents` | Nonnegative, valid finite duration count (including zero), and complementary count. Their sum equals recorded incidents. Never use all incidents as an average-duration denominator when eligibility differs. |
| `recorded_delay_minutes` | SUM of eligible numeric Min Delay, unit: recorded minutes. All-unavailable groups remain NULL. Not passenger minutes, elapsed network downtime or nonoverlapping real-world disruption duration. |
| `zero_minute_incidents` | Eligible records whose parsed Min Delay is exactly zero; subset of eligible records, not missing values. |
| FactMonth `observed_dates`, `first_observed_date`, `last_observed_date`, `calendar_month_days` | Distinct parsed dates with selected rows, observed bounds and number of calendar dates in the month. These describe recording coverage, not service exposure. Dates can be summed across disjoint months for a **single mode**; never across modes as distinct calendar dates. |
| FactMonth `weekday_conflicts`, `duplicate_candidate_records` | Retained source weekday/date conflicts and retained non-ID duplicate-candidate rows; not inferred corrections or confirmed duplicate events. Additive record counts. |
| FactMonth `missing_code_incidents`, `missing_line_incidents` | Counts in ineligible/missing raw-category buckets for that mode-month. Match corresponding facts via dimension `category_eligible=0`. Current ineligibility means blank source labels only. |
| `code_key`, `line_key` | SHA-256 of UTF-8 canonical JSON `[mode, category_eligible, exact_raw_label]`, separators `,`/`:`, no ASCII escaping. Mode/eligibility encoded to prevent cross-mode, delimiter or missing-label collisions. Relationship keys, not TTC identifiers. |
| DimCode/DimLine `category_eligible`, `raw_code` / `raw_line` | 1 for nonblank raw category, 0 for the missing bucket; raw field NULL only for that bucket. Original distinct blank strings remain recoverable in curated/staging. Preserve exact nonblank labels. Display missing as an explicitly marked presentation bucket, never overwrite raw values with an invented category/code meaning. |
| DimCode `code_description`, `code_display_label` | Two appended nullable Text attributes. Description is exact publisher text only for a unique, nonblank, encoding-valid mode/code match in the pinned 2026-10-26 reference. Otherwise description is NULL and display remains raw code (or `[Missing code]` for the existing missing bucket). Display prefixes the raw code to preserve code identity. Neither field is a relationship key or cause hierarchy. |
| FactCode/FactLine `category_observed_dates`, `category_first_date`, `category_last_date` | Dates on which that exact category had records in that month. Category dates overlap: do not sum across codes/lines. May sum across nonoverlapping months for one fixed category, with appropriate label. Not proof of dates of service operation. |
| `duration_band`, `sort_order` | Ordered disjoint bands: zero; positive >0–5; >5–15; >15–30; >30–60; >60–120; >120; unavailable_or_ineligible. Only observed fact rows are exported, with all eight dimension members retained. |
| DimDurationBand `is_over60`, `is_zero`, `is_duration_eligible` | Flags for >60 bands, zero band, and all bands except unavailable/ineligible. >60 is an existing descriptive threshold, not a verified severity standard. >120 is nested inside >60, not an extra additive group. |
| FactDuration `is_bus_mfdv` | 1 iff source mode is Bus and exact raw Code is `MFDV`; otherwise 0. Literal membership, not code meaning. This flag is not a general Code dimension or cross-fact filter. |
| ReportingGaps `calendar_date` | Observed internal calendar gap; currently LRT 2026-01-23. `month_start` permits monthly filtering. Absence is not zero-delay service. Does not enumerate dates before/after observed bounds. |

DimMode columns are **full selected-snapshot attributes**, unaffected by a month slicer: `snapshot_id` (local immutable version), `resource_id`, `raw_sha256`; `selected_records`; `first_observed_date`, `last_observed_date`, `observed_dates`, `calendar_span_days`, `dates_without_records_within_span`, `observed_months`; `outside_or_unallocated_scope`; `missing_date`, `invalid_date`, `missing_time`, `invalid_time`, `missing_delay`, `invalid_delay`, `negative_delay_records`; `validated_weekday_records`. These reuse the exact meanings in core `coverage` / `eligibility_audit`. Hide numeric attributes from implicit summation. Show their values as snapshot context for the selected mode, explicitly labelled full snapshot; month-filtered coverage/quality comes from FactMonth. Do not let a narrower date selection relabel full-snapshot quality counts as period counts.

### Snapshot provenance

The manifest embeds the unchanged `config/curated_snapshots.json`: one resource/snapshot/content-checksum per mode, snapshots 1/2/3/4 for Subway/Bus/Streetcar/LRT. DimMode exposes those identities in CSV. The manifest pins curated artifact SHA-256 `70e25ed9fd6ba4c6516f957e0fcfa0b825b5d4337ab7cb8203729fdf19bb5f31`, source manifests, SQL and tooling. The executor verifies selection against actual curated metadata and staging snapshot identity/lineage. No latest-ingestion/retrieval rule or unselected version is used. Aggregated cells trace through selected mode/month/category back to the preserved curated `(snapshot_id, record_ordinal)` records; these CSVs are not row-level lineage tables.

## 3. Power BI relationships and filter propagation

Create these active **one-to-many, single-direction dimension → fact** relationships:

| Dimension key | Many-side tables/columns |
|---|---|
| DimMode[source_mode] | FactMonth, FactCode, FactLine, FactDuration, ReportingGaps `[source_mode]` |
| DimMonth[month_start] | FactMonth, FactCode, FactLine, FactDuration, ReportingGaps `[month_start]` |
| DimCode[code_key] | FactCode[code_key] only |
| DimLine[line_key] | FactLine[line_key] only |
| DimDurationBand[duration_band] | FactDuration[duration_band] only |

Do **not** create relationships between facts; between DimMode and DimCode/DimLine; or between facts using mode/month combinations. Category dimensions retain source_mode as metadata for label context but have no extra relationship path. Do not enable bidirectional or many-to-many filtering. Do not append facts into a combined population. Disable automatic relationship/date-hierarchy creation for this model and retain the explicit monthly dimension.

Mode and month slicers intentionally filter all facts. Code slicers/axes affect only FactCode, line slicers/axes only FactLine, and duration-band/cohort filters only FactDuration. Use category slicers on their own pages, limited to the chosen mode; suppress empty categories. Require one selected mode for rankings and comparative profiles. Never pool routes/codes across modes into one rank. Global totals, if shown, must be labelled inventory across unequal source coverage, not reliability.

Unsupported filter combinations must be prevented in page interactions and guarded in public measures: an overview measure must return BLANK or a clear “unsupported filter” state if a code/line/duration/cohort selection would appear to constrain it; code measures must not respond as though filtered by lines/duration; line measures must not imply code/duration filtering. Shared hidden mode-month denominator measures deliberately ignore category selection through the relationship design. Never wire a cross-highlight that implies joint code-and-line or code-and-duration detail. The only supported code-duration overlap is literal Bus MFDV in FactDuration.

## 4. Measures and aggregation rules

Hide raw numeric columns from casual implicit aggregation; expose named explicit measures with units. The following are model specifications; no PBIX/DAX implementation is delivered in this task. Use prefixes (`Overview`, `Code`, `Line`, `Duration`) so users cannot silently substitute one fact for another.

| Measure | Definition and scope |
|---|---|
| Overview recorded incidents / minutes | `SUM(FactMonth[recorded_incidents])` / `SUM(FactMonth[recorded_delay_minutes])`; mode/month only. Respect unsupported-filter guards above. |
| Code / Line / Duration recorded incidents / minutes | Same sums from their own fact. Named-label analyses filter the relevant dimension `category_eligible=1`; missing-category counts remain separately displayed. |
| Average recorded minutes per eligible incident | `DIVIDE(SUM(fact[recorded_delay_minutes]), SUM(fact[duration_eligible_incidents]))`, for the chosen fact. Includes zero-duration incidents. BLANK for unavailable/zero denominator. Never average subgroup averages. |
| Zero-minute share | `DIVIDE(SUM(fact[zero_minute_incidents]), SUM(fact[duration_eligible_incidents]))`. Report availability/ineligible counts alongside. Never divide by assumed trips or average row shares. |
| Positive-minute incidents | Eligible count minus zero count, from the same fact/filter context. Unknown/negative durations are not positive or zero. |
| Code/Line share of selected mode-period records or minutes | Category-fact numerator / hidden `SUM(FactMonth[recorded_incidents])` or minutes denominator. Denominator includes missing categories and the same selected mode/months. A code/line filter affects numerator only. All-unavailable/zero minute denominator gives BLANK. For one month this is a monthly share; for multiple months it is a weighted selected-period share, not the average monthly share. |
| Named Code/Line rank | Recompute RANKX over all eligible raw categories of the selected mode, using category-fact counts or minutes in current month/selected period; ties use shared rank. Never reuse/import a stored monthly rank as an all-period rank. Do not rank unknown-minute categories as zero. Specify all eligible categories as ranking universe, independent of a category slicer's shortlist. |
| Long-duration record share / minute share | In FactDuration select `DimDurationBand[is_over60]=1`; divide relevant numerator by FactDuration total with **band/cohort filters removed**, retaining mode/month. Record-share denominator is recorded incidents; display eligible counts and unavailable counts too. |
| Bus MFDV record/minute share | Filter FactDuration `source_mode=bus AND is_bus_mfdv=1`; denominator is all Bus records/minutes for the same month selection with band/cohort filters removed. Return BLANK outside Bus. |
| Bus MFDV ∩ >60 | Intersection of `is_bus_mfdv=1` and band `is_over60=1` in FactDuration. Current full-period result: 3,775 records / 777,169 min. |
| Bus MFDV ∪ >60 | Filter FactDuration rows satisfying MFDV **OR** >60, once per disjoint cell; alternatively A+B−intersection. Current 7,722 records / 947,874 min. Never add two overlapping totals without subtracting intersection. |
| Observed dates | For a single mode, `SUM(FactMonth[observed_dates])` across selected disjoint months. It is neither days operated nor distinct dates pooled across modes. Category date counts require one fixed category or must be suppressed. |

All counts and minute sums are additive across disjoint rows **inside one fact**. Measures from different facts are alternative totals, not quantities to add. Shares, ranks, means, medians, date bounds and distinct-date counts are not generally additive. Medians are intentionally absent from this bundle; do not use an average of grouped medians or approximate one from duration-band midpoints. Daily/time-of-day slicing is unsupported. An absent fact row/date is not manufactured as zero service; avoid “show items with no data” presentations that imply zero activity. Hide non-observed duration bins or label them as having no selected records, without claiming absence of service impact.

### Denominator and overlap examples

For a Code page, hidden mode-month denominators can be plain FactMonth sums; category-page share measures use them even while a code is selected. Overview public measures require the filter guards above, rather than exposing an apparently unfiltered KPI beside a filtered category plot. For Duration shares, REMOVEFILTERS on DimDurationBand and FactDuration[is_bus_mfdv] preserves the mode/month context. Show the two ratio units distinctly: fraction of source records versus fraction of recorded minutes.

The independent Bus disjoint partition is: neither MFDV nor >60 = 94,535 records / 1,215,228 min; MFDV only = 3,513 / 94,218; >60 only = 434 / 76,487; both = 3,775 / 777,169. The four groups equal Bus totals 102,257 / 2,163,102. Other modes have `is_bus_mfdv=0` and no code-cause inference is made.

## 5. Coverage, eligibility and required disclosures

- All 176,004 selected records qualify for configured scope; all current durations/times parse and all durations are nonnegative. There are 49,830 zero-minute records. Future missing/invalid/negative durations remain in count and unavailable-band totals; eligible minutes stay NULL if unavailable, never fabricated zero.
- 1,777 missing Line records and one missing Streetcar Code are retained in dimension-backed buckets. Unknown nonblank codes/labels stay eligible for raw-category frequency; no code descriptions, canonical route mappings or geographic identity are invented.
- All 770 duplicate-candidate records remain; all 655 weekday/date conflicts remain flagged. No automatic deduplication, date shift or semantic correction. Validated-weekday eligibility is zero. Weekday visuals are excluded from the final model.
- Subway, Bus and Streetcar observed 2025-01-01–2026-08-31 (608 dates each); LRT observed 2025-12-07–2026-08-31 (267 dates in 268 days). LRT December is partial, January lacks 2026-01-23; EC first appears in February with 21 observed dates. Coverage columns are recording observations, not proof of service start, complete reporting or matched exposure. All sources end August 2026; do not extend lines into later months as zero.
- Long recorded durations are retained; >60 is descriptive. Bus MFDV meaning and duration recording semantics are unverified. Reported timestamps are not verified onset. Missing records never establish zero-delay service. Do not label recorded minutes “passenger delay,” rank modes by reliability, infer causal explanations or divide by assumed trips/passengers.
- Monthly ranks and shares describe the chosen immutable snapshots, not significance, forecasting or verified structural changes. Code and Line are raw source categories. LRT's full-span near-tie is not a headline comparator because histories differ.

## 6. Recommended report pages (no visuals built)

1. **Overview — two different stories:** selected-mode/month counts, eligible minutes, average duration, zero share; paired monthly count/minute profiles and duration record-share/minute-share panels. Coverage and availability always visible.
2. **Codes — persistent concentration:** raw-code frequency versus duration, monthly shares/ranks, Bus MFDV and long-duration intersection/union disclosure. Use FactCode for general code exploration and FactDuration for a separately labelled Bus-MFDV overlap panel; restrict interactions to avoid suggesting arbitrary code-duration cross-filtering. EFO’s 15-month leadership phase is descriptive, not a causal change claim.
3. **Lines — overall rank versus monthly variation:** raw-label profiles and selected-period ranks with monthly detail. Subway YU/BD illustrate differing leadership in three months; Bus overall leader is not a universal monthly leader. Mode-specific labels and coverage remain visible.
4. **Scope and quality:** selected snapshot IDs/checksums, observed bounds/dates, LRT gaps, missing-category counts, duplicate candidates, weekday conflicts, eligibility and source-semantic limitations. Distinguish full-snapshot attributes from month-filtered FactMonth metrics.

## 7. Exact export and verification commands

Run from repository root; standard-library Python only. The first command creates the delivered folder and **refuses overwrite if it already exists**. For any later rebuild, use a fresh output folder and review differences; do not delete source exports.

```sh
python3 scripts/export_power_bi.py --output results/power_bi
python3 -m unittest discover -s tests -v
python3 scripts/export_power_bi.py --output /tmp/ttc-power-bi-repeat
python3 - <<'PY'
from pathlib import Path
import hashlib, json
first=Path('results/power_bi'); repeat=Path('/tmp/ttc-power-bi-repeat')
assert {p.name:p.read_bytes() for p in first.iterdir()} == {p.name:p.read_bytes() for p in repeat.iterdir()}
m=json.loads((first/'manifest.json').read_text())
for name, expected in m['export_sha256'].items():
    assert hashlib.sha256((first/name).read_bytes()).hexdigest()==expected
print(m['result_row_counts'])
print(m['verification'])
PY
```

On Windows replace the `/tmp` output path in both commands with a new local directory. Optional flags `--database`, `--selection`, `--staging`, `--core`, `--temporal` are explicit paths; all inputs must represent the same selected curated artifact and unchanged, hashed analytical outputs. There is no source-update scheduling or automatic snapshot promotion.

The executor checks source export checksums, current SQL/tool hashes, exact selected artifact/selection, read-only staging lineage/integrity, recomputed temporal values, fact/dimension uniqueness and references, monthly counts/minutes/eligible/zero reconciliation, duration-band totals, and **all four disjoint Bus overlap cohorts**. It executes the new SQL twice. Two complete final exports were compared byte-for-byte. The final suite passes **54 tests** (five new contract tests). `reports/power_bi_handoff_verification.json` records file-integrity and repeat-export checks. Building/loading the PBIX, implementing DAX and manually validating visual interactions remain future work; Python contract tests do not claim to validate an unbuilt Power BI model.

## Additive code-description reference — 2026-10-26

The original `code_key`, `source_mode`, `category_eligible` and `raw_code` columns and all 479 rows are unchanged. Only `code_description` and `code_display_label` are appended to DimCode. All nine other CSVs are byte-identical to the approved baseline at commit `76837af`. No fact, relationship key, DAX definition or calculation changed. DimCode remains mode-scoped and related through code_key; use the code-prefixed display label for readability, not description alone, which can combine multiple raw codes.

The four official references and retrieval provenance are pinned under `references/ttc_delay_codes/2026-10-26/`. The export manifest pins reference/helper hashes and records coverage/unresolved codes; `mapping_issues.json` preserves reference conflicts, duplicates and defective text. Exact duplicate reference pairs may collapse, but incident records never do. EXVE remains ambiguous, encoding-defective descriptions remain unresolved, and no cross-mode fallback or text repair is performed. Definitions are published reference labels as retrieved, without verified historical effective dates or causal interpretation.

In Power BI Desktop, append the two Text fields to the existing DimCode query's type/schema list, then refresh/Close & Apply. The checked-header importer must expect six columns, in the original-four-plus-two order. Keep all ten queries, thirteen relationships and fifty-four DAX definitions. Switching an existing visual from raw_code to code_display_label is optional and manual; existing code/filter guards and panel interaction restrictions remain. Detailed steps and regression evidence: `../reports/code_description_enrichment.md`. No Desktop or PBIX changes were made by this implementation.

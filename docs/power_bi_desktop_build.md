# Power BI Desktop implementation — Task 6.1

Prepared 2026-10-22. Build **TTC Delay Patterns: Why Incident Frequency and Recorded Duration Tell Different Stories** from the verified `milestone5-v1` bundle. Deliverables here are import expressions, measures and exact visual/validation instructions. No PBIX is generated. Power Query evaluation, DAX compilation and visual interactions are **pending Windows Desktop execution**. Local checks verified actual CSV schemas, values, checksums and expected arithmetic; they are not a substitute for Desktop testing.

This user-approved task number refers to the Desktop package, while the historical roadmap's Milestone 6 describes source updates. Do not execute that update work in this task. Keep the existing four-source selection and every exported value unchanged.

## 1. Start in Desktop and import

1. Copy the **entire** `results/power_bi` directory to Windows, for example `C:\TTC\power_bi`. Keep `manifest.json` and `results.json` beside the CSVs for audit, but do not load JSON into the model. All ten CSVs must be from one verified bundle, not a mix of export runs.
2. Open a new Power BI Desktop report. In Options for the current file, disable automatic relationship detection and Auto date/time. Use Import mode. Do not let automatic type detection convert raw codes or labels to numbers. See Microsoft's [CSV connector guidance](https://learn.microsoft.com/en-us/power-query/connectors/text-csv).
3. Open Transform data. Create a **Text parameter** named `ExportFolder`, current value `C:\TTC\power_bi` (no trailing backslash). Create a Blank Query named `ReadTtcCsv`, open Advanced Editor and paste only that function's block from `power_bi/import_queries.pq`. Disable Enable load for the function; the parameter/function are not model tables.
4. For each `// QUERY: TableName` block in that file, create a separate Blank Query with **exactly** that name and paste just the expression below the comment. Enable load for each of the ten table queries. Do not paste the entire file as one query. The function checks exact header names/order, uses quoted UTF-8 CSV parsing, explicitly parses ISO dates and types every field. No Trim, Clean, deduplication, label replacement, or NULL-to-zero step is permitted. Microsoft's [Date.FromText](https://learn.microsoft.com/en-us/powerquery-m/date-fromtext) documents explicit format/culture parsing.
5. Confirm row counts below, no conversion errors, and that raw labels/keys remain Text. Close & Apply. Build relationships manually before measures or visuals.

| CSV | Exact query/model name | Rows |
|---|---|---:|
| dim_mode.csv | DimMode | 4 |
| dim_month.csv | DimMonth | 20 |
| dim_code.csv | DimCode | 479 |
| dim_line.csv | DimLine | 909 |
| dim_duration_band.csv | DimDurationBand | 8 |
| fact_month.csv | FactMonth | 69 |
| fact_code.csv | FactCode | 4,851 |
| fact_line.csv | FactLine | 5,592 |
| fact_duration.csv | FactDuration | 615 |
| reporting_gaps.csv | ReportingGaps | 1 |

### Every imported field and Power Query type

The following exhaustive mapping matches `import_queries.pq`. `Whole Number` = `Int64.Type`; `Decimal Number` = `type number`; `Date` = `type date`; `Text` = `type text`. Numeric/date empty cells become null, not zero. Text is not trimmed. Missing raw category membership is identified by `category_eligible=0` and its key; do not treat an empty raw label as a new named category. All hashes/keys are Text even when they start with digits.

| Model table | Power Query type | Exact columns |
|---|---|---|
| DimMode | Text | `source_mode`, `resource_id`, `raw_sha256` |
| DimMode | Date | `first_observed_date`, `last_observed_date` |
| DimMode | Whole Number | `snapshot_id`, `observed_dates`, `calendar_span_days`, `dates_without_records_within_span`, `observed_months`, `selected_records`, `outside_or_unallocated_scope`, `missing_date`, `invalid_date`, `missing_time`, `invalid_time`, `missing_delay`, `invalid_delay`, `negative_delay_records`, `validated_weekday_records` |
| DimMonth | Text | `month_label` |
| DimMonth | Date | `month_start` |
| DimMonth | Whole Number | `year`, `month_number` |
| DimCode | Text | `code_key`, `source_mode`, `raw_code`, `code_description`, `code_display_label` |
| DimCode | Whole Number | `category_eligible` |
| DimLine | Text | `line_key`, `source_mode`, `raw_line` |
| DimLine | Whole Number | `category_eligible` |
| DimDurationBand | Text | `duration_band` |
| DimDurationBand | Whole Number | `sort_order`, `is_over60`, `is_zero`, `is_duration_eligible` |
| FactMonth | Text | `source_mode` |
| FactMonth | Date | `month_start`, `first_observed_date`, `last_observed_date` |
| FactMonth | Whole Number | `recorded_incidents`, `duration_eligible_incidents`, `duration_ineligible_incidents`, `zero_minute_incidents`, `observed_dates`, `weekday_conflicts`, `duplicate_candidate_records`, `calendar_month_days`, `missing_code_incidents`, `missing_line_incidents` |
| FactMonth | Decimal Number | `recorded_delay_minutes` |
| FactCode | Text | `source_mode`, `code_key` |
| FactCode | Date | `month_start`, `category_first_date`, `category_last_date` |
| FactCode | Whole Number | `recorded_incidents`, `duration_eligible_incidents`, `duration_ineligible_incidents`, `zero_minute_incidents`, `category_observed_dates` |
| FactCode | Decimal Number | `recorded_delay_minutes` |
| FactLine | Text | `source_mode`, `line_key` |
| FactLine | Date | `month_start`, `category_first_date`, `category_last_date` |
| FactLine | Whole Number | `recorded_incidents`, `duration_eligible_incidents`, `duration_ineligible_incidents`, `zero_minute_incidents`, `category_observed_dates` |
| FactLine | Decimal Number | `recorded_delay_minutes` |
| FactDuration | Text | `source_mode`, `duration_band` |
| FactDuration | Date | `month_start` |
| FactDuration | Whole Number | `is_bus_mfdv`, `recorded_incidents`, `duration_eligible_incidents`, `duration_ineligible_incidents`, `zero_minute_incidents` |
| FactDuration | Decimal Number | `recorded_delay_minutes` |
| ReportingGaps | Text | `source_mode` |
| ReportingGaps | Date | `month_start`, `calendar_date` |

## 2. Model setup: 13 relationships

In Model view / Manage relationships, create exactly these **active 1:* relationships**, with Cross-filter direction **Single** from the first table to the second. Do not accept an automatically suggested relationship without checking it. Microsoft explains relationship direction/cardinality in [Model relationships](https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-relationships-understand).

| One side | Many side |
|---|---|
| DimMode[source_mode] | FactMonth[source_mode] |
| DimMode[source_mode] | FactCode[source_mode] |
| DimMode[source_mode] | FactLine[source_mode] |
| DimMode[source_mode] | FactDuration[source_mode] |
| DimMode[source_mode] | ReportingGaps[source_mode] |
| DimMonth[month_start] | FactMonth[month_start] |
| DimMonth[month_start] | FactCode[month_start] |
| DimMonth[month_start] | FactLine[month_start] |
| DimMonth[month_start] | FactDuration[month_start] |
| DimMonth[month_start] | ReportingGaps[month_start] |
| DimCode[code_key] | FactCode[code_key] |
| DimLine[line_key] | FactLine[line_key] |
| DimDurationBand[duration_band] | FactDuration[duration_band] |

No imported table is fully disconnected. **Do not connect DimMode to DimCode/DimLine**, connect facts to one another, join raw labels, or create many-to-many/bidirectional relationships. FactMonth, FactCode, FactLine and FactDuration are alternative aggregations of the same rows. Never append or sum them into one population. No new key or calculated relationship is required.

Set DimMonth[month_label] Sort by column = DimMonth[month_start]; DimDurationBand[duration_band] Sort by = [sort_order]. Set numeric source columns to Don't summarize, and hide them after creating explicit measures. Keep source_mode, month_label, raw_code/raw_line and duration_band available for their specified visual roles; hide fact keys and metadata from general report-author use. Hide category dimension source_mode from end-user field selection (retain it for measure logic).

DimMonth is a **monthly period dimension**, not a daily date table. Do not mark its 20 month-start rows as a classic date table, add automatic date hierarchies or use daily/YTD/time-intelligence quick measures. [Microsoft's date-table requirements](https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-date-tables) distinguish date-table behaviour from ordinary date fields. Use only month_label or month_start at month grain. A month slicer is a list/dropdown, not an apparent incident-day selector.

### Slicers, empty members and restrictions

- Shared slicers on every page: DimMode[source_mode], **single select**, default `bus`; DimMonth[month_label], multi-select, initially all months. Sync only these slicers across all three pages. QA grand totals are checked with Mode cleared in a temporary validation view; do not use multi-mode rankings in the final report.
- Mode filters the facts, but does **not** directly filter DimCode/DimLine. On a Code slicer, add visual filter `[Code Incidents] is not blank`; on a Line slicer use `[Line Incidents] is not blank`. This suppresses labels without selected-mode/period records through the measures. Do not add dimension-to-dimension or bidirectional relationships to make slicers cascade.
- Slicers use dimension fields only. Do not expose fact source_mode/key/numeric filters. The only allowed direct fact filter is the explicitly documented FactDuration[is_bus_mfdv] cohort in a dedicated duration view, not a generic code filter.
- Code selection affects only Code visuals. Line selection affects only Line visuals. Neither filters overview/duration or the other category fact. Generic Code=MFDV is **not** interchangeable with the literal Bus-MFDV cohort in FactDuration.
- Page 3 has independent Code and Line panels. In Edit interactions, each category slicer filters only its own panel and its matching raw-code/line table. Set its effect on the other panel, overview/coverage and gap table to **None**. Keep it unsynced to Pages 1–2. Clear category slicers before changing mode if a stale selection gives no data; provide a Reset page bookmark.
- Never add Code/Line filters at report level. On other pages, disable category/band chart click interactions with unrelated panels/cards. Public DAX guards return BLANK for unsupported combinations if such filters nevertheless reach a visual. Blanks mean “unsupported or unavailable,” not zero records.

## 3. Install and format measures

`power_bi/measures.dax` contains **54 ready-to-copy measure definitions**. Use Modeling → New measure, home table **FactMonth**, and paste **one** `Name = expression` block at a time, in file order. It is not a bulk DAX query or calculated-table script. Each block lists fact, filters/restrictions, format and a known verification example. Use commas as DAX argument separators; file examples use English function names. Hide underscore-prefixed helper measures after validation. Set the format supplied in each comment; set display units to None for validation cards.

The four `_Allow …` helpers detect direct foreign-category filters using [ISFILTERED](https://learn.microsoft.com/en-us/dax/isfiltered-function-dax). Overview and Duration allow multiple modes for labelled QA inventory only; Code/Line require one mode. Hidden FactMonth denominator measures deliberately retain mode/month but ignore Code/Line selection via the model. Public numerator measures preserve their own raw category, zero values and NULL duration semantics.

Ranks use [RANKX](https://learn.microsoft.com/en-us/dax/rankx-function-dax), descending with **Skip** ties, over all named categories for the selected mode/current months. They remove the current category filter and explicitly reapply each candidate key. They exclude blank measure values instead of letting them become rankable zero. They also restrict current-member identity to the selected mode, because a raw code text can occur in multiple source modes. Do not replace them with a stored overall rank or a simple ALL(raw_label) formula that ignores key/mode identity. [REMOVEFILTERS](https://learn.microsoft.com/en-us/dax/removefilters-function-dax) is used only where the denominator or ranking universe must clear category/band/cohort filters.

Cohort measures `Long …`, `MFDV …`, `Overlap …`, `Union …` deliberately ignore band/cohort selections and retain shared mode/month. MFDV/Overlap/Union require Bus. `Duration … Share` measures use the selected band/cohort as numerator and all mode-period duration cells as denominator. Do not combine those two meanings under one title. Medians and code×line joint measures are deliberately absent.

## 4. Design and interaction standard

Set each page to custom **1280×720 (16:9)**. Use a 24 px outer margin, 16 px gutters, 8 px internal spacing. Use Segoe UI throughout: page title 24 pt, chart titles 13–14 pt, labels 10–11 pt, KPI values 25–28 pt. Use white background, dark text `#1F2937`, light dividers `#E5E7EB`, incident-count blue `#1F5A99`, recorded-minute orange `#A34F00`, and muted neutral `#6B7280` for context. Always label units and series; never rely on colour alone. Keep count/minute colours consistent across pages.

Top band y=16–88: page title, Mode and Month slicers, three-page navigator. Main chart area y=104–620; footer y=636–704 contains `[Coverage Note]` plus the permanent caveat: “Source records and recorded minutes; no service-exposure or passenger-impact denominator.” Use native cards, bar/line charts, tables, matrices and slicers only. Use separate count/minute axes in aligned charts; **no dual-axis combo chart**. Monthly X axes use categorical chronological months; count/minute bar axes start at zero. Shares show percentage with an explicitly labelled denominator.

Navigation: identical Page navigator at upper right, same page order/names. Add a Reset page button per page using a bookmark capturing default mode/month/category selections; verify that it does not navigate unexpectedly. Tooltips show exact count/minutes, duration-eligible denominator, zero share where relevant, mode/month scope, and “raw reported label” for categories. No tooltip should imply route exposure or code meaning.

Default Edit interactions: shared Mode/Month slicers filter all visuals. Set **all analytical chart/table clicks to None for other analytical visuals**, avoiding cross-fact cross-highlighting and rank changes caused by selecting a bar. Slicer interactions are the deliberate exceptions below. This is a clear exploration design, not a claim that arbitrary cross-highlights are valid. Turn off Show items with no data; missing reporting periods stay unavailable, not zero.

## 5. Three-page visual build specification

Each line below is an exact visual specification. Suggested bounds are x,y,width,height in pixels within the common layout; small changes for text fit are acceptable. Every chart uses the measures listed, never an implicit Sum column. No physical-record drillthrough is supported by these aggregates.

### Page 1 — Frequency vs. Duration

Default Mode bus; all months. No Code/Line slicers. Native shared slicers as above. KPI row y=104–186: four cards at x=24/340/656/972, width 284: **“Recorded incident records”** `[Overview Incidents]`; **“Total recorded delay minutes”** `[Overview Minutes]`; **“Zero-minute share of eligible records”** `[Overview Zero Share]`; **“Average recorded minutes per eligible record”** `[Overview Average Minutes]`. All use FactMonth; mode/month only, no category/band interactions. Tooltips add `[Overview Eligible Records]` and `[Overview Zero Records]`. Takeaway: counts, duration and zeros are different measures; zero is not no passenger impact.

| Exact title / bounds | Visual and field assignments | Measures / source | Filter behaviour, takeaway and caveat |
|---|---|---|---|
| “Recorded incident records by month” / 24,202,600,210 | Line chart; X DimMonth[month_label]; Y Overview Incidents; no legend | Overview Incidents, FactMonth | Mode/month only; no chart click propagation. Compare shape, not risk; missing months are not zeros. |
| “Recorded delay minutes by month” / 656,202,600,210 | Line chart; X same month field; Y Overview Minutes | Overview Minutes, FactMonth | Same period and visual width; independent Y scale labelled minutes. Takeaway: January's duration prominence may differ from count peaks; no seasonality claim. |
| “Share of records by recorded duration band” / 24,428,600,192 | Horizontal bar; Y DimDurationBand[duration_band], sort by sort_order ascending; X Duration Incidents Share | FactDuration; tooltip Duration Incidents / Duration Eligible Records | Selected mode/month; each bar filters its band numerator only. Denominator all mode-period records. No chart clicks to other panels. Include unavailable band if it has records. |
| “Share of recorded minutes by duration band” / 656,428,600,192 | Same bands/alignment; X Duration Minutes Share | FactDuration; tooltip Duration Minutes | Denominator all eligible recorded minutes, not number of records. Highlights concentration among fewer records. No clipping, causal severity standard or passenger-minute interpretation. |

Use blue for count visuals, orange for minute visuals, no displayed legend if title/axis identifies the measure. Zero-share card can have neutral emphasis. `[Coverage Note]` occupies the footer and updates with mode/month.

### Page 2 — Concentration & Persistence

Mode defaults bus. No Code/Line slicers on this page: use fixed **visual-level** shortlist filters below so no shortlist filters reach unrelated facts. Monthly shares always divide by all mode-month records/minutes, including the missing bucket. Full-period examples are annotations, not dynamic claims after filtering.

| Exact title / bounds | Visual and fields | Source/measures | Filters, takeaway and caveat |
|---|---|---|---|
| “Most recorded raw codes: frequency and minutes” / 24,104,600,228 | Table; columns DimCode[raw_code], Code Incidents, Code Minutes, Code Incident Rank, Code Minute Rank | FactCode | Visual DimCode[category_eligible]=1; measure filter Code Incident Rank <=10; sort Code Incidents descending. Ranks remain against all eligible codes, not just top ten. No clicks to other visuals. Do not attach invented descriptions. |
| “Raw codes: monthly share of recorded minutes” / 656,104,600,228 | Line chart; X DimMonth[month_label], legend DimCode[raw_code], Y Code Minutes Share | FactCode | Visual filters category_eligible=1 and raw_code in MFDV,EFO,SUDP,MUIS,MTDV,EXO,PXSW. Mode removes irrelevant fact rows; hide empty legend members. Shortlist is an evidence-driven display, not full population. MFDV rank 1 in 20/20 months; EFO’s count leadership changes, not its verified cause. Tooltip Code Incident Rank, Code Minute Rank, Code Incidents, Code Minutes. |
| “Most recorded raw lines: frequency and minutes” / 24,348,600,220 | Table; DimLine[raw_line], Line Incidents, Line Minutes, Line Incident Rank, Line Minute Rank | FactLine | category_eligible=1; Line Incident Rank <=10; sort count descending. Labels remain exact; no exposure-adjusted ranking. Missing lines disclosed on Page 3. |
| “Raw lines: monthly recorded-minute share” / 656,348,600,220 | Line chart; X month_label, legend raw_line, Y Line Minutes Share | FactLine | Visual category_eligible=1; shortlist YU,BD,52 LAWRENCE WEST,504 KING,501 QUEEN,EC,FW. Mode-specific facts suppress unrelated labels. Inspect changing ranks; LRT uneven histories prevent full-span near-tie interpretation. Tooltip Line Incident Rank, Line Minute Rank. |

At y=584–628 add one native multi-card group with **“Bus MFDV and >60 minutes: intersection”** `[Overlap Incidents]`, `[Overlap Minutes]`, and **“Bus MFDV or >60 minutes: union”** `[Union Incidents]`, `[Union Minutes]`. Source FactDuration; month-filtered, Bus-only, no category/table interactions. Format count and minutes separately with explicit units. If Mode is not bus, leave BLANK and show adjacent fixed text “Bus-only overlap measures.” Tooltip Long Incidents, Long Minutes, MFDV Incidents, MFDV Minutes. These are related views, never additive independent impacts. The group fits only as a compact numeric strip; avoid four large cards crowding charts. Put coverage/caveats in footer.

### Page 3 — Explore the Records

“Records” means aggregated source-record activity, **not row-level records**. Keep this subtitle visible. Shared Mode/Month slicers; Code and Line are independent panels, not a joint filter intersection.

| Exact title / bounds | Visual and assignments | Source/measures | Filters, takeaway and caveat |
|---|---|---|---|
| “Choose raw code (Code panel only)” / 24,104,600,64 | Dropdown DimCode[raw_code]; multi-select; add Code Incidents is not blank visual filter | DimCode + FactCode measure | Filters Code table only. Does not affect Line table, snapshot/coverage or overview footer. Do not force category_eligible=1 here: blank/missing category is available for QA. Clear stale selection on mode change. |
| “Choose raw line (Line panel only)” / 656,104,600,64 | Dropdown DimLine[raw_line]; add Line Incidents is not blank | DimLine + FactLine measure | Filters Line table only; no Code interaction. Raw blank shown by native `(Blank)` presentation, with category_eligible in table to disambiguate. |
| “Raw-code activity for selected months” / 24,184,600,246 | Table: raw_code, category_eligible, Code Incidents, Code Minutes, Code Average Minutes, Code Zero Share, Code Incidents Share | FactCode | Code slicer + shared filters. Named and missing buckets retained; average eligible duration, not average of monthly averages. Shares denominator all selected mode-months, including other codes/missing. Rank is not required for multi-select aggregate cards. |
| “Raw-line activity for selected months” / 656,184,600,246 | Same columns using raw_line and Line measures | FactLine | Line slicer + shared filters only. A selected line does not constrain Code. Separate panels are not jointly filtered records. |
| “Selected snapshot — full source coverage” / 24,446,600,166 | Table: DimMode[source_mode], snapshot_id, resource_id, first_observed_date, last_observed_date, observed_dates, raw_sha256; Don't summarize | DimMode only | Shared Mode selects source; Month does not narrow these snapshot attributes. Title explicitly says full source coverage. Horizontal scroll/hash wrapping acceptable; no copied token strings as numeric keys. |
| “Internal dates without selected records” / 656,446,280,166 | Table: DimMode[source_mode], ReportingGaps[calendar_date] (Don't summarize) | ReportingGaps | Mode/month filter. LRT Jan 2026 shows Jan23. No missing rows for other modes is not proof of complete service reporting. |
| “Missing raw labels in selected months” / 952,446,304,166 | Two cards: Overview Missing Code Records, Overview Missing Line Records | FactMonth | Shared Mode/Month only; category slicers None. Counts remain period totals even when one label is selected; titles/caveat say this explicitly. Streetcar blank code is one zero-minute record. |

Do not add geography, hour, weekday or raw-incident drillthrough. These exports have neither supported geography nor row-level detail. Use the standard coverage footer; this page’s independent panels are explained in a permanent note. Chart/table clicks have None interactions with other panels.

## 6. Validation: complete in this order

**Pending Desktop** means not completed by this package. Record actual values/screenshots in a small Desktop QA log when performing these checks. `power_bi/validation_queries.dax` supplies copyable DAX Query View checks; execute each EVALUATE separately after measure creation.

| Step | Desktop action | Expected result / pass condition | Status |
|---|---|---|---|
| 1 | Load the ten queries with the supplied function; inspect errors and data types | All row counts/types match section 1; leading zeros/whitespace labels preserved; no transformed export values | Pending Desktop |
| 2 | Inspect all 13 relationship arrows, active status and cardinality | Only listed Single 1:* paths; no inferred fact relationships or auto date tables | Pending Desktop |
| 3 | Paste measures one by one and set formats; use Query View baseline | All measures compile; no renamed/missing fields or circular references | Pending Desktop |
| 4 | With all filters cleared in QA, show Overview Incidents, Minutes, Zero Records | **176,004**, **2,740,515**, **49,830**. Never add Code/Line/Duration totals to these | Pending Desktop |
| 5 | Select bus, subway, streetcar, lrt separately (all months) | Counts 102257 / 45475 / 23703 / 4569; minutes 2163102 / 122071 / 416513 / 38829; zeros 12974 / 29669 / 5279 / 1908 | Pending Desktop |
| 6 | Bus, January 2025 only | 3,908 records; 72,665 minutes; 411 zeros; 31 observed dates. Code and Line shares each sum to 100% **including missing buckets** | Pending Desktop |
| 7 | Subway full period | Zero share 65.24%; mean 2.6843540407; 608 observed dates. No recombined median card | Pending Desktop |
| 8 | Bus Code=MFDV on a temporary Code-only visual | Code Incidents 7288; Code Minutes 871387; incident share 7.13%; minute share 40.28%; incident rank 4/minute rank 1. MFDV minute rank remains 1 across 20 months | Pending Desktop |
| 9 | Confirm phase and monthly rank logic | EFO count rank 1 Jan2025–Mar2026; Apr–Aug2026 ranks 5,6,6,9,5. YU count rank 1 all months; BD minute rank 1 Mar2025, Mar2026, Apr2026 | Pending Desktop |
| 10 | Set category_eligible=0 for category QA | Missing lines: Subway177, Bus1241, Streetcar352, LRT7 (total1777). One missing Streetcar Code, zero minutes. Named-line incident totals: 45298 / 101016 / 23351 / 4562 in that same mode order | Pending Desktop |
| 11 | Deliberately apply generic Code filter to a temporary overview/line/duration visual | Public Overview/Line/Duration measures BLANK; Code remains valid. Remove filter. Repeat Line → Code/Overview/Duration. Guards must not turn unsupported contexts into zero | Pending Desktop |
| 12 | Page 3 choose one Code and one Line | Each slicer changes its own panel only; no joint intersection claim. Shared Mode/Month still affect both. No disconnected model table added to fake shared filtering | Pending Desktop |
| 13 | Bus cohort QA with no generic Code filter | Long: 4209 / 853656; MFDV: 7288 / 871387; intersection: 3775 / 777169; union: 7722 / 947874. Values are records/minutes respectively; A+B−intersection, not A+B | Pending Desktop |
| 14 | Select a band and change month selection | Duration band shares denominator remains all mode-period records/minutes; cohort cards ignore band selection by design. Generic Code filter still rejects cohort cards | Pending Desktop |
| 15 | LRT all months, then Jan2026, then Jan2025 | Full coverage Dec7 2025–Aug31 2026, 267 dates; Jan2026 has 30 dates and gap Jan23; Jan2025 has no selected rows and BLANK measures, not zero-delay service | Pending Desktop |
| 16 | Review missing numeric handling in Power Query / DAX | No Replace null with 0 or COALESCE. Current duration_ineligible total 0. Under an empty period, SUM and DIVIDE remain BLANK. Future all-unavailable-group behaviour requires an appropriately approved fixture, not editing these exports | Pending Desktop |
| 17 | Check Mode change with Code/Line slicer populated | Slicer lists suppress unavailable labels by matching measure; stale selection is clearable/resettable. No new relationship used to cascade dimensions | Pending Desktop |
| 18 | Inspect chart interactions, sorting, tooltips and zero baselines | No cross-fact highlighting, dual axes, implicit numeric sums, unsupported daily slicing or fabricated missing months | Pending Desktop |
| 19 | Refresh twice from identical verified folder; save/reopen PBIX | Same row counts, QA measures, source-selection metadata, filters and results; no new rows or snapshot selection | Pending Desktop |

Missing numeric values are not present in the current delivered durations, so the “invalid data becomes BLANK” case cannot honestly be claimed empirically from Desktop using this unchanged bundle. Local offline pipeline tests already exercise such inputs; Desktop typing and BLANK propagation still need verification without altering real exports.

## 7. Refresh and package verification

Refresh is a local re-read of a deterministic selected snapshot bundle, **not source update automation**. Keep all ten CSVs and both manifest/results files together. Before copying a newer approved bundle, run the exporter into a new folder and compare manifest selection/checksums. Change ExportFolder to that complete folder only after review; no latest-file or MAX(timestamp) selection is authorized. Refresh in Desktop and repeat baseline/mode/month/overlap tests before using new screenshots or findings.

Existing creation command (refuses overwrite):

```sh
python3 scripts/export_power_bi.py --output results/power_bi
python3 -m unittest discover -s tests -v
```

For a rerun use a fresh directory via `--output`, not the existing one. No export rerun was necessary for this documentation package. On Windows, verify the copied export bytes before import using PowerShell (set `$bundlePath` to the copied folder):

```powershell
$bundlePath = 'C:\TTC\power_bi'
$manifest = Get-Content -Raw (Join-Path $bundlePath 'manifest.json') | ConvertFrom-Json
foreach ($entry in $manifest.export_sha256.PSObject.Properties) {
    $actual = (Get-FileHash -Algorithm SHA256 -LiteralPath (Join-Path $bundlePath $entry.Name)).Hash.ToLowerInvariant()
    if ($actual -ne $entry.Value) { throw "Checksum mismatch: $($entry.Name)" }
}
```

The manifest also supplies `selection`, `curated_sha256` and export row/column counts. Compare these with the approved repository manifest; hash-checking files against a locally replaced manifest alone would not establish source authority. Do not mix bundles or import arbitrary CSVs from the parent results directory.

## 8. Local checks and remaining work

Local checks inspected every real schema and sample values; verified all bundle file hashes; checked that M type mappings cover all imported columns exactly and DAX table/column references use existing fields; confirmed current raw-label case/whitespace display collisions do not exist within mode; and recomputed the numerical QA examples from typed exports. All pre-existing repository files, raw/staging/curated data and exports are unchanged. Static checks do not execute M or DAX and do not establish Desktop compilation/filter semantics. Desktop checks above remain pending. No installed Windows Desktop session or reliable report-generation path was used; no PBIX or visuals were generated.

Created only `docs/power_bi_desktop_build.md`, `power_bi/import_queries.pq`, `power_bi/measures.dax` and `power_bi/validation_queries.dax`. No pipeline change, dependencies, data downloads, commits, pushes or next-task work. Begin in Desktop with section 1, then model/measure QA, then the three pages.

## Additive DimCode refresh — 2026-10-26

For an already-built and validated model, **do not recreate or rename any query, column, key, relationship or DAX measure**. The existing DimCode CSV now appends two fields. Its original four columns and 479 rows are identical; all other nine CSVs are unchanged. The new official reference snapshots and audit are described in `../reports/code_description_enrichment.md`.

1. Copy the complete reviewed export bundle to the existing Windows ExportFolder; keep manifest and typed JSON together. Verify the new manifest checksums.
2. Transform data → select the existing **DimCode** query → Advanced Editor. For the supplied `ReadTtcCsv` import, retain its query/function names and replace only the existing four-item argument list with:

```powerquery
ReadTtcCsv("dim_code.csv", {
    {"code_key", type text},
    {"source_mode", type text},
    {"category_eligible", Int64.Type},
    {"raw_code", type text},
    {"code_description", type text},
    {"code_display_label", type text}
})
```

3. Do not disable strict header validation. The supplied helper derives the expected headers from this list and already parses UTF-8 Text without normalization. If a manually built query instead has a fixed CSV column count of four, append support for six columns and the two Text conversions only; preserve the first four bindings.
4. Preview: 479 rows; first four fields unchanged; two new Text fields. Unresolved descriptions are blank, not guessed text. Close & Apply / refresh in the existing model.
5. Confirm **10 imported queries, 13 relationships, 54 unchanged measures**. The code_key relationship stays unique/active/single-direction. Keep raw_code and the existing slicer/interaction restrictions.
6. Optionally replace raw_code with code_display_label in the intended Code slicers, tables, axes or legends. Do this manually. Do not create relationships on either new attribute; description-only grouping is not a one-code identity. New label filters remain DimCode filters and therefore trigger existing foreign-fact guards.
7. Compare identical key selections before/after: code counts, minutes, shares and ranks, zero shares, independent Line panels and Bus-MFDV duration measures must match. Check missing and ambiguous examples and Desktop refresh twice. Desktop/DAX execution remains a manual regression check; repository tests do not execute the PBIX.

The implementation package `power_bi/import_queries.pq` includes this minimal schema addition. `power_bi/measures.dax` and `validation_queries.dax` are unchanged. No Desktop or PBIX was modified automatically.

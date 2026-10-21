# Cleaning and validation rules — Milestone 4, Task 4.1

Rules proposed and verified against local evidence on 2026-10-21. **Specification only:** no curated table, transformation, source change or analytical finding is implemented. Rules use recorded incident records and recorded minutes, not unique real-world incidents, verified causes, passenger impact or normalized reliability.

## Checkpoint, evidence and audit scope

Local checkpoint **`aa0f010`** commits exactly the 14 reviewed Milestone 3 implementation/test/documentation/result files. Git status, tracked/untracked inventory, cached diff and credential-pattern checks were reviewed. Raw CSVs, SQLite files/sidecars, environment/credential/key files and temporary files remain ignored. No unexpected files or secret patterns were found; staged whitespace checks passed. Nothing was pushed. The new rules document is left uncommitted for review.

The audit selected original snapshot IDs 1–4 explicitly, matching the resource IDs/checksums below and their successful staging receipts. These are the agreed inspection snapshots, not automatically authoritative latest versions. Queries join staging to snapshot metadata, not directly to retrieval rows, so repeated acquisitions cannot multiply counts. Future runs must record one explicitly selected snapshot per logical source series, with resource ID and checksum; never select by maximum ingestion/retrieval timestamp.

| Mode | Snapshot | CKAN CSV resource ID | SHA-256 |
|---|---:|---|---|
| Subway | 1 | `0b6e5c52-e993-46d6-8d74-8602ee224457` | `ec7c36eeb4785e34d58229e5da6af741c89dfdf9fa59c58a63abe5b026b95c44` |
| Bus | 2 | `b5725365-9252-4bfe-b6f4-cda7ddf74341` | `1474f16414e63aaeab58714c236446ea370f5e00e072a3b97fdfeb1f079cd8fe` |
| Streetcar | 3 | `cf2fdd12-6f0e-4644-aae7-0bbfc31df031` | `c6c081880619ffff8779c61af3a0b77466471473a014d8dec48d16306ddf9606` |
| LRT | 4 | `9a800c92-0362-4cee-8232-7374596b6a43` | `a493ad2f0d3c2889c34eba7cb42b3c27fc1d6cbf15728be09d7f1b230964984a` |

Evidence: unchanged raw/staging/provenance, existing per-mode profiles, cross_mode_assessment.md, data_model_readiness.md and snapshot_versioning.md. SQLite was opened with `mode=ro`, `PRAGMA query_only=ON` and a consistent read transaction. Temporary deterministic audit functions validated exact date/time formats and finite numeric syntax; they did not write derived fields. Official code dictionaries came from the cached HTTP-200 payloads inspected for the readiness assessment on this same date; no network or new dictionary download was performed. Dictionary status is relative to those versions, not a permanent statement about all TTC codes.

## Verified observations

Counts are per record and per selected snapshot. Flags overlap: do not sum anomaly counts as though they represent distinct excluded records.

| Mode | Rows | Actual date range | Distinct dates | Date/time parse failures | Day/Date conflicts |
|---|---:|---|---:|---:|---:|
| Subway | 45,475 | 2025-01-01–2026-08-31 | 608 | 0/0 | 63 |
| Bus | 102,257 | 2025-01-01–2026-08-31 | 608 | 0/0 | 130 |
| Streetcar | 23,703 | 2025-01-01–2026-08-31 | 608 | 0/0 | 42 |
| LRT | 4,569 | 2025-12-07–2026-08-31 | 267 | 0/0 | 420 |

**176,004 rows total.** There are no SQL NULLs in any of the 11 source fields. All nonzero blank counts are listed below; every other field has zero blanks. Blanks are empty strings in these snapshots; no whitespace-only/leading/trailing-space anomaly was found in existing profiles or contradicted by the SQL checks. No literal null-like strings were reported by the profiles. No source values were reinterpreted as NULL during the audit.

| Mode | Blank Bound | Blank Line | Blank Code | Vehicle text `0` | Non-cardinal, nonblank Bound |
|---|---:|---:|---:|---:|---:|
| Subway | 15,860 | 177 | 0 | 18,008 | 62 |
| Bus | 21,327 | 1,241 | 0 | 4,986 | 56 |
| Streetcar | 5,327 | 352 | 1 | 1,467 | 17 |
| LRT | 773 | 7 | 0 | 1,149 | 2 |

All duration fields are nonblank finite unsigned-integer strings in these actual snapshots: zero numeric parse failures, fractional values or negatives. The guarded SQL casts below are audit-only; they are not a proposed permissive parsing rule. Units for Min Delay are documented minutes; Min Gap's current operational interpretation remains unresolved.

| Mode / field | Zero | Negative | >60 | >120 | >1440 | Maximum | Raw sum |
|---|---:|---:|---:|---:|---:|---:|---:|
| Subway / Min Delay | 29,669 | 0 | 110 | 41 | 0 | 900 | 122071 |
| Bus / Min Delay | 12,974 | 0 | 4209 | 2220 | 0 | 999 | 2.1631e+06 |
| Streetcar / Min Delay | 5,279 | 0 | 1188 | 365 | 0 | 999 | 416513 |
| LRT / Min Delay | 1,908 | 0 | 110 | 46 | 0 | 971 | 38829 |
| Subway / Min Gap | 30,403 | 0 | 103 | 38 | 0 | 906 | 169074 |
| Bus / Min Gap | 13,216 | 0 | 5783 | 2682 | 0 | 997 | 3.41733e+06 |
| Streetcar / Min Gap | 5,359 | 0 | 1547 | 415 | 0 | 999 | 590287 |
| LRT / Min Gap | 2,003 | 0 | 122 | 51 | 0 | 981 | 55939 |

There are 49,830 zero-Min-Delay records and 2,740,515 raw Min Delay minutes. The zero-record count is not the count of days with no delays. Min Gap is smaller than Min Delay in 744 Subway, 758 Bus, 256 Streetcar and 100 LRT rows. This relationship is flagged, not declared invalid. Thresholds >60/>120/>1440 are descriptive review flags, not documented error cutoffs or caps. No evidence proves that 999 is a sentinel or an invalid duration.

Duplicate candidates below group **all 10 source fields except `_id`**, within each snapshot, retaining multiplicity. Source `_id` is individually unique in the existing profiles, so all-11-field duplicates are zero. This does not prove absence of duplicated incident records.

| Mode | Repeated groups | All rows in groups | Excess beyond first |
|---|---:|---:|---:|
| Subway | 66 | 132 | 66 |
| Bus | 297 | 595 | 298 |
| Streetcar | 18 | 36 | 18 |
| LRT | 2 | 7 | 5 |

The 770 rows in repeated groups include 387 excess occurrences; neither number is an approved exclusion count. Do not flag only an arbitrary “later” member as invalid; every member gets the candidate flag.

### Codes and reference quality

Exact, mode-scoped anti-match checks used the official dictionaries linked in data_model_readiness.md. Dictionary entries were passed into a read-only JSON CTE; nothing was loaded into SQLite. NOT EXISTS prevents duplicate reference keys from inflating source counts.

| Mode | Nonblank codes absent from own dictionary | Affected source rows | Blank Code rows |
|---|---:|---:|---:|
| Subway | 10 | 1,654 | 0 |
| Bus | 35 | 5,468 | 0 |
| Streetcar | 74 | 3,225 | 1 |
| LRT | 16 | 531 | 0 |

LRT dictionary CODE EXVE has two different descriptions and affects 1 record. TXSUP repeats the same description twice and affects 4 records. Reference-only exact `(CODE, DESCRIPTION)` duplicate collapse can be an explicitly tested lookup preparation rule; it must never deduplicate incident records. EXVE remains ambiguous. Dictionary descriptions with corrupted characters (noted in the readiness assessment) remain flagged, not silently repaired. Do not infer a meaning for unmapped/blank codes or borrow another mode's mapping.

### Labels and coverage

| Mode | Distinct Line labels including blank | Distinct Station strings | Rows with `/` in Line | Numeric-only nonblank Line rows | Station length exactly 22 |
|---|---:|---:|---:|---:|---:|
| Subway | 38 | 1251 | 596 | 1 | 4267 |
| Bus | 664 | 16396 | 16 | 1180 | 24554 |
| Streetcar | 198 | 3130 | 2 | 221 | 3831 |
| LRT | 9 | 317 | 8 | 0 | 909 |

These are syntactic observations, not a validated count of incorrectly labelled routes or truncated locations. All modes have maximum Station length 22; do not reconstruct clipped text or classify every 22-character value as truncated.

SQL spot checks confirm Bus `100 FLEMINGDON PARK` (1,063) and `100 FLEMINGTON PARK` (1), `999` (566), `FLEET VEHICLE` (8), `LINE 1 SHUTTLE` (65); Streetcar `504 KING` (4,102), `504 AKING` (1), `TRACK 11` (1), `CARHOUSE` (1). LRT has EC (2,743), FW (1,808), combined/generic variants (11), and blank Line (7). Similar strings do not prove equivalence or error; package mode is not inferred from these labels. Bound values beyond N/S/E/W include B in all modes and additional numeric/letter tokens in Bus/Streetcar. No automatic direction mapping is approved.

Subway/Bus/Streetcar have records on every date within their 608-day endpoint ranges. LRT has 267 distinct dates within its 268-day span, with **2026-01-23 absent**. Earlier LRT months and September/October 2026 are not present; absent records are not zero-delay service. Existing line coverage shows FW beginning 2025-12-07 and EC beginning 2026-02-08; these are observed reporting endpoints, not proven service-opening dates. Cross-mode exposure and recording completeness are not established.

All Bus Date strings have midnight timestamp components, unlike date-only strings in other modes. Separate Time values carry the reported HH:MM. All four have weekday conflicts on 2026-04-26; LRT has other conflicts, predominantly on Sundays in the inspected evidence. LRT's 420/4,569 conflicts (about 9.2%) warrant particular caution; no timezone or service-day explanation is verified.

## Proposed rule catalogue

Every rule retains `(snapshot_id, record_ordinal)` and exact raw strings through the staging reference. “Flag” means add an explicit future curated status, never update staging. No ordinary anomaly below justifies deleting a record globally.

| Rule / observed condition and affected count | Proposed handling and justification | Effect on counts / recorded minutes |
|---|---|---|
| R1 Structural provenance/integrity failure: none found; all 176,004 rows trace to preserved source evidence | Preserve one curated row per selected staging row. If source identity, hash, key uniqueness or join cardinality fails, stop publication and quarantine the candidate **build**, not silently discard individual records. | Prevents unsupported totals for both measures; no current exclusions. |
| R2 Empty/blank fields: counts above; all other fields zero | Preserve raw empty string; represent unavailable derived values as NULL plus a reason. Keep explicit unknown/missing buckets and field-level statuses. Numeric zero and text `0` are not missing automatically. | Overall record counts unchanged. Only analyses needing the missing field lose named-category eligibility; missing duration would be absent from minute sums, never zero-filled. |
| R3 Date/Time: failures 0/0 in each mode; non-midnight Bus Date components 0 | Parse exact observed formats with round-trip checks. Keep original Date/Time. Derive source date and separate local-looking time; no inferred UTC offset, seconds of precision or incident end time. A future non-midnight Bus Date is a representation-review flag; do not silently combine conflicting timestamps. | Invalid/missing Date blocks period assignment; invalid/missing Time blocks hour assignment. Other usable analyses retain records/minutes. |
| R4 Day disagrees with parsed Date: 63/130/42/420 | Preserve source Day; derive calendar weekday from source Date and a conflict flag. Do not shift Date or “correct” Day in place. Derived-date summaries must be labelled provisional, not authoritative service-day patterns. Publish conflict counts and a sensitivity excluding conflicts before weekday interpretation. | No loss from inventory, date-based counts or minute sums. Weekday allocation is uncertain for both measures; conservative weekday sensitivity omits flagged rows explicitly. |
| R5 Zero Min Delay: 29,669/12,974/5,279/1,908 | Retain as recorded incident records when otherwise eligible; parsed value is numeric 0. Never infer missing service records or no passenger disruption. | Each contributes 1 record and 0 recorded delay minutes. |
| R6 Invalid/missing/negative Min Delay: 0 currently | Keep the record and original duration. Derived numeric is NULL for blank/invalid; a parsed negative remains identifiable as negative but is ineligible for nonnegative-delay-minute totals. Never clamp or cast invalid text to 0. | Record counts remain eligible independently. Exclude only from delay-minute analysis with explicit reason/count; totals must disclose unavailable durations. |
| R7 Long Min Delay: >60/>120 counts above; >1440 zero | Preserve and flag thresholds; no automatic cap, winsorization or exclusion. Thresholds support review only; unusually large is not synonymous with erroneous. | Current record and minute totals unchanged; any later exclusion requires separate evidence and approval. |
| R8 Repeated non-ID records: affected rows 132/595/36/7 | Flag all group members and group size; retain every occurrence. No real-world unique key is established. Never deduplicate by _id, field equality or row order. | Both measures retain all occurrences. Do not report deduplicated counts as unique incidents. |
| R9 Missing/unmatched/ambiguous codes: table above; conflicting EXVE affects 1 | Preserve exact Code and mode. Derive missing/matched/unmapped/ambiguous/not_evaluated status against a pinned dictionary version. Description remains NULL when unavailable/ambiguous. Never invent meanings or resolve conflict by first match. | Counts and minutes remain in raw-code totals. Description-based totals require eligible mappings plus separately reported unresolved buckets. |
| R10 Nonuniform Line/Station/Bound: exact counts/examples above; no validated global error count | Keep mode-scoped raw labels. Do not fuzzy-match, split combined labels into multiple incidents, infer route IDs, geocode, expand abbreviations or map B automatically. Placeholder-looking labels are review candidates, not proven invalid. | Overall measures unchanged. Only raw-label analysis is supported; canonical route/location/direction analysis remains gated on verified mappings. |
| R11 Vehicle text `0`: 18,008/4,986/1,467/1,149 | Preserve as identifier text and flag placeholder candidate; no verified zero semantics or cross-mode namespace. Retain leading zeros in all identifiers. | Neither incident counts nor delay-minute eligibility depends on Vehicle. |
| R12 Min Gap: zeros/maxima and Gap<Delay counts above | Preserve raw and any safely parsed numeric value with a semantic-status flag. Do not combine it with Min Delay, enforce Gap≥Delay, or define cross-mode headway/reliability measures. | No effect on incident or delay-minute eligibility; no verified gap-based metric is approved. |
| R13 Coverage differences: LRT starts later, one internal date absent; all snapshots end August | Store observed bounds and selected source lineage. Missing-date markers mean no recorded rows, not zero incidents/service. Do not fill unavailable periods with zero or compare unequal source exposure as reliability. | Denominators/comparison windows remain explicit. Calendar buckets outside observed reporting cannot be assigned zero counts/minutes. |

Counts in slash-separated rule entries follow Subway / Bus / Streetcar / LRT. All rule decisions remain mode-scoped; matching column names do not establish equal recording practices.

## Curated eligibility and missing-value contract

**Base record:** a source row with valid traceability from an explicitly selected, reconciled snapshot. No general “clean record” exclusion flag is permitted. All 176,004 current rows pass the structural gate and remain represented. Keep analysis eligibility as separate booleans/reason sets. “Incident count” must be labelled a count of recorded incident records, not distinct real-world incidents.

**Scope gate:** when an analysis specifies a date range, require a parseable source date in that range. Missing/invalid dates are reported as unallocated records, not silently counted within 2025-onward temporal scope. A source-wide inventory can still count them. Default initial scope starts 2025-01-01; do not extrapolate beyond observed coverage. Calendar interpretation remains provisional where source Date/Day conflicts exist.

| Analysis | Eligibility beyond base/specified scope | Representation of ineligible or unresolved values |
|---|---|---|
| Incident-record counts | No duration, code, route, Vehicle or direction requirement. A date is required only to assign a period. Zero-minute and duplicate-candidate records are included. | Retain unallocated-date and unknown-category record counts separately; do not imply omitted records were zero activity. |
| Recorded delay minutes | Strictly parsed, finite, nonnegative Min Delay. Zero is eligible. A date is needed for period allocation, not for a source-wide inventory total. | NULL numeric for missing/invalid plus status; negative kept/flagged but excluded from valid-minute sum. Report all such record counts, eligible count and completeness of duration availability. An all-unavailable group has NULL minutes, not 0. |
| Hour of day | Valid reported HH:MM; use its hour. Apply date scope if requested. Delay-minute-by-hour additionally requires minute eligibility. Do not use the Bus Date midnight suffix as incident hour. | Invalid/missing Time gets NULL hour and an unallocated-hour count; no fallback to midnight. |
| Reported raw Line labels | Nonblank Line, mode retained. Category displays must say reported labels. Add minute eligibility when summing minutes. | Blank labels appear in an explicit missing-line bucket for reconciliation. Named-label subtotals alone do not equal overall counts. Canonical-route/line ranking is **not eligible** until an approved mapping exists. |
| Incident Code (raw code frequency) | Nonblank exact Code with source mode. A dictionary match is not required. Add minute eligibility for code-level minutes. | Blank Code has its own bucket. Unmapped codes retain their literal code and status; never replace them all with an invented cause. |
| Incident description grouping | Version-pinned dictionary, exact mode-scoped Code and exactly one usable distinct description. Reference-only identical duplicates may be collapsed by explicit rule. | Blank/unmatched/conflicting codes stay in separately counted buckets. With no pinned reference, status is not_evaluated; do not mislabel as known-unmapped. A left join must not drop or multiply records. |

Proposed accounting for the existing full observed ranges (not cross-mode reliability comparisons):

| Mode | Incident / valid-delay / hour rows | Named raw Line rows | Nonblank raw Code rows | Unambiguously mapped description rows* |
|---|---:|---:|---:|---:|
| Subway | 45,475 | 45,298 | 45,475 | 43,821 |
| Bus | 102,257 | 101,016 | 102,257 | 96,789 |
| Streetcar | 23,703 | 23,351 | 23,702 | 20,477 |
| LRT | 4,569 | 4,562 | 4,569 | 4,037 |

*Description counts are conditional on preserving the inspected dictionaries and collapsing identical **reference** pairs (TXSUP), never incident rows. No mapping has been materialized. These projected eligibility counts are specification checks, not implemented curated outputs. All current durations are eligible under the proposed numeric rule; that does not verify operational correctness of every value.

For weekdays, always retain both reported and derived values plus conflict status. Date-derived weekday distributions are provisional; a comparison presented as source-validated weekday behaviour must wait for source-calendar clarification. A conflict-excluded sensitivity is an explicit alternative analysis, not a permanent record deletion. LRT requires this caution particularly strongly.

Derived columns should distinguish `valid`, `missing`, `invalid`, `negative`, `unmapped`, `ambiguous`, `not_evaluated` or other relevant statuses rather than overload one NULL meaning. Apply only statuses relevant to each field. A display bucket is a label in reporting, not a fabricated raw category. Eligibility flags can overlap; reconcile each analysis independently.

## Source-to-curated traceability

- Keep one curated row per selected `(snapshot_id, record_ordinal)` under a named rule/transformation version. Preserve source `_id` as data, never as a permanent incident key.
- Retain exact raw values through staging references or explicit raw columns. Parsed Date/Time, weekday and durations are additional fields; no UPDATE to staging/raw/provenance.
- Record selection by resource ID, snapshot ID and checksum; preserve source mode, related retrieval/provenance and any dictionary version. Never join a record to every retrieval and accidentally count it repeatedly.
- Key any category lookup by mode, dictionary version and raw Code with proven output cardinality. Keep conflicts/unmatched rows and mapping status visible. Preserve original reference descriptions, including encoding concerns, for audit.
- Reconcile source-to-curated row count and value lineage; for every analysis reconcile eligible + ineligible records to its scoped base, and known-category + missing/unresolved-category contributions to totals. Do not combine Min Gap with delay minutes.

## Open questions and acceptance checklist for Task 4.2

Still unresolved: authoritative source calendar versus service day/timezone; LRT conflicts and reporting starts; incident inclusion thresholds and real-event identity; duplicated record semantics; zero/999-like duration meanings; current Min Gap definitions; correct code mappings/version applicability and corrupted descriptions; legitimate route/location/direction conventions; truncation and Vehicle 0; missing-period completeness; actual historical revision behaviour. Rules above preserve uncertainty instead of inventing answers.

Before Task 4.2 is accepted:

- [ ] Approve a specific snapshot selection and rules version. Preserve original files, staging rows and provenance; hash-check before/after.
- [ ] Produce one curated row per selected source row with unique source lineage, even for zero minutes, duplicates and unmatched codes. No unexplained global exclusions.
- [ ] Test strict date/time/numeric parsing with blanks, malformed/nonfinite values, negatives, fractional durations and midnight representation. No SQLite permissive CAST-to-zero fallback. Use an exact or demonstrably lossless numeric representation; no rounding/capping policy is approved.
- [ ] Preserve source Day; derive calendar weekday separately, reproduce all 655 conflicts and apply the documented provisional/sensitivity policy. Do not shift LRT dates.
- [ ] Reproduce current base count 176,004 and raw Min Delay total 2,740,515, with 49,830 zero-minute records, while exposing metric-specific eligibility/reasons. Any future ineligible amount must be separately accounted for.
- [ ] Reproduce blank/duplicate/long-duration/code diagnostics above. Use exact source fields for duplicate flags, mode-scoped keys, and retain all occurrences.
- [ ] If enriching descriptions, first preserve/version reference evidence and prove join cardinality. Test absent CODE, EXVE conflict and TXSUP identical reference duplicates. Without a persisted pinned dictionary, leave enrichment not_evaluated rather than claim validation.
- [ ] Test analysis-specific eligibility: invalid duration does not erase an otherwise countable incident; unknown code does not erase hour/line eligibility; absent Time does not erase source-wide minutes; absent Line remains in missing-category totals.
- [ ] Keep structural integrity gates separate from semantic flags. Verify no changes to accepted staging, no lost/multiplied records, consistent eligibility totals and reproducible reruns. Do not introduce reliability denominators or fill absent coverage with zero.

These are requirements for a separately approved Task 4.2, not tasks executed here.

## Verification record and SQL

Executed commands: Git inventory/diff/ignore/secret-pattern checks; reviewed `git add` and local `git commit` for Milestone 3; `python3 /tmp/ttc_cleaning_audit.py`; Python assertion checks reconciling SQL with existing profiles and comparing pre-task file SHA-256 values. No ingestion/profiling script was rerun. Every date, time, blank, duration, duplicate and coverage metric checked agreed with the existing profiles. Dictionary anti-match counts agree with data_model_readiness.md. SQL-only label and ambiguity counts are documented above.

The audit script and cached official payload are temporary examination material outside the repository, not transformation code. The queries below record the checks; JSON dictionary parameters came from the exact mode-specific CODE/DESCRIPTION payloads previously inspected. The source register in data_model_readiness.md links those official resources. Re-fetching a changed dictionary in the future may legitimately change match counts and must be versioned.

Audit functions (connection-local, read-only): `blank(v)` means non-NULL and Python whitespace-strip is empty; `parsed_date(mode,v)` requires exact round-trip `%Y-%m-%dT%H:%M:%S` for Bus or `%Y-%m-%d` otherwise and returns its date component; `valid_time(v)` requires round-trip `%H:%M`; `source_weekday(mode,v)` returns an English weekday from that parsed date. `num_state(v)` distinguishes null, blank, invalid and valid finite Decimal, using ASCII syntax `[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?` with full match, no trimming of nonblank values. These are validation definitions for this audit, not materialized transformations.

Read connection setup:

```python
sqlite3.connect('file:data/local/ttc.sqlite3?mode=ro', uri=True)
# PRAGMA query_only=ON; BEGIN;
```

### snapshots

```sql
SELECT snapshot_id, source_mode, resource_id, sha256 FROM raw_snapshots WHERE snapshot_id IN (1,2,3,4) ORDER BY snapshot_id;
```

### summary

```sql
SELECT snapshot_id, source_mode, COUNT(*) rows,
MIN(parsed_date(source_mode,"Date")) first_date, MAX(parsed_date(source_mode,"Date")) last_date,
COUNT(DISTINCT parsed_date(source_mode,"Date")) distinct_dates,
SUM(parsed_date(source_mode,"Date") IS NULL) invalid_dates,
SUM(NOT valid_time("Time")) invalid_times,
SUM("Day"<>source_weekday(source_mode,"Date")) weekday_conflicts,
SUM(source_mode='bus' AND substr("Date",11)<>'T00:00:00') non_midnight_bus_dates,
SUM("Bound"<>'' AND "Bound" NOT IN ('N','S','E','W')) non_cardinal_bound,
SUM("Vehicle"='0') zero_vehicle,
COUNT(DISTINCT "Line") line_labels, COUNT(DISTINCT "Station") location_labels,
SUM(instr("Line",'/')>0) slash_line_rows,
SUM("Line"<>'' AND "Line" NOT GLOB '*[^0-9]*') numeric_only_line_rows,
MAX(length("Station")) max_location_length, SUM(length("Station")=22) location_length_22
 FROM staged_delay_records d JOIN raw_snapshots s USING(snapshot_id) WHERE snapshot_id IN (1,2,3,4) GROUP BY snapshot_id ORDER BY snapshot_id;
```

### missing_template

The shown query is the last executed field (Vehicle); the same quoted-field query ran for all 11 source columns.

```sql
SELECT snapshot_id, SUM("Vehicle" IS NULL) nulls, SUM(blank("Vehicle")) blanks, SUM("Vehicle"='') empty_strings, SUM("Vehicle"<>trim("Vehicle")) surrounding_spaces FROM staged_delay_records d JOIN raw_snapshots s USING(snapshot_id) WHERE snapshot_id IN (1,2,3,4) GROUP BY snapshot_id ORDER BY snapshot_id;
```

### duration_template

The shown query is Min Gap; it also ran with Min Delay. Integer syntax was independently checked before interpreting these actual sums; invalid text was guarded, not blindly cast.

```sql
SELECT snapshot_id,
 SUM(num_state("Min Gap")='invalid') invalid_numbers,
 SUM(num_state("Min Gap")='valid' AND CAST("Min Gap" AS REAL)=0) zeros,
 SUM(num_state("Min Gap")='valid' AND CAST("Min Gap" AS REAL)<0) negatives,
 SUM(num_state("Min Gap")='valid' AND CAST("Min Gap" AS REAL)>60) over_60,
 SUM(num_state("Min Gap")='valid' AND CAST("Min Gap" AS REAL)>120) over_120,
 SUM(num_state("Min Gap")='valid' AND CAST("Min Gap" AS REAL)>1440) over_1440,
 MIN(CASE WHEN num_state("Min Gap")='valid' THEN CAST("Min Gap" AS REAL) END) minimum,
 MAX(CASE WHEN num_state("Min Gap")='valid' THEN CAST("Min Gap" AS REAL) END) maximum,
 SUM(CASE WHEN num_state("Min Gap")='valid' THEN CAST("Min Gap" AS REAL) END) total
 FROM staged_delay_records d JOIN raw_snapshots s USING(snapshot_id) WHERE snapshot_id IN (1,2,3,4) GROUP BY snapshot_id ORDER BY snapshot_id;
```

### noninteger_durations

```sql
SELECT snapshot_id,SUM("Min Delay" GLOB '*[^0-9]*') delay_not_unsigned_integer,SUM("Min Gap" GLOB '*[^0-9]*') gap_not_unsigned_integer FROM staged_delay_records d JOIN raw_snapshots s USING(snapshot_id) WHERE snapshot_id IN (1,2,3,4) GROUP BY snapshot_id;
```

### duplicates

```sql
WITH g AS (
 SELECT snapshot_id,"Date", "Time", "Day", "Station", "Code", "Min Delay", "Min Gap", "Bound", "Line", "Vehicle",COUNT(*) n FROM staged_delay_records
 WHERE snapshot_id IN (1,2,3,4) GROUP BY snapshot_id,"Date", "Time", "Day", "Station", "Code", "Min Delay", "Min Gap", "Bound", "Line", "Vehicle" HAVING COUNT(*)>1)
 SELECT snapshot_id,COUNT(*) groups,SUM(n) affected_rows,SUM(n-1) excess FROM g GROUP BY snapshot_id ORDER BY snapshot_id;
```

### mismatch_dates

```sql
SELECT snapshot_id,parsed_date(source_mode,"Date") date,"Day",source_weekday(source_mode,"Date") derived_day,COUNT(*) n FROM staged_delay_records d JOIN raw_snapshots s USING(snapshot_id) WHERE snapshot_id IN (1,2,3,4) AND "Day"<>source_weekday(source_mode,"Date") GROUP BY snapshot_id,date,"Day",derived_day ORDER BY snapshot_id,date;
```

### missing_dates

```sql
WITH RECURSIVE bounds AS (
 SELECT snapshot_id,MIN(parsed_date(s.source_mode,d."Date")) lo,MAX(parsed_date(s.source_mode,d."Date")) hi FROM staged_delay_records d JOIN raw_snapshots s USING(snapshot_id) WHERE snapshot_id IN (1,2,3,4) GROUP BY snapshot_id),
 dates(snapshot_id,day,hi) AS (SELECT snapshot_id,lo,hi FROM bounds UNION ALL SELECT snapshot_id,date(day,'+1 day'),hi FROM dates WHERE day<hi)
 SELECT a.snapshot_id,a.day FROM dates a WHERE NOT EXISTS (SELECT 1 FROM staged_delay_records d JOIN raw_snapshots s USING(snapshot_id) WHERE d.snapshot_id=a.snapshot_id AND parsed_date(s.source_mode,d."Date")=a.day) ORDER BY a.snapshot_id,a.day;
```

### unmapped_codes

Parameters: JSON array of official dictionary rows, then explicit matching snapshot ID; executed separately for each mode.

```sql
WITH dict AS (SELECT json_extract(value,'$.CODE') code FROM json_each(?))
 SELECT d."Code" code,COUNT(*) rows FROM staged_delay_records d WHERE snapshot_id=? AND d."Code"<>'' AND NOT EXISTS (SELECT 1 FROM dict WHERE dict.code=d."Code") GROUP BY d."Code" ORDER BY d."Code";
```

### ambiguous_codes

Parameters: JSON array of official dictionary rows, then explicit matching snapshot ID; executed separately for each mode.

```sql
WITH dict AS (SELECT json_extract(value,'$.CODE') code,json_extract(value,'$.DESCRIPTION') description FROM json_each(?)),g AS (SELECT code,COUNT(*) entries,COUNT(DISTINCT description) descriptions FROM dict GROUP BY code HAVING COUNT(*)>1)
 SELECT g.*, (SELECT COUNT(*) FROM staged_delay_records d WHERE d.snapshot_id=? AND d."Code"=g.code) affected_rows FROM g;
```

### label_examples

```sql
SELECT snapshot_id,"Line",COUNT(*) rows FROM staged_delay_records WHERE (snapshot_id=2 AND "Line" IN ('100 FLEMINGDON PARK','100 FLEMINGTON PARK','999','FLEET VEHICLE','LINE 1 SHUTTLE')) OR (snapshot_id=3 AND "Line" IN ('504 KING','504 AKING','TRACK 11','CARHOUSE')) OR (snapshot_id=4) GROUP BY snapshot_id,"Line" ORDER BY snapshot_id,"Line";
```

### bound_values

```sql
SELECT snapshot_id,"Bound",COUNT(*) rows FROM staged_delay_records d JOIN raw_snapshots s USING(snapshot_id) WHERE snapshot_id IN (1,2,3,4) AND "Bound"<>'' AND "Bound" NOT IN ('N','S','E','W') GROUP BY snapshot_id,"Bound" ORDER BY snapshot_id,"Bound";
```

### gap_less_delay

```sql
SELECT snapshot_id,SUM(CAST("Min Gap" AS REAL)<CAST("Min Delay" AS REAL)) rows FROM staged_delay_records d JOIN raw_snapshots s USING(snapshot_id) WHERE snapshot_id IN (1,2,3,4) GROUP BY snapshot_id;
```

Final database checks: `PRAGMA integrity_check` returned `ok`; `PRAGMA foreign_key_check` returned no rows. Database and all raw/provenance hashes remain unchanged. No table, view, ingestion behaviour, profile, dictionary or acquisition file was changed. Only `docs/cleaning_validation_rules.md` was created for Task 4.1. Milestone 3 checkpoint is committed; these rules await review. Task 4.2 was not started.

# Data-model readiness — TTC delay sources

Assessment date: 2026-10-21. Status: **ready to design lossless staging and snapshot-based repeat ingestion; semantic normalization remains conditional.** This is a recommendation, not an implemented model or a claim that all source definitions are resolved.

## Evidence and limits

Read the governing documents, source assessment, cross-mode assessment, all four profiling reports/JSON results, and representative rows from each preserved CSV. Existing profile results are reused, not rerun. Raw files and completed artifacts remain unchanged.

For the remaining definition questions, successfully retrieved four official package metadata responses, four datastore schemas using `datastore_search` with `limit=0` (no delay records), three official README workbooks and four small Code Descriptions CSVs. Verified TLS used the already-installed certifi bundle; no dependencies were installed. README worksheet text was read using Python's standard-library ZIP/XML support. Documentation responses were inspected in temporary files outside the project. No new delay CSVs were acquired.

Evidence labels throughout:

- **Official/current:** definitions or types in the live Toronto datastore field metadata, or contents of a currently listed dictionary. This verifies what the publisher says, not that every value complies.
- **Official/legacy:** definitions in README workbooks last modified in April 2022. Their format/column names sometimes differ from the current resources. Carry-forward applicability is an interpretation unless current metadata agrees.
- **Observed:** prior profiles and selected unchanged raw examples; not proof of collection completeness or semantic equivalence.
- **Recommended:** a proposed local design policy; not a source fact.

Package metadata still declares Monthly refreshes and September 21, 2026 last refreshes. The browser-readable portal pages exposed empty dynamic field sections, so direct official metadata and README resources were used instead. No official incident inclusion/exclusion policy, timezone/service-day rule, or stable incident-ID contract was found in the inspected material. This is a bounded investigation, not proof that none exists elsewhere.

## Concise field dictionary

Exact shared names, in Subway order: `_id`, `Date`, `Time`, `Day`, `Station`, `Code`, `Min Delay`, `Min Gap`, `Bound`, `Line`, `Vehicle`. Bus/Streetcar/LRT place `Line` after `Date`; ingest by column name, not position. There are no mode-only columns in these snapshots.

Live datastore types are `_id`: integer; `Date`: timestamp for Bus, date for the other modes; **all remaining columns, including durations and Vehicle, are text**. Apparent numeric values in CSVs are not authoritative datastore numeric types.

| Exact column | Observed/apparent meaning | Official definition and applicability | Mode differences / recommended handling |
|---|---|---|---|
| `_id` | Sequential row identifier within each export | Current metadata declares integer, without a TTC incident definition. CKAN implementation supplies an internal row key; see identity findings below. | Store as source identifier text with snapshot context. Never use as permanent incident key. |
| `Date` | Reported incident/delay date; Bus has an all-midnight timestamp suffix | Current Subway/Streetcar/LRT metadata associates it with the delay date. Legacy Bus/Streetcar `Report Date` refers to when the incident occurred. Bus current metadata provides type only. | Parse the observed formats explicitly and retain original text. Bus midnight is not the incident time. No verified timezone, service-day boundary or conflict precedence. |
| `Time` | Reported time, observed as HH:MM | Current Subway/Streetcar/LRT metadata identifies delay time. Subway README describes a 24-hour clock. Legacy Bus/Streetcar documentation associates Time with incident occurrence, using an older display format. | Preserve minute precision; do not invent seconds, UTC offsets or an end timestamp. |
| `Day` | Reported English weekday label | Current Subway/Streetcar/LRT metadata identifies weekday; legacy Bus/Streetcar calls it the day name. | Preserve source label separately from weekday calculated from parsed Date. A conflict does not establish which source value is wrong. |
| `Station` | Free-text location: stations, intersections, facilities and longer descriptions | Current Subway/Streetcar/LRT metadata covers locations as well as stations. Subway legacy README is narrower. Legacy Bus/Streetcar `Location` describes incident location. | Bus mapping from old Location to current Station is inferred, not a verified migration contract. Not a station/stop key or geocode; retain exact string and mode. |
| `Code` | Reported incident category code | Current Subway/Streetcar/LRT metadata describes an incident category. Official dictionaries use CODE/DESCRIPTION. Legacy Bus/Streetcar `Incident` was a description, not the present code field. | Mode-scoped lookup; retain unrecognized codes. A category label is not independently verified root cause. Do not equate current Code with old Incident automatically. |
| `Min Delay` | Numeric-looking recorded delay amount | Current Subway/Streetcar/LRT metadata defines delay length in minutes. Subway README relates it to subway service. Legacy Bus/Streetcar defines schedule delay affecting the following vehicle. | Can store parsed reported minutes under a common technical name, retaining mode. Bus current applicability and exact operational equivalence remain conditional. Zeros are valid observed values; extremes are review candidates. |
| `Min Gap` | Separate numeric-looking gap amount | Current Subway/Streetcar/LRT field notes are empty; Bus has none. Subway legacy README relates it to spacing between trains in minutes. Legacy Bus/Streetcar refers to scheduled spacing involving the preceding and following vehicle. | LRT operational meaning is not established. Retain as reported gap with provisional minute interpretation outside Subway/legacy documentation; never sum with delay or assume Gap ≥ Delay. |
| `Bound` | Direction-like labels, blanks and unexpected tokens | Current Subway/Streetcar/LRT describes vehicle direction; Subway legacy ties direction to line. Legacy Bus/Streetcar Direction explains cardinal directions and B/b/BW for both ways. | Legacy meaning of B is useful context, not a verified current four-mode mapping. Do not automatically map B, numeric tokens or other letters; retain raw. |
| `Line` | Line/route label, combined lines, shuttles and operational text | Current Subway explicitly identifies subway line; Streetcar/LRT identifies the line involved. Legacy Bus/Streetcar Route is a route number. | Current Bus Line is interpreted as a route label, not guaranteed numeric route ID. Package-derived source mode must remain separate from Line or physical vehicle type. |
| `Vehicle` | Vehicle/train identifier, numeric-looking including 0 | Current Subway/Streetcar/LRT metadata identifies the vehicle; Subway README describes train number; legacy Bus/Streetcar describes vehicle number. | Preserve as text. No verified meaning of 0, namespace, permanence or correspondence to GTFS identifiers. |

Current field descriptions are in each mode's schema link below. README definitions explain history, but their older Date/Time representations and former Bus/Streetcar field names demonstrate why they cannot serve as a complete current schema contract. Streetcar's legacy Direction text even refers to a bus route; do not silently repair that documentation inconsistency.

## Record identity and counted events

**Observed, already verified:** _id runs uniquely from 1 through the row count in every preserved snapshot: Subway 45,475; Bus 102,257; Streetcar 23,703; LRT 4,569. These namespaces overlap. Rows identical except for _id remain: excess counts are respectively 66, 298, 18 and 5. Their legitimate-event versus duplicate status is unresolved.

**Platform evidence:** CKAN 2.11.6's PostgreSQL backend `create_table` declares `_id` as `serial primary key`, and its result-field code exposes it as integer. Thus the standard CKAN _id is datastore infrastructure, not a documented TTC event number. The live schemas and sequential exports are consistent with that mechanism. Toronto's deployed CKAN version, uploader implementation and pre-CKAN input rows were not inspected; the specific generation history of each Toronto value cannot be proved from an export alone. [CKAN backend source](https://raw.githubusercontent.com/ckan/ckan/ckan-2.11.6/ckanext/datastore/backend/postgres.py).

CKAN supports row updates, inserts and table deletion/recreation. These capabilities establish possibilities, not Toronto's actual refresh procedure. No source promises _id persistence. A key stable during an in-place update could change after table recreation or reload. `(resource_id, _id)` therefore cannot safely identify the same TTC incident across snapshots. [CKAN DataStore API](https://docs.ckan.org/en/2.11/maintaining/datastore.html#the-data-api).

**Recommended counting contract:** retain one local record per source row in a selected snapshot, including zeros and duplicate candidates. Call the initial measure “recorded rows” or explicitly defined “recorded incident records,” not unique real-world incidents. A unique-incident count requires a defensible identity rule not currently supplied. Do not use DISTINCT, guessed date/time keys or a content hash to remove repeated events by default.

**Duration contract:** keep Min Delay and Min Gap separate. A sum of parsed Min Delay is a sum of recorded source minutes under documented inclusion rules; it does not measure passenger-minutes, total interruption duration or normalized service reliability. Simultaneous records could describe overlapping effects. No inspected documentation establishes incident thresholds, all-zero semantics, 999-like sentinel meanings, reporting exclusions, duplicate handling, or cross-mode collection parity. Do not infer such rules from value distributions.

## Code dictionaries: verified content, incomplete coverage

The current listed dictionaries have `_id`, `CODE`, `DESCRIPTION`. Comparing their exact CODE values with the existing profiles' category-frequency maps is a semantic coverage check, not a repeat of raw profiling. Do not use another mode's dictionary to silently fill omissions.

| Mode | Dictionary rows / distinct CODE | Observed nonblank codes | Observed codes absent from own dictionary | Rows using those codes | Blank Code rows |
|---|---:|---:|---:|---:|---:|
| Subway | 140 / 140 | 140 | 10 | 1654 | 0 |
| Bus | 46 / 46 | 75 | 35 | 5468 | 0 |
| Streetcar | 85 / 85 | 148 | 74 | 3225 | 1 |
| Lrt | 130 / 128 | 115 | 16 | 531 | 0 |

Examples: SUDP is labelled DISORDERLY PATRON in Subway's dictionary; Bus MFDV and Streetcar MTDV are labelled ON DIVERSION in their respective dictionaries; LRT PXOV is labelled OVERHEAD DEFECT. These are published category labels, not causal verification. Subway SUL, Bus EFAS, Streetcar MFDV and LRT SXGDS are examples absent from their own current dictionaries despite appearing in the preserved data.

LRT's EXVE occurs twice with **different descriptions** (work vehicle versus unspecified vehicle problem); TXSUP occurs twice with the same description. Blindly joining on CODE could multiply records. Bus MFUIR's description also contains visibly corrupted dash characters when decoded as UTF-8; preserve the supplied text and flag encoding quality rather than silently rewriting it. Neither a missing mapping nor an encoding problem invalidates the original delay row.

Recommended enrichment: retain dictionary source/version and original rows, test uniqueness before joining, resolve identical duplicates only by an explicit lookup rule, and leave conflicting/unmatched codes flagged without choosing a description arbitrarily. Any candidate left join must preserve the delay row count and Min Delay total. Do not collapse codes into a universal cause hierarchy until definitions and coverage are validated.

## Cross-mode compatibility and LRT caution

**Safe technical commonality:** snapshot provenance, source mode, exact source values, row position, parsed source date/time, separately parsed delay/gap numbers and parse/quality flags. These can share a structural representation without claiming equivalent recording practices. Store common columns by explicit names; preserve original column order in snapshot schema metadata.

**Conditional analytical commonality:** temporal patterns, source-category frequencies and reported-minute distributions can support within-mode investigation. For date-based summaries, label derived weekdays as calculated from the source Date, not as corrected truth; keep source Day and conflict flags. Avoid presenting affected weekday patterns as validated until conflicts are investigated. Route/line, location, direction, category and Vehicle interpretations remain mode-scoped, even when labels match. Do not force a route, station dimension or geographic match now.

LRT has 420 Day/Date conflicts in 4,569 rows (about 9.2%), compared with 63/45,475 Subway, 130/102,257 Bus and 42/23,703 Streetcar. Existing comparison evidence locates many LRT conflicts on Sundays, beyond the shared 2026-04-26 issue; an example is 2025-12-27 labelled Friday. This does not prove a timezone shift, a service-day convention or which field is correct. Retain both values and flag the conflict; never shift dates to force agreement.

Subway/Bus/Streetcar observed coverage is 2025-01-01–2026-08-31. LRT is 2025-12-07–2026-08-31, with no records dated 2026-01-23 within that interval. In the existing Line-coverage results, FW first appears 2025-12-07 and EC first appears 2026-02-08; combined/other labels also occur. These are reporting endpoints, not independently verified opening dates or complete line coverage. Do not backfill missing LRT periods with zeros or compare full-period mode totals as reliability scores. Even a common overlapping window cannot supply exposure denominators or guarantee comparable reporting.

## Updates: verified facts and conservative recommendation

Verified catalog facts: all packages declare Monthly; the inventory has datastore delay tables and separately identified CSV/XML/JSON cache uploads. The preserved downloads' HTTP Last-Modified headers are September 21, 2026, and the current metadata check still shows September refreshes and matching datastore totals. CKAN documents table access and downloadable exports, but that does not prove byte-for-byte cache/table equivalence, cache freshness, or Toronto's refresh implementation. [CKAN DataStore/download documentation](https://docs.ckan.org/en/2.11/maintaining/datastore.html).

No later delay snapshot was acquired in this assessment. There is no before/after content evidence of an actual monthly revision. Whether files are replaced under the same ID, IDs are reassigned, rows are corrected/deleted, exports lag, or history eventually rolls off remains unknown. No append-only strategy is justified.

Recommended minimum behavior for future implementation:

1. Treat each resource download as a complete candidate snapshot of that resource's **observed contents**, not guaranteed complete history. Preserve bytes/provenance and record repeated retrieval attempts separately from logical snapshot identity. A SHA-256 hash detects equal bytes, not equal real-world incidents.
2. Reprocessing the same resource/content hash should not add another copy to active staging. A different hash creates a new immutable snapshot. Preserve the previous accepted snapshot while checking schema, coverage and reconciliation.
3. Build a candidate curated result from one selected snapshot per mode, then switch that mode's active reference atomically after validation; do not union every historical snapshot into current counts. Keep prior snapshots available for reproducibility. A failure must leave accepted outputs unchanged.
4. Investigate a shrinking date range or row count before promotion; it may indicate incomplete/rolling exports rather than legitimate deletion. Do not overwrite or silently discard older history. Changed IDs/URLs require review as possible replacements of the same series, not automatic additional series.
5. Compare overlapping snapshots using exact-value row multisets excluding _id, retaining multiplicity, alongside _id/content comparisons. This can reveal reordered IDs, revised values and changed counts; it cannot uniquely match indistinguishable incidents. Rebuild current-mode results from the selected snapshot until stable identity is established.
6. Track metadata, schema, hashes and retrieval time together. ETag/Last-Modified/count are useful hints, not authoritative row-change guarantees. Version code dictionaries independently and record the actual set of mode snapshots used for a cross-mode output.

These are safety requirements for the design, not implemented ingestion, transformations or update automation.

## Recommended minimum structures (conceptual only)

| Structure / grain | Minimum contents | Identity and reason |
|---|---|---|
| Snapshot/provenance: one immutable content snapshot for a source resource | Internal snapshot reference; package and CSV resource IDs; related datastore ID separately; source mode; URL; raw path; retrieval event metadata; hash/size; HTTP status/headers; source schema; parser version; observed row count/date range; acceptance status | Resource identity plus content hash supports repeat detection; retrieval history does not duplicate analytical rows. A selected/accepted snapshot reference identifies each mode's current version. |
| Raw staging: one row per parsed CSV record per snapshot | All 11 source columns as exact strings, including blanks and original Date representation; snapshot reference; one-based data-record ordinal; parsing failures if any | `(snapshot reference, record ordinal)` is a local row key, not an incident key. Keep original _id as data; preserve repeated source records. No eager type conversion or lookup joins. |
| Curated records: one row per staging row under a specified transformation version | Staging reference; source mode; parsed source date and time; source Day plus derived calendar weekday/conflict flag; parsed Min Delay/Min Gap; raw category/location/line/direction/Vehicle; parse, blank, extreme-value and duplicate-candidate flags | Preserve row-level lineage and distinguish parse failure from zero. No forced canonical route/station or global event ID. Use only selected accepted snapshots in default current outputs. Explicitly version any later exclusions. |

Do not duplicate all raw fields unnecessarily in curated storage: retain them through the staging reference or a view. Select an engine and physical table/view representation in the next approved architecture task. No star schema or mapping framework is needed to preserve this evidence.

Code descriptions can remain a separately versioned reference artifact initially. If added as a relation, preserve its original rows and scoped CODE/description plus dictionary-snapshot reference; do not pretend CODE alone is unique until conflict handling is approved. The conflicting LRT dictionary prevents a naive dimension join, not lossless staging.

## Implementation tests and remaining decisions

| Specific test/question | Required result / fallback |
|---|---|
| Same snapshot loaded twice; interrupted parse/load | No extra active rows; no partial accepted result; deterministic row count and source totals. |
| New snapshot with reordered/reset _id, changed old record, repeated identical rows, deletion, narrower coverage, or replacement resource ID | Preserve old evidence; detect differences without using _id as cross-version identity; review shrinkage/replacement before promotion. Controlled fixtures may test failure behavior; they cannot prove actual City revision practice. |
| Header reordered, renamed, added, removed; Bus non-midnight Date; invalid Date/Time/number | Explicit schema/parse results with retained raw values; no silent truncation, dropped records or default zeros. Do not impose integer-only duration types permanently without a checked rule. |
| One curated row per staging row, including repeat candidates and zero minutes | Reconcile counts and valid recorded-minute totals. Exclusions, if ever approved, need separately reconciled counts/totals. |
| Dictionary missing/blank code, conflicting EXVE, repeated TXSUP or corrupted description | No row multiplication or dropped delay records; explicit unmatched/conflict flags and independent dictionary version. |
| Source Day disagrees with Date, especially LRT | Reproduce conflict flags; seek authoritative calendar/service-day guidance. No silent date correction; weekday interpretation remains provisional. |
| Meaning of Min Gap, Gap < Delay, zeros and extreme/999-like durations | Preserve separate source fields and flags; obtain current operational definitions before exclusion or combined metrics. |
| Incident inclusion threshold, multi-row events, route/mode identity, Vehicle 0, Bound B/other tokens, label length limits | Keep mode-specific raw interpretation and refrain from unique-incident counts, automatic normalization or reliability rates until supported. |
| Missing LRT day/early months, per-line start dates and September/October absence | Distinguish observed coverage from reporting/operating completeness. Never replace absent records with zero service delay. |
| Actual publication mechanism and historical revisions | Observe successive approved raw snapshots or obtain a publisher contract. Metadata-only agreement is insufficient; retain snapshot-based rebuild capability. |

Lossless staging can proceed after the next design approval without answering every analytical question. Final incident identity, operationally equivalent gap metrics, automatic category mapping and validated weekday comparisons are not ready to claim.

## Source register and verification record

Official sources consulted on 2026-10-21; every direct package/schema/README/code request below returned HTTP 200. API `success` is true for all four schema responses. Direct schema responses returned no records (`limit=0`) and exact totals 45,475 / 102,257 / 23,703 / 4,569. README workbook examples are Excel serial encodings in the source; they were not misreported as incident dates.

| Mode | Current package / field metadata | README (legacy) | Code dictionary |
|---|---|---|---|
| Subway | [Package](https://ckan0.cf.opendata.inter.prod-toronto.ca/api/3/action/package_show?id=ttc-subway-delay-data) · [Fields](https://ckan0.cf.opendata.inter.prod-toronto.ca/api/3/action/datastore_search?resource_id=6088e14f-e46e-4f5c-9daa-dea1359ad396&limit=0) | [Workbook](https://ckan0.cf.opendata.inter.prod-toronto.ca/dataset/996cfe8d-fb35-40ce-b569-698d51fc683b/resource/ca43ac3d-3940-4315-889b-a9375e7b8aa4/download/ttc-subway-delay-readme.xlsx) | [CSV](https://ckan0.cf.opendata.inter.prod-toronto.ca/dataset/996cfe8d-fb35-40ce-b569-698d51fc683b/resource/b2d8f5e0-0997-46b5-8abd-caa685a0290b/download/code-descriptions.csv) |
| Bus | [Package](https://ckan0.cf.opendata.inter.prod-toronto.ca/api/3/action/package_show?id=ttc-bus-delay-data) · [Fields](https://ckan0.cf.opendata.inter.prod-toronto.ca/api/3/action/datastore_search?resource_id=c3451ac9-c04a-4645-bd80-0e2a3b7d7199&limit=0) | [Workbook](https://ckan0.cf.opendata.inter.prod-toronto.ca/dataset/e271cdae-8788-4980-96ce-6a5c95bc6618/resource/71bb1283-7388-4d23-aa4e-0f393a80abce/download/ttc-bus-delay-data-readme.xlsx) | [CSV](https://ckan0.cf.opendata.inter.prod-toronto.ca/dataset/e271cdae-8788-4980-96ce-6a5c95bc6618/resource/874ae66c-9f6f-443f-91e0-1d37d416e0d8/download/code-descriptions.csv) |
| Streetcar | [Package](https://ckan0.cf.opendata.inter.prod-toronto.ca/api/3/action/package_show?id=ttc-streetcar-delay-data) · [Fields](https://ckan0.cf.opendata.inter.prod-toronto.ca/api/3/action/datastore_search?resource_id=7d545629-745c-4fbf-a348-76692bb2772d&limit=0) | [Workbook](https://ckan0.cf.opendata.inter.prod-toronto.ca/dataset/b68cb71b-44a7-4394-97e2-5d2f41462a5d/resource/0fe61851-c67b-49bc-8c27-3a89b33b43af/download/ttc-streetcar-delay-data-readme.xlsx) | [CSV](https://ckan0.cf.opendata.inter.prod-toronto.ca/dataset/b68cb71b-44a7-4394-97e2-5d2f41462a5d/resource/06d13be4-a8b7-4365-ac68-2169de8e0630/download/code-descriptions.csv) |
| Lrt | [Package](https://ckan0.cf.opendata.inter.prod-toronto.ca/api/3/action/package_show?id=ttc-lrt-delay-data) · [Fields](https://ckan0.cf.opendata.inter.prod-toronto.ca/api/3/action/datastore_search?resource_id=8de5f6e3-9e5b-49c5-9f06-9f3b556966ec&limit=0) | No README listed in this inventory | [CSV](https://ckan0.cf.opendata.inter.prod-toronto.ca/dataset/d4d64b0e-2945-4c92-960e-f0103ad48b02/resource/662bc8f7-887f-4112-8b8d-dbc6bc4ebfb1/download/code-descriptions.csv) |

Local anchors: [cross-mode assessment](cross_mode_assessment.md), [comparison verification](cross_mode_verification.json), per-mode `*_tracer_profile.md` / `.json`, preserved raw paths and dated provenance already recorded there. Code dictionary exact-match checks used existing profile frequencies; no raw profiling scripts were rerun. Local spot checks inspected actual CSV headers/examples, including a reported Day conflict, and compared the dictionaries' CODE/DESCRIPTION rows. No source text was silently normalized.

Commands actually executed: read project files with `cat`; Python CSV/JSON reads and pre-task SHA-256 inventory; `python3 /tmp/ttc_semantics_sources.py` under elevated network access with verifying certifi TLS; Python ZIP/XML extraction and dictionary exact-match checks; official portal/CKAN documentation browsing; final Python assertions over field names, source responses, dictionary statistics and unchanged pre-existing files. Temporary source inspection code/responses live outside the project and are not a new pipeline component.

Only `reports/data_model_readiness.md` was created. No existing project file was modified, no raw delay bytes were changed/downloaded, and no dependencies, tables, transformations, analytical queries, commits or pushes were introduced. Stop for review before architecture or implementation.

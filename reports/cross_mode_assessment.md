# Cross-mode source profiling — Milestone 2

Assessment date: 2026-10-21. All observations refer to preserved snapshots acquired on this date, not live ongoing coverage.

## Method and scope

The existing acquisition and profiling scripts were parameterized with explicit mode/resource selection, schema-order tolerance, mode-specific date parsing, manifest record counts, and distinct output filenames. Filenames retain their original Subway names for command compatibility. Subway bytes, provenance and completed reports were preserved. No cleaning, deduplication, database, SQL, dashboard or update automation was implemented.

Each acquisition used the exact approved manifest URL, Python 3.11.9 and the already-installed certifi bundle with certificate and hostname verification enabled. Only Bus, Streetcar and LRT were downloaded in this task; all returned HTTP 200. No dependencies were installed. Raw snapshots and output reports use exclusive creation.

Strict UTF-8/CSV parsing retained every record. Blank means empty or whitespace-only; literal null-like strings were counted separately. Nearest-rank percentiles and >60/>120/>1440 minute thresholds are descriptive review flags, not rules for exclusion. All columns and exact category frequencies appear in per-mode JSON profiles.

## Coverage and missingness

| Mode | Rows | Observed date range | Days with records | Days absent within range | Blank Bound | Blank Line | Blank Code | Weekday conflicts |
|---|---:|---|---:|---:|---:|---:|---:|---:|
| Subway | 45,475 | 2025-01-01–2026-08-31 | 608 | 0 | 15,860 | 177 | 0 | 63 |
| Bus | 102,257 | 2025-01-01–2026-08-31 | 608 | 0 | 21,327 | 1,241 | 0 | 130 |
| Streetcar | 23,703 | 2025-01-01–2026-08-31 | 608 | 0 | 5,327 | 352 | 1 | 42 |
| Lrt | 4,569 | 2025-12-07–2026-08-31 | 267 | 1 | 773 | 7 | 0 | 420 |

Every date, time and numeric value parsed in all four files, and no malformed-width records were found. The table contains all nonzero blank counts; every other column has zero blanks. No literal null-like tokens or leading/trailing whitespace were observed. Zero Vehicle values are not counted as blank.

Subway, Bus and Streetcar cover all 608 calendar dates between their endpoints. LRT begins 2025-12-07 and has no records dated 2026-01-23 within its 268-day endpoint span. This does not establish zero-delay service, missing reporting, or an operating start date. All four end on 2026-08-31 despite retrieval in October and September Last-Modified headers. September/October coverage and publication lag remain unresolved. Count agreement with datastore metadata does not establish complete incident capture.

## Schema and identifiers

All four expose the same 11 column names: `_id`, `Date`, `Time`, `Day`, `Station`, `Code`, `Min Delay`, `Min Gap`, `Bound`, `Line`, `Vehicle`. No mode-specific columns were observed.

Bus, Streetcar and LRT order columns as `_id, Date, Line, Time, Day, Station, Code, Min Delay, Min Gap, Bound, Vehicle`; Subway places Line after Bound. Bus Date is `YYYY-MM-DDTHH:MM:SS`, with every timestamp suffix `T00:00:00`; the other modes use `YYYY-MM-DD`. Time is separate `HH:MM` without a timezone in all four. Date/time semantics still require documentation.

`_id`, Min Delay, Min Gap and Vehicle contain integer-looking numeric text. Day, Station, Code, Bound and Line are text. Vehicle and _id should retain source values: numeric-looking identifiers are not measurements.

All four _id columns are individually unique, sequential from 1 to their row count. IDs overlap between modes and are not globally unique. Snapshot uniqueness does not establish persistent incident identity across refreshes.

| Mode | Exact duplicate excess (all columns) | Duplicate groups excluding _id | Rows in those groups | Excess excluding _id | Potential key excess |
|---|---:|---:|---:|---:|---:|
| Subway | 0 | 66 | 132 | 66 | 76 |
| Bus | 0 | 297 | 595 | 298 | 336 |
| Streetcar | 0 | 18 | 36 | 18 | 42 |
| Lrt | 0 | 2 | 7 | 5 | 11 |

Potential key = Date, Time, Station, Code, Bound, Line. This is a profiling hypothesis, not a proven incident key. Repeated rows may include legitimate repeated events. No records were removed.

## Recorded duration observations

| Mode | Zero Min Delay | Negative | Median | P99 | Max | >60 | >120 | Raw sum Min Delay | Vehicle 0 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Subway | 29,669 | 0 | 0 | 26 | 900 | 110 | 41 | 122071 | 18008 |
| Bus | 12,974 | 0 | 12 | 247 | 999 | 4209 | 2220 | 2163102 | 4986 |
| Streetcar | 5,279 | 0 | 10 | 154 | 999 | 1188 | 365 | 416513 | 1467 |
| Lrt | 1,908 | 0 | 3 | 122 | 971 | 110 | 46 | 38829 | 1149 |

Counts and recorded minutes measure different things. These uncleaned sums retain zero-duration and possible duplicate records; they are not rankings of reliability or passenger impact. No Min Delay or Min Gap value exceeds 1,440 minutes. Min Gap is separate and is never added to Min Delay. Their intended relationship is unverified; Min Gap is smaller than Min Delay in subway: 744 rows, bus: 758 rows, streetcar: 256 rows, lrt: 100 rows.

## Labels, locations and source concerns

- **Subway:** 140 nonblank codes; 38 Line labels including blank; 1251 Station values. Non-cardinal nonblank Bound values: `{'B': 62}`.
- **Bus:** 75 nonblank codes; 664 Line labels including blank; 16396 Station values. Non-cardinal nonblank Bound values: `{'2': 1, '3': 1, '4': 2, '7': 1, '8': 2, 'A': 2, 'B': 33, 'D': 4, 'G': 1, 'M': 6, 'Q': 1, 'Z': 1, '`': 1}`.
- **Streetcar:** 148 nonblank codes; 198 Line labels including blank; 3130 Station values. Non-cardinal nonblank Bound values: `{'8': 1, 'B': 16}`.
- **Lrt:** 115 nonblank codes; 9 Line labels including blank; 317 Station values. Non-cardinal nonblank Bound values: `{'B': 2}`.

- Bus Line contains route names, numeric-only labels, branches, shuttles and operational labels. Examples include `100 FLEMINGDON PARK` vs `100 FLEMINGTON PARK`, `999`, `FLEET VEHICLE` and `LINE 1 SHUTTLE`. Streetcar similarly mixes `504 KING`, `504 AKING`, `TRACK 11`, `CARHOUSE` and Bus-like labels. Do not infer physical vehicle mode from route names alone.
- Subway Line has combined or inconsistent abbreviations and other-route labels; its completed report preserves examples. LRT includes EC/FW combinations and generic LRT labels; EC and FW meanings require official confirmation.
- Bus code `XXXXX` occurs once; Streetcar has `XXXXX` 53 times and one empty Code. LRT contains `MFUIR` once alongside predominantly other code families. Treat these as review candidates; no dictionary validation was performed.
- Station contains location strings, not verified station IDs. Observed maxima for Station and Line lengths are in the comparison JSON. Apparent truncation, spelling variants, intersections, facilities and route combinations make location grouping uncertain.
- Weekday/date conflicts recur across modes. All four have conflicts on 2026-04-26; LRT also has conflicts on other dates. These overlaps warrant source investigation; they do not establish a shared cause or which field is correct.

Observed LRT coverage by exact Line label:

| Line (blank shown explicitly) | Rows | First observed | Last observed |
|---|---:|---|---|
| (blank) | 7 | 2026-04-15 | 2026-08-26 |
| EC | 2743 | 2026-02-08 | 2026-08-31 |
| EC/FW | 3 | 2026-07-27 | 2026-08-29 |
| ECLRT/FWLRT | 1 | 2026-06-17 | 2026-06-17 |
| EGLINTON/FINCH | 1 | 2026-03-27 | 2026-03-27 |
| FW | 1808 | 2025-12-07 | 2026-08-31 |
| FW (OTC) | 2 | 2026-03-23 | 2026-03-23 |
| FW/EC | 3 | 2026-04-21 | 2026-05-19 |
| LRT | 1 | 2026-07-23 | 2026-07-23 |

These are record endpoints, not independently verified dates of service availability.

## What may support shared analysis, and what must remain mode-specific

Date/Time may support calendar/hour patterns after resolving timestamp, timezone and service-day meaning. Recorded row counts and Min Delay distributions are candidates for within-mode analysis after recording definitions and duplicate treatment are agreed. Source mode, raw value and snapshot identity must remain traceable. These are possibilities supported by the schema, not implemented transformations.

Code meanings, route/line interpretation, direction conventions, location normalization and Vehicle placeholders require mode-specific review. Shared spellings or columns do not establish equivalent event definitions, thresholds or collection practices. Comparing raw totals across unequal coverage or exposure would not answer which service is more reliable.

## Questions for official documentation and code dictionaries

1. What constitutes a recorded incident in each mode? Which events are omitted, and can several records describe one incident?
2. What do Min Delay and Min Gap measure, including zeros, extreme values and Gap smaller than Delay? Are 999-like values valid durations or sentinels?
3. Which date/day field is authoritative? Are dates calendar or operating-service dates, and what timezone applies?
4. Are code dictionaries mode-specific/versioned? How should XXXXX, blank codes and codes shared between packages be interpreted?
5. What do Bound B and unexpected numeric/letter values mean? Do Vehicle 0 and blank Line mean unknown or not applicable?
6. Are Station/Line strings length-limited? How should combined lines, shuttle labels, facilities and apparent misspellings be interpreted?
7. What is the LRT reporting start, which lines are included, why is 2026-01-23 absent, and what explains the shorter observed period?
8. Are exports complete and current? Can older rows be revised or IDs reassigned? A single snapshot cannot establish safe update behavior.

No official dictionaries or extra resources were downloaded. Apparent completeness remains a reporting question, not a conclusion from these CSVs.

## Acquisition inventory and verification

| Mode | Bytes | SHA-256 | Provenance |
|---|---:|---|---|
| Subway | 3069485 | `ec7c36eeb4785e34d58229e5da6af741c89dfdf9fa59c58a63abe5b026b95c44` | `data/provenance/20261021T190204614685Z__subway.json` |
| Bus | 9492730 | `1474f16414e63aaeab58714c236446ea370f5e00e072a3b97fdfeb1f079cd8fe` | `data/provenance/20261021T190548363172Z__bus.json` |
| Streetcar | 1882886 | `c6c081880619ffff8779c61af3a0b77466471473a014d8dec48d16306ddf9606` | `data/provenance/20261021T190549738480Z__streetcar.json` |
| Lrt | 313915 | `a493ad2f0d3c2889c34eba7cb42b3c27fc1d6cbf15728be09d7f1b230964984a` | `data/provenance/20261021T190550293696Z__lrt.json` |

Resource IDs and full URLs, retrieval timestamps, HTTP headers, Python version, CA-bundle path/hash and TLS flags are in each provenance record. Raw paths and exact columns are in each profile. Raw data are Git-ignored; provenance/reports are versionable.

Executed acquisitions: `python3 scripts/acquire_subway_tracer.py --mode bus`, then `--mode streetcar`, then `--mode lrt` (elevated network access).

Executed profiles: `python3 scripts/profile_subway_tracer.py <provenance>` for each of the three new provenance paths above. Existing Subway results were read and independently reconciled, not regenerated.

Verification/comparison command: `python3 scripts/verify_and_compare_modes.py`. It independently checks bytes/hash against provenance and HTTP Content-Length, exact manifest URLs and size, raw schema/row count, blanks/distinct values, numeric parsing, ISO dates/times, monthly counts, missing dates, weekday conflicts, both duration fields and percentiles, all category frequencies, _id sequence and four duplicate definitions. Every check passed for all four modes. All raw row counts match their manifest datastore counts.

Reports refuse overwrite. No completed milestone documents, discovery metadata, Subway raw/provenance or Subway reports were changed. Git has no commits; session hashes provide the before/after comparison. No commit or push was performed. Stop here for review.

## Session file audit

Modified existing files:

- `scripts/acquire_subway_tracer.py`
- `scripts/profile_subway_tracer.py`

Created files:

- `data/provenance/20261021T190548363172Z__bus.json`
- `data/provenance/20261021T190549738480Z__streetcar.json`
- `data/provenance/20261021T190550293696Z__lrt.json`
- `data/raw/bus/20261021T190548363172Z__b5725365-9252-4bfe-b6f4-cda7ddf74341.csv`
- `data/raw/lrt/20261021T190550293696Z__9a800c92-0362-4cee-8232-7374596b6a43.csv`
- `data/raw/streetcar/20261021T190549738480Z__cf2fdd12-6f0e-4644-aae7-0bbfc31df031.csv`
- `reports/bus_tracer_profile.json`
- `reports/bus_tracer_profile.md`
- `reports/cross_mode_assessment.md`
- `reports/cross_mode_verification.json`
- `reports/lrt_tracer_profile.json`
- `reports/lrt_tracer_profile.md`
- `reports/streetcar_tracer_profile.json`
- `reports/streetcar_tracer_profile.md`
- `scripts/verify_and_compare_modes.py`

SHA-256 comparisons with a pre-task inventory confirmed every other pre-existing file is byte-for-byte unchanged, including governing documents, source assessment, manifest, discovery script, and all Subway data/provenance/reports. Python syntax checks passed for all three scripts.

# LRT tracer inspection

Inspection date: 2026-10-21

## Acquisition and method

Source: `ttc-lrt-delay-data`, resource `9a800c92-0362-4cee-8232-7374596b6a43`. URL resolved from the unchanged local manifest. Only the selected CSV was downloaded by this acquisition command.

HTTP 200; 313,915 bytes; SHA-256 `a493ad2f0d3c2889c34eba7cb42b3c27fc1d6cbf15728be09d7f1b230964984a`. Raw snapshot: `data/raw/lrt/20261021T190550293696Z__9a800c92-0362-4cee-8232-7374596b6a43.csv`. Provenance: `data/provenance/20261021T190550293696Z__lrt.json`.

Python `/Library/Frameworks/Python.framework/Versions/3.11/bin/python3` (3.11.9); installed certifi CA bundle `/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages/certifi/cacert.pem`; `CERT_REQUIRED` and hostname verification enabled. No dependencies installed. HTTP Content-Length matched the saved size. HTTP Last-Modified: `Mon, 21 Sep 2026 12:20:16 GMT`. Full headers and CA-bundle hash are in provenance.

Profiling uses the Python standard library, strict CSV parsing and UTF-8 decoding. Raw bytes are verified against provenance before and after profiling. No source rows are altered, removed, or ingested. Blank means empty or whitespace-only; literal null-like tokens are counted separately, not converted. Types below are observations, not source definitions.

## Schema and missingness

| Exact column | Apparent type | Blank | Distinct (including blank) | Numeric failures |
|---|---|---:|---:|---:|
| `_id` | integer-looking numeric text | 0 | 4569 | 0 |
| `Date` | date text (YYYY-MM-DD) | 0 | 267 | — |
| `Line` | text | 7 | 9 | — |
| `Time` | time text (HH:MM; no timezone) | 0 | 1245 | — |
| `Day` | text | 0 | 7 | — |
| `Station` | text | 0 | 317 | — |
| `Code` | text | 0 | 115 | — |
| `Min Delay` | integer-looking numeric text | 0 | 139 | 0 |
| `Min Gap` | integer-looking numeric text | 0 | 141 | 0 |
| `Bound` | text | 773 | 6 | — |
| `Vehicle` | integer-looking numeric text | 0 | 121 | 0 |

Records: **4,569**; malformed-width rows: 0. Date failures: 0; time failures: 0; weekday mismatches: 420.
Literal null-like tokens: `{}`. Values with surrounding whitespace: `{}`.

## Observed coverage

Parsed dates: **2025-12-07 through 2026-08-31**; 267 distinct incident dates. Dates before 2025: 0; dates after retrieval: 0. Dates without records between endpoints: 1 (listed in JSON).

The 4,569 CSV records match the snapshot's 4,569 datastore record_count. Count agreement does not prove identical contents, complete reporting, or absence of revisions. Missing dates or periods do not establish zero-delay service. No records beyond the maximum date can be inferred from the filename or monthly refresh label.

| Month | Recorded rows |
|---|---:|
| 2025-12 | 350 |
| 2026-01 | 386 |
| 2026-02 | 598 |
| 2026-03 | 650 |
| 2026-04 | 511 |
| 2026-05 | 530 |
| 2026-06 | 546 |
| 2026-07 | 517 |
| 2026-08 | 481 |

## Recorded durations

Thresholds above 60, 120 and 1,440 minutes are descriptive review flags, not validated error rules. Percentiles use nearest rank. Min Gap is profiled separately; it is not added to Min Delay.

| Field | Zero | Negative | Min | Median | P95 | P99 | Max | >60 | >120 | >1440 | Sum |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Min Delay | 1908 | 0 | 0 | 3 | 30 | 122 | 971 | 110 | 46 | 0 | 38829 |
| Min Gap | 2003 | 0 | 0 | 9 | 39 | 128 | 981 | 122 | 51 | 0 | 55939 |

Recorded row count (4,569) and the sum of Min Delay (38829 recorded minutes) are different measures. Zero-minute rows remain records. These are uncleaned source totals, not passenger impact or normalized reliability measures.
Min Gap is less than Min Delay in 100 rows; the fields' intended relationship requires documentation. The JSON includes the five largest rows for each duration field.

## Duplicate candidates and identifiers

| Definition | Repeated groups | Rows in groups | Excess beyond first |
|---|---:|---:|---:|
| All 11 columns | 0 | 0 | 0 |
| All columns except _id | 2 | 7 | 5 |
| Date, Time, Station, Code, Bound, Line | 6 | 17 | 11 |
| Date, Time, Station, Line | 17 | 39 | 22 |

_id summary: `{'minimum': '1', 'maximum': '4569', 'distinct': 4569, 'duplicate_excess': 0, 'sequential_in_file': True}`. Export ID uniqueness does not establish stable incident identity across refreshes. Candidate keys are hypotheses, not documented unique keys; repeated groups may contain legitimate concurrent or repeated incidents. Nothing was deleted. JSON includes examples.

## Codes and categories

Distinct Code values (including blank): 115; stations: 317; vehicle values: 121. Full exact value frequencies for Code, Day, Station, Bound, Line and Vehicle are in the JSON; no codes were translated into causes.

Day frequencies: `{'Friday': 702, 'Monday': 680, 'Saturday': 989, 'Sunday': 202, 'Thursday': 630, 'Tuesday': 693, 'Wednesday': 673}`.
Bound frequencies: `{'': 773, 'B': 2, 'E': 1987, 'N': 1, 'S': 7, 'W': 1799}`.
Line frequencies: `{'': 7, 'EC': 2743, 'EC/FW': 3, 'ECLRT/FWLRT': 1, 'EGLINTON/FINCH': 1, 'FW': 1808, 'FW (OTC)': 2, 'FW/EC': 3, 'LRT': 1}`.
Vehicle `0` occurs 1149 times; whether it means unknown, not applicable, or an actual identifier is unresolved. Vehicle identifiers should be retained as source text pending definition checks.

Most frequent codes: `EXO` (392), `SXGDS` (356), `MXPAA` (339), `EXBK` (301), `PXSW` (206), `SXUEG` (187), `EXGA` (144), `EXDO` (134), `MXO` (133), `EXATC` (128), `EXCE` (115), `TXO` (109), `EXAC` (109), `SXO` (106), `SXUT` (96).

## Additional source observations

Exact column order: `['_id', 'Date', 'Line', 'Time', 'Day', 'Station', 'Code', 'Min Delay', 'Min Gap', 'Bound', 'Vehicle']`. Same names as Subway; different order.
Date suffix frequencies: `{'': 4569}`. Bus timestamp dates are parsed explicitly; any non-midnight components remain in the source and are not silently removed.
Date/weekday mismatch examples: `[{'record_number': 278, 'date': '2025-12-27', 'day': 'Friday'}, {'record_number': 279, 'date': '2025-12-27', 'day': 'Friday'}, {'record_number': 280, 'date': '2025-12-27', 'day': 'Friday'}, {'record_number': 281, 'date': '2025-12-27', 'day': 'Friday'}, {'record_number': 282, 'date': '2025-12-27', 'day': 'Friday'}]`.
Largest Min Delay examples: `[{'_id': '2812', 'Date': '2026-05-20', 'Line': 'EC', 'Time': '09:38', 'Day': 'Wednesday', 'Station': 'LEASIDE STATION', 'Code': 'PXOV', 'Min Delay': '971', 'Min Gap': '981', 'Bound': 'W', 'Vehicle': '6208'}, {'_id': '632', 'Date': '2026-01-25', 'Line': 'FW', 'Time': '15:17', 'Day': 'Sunday', 'Station': 'HUMBER COLLEGE TO FINC', 'Code': 'MXWEA', 'Min Delay': '449', 'Min Gap': '456', 'Bound': '', 'Vehicle': '0'}, {'_id': '1768', 'Date': '2026-03-20', 'Line': 'EC', 'Time': '16:45', 'Day': 'Friday', 'Station': 'WYNFORD STOP', 'Code': 'PXOV', 'Min Delay': '406', 'Min Gap': '412', 'Bound': 'E', 'Vehicle': '6233'}]`.
Duplicate examples excluding _id: `[{'values': {'Date': '2026-06-30', 'Line': 'FW', 'Time': '08:04', 'Day': 'Tuesday', 'Station': 'FINCH WEST FWLRT STATI', 'Code': 'PXDCS', 'Min Delay': '7', 'Min Gap': '14', 'Bound': 'W', 'Vehicle': '6000'}, 'count': 5}, {'values': {'Date': '2026-07-22', 'Line': 'EC', 'Time': '20:59', 'Day': 'Wednesday', 'Station': 'HAKIMI LEBOVIC STOP', 'Code': 'MXPAA', 'Min Delay': '0', 'Min Gap': '0', 'Bound': 'E', 'Vehicle': '6265'}, 'count': 2}]`.
Station and Line frequencies in JSON preserve exact labels; these fields must not be assumed to contain only stations or single standardized routes. Codes require official mode-specific definitions.

## Implications and unresolved questions

- Preserve source strings, file hash, resource identity and record position. Parse dates, times and durations explicitly; timezone/service-day meaning remains unverified.
- Keep blank direction values and zero vehicle/duration values distinct from missing records. Review station/line labels and unusual durations before setting cleaning rules.
- Do not deduplicate using _id or a guessed incident key. Investigate duplicate examples and whether IDs persist across replacement exports.
- Verify code meanings, Min Delay/Min Gap definitions, direction/line conventions, station naming and recording rules against official documentation before interpretation. No lookup or other resource was downloaded.
- Establish publication lag and completeness separately from observed date range; compare future approved snapshots to investigate revisions. This single download establishes no append-only update behavior.
- Shared column names do not prove cross-mode compatibility. No database, pipeline, analytical SQL, dashboard or update automation was implemented.

## Reproduce

`python3 scripts/profile_subway_tracer.py data/provenance/20261021T190550293696Z__lrt.json`

Outputs use exclusive creation and refuse to overwrite an existing report. Preserve or deliberately relocate previous reports before rerunning. Acquisition is a separate network command (`python3 scripts/acquire_subway_tracer.py --mode lrt`); each successful acquisition creates a new timestamped snapshot.

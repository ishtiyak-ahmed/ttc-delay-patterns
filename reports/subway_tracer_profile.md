# Subway tracer inspection

Inspection date: 2026-10-21

## Acquisition and method

Source: `ttc-subway-delay-data`, resource `0b6e5c52-e993-46d6-8d74-8602ee224457`. URL resolved from the unchanged local manifest. Only the approved Subway CSV was downloaded.

HTTP 200; 3,069,485 bytes; SHA-256 `ec7c36eeb4785e34d58229e5da6af741c89dfdf9fa59c58a63abe5b026b95c44`. Raw snapshot: `data/raw/subway/20261021T190204614685Z__0b6e5c52-e993-46d6-8d74-8602ee224457.csv`. Provenance: `data/provenance/20261021T190204614685Z__subway.json`.

Python `/Library/Frameworks/Python.framework/Versions/3.11/bin/python3` (3.11.9); installed certifi CA bundle `/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages/certifi/cacert.pem`; `CERT_REQUIRED` and hostname verification enabled. No dependencies installed. HTTP Content-Length matched the saved size. HTTP Last-Modified: `Mon, 21 Sep 2026 12:50:37 GMT`. Full headers and CA-bundle hash are in provenance.

Profiling uses the Python standard library, strict CSV parsing and UTF-8 decoding. Raw bytes are verified against provenance before and after profiling. No source rows are altered, removed, or ingested. Blank means empty or whitespace-only; literal null-like tokens are counted separately, not converted. Types below are observations, not source definitions.

## Schema and missingness

| Exact column | Apparent type | Blank | Distinct (including blank) | Numeric failures |
|---|---|---:|---:|---:|
| `_id` | integer-looking numeric text | 0 | 45475 | 0 |
| `Date` | date text (YYYY-MM-DD) | 0 | 608 | — |
| `Time` | time text (HH:MM; no timezone) | 0 | 1437 | — |
| `Day` | text | 0 | 7 | — |
| `Station` | text | 0 | 1251 | — |
| `Code` | text | 0 | 140 | — |
| `Min Delay` | integer-looking numeric text | 0 | 135 | 0 |
| `Min Gap` | integer-looking numeric text | 0 | 133 | 0 |
| `Bound` | text | 15860 | 6 | — |
| `Line` | text | 177 | 38 | — |
| `Vehicle` | integer-looking numeric text | 0 | 882 | 0 |

Records: **45,475**; malformed-width rows: 0. Date failures: 0; time failures: 0; weekday mismatches: 63.
Literal null-like tokens: `{}`. Values with surrounding whitespace: `{}`.

## Observed coverage

Parsed dates: **2025-01-01 through 2026-08-31**; 608 distinct incident dates. Dates before 2025: 0; dates after retrieval: 0. Dates without records between endpoints: 0 (listed in JSON).

The 45,475 CSV records match the snapshot's 45,475 datastore record_count. Count agreement does not prove identical contents, complete reporting, or absence of revisions. Missing dates or periods do not establish zero-delay service. No records beyond the maximum date can be inferred from the filename or monthly refresh label.

| Month | Recorded rows |
|---|---:|
| 2025-01 | 2106 |
| 2025-02 | 2274 |
| 2025-03 | 1986 |
| 2025-04 | 2117 |
| 2025-05 | 2175 |
| 2025-06 | 1941 |
| 2025-07 | 2122 |
| 2025-08 | 2719 |
| 2025-09 | 1813 |
| 2025-10 | 2027 |
| 2025-11 | 2215 |
| 2025-12 | 2242 |
| 2026-01 | 2481 |
| 2026-02 | 2048 |
| 2026-03 | 2400 |
| 2026-04 | 2719 |
| 2026-05 | 2633 |
| 2026-06 | 2638 |
| 2026-07 | 2513 |
| 2026-08 | 2306 |

## Recorded durations

Thresholds above 60, 120 and 1,440 minutes are descriptive review flags, not validated error rules. Percentiles use nearest rank. Min Gap is profiled separately; it is not added to Min Delay.

| Field | Zero | Negative | Min | Median | P95 | P99 | Max | >60 | >120 | >1440 | Sum |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Min Delay | 29669 | 0 | 0 | 0 | 10 | 26 | 900 | 110 | 41 | 0 | 122071 |
| Min Gap | 30403 | 0 | 0 | 0 | 14 | 28 | 906 | 103 | 38 | 0 | 169074 |

Recorded row count (45,475) and the sum of Min Delay (122071 recorded minutes) are different measures. Zero-minute rows remain records. These are uncleaned source totals, not passenger impact or normalized reliability measures.
Min Gap is less than Min Delay in 744 rows; the fields' intended relationship requires documentation. The JSON includes the five largest rows for each duration field.

## Duplicate candidates and identifiers

| Definition | Repeated groups | Rows in groups | Excess beyond first |
|---|---:|---:|---:|
| All 11 columns | 0 | 0 | 0 |
| All columns except _id | 66 | 132 | 66 |
| Date, Time, Station, Code, Bound, Line | 76 | 152 | 76 |
| Date, Time, Station, Line | 165 | 330 | 165 |

_id summary: `{'minimum': '1', 'maximum': '45475', 'distinct': 45475, 'duplicate_excess': 0, 'sequential_in_file': True}`. Export ID uniqueness does not establish stable incident identity across refreshes. Candidate keys are hypotheses, not documented unique keys; repeated groups may contain legitimate concurrent or repeated incidents. Nothing was deleted. JSON includes examples.

## Codes and categories

Observed codes: 140; stations: 1251; vehicle values: 882. Full exact value frequencies for Code, Day, Station, Bound, Line and Vehicle are in the JSON; no codes were translated into causes.

Day frequencies: `{'Friday': 6980, 'Monday': 6796, 'Saturday': 5812, 'Sunday': 5123, 'Thursday': 7080, 'Tuesday': 6731, 'Wednesday': 6953}`.
Bound frequencies: `{'': 15860, 'B': 62, 'E': 7516, 'N': 6940, 'S': 7989, 'W': 7108}`.
Line frequencies: `{'': 177, '116 MORNINGSIDE': 1, '29 DUFFERIN': 1, '47 LANSDOWNE': 1, '50 BURNHAMTHORPE': 1, '504 KING': 1, '506 CARLTON': 1, '508 LAKESHORE': 1, '60 STEELES WEST': 1, '62 MORTIMER': 1, '76 ROYAL YORK SOUTH': 1, '95 YORK MILLS': 1, '999': 1, 'BD': 19758, 'BD/YU': 7, 'BD/YUS': 5, 'BD/YUS/SHP/FWLRT/ECLRT': 1, 'EC': 2, 'LINE 1': 1, 'LINE 2 - BLOOR DANFORT': 1, 'LINE 2 BLOOR-DANFORTH': 1, 'SHP': 1772, 'SRT': 5, 'TRANSIT CONTROL': 1, 'WOODBINE STN': 1, 'YU': 23134, 'YU -BD LINES': 1, 'YU / BD': 2, 'YU/ BD': 4, 'YU/BD': 470, 'YU/BD LINES': 2, 'YU/BD/SHP': 11, 'YUS': 13, 'YUS / BD': 2, 'YUS/ BD': 3, 'YUS/ BD/ SHP': 1, 'YUS/BD': 87, 'YUS/BD/SHP': 1}`.
Vehicle `0` occurs 18008 times; whether it means unknown, not applicable, or an actual identifier is unresolved. Vehicle identifiers should be retained as source text pending definition checks.

Most frequent codes: `SUDP` (5171), `MUIS` (4263), `SUO` (3279), `MUPAA` (2405), `PUOPO` (2341), `MUIRS` (2049), `MUIR` (1574), `MUSC` (1457), `MUO` (1437), `PUMEL` (1407), `TUNCA` (1205), `SUL` (1132), `SUAP` (1019), `MUNCA` (963), `SUUT` (950).

## Specific anomalies requiring review

- `_id` 34928 records `2026-04-26` with Day `Saturday`; that calendar date is Sunday. This is one of 63 date/weekday conflicts. Preserve both fields until their intended meaning is verified.
- `Line` includes `SRT` (5 rows), `999` (1), `WOODBINE STN` (1), and labels such as `504 KING` (1). Combined labels also vary (`YU/BD`, `YU / BD`, `YUS/BD`). Do not infer mode or normalize these values without reviewing context.
- The largest Min Delay is 900 minutes at SHEPPARD WEST STATION on 2025-02-16 at 11:03 (`_id` 3321, code `MUWEA`, Min Gap 906). These values are retained and flagged for semantic review, not declared invalid.
- One duplicate pair excluding `_id` records 2025-02-28 20:21, KENNEDY BD STATION, code `MUSC`, Min Delay/Gap 0, Bound `W`, Line `BD`, Vehicle `5290`. All duplicate candidates remain in the raw total.
- As retrieved on 2026-10-21, this file stops on 2026-08-31. September and October records are absent from this snapshot; whether that reflects publication lag, a stale export, or another limitation remains unknown.

## Implications and unresolved questions

- Preserve source strings, file hash, resource identity and record position. Parse dates, times and durations explicitly; timezone/service-day meaning remains unverified.
- Keep blank direction values and zero vehicle/duration values distinct from missing records. Review station/line labels and unusual durations before setting cleaning rules.
- Do not deduplicate using _id or a guessed incident key. Investigate duplicate examples and whether IDs persist across replacement exports.
- Verify code meanings, Min Delay/Min Gap definitions, direction/line conventions, station naming and recording rules against official documentation before interpretation. No lookup or other resource was downloaded.
- Establish publication lag and completeness separately from observed date range; compare future approved snapshots to investigate revisions. This single download establishes no append-only update behavior.
- Cross-mode compatibility remains unknown. No database, pipeline, analytical SQL, dashboard or update automation was implemented.

## Reproduce

`python3 scripts/profile_subway_tracer.py data/provenance/20261021T190204614685Z__subway.json`

Outputs use exclusive creation and refuse to overwrite an existing report. Preserve or deliberately relocate previous reports before rerunning. Acquisition is a separate network command (`python3 scripts/acquire_subway_tracer.py`); each successful acquisition creates a new timestamped snapshot.

# Streetcar tracer inspection

Inspection date: 2026-10-21

## Acquisition and method

Source: `ttc-streetcar-delay-data`, resource `cf2fdd12-6f0e-4644-aae7-0bbfc31df031`. URL resolved from the unchanged local manifest. Only the selected CSV was downloaded by this acquisition command.

HTTP 200; 1,882,886 bytes; SHA-256 `c6c081880619ffff8779c61af3a0b77466471473a014d8dec48d16306ddf9606`. Raw snapshot: `data/raw/streetcar/20261021T190549738480Z__cf2fdd12-6f0e-4644-aae7-0bbfc31df031.csv`. Provenance: `data/provenance/20261021T190549738480Z__streetcar.json`.

Python `/Library/Frameworks/Python.framework/Versions/3.11/bin/python3` (3.11.9); installed certifi CA bundle `/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages/certifi/cacert.pem`; `CERT_REQUIRED` and hostname verification enabled. No dependencies installed. HTTP Content-Length matched the saved size. HTTP Last-Modified: `Mon, 21 Sep 2026 12:39:56 GMT`. Full headers and CA-bundle hash are in provenance.

Profiling uses the Python standard library, strict CSV parsing and UTF-8 decoding. Raw bytes are verified against provenance before and after profiling. No source rows are altered, removed, or ingested. Blank means empty or whitespace-only; literal null-like tokens are counted separately, not converted. Types below are observations, not source definitions.

## Schema and missingness

| Exact column | Apparent type | Blank | Distinct (including blank) | Numeric failures |
|---|---|---:|---:|---:|
| `_id` | integer-looking numeric text | 0 | 23703 | 0 |
| `Date` | date text (YYYY-MM-DD) | 0 | 608 | — |
| `Line` | text | 352 | 198 | — |
| `Time` | time text (HH:MM; no timezone) | 0 | 1440 | — |
| `Day` | text | 0 | 7 | — |
| `Station` | text | 0 | 3130 | — |
| `Code` | text | 1 | 149 | — |
| `Min Delay` | integer-looking numeric text | 0 | 297 | 0 |
| `Min Gap` | integer-looking numeric text | 0 | 316 | 0 |
| `Bound` | text | 5327 | 7 | — |
| `Vehicle` | integer-looking numeric text | 0 | 1179 | 0 |

Records: **23,703**; malformed-width rows: 0. Date failures: 0; time failures: 0; weekday mismatches: 42.
Literal null-like tokens: `{}`. Values with surrounding whitespace: `{}`.

## Observed coverage

Parsed dates: **2025-01-01 through 2026-08-31**; 608 distinct incident dates. Dates before 2025: 0; dates after retrieval: 0. Dates without records between endpoints: 0 (listed in JSON).

The 23,703 CSV records match the snapshot's 23,703 datastore record_count. Count agreement does not prove identical contents, complete reporting, or absence of revisions. Missing dates or periods do not establish zero-delay service. No records beyond the maximum date can be inferred from the filename or monthly refresh label.

| Month | Recorded rows |
|---|---:|
| 2025-01 | 1037 |
| 2025-02 | 1920 |
| 2025-03 | 1120 |
| 2025-04 | 1170 |
| 2025-05 | 1228 |
| 2025-06 | 1279 |
| 2025-07 | 1146 |
| 2025-08 | 1224 |
| 2025-09 | 897 |
| 2025-10 | 1111 |
| 2025-11 | 1122 |
| 2025-12 | 1191 |
| 2026-01 | 1366 |
| 2026-02 | 1109 |
| 2026-03 | 1229 |
| 2026-04 | 1296 |
| 2026-05 | 1295 |
| 2026-06 | 972 |
| 2026-07 | 944 |
| 2026-08 | 1047 |

## Recorded durations

Thresholds above 60, 120 and 1,440 minutes are descriptive review flags, not validated error rules. Percentiles use nearest rank. Min Gap is profiled separately; it is not added to Min Delay.

| Field | Zero | Negative | Min | Median | P95 | P99 | Max | >60 | >120 | >1440 | Sum |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Min Delay | 5279 | 0 | 0 | 10 | 61 | 154 | 999 | 1188 | 365 | 0 | 416513 |
| Min Gap | 5359 | 0 | 0 | 20 | 70 | 161 | 999 | 1547 | 415 | 0 | 590287 |

Recorded row count (23,703) and the sum of Min Delay (416513 recorded minutes) are different measures. Zero-minute rows remain records. These are uncleaned source totals, not passenger impact or normalized reliability measures.
Min Gap is less than Min Delay in 256 rows; the fields' intended relationship requires documentation. The JSON includes the five largest rows for each duration field.

## Duplicate candidates and identifiers

| Definition | Repeated groups | Rows in groups | Excess beyond first |
|---|---:|---:|---:|
| All 11 columns | 0 | 0 | 0 |
| All columns except _id | 18 | 36 | 18 |
| Date, Time, Station, Code, Bound, Line | 31 | 73 | 42 |
| Date, Time, Station, Line | 73 | 158 | 85 |

_id summary: `{'minimum': '1', 'maximum': '23703', 'distinct': 23703, 'duplicate_excess': 0, 'sequential_in_file': True}`. Export ID uniqueness does not establish stable incident identity across refreshes. Candidate keys are hypotheses, not documented unique keys; repeated groups may contain legitimate concurrent or repeated incidents. Nothing was deleted. JSON includes examples.

## Codes and categories

Distinct Code values (including blank): 149; stations: 3130; vehicle values: 1179. Full exact value frequencies for Code, Day, Station, Bound, Line and Vehicle are in the JSON; no codes were translated into causes.

Day frequencies: `{'Friday': 3521, 'Monday': 3315, 'Saturday': 3774, 'Sunday': 3417, 'Thursday': 3270, 'Tuesday': 3183, 'Wednesday': 3223}`.
Bound frequencies: `{'': 5327, '8': 1, 'B': 16, 'E': 6785, 'N': 2339, 'S': 2361, 'W': 6874}`.
Line frequencies: `{'': 352, '114': 1, '129 MCCOWAN NORTH': 1, '131 NUGGET': 1, '25': 1, '26': 1, '301 OVERHEAD CREW': 2, '301 QUEEN': 7, '301 QUEEN NIGHT': 258, '303': 1, '303 KINGSTOM': 1, '303 KINGSTON RD': 5, '303 KINGSTON ROAD': 9, '303 KINGSTON ROAD NIGH': 27, '303 OVERHEAD': 1, '304 KING': 5, '304 KING NIGHT': 145, '305': 4, '305 DUNDAS': 32, '305 DUNDAS NIGHT': 136, '305 NIGHT CAR': 1, '306 CARLTON': 8, '306 CARLTON NIGHT': 167, '309 HARBOURFRONT': 2, '310 SPADINA': 4, '310 SPADINA NIGHT': 55, '311': 2, '311 BATHURST': 2, '312 ST. CLAIR NIGHT': 30, '335 JANE': 1, '39 FINCH EAST': 1, '4404': 1, '500': 70, '500 (512 ST CLAIR)': 1, '500 - RAD': 1, '500 RAD': 1, '5003': 1, '501 (RAD)': 1, '501 LAKESHORE': 1, '501 QUEEN': 3992, '501 QUEEN (600)': 1, '501 QUEEN - RAD': 1, '501 QUEEN - RAD VEHICL': 1, '502 DOWNTOWNER': 1, '503': 3, '503 KINGSOTN ROAD': 1, '503 KINGSTON RD': 1, '503 KINGSTON ROAD': 1814, '503 KINGSTON ROAD - BU': 1, '503 LONG BRANCH': 1, '504': 4, '504 AKING': 1, '504 KING': 4102, '504 KING (A-BRANCH)': 2, '504 KING (B-BRANCH)': 1, '504 KING (PRIVATE)': 1, '504 KING - B BRANCH': 1, '504 KING - SHUTTLE BUS': 1, '504 KING RAD CAR': 1, '504 KING SHUTTLE': 1, '504 KING SHUTTLE BUS': 1, '504 KING- 600': 1, '5047': 1, '504A KING': 4, '504B KING': 6, '504C KING': 1, '504D KING': 2, '504D/C KING': 1, '505': 3, '505 DUNDAS': 3230, '505 DUNDAS  (RAD BUS)': 1, '505 DUNDAS (NO RUN - R': 1, '505 DUNDAS (RAD)': 2, '505 RAD STREETCAR': 1, '506': 2, '506 CARLTON': 2950, '506 CARLTON  (RAD)': 1, '506 CARLTON (600)': 1, '506 CARLTON (RAD)': 2, '506 CARLTON - 600 RAD': 1, '506 CARLTON - RAD': 1, '506 CARLTON - RAD BUS': 1, '506 CARLTON RAD': 1, '506RAD': 1, '507 LONG BRANCH': 805, '507 LONG BRANCH (600 R': 2, '507 LONG BRANCH (OTC)': 1, '507 LONG BRANCH - 500': 1, '507 LONG BRANCH EXTRA': 1, '507 SHUTTLE': 1, '508 KING': 1, '508 LAKESHORE': 103, '508 LAKESHORE (600 SER': 1, '509 HARBOUR FRONT': 1, '509 HARBOURFRONT': 616, '509 HARBOURFRONT (RAD': 1, '509 HARBOURFRONT (RAD)': 1, '509 HARBOURFRONT (RADI': 1, '510': 5, '510 SPADINA': 1761, '510 SPADINA (RUN-IN-RA': 1, '510 SPADINA -': 1, '511': 2, '511 BATHURST': 1036, '511 BATHURST (600 RAD)': 1, '511 BATHURST (600 SERI': 1, '511 BATHURST (600)': 1, '5111': 1, '512': 2, '512 ST CLAIR': 7, '512 ST. CLAIR': 1616, '512 ST. CLAIR ( RAD)': 1, '512 ST. CLAIR (RAD BUS': 1, '512`': 1, '514 CHERRY': 1, '54': 1, '555': 12, '555 (505 DUNDAS)': 1, '555 (507 RAD)': 1, '600': 23, '600 (506 CARLTON)': 1, '600 (509 HARBOURFRONT)': 1, '600 (510 SPADINA)': 1, '600 (511 BATHURST)': 1, '600 (OPERATING AS 503': 1, '600 (RAD)': 1, '600 - 506 CARLTON': 1, '600 - QUEENSWAY GARAGE': 1, '600 - RAD': 1, '600 - STORM CAR': 1, '600 RAD': 13, '600 RAD (510 SPADINA)': 1, '600 RAD (512 ROUTE)': 1, '600 RAD 504': 1, '600 RAD 512': 1, '600 RAD ON 512 ST CLAI': 1, '600 RAD VEHICLE': 1, '600 SERIES (506 CARLTO': 1, '600 SHUTTLE': 1, '600 STORM CAR': 1, '600(506)': 1, '600(512 ST CLAIR)': 1, '600- 507 ROUTE': 1, '600/506 CARLTON': 1, '600RAD': 1, '600RAD, 504': 1, '69': 1, '7 BATHURST': 1, '705': 21, '705 LONG BRANCH': 1, '705 RAD': 12, '706': 1, '72652': 1, '75 SHERBOURNE': 1, '831 STREETCAR WAY': 1, '899': 1, '899 TRAINING ROUTE': 1, '900': 1, '929 DUFFERIN EXPRESS': 1, '939 FINCH EXPRESS': 1, '96 WILSON': 1, '999': 54, '999 (505 DUNDAS)': 1, 'A410': 1, 'BD': 3, 'CARHOUSE': 1, 'CHO': 1, 'CNE EXTRA': 2, 'CSR B#T010165': 1, 'EXHIBITION LOOP': 1, 'EXTRA': 1, 'EXTRA CAR': 1, 'FLEET TRUCK': 1, 'FLEET VEHICLE - A': 1, 'OTC': 4, 'OTC - 501 QUEEN': 1, 'OTC CAR': 2, 'OVERHEAD': 1, 'RAD': 20, 'RAD (510 SPADINA)': 1, 'RAD - #507': 1, 'RAD - 504 KING': 1, 'RAD - 506 CARLTON': 1, 'RAD 600': 1, 'RAD CAR - DOING #501': 1, 'RAD CAR ON #501': 1, 'RUN IN': 1, 'RUN IN CAR': 1, 'S': 1, 'STORM CAR': 2, 'STORM CAR - 505': 1, 'STORM STREETCAR': 1, 'TEST CAR': 1, 'TRACK 11': 1, 'TRACK 2 - SWITCH 130': 1, 'TRACK 7E': 1, 'TRAINING VEHICLE': 1, 'YU': 2}`.
Vehicle `0` occurs 1467 times; whether it means unknown, not applicable, or an actual identifier is unresolved. Vehicle identifiers should be retained as source text pending definition checks.

Most frequent codes: `MTDV` (2449), `MTSAN` (2320), `STDP` (1981), `MTAFR` (1403), `MTUI` (1290), `MTGD` (1233), `STO` (1165), `MTUIR` (932), `MTNOA` (764), `MTO` (685), `TTPD` (683), `TTO` (605), `MTUS` (575), `TTUS` (454), `EFO` (420).

## Additional source observations

Exact column order: `['_id', 'Date', 'Line', 'Time', 'Day', 'Station', 'Code', 'Min Delay', 'Min Gap', 'Bound', 'Vehicle']`. Same names as Subway; different order.
Date suffix frequencies: `{'': 23703}`. Bus timestamp dates are parsed explicitly; any non-midnight components remain in the source and are not silently removed.
Date/weekday mismatch examples: `[{'record_number': 19240, 'date': '2026-04-26', 'day': 'Saturday'}, {'record_number': 19241, 'date': '2026-04-26', 'day': 'Saturday'}, {'record_number': 19242, 'date': '2026-04-26', 'day': 'Saturday'}, {'record_number': 19243, 'date': '2026-04-26', 'day': 'Saturday'}, {'record_number': 19244, 'date': '2026-04-26', 'day': 'Saturday'}]`.
Largest Min Delay examples: `[{'_id': '17282', 'Date': '2026-03-10', 'Line': '504 KING', 'Time': '08:18', 'Day': 'Tuesday', 'Station': 'KING AND BERKELEY', 'Code': 'MFDV', 'Min Delay': '999', 'Min Gap': '999', 'Bound': '', 'Vehicle': '8777'}, {'_id': '16818', 'Date': '2026-02-26', 'Line': '503 KINGSTON ROAD', 'Time': '22:57', 'Day': 'Thursday', 'Station': 'BROADVIEW AND DUNDAS', 'Code': 'MFDV', 'Min Delay': '922', 'Min Gap': '932', 'Bound': 'W', 'Vehicle': '8794'}, {'_id': '2709', 'Date': '2025-02-24', 'Line': '504 KING', 'Time': '06:34', 'Day': 'Monday', 'Station': 'RONCESVALLES AND HOWAR', 'Code': 'MTAFR', 'Min Delay': '840', 'Min Gap': '850', 'Bound': 'S', 'Vehicle': '4445'}]`.
Duplicate examples excluding _id: `[{'values': {'Date': '2025-01-13', 'Line': '500', 'Time': '06:00', 'Day': 'Monday', 'Station': 'TORONTO TRANSIT COMMIS', 'Code': 'MTO', 'Min Delay': '0', 'Min Gap': '0', 'Bound': '', 'Vehicle': '0'}, 'count': 2}, {'values': {'Date': '2025-02-18', 'Line': '504 KING', 'Time': '19:29', 'Day': 'Tuesday', 'Station': 'KING AND PARLIAMENT', 'Code': 'MTNOA', 'Min Delay': '10', 'Min Gap': '18', 'Bound': 'E', 'Vehicle': '4465'}, 'count': 2}]`.
Station and Line frequencies in JSON preserve exact labels; these fields must not be assumed to contain only stations or single standardized routes. Codes require official mode-specific definitions.

## Implications and unresolved questions

- Preserve source strings, file hash, resource identity and record position. Parse dates, times and durations explicitly; timezone/service-day meaning remains unverified.
- Keep blank direction values and zero vehicle/duration values distinct from missing records. Review station/line labels and unusual durations before setting cleaning rules.
- Do not deduplicate using _id or a guessed incident key. Investigate duplicate examples and whether IDs persist across replacement exports.
- Verify code meanings, Min Delay/Min Gap definitions, direction/line conventions, station naming and recording rules against official documentation before interpretation. No lookup or other resource was downloaded.
- Establish publication lag and completeness separately from observed date range; compare future approved snapshots to investigate revisions. This single download establishes no append-only update behavior.
- Shared column names do not prove cross-mode compatibility. No database, pipeline, analytical SQL, dashboard or update automation was implemented.

## Reproduce

`python3 scripts/profile_subway_tracer.py data/provenance/20261021T190549738480Z__streetcar.json`

Outputs use exclusive creation and refuse to overwrite an existing report. Preserve or deliberately relocate previous reports before rerunning. Acquisition is a separate network command (`python3 scripts/acquire_subway_tracer.py --mode streetcar`); each successful acquisition creates a new timestamped snapshot.

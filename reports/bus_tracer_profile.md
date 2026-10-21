# Bus tracer inspection

Inspection date: 2026-10-21

## Acquisition and method

Source: `ttc-bus-delay-data`, resource `b5725365-9252-4bfe-b6f4-cda7ddf74341`. URL resolved from the unchanged local manifest. Only the selected CSV was downloaded by this acquisition command.

HTTP 200; 9,492,730 bytes; SHA-256 `1474f16414e63aaeab58714c236446ea370f5e00e072a3b97fdfeb1f079cd8fe`. Raw snapshot: `data/raw/bus/20261021T190548363172Z__b5725365-9252-4bfe-b6f4-cda7ddf74341.csv`. Provenance: `data/provenance/20261021T190548363172Z__bus.json`.

Python `/Library/Frameworks/Python.framework/Versions/3.11/bin/python3` (3.11.9); installed certifi CA bundle `/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages/certifi/cacert.pem`; `CERT_REQUIRED` and hostname verification enabled. No dependencies installed. HTTP Content-Length matched the saved size. HTTP Last-Modified: `Mon, 21 Sep 2026 12:32:38 GMT`. Full headers and CA-bundle hash are in provenance.

Profiling uses the Python standard library, strict CSV parsing and UTF-8 decoding. Raw bytes are verified against provenance before and after profiling. No source rows are altered, removed, or ingested. Blank means empty or whitespace-only; literal null-like tokens are counted separately, not converted. Types below are observations, not source definitions.

## Schema and missingness

| Exact column | Apparent type | Blank | Distinct (including blank) | Numeric failures |
|---|---|---:|---:|---:|
| `_id` | integer-looking numeric text | 0 | 102257 | 0 |
| `Date` | timestamp text (YYYY-MM-DDTHH:MM:SS; no timezone) | 0 | 608 | — |
| `Line` | text | 1241 | 664 | — |
| `Time` | time text (HH:MM; no timezone) | 0 | 1440 | — |
| `Day` | text | 0 | 7 | — |
| `Station` | text | 0 | 16396 | — |
| `Code` | text | 0 | 75 | — |
| `Min Delay` | integer-looking numeric text | 0 | 678 | 0 |
| `Min Gap` | integer-looking numeric text | 0 | 706 | 0 |
| `Bound` | text | 21327 | 18 | — |
| `Vehicle` | integer-looking numeric text | 0 | 2767 | 0 |

Records: **102,257**; malformed-width rows: 0. Date failures: 0; time failures: 0; weekday mismatches: 130.
Literal null-like tokens: `{}`. Values with surrounding whitespace: `{}`.

## Observed coverage

Parsed dates: **2025-01-01 through 2026-08-31**; 608 distinct incident dates. Dates before 2025: 0; dates after retrieval: 0. Dates without records between endpoints: 0 (listed in JSON).

The 102,257 CSV records match the snapshot's 102,257 datastore record_count. Count agreement does not prove identical contents, complete reporting, or absence of revisions. Missing dates or periods do not establish zero-delay service. No records beyond the maximum date can be inferred from the filename or monthly refresh label.

| Month | Recorded rows |
|---|---:|
| 2025-01 | 3908 |
| 2025-02 | 5583 |
| 2025-03 | 4703 |
| 2025-04 | 4764 |
| 2025-05 | 5291 |
| 2025-06 | 5803 |
| 2025-07 | 5318 |
| 2025-08 | 5515 |
| 2025-09 | 5406 |
| 2025-10 | 5325 |
| 2025-11 | 5630 |
| 2025-12 | 5783 |
| 2026-01 | 6008 |
| 2026-02 | 4824 |
| 2026-03 | 5319 |
| 2026-04 | 4965 |
| 2026-05 | 4893 |
| 2026-06 | 4525 |
| 2026-07 | 4338 |
| 2026-08 | 4356 |

## Recorded durations

Thresholds above 60, 120 and 1,440 minutes are descriptive review flags, not validated error rules. Percentiles use nearest rank. Min Gap is profiled separately; it is not added to Min Delay.

| Field | Zero | Negative | Min | Median | P95 | P99 | Max | >60 | >120 | >1440 | Sum |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Min Delay | 12974 | 0 | 0 | 12 | 48 | 247 | 999 | 4209 | 2220 | 0 | 2163102 |
| Min Gap | 13216 | 0 | 0 | 22 | 70 | 266 | 997 | 5783 | 2682 | 0 | 3417331 |

Recorded row count (102,257) and the sum of Min Delay (2163102 recorded minutes) are different measures. Zero-minute rows remain records. These are uncleaned source totals, not passenger impact or normalized reliability measures.
Min Gap is less than Min Delay in 758 rows; the fields' intended relationship requires documentation. The JSON includes the five largest rows for each duration field.

## Duplicate candidates and identifiers

| Definition | Repeated groups | Rows in groups | Excess beyond first |
|---|---:|---:|---:|
| All 11 columns | 0 | 0 | 0 |
| All columns except _id | 297 | 595 | 298 |
| Date, Time, Station, Code, Bound, Line | 334 | 670 | 336 |
| Date, Time, Station, Line | 550 | 1105 | 555 |

_id summary: `{'minimum': '1', 'maximum': '102257', 'distinct': 102257, 'duplicate_excess': 0, 'sequential_in_file': True}`. Export ID uniqueness does not establish stable incident identity across refreshes. Candidate keys are hypotheses, not documented unique keys; repeated groups may contain legitimate concurrent or repeated incidents. Nothing was deleted. JSON includes examples.

## Codes and categories

Distinct Code values (including blank): 75; stations: 16396; vehicle values: 2767. Full exact value frequencies for Code, Day, Station, Bound, Line and Vehicle are in the JSON; no codes were translated into causes.

Day frequencies: `{'Friday': 16288, 'Monday': 13804, 'Saturday': 13608, 'Sunday': 10699, 'Thursday': 16268, 'Tuesday': 15547, 'Wednesday': 16043}`.
Bound frequencies: `{'': 21327, '2': 1, '3': 1, '4': 2, '7': 1, '8': 2, 'A': 2, 'B': 33, 'D': 4, 'E': 18729, 'G': 1, 'M': 6, 'N': 22742, 'Q': 1, 'S': 21881, 'W': 17522, 'Z': 1, '`': 1}`.
Line frequencies: `{'': 1241, '08': 1, '09 BELLAMY': 1, '1 LINE SHUTTLE': 3, '1 SHUTTLE': 5, '1 SHUTTLE BUS': 1, '10 VAN HORNE': 27, '100': 3, '100 FLEMINGDON PARK': 1063, '100 FLEMINGDON PARK (6': 2, '100 FLEMINGTON PARK': 1, '101 DOWNSVIEW PARK': 211, '101 DOWNSVIEW PARK / 1': 1, '102': 1, '102 MARKHAM RD': 1, '102 MARKHAM ROAD': 1982, '102 MARKHAM ROAD (D-BR': 1, '102 MARKHAM ROAD (RAD': 1, '102D MARKHAM ROAD': 3, '103 MT. PLEASANT NORTH': 47, '104 FAYWOOD': 232, '105 DUFFERIN NORTH': 203, '106 SENTIAL': 1, '106 SENTINEL': 275, '107 ALLNESS-CHESSWOOD': 24, '107 YORK UNIVERSITY HE': 148, '108 DRIFTWOOD': 558, '109 RANEE': 304, '109 RANEE - B BRANCH': 1, '11 BAYVIEW': 581, '110': 1, '110 ISLINGTON SOUTH': 580, '111': 1, '111 EAST MALL': 369, '112 WEST MALL': 608, '112 WEST MALL (300 BLO': 1, '113 DANFORTH': 327, '114': 1, '114 QUEENS QUAY EAST': 450, '115 SILVER HILLS': 31, '116': 1, '116 MORNINGSIDE': 1566, '117 ALNESS-CHESSWOOD': 10, '117 BIRCHMOUNT SOUTH': 50, '1174': 1, '118 THISTLE DOWN': 284, '119 TORBARRIE': 141, '12 KINGSTON ROAD': 730, '120 CALVINGTON': 168, '120 CALVINGTON ( RAD)': 1, '1202': 2, '121 ESPLANADE-RIVER': 342, '122 GRAYDON HALL': 400, '122 GRAYDON HALL DRIVE': 1, '123 SHERWAY': 686, '123 SHERWAY (RAD)': 1, '123 SHERWAY - F': 1, '123C SHERWAY': 1, '124': 1, '124 SUNNYBROOK': 235, '125 DREWRY': 193, '126 CHRISTIE': 175, '127 DAVENPORT': 224, '128 STANLEY GREENE': 42, '129 MCCOWAN NORTH': 867, '129 MCCOWAN NORTH (A-B': 1, '13 AVENUE ROAD': 259, '130 MIDDLEFIELD': 422, '130 NEILSON': 1, '131': 1, '131 NUGGET': 690, '132 MILNER': 106, '133': 1, '133 NEILSON': 1047, '134': 2, '134 PROGRESS': 440, '135 GERRARD': 166, '135 GERRRARD': 1, '14': 2, '14 GLENCAIRN': 316, '14 GLENCAIRN (28 BAYVI': 1, '14 GLENCAIRN / 28 BAYV': 1, '14 GLENCAIRN/ 28': 1, '147': 1, '149': 11, '149 - ETOBICOKE-BLOOR': 1, '149 ETOBICOKE': 1, '149 ETOBICOKE - BLOOR': 6, '149 ETOBICOKE BLOOR': 9, '149 ETOBICOKE- BLOOR': 1, '149 ETOBICOKE-BLOOR': 192, '15 EVANS': 156, '151 LESLIE NORTH': 46, '154 CURRAN HALL': 402, '154 CURRAN HALL (300 B': 1, '156': 6, '156 - MILLWOOD': 1, '156 MILLWOOD': 19, '158 THRETHEWEY': 1, '158 TRETHEWEY': 116, '16 MCCOWAN': 585, '160 BATHURST NORTH': 400, '160 BATHURST NORTH (RA': 1, '161 ROGERS ROAD': 550, '162': 1, '162 LAWRENCE-DONWAY': 234, '164 CASTELFIELD': 1, '164 CASTLEFIELD': 96, '165': 1, '165 WESTON ROAD NORTH': 1492, '166': 5, '166 TORYORK': 51, '167 PHARMACY NORTH': 128, '168': 1, '168 SYMINGTON': 489, '168/': 1, '169 HUNTINGWOOD': 270, '17 BIRCHMOUNT': 488, '171 MOUNT DENNIS': 1, '171 MT. DENNIS': 103, '18 CALEDONIA': 61, '184 ANCASTER PARK': 20, '185 SHEPPARD CENTRAL': 206, '189 STOCKYARDS': 56, '19 BAY': 335, '191 UNDERHILL': 74, '20 CLIFFSIDE': 403, '20 CLIFFSIDE (RAD)': 1, '200': 1, '200 TORONTO ZOO': 26, "201 BLUFFER'S PARK": 57, '202 CHERRY BEACH': 153, '203': 2, '203 - HIGH PARK': 1, '203 HIGH PARK': 4, '203 HIGH PARK SHUTTLE': 1, '21 BRIMLEY': 547, '22': 1, '22 COXWELL': 318, '23': 1, '23 DAWES': 307, '238': 1, '24 VICTORIA PARK': 1194, '24B VICTORIA PARK': 1, '25': 1, '25 DON MILLS': 1490, '25 DON MILLS (600)': 1, '26 DUPONT': 378, '27 JANE SOUTH': 186, '28 BAYVIEW': 1, '28 BAYVIEW SOUTH': 40, '29 DUFFERIN': 1907, '29 DUFFERIN / 929 DUFF': 1, '29 DUFFERIN EXPRESS': 1, '29C DUFFERIN': 5, '30 HIGH PARK': 20, '30 HIGH PARK NORTH': 150, '300': 1, '300 BLOOR - DANFORTH': 1, '300 BLOOR DANFORTH': 2, '300 BLOOR NIGHT': 1, '300 BLOOR-DANFORTH': 710, '301': 3, '301 OVERHEAD': 2, '301 QUEEN NIGHT': 2, '302 KINGSTON ROAD-MCCO': 30, '304': 1, '304 KING': 1, '305': 1, '305 DUNDAS': 1, '306 COLLEGE NIGHT': 1, '307 BATHURST': 114, '307 BATHURST NIGHT': 1, '307 BATHURST NIGHT BUS': 1, '31 GREENWOOD': 321, '312 ST CLAIR': 1, "315 EVANS-BROWN'S LINE": 7, '316': 5, '316 KINGSTON RD - MCCO': 2, '316 KINGSTON RD-MCCOWA': 1, '316 KINGSTON ROAD MCCO': 2, '32 (C) EGLINTON WEST': 1, '32 EGLINTON EAST': 1, '32 EGLINTON WEST': 2124, '32 EGLINTON WEST (RAD)': 1, '320 YONGE': 786, '320 YONGE (RAD)': 1, '322 COXWELL': 49, '324 STEELES': 1, '324 VICTORIA PARK': 26, '325 DON MILLS': 60, '329 DUFFERIN': 88, '32A EGLINTON WEST': 1, '32C EGLINTON WEST': 2, '33 FOREST HILL': 169, '332 EGLINTON WEST': 39, '334 EGLINTON EAST': 181, '335 JANE': 60, '336 FINCH WEST': 92, '337 EVANS': 1, '337 ISLINGTON': 31, '339 FINCH EAST': 69, '34 EGLINTON': 341, '34 EGLINTON - RAD': 1, '34 EGLINTON EAST': 930, '34 EGLINTON EAST - C B': 2, '340 JUNCTION': 18, '340 JUNCTION-DUNDAS WE': 1, '341 KEELE': 45, '343 KENNEDY': 36, '34C EGLINTON EAST': 1, '35 JANE': 1501, '35 JANE (A-BRANCH)': 1, '35 JANE (TRAINING BUS)': 1, '35 JANE - B BRANCH': 1, '352 LAWRENCE WEST': 62, '353 STEELES': 82, '353 STEELES EAST': 2, '354 LAWRENCE EAST': 49, '36 FINCH WEST': 1500, '363 OSSINGTON': 35, '365 PARLIAMENT': 9, '368': 1, '37 ISLINGTON': 1084, '37 ISLINGTON (A-BRANCH': 1, '37B ISLINGTON': 1, '38 HIGHLAND CREEK': 1051, '384 SHEPPARD WEST': 14, '385 SHEPPARD EAST': 46, '386': 8, '386 (RAD BUS)': 1, '386 NIGHT BUS': 1, '386 SCARBOROUGH': 10, '39 FINCH EAST': 1054, '39 FINCH EAST (RAD)': 1, '39 FINCH WEST': 1, '393': 1, '3935': 1, '395 YORK MILLS': 34, '396 WILSON': 57, '39B FINCH EAST': 3, '39C FINCH EAST': 1, '3X - 600': 1, '40 JUNCTION-DUNDAS WES': 535, '41': 2, '41 KEELE': 1231, '41 KEELE/941 KEELE EXP': 1, '42 CUMMER': 534, '42 CUMMER - 600 RAD': 1, '43 KENNEDY': 1139, '43 KENNEDY (320 YONGE': 1, '439': 1, '44 KIPLING SOUTH': 663, '444': 1, '45 KIPLING': 777, '45 KIPLING (B BRANCH)': 1, '46 MARTIN GROVE': 374, '47': 3, '47 LANSDOWNE': 1306, '47 LANSDOWNE (RAD BUS)': 1, '47 LANSDOWNE - A BRANC': 1, '48 RATHBURN': 120, '49 BLOOR WEST': 92, '50 BURNHAMTHORPE': 184, '50 BURNHAMTHORPE - RAD': 1, '500': 4, '500 (512 ST CLAIR)': 1, '501': 7, '501 QUEEN': 13, '501 REPLACEMENT': 1, '503': 21, '503 KINGSTON': 21, '503 KINGSTON RD': 3, '503 KINGSTON ROAD': 27, '504': 26, '504 KING': 32, '505': 5, '505 DUNDAS': 4, '506': 16, '506 CARLTON': 16, '506 RAD BUS': 1, '506 REPLACEMENT': 1, '506 SHUTTLE': 2, '506 SHUTTLE BUS': 1, '507': 10, '507 (600 RAD)': 1, '507 LONG BRANCH': 12, '507 LONGBRANCH': 1, '507 RAD': 1, '508 LAKESHORE': 1, '509 HARBOURFRONT': 8, '51 LESLIE': 483, '510': 6, '510 SPADINA': 23, '511': 6, '511 BATHURST': 9, '511 BATHURST (600)': 1, '512': 7, '512 ST CLAIR': 5, '512 ST CLAIR - 600 RAD': 1, '512 ST. CLAIR': 6, '513 QUEEN EAST': 1, '52': 5, '52 BURNHAMTHORPE': 1, '52 LAWRENCE WEST': 2387, '52 LAWRENCE WEST & 952': 1, '52B LAWRENCE WEST': 1, '52F LAWRENCE WEST': 1, '53 STEELES EAST': 1435, '534': 1, '54': 2, '54 LAWRENCE EAST': 1618, '55 WARREN PARK': 123, '555': 30, '56 LEASIDE': 270, '57 MIDLAND': 483, '59 MAPLE LEAF': 363, '59 MAPLE LEAF (A-BRANC': 1, '60 STEELES WEST': 742, '60 STEELES WEST(600 RA': 1, '600': 314, '600  (57 MIDLAND)': 1, '600  -LINE 2 SHUTTLE': 1, '600 (42 CUMMER)': 1, '600 (510)': 1, '600 (900 AIRPORT EXPRE': 1, '600 (RAD)': 4, '600 - 22': 1, '600 - 42 CUMMER': 1, '600 - 501': 1, '600 - 506': 1, '600 - ARROW (32 EGLINT': 1, '600 - ARROW DIVISION': 1, '600 - LINE 2 SHUTTLE': 1, '600 - QUEENSWAY GARAGE': 1, '600 - RAD': 1, '600 - RUNNING AS 506': 1, '600 CONSTRUCTION': 2, '600 CONSTRUCTION XTRA': 1, '600 LINE 1 SHUTTLE': 1, '600 LINE SHUTTLE': 1, '600 RAD': 160, '600 RAD (41 ROUTE)': 1, '600 RAD (LINE 1 SHUTTL': 1, '600 RAD - #504': 1, '600 RAD - 116 BUS': 1, '600 RAD - 52 LAWRENCE': 1, '600 RAD - 95 YORK MILL': 1, '600 RAD - LINE 1 SHUTT': 2, '600 RAD - LINE 2 SHUTT': 1, '600 RAD - ON #35': 1, '600 RAD - OPERATING AS': 1, '600 RAD - OPERATING ON': 1, '600 RAD BUS': 9, '600 RAD LINE 1': 1, '600 RAD LINE 1 SHUTTLE': 1, '600 RAD ON 67 PHARMACY': 1, "600 RAD'S": 1, '600 ROUTE': 1, '600 SERIES': 6, '600 SERIES (501 QUEEN)': 1, '600 SERIES (805 SHUTTL': 1, '600 SERIES (84 SHEPPAR': 1, '600 SERIES (96 WILSON)': 1, '600 SERIES (LINE 2 SHU': 1, '600 SERIES (LINE 6 SHU': 1, '600 SERIES (SHUTTLE)': 1, '600 SHUTTLE': 2, '600 SHUTTLE LINE 1': 1, '600- 510ROUTE': 1, '600-RAD': 3, '600/ 79 SCARLETT': 1, '600/ 84A  SHEPPARD': 1, '600/ 85': 1, '600/ LINE 2 SHUTTLE': 1, '600/42': 1, '600RAD': 8, '601RAD': 1, '61 AVENUE ROAD NORTH': 240, '61 AVENUE ROAD NORTH (': 1, '62 MORTIMER': 303, '63': 4, '63 OSSINGTON': 1669, '63 OSSINGTON (RAD)': 1, '64': 1, '64 MAIN': 816, '65 PARLIAMENT': 503, '66 PRINCE EDWARD': 255, '66B PRINCE EDWARD': 1, '67 PHARMACY': 395, '68 WARDEN': 806, '68 WARDEN (B-BRANCH)': 1, '69': 1, '69 WARDEN SOUTH': 471, '7': 1, '7 BATHURST': 1840, '7 BATHURST (600)': 1, '7 BATHURST (RAD)': 1, '7 BATHURST - 600 RAD': 1, "70 O'CONNOR": 429, '705': 1, '71 RUNNYMEDE': 364, '7107': 1, '72': 1, '72 PAPE': 1077, '73 ROYAL YORK': 608, '73B ROYAL YORK': 1, '74 MOUNT PLEASANT': 125, '74 MT. PLEASANT': 29, '75 SHERBOURNE': 833, '76': 3, '76 ROYAL YORK SOUTH': 400, '76 ROYAL YORK SOUTH (B': 1, '77 SWANSEA': 149, '77 SWANSEA (1 BUS ROUT': 1, '77 SWANSEA (LINE 2 SHU': 1, '78 ST. ANDREWS': 233, '79 SCARLETT ROAD': 483, '7935': 1, '79A SCARLETT ROAD': 1, '79B SCARLETT ROAD': 1, '8 BROADVIEW': 321, '80 QUEENSWAY': 405, '80 QUEENSWAY (RAD)': 1, '805': 3, '805 - EGLINTON LINE 5': 1, '805 - LINE 5 SHUTTLE': 1, '805 LINE 5 SHUTTLE': 3, '805: LINE 5 SHUTTLE': 1, '806': 1, '806 - LINE 6 SHUTTLE': 1, '806 LINE 6 FWLRT SHUTT': 1, '806 LINE 6 SHUTTLE': 1, '82 ROSEDALE': 85, '825': 1, '827': 1, '829 DUFFERIN EXPRESS': 1, '829 DUFFERIN GATE EXPR': 4, '83 JONES': 215, '831 STREETCAR WAY': 1, '84 SHEPPARD': 1, '84 SHEPPARD WEST': 1077, '84 SHEPPARD WEST 984': 1, '8468': 1, '85 SHEPPARD EAST': 1502, '85 SHEPPARD EAST (A BR': 1, '85 SHEPPARD EAST - A B': 1, '85 SHEPPARD EAST / 985': 1, '86': 2, '86 SCARBOROUGH': 1500, '87 COSBURN': 184, '88 SHOUTH LEASIDE': 1, '88 SOUTH LEASIDE': 358, '882 SHUTTLE': 1, '889 RAD, REPLACEMENT O': 1, '89': 2, '89 WESTON': 1127, '89/ / 989 WESTON': 1, '899': 14, '899 OTC': 1, '899 TRAINING BUS': 2, '899 TRAINING ROUTE': 2, '9 BELLAMY': 385, '9*7': 1, '9/16/21/38/43/95/129/1': 1, '90 VAUGHAN': 416, '900': 4, '900 AIRPORT EXPRESS': 497, '900 AIRPORT ROCKET': 98, '9000': 1, '902 /102 MARKHAM ROAD': 1, '902 MARKHAM RD EXPRESS': 567, '9020': 1, '903 KENNEDY SCARBOROUG': 727, '904 SHEPPARD-KENNEDY E': 820, '905 EGLINTON EAST EXPR': 545, '906': 2, '906 AIRPORT - HUMBER C': 1, '906 AIRPORT HUMBER EXP': 1, '906 AIRPORT-HUMBER COL': 89, '9060': 1, '91 WOODBINE': 324, '9129': 1, '913 PROGRESS EXPRESS': 1, '92 WOODBINE SOUTH': 241, '924 VICTORIA PARK EXPR': 376, '925': 2, '925 DON MILLS EXPRESS': 844, '9252': 1, '927 HIGHWAY 27 EXPRESS': 918, '927D  HIGHWAY 27 EXPRE': 1, '929': 1, '929 DUFFERIN': 2, '929 DUFFERIN EXPRESS': 1163, '929 DUFFERIN EXPRESS (': 1, '929 DUFFERIN EXPRESS -': 1, '93 PARKVIEW HILLS': 71, '93 WOODBINE SOUTH': 1, '935': 1, '935 JANE EXPRESS': 733, '937 ISLINGTON EXPRESS': 191, '938 HIGHLAND CREEK EXP': 14, '939': 1, '939 FINCH EAST': 1, '939 FINCH EXPRESS': 1727, '939 FINCH EXPRESS (B)': 1, '939B FINCH EXPRESS': 2, '94 WELLESLEY': 747, '94 WELLESLEY - STATION': 1, '941 KEELE EXPRESS': 228, '944 KIPLING SOUTH EXPR': 64, '945 KIPLING': 1, '945 KIPLING EXPRESS': 269, '9484': 1, '94A WELLESLEY': 1, '95 YORK MILLS': 1476, '95 YORK MILLS/995 YORK': 1, '952 LAWRENCE WEST EXPR': 349, '953 STEELES EAST EXPRE': 100, '953 STEELES EXPRESS': 1, '9535': 1, '954 LAWRENCE EAST EXPR': 187, '956': 2, '9560': 1, '9584': 1, '96': 2, '96 WILSON': 1506, '96 WILSON (OTC)': 1, '960': 2, '960 STEELES WEST EXPRE': 1073, '968': 1, '968 WARDEN EXPRESS': 134, '968 WARDEN EXPRESS (RA': 1, '96B WILSON': 1, '97': 2, '97 YONGE': 1029, '97 YONGE (C BRANCH)': 1, '97B YONGE': 1, '97C YONGE': 3, '98 WILLOWDALE-SENLAC': 275, '984 SHEPPARD WEST EXPR': 236, '985 SHEPPARD EAST EXPR': 258, '986 SCARBOROUGH EXPRES': 278, '989 WESTON': 1, '989 WESTON EXPRESS': 328, '99': 1, '99 ARROW ROAD': 87, '995 EGLINTON EAST EXPR': 1, '995 YORK MILLS EXPRESS': 612, '996 WILSON': 1, '996 WILSON EXPRESS': 875, '9984': 2, '9985': 1, '999': 566, '999 (100 FLEMINGDON)': 1, '999 (111 EAST MALL)': 1, '999 (132 MILNER)': 1, '999 (165 WESTON ROAD)': 1, '999 (33 FOREST HILL)': 1, '999 (600 RAD)': 2, '999 (7 BATHURST)': 1, '999 - CNE EXPRESS': 1, '999 - CNE SHUTTLE': 1, '999 - RAD': 1, '999 - SHUTTLE': 1, '999 RAD': 8, '999 ROUTE FAM': 1, '9999': 1, 'A': 12, 'A150': 1, 'A304': 1, 'A356': 1, 'A421': 1, 'A433': 1, 'A521': 1, 'ALL ROUTES': 1, 'BATHURST': 1, 'BD': 18, 'CHARTERED BUS': 1, 'CNE SHUTTLES': 1, 'CONSTRUCTION BUS': 2, 'DIVISIONAL CLERK': 1, 'DIVISIONAL TRAINING': 1, 'EC': 1, 'EMERGENCY SHUTTLE': 1, 'FIFA TPS CHARTER': 1, 'FLEET': 4, 'FLEET 079': 1, 'FLEET 898': 1, 'FLEET A': 1, 'FLEET A398': 1, 'FLEET VEHICLE': 8, 'GARAGE MECHANIC ROUTIN': 1, 'HARVEY SHOP REPAIR PER': 1, 'HILLCREST COMPLEX': 1, 'LINE #2 SHUTTLE': 1, 'LINE #6 SHUTTLE': 1, 'LINE 1': 1, 'LINE 1 - SHUTTLE': 1, 'LINE 1 SHUTTLE': 65, 'LINE 1 SHUTTLE (600 RA': 1, 'LINE 1 SHUTTLE (RAD)': 1, 'LINE 1 SHUTTLE BUS': 4, 'LINE 2': 4, 'LINE 2 SHUTLE': 1, 'LINE 2 SHUTLLE': 1, 'LINE 2 SHUTTLE': 52, 'LINE 2 SHUTTLE (RAD BU': 1, 'LINE 2 SHUTTLE - 600 R': 1, 'LINE 2 SHUTTLE BUS': 9, 'LINE 4 SHUTTLE': 2, 'LINE 5 SHUTTLE': 1, 'LINE 6 SHUTTLE': 3, 'LINE 6 SHUTTLE BUS': 1, 'LINE SHUTTLE': 1, 'MCCOWAN': 1, 'MT DENNIS TEST BUS': 1, 'NIGHT TRADES': 1, 'OPERATIONS TRAINING CE': 1, 'OTC': 10, 'OTC BUS': 5, 'OTC TRAINING BUS': 5, 'R': 1, 'R5 - DODGE RAM FLEET V': 1, 'RAD': 25, 'RAD (600)': 1, 'RAD - 151 LESLIE': 1, 'RAD - 53 STEELES EAST': 1, 'RAD - 806': 1, 'RAD 600': 5, 'RAD 600 - 506 CARLTON': 1, 'RAD 63': 1, 'RAD 72 PAPE': 1, 'RAD 999': 1, 'RAD BUS': 2, 'RENTAL FLEET VEHICLE': 1, 'REVENUE DEPARTMENT': 1, 'REVENUE OPERATIONS TRU': 1, 'REVENUE SERVICES': 1, 'REVENUE TRUCK 85': 1, 'ROAD TEST': 1, 'SHELTER BUS': 1, 'SHEPPARD-KENNEDY EXPRE': 1, 'SHP': 4, 'SHUTTLE': 1, 'SHUTTLE BUS': 23, 'SHUTTLE BUS - LINE 1': 1, 'SHUTTLE BUS LINE 2': 1, 'SHUTTLE BUS-504': 1, 'SHUTTLE LINE 1': 2, 'SIGNALS FLEET VEHICLE': 1, 'SRT': 24, 'ST. CLAIR': 1, 'TBM': 6, 'TBM OPERATOR KAUDA': 1, 'TRAINING BUS': 17, 'TRANSIT CONTROL BUS OP': 1, 'TRANSIT CONTROL CENTRE': 1, 'TRANSIT SPECIAL CONSTA': 1, 'TTC SPECIAL EVENTS BUS': 1, 'VARIOUS ROUTE(S)': 1, 'VISION ISSUES': 1, 'WHEEL-TRANS': 1, 'YU': 27}`.
Vehicle `0` occurs 4986 times; whether it means unknown, not applicable, or an actual identifier is unresolved. Vehicle identifiers should be retained as source text pending definition checks.

Most frequent codes: `EFO` (18178), `TFCNO` (8742), `MFSH` (7730), `MFDV` (7288), `TFPD` (6776), `TFO` (5593), `MFUS` (4272), `EFD` (4078), `SFDP` (3747), `MFSAN` (2745), `EFB` (2742), `TFOI` (2673), `MFUI` (2594), `MFVIS` (2485), `SFO` (2342).

## Additional source observations

Exact column order: `['_id', 'Date', 'Line', 'Time', 'Day', 'Station', 'Code', 'Min Delay', 'Min Gap', 'Bound', 'Vehicle']`. Same names as Subway; different order.
Date suffix frequencies: `{'T00:00:00': 102257}`. Bus timestamp dates are parsed explicitly; any non-midnight components remain in the source and are not silently removed.
Date/weekday mismatch examples: `[{'record_number': 83351, 'date': '2026-04-26T00:00:00', 'day': 'Saturday'}, {'record_number': 83352, 'date': '2026-04-26T00:00:00', 'day': 'Saturday'}, {'record_number': 83353, 'date': '2026-04-26T00:00:00', 'day': 'Saturday'}, {'record_number': 83354, 'date': '2026-04-26T00:00:00', 'day': 'Saturday'}, {'record_number': 83355, 'date': '2026-04-26T00:00:00', 'day': 'Saturday'}]`.
Largest Min Delay examples: `[{'_id': '16965', 'Date': '2025-04-18T00:00:00', 'Line': '12 KINGSTON ROAD', 'Time': '05:45', 'Day': 'Friday', 'Station': 'EGLINTON AND BRIMLEY', 'Code': 'MFDV', 'Min Delay': '999', 'Min Gap': '101', 'Bound': 'E', 'Vehicle': '8421'}, {'_id': '14656', 'Date': '2025-04-03T00:00:00', 'Line': '57 MIDLAND', 'Time': '08:31', 'Day': 'Thursday', 'Station': 'MIDLAND AND STEELES', 'Code': 'MFDV', 'Min Delay': '997', 'Min Gap': '101', 'Bound': 'N', 'Vehicle': '0'}, {'_id': '91335', 'Date': '2026-06-16T00:00:00', 'Line': '11 BAYVIEW', 'Time': '08:50', 'Day': 'Tuesday', 'Station': 'DAVISVILLE AND YONGE', 'Code': 'MFDV', 'Min Delay': '997', 'Min Gap': '101', 'Bound': 'S', 'Vehicle': '8797'}]`.
Duplicate examples excluding _id: `[{'values': {'Date': '2025-01-02T00:00:00', 'Line': '35 JANE', 'Time': '20:13', 'Day': 'Thursday', 'Station': 'JANE AND CHALKFARM', 'Code': 'TFCNO', 'Min Delay': '10', 'Min Gap': '20', 'Bound': 'S', 'Vehicle': '1010'}, 'count': 2}, {'values': {'Date': '2025-01-07T00:00:00', 'Line': '29 DUFFERIN', 'Time': '19:43', 'Day': 'Tuesday', 'Station': 'WILSON STATION', 'Code': 'EFHVA', 'Min Delay': '8', 'Min Gap': '16', 'Bound': 'N', 'Vehicle': '9418'}, 'count': 2}]`.
Station and Line frequencies in JSON preserve exact labels; these fields must not be assumed to contain only stations or single standardized routes. Codes require official mode-specific definitions.

## Implications and unresolved questions

- Preserve source strings, file hash, resource identity and record position. Parse dates, times and durations explicitly; timezone/service-day meaning remains unverified.
- Keep blank direction values and zero vehicle/duration values distinct from missing records. Review station/line labels and unusual durations before setting cleaning rules.
- Do not deduplicate using _id or a guessed incident key. Investigate duplicate examples and whether IDs persist across replacement exports.
- Verify code meanings, Min Delay/Min Gap definitions, direction/line conventions, station naming and recording rules against official documentation before interpretation. No lookup or other resource was downloaded.
- Establish publication lag and completeness separately from observed date range; compare future approved snapshots to investigate revisions. This single download establishes no append-only update behavior.
- Shared column names do not prove cross-mode compatibility. No database, pipeline, analytical SQL, dashboard or update automation was implemented.

## Reproduce

`python3 scripts/profile_subway_tracer.py data/provenance/20261021T190548363172Z__bus.json`

Outputs use exclusive creation and refuse to overwrite an existing report. Preserve or deliberately relocate previous reports before rerunning. Acquisition is a separate network command (`python3 scripts/acquire_subway_tracer.py --mode bus`); each successful acquisition creates a new timestamped snapshot.

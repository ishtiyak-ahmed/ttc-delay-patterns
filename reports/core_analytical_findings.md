# Core analytical findings — Task 5.1

These executed SQL results describe recurring **recorded TTC delay activity**, not verified unique real-world disruptions or comparative service reliability. Modes remain separate. All selected records are in the configured 2025-onward scope; all current durations and reported times pass their corresponding eligibility rules.

## Measures and observed coverage

Source: `sql/analysis/mode_summary.sql`, `coverage.sql`, `dates_without_records.sql`.
Counts include zero-minute records and duplicate candidates. Means and medians include eligible zero durations. Zero share uses the eligible-duration record count, not assumed trips or passengers. Missing/invalid durations never become zero. See `sql/analysis/README.md` for measure and export contracts.

| Mode | Recorded incidents | Recorded minutes | Mean minutes | Median minutes | Zero-minute records | Zero share |
| --- | --- | --- | --- | --- | --- | --- |
| Subway | 45,475 | 122,071 | 2.68 | 0 | 29,669 | 65.24% |
| Bus | 102,257 | 2,163,102 | 21.15 | 12 | 12,974 | 12.69% |
| Streetcar | 23,703 | 416,513 | 17.57 | 10 | 5,279 | 22.27% |
| LRT | 4,569 | 38,829 | 8.50 | 3 | 1,908 | 41.76% |

| Mode | First observed date | Last observed date | Observed dates / calendar span | Observed months |
| --- | --- | --- | --- | --- |
| Subway | 2025-01-01 | 2026-08-31 | 608 / 608 | 20 |
| Bus | 2025-01-01 | 2026-08-31 | 608 / 608 | 20 |
| Streetcar | 2025-01-01 | 2026-08-31 | 608 / 608 | 20 |
| LRT | 2025-12-07 | 2026-08-31 | 267 / 268 | 9 |

LRT has no recorded rows for 2026-01-23 within its observed span. Its December 2025 coverage starts on the 7th; it cannot be compared with the other modes' full 20-month spans as equivalent exposure. Every snapshot ends 2026-08-31. Observing rows on every date in another mode does not prove complete reporting or service exposure. No missing dates are filled with zero-delay service.

## When records recur

Sources: `monthly.sql`, `hourly.sql`, `weekday_hour.sql`. Parentheses below are counts or minutes as labelled, not normalized rates. Tied maxima are retained.

| Mode | Highest monthly count | Highest monthly recorded minutes | Highest hourly count | Highest hourly recorded minutes |
| --- | --- | --- | --- | --- |
| Subway | 2025-08 (2,719); 2026-04 (2,719) | 2026-01 (12,376) | 22 (2,692) | 5 (8,368) |
| Bus | 2026-01 (6,008) | 2026-01 (143,043) | 16 (6,879) | 8 (129,915) |
| Streetcar | 2025-02 (1,920) | 2025-02 (42,873) | 15 (1,221) | 15 (22,611) |
| LRT | 2026-03 (650) | 2026-03 (5,210) | 15 (383) | 15 (4,258) |

Subway's busiest months by count are August 2025 and April 2026, tied at 2,719 records, while January 2026 has the highest minute total (12,376). The hours with the most Subway and Bus records differ from those with the most recorded minutes. Frequency and duration therefore answer different temporal questions. These are reported Time buckets, not verified disruption onset or service-day clocks. Monthly totals also reflect different calendar lengths and observed reporting coverage.

Monthly zero-minute shares vary within each mode:

| Mode | Lowest monthly zero share | Highest monthly zero share |
| --- | --- | --- |
| Subway | 59.67% | 72.75% |
| Bus | 10.52% | 14.40% |
| Streetcar | 18.94% | 26.87% |
| LRT | 21.76% | 54.60% |

Exploratory date-derived weekday/hour maxima:

| Mode | Peak weekday/hour cell | Records in cell | All exploratory records | Conflict-excluded records | Conflicts omitted only in sensitivity |
| --- | --- | --- | --- | --- | --- |
| Subway | Monday 08:00–08:59 | 455 | 45,475 | 45,412 | 63 |
| Bus | Friday 15:00–15:59 | 1187 | 102,257 | 102,127 | 130 |
| Streetcar | Saturday 16:00–16:59 | 209 | 23,703 | 23,661 | 42 |
| LRT | Friday 15:00–15:59 | 77 | 4,569 | 4,149 | 420 |

These two variants are alternatives, never additive. All source-validated weekday eligibility remains zero. LRT loses 420/4,569 records (9.19%) under the sensitivity, so its weekday pattern is particularly uncertain. Different weekdays have different numbers of observed dates; these are raw frequency distributions, not per-service-day risk estimates.

## Where: exact reported route/line labels

Source: `raw_lines.sql` includes per-mode ranks by both frequency and recorded minutes, means, medians, zero shares and distinct observed dates. `eligibility_audit.sql` accounts for exclusions.

| Mode | Most frequent raw label | Records | Highest-minute raw label | Recorded minutes |
| --- | --- | --- | --- | --- |
| Subway | YU | 23,134 | YU | 65,506 |
| Bus | 52 LAWRENCE WEST | 2,387 | 52 LAWRENCE WEST | 48,648 |
| Streetcar | 504 KING | 4,102 | 504 KING | 77,703 |
| LRT | EC | 2,743 | FW | 19,324 |

LRT illustrates frequency versus duration: `EC` has 2,743 records and 19,256 minutes (mean 7.02), while `FW` has 1,808 records and 19,324 minutes (mean 10.69). Their observed dates also differ (205 and 262). This does not establish which line is more reliable. Subway `YU` has 23,134 records and 65,506 minutes; `BD` has 19,758 records and 51,508 minutes. Labels remain literal source categories, including other unusual and compound labels in the complete export.

| Mode | Excluded blank raw Line records | Their recorded minutes | Excluded blank raw Code records | Their recorded minutes |
| --- | --- | --- | --- | --- |
| Subway | 177 | 8 | 0 | No excluded records |
| Bus | 1,241 | 2,017 | 0 | No excluded records |
| Streetcar | 352 | 1,581 | 1 | 0 |
| LRT | 7 | 131 | 0 | No excluded records |

The 1,777 blank-line records contribute 3,737 minutes and remain in overall and temporal totals; they are excluded only from named-label analyses. The single blank Streetcar code contributes zero minutes and remains an incident elsewhere. No nonblank raw label is excluded merely because its canonical identity is uncertain. None has been canonicalized.

## How: recorded code and duration patterns

Sources: `raw_codes.sql`, `duration_distribution.sql`.

| Mode | Most frequent raw Code | Records | Highest-minute raw Code | Recorded minutes |
| --- | --- | --- | --- | --- |
| Subway | SUDP | 5,171 | SUDP | 12,141 |
| Bus | EFO | 18,178 | MFDV | 871,387 |
| Streetcar | MTDV | 2,449 | MTDV | 102,254 |
| LRT | EXO | 392 | PXSW | 6,485 |

Bus `MFDV` contributes 871,387 recorded minutes from 7,288 records (mean 119.56, median 65), while the more frequent `EFO` contributes 251,714 minutes from 18,178 records. Subway `MUIS` has 4,263 records but only 369 minutes; 4,217 are zero-minute records. The raw-code outputs reveal different frequency/duration profiles without asserting verified causes. No descriptions are attached: dictionary applicability remains unverified.

Long recorded durations account for substantial portions of minute totals within individual modes:

| Mode | Records over 60 min | Share of eligible records | Their recorded minutes | Share of recorded minutes |
| --- | --- | --- | --- | --- |
| Subway | 110 | 0.24% | 18,426 | 15.09% |
| Bus | 4,209 | 4.12% | 853,656 | 39.46% |
| Streetcar | 1,188 | 5.01% | 156,460 | 37.56% |
| LRT | 110 | 2.41% | 16,269 | 41.90% |

The distribution export separates zero, positive up to 5, over 5–15, over 15–30, over 30–60, over 60–120, over 120, and unavailable/ineligible duration buckets where observed. There is no clipping or deletion of long records. Recorded minutes cannot be summed into passenger delay or network-wide service impact; concurrent or repeated reporting may overlap.

## Execution and verification

Local Milestone 4 checkpoint: `c305b1e` (`Complete curated layer with explicit snapshots and validation rules`). Reviewed exactly nine source/test/config/report files; raw/local databases, environment files, credential filenames and temporary files passed ignore probes. No files were pushed. Task 5.1 changes remain uncommitted for review.

Commands executed (repository root):

```sh
git status --short
git diff --stat
git check-ignore data/raw/probe.csv data/local/probe.sqlite3 .env credentials-test.json probe.tmp
git add config/curated_snapshots.json docs/cleaning_validation_rules.md reports/curated_layer_verification.md reports/curated_repeat_verification.json reports/curated_verification.json scripts/build_curated.py sql/build_curated.sql sql/curated_schema.sql tests/test_curated_layer.py
git diff --cached --check
git diff --cached --stat
git commit -m "Complete curated layer with explicit snapshots and validation rules"
python3 -m unittest discover -s tests -v
python3 scripts/run_core_analysis.py --output results/core_analysis
```

Additional local Python checks captured pre/post hashes of every existing file under `data/`, independently recomputed medians, sums and zero counts from actual eligible database values, and executed/exported the final code again into `/tmp/ttc-core-repeat-export` for byte comparison. An earlier development export was moved to `/tmp/ttc-analysis-initial-export` before the final export; no original input was overwritten.

- All **43 tests pass**, including five new offline analytical tests: even/odd medians; zero, blank, invalid and negative durations; all-unavailable NULL groups; category/hour exclusions; weekday sensitivity; raw-label and duplicate retention; unselected revision isolation; wrong-selection rejection; deterministic exports and overwrite refusal. An initial duplicate test fixture accidentally had differing source weekdays; the fixture was corrected and the complete suite rerun successfully.
- **176,004** selected records reconcile to **176,004** staging keys. Summary, monthly, duration-band, eligible-hour, eligible-line, eligible-code and both weekday variant totals pass independent eligibility-based checks. Category exclusions reconcile both counts and minutes.
- All **49,830 zero-minute records** are retained; eligible duration records total **176,004**, with **126,174 positive** and **zero missing/invalid/negative durations** in the current data. Total recorded minutes: **2,740,515**. No scoped/unallocated-hour exclusions occur currently; synthetic tests cover future invalid values.
- All **770 duplicate-candidate records** remain represented. All **655 weekday conflicts** remain in the main exploratory distribution and are omitted only in the explicitly named sensitivity. No curated record changed.
- SQLite integrity is `ok`, foreign-key violations are zero, and every row references a selected snapshot with matching resource/checksum identity in staging. The executor checks the full selection configuration, not the latest ingestion timestamp. Unselected revisions cannot enter these outputs.
- Each query executed twice with identical ordered results; two final exports are byte-identical. Independent Python medians, duration sums and zero counts agree with SQL. All original raw/provenance/staging/curated files match their pre-task hashes. Checksums and detailed checks are in `reports/core_analysis_verification.json`; query/artifact/selection/export hashes are in `results/core_analysis/manifest.json`.

Curated artifact SHA-256: `70e25ed9fd6ba4c6516f957e0fcfa0b825b5d4337ab7cb8203729fdf19bb5f31`.

Files created: ten query files plus `sql/analysis/README.md`; `scripts/run_core_analysis.py`; `tests/test_core_analysis.py`; ten CSVs, typed `results.json` and `manifest.json` under `results/core_analysis/`; this report and `reports/core_analysis_verification.json`. Existing working code, governing documents, raw files, provenance and database records were not modified.

Remaining limitations: uncertain reporting completeness and mode-specific inclusion practices; unverified source-calendar/service-day semantics; unresolved code dictionaries and Min Gap meaning; no permanent real-incident identity; raw labels without approved mappings; no suitable service-exposure or passenger denominator. These outputs answer where recorded activity concentrates within each source, not comparative reliability, causality or passenger impact. Task 5.2 has not started.

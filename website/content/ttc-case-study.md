---
title: Understanding TTC Delay Patterns
subtitle: When incident frequency and recorded duration tell different stories
status: editorial-source-draft
period: January 2025–August 2026 (mode-dependent)
author: Ishtiyak Ahmed
---

> **Editorial source note (remove from published website):** This is a comprehensive, evidence-grounded reconstruction of the six previously developed sections, assembled from the available editorial draft and verified project notes. The original six WritingBlock bodies were not available verbatim in the current workspace. **Do not represent this file as a word-for-word reproduction of those blocks.** Before final publication, reconcile wording against the original blocks if they become available. Preserve every substantive finding and caveat below; do not silently abbreviate.

# Understanding TTC Delay Patterns

**When incident frequency and recorded duration tell different stories.**

An independent data analytics case study of **176,004 recorded incidents**, **2,740,515 recorded delay minutes**, and **four TTC transit modes**. Built with Python, SQLite, SQL, and prepared Power BI reporting assets.

**Research question:** *When, where, and how do recorded TTC delays recur—and what changes when we examine both incident frequency and recorded delay duration?*

**Project status:** Analysis, SQL aggregates, source validation, and Power BI exports are complete at the verified checkpoint. Power BI Desktop model validation was previously reported complete by the author. No PBIX, screenshots, or public report URL are supplied in this repository; publication is not independently verified. Dashboard placements are explicitly pending assets.

## 01 — Project Overview

### The question behind the analysis

As a university student who regularly uses the TTC, I wanted to investigate transit disruptions using recorded evidence rather than personal anecdotes. Delays are often discussed in terms of how frequently they happen, but frequency alone can conceal important differences in duration. A large number of short or zero-minute records can dominate a count-based ranking, while a relatively small group of long-duration records contributes a disproportionate share of accumulated delay minutes.

I developed an end-to-end workflow for selected Toronto Transit Commission Bus, Subway, Streetcar, and LRT delay datasets. The workflow ingests versioned public source snapshots, preserves original fields, applies explicit validation rules, and produces SQL-based analytical aggregates for Power BI. The selected data contains **176,004 source-reported incident records** and **2,740,515 recorded delay minutes**. These are *records and recorded minutes*, not independently verified unique disruptions or passenger-minutes lost.

The central analytical decision was to examine **incident frequency and recorded duration together** rather than treat either as a complete description of disruption. This reveals three findings:

1. **Long Bus records dominate recorded minutes:** Records exceeding 60 minutes represent **4.12%** of Bus incidents but **39.46%** of Bus recorded delay minutes.
2. **Zero-minute Subway entries reshape count-based analysis:** **65.24%** of Subway records contain zero recorded delay minutes, including **98.92%** of records under the raw code `MUIS`.
3. **Monthly leaders depend on the metric:** The Subway raw line label `YU` leads incident counts in all 20 months, but `BD` leads recorded minutes in three months. Bus code `MFDV` leads monthly recorded minutes throughout the same 20-month period.

These findings are not claims about the TTC's exposure-adjusted reliability or the number of riders affected. They are evidence about the **composition, concentration, and recurrence of recorded incident activity**, intended to guide more specific operational questions.

**[VISUAL: Hero summary of the three findings; native, responsive graphics; no dashboard screenshot required.]**

## 02 — Data & Methodology

### Sources and observation windows

The analysis uses selected, versioned snapshots of four official Toronto Open Data TTC delay datasets. Different modes have different observation windows, which matters when interpreting comparisons.

| Mode | Observed period | Records | Recorded delay minutes | Zero-minute records |
|---|---|---:|---:|---:|
| Bus | Jan 1, 2025–Aug 31, 2026 | 102,257 | 2,163,102 | 12,974 |
| Subway | Jan 1, 2025–Aug 31, 2026 | 45,475 | 122,071 | 29,669 |
| Streetcar | Jan 1, 2025–Aug 31, 2026 | 23,703 | 416,513 | 5,279 |
| LRT | Dec 7, 2025–Aug 31, 2026 | 4,569 | 38,829 | 1,908 |
| **Total** | **Mode-dependent** | **176,004** | **2,740,515** | **49,830** |

Bus, Subway, and Streetcar have records on **608 calendar dates across 20 months**. LRT has **267 observed dates** over a 268-day span; **January 23, 2026** has no observed LRT record. The number of observed dates does not establish that the source captured all incidents on those dates, and the shorter LRT period makes unadjusted cross-mode comparisons inappropriate.

### A reproducible pipeline

**[VISUAL: Five-stage architecture diagram; must be built as real HTML/SVG, not escaped markup.]**

1. **Selected source snapshots:** Pin source versions and retain provenance and SHA-256 checksums.
2. **Lossless staging:** Load raw incident fields without overwriting original values.
3. **Curated validation:** Normalize analysis fields while retaining source values; flag, rather than silently delete, ambiguous records.
4. **SQL analytical aggregates:** Produce reconciled frequency, duration, temporal, code, line, and duration-band outputs.
5. **Power BI reporting exports:** Generate validated CSVs and a documented reporting-model contract with DAX measures.

This separation between source preservation and analytical normalization is deliberate. It makes cleaning decisions inspectable and permits aggregate findings to be traced back to the selected data. It also protects against seemingly convenient corrections that would quietly change the observed population.

### Data-quality decisions

| Observed issue | Records or entries | Analytical decision |
|---|---:|---|
| Zero recorded delay minutes | 49,830 records | Keep as valid source-reported zeros; distinguish from missing duration |
| Duplicate-candidate records | 770 records in 383 groups, including 387 beyond the first | Flag; do not assume duplicate real-world incidents or automatically remove |
| Recorded weekday inconsistent with parsed date | 655 records | Retain original and derived weekday separately; qualify weekday analysis |
| Missing line labels | 1,777 records | Preserve and mark unknown rather than inventing a line |
| Missing operational code | 1 record | Preserve as unresolved |
| LRT reporting-date gap | Jan 23, 2026 has no observed records | Keep the reporting gap visible; do not invent a record or interpret absence as zero-delay service |

The selected records have no missing, invalid, or negative duration values at the verified checkpoint. Duration outliers are **not capped** simply because they are large: the long-duration tail is one of the questions under investigation.

### Analytical definitions and validation

**Incident count** means the number of source-reported records meeting the current filter conditions. **Recorded delay minutes** means the sum of the corresponding source-reported durations. **Incident share** and **minute share** use the appropriate mode, period, and eligible-record denominators. **Duration bands** distinguish zero minutes from positive-duration ranges, including over 60 minutes. **Monthly leaders** are calculated independently for each metric; a count leader need not be a minute leader.

The pipeline checks count/minute reconciliation, provenance and export integrity, deterministic outputs, and dimensional consistency. The latest verified checkpoint has **76 passing automated tests**. Reproducibility and arithmetic consistency establish that the published computations match the selected source snapshots; they do **not** independently verify the TTC's operational reporting practices.

**[VISUAL: Compact pipeline + validation evidence panel. Keep the full issue table readable on desktop and mobile.]**

## 03 — Data Enrichment & Validation

### Making operational codes interpretable

Raw TTC operational codes are useful grouping keys, but not self-explanatory labels. To support readable analysis, I matched observed codes against official **mode-specific** reference dictionaries. A code is identified by the combination of **transit mode and exact code**, not by assuming that the same text has the same meaning across modes.

The first accepted dictionary matches covered **133,713 of 176,004 incident records (75.97%)**. Review revealed a character-encoding defect in some reference descriptions. Rather than perform an indiscriminate text rewrite, I examined **56 candidate repairs**—10 Bus, 13 Streetcar, and 33 Subway—and accepted only the exact reversible recovery of a corrupted en-dash sequence. Strict Latin-1 encoding / UTF-8 decoding, an exact round-trip check, and a checksum-bound allowlist preserve all surrounding source wording. LRT required no such repairs.

After review, **165,124 records (93.82%)** had accepted descriptions: **31,411 additional records**, or a **17.85-percentage-point increase** in incident-weighted coverage. The accepted dictionary contains **342 described entries** among **479 mode/code dimension entries**.

**[VISUAL: Before/after coverage comparison, 75.97% → 93.82%, with 31,411 additional covered records and exact denominators.]**

### What remained unresolved—and why that matters

The remaining **137 mode/code entries** are not silently assigned meanings. They include **135 entries without an accepted mapping**, one LRT code with conflicting official interpretation, and one blank Streetcar code. Together these unresolved categories account for **10,880 incident records**. The interface displays the original code with a clearly identified **“Description unavailable”** fallback where necessary.

Crucially, enrichment changed **descriptive metadata**, not the incident population, code keys, or recorded-minute totals. The 176,004 records, 2,740,515 minutes, and 479 mode/code dimension entries remain reconciled after recovery. This is a small but important example of engineering judgment: improving interpretability while resisting unsupported inferences.

An accepted reference description is still a **reporting label**, not proof of a physical cause. This case study avoids expanding acronyms or inferring broad code families without accepted evidence.

**[VISUAL: Three-step evidence strip: detect encoding defect → review official dictionaries → validate unchanged totals.]**

## 04 — Dashboard & Key Findings

The intended Power BI experience has three pages: **Frequency vs Duration**, **Concentration & Persistence**, and **Explore the Records**. The analytical findings below have been independently verified against the selected aggregates. Desktop model validation was previously reported complete by the author; report screenshots and public publication are not verified in this repository. Native evidence graphics appear below; clearly labeled placements reserve space for later report screenshots.

### Finding 1 — Long Bus records dominate accumulated minutes

Only **4,209 of 102,257 Bus records (4.12%)** exceed 60 recorded minutes, yet they contribute **853,656 of 2,163,102 Bus minutes (39.46%)**. That contrast makes duration concentration impossible to see from incident counts alone.

The raw Bus code `MFDV` demonstrates a related ranking reversal. It appears in **7,288 records (7.13%)** but accounts for **871,387 minutes (40.28%)**. By comparison, `EFO` appears in **18,178 records (17.78%)** yet accounts for **251,714 minutes (11.64%)**. `EFO` is more frequent, while `MFDV` contributes far more recorded minutes. `MFDV` leads Bus recorded-minute totals in **all 20 months**, contributing between **29.05% and 50.33%** of each month's Bus minutes.

These are **overlapping lenses on the same records**, not two independent sources of delay. Specifically, `MFDV` and the over-60-minute group overlap in **3,775 records and 777,169 minutes**. Do **not** add their percentages together. Their union accounts for **7,722 Bus records and 947,874 Bus minutes (43.82%)**.

**Interpretation:** Count-first triage would highlight `EFO`, while accumulated-duration review would consistently surface `MFDV` and the long-duration tail. The appropriate next step is to investigate recording definitions, durations, and operational context—not to infer causes from code labels alone.

**[NATIVE FIGURE 1A: Two aligned horizontal share comparisons: >60-minute Bus incident share 4.12% vs minute share 39.46%.]**

**[NATIVE FIGURE 1B: `EFO` vs `MFDV` incident-share and minute-share comparison, with visible overlap caveat.]**

**[POWER BI PLACEHOLDER 1: Screenshot from Frequency vs Duration; preserve original aspect ratio, descriptive caption, and alt text. Do not render fake dashboard UI.]**

### Finding 2 — Zero-minute records shape Subway counts

Of **45,475 Subway records**, **29,669 (65.24%)** report **zero recorded delay minutes**. This is not a small edge case: the monthly zero-minute share remains above half throughout the 20-month period, ranging from **59.67% to 72.75%**.

The raw code `MUIS` is particularly concentrated in this category: **4,217 of 4,263 records (98.92%)** have zero recorded minutes, and all `MUIS` records together contribute only **369 recorded minutes**.

**Interpretation:** A count-based ranking can be strongly influenced by categories that contribute little or no positive recorded duration. A zero-minute entry must not be converted to missing data, but it also must not be interpreted as proof of zero passenger impact. The distinction between **reported record count** and **recorded duration** is essential.

**[NATIVE FIGURE 2A: Subway 65.24% zero-minute / 34.76% positive-minute record composition.]**

**[NATIVE FIGURE 2B: Monthly zero-minute share range, using the verified monthly CSV; no invented intermediate month values.]**

**[POWER BI PLACEHOLDER 2: Screenshot from Concentration & Persistence.]**

### Finding 3 — Monthly leaders depend on the metric

The Subway raw line label `YU` leads incident counts in **all 20 observed months**. However, `BD` leads recorded minutes in **March 2025, March 2026, and April 2026**; `YU` leads recorded minutes in the other **17 months**. A stable count leader therefore does not imply an uninterrupted duration leader.

Bus records show a related temporal change. `EFO` leads monthly Bus incident counts for the first **15 months (January 2025–March 2026)**, but not for **April–August 2026**. `MFDV` remains the Bus recorded-minute leader in **all 20 months**. These observations support examining persistence and changes in rank, not merely full-period totals.

A separate LRT near-tie (`EC` versus `FW`) is **not** presented as a headline rank reversal: their observed reporting coverage differs, making an unqualified comparison misleading.

**Interpretation:** Temporal persistence adds context to aggregate rankings. Stable or shifting leaders can help focus investigation, but reporting changes and incomplete operational denominators limit what those patterns establish about service performance.

**[NATIVE FIGURE 3: Subway `YU` / `BD` month-by-month count and minute leadership. Use actual month data; an evidence-backed 20-cell matrix is acceptable.]**

**[POWER BI PLACEHOLDER 3: Screenshot from Explore the Records.]**

### Synthesis

The findings reveal three complementary ways that frequency can mislead when used alone: **duration concentration**, **zero-minute composition**, and **temporal ranking changes**. None of these establishes an exposure-adjusted reliability ranking. Together, they provide a disciplined framework for asking which records, codes, lines, and periods warrant further scrutiny.

## 05 — Discussion & Limitations

### From descriptive evidence to investigation priorities

The results are most useful as a way to prioritize follow-up analysis—not as definitive operational diagnoses.

| Observed pattern | Investigation priority | What would strengthen the conclusion |
|---|---|---|
| Long Bus durations and `MFDV` concentration | Examine recording practices and the underlying long-duration records | Operational logs, incident definitions, and contextual verification |
| Subway zero-minute records and `MUIS` | Understand what a zero means in the reporting workflow | Documentation of reporting rules and event lifecycle |
| Monthly line and code rank changes | Examine persistent and shifting categories | Consistent reporting practices and service exposure by period |

### Boundaries of interpretation

**Incident counts are not exposure-adjusted reliability.** The selected sources do not supply a consistent denominator such as scheduled trips or vehicle-kilometres. Comparing raw counts across modes, routes, or lines cannot establish which service is more reliable.

**Recorded minutes are not passenger impact.** Source-reported duration is not passenger-minutes lost. Multiple records may refer to overlapping activity, and the dataset does not establish the number of people affected.

**Descriptions are not verified causes.** A dictionary label improves interpretation of a code but cannot independently establish the operational cause. Unresolved codes remain unresolved.

**Coverage and reporting practices matter.** LRT begins later than the other modes, and recorded dates are not a guarantee of complete reporting. Changes in logging conventions may influence observed trends. LRT weekday labels also contain substantial source/derived-date disagreement, so weekday analysis for that mode should remain exploratory.

These constraints do not invalidate the arithmetic findings. They define the question the data can answer: **how selected source-reported incident records are distributed**, not the TTC's overall reliability or the full passenger experience.

## 06 — Conclusion & Next Steps

The TTC delay records show why frequency and duration need to be interpreted together. A small share of long Bus records accounts for a large share of recorded minutes; most Subway records contain zero reported minutes; and monthly rankings can change depending on the measure. These are distinct, reproducible observations that a single incident-count leaderboard would miss.

The project's technical contribution is an auditable Python/SQLite pipeline, SQL analytical aggregates, source-preserving validation rules, and mode-specific code-description recovery that raised incident-weighted coverage from **75.97% to 93.82%**. Validated reporting exports, model specifications, and DAX measures are prepared for the final Power BI interface.

The highest-value extensions are to **(1)** incorporate service-exposure denominators, **(2)** obtain operational context for long durations, code definitions, and zero-minute records, and **(3)** link appropriate passenger-impact data where available. Those additions would allow the investigation to move from describing recorded patterns toward more consequential operational conclusions.

The broader lesson is methodological: good analysis is not simply identifying the largest number. It requires choosing defensible measures, preserving uncertainty, testing transformations, and communicating what the evidence can—and cannot—support.

---

## Publication metadata and references (implementation notes, not body copy)

- **Independent analysis:** Not affiliated with or endorsed by the Toronto Transit Commission.
- **Sources:** Official City of Toronto Open Data TTC Bus, Subway, Streetcar, and LRT delay datasets, selected versioned snapshots. Codex must retrieve exact dataset URLs from the repository's provenance metadata rather than invent them.
- **Repository evidence:** `reports/temporal_persistence_evidence.md`, `reports/core_analytical_findings.md`, `reports/code_description_encoding_recovery.md`, `reports/code_description_enrichment.md`, `docs/cleaning_validation_rules.md`, `docs/power_bi_data_contract.md`, `docs/power_bi_desktop_build.md`, `power_bi/measures.dax`, `sql/analysis/`.
- **Unpublished assets:** Do not link to a non-existent Power BI public report. Clearly label placeholders during development; hide or replace them before public launch if necessary.
- **Data accuracy:** The full 20-month monthly values must come from checked-in analysis CSVs, never be inferred from ranges in this document.

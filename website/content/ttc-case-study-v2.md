# Understanding TTC Delay Patterns

**Why incident frequency and recorded delay duration tell different stories.**

An analysis of **176,004 TTC incident records** reveals how incident frequency, accumulated delay duration, and monthly rankings produce different views of reported disruptions.

Official Toronto Open Data · Bus, Subway, Streetcar & LRT · Through August 2026

---

# 01 — Project Overview

## Motivation

As a regular TTC commuter, I wanted to understand disruption patterns beyond my own experience: which incidents recur most frequently, which accumulate the most recorded delay time, and whether those patterns persist across months.

**Incident frequency and recorded delay duration measure different things.** A frequently reported category may contribute relatively few delay minutes, while a less frequent category may account for a disproportionate share.

## Research question

**When, where, and how do recorded TTC delays recur—and what changes when we compare incident frequency with recorded delay duration?**

The analysis examines three dimensions:

1. **Frequency vs. duration:** How do rankings of transit modes, operational codes, and reported lines change between incident counts and accumulated recorded minutes?
    
2. **Concentration:** Which duration ranges and operational categories account for disproportionate shares of recorded delay time?
    
3. **Persistence:** Which patterns remain consistent across months, and which depend on the reporting period or measure?
    

The objective is to characterize reported disruptions, not produce a single TTC reliability score.

## Dataset

Four official TTC delay datasets published through Toronto Open Data:

|Measure|Scope|
|---|---|
|Recorded incidents|**176,004**|
|Recorded delay minutes|**2,740,515**|
|Transit modes|Bus, Subway, Streetcar, LRT|
|Bus, Subway, Streetcar coverage|January 2025 – August 2026 (20 months)|
|LRT coverage|December 2025 – August 2026|

The datasets have mode-specific reporting characteristics and unequal observation periods. Totals represent source-reported incidents and accumulated recorded minutes—not affected passenger counts, passenger-minutes lost, or service-exposure-adjusted reliability.

## Engineering approach

I built a reproducible **Python, SQLite, and SQL** pipeline to ingest source files, preserve raw values, apply documented cleaning and validation rules, and generate analytical outputs.

The workflow includes:

- **Source preservation and validation:** Retain original fields, standardize analytical values, and flag unresolved reporting inconsistencies.
    
- **Operational-code enrichment:** Review reference descriptions, recover verified text-encoding defects, and leave unsupported mappings unresolved rather than inventing meanings.
    
- **Analysis:** Compare incident counts, recorded minutes, duration distributions, operational categories, reported lines, and monthly patterns.
    
- **Reporting preparation:** Prepare validated analytical exports and a Power BI reporting model with documented relationships and DAX measures. Interactive report pages remain to be completed and validated.
    

## Key findings

**Bus duration concentration.** Incidents exceeding 60 minutes represent **4.12% of Bus records** but contribute **39.46% of recorded Bus delay minutes**.

**Subway zero-minute records.** **65.24% of Subway incidents** report zero delay minutes. These observations remain in incident counts but contribute no recorded duration.

**Measure-dependent rankings.** Bus operational-code rankings differ between incident frequency and accumulated minutes. Subway line leadership also changes when comparing monthly incident counts with recorded delay minutes.

These are descriptive findings from published records. They do not establish operational causes, passenger impact, or comparative service reliability.

**Central finding:** Incident counts alone cannot characterize recorded TTC delay patterns. Duration concentration and monthly persistence provide essential complementary evidence.

---
# 02 — Data & Methodology

## Data sources and reporting coverage

The analysis uses four incident-level TTC datasets published through **Toronto Open Data**. Each dataset contains source-reported disruptions for a specific transit mode, with fields including dates, times, operational codes, line or location labels, and recorded delay durations.

The datasets receive monthly updates and differ in field structure, reporting conventions, and observation periods. This analysis uses fixed source snapshots through August 2026.

|Mode|Reporting period|Incident records|Recorded delay minutes|
|---|---|---|---|
|Bus|Jan 2025 – Aug 2026|102,257|2,163,102|
|Subway|Jan 2025 – Aug 2026|45,475|122,071|
|Streetcar|Jan 2025 – Aug 2026|23,703|416,513|
|LRT|Dec 2025 – Aug 2026|4,569|38,829|
|**Total**|**Mode-dependent**|**176,004**|**2,740,515**|

Bus, Subway, and Streetcar each contain observations on **608 calendar dates** across 20 months. LRT reporting begins **December 7, 2025**, with records on **267 of 268 calendar dates** through August 31, 2026.

The datasets lack a common service-exposure denominator, such as scheduled trips, vehicle-hours, or passenger journeys. Differences in record counts or accumulated minutes therefore cannot establish comparative reliability across modes.

Exact source snapshots and their **SHA-256 hashes** are retained to make the analytical baseline reproducible and independent of subsequent monthly dataset updates.

## Pipeline architecture

I built a reproducible **Python, SQLite, and SQL** pipeline with five stages:

|Stage|Implementation|
|---|---|
|**1. Ingestion**|Load the four source datasets into SQLite using Python; preserve original field values alongside standardized analytical fields.|
|**2. Standardization**|Normalize dates, times, transit-mode identifiers, operational codes, line labels, and numeric durations using documented, mode-aware rules.|
|**3. Validation**|Check structural integrity, data types, derived fields, source-to-curated record preservation, and reporting exceptions.|
|**4. Aggregation**|Use SQL to calculate incident counts, recorded minutes, duration distributions, operational-code and line summaries, and monthly patterns.|
|**5. Reporting**|Export validated analytical tables for **Power BI**, with documented relationships, measures, and restrictions on unsupported dimension combinations.|

Source fields remain available after standardization. Derived or corrected analytical values do not overwrite the original observations.

SQL aggregations use consistent measure definitions across the written analysis and reporting exports.

## Data-quality findings

Validation identified the following source-data exceptions:

|Issue|Count|Treatment|
|---|---|---|
|Duplicate candidates beyond the first occurrence|**387**|Flagged; not automatically deleted|
|Reported weekday conflicts with calendar-derived weekday|**655**|Both values preserved; substantial concentration in LRT|
|Missing line labels|**1,777**|Retained as unresolved|
|Missing operational code|**1**|Explicitly retained without an inferred code|
|LRT date without recorded rows within the observed span|**1 date: January 23, 2026**|Reporting-date gap; not interpreted as zero-delay service|

These counts describe observed inconsistencies, not necessarily confirmed source errors.

**Duplicate handling.** Without reliable event-level identifiers, identical or similar rows cannot be assumed to represent the same real-world disruption. Automatic deduplication could remove legitimate observations.

**Weekday conflicts.** Calendar-derived weekdays support temporal analysis when valid dates exist. They are stored separately from conflicting source-reported weekday labels.

**Missing fields.** Line labels, operational codes, and dates are not inferred without authoritative evidence. Missing or conflicting values remain traceable to the original records.

The pipeline applies deterministic corrections only when supported by documented rules. Unresolved source ambiguities remain visible.

## Analytical measures

|Measure|Definition|Interpretation boundary|
|---|---|---|
|**Incident frequency**|Count of source-reported incident records in a selected group|Not a count of affected passengers or independently verified disruptions|
|**Recorded delay minutes**|Sum of reported delay-minute values for selected records|Not passenger-minutes lost, network-wide downtime, or individual journey delay|
|**Duration distribution**|Grouping of individual recorded durations to examine their frequency and accumulated minutes|Long-duration records can contribute disproportionately to totals; reported minutes need not represent nonoverlapping disruption periods|

Neither incident frequency nor accumulated recorded duration provides a standalone measure of TTC reliability.

## Zero-minute records

**Zero-minute observations are retained as valid source-reported records unless independent evidence establishes otherwise.**

A reported duration of zero is not automatically missing or erroneous. These records contribute to incident frequency but not accumulated delay minutes.

Removing them would alter the source population and bias frequency-versus-duration comparisons, particularly for Subway, where zero-minute records constitute a majority.

The analysis distinguishes zero-minute and positive-duration observations without deleting either group.

## Reproducibility and testing

The verified analytical baseline passed **76 automated tests** covering pipeline behavior, cleaning rules, analytical contracts, and reporting outputs. Additional website-related tests were introduced later; 76 is the baseline analytical test count, not the current project-wide total.

The repository maintains:

- Fixed source snapshots and SHA-256 checksums.
    
- Python ingestion and transformation logic.
    
- Documented mode-specific cleaning and validation rules.
    
- SQL aggregation queries and analytical outputs.
    
- Power BI reporting contracts, relationships, and measures.
    
- Validation documentation and reproducibility checks.
    

The pipeline preserves source provenance, flags unresolved inconsistencies, and generates repeatable analytical outputs from the selected input snapshots. The published analysis uses a fixed, versioned dataset through August 2026. Pipeline reproducibility does not imply scheduled ingestion of future TTC releases or automatic Power BI refresh.

---
# 03 — Data Enrichment & Validation

## Analytical dimensions

I organized the validated TTC records into dimensions for **reporting month, transit mode, operational code, reported line, and recorded delay duration**.

Calendar-month groupings support temporal comparisons. Operational codes and line labels use **mode-specific identities** to prevent identical values from different transit datasets from being combined incorrectly.

Missing codes and line labels remain explicit categories. Their records contribute to incident counts and recorded-minute totals without receiving inferred identifiers.

### Duration classification

Recorded durations are assigned to eight mutually exclusive categories:

|Duration band|Definition|
|---|---|
|Zero|Exactly 0 minutes|
|Over 0–5|Greater than 0, up to 5 minutes|
|Over 5–15|Greater than 5, up to 15 minutes|
|Over 15–30|Greater than 15, up to 30 minutes|
|Over 30–60|Greater than 30, up to 60 minutes|
|Over 60–120|Greater than 60, up to 120 minutes|
|Over 120|Greater than 120 minutes|
|Unavailable / ineligible|Cannot be included in a nonnegative-minute calculation|

The bands support comparisons between each group's **share of incident records** and **share of accumulated recorded minutes**. Mutually exclusive assignment prevents double counting across duration ranges.

Zero-minute records remain separate from missing or ineligible durations. Derived dimensions do not create incidents, change reported minutes, or infer missing source information.

## Operational-code enrichment

TTC operational codes identify incident categories but are not consistently interpretable without reference descriptions.

I reviewed official code-description dictionaries for Bus, Subway, Streetcar, and LRT. The reference material contained missing mappings, conflicting descriptions, and character-encoding defects.

Descriptions were matched using the exact **transit mode + raw operational code** combination. Acceptance rules distinguished:

- Unambiguous, source-supported descriptions.
    
- Codes absent from the relevant reference dictionary.
    
- Codes associated with conflicting descriptions.
    
- Descriptions with identified encoding defects.
    
- Missing or blank operational codes.
    

Only supported descriptions entered the analytical model. Unresolved codes retained their original identifiers without invented labels.

### Encoding recovery

Some reference descriptions contained text consistent with **UTF-8 bytes incorrectly interpreted as Latin-1**.

I implemented a bounded recovery process that reconstructs and decodes affected text only when the transformation is deterministic, reversible, and satisfies explicit review criteria. Accepted repairs are recorded for repeatable processing; ambiguous or unsuccessful candidates remain unresolved.

|Mode|Accepted encoding repairs|
|---|---|
|Bus|10|
|Subway|33|
|Streetcar|13|
|LRT|0|
|**Total**|**56**|

These repairs affect human-readable reference descriptions, not the underlying incident records.

## Enrichment results

I measured accepted-description coverage at two levels:

- **Code-level coverage:** Distinct mode-specific operational-code entries with accepted descriptions.
    
- **Incident-weighted coverage:** Source incident records associated with accepted descriptions.
    

|Measure|Before enrichment|After enrichment|
|---|---|---|
|Incidents with accepted descriptions|133,713|165,124|
|Share of all incidents|75.97%|93.82%|

Enrichment added accepted descriptions for **31,411 incident records**, increasing incident-weighted coverage by **17.85 percentage points**.

Of **479 mode-specific code entries**, **342 have accepted descriptions** and **137 remain unresolved**. These are code-inventory entries, not incident-record counts.

Unresolved entries include codes without accepted reference mappings, an LRT code with conflicting descriptions, and a Streetcar entry with a blank operational code.

The reporting layer displays accepted descriptions alongside raw codes. Where no description is supported, it retains the code and explicitly marks the description unavailable.

**Accepted descriptions are reference labels, not independently verified operational causes.** Enrichment changes neither incident counts nor recorded delay durations.

## Analytical reconciliation

The reporting exports aggregate the same incident population by month, operational code, reported line, and duration band.

These are **alternative views of the same records**, not independent datasets. Each aggregation must reconcile separately to the source population; totals from different fact tables must not be added together.

The validated baseline is:

|Reconciliation measure|Verified total|
|---|---|
|Recorded incidents|**176,004**|
|Recorded delay minutes|**2,740,515**|
|Zero-minute records|**49,830**|

Monthly, code-level, line-level, and duration-level summaries independently reconcile to the corresponding source totals.

Validation also checks missing-category preservation, mutually exclusive duration-band assignment, and consistency of derived measures. Code-description enrichment leaves all three baseline totals unchanged.

## Power BI aggregation and filtering safeguards

The prepared **Power BI** model uses separate fact tables for monthly, operational-code, line, and duration analysis, with shared transit-mode and reporting-month dimensions.

The model supports consistent mode and month selections while preventing aggregation across alternative fact tables as though they represented separate incident populations.

Category-specific dimensions apply only to their supported facts. For example, a code-level filter cannot automatically determine the corresponding line-level population because the exported summaries do not preserve every code-and-line intersection.

The same restriction applies to unsupported combinations of operational codes, lines, and duration bands.

### Overlapping analytical groups

A Bus record classified under operational code **MFDV** may also belong to the **over-60-minute** duration group. These are overlapping attributes of one record, not independent contributions.

The MFDV/long-duration intersection is calculated from the underlying **SQL** analysis. It cannot be inferred by adding independently aggregated totals or applying unsupported cross-fact filters in Power BI.

The reporting model restricts or explicitly handles these combinations to prevent misleading calculations.

## Validation and reproducibility

Automated checks enforce the enrichment and reporting contracts:

- **Exact matching:** Accepted descriptions correspond to the correct transit mode and raw operational code.
    
- **Encoding integrity:** Repairs match reviewed, deterministic transformations.
    
- **Unresolved mappings:** Missing, conflicting, and ambiguous descriptions remain unassigned without supporting evidence.
    
- **Source preservation:** Incident records, counts, and recorded minutes remain unchanged.
    
- **Reconciliation:** Every analytical aggregation agrees with its underlying source population.
    
- **Reporting integrity:** Relationships, measures, and filtering rules respect the supported aggregation structure.
    
- **Determinism:** Repeated exports from identical inputs produce consistent results.
    

Reference-source provenance and checksums are retained alongside the accepted mappings and generated outputs, supporting independent inspection and reproduction.

---

# 04 — Analytical Findings

## Finding 1 — Bus delay minutes are concentrated in long-duration records

Of **102,257 Bus incidents**, **4,209 records (4.12%)** report durations exceeding 60 minutes. These records contribute **853,656 minutes (39.46%)** of the **2,163,102 recorded Bus delay minutes**.

|Bus duration group|Share of incidents|Share of recorded minutes|
|---|---|---|
|Over 60 minutes|4.12%|39.46%|
|60 minutes or less|95.88%|60.54%|

The 60-minute threshold is an analytical grouping, not an official TTC severity classification. Long-duration observations were retained without arbitrary capping or deletion.

### EFO leads frequency; MFDV leads duration

|Bus operational code|Incidents|Recorded minutes|Incident share|Minute share|
|---|---|---|---|---|
|**EFO**|18,178|251,714|17.78%|11.64%|
|**MFDV**|7,288|871,387|7.13%|40.28%|

**EFO** leads full-period Bus incident frequency; **MFDV** leads accumulated recorded minutes.

Their duration distributions differ substantially:

|Metric|EFO|MFDV|
|---|---|---|
|Mean recorded duration|13.85 min|119.56 min|
|Median recorded duration|12 min|65 min|

### MFDV overlaps with long-duration records

The MFDV and over-60-minute groups are not independent populations.

Of the **4,209** Bus records exceeding 60 minutes, **3,775** carry the **MFDV** code, accounting for **777,169 recorded minutes**.

The two groups contribute **39.46%** and **40.28%** of Bus recorded minutes, respectively, but these percentages **must not be added**.

Their deduplicated union contains **7,722 distinct source rows** and **947,874 recorded minutes**, representing **43.82% of the Bus total**.

The intersection and union were calculated from the underlying SQL records, not by adding separate aggregate totals.

### Monthly persistence

Across all **20 Bus reporting months (January 2025–August 2026)**:

- **MFDV led recorded delay minutes in every month**, contributing **29.05%–50.33%** of monthly Bus minutes.
    
- Records exceeding 60 minutes represented **2.82%–5.74%** of monthly Bus incidents but contributed **27.73%–49.37%** of monthly recorded minutes.
    

The concentration persists across the study period rather than arising from one exceptional month.

The data does not establish the operational cause of MFDV's duration profile, whether recorded minutes represent nonoverlapping disruption periods, or how many passengers were affected.

## Finding 2 — Zero-minute records dominate Subway incident frequency

Of **45,475 Subway incident records**, **29,669 (65.24%)** report **zero delay minutes**.

These records contribute to incident counts but add no recorded minutes. They remain in the analysis because zero is a reported value, not independently established missing or erroneous data.

### Monthly zero-minute composition

Across the **20 Subway reporting months**, zero-minute records account for **59.67%–72.75%** of monthly incident counts—a majority in every month.

### MUIS: frequent incidents, minimal recorded duration

|MUIS measure|Value|
|---|---|
|Recorded incidents|**4,263**|
|Zero-minute incidents|**4,217**|
|Zero-minute share|**98.92%**|
|Total recorded delay minutes|**369**|
|Monthly zero-minute share|**97.79%–100%**|

**MUIS** appears in all 20 months and ranks among the **three most frequent Subway operational codes in every month**, but never leads in recorded minutes.

A zero-minute value does not prove that passengers experienced no disruption. The dataset also cannot establish whether all zero-minute records follow identical reporting conventions.

## Finding 3 — Subway line leadership differs by measure and month

The reported Subway line labels **YU** and **BD** account for the following full-period totals:

|Subway line label|Incidents|Recorded minutes|
|---|---|---|
|**YU**|23,134|65,506|
|**BD**|19,758|51,508|

**YU leads both full-period measures** and ranks first in monthly incident frequency in **all 20 months**.

However, YU leads monthly recorded minutes in only **17 of 20 months**. **BD leads recorded minutes** in:

- March 2025
    
- March 2026
    
- April 2026
    

YU continues to lead incident frequency during those months.

These are comparisons of source-reported line records, not exposure-adjusted reliability. The data lacks comparable trip counts, passenger exposure, and verified equivalence of reporting conditions.

## Supporting finding — EFO loses monthly frequency leadership

Although **EFO** leads overall Bus incident frequency, its monthly ranking changes substantially.

EFO ranks first for **15 consecutive months (January 2025–March 2026)**. During **April–August 2026**, its monthly frequency rankings are:

|Month|EFO frequency rank|
|---|---|
|April 2026|5th|
|May 2026|6th|
|June 2026|6th|
|July 2026|9th|
|August 2026|5th|

EFO remains present in every month but stops leading frequency. **MFDV continues to lead Bus recorded minutes in all 20 months.**

This distinguishes **presence** (a category continues to appear) from **leadership** (it ranks first under a selected measure).

The ranking change does not establish an operational intervention, improved service conditions, or a causal shift. Changes in category usage, reporting conventions, or underlying activity remain possible explanations.

## Supporting finding — Full-period line leaders vary monthly

The reported Bus line label **52 LAWRENCE WEST** leads the full-period Bus dataset in both measures:

- **2,387 incidents**
    
- **48,648 recorded minutes**
    

It leads monthly incident frequency in only **6 of 20 months** and monthly recorded minutes in only **2 of 20 months**. Its monthly minute ranking ranges from **1st to 16th**.

Streetcar line rankings also vary:

- **504 KING** leads monthly incident counts in **9 of 20 months** and recorded minutes in **11 of 20 months**.
    
- **501 QUEEN** also leads in several months.
    

Full-period leadership does not imply consistent monthly leadership.

## Coverage qualification — LRT EC versus FW

The LRT data produces an apparent reversal between incident frequency and recorded duration:

|LRT line label|Incidents|Recorded minutes|
|---|---|---|
|**EC**|2,743|19,256|
|**FW**|1,808|19,324|

**EC** leads incident frequency, while **FW** narrowly leads accumulated minutes across the selected LRT period.

However, the labels have different observed reporting histories:

- **FW** first appears in December 2025.
    
- **EC** first appears in February 2026.
    

Restricting the comparison to the shared **February–August 2026** calendar window changes the results:

|LRT line label|Incidents|Recorded minutes|
|---|---|---|
|**EC**|2,743|19,256|
|**FW**|1,072|10,869|

EC leads both measures within that shared window.

The source records do not establish actual service start dates, equivalent service exposure, or complete reporting coverage. A shared calendar window does not resolve those limitations.

**The full-period EC/FW reversal is therefore not treated as a primary finding about comparative delay patterns.**

## Power BI reporting model

The validated SQL outputs support a prepared **Power BI reporting model** with:

|Component|Specification|
|---|---|
|Reporting tables|**10**|
|One-to-many relationships|**13**|
|DAX measures|**54**|
|Planned report pages|**3**|

The planned report pages are:

**Frequency vs Duration** — Compare incident counts, recorded minutes, and rankings across supported transit-mode, reporting-month, and operational-category selections.

**Concentration & Persistence** — Examine duration distributions, accumulated-minute concentration, and recurring monthly patterns.

**Explore the Records** — Inspect validated aggregate outputs, operational codes, line labels, reporting coverage, and data-quality context.

The reporting model restricts unsupported code, line, and duration intersections because its aggregate fact tables do not preserve every possible combination of source-record attributes.

All reported findings were calculated and verified using SQL. The Power BI reporting model is prepared, but the interactive report pages and their visual interactions have not yet been completed and validated. No dashboard screenshots or published interactive views are presented as completed work.

---

# 05 — Discussion & Limitations

## Measurement validity

The analysis measures **source-reported incident frequency and accumulated recorded delay minutes**, not independently verified disruptions or passenger impact.

A recorded 30-minute incident does not establish how many passengers were affected, how long they waited, or whether other services continued operating.

Incident records may also overlap in time or location. Summing their reported minutes is valid as an aggregation of source values, but the result does not necessarily represent nonoverlapping network downtime.

Consequently, recorded-minute concentration cannot be interpreted as a proportional share of passenger inconvenience.

Measuring passenger impact would require additional evidence, including ridership, service frequency, vehicle movements, passenger travel times, and other operational data absent from the selected TTC delay datasets.

## Cross-mode comparability

**Bus, Subway, Streetcar, and LRT cannot be ranked by reliability using raw incident counts or recorded delay minutes.**

The modes differ in operating conditions, reporting practices, and observed coverage periods. The datasets also lack a common service-exposure denominator.

A higher incident count may reflect more vehicles, routes, or scheduled trips rather than worse reliability. Lower recorded minutes may reflect less service exposure, different reporting conventions, or differences in the types of recorded events.

Comparable rates would require measures such as:

- Scheduled trips or service frequency.
    
- Vehicle-hours or distance operated.
    
- Passenger journeys or other exposure measures.
    

Without these denominators, the analysis cannot calculate comparable incident or delay rates across modes.

The strongest comparisons are therefore **within modes**, using consistent source populations and reporting definitions. Four-mode totals describe dataset scope, not comparative service quality.

## Reporting coverage and missing observations

Bus, Subway, and Streetcar observations cover **January 2025–August 2026**. LRT records begin in **December 2025**.

The selected LRT dataset contains **no records for January 23, 2026**. Its reported line labels **EC** and **FW** also have different observed histories, affecting full-period rankings.

Restricting EC and FW to a shared calendar window changes their relative results but does not establish equivalent service exposure, reporting completeness, or actual service start dates.

**No records on a given date does not prove that service operated without delays.** Conversely, records appearing on every date do not establish complete reporting.

Observed dates measure dataset coverage, not verified service availability.

Monthly changes may reflect actual recorded activity, shifts in reporting coverage, changes in reporting practices, or combinations of these factors. The selected data cannot reliably separate them.

## Incident identity and source-data uncertainty

The pipeline preserves source-reported rows rather than reconstructing a definitive population of unique real-world disruptions.

Validation flagged **387 duplicate candidates beyond the first occurrence**, identified through matching source fields excluding source identifiers. These were not automatically deleted.

Similar records may represent duplicate reporting, separate incidents with identical attributes, or circumstances not distinguishable from the available fields. Without reliable event-level identifiers, deduplication could remove legitimate observations and arbitrarily alter counts and recorded minutes.

The duplicate candidates, weekday conflicts, missing labels, and incomplete fields documented in Section 02 remain unresolved where the source provides insufficient evidence. These uncertainties limit reconstruction of unique real-world incidents and the interpretation of affected categories.

For valid dates, calendar-derived weekdays are stored separately from conflicting source labels. Missing codes, line labels, and dates remain unresolved without authoritative evidence.

These exceptions remain visible in the analytical workflow rather than being converted into unsupported corrections.

## Operational-code interpretation

Operational codes are treated as **source-reported categories**, not independently verified causal classifications.

The enrichment process matches exact mode-specific codes to official reference dictionaries and applies controlled, evidence-supported encoding repairs.

Accepted descriptions improve interpretability but do not establish the operational cause of individual incidents.

Some descriptions remain unresolved. The available dictionaries also do not guarantee that each code's meaning or usage remained unchanged throughout the historical reporting period.

The duration profile associated with **MFDV**, for example, establishes a pattern in recorded values—not the mechanism responsible for those durations or consistency of operational circumstances across records.

Causal interpretation would require additional TTC operational documentation or direct confirmation.

## Long-duration sensitivity

Accumulated recorded minutes are sensitive to unusually long incident durations.

Bus records exceeding **60 minutes** contribute a disproportionate share of recorded minutes. Records exceeding **120 minutes** also contribute substantially to the total.

These observations contain numeric source-reported durations; their magnitude alone does not establish an error.

The pipeline therefore retains long-duration records without arbitrary capping, deletion, or replacement with trimmed estimates.

The resulting concentration is valid for the selected source records but remains sensitive to the reporting conventions used to assign long durations. Those conventions require further investigation before interpreting the values as equivalent operational disruption periods.

## Temporal inference

Monthly rankings and duration shares establish **descriptive persistence**, not causation.

MFDV's recurring recorded-minute leadership demonstrates a stable pattern in the selected Bus records. EFO's later decline in monthly frequency ranking documents a change in relative position.

Neither establishes why the pattern occurred, whether service conditions improved, or whether an operational intervention took place.

Potential explanations include changes in:

- Reporting definitions or category usage.
    
- Service levels and operating patterns.
    
- Underlying incident activity.
    
- Other unobserved operational conditions.
    

The study does not apply **causal inference, controlled comparisons, or statistical change-point testing**. It cannot distinguish among these explanations or attribute observed changes to specific interventions.

## Scope of inference

The analysis supports conclusions about **recorded incident distributions, accumulated delay duration, and recurring temporal patterns** within the selected TTC datasets.

It does not establish passenger-minutes lost, independently verified unique disruptions, comparable reliability across transit modes, or the operational causes of observed patterns.

These are boundaries of the available evidence, not assumptions filled through estimation.

---

# 06 — Conclusion & Next Steps

## Project outcomes

The project produced a reproducible analysis of **176,004 TTC incident records**, distinguishing incident frequency, accumulated recorded delay duration, and monthly persistence across Bus, Subway, Streetcar, and LRT services.

Using **Python, SQLite, and SQL**, I developed a pipeline that:

- Preserves original source records and applies documented, mode-specific cleaning rules.
    
- Identifies reporting inconsistencies without inventing corrections or removing ambiguous records.
    
- Enriches operational codes using official reference dictionaries and verified encoding repairs, increasing incident-weighted accepted-description coverage from **75.97% to 93.82%**.
    
- Produces independently reconciled analytical summaries for incident counts, recorded minutes, duration distributions, operational categories, lines, and reporting months.
    
- Prepares a **Power BI** reporting model with documented relationships, measures, and safeguards against unsupported cross-fact aggregations.
    

The verified findings establish duration concentration, persistent zero-minute reporting, and differences between full-period and monthly rankings. They do not establish operational causes, passenger impact, or exposure-adjusted TTC reliability.

## Next steps

### 1. Normalize findings by service exposure

Integrate scheduled trips, vehicle-hours, service distance, or comparable operating data to calculate incident and recorded-minute rates relative to service delivered.

This would support more defensible comparisons across modes and lines and help distinguish higher incident totals caused by greater service volume from higher rates of reported disruptions.

### 2. Investigate duration-reporting conventions

Examine how the TTC defines and records long-duration Bus incidents, particularly those associated with **MFDV**, including whether incident periods overlap and how operational categories are applied.

Investigate why Subway records frequently report zero minutes, which events qualify for incident reporting, and whether zero-duration observations follow consistent conventions.

These questions require TTC operational documentation or direct clarification; they cannot be resolved from the selected incident records alone.

### 3. Extend temporal monitoring

Incorporate subsequent monthly TTC releases while preserving versioned source snapshots, validation rules, and reproducible analytical outputs.

Track whether **MFDV** maintains its recorded-minute leadership, whether Subway's zero-minute composition persists, and how monthly rankings for categories such as **EFO** evolve beyond August 2026.

Review changes in source schemas, reporting conventions, and reference dictionaries before comparing new observations with the historical baseline.

### 4. Resolve remaining category and coverage gaps

Obtain additional authoritative references for unresolved or conflicting operational-code descriptions and investigate whether code definitions changed during the study period.

Extend and validate LRT reporting coverage, particularly the unequal observed histories of **EC** and **FW**, before drawing stronger line-level comparisons.

Preserve unresolved categories and missing observations until supporting evidence permits correction or classification.

### 5. Complete the Power BI reporting experience

Build and validate the three planned report pages:

- **Frequency vs Duration:** Incident counts, recorded minutes, and supported category comparisons.
    
- **Concentration & Persistence:** Duration distributions and recurring monthly patterns.
    
- **Explore the Records:** Operational codes, reported lines, coverage, and data-quality context.
    

Verify Power BI Desktop visuals, measures, and filtering interactions against the validated **SQL** outputs. Restrict unsupported intersections between aggregated code, line, and duration fact tables.

Publish reviewed dashboard views within the public case study once the interactive report is complete.

## Conclusion

The analysis establishes measurable patterns in published TTC incident records, not a complete assessment of service reliability or passenger experience.

Its engineering contribution is a traceable analytical workflow: preserved source evidence, validated transformations, source-supported enrichment, reconciled aggregations, and explicit reporting constraints.

**Understanding recorded disruptions requires knowing what was counted, what was measured, and what the available evidence can actually support.**
# Analytical case study strategy

Task 5.2, 2026-10-21. This establishes editorial principles and recommends a direction for review. It does not change the governing project scope, selected snapshots, pipeline or research question in `instructions.md` or `ROADMAP.md`. The user’s Task 5.2 brief defines this review; the older roadmap uses the task number for analytical-query implementation.

## Purpose and audience

Demonstrate both analytical reasoning and engineering reliability. The analysis must contribute defensible questions, measures, interpretation and investigation priorities. Engineering must contribute reproducible acquisition, immutable evidence, provenance, snapshot selection, safe reruns, validation, SQL transformations and reconciled outputs. Neither is decoration for the other.

Write for data analyst hiring managers, data engineering hiring managers and technically literate nontechnical stakeholders. Readers should understand the analytical problem and principal evidence before they encounter implementation details. Technical readers should then be able to trace each claim through SQL, eligibility rules and selected source snapshots.

## Recommended analytical direction — pending review

Proposed question: **Within each TTC mode, where do recorded incident frequency and recorded delay minutes point to different investigation priorities?**

Use temporal buckets, raw reported line labels and raw incident codes as analytical lenses. Retain “When, where, and how do recorded TTC delays recur?” as the wider exploratory context. Do not promise persistence or recurring causal mechanisms from full-period totals. This is a framing recommendation using the same four sources and existing pipeline, not an implemented scope change.

The strongest current evidence is duration concentration, frequency-versus-duration differences by raw code, and zero-minute records’ effect on count interpretation. Temporal differences provide useful supporting evidence. A route/location section earns space only if it adds more than a top-label ranking; it may be shortened or replaced by stronger evidence. Raw Line analyses do not establish geographic hotspots.

The existing data supports a recorded-activity case study. It does not support mode reliability rankings, passenger impact estimates, verified causes or recommendations to change service provision. Practical implications should identify what to investigate and what further evidence would be needed, rather than claim operational remedies.

## Deliverables and editorial format

The main deliverable is a professional analytical case-study report of approximately **9–11 pages**, supported by interactive Power BI exploration and a reproducible GitHub repository. Suggested ten-page allocation, flexible to the verified evidence:

| Editorial role | Approximate space | Purpose |
|---|---|---|
| Executive summary | 1 page | Question, three strongest findings, bounded implications and scope warning |
| Analytical problem and questions | 1 page | Explain why frequency and duration may identify different priorities |
| Data scope, methodology and measures | 1 page | Observed coverage, record grain, eligibility, zero/NULL distinction and mode separation |
| Strongest temporal evidence | 1 page | Contrast count and minute patterns; distinguish aggregate differences from persistence |
| Strongest route/line or other evidence | 1 page | Include only if useful beyond ranking; otherwise use this space for a stronger analytical comparison |
| Incident characteristics and duration concentration | 2 pages | Explain raw-code profiles, zero records and duration distribution with clear denominators |
| Evidence-based implications and investigation priorities | 1 page | Explain which recorded categories warrant investigation and which evidence is missing |
| Engineering methodology and reproducibility | 1 page | Show source-to-result traceability, snapshot selection and validation; link implementation detail |
| Conclusions, limitations and next steps | 1 page | Answer the supported question, retain uncertainty and avoid speculative expansions |

These are editorial roles, not nine compulsory findings or fixed chapter lengths. Do not stretch ordinary rankings to fill pages. Build the final structure around the strongest verified evidence after the small follow-up checks in the viability review.

The written case study explains the problem, evidence, reasoning and implications. Power BI lets users explore validated results and their coverage. GitHub demonstrates implementation, testing, lineage and reproducibility. Link lengthy technical documentation instead of reproducing it in the main report. This task produces strategy and review documents only, not the final report or visuals.

## Finding and writing standard

Every major finding must distinguish these five elements, whether in prose or an accompanying evidence note:

| Element | Required content |
|---|---|
| Claim | One bounded statement about the selected records, mode and period |
| Quantitative evidence | Counts, minutes, denominator, eligibility, exact query/export and source selection |
| Interpretation | What the numerical relationship establishes; identify inference explicitly |
| Practical implication | A reasonable investigation priority, not an unsupported causal or operational recommendation |
| Limitations | Coverage, category semantics, uncertainty, sensitivity and evidence that could change the claim |

Separate established results from hypotheses and proposed analyses. Explain “recorded incident” as an eligible source-row count, not an independently verified unique disruption. Never infer causes from literal codes or invent their descriptions. Recorded minutes are not passenger minutes or additive network-wide service impact. Do not infer disruption onset from reported Time, complete reporting from observed dates, or zero-delay service from missing records.

Keep modes identified and avoid shared reliability rankings. Keep original raw codes and line labels; do not imply canonical routes, physical locations or approved mappings. Preserve zero-minute records, unknown categories, long durations and duplicate candidates. Make category exclusions and duration availability visible. Retain explicit snapshot selection; newest retrieval or ingestion is not automatically authoritative.

## Visual and reporting discipline

Use a visual only when it answers a specific question. Prefer paired count/minute panels, duration-distribution shares, and frequency-versus-duration plots over a sequence of unrelated top-ten lists. Put units, coverage, denominators and mode in titles or nearby notes. Avoid dual axes that imply commensurate counts and minutes. Treat weekday displays as exploratory; LRT’s 420 conflicts among 4,569 records make a weekday headline unsuitable.

Power BI should expose only filters supported by the export grain. Sum compatible counts and minutes; compute means and zero shares from their numerators and eligible denominators. Do not average averages, medians or shares, or sum distinct-date counts across overlapping category groups. Median and distinct-date cards require results computed at the selected grain or must be withheld for unsupported filter combinations. The two weekday variants are alternatives, never additive. Display a missing category separately and leave absent reporting periods visibly unavailable.

## Scope and publication gates

Prefer reframing and targeted queries before new sources or architectural changes. Keep the working four-mode pipeline. A dataset change or major project-direction change requires explicit review and approval. The recommendation here remains subject to review; no governing document is edited.

Before Power BI, complete only the two focused monthly cross-tabs and their reconciliation described in `../reports/analytical_viability_review.md`, then decide which claims survive. Persistence and robustness remain hypotheses until tested. If the differences are concentrated in a small period or a few extreme records, publish that narrower conclusion rather than expanding the dataset to rescue the story. Resolve export-grain/filter behaviour before building interactive measures.

The case study is ready for final writing when its headline claims have reproducible evidence, compatible denominators, coverage disclosures, defensible interpretation and bounded implications. Engineering acceptance and analytical acceptance are separate: successful reconciliation does not establish semantic validity, completeness or analytical importance.

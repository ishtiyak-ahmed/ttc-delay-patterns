# Website v2 content coverage

`website/content/ttc-case-study-v2.md` is the single source of truth for report prose. `src/App.tsx` splits that file only at its six numbered section headings and renders every section body through the same Markdown renderer. No report paragraph is copied into a component, summarized, or hidden behind an accordion.

The hero, navigation labels, figure captions, dashboard placeholders, evidence links, provenance explanation, and footer are interface copy around the manuscript. They do not replace manuscript content.

## Section map

| Manuscript section | Page anchor / rail label | Subsections rendered | Added presentation |
| --- | --- | --- | --- |
| 01 — Project Overview | `#overview` / Overview | Motivation; Research question; Dataset; Engineering approach; Key findings | Editorial hero and restrained report tables |
| 02 — Data & Methodology | `#pipeline` / Data & Pipeline | Data sources and reporting coverage; Pipeline architecture; Data-quality findings; Analytical measures; Zero-minute records; Reproducibility and testing | Five-stage source-to-report architecture figure |
| 03 — Data Enrichment & Validation | `#modeling` / Enrichment & Modeling | Analytical dimensions; Duration classification; Operational-code enrichment; Encoding recovery; Enrichment results; Analytical reconciliation; Power BI safeguards; Overlapping groups; Validation and reproducibility | Incident-weighted enrichment coverage figure |
| 04 — Analytical Findings | `#findings` / Findings | Three primary findings; EFO monthly rank change; monthly Bus/Streetcar line variation; qualified LRT comparison; Power BI reporting model | Three clearly pending Power BI page placements; one supporting native evidence figure per primary finding |
| 05 — Discussion & Limitations | `#limitations` / Limitations | Measurement validity; Cross-mode comparability; Reporting coverage; Incident identity; Code interpretation; Long-duration sensitivity; Temporal inference; Scope of inference | Text-led treatment; no added chart |
| 06 — Conclusion & Next Steps | `#conclusion` / Conclusion | Project outcomes; five next steps; Conclusion | Restrained ending flowing into provenance |

## Visual hierarchy and placeholders

- The hero's right column is reserved for the verified Power BI dashboard. It lists the prepared model scope but does not imply that report pages are finished.
- Section 04 reserves placements for Frequency vs Duration, Concentration & Persistence, and Explore the Records. Each explicitly states that no screenshot or interaction has been fabricated.
- Native figures are limited to the pipeline, enrichment change, Bus duration concentration, Subway zero-minute composition, and Subway monthly leaders. They support specific manuscript claims and remain secondary to the planned Power BI report.
- The `IA` author mark is an intentional profile-image placeholder. No portrait or stock photograph is invented.
- `Website` in the project navigation is a labeled non-link until a portfolio URL is supplied. `Dashboard` targets the hero placeholder until an approved report destination exists.

## Preserved v0.1 decisions

The red, black, and warm-white palette; serif display typography; supporting sans serif; thin rules; section numbering; sticky top bar; left report rail; central reading column; understated tables; uppercase labels; author treatment; source-by-mode provenance; and authored footer remain recognizable from v0.1. Spacing and hero proportions are tightened so the KPI values fit inside a normal desktop first viewport.

## Content-integrity notes for review

- Publication correction: the LRT table now identifies January 23, 2026 as one date without recorded rows, not a record with a missing date. `reports/lrt_tracer_profile.json` records 267 observed dates and that absent date; `reports/curated_verification.json` reports zero invalid LRT dates. The table heading is “Count” because its rows mix record counts with one reporting-date count. Other references discuss missing dates as a general policy or correctly describe the reporting gap and remain unchanged.
- The unmatched opening bold marker in the Power BI status paragraph was removed without changing its wording. Dashboard and personal website placeholders remain approved for initial publication.
- Interface copy keeps the v0.1 editorial title treatment because the implementation brief explicitly preferred it. The exact manuscript title and subtitle remain the report's authoritative framing and are reflected in the project label and deck.

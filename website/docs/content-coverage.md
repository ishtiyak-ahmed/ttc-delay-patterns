# Content coverage and editorial audit

## Source and preservation

Source: `TTC_Codex_Website_Handoff.zip`, `content/ttc-case-study.md`, a reconstructed six-section narrative supplied by the author. It is not certified as a verbatim copy of the earlier WritingBlocks. The complete maintained narrative is `../content/ttc-case-study.md`; `src/App.tsx` renders all six sections from that file, not shortened component copy. Frontmatter, the internal editorial note and publication implementation notes are not published as article paragraphs; their status, attribution and source requirements are represented in the hero/footer and this audit.

Rendering order is unchanged. Illustration markers are replaced by native figures or explicitly pending screenshot placements. All substantive paragraphs, lists, tables, interpretations and caveats are retained except the factual/status corrections listed below. No operational family is inferred.

Original supplied narrative SHA-256: `c4666e72947cf7da60d43fac01ce58402bb7881cc4046a9049a8fb89a2ef9cfb`. This identifies the pre-correction source within the handoff ZIP.

## Section and subsection coverage

| Source section / major subsection | Page anchor / implementation | Evidence or handling |
| --- | --- | --- |
| Title, subtitle, research question, author, observation period and project status | Hero; `#overview` research-question block; `#findings`; footer | Headline adapted for editorial design; original source title retained in Markdown. Author/status pending review. |
| 01 Project Overview — The question behind the analysis | `#overview`, `Narrative` | Full personal motivation, pipeline explanation, three findings and denominator/impact qualifications retained. `finding-links` connects to all three findings. |
| 02 Data & Methodology — Sources and observation windows | `#sources-and-observation-windows` | Complete four-mode table; 608-date versus 267/268-date coverage; reporting completeness caveat. Source links and snapshot hashes at `#sources`. |
| 02 — A reproducible pipeline | `#a-reproducible-pipeline`, `Architecture` | All five prose stages plus real semantic HTML flow. Original values remain traceable; no ingestion at website build time. |
| 02 — Data-quality decisions | `#data-quality-decisions` | Full issue table, corrected duplicate terminology and LRT gap, uncapped durations and zero/NULL distinction. |
| 02 — Analytical definitions and validation | `#analytical-definitions-and-validation`, validation strip | Complete definitions and limitations. 76 at analytical checkpoint versus 79 with three website-adapter tests. |
| 03 Data Enrichment & Validation — Making operational codes interpretable | `#making-operational-codes-interpretable`, `EnrichmentFigure` | Mode/code identity; initial 133,713 / 176,004; 56 strictly bounded recoveries; resulting 165,124 / 176,004. |
| 03 — What remained unresolved—and why that matters | `#what-remained-unresolved-and-why-that-matters`, recovery strip | Full 137-entry / 10,880-record explanation, fallback, unchanged totals and descriptions-not-causes caveat. |
| 04 Dashboard & Key Findings — reporting introduction | `#findings` | Three planned page names retained; author-reported Desktop validation distinguished from unverified screenshot/publication state. |
| 04 — Finding 1: Long Bus records dominate accumulated minutes | `#finding-1-long-bus-records-dominate-accumulated-minutes`, `BusConcentration`, `CodeComparison` | Full concentration, code comparison, monthly persistence, overlap/intersection/union, interpretation and follow-up requirements. |
| 04 — Finding 2: Zero-minute records shape Subway counts | `#finding-2-zero-minute-records-shape-subway-counts`, `ZeroComposition`, `MonthlyZeros` | Overall zero share, MUIS totals and share, actual 20 monthly values with accessible table, interpretation and passenger-impact warning. |
| 04 — Finding 3: Monthly leaders depend on the metric | `#finding-3-monthly-leaders-depend-on-the-metric`, `MonthlyLeaders` | Twenty actual months and YU/BD counts/minutes; all-label leader evaluation; Bus EFO/MFDV persistence; LRT near-tie caution. |
| 04 — Synthesis | `#synthesis` | All three analytical lenses and the non-reliability-ranking qualification retained. |
| 05 Discussion & Limitations — From descriptive evidence to investigation priorities | `#from-descriptive-evidence-to-investigation-priorities` | Complete three-row priority/evidence table and bounded framing. |
| 05 — Boundaries of interpretation | `#boundaries-of-interpretation` | Exposure denominators, passenger impact, causal limits, coverage, logging conventions and LRT weekday uncertainty retained. |
| 06 Conclusion & Next Steps | `#conclusion` | All four synthesis paragraphs and three extensions retained: service exposure, operational definitions/context and passenger-impact information. No extensions implemented. |
| Publication metadata / source references | `#sources`, footer and provenance disclosure | Exact portal/resource URLs from repository manifest; selected resource IDs/hashes; unofficial attribution; no invented public dashboard URL. |
| Three Power BI illustration markers | `PendingDashboard` after each finding | Each named placement is explicitly pending; no fabricated screenshot, active embed button or public-report claim. |

## Numerical claim traceability

The adapter validates the bundle hashes before reading its typed JSON. All figures use `src/data/evidence.json`; the full source selection and input/adapter hashes are embedded. Underlying SQL remains unchanged.

| Claim(s) retained in narrative | Authoritative evidence | Website implementation |
| --- | --- | --- |
| 176,004 records; 2,740,515 minutes; 49,830 zeros; per-mode totals/windows | `results/power_bi/fact_month.csv`, `dim_mode.csv`; `sql/analysis/coverage.sql` | Hero, full methodology table, sources; `evidence.totals/modes` |
| 608 dates for three modes; LRT 267/268 dates; Jan 23 gap | `dim_mode.csv`, `reporting_gaps.csv` | Methodology and explicit corrected gap row |
| 770 candidate records / 383 groups / 387 excess; 655 weekday conflicts; 1,777 missing lines; one missing code; no invalid dates/durations | `docs/cleaning_validation_rules.md`, actual read-only curated audit | Full quality table and caveats; no dropped rows |
| >60 Bus: 4,209 / 102,257 = 4.12%; 853,656 / 2,163,102 = 39.46% | `fact_duration.csv`, `dim_duration_band.csv`, temporal report | Hero + Figure 01A; same 0–100% scale |
| MFDV 7,288 / 871,387; EFO 18,178 / 251,714; respective mode shares | `fact_code.csv`, `dim_code.csv` | Figure 01B; full numerator/denominator text |
| MFDV minute leader 20/20; monthly share 29.05–50.33%; EFO count leader first 15 months | Temporal report; month-level `fact_code.csv` | Full finding paragraphs; evidence contains actual monthly MFDV totals |
| Intersection 3,775 / 777,169; union 7,722 / 947,874, 43.82% of Bus minutes | Disjoint `fact_duration.csv` cohorts; temporal report | Full finding paragraph + visible overlap warning |
| Subway zeros 29,669 / 45,475 = 65.24%; month range 59.67–72.75% | `fact_month.csv` | Figures 02A/02B; twenty actual values, table alternative |
| MUIS 4,217 / 4,263 = 98.92%; 369 recorded minutes | `fact_code.csv`, `dim_code.csv` | Complete finding-2 paragraph |
| YU count leader 20/20; BD minute leader March 2025, March/April 2026; YU other 17 | `fact_line.csv`, `dim_line.csv`; temporal report | Figure 03 with actual YU/BD totals and explicit exceptions |
| Enrichment 133,713 → 165,124 records; 75.97 → 93.82%; gain 31,411 / 17.85pp | `dim_code.csv`, `fact_code.csv`, `config/code_description_recovery.json` | `EnrichmentFigure`, complete enrichment prose |
| 342 described / 479 dimension entries; 137 unresolved / 10,880 records | Bundle + recovery/fallback reports | Enrichment prose and caveats |
| 76 tests at baseline; three additional adapter tests | Actual unittest run in implementation | Methodology validation strip; root README / validation report |

## Explicit factual / presentation edits to supplied text

1. Replaced the erroneous “one LRT record without a usable internal date” with the documented reporting-date gap. Actual selected data has zero missing/invalid incident dates; absence is not a fabricated record or zero-delay day.
2. Reworded duplicate-candidate table row to 770 records in 383 groups, including 387 excess occurrences. No deduplication occurred.
3. Described 56 encoding recoveries as the exact reversible, checksum-bound en-dash process, not discretionary rewriting or inferred meanings.
4. Qualified Power BI status using the author's prior report of model validation, while stating that no PBIX/screenshots/public URL are supplied for independent verification.
5. Converted implementation-facing “website should / interface should” sentences into statements describing this implementation, without dropping the substance.
6. Kept the 76-test checkpoint statement and separately exposed the current 79-test total.
7. Adapted the hero title and introductory deck for editorial presentation; retained the full research question, original title in content, and every substantive section.

## Editorial approval still required

- Reconcile reconstructed wording with original WritingBlocks if supplied later. This implementation cannot certify verbatim identity to unavailable drafts.
- Review personal voice (including the university-student introduction) and the new hero headline; no biographical verification is claimed.
- Confirm current Desktop/report status and provide approved screenshots/public link if desired. Do not substitute placeholders for proof of a finished report.
- Confirm source-repository public access before resume publication. No visibility change, deployment, PR, merge or push has occurred.
- Supplied design/handoff files are retained as provenance; their earlier “dashboard not built” wording is superseded by the qualified author-reported status above.

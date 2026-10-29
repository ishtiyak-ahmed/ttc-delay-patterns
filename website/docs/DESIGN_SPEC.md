# TTC Delay Patterns — Website Design Specification

## Product objective
Build a **standalone, publication-quality analytical case study** that can be linked directly beside the TTC project on a resume. It is not a personal portfolio homepage, a PDF reproduction, a Power BI dashboard clone, or a generic SaaS landing page. A recruiter should grasp the question and strongest result in 30 seconds; a hiring manager should understand decisions and implications in 3 minutes; a technical reviewer should be able to inspect the full six-section evidence in 10+ minutes.

## Visual identity: TTC Analytical Editorial
- Editorial data storytelling, informed by professional data journalism, with visible engineering credibility.
- Warm off-white `#F8F7F4`, charcoal `#22252B`, TTC-inspired red `#D71920`, muted slate blue `#39779B`, soft gray `#E2E2DF`, accessible secondary text `#5B616A`.
- **No orange or amber.** Use muted slate blue for **incident frequency**, deep red for **recorded minutes**, and neutral gray for context; this must be consistent in legends, captions, and charts. Red is also the page's identity color, so distinguish decorative red accents from quantitative encodings through context and clear labels. Consider a deeper red for charts if contrast requires it.
- This is an independent analysis, not official TTC branding. Do not use TTC logos or official-looking marks without appropriate rights; prefer original linework or transit-inspired geometry.
- Headings: editorial display serif or distinctive grotesk; body: highly readable sans-serif; numeric labels: tabular numerals. Use accessible web fonts or system fallbacks.
- No glassmorphism, giant gradients, excessive shadows, faux terminal UI, decorative dashboards, animated number counters, or gratuitous motion.

## Information architecture
1. Minimal site header: project title/monogram, jump to findings, methodology, GitHub, Power BI (only when published).
2. Hero: eyebrow `INDEPENDENT DATA ANALYSIS · TORONTO`, headline, concise thesis, author attribution, exact dataset period note, three context metrics (176,004 records; 2,740,515 minutes; four modes).
3. Prominent **featured evidence**: 4.12% versus 39.46% Bus long-duration share, clearly labeled and charted.
4. Complete six-section narrative from `content/ttc-case-study.md`, in order, without dropping tables, qualifications, or technical evidence.
5. Full-width findings illustrations; narrow readable prose column; medium-width methodology tables; wider charts.
6. Footer with author, independent-analysis notice, verified source/repository links, and last-updated/status.

## Section-by-section presentation
- **01 Overview:** narrative intro, research question, three finding teasers; avoid repeating hero metrics in giant cards.
- **02 Methodology:** source coverage table, five-stage architecture flow, compact quality issue table, 76-test validation fact. Mobile tables must remain readable, e.g. horizontal scroll with headers.
- **03 Enrichment:** 75.97% → 93.82% before/after graphic with 133,713 and 165,124 denominators; 56 reviewed repairs; 137 unresolved dimension entries; validation strip.
- **04 Findings:** largest section (~35–40% of vertical attention). Three numbered findings, each with a headline claim, evidence visualization, interpretation, and appropriately placed caveat. Bus concentration + `MFDV` overlap is one finding, not two additive impacts. Add three clearly labeled Power BI screenshot slots, not fabricated screenshot imagery.
- **05 Discussion:** investigation priorities table and compact limitations with explicit measure/coverage constraints.
- **06 Conclusion:** analytical synthesis, technical contribution, and three next-step extensions; end with GitHub and dashboard links when verified.

## Chart specifications and constraints
1. Bus long-duration: horizontal percent bars, **4.12% incident share** and **39.46% minute share**. Same 0–100 scale; direct numeric labels; not misleadingly scaled.
2. Bus code comparison: `EFO` **17.78% incidents / 11.64% minutes**, `MFDV` **7.13% incidents / 40.28% minutes**. Show two metrics explicitly; code labels are raw codes, not inferred causes. Include overlap warning for `MFDV` and >60 records.
3. Subway zeros: **29,669 / 45,475 = 65.24%** zero-minute share; `MUIS` **4,217 / 4,263 = 98.92%** zero. A zero means a source-reported zero, not missing and not proven zero passenger impact.
4. Monthly zeros and line leadership: fetch actual month-by-month data from `results/temporal_persistence/*.csv` or verified outputs. Do not invent 20 intermediate values. If not available, use a truthful qualitative timeline and reserve detailed chart.
5. Enrichment: **75.97% → 93.82%**, +31,411 covered records, +17.85 percentage points; same 0–100 scale.
6. All charts: titles state a claim; axis/denominator/unit and period are explicit; source notes; text alternatives or accessible data tables; no false precision; responsive labels.

## Interaction and accessibility
- Sticky desktop table of contents, compact mobile section navigation, working anchor links, visible focus states, skip-to-content link, semantic heading hierarchy.
- Reduced-motion support; no scroll-jacking. Responsive from 360px to wide desktop; max-width reading column about 68–76 characters.
- Prefer static native SVG for simple editorial charts; add interactive charting only when it improves comprehension. Accessible table fallback for key figures.
- All navigation and buttons must function. Avoid inert controls or placeholder external links that look active.

## Content integrity
- **Do not paraphrase away or replace the six sections.** Preserve full substantive content and caveats; presentation may be adapted into accessible tables, charts, or pull-quotes without losing claims.
- Source of truth is `content/ttc-case-study.md`, plus verified repository evidence. The older HTML prototype and prior PDF are not authoritative.
- Do not describe the Power BI dashboard as built or published; current work consists of exports, contract, and DAX definitions. Screenshots are pending.
- Do not present raw mode comparisons as exposure-adjusted reliability or minutes as passenger-minutes.
- Keep an editorial QA checklist that maps every source section/subheading to the implemented page.

## Suggested implementation
React + TypeScript + Vite + Tailwind CSS, or equivalent lightweight static build. Content can be MDX or structured Markdown with reusable chart components. No backend needed. Deploy to Vercel or comparable static hosting; choose domain only when user confirms. Organize assets and content so the case study can later be embedded in a broader portfolio without a rewrite.

## Acceptance criteria
- All six sections and substantive paragraphs represented.
- Exact headline numbers and denominators checked against repository outputs.
- No orange anywhere in site palette, charts, or gradients.
- Works at mobile, tablet, desktop widths; no clipped tables/charts.
- Proper focus/keyboard navigation, alt text, semantic sections.
- `npm run build`, type check, and lint pass; include commands/results in handoff.
- Clearly labeled pending Power BI visuals; no fake dashboard screenshots.
- A concise independent-project README and deployment instructions.
- Final screenshot-based visual QA for desktop and mobile.

# Codex implementation handoff

## Objective
Build the standalone TTC Delay Patterns case-study website from the accompanying content and design specification. This is a hiring-facing analytical publication, not a personal portfolio homepage.

## Read first, in order
1. `content/ttc-case-study.md` — authoritative assembled narrative and all six sections. **Note its editorial-source caveat:** comprehensive reconstruction, not confirmed verbatim text from previous WritingBlocks.
2. `docs/DESIGN_SPEC.md` — design system, page architecture, chart specs, constraints, acceptance tests.
3. Source repository evidence and verified CSVs (listed at end of case study). Prefer checked-in data over hardcoded monthly series.
4. Existing HTML prototype only as optional historical reference; do not copy its abbreviated narrative.

## Deliverables
- React/TypeScript static site with polished editorial design.
- Full six-section content, rendered with correct typography, tables, diagrams, and annotated native charts.
- Verified chart data with a small traceable data module and source notes.
- Three labeled Power BI screenshot placeholders that are easy to replace with real screenshots later.
- README explaining local run, build, deploy, content editing, and pending dashboard assets.
- Visual QA screenshots at 1440px desktop and 390px mobile, and a checklist showing each narrative subsection is present.

## Critical instructions
- Do not shorten or independently rewrite the case study into a marketing landing page.
- No orange/amber; red for minutes and slate blue for incident counts.
- Preserve source qualifiers and exact denominators; do not sum overlapping Bus populations.
- Never invent monthly data or operational causes.
- Don't claim that the final Power BI dashboard is published.
- The website and the data-pipeline GitHub README are **different deliverables**. Do not replace the analytical repository README with this long-form website copy.

## Suggested work sequence
1. Audit source content and repo data; write a source-to-page content map.
2. Implement responsive site shell, type scale, and navigation.
3. Render all six sections faithfully.
4. Implement native evidence charts using verified data.
5. Add placeholders, citations, accessibility, and responsive refinements.
6. Build, test, inspect screenshots, and report remaining issues.

## Editorial review gate
Before public launch, compare `content/ttc-case-study.md` to the original six WritingBlocks if those exact drafts can be exported. This bundle cannot certify verbatim reproduction. This is a review requirement, not permission to discard any current material.

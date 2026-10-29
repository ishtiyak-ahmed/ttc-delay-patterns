# Website v2 validation

This document records checks for the local implementation on `feature/case-study-website-v2`. It does not claim a public deployment, completed Power BI dashboard, real-device certification, or publication approval.

## Required checks

Run from the repository root:

```sh
python3 -B scripts/export_website_evidence.py --check
python3 -B -m unittest discover -s tests -q
npm --prefix website run typecheck
npm --prefix website run lint
npm --prefix website run build
```

The implementation also requires production-preview checks at representative desktop, tablet, and mobile widths for section navigation, first-viewport KPI visibility, table overflow, dashboard placeholders, direct hash navigation, keyboard focus, and page-level horizontal overflow.

## Content contract

- Exactly six numbered top-level manuscript sections render in order.
- `App.tsx` imports `ttc-case-study-v2.md`; it does not copy report section bodies into components.
- All report prose remains visible by default. Only supplementary snapshot provenance is expandable.
- Dashboard and portfolio destinations remain explicit placeholders until supplied.
- Existing analytical evidence remains a deterministic, hash-checked projection of the approved export bundle.

## Actual results — 2026-10-29

| Check | Result |
| --- | --- |
| Website evidence adapter | Pass; checked-in projection matches the approved export bundle |
| Python tests | 82 passing: 79 baseline tests plus three v2 content-contract tests |
| TypeScript type-check | Pass |
| ESLint | Pass |
| Vite production build | Pass; HTML, favicon, CSS and JavaScript emitted to ignored `website/dist/` |
| Git diff whitespace check | Pass |
| Privacy/credential pattern scan of changed text files | No personal machine paths, private-key markers, common GitHub token forms or AWS access-key forms found |
| Desktop 1440 × 1000 | No page-level horizontal overflow; all four KPI values end above 780px and are visible in the first viewport |
| Tablet 768 × 1024 | No page-level horizontal overflow; report rail and hero remain usable |
| Mobile 390 × 844 | No page or header overflow; tables retain keyboard-focusable horizontal scrolling |
| Direct hash navigation | `/#findings` loads and refreshes with the target section positioned below the sticky header |
| Page structure | One `h1`, six report sections, semantic heading progression, zero broken internal anchors |
| Browser console | No warnings or errors during inspected desktop/tablet states |

QA captures: `docs/qa/v2-desktop.jpg`, `docs/qa/v2-mobile.jpg`, and `docs/qa/v2-findings.jpg`. They show the production build, not Power BI screenshots. No live Vercel deployment, real device, screen reader, automated axe scan or cross-browser matrix is claimed.

## Known editorial items

The two publication issues are resolved with the author’s approval: the LRT table distinguishes one reporting-date gap from missing incident dates, and the unmatched bold marker was removed without rewriting the Power BI status paragraph. See `v2-content-coverage.md` for the evidence and exact scope. All 82 Python tests, evidence verification, type-check, lint and production build were rerun successfully before publication of the branch.

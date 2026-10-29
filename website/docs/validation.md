# First website implementation — validation

Date: 2026-10-28 (America/Toronto). Branch: `feature/case-study-website`, based on `c151470f5c76426062552f00cdcd7aa0924685a6`. No commit, push, PR, merge, hosting registration or deployment was performed.

## Results

| Check | Actual result |
| --- | --- |
| `python3 -B -m unittest discover -s tests -q` | 79 passing tests: all 76 prior tests plus three evidence-adapter tests |
| `python3 -B scripts/export_website_evidence.py --check` | Checked-in website evidence matches deterministic projection |
| Two in-memory evidence serializations | Byte-identical; source bundle protected by hashes |
| `npm ci` in website | Successful from lockfile; audit reported zero vulnerabilities; optional fsevents install-script approval warning noted below |
| `npm run typecheck` | Pass |
| `npm run lint` | Pass, no remaining warnings |
| `npm run build` | Pass; independently produces website/dist without Python, SQLite or private environment variables |
| Original analytical artifacts | All baseline hashes unchanged: raw/provenance, databases, SQL, original Python, tests, dictionaries, recovery config, governing documents, contracts, reports and approved exports |
| Existing-file changes | Only root .gitignore; all other implementation files are additive |
| Frozen-source reproduction recipe | Executed initializer → staging → independent staging verification → curated build → core → temporal → Power BI export in disposable databases/output directories |
| Reproduced analytical data | All ten CSVs and typed results.json byte-identical to approved bundle |
| Reproduced manifest | Differs only in curated artifact hash and input-manifest hashes; not represented as a byte-identical SQLite rebuild |
| Numerical checks | 176,004 incidents; 2,740,515 minutes; 49,830 zero-minute records; code description coverage 165,124 / 176,004 |
| Content coverage | Six sections and all original subsection headings retained; detailed claim/component map in content-coverage.md |
| Private data scan | No personal home paths or credential-pattern matches in new versionable text files; no raw/database/dependency/build artifacts staged |

The original narrative SHA-256 is recorded in the implementation audit command output and can be recalculated from the supplied ZIP. No claim of verbatim equivalence to unavailable WritingBlocks is made. The author-provided narrative and design/handoff references remain editorial inputs, subordinate to verified numerical evidence.

## Browser and accessibility checks actually performed

Used the local in-app browser against the running Vite site:

- Effective CSS viewports: **1440×1000**, **768×1024**, **390×844**, **360×800**. Overrides accounted for the in-app browser's zoom; dimensions were read from the actual DOM. No page-level horizontal overflow at these widths.
- Visually reviewed desktop hero, long-form findings, sticky navigation and mobile hero/data presentation. A Tailwind `contents` utility collision was observed and fixed by explicitly setting the sidebar's display to block; sticky positioning was then verified.
- All six story sections render; no broken internal anchors; one main landmark and one h1.
- Header and finding links navigate to actual sections. Keyboard Shift+Tab reaches the visible skip link; Enter navigates to main content. Visible focus styles are present.
- Monthly chart disclosure opens and exposes 20 actual data rows. Wide tables/charts use individually scrollable, keyboard-focusable containers instead of overflowing the page.
- Labels, units, numerators/denominators, shared percent scales and source notes accompany figures. Text/data alternatives distinguish metrics without relying solely on color.
- Palette text contrast spot checks: secondary text #5B616A is 5.33:1 on figure background; duration #B21D2A is 5.77:1; blue #39779B is 4.18:1 on figures and is used for large numeric text/graphics (above 3:1), with normal labels in charcoal/slate. On paper its contrast is 4.57:1. No orange/amber colors are used.
- Browser console check found no warning/error entries at inspection.
- Screenshots retained in qa/: desktop.png, desktop-findings.png, mobile.png, mobile-data.png. These are in-app captures, not real-device screenshots or Power BI visuals.

## Commands

From repository root:

```sh
python3 -B scripts/export_website_evidence.py
python3 -B scripts/export_website_evidence.py --check
python3 -B -m unittest discover -s tests -q
npm --prefix website ci
npm --prefix website run typecheck
npm --prefix website run lint
npm --prefix website run build
npm --prefix website run dev -- --port 5173
```

The full frozen-source commands are in the root README; they were executed using temporary outputs. Acquisition and metadata discovery were not run. Relative links in the new READMEs were checked locally. The official data licence destination was checked through the City portal and corrected to `https://open.toronto.ca/open-data-licence/`.

## Limits and remaining decisions

- No Windows Power BI execution, PBIX inspection, live dashboard interaction or screenshot validation was possible here. Status is explicitly author-reported, not independently verified publication.
- No public website/dashboard URL exists in this implementation. GitHub public accessibility, Vercel configuration on an account and deployed behavior remain unverified. No deployment was attempted.
- No real-device, screen-reader, full cross-browser suite, automated axe scan or Lighthouse performance score is claimed. Keyboard/DOM/contrast checks and visual inspection are bounded evidence, not a complete accessibility certification.
- npm ci emits a warning about an unapproved optional macOS fsevents install script. No approval/security setting was changed. Installation and production/type/lint checks still pass.
- Python venv/pip setup is documented using the existing runtime/dependency interface; a fresh Python environment/network installation was not repeated. Core tests and analysis require no third-party Python dependency.
- Screenshot assets, source wording/personal voice, hero headline and final public publication decisions require author review. Original narrative is reconstructed; do not present it as certified verbatim source text.
- A software/content licence is not selected on the author's behalf. Official data attribution is included separately.
- Acquisition/provenance producer privacy changes, source-update automation, new inferred code families and analytical restructuring are deliberately deferred.

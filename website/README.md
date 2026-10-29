# TTC Delay Patterns — Version 2 case study

React + TypeScript + Vite + Tailwind. Version 2 preserves the v0.1 editorial visual system while rendering the finalized six-section manuscript from `content/ttc-case-study-v2.md`. It includes semantic tables, selected native evidence figures, and explicit placeholders for the unfinished Power BI dashboard assets. No backend, credentials, SQLite connection or Python process is required at build/deploy time.

## Local development

From this directory, with Node 22.12+ (or Vite's supported Node 20.19 line):

```sh
npm ci
npm run dev
```

Open Vite's printed localhost URL. Production checks:

```sh
npm run typecheck
npm run lint
npm run build
npm run preview
```

The npm lockfile is tracked. `node_modules/`, `dist/`, `.vercel/`, coverage and build caches are ignored. No API keys or environment variables are required. External fonts and analytics are not used.

## Content and evidence

- `content/ttc-case-study-v2.md` is the authoritative report manuscript. `src/App.tsx` renders every section body directly from that file and adds interface labels and figures around it. No raw HTML execution is enabled in Markdown.
- `src/App.tsx` keeps the v0.1 hero, section rail, evidence area, footer, and editorial hierarchy. The Power BI placeholders are deliberate: no dashboard image, embed, or public report URL has been supplied.
- `src/data/evidence.json` is a deterministic, small projection of the checked-in approved export bundle. It records selection, raw hashes, bundle hashes and adapter hash. No values are fetched from a live data feed in the browser.
- `docs/v2-content-coverage.md` maps the finalized manuscript sections to the v2 implementation and records remaining asset placeholders. `docs/v2-validation.md` records current checks and limits. The v0.1 audit and supplied design/handoff references remain preserved separately.

From the repository root:

```sh
python3 -B scripts/export_website_evidence.py --check
python3 -B -m unittest discover -s tests -v
```

To inspect a future changed bundle without replacing reviewed evidence:

```sh
python3 -B scripts/export_website_evidence.py --output /tmp/ttc-website-candidate-evidence.json
```

The adapter refuses a differing existing output. Review the candidate and source checksums before explicitly replacing the checked-in evidence; source CSVs are never changed by the adapter. It uses compatible additive measures, existing named-label eligibility and tie-preserving leader comparisons. It adds no cleaning, imputation, inferred descriptions or exposure denominators.

## Vercel deployment readiness

Do not deploy until the author approves the content, design and publication status.

| Setting | Value |
| --- | --- |
| Repository root directory | `website` |
| Framework preset | Vite |
| Install command | `npm ci` |
| Build command | `npm run build` |
| Output directory | `dist` |
| Environment variables | None |
| Node.js version | 24.x (set explicitly in Vercel project settings) |
| Include source files outside Root Directory | Off; this app is self-contained |

The app uses same-page anchor navigation, so it needs no client-route rewrite configuration. Node 24.x is supported by Vercel and satisfies the installed Vite requirements; local checks used Node 26.7.0, so the first Vercel build remains a hosting-environment check. No GitHub workflow, hosting registration or deployment has been created. Public website/dashboard URLs are not invented.

### Exact deployment steps — only after publication approval

1. Approve the editorial baseline and any remaining dashboard placeholders. Authorize pushing the reviewed website branch/commit to the existing GitHub repository; nothing is automatically pushed by local build commands.
2. In Vercel, select **Add New → Project**, connect GitHub, and import the existing `ishtiyak-ahmed/ttc-delay-patterns` repository. Grant repository access only as needed. Importing/deploying is a publication action: do not perform this during local review.
3. Set **Root Directory** to `website`, **Framework Preset** to Vite, and the install/build/output/Node settings above. Do not set the output directory to the repository root or enable outside-root sources. No Python command, database, pipeline regeneration or environment secret is needed.
4. Deliberately select the approved production branch/commit. `main` currently does not contain this website; do not assume its default deployment will include the site. Review automatic Git deployment behavior before connecting/pushing future changes.
5. After approval, deploy and verify `/`, `/#overview`, `/#findings`, and `/#conclusion` by direct opening and refresh. Check all six sections, local assets, narrow-screen charts and official source links. Navigation is hash-based; there are no application routes such as `/findings` and no route rewrites are required.
6. Confirm the chosen deployment is publicly viewable without Vercel sign-in before adding its stable production URL or custom domain to the resume. A private GitHub repository can remain private; its footer link will still require repository permission.

Only `dist/` is served: HTML, CSS, JavaScript (including the maintained narrative and small aggregated evidence projection), and the favicon. Source docs, QA screenshots, raw CSVs, databases, approved analytical CSV bundles and Python code are not copied into it. Visitors need JavaScript enabled. Once hosted, the site remains available without the author's computer running.

Reference: [Vercel Vite deployment](https://vercel.com/docs/frameworks/frontend/vite), [build/root-directory settings](https://vercel.com/docs/builds/configure-a-build), and [supported Node versions](https://vercel.com/docs/functions/runtimes/node-js/node-js-versions). No account-side configuration or actual hosted deployment has yet been verified.

## Pending author decisions

Review the finalized manuscript in context, the retained editorial hero headline, dashboard and author-photo placeholders, and eventual personal-website and Power BI URLs. GitHub visibility/access should be checked before using the site as a recruiter-facing link. The source data attribution is separate from a software/content licence; no software licence was selected for the author. No TTC logos, fabricated dashboards or inferred broad operational families are used.

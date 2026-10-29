import { useEffect, useState } from 'react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import narrative from '../content/ttc-case-study-v2.md?raw'
import evidence from './data/evidence.json'
import { fmt } from './format'
import { Architecture, BusConcentration, EnrichmentFigure, MonthlyLeaders, ZeroComposition } from './Charts'

const repositoryUrl = 'https://github.com/ishtiyak-ahmed/ttc-delay-patterns'
const navigation = [
  ['overview', 'Overview'],
  ['pipeline', 'Data & Pipeline'],
  ['modeling', 'Enrichment & Modeling'],
  ['findings', 'Findings'],
  ['limitations', 'Limitations'],
  ['conclusion', 'Conclusion'],
] as const

const sections = narrative.split(/\n# (?=0[1-6] — )/).slice(1).map((part, index) => ({
  id: navigation[index][0],
  title: part.split('\n')[0].replace(/^0[1-6] — /, ''),
  body: part.slice(part.indexOf('\n') + 1).replace(/\n---\s*$/, '').trim(),
}))

const slug = (value: string) => value.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '')

function DashboardPlaceholder({ page, hero = false }: { page?: number; hero?: boolean }) {
  const names = ['Frequency vs Duration', 'Concentration & Persistence', 'Explore the Records']
  const Heading = hero ? 'h2' : 'h4'
  return <figure className={hero ? 'dashboard-preview hero-dashboard' : 'dashboard-preview'} id={hero ? 'dashboard' : undefined}>
    <div className="dashboard-frame" aria-label="Power BI dashboard asset placeholder">
      <div className="dashboard-toolbar"><span>Power BI</span><span>Verified asset pending</span></div>
      <div className="dashboard-canvas">
        <span className="dashboard-mark" aria-hidden="true">BI</span>
        <div>
          <span className="figure-kicker">{hero ? 'Primary project deliverable' : `Planned report page ${String(page).padStart(2, '0')}`}</span>
          <Heading>{hero ? 'Dashboard preview reserved.' : names[(page ?? 1) - 1]}</Heading>
          <p>{hero
            ? 'The verified Power BI dashboard will appear here after its visuals and interactions have been completed and validated.'
            : 'This report placement is reserved for a verified Power BI screenshot. No dashboard image or interaction has been fabricated.'}</p>
        </div>
      </div>
      <div className="dashboard-tabs" aria-label="Planned Power BI pages">{names.map((name, index) => <span className={page === index + 1 ? 'active' : ''} key={name}>{name}</span>)}</div>
    </div>
    <figcaption>{hero ? 'Prepared model: 10 reporting tables · 13 one-to-many relationships · 54 DAX measures. Interactive pages remain to be completed and validated.' : 'Power BI remains the intended primary visual analytical deliverable; the surrounding report preserves the SQL-verified evidence in the meantime.'}</figcaption>
  </figure>
}

function SectionFigure({ heading }: { heading: string }) {
  if (heading === 'Pipeline architecture') return <Architecture />
  if (heading === 'Enrichment results') return <EnrichmentFigure />
  if (heading === 'Finding 1 — Bus delay minutes are concentrated in long-duration records') return <><DashboardPlaceholder page={1} /><BusConcentration /></>
  if (heading === 'Finding 2 — Zero-minute records dominate Subway incident frequency') return <><DashboardPlaceholder page={2} /><ZeroComposition /></>
  if (heading === 'Finding 3 — Subway line leadership differs by measure and month') return <><DashboardPlaceholder page={3} /><MonthlyLeaders /></>
  return null
}

function Narrative({ body }: { body: string }) {
  return <ReactMarkdown remarkPlugins={[remarkGfm]} components={{
    h2: ({ children }) => {
      const heading = String(children)
      return <><h3 id={`sub-${slug(heading)}`}>{children}</h3><SectionFigure heading={heading} /></>
    },
    h3: ({ children }) => <h4 id={`sub-${slug(String(children))}`}>{children}</h4>,
    table: ({ children }) => <div className="table-scroll" role="region" aria-label="Case-study evidence table" tabIndex={0}><table>{children}</table></div>,
    a: ({ href, children }) => <a href={href}>{children}</a>,
  }}>{body}</ReactMarkdown>
}

export default function App() {
  const [active, setActive] = useState('overview')
  useEffect(() => {
    const observer = new IntersectionObserver(entries => {
      const visible = entries.find(entry => entry.isIntersecting)
      if (visible) setActive(visible.target.id)
    }, { rootMargin: '-12% 0px -65% 0px' })
    document.querySelectorAll('.story-section').forEach(section => observer.observe(section))
    const target = document.getElementById(window.location.hash.slice(1))
    if (target) requestAnimationFrame(() => target.scrollIntoView())
    return () => observer.disconnect()
  }, [])

  return <>
    <a className="skip-link" href="#main">Skip to the case study</a>
    <header className="site-header"><div className="header-inner">
      <a href="#top" className="wordmark" aria-label="TTC Delay Patterns, back to top"><span className="project-mark" aria-hidden="true">T</span><span><span className="ttc-word">TTC</span> <b>Delay Patterns</b></span></a>
      <nav aria-label="Project navigation"><span className="pending-link" aria-label="Personal website link pending" title="Personal portfolio URL pending">Website</span><a href="#overview">Report</a><a href="#dashboard">Dashboard</a><a href={repositoryUrl}>GitHub <span aria-hidden="true">↗</span></a></nav>
    </div></header>
    <main id="main">
      <section className="hero" id="top" aria-labelledby="site-title">
        <div className="hero-meta"><span>Independent data analysis · Toronto</span><span className="draft-note">Version 2 · editorial review</span></div>
        <div className="hero-grid">
          <div className="hero-copy">
            <p className="issue-number">Understanding TTC delay patterns / 01</p>
            <h1 id="site-title">TTC delay patterns.<br /><em>Frequency is only<br className="desktop-break" /> half the story.</em></h1>
            <p className="hero-deck">An analysis of <strong>176,004 TTC incident records</strong> reveals how incident frequency, accumulated delay duration, and monthly rankings produce different views of reported disruptions.</p>
            <div className="byline"><span className="byline-mark" aria-label="Author photo placeholder">IA</span><span><strong>Ishtiyak Ahmed</strong><small>Python · SQLite · SQL · Power BI</small></span></div>
            <a className="read-link" href="#overview">Read the investigation <span aria-hidden="true">↓</span></a>
          </div>
          <DashboardPlaceholder hero />
        </div>
        <dl className="context-strip"><div><dt>Recorded incidents</dt><dd>{fmt(evidence.totals.recorded_incidents)}</dd></div><div><dt>Recorded delay minutes</dt><dd>{fmt(evidence.totals.recorded_delay_minutes)}</dd></div><div><dt>Source modes</dt><dd>04 <span>Bus / Subway / Streetcar / LRT</span></dd></div><div className="period-context"><dt>Observation window</dt><dd>Jan 2025–Aug 2026<span>LRT begins Dec 7, 2025. Coverage varies.</span></dd></div></dl>
      </section>

      <div className="story-layout">
        <aside className="contents"><div className="contents-inner"><p className="figure-kicker">In this report</p><nav aria-label="Report sections">{navigation.map(([id, label], index) => <a key={id} href={`#${id}`} aria-current={active === id ? 'location' : undefined}><span>{String(index + 1).padStart(2, '0')}</span>{label}</a>)}</nav><div className="contents-note">Recorded activity.<br />Not passenger impact.<br />Not a reliability ranking.</div></div></aside>
        <article className="story">{sections.map((section, index) => <section className="story-section" id={section.id} key={section.id} aria-labelledby={`${section.id}-title`}>
          <div className="section-heading"><span className="section-index">{String(index + 1).padStart(2, '0')}</span><div><p className="figure-kicker">{['The question', 'The pipeline', 'The model', 'The evidence', 'The boundaries', 'The contribution'][index]}</p><h2 id={`${section.id}-title`}>{section.title}</h2></div></div>
          <div className="prose"><Narrative body={section.body} /></div>
        </section>)}</article>
      </div>

      <section className="sources-section" id="sources" aria-labelledby="sources-title"><div className="sources-heading"><span className="figure-kicker">Evidence &amp; provenance</span><h2 id="sources-title">Follow the tracks.</h2><p>Official source snapshots, retained checksums, documented validation and reproducible SQL support the report. Observed dates do not prove complete reporting.</p></div>
        <nav className="artifact-links" aria-label="Project evidence"><a href="#pipeline">Methodology</a><a href="#modeling">Validation &amp; enrichment</a><a href="#dashboard">Power BI experience</a><a href={repositoryUrl}>GitHub repository ↗</a></nav>
        <div className="source-list">{evidence.modes.map(mode => <div key={mode.source_mode}><strong>{mode.source_mode === 'lrt' ? 'LRT' : mode.source_mode[0].toUpperCase() + mode.source_mode.slice(1)}</strong><span>{fmt(mode.recorded_incidents)} records · {mode.first_observed_date}–{mode.last_observed_date}</span><a href={mode.portal_url}>Official dataset ↗</a><a href={mode.source_url}>Resource ↗</a></div>)}</div>
        <details className="provenance-details"><summary>Inspect selected snapshot provenance</summary><p>The website uses a deterministic projection of the approved analytical export bundle. It does not query a live feed or run the pipeline during deployment.</p><p>Bundle manifest SHA-256: <code>{evidence.provenance.bundle_manifest_sha256}</code></p>{evidence.provenance.selection.snapshots.map(snapshot => <p key={snapshot.mode}><strong>{snapshot.mode}</strong> · Resource <code>{snapshot.resource_id}</code><br />Raw SHA-256 <code>{snapshot.sha256}</code></p>)}</details>
      </section>
    </main>
    <footer className="site-footer"><div><span className="figure-kicker">An independent case study by</span><strong>Ishtiyak Ahmed</strong><p>Not affiliated with or endorsed by the Toronto Transit Commission. Contains information licensed under the Open Government Licence – Toronto.</p></div><div><a href={repositoryUrl}>View the repository ↗</a><p>Repository access may require permission.<br />Personal website URL: pending.<br />Power BI public link: not supplied.</p><a href="https://open.toronto.ca/open-data-licence/">Source data licence ↗</a></div><a className="back-top" href="#top">Back to top ↑</a></footer>
  </>
}

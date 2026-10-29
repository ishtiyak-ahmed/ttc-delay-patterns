import { useEffect, useState } from 'react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import narrative from '../content/ttc-case-study.md?raw'
import evidence from './data/evidence.json'
import { fmt } from './format'
import { Architecture, BusConcentration, CodeComparison, EnrichmentFigure, MonthlyLeaders, MonthlyZeros, ZeroComposition } from './Charts'

const repo = 'https://github.com/ishtiyak-ahmed/ttc-delay-patterns'
const navigation = [
  ['overview', 'Overview'], ['methodology', 'Data & methodology'], ['enrichment', 'Enrichment & validation'],
  ['findings', 'Dashboard & findings'], ['limitations', 'Discussion & limitations'], ['conclusion', 'Conclusion & next steps'],
]
const sections = narrative.split(/\n## (?=0[1-6] — )/).slice(1).map((part, i) => ({
  id: navigation[i][0], title: part.split('\n')[0].replace(/^0[1-6] — /, ''),
  body: part.slice(part.indexOf('\n') + 1).split('\n---\n')[0].trim(),
}))
const slug = (s: string) => s.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '')

function PendingDashboard({ number }: { number: number }) {
  const name = ['Frequency vs Duration', 'Concentration & Persistence', 'Explore the Records'][number - 1]
  return <figure className="pending-dashboard">
    <span className="figure-kicker">Power BI / {String(number).padStart(2, '0')} / Pending asset</span>
    <h3>{name}</h3>
    <p>A place for the author’s validated report screenshot. No dashboard image or public embed has been supplied.</p>
    <figcaption>Native evidence figures above are working visualizations of the verified exports. This placement is not a dashboard preview.</figcaption>
  </figure>
}

function Illustration({ marker }: { marker: string }) {
  if (marker.includes('POWER BI PLACEHOLDER')) return <PendingDashboard number={Number(marker.match(/PLACEHOLDER (\d)/)?.[1])} />
  if (marker.includes('FIGURE 1A')) return <BusConcentration />
  if (marker.includes('FIGURE 1B')) return <CodeComparison />
  if (marker.includes('FIGURE 2A')) return <ZeroComposition />
  if (marker.includes('FIGURE 2B')) return <MonthlyZeros />
  if (marker.includes('FIGURE 3:')) return <MonthlyLeaders />
  if (marker.includes('Five-stage')) return <Architecture />
  if (marker.includes('Before/after')) return <EnrichmentFigure />
  if (marker.includes('Hero summary')) return <div className="finding-links"><span className="figure-kicker">Three lenses on the same question</span><a href="#finding-1-long-bus-records-dominate-accumulated-minutes">01 / Duration concentration <span>↓</span></a><a href="#finding-2-zero-minute-records-shape-subway-counts">02 / Zero-minute composition <span>↓</span></a><a href="#finding-3-monthly-leaders-depend-on-the-metric">03 / Monthly persistence <span>↓</span></a></div>
  if (marker.includes('Three-step')) return <aside className="validation-strip"><span>Detect the corrupted dash</span><b aria-hidden="true">→</b><span>Recover only reviewed text</span><b aria-hidden="true">→</b><span>Reconcile unchanged totals</span></aside>
  return <aside className="validation-strip"><strong>Validated, not assumed.</strong><span>79 automated tests in this implementation; 76 at the analytical checkpoint. Snapshot identity, source preservation and compatible totals are checked separately from interpretation.</span></aside>
}

function Narrative({ body }: { body: string }) {
  return <>{body.split(/(\*\*\[(?:VISUAL|NATIVE FIGURE|POWER BI PLACEHOLDER)[\s\S]*?\]\*\*)/g).map((part, index) => part.startsWith('**[')
    ? <Illustration key={index} marker={part} />
    : <ReactMarkdown key={index} remarkPlugins={[remarkGfm]} components={{
      h3: ({ children }) => <h3 id={slug(String(children))}>{children}</h3>,
      table: ({ children }) => <div className="table-scroll" role="region" aria-label="Case-study evidence table" tabIndex={0}><table>{children}</table></div>,
      a: ({ href, children }) => <a href={href}>{children}</a>,
    }}>{part}</ReactMarkdown>)}</>
}

export default function App() {
  const [active, setActive] = useState('overview')
  useEffect(() => {
    const observer = new IntersectionObserver(entries => {
      const visible = entries.find(entry => entry.isIntersecting)
      if (visible) setActive(visible.target.id)
    }, { rootMargin: '-12% 0px -65% 0px' })
    document.querySelectorAll('.story-section').forEach(section => observer.observe(section))
    return () => observer.disconnect()
  }, [])
  return <>
    <a className="skip-link" href="#main">Skip to the case study</a>
    <header className="site-header"><div className="header-inner">
      <a href="#top" className="wordmark" aria-label="TTC Delay Patterns, back to top"><span className="project-mark" aria-hidden="true">T</span><span>TTC <b>Delay Patterns</b></span></a>
      <nav aria-label="Primary"><a href="#findings">Findings</a><a href="#methodology">Methodology</a><a href={repo}>GitHub <span aria-hidden="true">↗</span></a></nav>
    </div></header>
    <main id="main">
      <section className="hero" id="top" aria-labelledby="site-title">
        <div className="hero-meta"><span>Independent data analysis · Toronto</span><span className="draft-note">First implementation · editorial review pending</span></div>
        <div className="hero-grid">
          <div className="hero-copy"><p className="issue-number">A study in how we measure disruption / 01</p>
            <h1 id="site-title">TTC delay patterns.<br /><em>Frequency is only<br className="desktop-break" /> half the story.</em></h1>
            <p className="hero-deck">The most frequent incident is not always the largest contributor to recorded delay. A source-preserving investigation of four TTC modes, two measures, and the difference between them.</p>
            <div className="byline"><span className="byline-mark" aria-hidden="true">IA</span><span><strong>Ishtiyak Ahmed</strong><small>Python · SQLite · SQL · Power BI reporting assets</small></span></div>
            <a className="read-link" href="#overview">Read the investigation <span aria-hidden="true">↓</span></a>
          </div>
          <BusConcentration featured />
        </div>
        <dl className="context-strip"><div><dt>Recorded incidents</dt><dd>{fmt(evidence.totals.recorded_incidents)}</dd></div><div><dt>Recorded delay minutes</dt><dd>{fmt(evidence.totals.recorded_delay_minutes)}</dd></div><div><dt>Source modes</dt><dd>04 <span>Bus / Subway / Streetcar / LRT</span></dd></div><div className="period-context"><dt>Observation window</dt><dd>Jan 2025–Aug 2026<span>LRT begins Dec 7, 2025. Coverage varies.</span></dd></div></dl>
      </section>
      <div className="story-layout">
        <aside className="contents"><div className="contents-inner"><p className="figure-kicker">In this investigation</p><nav aria-label="Case-study sections">{navigation.map(([id, label], i) => <a key={id} href={`#${id}`} aria-current={active === id ? 'location' : undefined}><span>{String(i + 1).padStart(2, '0')}</span>{label}</a>)}</nav><div className="contents-note">Recorded activity.<br />Not passenger impact.<br />Not a reliability ranking.</div></div></aside>
        <article className="story">{sections.map((section, i) => <section className="story-section" id={section.id} key={section.id} aria-labelledby={`${section.id}-title`}>
          <div className="section-heading"><span className="section-index">{String(i + 1).padStart(2, '0')}</span><div><p className="figure-kicker">{['The question', 'The foundation', 'The judgment', 'The evidence', 'The boundaries', 'The contribution'][i]}</p><h2 id={`${section.id}-title`}>{section.title}</h2></div></div>
          <div className="prose">{i === 0 && <blockquote className="research-question"><span className="figure-kicker">The research question</span><p>When, where, and how do recorded TTC delays recur—and what changes when we examine both incident frequency and recorded delay duration?</p></blockquote>}<Narrative body={section.body} /></div>
        </section>)}</article>
      </div>
      <section className="sources-section" id="sources" aria-labelledby="sources-title"><div className="sources-heading"><span className="figure-kicker">Evidence, not decoration</span><h2 id="sources-title">Follow the trail.</h2><p>Official source snapshots, retained checksums and reproducible SQL support each figure. Observed dates do not prove complete reporting.</p></div><div className="source-list">{evidence.modes.map(mode => <div key={mode.source_mode}><strong>{mode.source_mode === 'lrt' ? 'LRT' : mode.source_mode[0].toUpperCase() + mode.source_mode.slice(1)}</strong><span>{fmt(mode.recorded_incidents)} records · {mode.first_observed_date}–{mode.last_observed_date}</span><a href={mode.portal_url}>Official dataset ↗</a><a href={mode.source_url}>Resource ↗</a></div>)}</div>
        <details className="provenance-details"><summary>Inspect snapshot and figure provenance</summary><p>The website uses a deterministic projection of the approved Power BI bundle. It does not query a live feed or run the analytical pipeline during deployment.</p><p>Bundle manifest SHA-256: <code>{evidence.provenance.bundle_manifest_sha256}</code></p>{evidence.provenance.selection.snapshots.map(s => <p key={s.mode}><strong>{s.mode}</strong> · Resource <code>{s.resource_id}</code><br />Raw SHA-256 <code>{s.sha256}</code></p>)}</details>
      </section>
    </main>
    <footer className="site-footer"><div><span className="figure-kicker">An independent case study by</span><strong>Ishtiyak Ahmed</strong><p>Not affiliated with or endorsed by the Toronto Transit Commission. Contains information licensed under the Open Government Licence – Toronto.</p></div><div><a href={repo}>View the repository ↗</a><p>Repository access may require permission.<br />Power BI public link: not supplied.<br />Editorial review and dashboard assets pending.</p><a href="https://open.toronto.ca/open-data-licence/">Source data licence ↗</a></div><a className="back-top" href="#top">Back to top ↑</a></footer>
  </>
}

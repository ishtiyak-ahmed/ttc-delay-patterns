import evidence from './data/evidence.json'

import { fmt, percent } from './format'
const pct = (n: number) => `${n.toFixed(2)}%`
const bus = evidence.modes.find(m => m.source_mode === 'bus')!
const subway = evidence.modes.find(m => m.source_mode === 'subway')!
const monthName = (date: string) => new Date(`${date}T12:00:00Z`).toLocaleDateString('en-CA', { month: 'short', year: 'numeric', timeZone: 'UTC' })

function Source({ children }: { children: React.ReactNode }) {
  return <figcaption className="source-note">{children} · Selected snapshots, through August 2026. <a href="#sources">Sources &amp; traceability ↗</a></figcaption>
}

function ShareBars({ rows }: { rows: { label: string; value: number; type: string; detail: string }[] }) {
  return <div className="share-bars">
    {rows.map(row => <div className="share-row" key={row.label}>
      <div className="share-label"><span>{row.label}</span><strong className={row.type}>{pct(row.value)}</strong></div>
      <div className="bar-track" aria-hidden="true"><div className={`bar-fill ${row.type}`} style={{ width: `${row.value}%` }} /></div>
      <span className="bar-detail">{row.detail}</span>
    </div>)}
    <div className="bar-axis" aria-hidden="true"><span>0%</span><span>25%</span><span>50%</span><span>75%</span><span>100%</span></div>
  </div>
}

export function BusConcentration({ featured = false }: { featured?: boolean }) {
  const Heading = featured ? 'h2' : 'h3'
  return <figure className={featured ? 'hero-evidence' : 'evidence-figure'}>
    <div className="figure-kicker">{featured ? 'The central contrast' : 'Figure 01A · Bus'}</div>
    <Heading>A small share of records.<br />A much larger share of minutes.</Heading>
    <ShareBars rows={[
      { label: 'Incidents exceeding 60 minutes', value: percent(evidence.bus.long.recorded_incidents, bus.recorded_incidents), type: 'frequency', detail: `${fmt(evidence.bus.long.recorded_incidents)} of ${fmt(bus.recorded_incidents)} records` },
      { label: 'Recorded minutes from those incidents', value: percent(evidence.bus.long.recorded_delay_minutes, bus.recorded_delay_minutes), type: 'duration', detail: `${fmt(evidence.bus.long.recorded_delay_minutes)} of ${fmt(bus.recorded_delay_minutes)} minutes` },
    ]} />
    <Source>FactDuration, compatible Bus duration bands. Both bars use the same 0–100% scale</Source>
  </figure>
}

export function CodeComparison() {
  return <figure className="evidence-figure">
    <div className="figure-kicker">Figure 01B · Bus raw codes</div>
    <h3>The most frequent code is not the minute leader.</h3>
    <div className="legend"><span><i className="frequency" />Incident share</span><span><i className="duration" />Recorded-minute share</span></div>
    {evidence.bus.codes.map(code => <div className="code-comparison" key={code.raw_code}>
      <h4>{code.raw_code}</h4>
      <ShareBars rows={[
        { label: 'Incident frequency', value: percent(code.recorded_incidents, bus.recorded_incidents), type: 'frequency', detail: `${fmt(code.recorded_incidents)} records / ${fmt(bus.recorded_incidents)} Bus records` },
        { label: 'Recorded duration', value: percent(code.recorded_delay_minutes, bus.recorded_delay_minutes), type: 'duration', detail: `${fmt(code.recorded_delay_minutes)} minutes / ${fmt(bus.recorded_delay_minutes)} Bus minutes` },
      ]} />
    </div>)}
    <p className="figure-warning">MFDV and the over-60-minute population overlap: {fmt(evidence.bus.overlap.recorded_incidents)} records and {fmt(evidence.bus.overlap.recorded_delay_minutes)} minutes. These groups must not be added together.</p>
    <Source>FactCode joined to DimCode by unchanged code_key; exact mode/code grouping</Source>
  </figure>
}

export function ZeroComposition() {
  return <figure className="evidence-figure">
    <div className="figure-kicker">Figure 02A · Subway</div>
    <h3>Most logged Subway records report zero minutes.</h3>
    <div className="big-stat frequency">{pct(percent(subway.zero_minute_incidents, subway.recorded_incidents))}<span> of recorded incidents</span></div>
    <div className="composition" aria-hidden="true"><div style={{ width: `${percent(subway.zero_minute_incidents, subway.recorded_incidents)}%` }} /></div>
    <div className="composition-labels"><span><b>{fmt(subway.zero_minute_incidents)}</b> zero-minute records</span><span><b>{fmt(subway.recorded_incidents - subway.zero_minute_incidents)}</b> positive-minute records</span></div>
    <p className="figure-warning">Source-reported zero is a valid value. It is neither missing data nor proof of zero passenger impact.</p>
    <Source>FactMonth; all {fmt(subway.recorded_incidents)} selected Subway records have eligible durations</Source>
  </figure>
}

export function MonthlyZeros() {
  return <figure className="evidence-figure">
    <div className="figure-kicker">Figure 02B · Subway, January 2025–August 2026</div>
    <h3>Zero-minute records remain a majority every month.</h3>
    <div className="chart-scroll" role="region" aria-label="Monthly zero-minute incident share chart; scroll horizontally on small screens" tabIndex={0}>
      <div className="monthly-chart" role="img" aria-label="Twenty monthly shares range from 59.67 to 72.75 percent; exact values in the table below.">
        <div className="chart-guides"><span>100%</span><span>50%</span><span>0%</span></div>
        <div className="monthly-bars">{evidence.monthly.map((row, index) => <div className="month-column" key={row.month_start}>
          <div className="monthly-bar-space"><div style={{ height: `${percent(row.subway.zero_minute_incidents, row.subway.recorded_incidents)}%` }} /></div>
          <span>{row.month_start.slice(5, 7)}</span><small>{index === 0 || index === 12 ? row.month_start.slice(0, 4) : '\u00a0'}</small>
        </div>)}</div>
      </div>
    </div>
    <details><summary>Read the monthly chart data</summary><div className="table-scroll"><table><caption>Subway zero-minute composition, eligible records</caption><thead><tr><th>Month</th><th>Zero records</th><th>All records</th><th>Share</th></tr></thead><tbody>{evidence.monthly.map(row => <tr key={row.month_start}><th scope="row">{monthName(row.month_start)}</th><td>{fmt(row.subway.zero_minute_incidents)}</td><td>{fmt(row.subway.recorded_incidents)}</td><td>{pct(percent(row.subway.zero_minute_incidents, row.subway.recorded_incidents))}</td></tr>)}</tbody></table></div></details>
    <Source>FactMonth, twenty actual observed months; no interpolated or fabricated values</Source>
  </figure>
}

export function MonthlyLeaders() {
  return <figure className="evidence-figure">
    <div className="figure-kicker">Figure 03 · Subway raw line labels</div>
    <h3>One count leader. Three exceptions for minutes.</h3>
    <div className="leader-summary"><span><b className="frequency">20 / 20</b> months led by YU in incident count</span><span><b className="duration">3 / 20</b> months led by BD in recorded minutes</span></div>
    <div className="table-scroll" role="region" aria-label="Monthly line leadership and actual values" tabIndex={0}><table className="leader-table"><caption>Separate leaders for counts and recorded minutes; raw labels retained</caption><thead><tr><th>Month</th><th>Count leader</th><th>Minute leader</th><th>YU records / minutes</th><th>BD records / minutes</th></tr></thead><tbody>{evidence.monthly.map(row => <tr key={row.month_start} className={row.minute_leaders.includes('BD') ? 'exception-row' : ''}>
      <th scope="row">{monthName(row.month_start)}</th><td><span className="leader-token count-token">{row.count_leaders.join(' / ')}</span></td><td><span className="leader-token minute-token">{row.minute_leaders.join(' / ')}</span>{row.minute_leaders.includes('BD') && <span className="exception-label"> exception</span>}</td>
      {['YU', 'BD'].map(label => { const r = row.line_values.find(r => r.raw_line === label); return <td key={label}>{r ? `${fmt(r.recorded_incidents)} / ${fmt(r.recorded_delay_minutes)}` : 'No observed category records'}</td> })}
    </tr>)}</tbody></table></div>
    <Source>FactLine and DimLine; leaders evaluated across all eligible named raw labels, not just YU and BD; ties retained</Source>
  </figure>
}

export function EnrichmentFigure() {
  const e = evidence.enrichment
  return <figure className="evidence-figure enrichment-figure">
    <div className="figure-kicker">Reference quality · Incident-weighted coverage</div>
    <h3>Recover the text. Preserve the evidence.</h3>
    <ShareBars rows={[
      { label: 'Initial accepted descriptions', value: percent(e.before_records, evidence.totals.recorded_incidents), type: 'frequency', detail: `${fmt(e.before_records)} / ${fmt(evidence.totals.recorded_incidents)} records` },
      { label: 'After reviewed encoding recovery', value: percent(e.after_records, evidence.totals.recorded_incidents), type: 'frequency', detail: `${fmt(e.after_records)} / ${fmt(evidence.totals.recorded_incidents)} records` },
    ]} />
    <p className="figure-warning">+{fmt(e.recovered_records)} records covered · {e.recovered_codes} reviewed descriptions · {e.unresolved_codes} dimension entries still unresolved. Coverage is not causal verification.</p>
    <Source>DimCode, FactCode and checksum-bound recovery evidence; same total-record denominator</Source>
  </figure>
}

export function Architecture() {
  return <figure className="architecture"><div className="figure-kicker">From source bytes to explainable evidence</div><ol>{[
    ['01', 'Pin', 'Source snapshots + provenance'], ['02', 'Preserve', 'Lossless SQLite staging'], ['03', 'Validate', 'Curated values + quality flags'], ['04', 'Analyze', 'Reconciled SQL aggregates'], ['05', 'Present', 'Power BI + static case study'],
  ].map(([n, title, detail]) => <li key={n}><span>{n}</span><strong>{title}</strong><small>{detail}</small></li>)}</ol><figcaption>Immutable source values remain traceable through snapshot and source-row identity.</figcaption></figure>
}

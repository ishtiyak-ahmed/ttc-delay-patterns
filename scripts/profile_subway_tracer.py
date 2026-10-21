"""Read-only profiling of approved TTC CSV snapshots. Standard library only; no cleaning or ingestion."""
import argparse
import csv
import hashlib
import json
from collections import Counter
from datetime import datetime, timedelta
from decimal import Decimal, InvalidOperation
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = ['_id', 'Date', 'Time', 'Day', 'Station', 'Code', 'Min Delay', 'Min Gap', 'Bound', 'Line', 'Vehicle']
NUMERIC = ['_id', 'Min Delay', 'Min Gap', 'Vehicle']

def duplicate_summary(rows, columns):
    counts = Counter(tuple(r[c] for c in columns) for r in rows)
    repeated = [(key, n) for key, n in counts.items() if n > 1]
    return dict(columns=columns, repeated_groups=len(repeated), rows_in_groups=sum(n for _, n in repeated),
                excess_rows=sum(n-1 for _, n in repeated), examples=[dict(values=dict(zip(columns,k)), count=n) for k,n in repeated[:5]])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('provenance', type=Path)
    args = parser.parse_args()
    provenance = json.loads(args.provenance.read_text())
    assert provenance['status'] == 'downloaded'
    mode = provenance['package_name'].removeprefix('ttc-').removesuffix('-delay-data')
    assert mode in {'subway', 'bus', 'streetcar', 'lrt'}
    label = 'LRT' if mode == 'lrt' else mode.capitalize()
    manifest = json.loads((ROOT / 'source_manifest.json').read_text())
    package = next(p for p in manifest['packages'] if p['package_id'] == provenance['package_id'])
    resource = next(r for r in package['resources'] if r['resource_id'] == provenance['resource_id'])
    assert provenance['source_url'] == resource['url']
    datastore_counts = [r['record_count'] for r in package['resources'] if r['datastore_active'] and 'Code' not in r['name']]
    assert len(datastore_counts) == 1
    catalog_count = datastore_counts[0]
    raw = ROOT / provenance['raw_path']
    original = raw.read_bytes()
    checksum = hashlib.sha256(original).hexdigest()
    assert checksum == provenance['sha256'] and len(original) == provenance['file_size_bytes']
    with raw.open(encoding='utf-8-sig', newline='') as stream:
        reader = csv.reader(stream, strict=True)
        header = next(reader)
        parsed = list(reader)
    assert len(header) == len(EXPECTED) and set(header) == set(EXPECTED), ('Unexpected schema', header)
    bad_widths = [dict(record_number=i+1, fields=len(row)) for i,row in enumerate(parsed, 1) if len(row) != len(header)]
    assert not bad_widths, bad_widths[:10]
    rows = [dict(zip(header, row)) for row in parsed]
    n = len(rows)
    stats = {}
    numbers = {}
    for c in header:
        counts = Counter(r[c] for r in rows)
        blank = sum(v for k,v in counts.items() if not k.strip())
        stats[c] = dict(apparent_type='text', blank=blank, empty_string=counts[''], whitespace_only=sum(v for k,v in counts.items() if k and not k.strip()),
                        null_like_tokens={k:v for k,v in counts.items() if k.strip().lower() in {'null','none','nan','n/a','na'}},
                        distinct_including_blank=len(counts), surrounding_whitespace=sum(v for k,v in counts.items() if k != k.strip()))
        if c in NUMERIC:
            values = []; failures = []; fractional = 0
            for i,r in enumerate(rows, 1):
                if not r[c].strip(): continue
                try:
                    value = Decimal(r[c])
                    if not value.is_finite(): raise InvalidOperation
                    values.append(value)
                    fractional += value != value.to_integral_value()
                except InvalidOperation:
                    failures.append(dict(record_number=i, value=r[c]))
            stats[c].update(apparent_type='integer-looking numeric text' if not fractional else 'numeric text', numeric_failures=len(failures), failure_examples=failures[:5], fractional=fractional)
            numbers[c] = values
    date_format = '%Y-%m-%dT%H:%M:%S' if mode == 'bus' else '%Y-%m-%d'
    dates = []; date_failures = []; time_failures = []; weekday_mismatches = []
    for i,r in enumerate(rows, 1):
        try:
            parsed_date = datetime.strptime(r['Date'], date_format)
            if parsed_date.strftime(date_format) != r['Date']: raise ValueError('Noncanonical date')
            d = parsed_date.date()
            dates.append(d)
            if d.strftime('%A') != r['Day']:
                weekday_mismatches.append(dict(record_number=i, date=r['Date'], day=r['Day']))
        except ValueError:date_failures.append(dict(record_number=i, value=r['Date']))
        try:
            t = datetime.strptime(r['Time'], '%H:%M')
            if t.strftime('%H:%M') != r['Time']:raise ValueError('Noncanonical time')
        except ValueError:time_failures.append(dict(record_number=i, value=r['Time']))
    stats['Date']['apparent_type'] = 'timestamp text (YYYY-MM-DDTHH:MM:SS; no timezone)' if mode == 'bus' else 'date text (YYYY-MM-DD)'
    stats['Time']['apparent_type'] = 'time text (HH:MM; no timezone)'
    durations = {}
    for c in ['Min Delay','Min Gap']:
        values = sorted(numbers[c])
        # Nearest-rank percentiles: ceil(p*n), one-based.
        def percentile(p):return str(values[max(0, (len(values)*p+99)//100-1)])
        durations[c] = dict(valid_count=len(values), zero=sum(v==0 for v in values), negative=sum(v<0 for v in values),
                            minimum=str(min(values)), maximum=str(max(values)), total=str(sum(values)),
                            nearest_rank_percentiles={str(p):percentile(p) for p in [50,90,95,99]},
                            greater_than_60=sum(v>60 for v in values), greater_than_120=sum(v>120 for v in values),
                            greater_than_1440=sum(v>1440 for v in values),
                            largest_rows=sorted(rows,key=lambda r:Decimal(r[c]) if r[c].strip() else Decimal('-Infinity'),reverse=True)[:5])
    counts_by_date = Counter(d.isoformat() for d in dates)
    missing_dates = []
    day = min(dates)
    while day <= max(dates):
        if day.isoformat() not in counts_by_date:missing_dates.append(day.isoformat())
        day += timedelta(days=1)
    categories = {c:dict(sorted(Counter(r[c] for r in rows).items())) for c in ['Day','Station','Code','Bound','Line','Vehicle']}
    full = duplicate_summary(rows, header)
    without_id = duplicate_summary(rows, [c for c in header if c != '_id'])
    candidate = duplicate_summary(rows, ['Date','Time','Station','Code','Bound','Line'])
    coarse = duplicate_summary(rows, ['Date','Time','Station','Line'])
    ids = numbers['_id']
    result = dict(mode=mode, provenance_path=str(args.provenance), date_format=date_format, date_time_components=dict(Counter(r['Date'][10:] for r in rows)), raw_path=provenance['raw_path'], sha256=checksum, bytes=len(original), encoding='UTF-8, decoded with utf-8-sig', utf8_bom=original.startswith(b'\xef\xbb\xbf'),
                  columns=header, rows=n, malformed_width_rows=bad_widths, columns_profile=stats,
                  minimum_date=min(dates).isoformat(), maximum_date=max(dates).isoformat(),
                  date_parse_failures=len(date_failures), date_failure_examples=date_failures[:5],
                  time_parse_failures=len(time_failures), time_failure_examples=time_failures[:5],
                  weekday_mismatches=len(weekday_mismatches), weekday_mismatch_examples=weekday_mismatches[:5],
                  dates_before_2025=sum(d.year<2025 for d in dates), dates_after_retrieval=sum(d>datetime.fromisoformat(provenance['retrieved_at_utc']).date() for d in dates),
                  distinct_dates=len(counts_by_date), missing_dates_between_endpoints=missing_dates,
                  monthly_rows=dict(sorted(Counter(d.strftime('%Y-%m') for d in dates).items())),
                  durations=durations, exact_duplicates=full, duplicates_excluding_id=without_id,
                  potential_key_duplicates=candidate, coarse_key_duplicates=coarse, categories=categories,
                  id_summary=dict(minimum=str(min(ids)),maximum=str(max(ids)),distinct=len(set(ids)),duplicate_excess=len(ids)-len(set(ids)),
                                  sequential_in_file=ids==[Decimal(i) for i in range(1,n+1)]),
                  zero_vehicle=categories['Vehicle'].get('0',0),
                  min_gap_less_than_min_delay=sum(Decimal(r['Min Gap'])<Decimal(r['Min Delay']) for r in rows),
                  manifest_datastore_record_count=catalog_count, matches_manifest_datastore_count=n==catalog_count)
    outdir = ROOT/'reports';outdir.mkdir(exist_ok=True)
    output = outdir/(mode + '_tracer_profile.json')
    with output.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
    lines = [f'# {label} tracer inspection', '', 'Inspection date: '+provenance['retrieved_at_utc'][:10], '',
             '## Acquisition and method', '',
             f"Source: `{provenance['package_name']}`, resource `{provenance['resource_id']}`. URL resolved from the unchanged local manifest. Only the selected CSV was downloaded by this acquisition command.", '',
             f"HTTP {provenance['http_status']}; {len(original):,} bytes; SHA-256 `{checksum}`. Raw snapshot: `{provenance['raw_path']}`. Provenance: `{args.provenance}`.", '',
             f"Python `{provenance['python_executable']}` ({provenance['python_version'].split()[0]}); installed certifi CA bundle `{provenance['ca_bundle']}`; `CERT_REQUIRED` and hostname verification enabled. No dependencies installed. HTTP Content-Length matched the saved size. HTTP Last-Modified: `{provenance['response_headers'].get('Last-Modified')}`. Full headers and CA-bundle hash are in provenance.", '',
             'Profiling uses the Python standard library, strict CSV parsing and UTF-8 decoding. Raw bytes are verified against provenance before and after profiling. No source rows are altered, removed, or ingested. Blank means empty or whitespace-only; literal null-like tokens are counted separately, not converted. Types below are observations, not source definitions.', '',
             '## Schema and missingness', '', '| Exact column | Apparent type | Blank | Distinct (including blank) | Numeric failures |', '|---|---|---:|---:|---:|']
    for c in header:
        st=stats[c];lines.append(f"| `{c}` | {st['apparent_type']} | {st['blank']} | {st['distinct_including_blank']} | {st.get('numeric_failures','—')} |")
    lines += ['',f"Records: **{n:,}**; malformed-width rows: {len(bad_widths)}. Date failures: {len(date_failures)}; time failures: {len(time_failures)}; weekday mismatches: {len(weekday_mismatches)}.",
              f"Literal null-like tokens: `{ {c:st['null_like_tokens'] for c,st in stats.items() if st['null_like_tokens']} }`. Values with surrounding whitespace: `{ {c:st['surrounding_whitespace'] for c,st in stats.items() if st['surrounding_whitespace']} }`.", '',
              '## Observed coverage', '', f"Parsed dates: **{min(dates)} through {max(dates)}**; {len(counts_by_date)} distinct incident dates. Dates before 2025: {result['dates_before_2025']}; dates after retrieval: {result['dates_after_retrieval']}. Dates without records between endpoints: {len(missing_dates)} (listed in JSON).", '',
              f"The {n:,} CSV records {'match' if result['matches_manifest_datastore_count'] else 'do not match'} the snapshot's {catalog_count:,} datastore record_count. Count agreement does not prove identical contents, complete reporting, or absence of revisions. Missing dates or periods do not establish zero-delay service. No records beyond the maximum date can be inferred from the filename or monthly refresh label.", '', '| Month | Recorded rows |','|---|---:|']
    for month,count in result['monthly_rows'].items():lines.append(f'| {month} | {count} |')
    lines += ['', '## Recorded durations', '', 'Thresholds above 60, 120 and 1,440 minutes are descriptive review flags, not validated error rules. Percentiles use nearest rank. Min Gap is profiled separately; it is not added to Min Delay.', '',
              '| Field | Zero | Negative | Min | Median | P95 | P99 | Max | >60 | >120 | >1440 | Sum |','|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
    for c,st in durations.items():lines.append(f"| {c} | {st['zero']} | {st['negative']} | {st['minimum']} | {st['nearest_rank_percentiles']['50']} | {st['nearest_rank_percentiles']['95']} | {st['nearest_rank_percentiles']['99']} | {st['maximum']} | {st['greater_than_60']} | {st['greater_than_120']} | {st['greater_than_1440']} | {st['total']} |")
    lines += ['', f"Recorded row count ({n:,}) and the sum of Min Delay ({durations['Min Delay']['total']} recorded minutes) are different measures. Zero-minute rows remain records. These are uncleaned source totals, not passenger impact or normalized reliability measures.",
              f"Min Gap is less than Min Delay in {result['min_gap_less_than_min_delay']} rows; the fields' intended relationship requires documentation. The JSON includes the five largest rows for each duration field.", '',
              '## Duplicate candidates and identifiers', '', '| Definition | Repeated groups | Rows in groups | Excess beyond first |', '|---|---:|---:|---:|']
    for label,st in [('All 11 columns',full),('All columns except _id',without_id),('Date, Time, Station, Code, Bound, Line',candidate),('Date, Time, Station, Line',coarse)]:
        lines.append(f"| {label} | {st['repeated_groups']} | {st['rows_in_groups']} | {st['excess_rows']} |")
    lines += ['',f"_id summary: `{result['id_summary']}`. Export ID uniqueness does not establish stable incident identity across refreshes. Candidate keys are hypotheses, not documented unique keys; repeated groups may contain legitimate concurrent or repeated incidents. Nothing was deleted. JSON includes examples.", '',
              '## Codes and categories', '',
              f"Distinct Code values (including blank): {len(categories['Code'])}; stations: {len(categories['Station'])}; vehicle values: {len(categories['Vehicle'])}. Full exact value frequencies for Code, Day, Station, Bound, Line and Vehicle are in the JSON; no codes were translated into causes.", '',
              f"Day frequencies: `{categories['Day']}`.",f"Bound frequencies: `{categories['Bound']}`.",f"Line frequencies: `{categories['Line']}`.",
              f"Vehicle `0` occurs {result['zero_vehicle']} times; whether it means unknown, not applicable, or an actual identifier is unresolved. Vehicle identifiers should be retained as source text pending definition checks.", '',
              'Most frequent codes: '+', '.join(f'`{k}` ({v})' for k,v in Counter(r['Code'] for r in rows).most_common(15))+'.', '',
              '## Implications and unresolved questions', '',
              '- Preserve source strings, file hash, resource identity and record position. Parse dates, times and durations explicitly; timezone/service-day meaning remains unverified.',
              '- Keep blank direction values and zero vehicle/duration values distinct from missing records. Review station/line labels and unusual durations before setting cleaning rules.',
              '- Do not deduplicate using _id or a guessed incident key. Investigate duplicate examples and whether IDs persist across replacement exports.',
              '- Verify code meanings, Min Delay/Min Gap definitions, direction/line conventions, station naming and recording rules against official documentation before interpretation. No lookup or other resource was downloaded.',
              '- Establish publication lag and completeness separately from observed date range; compare future approved snapshots to investigate revisions. This single download establishes no append-only update behavior.',
              '- Shared column names do not prove cross-mode compatibility. No database, pipeline, analytical SQL, dashboard or update automation was implemented.', '',
              '## Reproduce', '', f"`python3 scripts/profile_subway_tracer.py {args.provenance}`", '',
              f'Outputs use exclusive creation and refuse to overwrite an existing report. Preserve or deliberately relocate previous reports before rerunning. Acquisition is a separate network command (`python3 scripts/acquire_subway_tracer.py --mode {mode}`); each successful acquisition creates a new timestamped snapshot.']
    extra = [
        '## Additional source observations', '',
        f"Exact column order: `{header}`. Same names as Subway; {'same' if header == EXPECTED else 'different'} order.",
        f"Date suffix frequencies: `{result['date_time_components']}`. Bus timestamp dates are parsed explicitly; any non-midnight components remain in the source and are not silently removed.",
        f"Date/weekday mismatch examples: `{weekday_mismatches[:5]}`.",
        f"Largest Min Delay examples: `{durations['Min Delay']['largest_rows'][:3]}`.",
        f"Duplicate examples excluding _id: `{without_id['examples'][:2]}`.",
        'Station and Line frequencies in JSON preserve exact labels; these fields must not be assumed to contain only stations or single standardized routes. Codes require official mode-specific definitions.', '',
    ]
    insert = lines.index('## Implications and unresolved questions')
    lines[insert:insert] = extra
    report=outdir/(mode + '_tracer_profile.md')
    with report.open('x') as f:f.write('\n'.join(lines)+'\n')
    assert hashlib.sha256(raw.read_bytes()).hexdigest()==checksum
    print('\n'.join(lines))
    print('Machine-readable details:',output)

if __name__ == '__main__':main()

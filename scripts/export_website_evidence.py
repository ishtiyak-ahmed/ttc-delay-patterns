"""Read-only, deterministic projection of the approved Power BI bundle for the website."""
import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIELDS = ('recorded_incidents', 'recorded_delay_minutes', 'zero_minute_incidents')


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def totals(rows):
    # Existing compatible additive measures only; never average shares or sum distinct dates.
    return {field: sum(row[field] for row in rows) for field in FIELDS}


def build_evidence(bundle=ROOT / 'results/power_bi', source=ROOT / 'source_manifest.json',
                   recovery=ROOT / 'config/code_description_recovery.json'):
    bundle, source, recovery = Path(bundle), Path(source), Path(recovery)
    manifest = json.loads((bundle / 'manifest.json').read_text())
    for name, expected in manifest['export_sha256'].items():
        path = (bundle / name).resolve()
        if path.parent != bundle.resolve() or digest(path) != expected:
            raise ValueError('Bundle checksum/path mismatch')
    if digest(recovery) != manifest['code_enrichment']['recovery_evidence_sha256']:
        raise ValueError('Recovery evidence checksum mismatch')
    data = json.loads((bundle / 'results.json').read_text())
    recovery_data = json.loads(recovery.read_text())
    source_data = json.loads(source.read_text())
    codes = {r['code_key']: r for r in data['dim_code']}
    lines = {r['line_key']: r for r in data['dim_line']}
    modes = []
    for mode in data['dim_mode']:
        rows = [r for r in data['fact_month'] if r['source_mode'] == mode['source_mode']]
        package = next(p for p in source_data['packages']
                       if any(r['resource_id'] == mode['resource_id'] for r in p['resources']))
        resource = next(r for r in package['resources'] if r['resource_id'] == mode['resource_id'])
        modes.append(dict(mode, **totals(rows), portal_url=package['portal_url'], source_url=resource['url']))

    def code_total(mode, code):
        keys = {key for key, r in codes.items() if r['source_mode'] == mode and r['raw_code'] == code}
        if len(keys) != 1:
            raise ValueError('Headline code is absent or ambiguous')
        return dict(raw_code=code, **totals([r for r in data['fact_code'] if r['code_key'] in keys]))

    bus_duration = [r for r in data['fact_duration'] if r['source_mode'] == 'bus']
    long_bands = {'over_60_to_120', 'over_120'}
    bus_long = [r for r in bus_duration if r['duration_band'] in long_bands]
    overlap = [r for r in bus_long if r['is_bus_mfdv'] == 1]
    union = [r for r in bus_duration if r['duration_band'] in long_bands or r['is_bus_mfdv'] == 1]
    month_rows = []
    for month in sorted(r['month_start'] for r in data['fact_month'] if r['source_mode'] == 'subway'):
        subway = next(r for r in data['fact_month'] if r['source_mode'] == 'subway' and r['month_start'] == month)
        eligible_lines = [r for r in data['fact_line'] if r['source_mode'] == 'subway'
                          and r['month_start'] == month and lines[r['line_key']]['category_eligible']]
        # Same named-label eligibility and leading-rank definition as monthly_lines.sql; retain ties.
        leaders = {field: sorted(lines[r['line_key']]['raw_line'] for r in eligible_lines
                                if r[field] == max(x[field] for x in eligible_lines))
                   for field in ('recorded_incidents', 'recorded_delay_minutes')}
        line_values = [dict(raw_line=lines[r['line_key']]['raw_line'], **totals([r]))
                       for r in eligible_lines if lines[r['line_key']]['raw_line'] in ('YU', 'BD')]
        bus = next(r for r in data['fact_month'] if r['source_mode'] == 'bus' and r['month_start'] == month)
        mfdv = next(r for r in data['fact_code'] if r['source_mode'] == 'bus'
                    and r['month_start'] == month and codes[r['code_key']]['raw_code'] == 'MFDV')
        month_rows.append(dict(month_start=month, subway=totals([subway]), line_values=line_values,
                               count_leaders=leaders['recorded_incidents'],
                               minute_leaders=leaders['recorded_delay_minutes'],
                               bus=totals([bus]), bus_mfdv=totals([mfdv])))

    weights = defaultdict(int)
    for row in data['fact_code']:
        weights[row['code_key']] += row['recorded_incidents']
    reviewed = {(r['source_mode'], r['raw_code']) for r in recovery_data['entries']}
    accepted = [r for r in codes.values() if r['code_description'] is not None]
    recovered = [r for r in accepted if (r['source_mode'], r['raw_code']) in reviewed]
    after = sum(weights[r['code_key']] for r in accepted)
    gain = sum(weights[r['code_key']] for r in recovered)
    return dict(
        totals=totals(data['fact_month']), modes=modes,
        bus=dict(long=totals(bus_long), overlap=totals(overlap), union=totals(union),
                 codes=[code_total('bus', code) for code in ('EFO', 'MFDV')]),
        subway=dict(muis=code_total('subway', 'MUIS')), monthly=month_rows,
        enrichment=dict(before_records=after-gain, after_records=after, recovered_records=gain,
                        recovered_codes=len(recovered), accepted_codes=len(accepted),
                        total_codes=len(codes), unresolved_codes=len(codes)-len(accepted)),
        provenance=dict(bundle_manifest_sha256=digest(bundle/'manifest.json'),
                        typed_results_sha256=digest(bundle/'results.json'),
                        source_manifest_sha256=digest(source), recovery_evidence_sha256=digest(recovery),
                        adapter_sha256=digest(__file__), selection=manifest['selection'],
                        source='results/power_bi',
                        method='Projection and compatible additive sums of approved measures; existing named-line eligibility; ties retained. No cleaning, inference or exposure normalization.'))


def serialized_evidence(**kwargs):
    return (json.dumps(build_evidence(**kwargs), indent=2, ensure_ascii=False, allow_nan=False) + '\n').encode('utf-8')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT/'website/src/data/evidence.json')
    parser.add_argument('--check', action='store_true', help='Verify checked-in evidence without writing')
    args = parser.parse_args()
    payload = serialized_evidence()
    if args.check:
        if not args.output.is_file() or args.output.read_bytes() != payload:
            parser.error('Website evidence differs; investigate before regeneration')
    else:
        if args.output.exists() and args.output.read_bytes() != payload:
            parser.error('Evidence already exists with different bytes; choose a fresh output for review')
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_bytes(payload)
    print('Website evidence verified' if args.check else 'Website evidence written')


if __name__ == '__main__':
    main()

"""Reconcile four read-only profiles against raw bytes and write their comparison."""
import csv
import hashlib
import json
from collections import Counter
from datetime import date, time, timedelta
from decimal import Decimal, InvalidOperation
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODES = ['subway', 'bus', 'streetcar', 'lrt']

def main():
    manifest = json.loads((ROOT/'source_manifest.json').read_text())
    profiles = {}; details = {}; provenance_files = {}
    for mode in MODES:
        profile = json.loads((ROOT/'reports'/f'{mode}_tracer_profile.json').read_text())
        records = []
        for path in (ROOT/'data/provenance').glob('*.json'):
            record = json.loads(path.read_text())
            if record.get('status') == 'downloaded' and record.get('raw_path') == profile['raw_path']:
                records.append((path,record))
        assert len(records)==1
        provenance_path, provenance = records[0]
        provenance_files[mode] = str(provenance_path.relative_to(ROOT))
        package = next(p for p in manifest['packages'] if p['package_id']==provenance['package_id'])
        resource = next(r for r in package['resources'] if r['resource_id']==provenance['resource_id'])
        assert resource['url']==provenance['source_url']==provenance['final_url']
        assert provenance['http_status']==200 and provenance['certificate_verification']=='CERT_REQUIRED' and provenance['hostname_verification'] is True
        body = (ROOT/provenance['raw_path']).read_bytes()
        assert len(body)==provenance['file_size_bytes']==profile['bytes']==int(provenance['response_headers']['Content-Length'])==resource['size']
        assert hashlib.sha256(body).hexdigest()==provenance['sha256']==profile['sha256']
        with (ROOT/provenance['raw_path']).open(encoding='utf-8-sig',newline='') as f:
            reader=csv.DictReader(f);rows=list(reader);header=reader.fieldnames
        assert header==profile['columns'] and len(rows)==profile['rows']
        assert all(None not in r and all(v is not None for v in r.values()) for r in rows)
        for c, st in profile['columns_profile'].items():
            assert sum(not r[c].strip() for r in rows)==st['blank']
            assert len(set(r[c] for r in rows))==st['distinct_including_blank']
            if 'numeric_failures' in st:
                failures=0
                for r in rows:
                    if not r[c].strip():continue
                    try:
                        if not Decimal(r[c]).is_finite():failures+=1
                    except InvalidOperation:failures+=1
                assert failures==st['numeric_failures']
        # Independent ISO date/time parser; retains the raw timestamp separately.
        dates=[date.fromisoformat(r['Date'].split('T')[0]) for r in rows]
        times=[time.fromisoformat(r['Time']) for r in rows]
        assert len(dates)==len(times)==len(rows)
        assert profile['date_parse_failures']==profile['time_parse_failures']==0
        assert min(dates).isoformat()==profile['minimum_date'] and max(dates).isoformat()==profile['maximum_date']
        monthly=dict(sorted(Counter(d.strftime('%Y-%m') for d in dates).items()))
        assert monthly==profile['monthly_rows'] and sum(monthly.values())==len(rows)
        day_set=set(dates);missing=[];d=min(dates)
        while d<=max(dates):
            if d not in day_set:missing.append(d.isoformat())
            d+=timedelta(days=1)
        assert missing==profile['missing_dates_between_endpoints'] and len(day_set)==profile['distinct_dates']
        mismatches=Counter(d.isoformat() for r,d in zip(rows,dates) if r['Day']!=d.strftime('%A'))
        assert sum(mismatches.values())==profile['weekday_mismatches']
        for c,st in profile['durations'].items():
            values=sorted(Decimal(r[c]) for r in rows if r[c].strip())
            assert str(sum(values))==st['total'] and len(values)==st['valid_count']
            assert str(min(values))==st['minimum'] and str(max(values))==st['maximum']
            assert sum(v==0 for v in values)==st['zero'] and sum(v<0 for v in values)==st['negative']
            for threshold in [60,120,1440]:assert sum(v>threshold for v in values)==st[f'greater_than_{threshold}']
            for pct,value in st['nearest_rank_percentiles'].items():assert str(values[(len(values)*int(pct)+99)//100-1])==value
        for k in ['exact_duplicates','duplicates_excluding_id','potential_key_duplicates','coarse_key_duplicates']:
            st=profile[k];counts=Counter(tuple(r[c] for c in st['columns']) for r in rows)
            repeated=[n for n in counts.values() if n>1]
            assert (len(repeated),sum(repeated),sum(n-1 for n in repeated))==(st['repeated_groups'],st['rows_in_groups'],st['excess_rows'])
        for c,counts in profile['categories'].items():assert dict(Counter(r[c] for r in rows))==counts
        ids=[r['_id'] for r in rows]
        assert len(set(ids))==profile['id_summary']['distinct'] and ids==[str(i) for i in range(1,len(rows)+1)]
        assert sum(Decimal(r['Min Gap'])<Decimal(r['Min Delay']) for r in rows)==profile['min_gap_less_than_min_delay']
        assert len(rows)==next(r['record_count'] for r in package['resources'] if r['datastore_active'] and 'Code' not in r['name'])
        line_dates={}
        for r,d in zip(rows,dates):line_dates.setdefault(r['Line'],[]).append(d)
        line_coverage={k:dict(rows=len(v),minimum=min(v).isoformat(),maximum=max(v).isoformat()) for k,v in sorted(line_dates.items())}
        details[mode]=dict(verification='PASS',weekday_mismatches_by_date=dict(sorted(mismatches.items())),line_coverage=line_coverage,
                           non_cardinal_bound={k:v for k,v in profile['categories']['Bound'].items() if k not in ['','N','S','E','W']},
                           maximum_label_lengths={c:max(len(r[c]) for r in rows) for c in ['Line','Station','Code']})
        profiles[mode]=profile
        print(mode, 'PASS:',len(rows),'rows; checksums, bytes, schema, blanks, dates, durations, categories and duplicate metrics reconciled')
    shared=set.intersection(*(set(p['columns']) for p in profiles.values()))
    lines=['# Cross-mode source profiling — Milestone 2', '', 'Assessment date: 2026-10-21. All observations refer to preserved snapshots acquired on this date, not live ongoing coverage.', '',
           '## Method and scope', '',
           'The existing acquisition and profiling scripts were parameterized with explicit mode/resource selection, schema-order tolerance, mode-specific date parsing, manifest record counts, and distinct output filenames. Filenames retain their original Subway names for command compatibility. Subway bytes, provenance and completed reports were preserved. No cleaning, deduplication, database, SQL, dashboard or update automation was implemented.', '',
           'Each acquisition used the exact approved manifest URL, Python 3.11.9 and the already-installed certifi bundle with certificate and hostname verification enabled. Only Bus, Streetcar and LRT were downloaded in this task; all returned HTTP 200. No dependencies were installed. Raw snapshots and output reports use exclusive creation.', '',
           'Strict UTF-8/CSV parsing retained every record. Blank means empty or whitespace-only; literal null-like strings were counted separately. Nearest-rank percentiles and >60/>120/>1440 minute thresholds are descriptive review flags, not rules for exclusion. All columns and exact category frequencies appear in per-mode JSON profiles.', '',
           '## Coverage and missingness', '', '| Mode | Rows | Observed date range | Days with records | Days absent within range | Blank Bound | Blank Line | Blank Code | Weekday conflicts |', '|---|---:|---|---:|---:|---:|---:|---:|---:|']
    for mode,p in profiles.items():
        st=p['columns_profile'];lines.append(f"| {mode.title()} | {p['rows']:,} | {p['minimum_date']}–{p['maximum_date']} | {p['distinct_dates']} | {len(p['missing_dates_between_endpoints'])} | {st['Bound']['blank']:,} | {st['Line']['blank']:,} | {st['Code']['blank']} | {p['weekday_mismatches']} |")
    lines += ['', 'Every date, time and numeric value parsed in all four files, and no malformed-width records were found. The table contains all nonzero blank counts; every other column has zero blanks. No literal null-like tokens or leading/trailing whitespace were observed. Zero Vehicle values are not counted as blank.', '',
              'Subway, Bus and Streetcar cover all 608 calendar dates between their endpoints. LRT begins 2025-12-07 and has no records dated 2026-01-23 within its 268-day endpoint span. This does not establish zero-delay service, missing reporting, or an operating start date. All four end on 2026-08-31 despite retrieval in October and September Last-Modified headers. September/October coverage and publication lag remain unresolved. Count agreement with datastore metadata does not establish complete incident capture.', '',
              '## Schema and identifiers', '',
              'All four expose the same 11 column names: '+', '.join('`'+c+'`' for c in profiles['subway']['columns'])+'. No mode-specific columns were observed.', '',
              'Bus, Streetcar and LRT order columns as `_id, Date, Line, Time, Day, Station, Code, Min Delay, Min Gap, Bound, Vehicle`; Subway places Line after Bound. Bus Date is `YYYY-MM-DDTHH:MM:SS`, with every timestamp suffix `T00:00:00`; the other modes use `YYYY-MM-DD`. Time is separate `HH:MM` without a timezone in all four. Date/time semantics still require documentation.', '',
              '`_id`, Min Delay, Min Gap and Vehicle contain integer-looking numeric text. Day, Station, Code, Bound and Line are text. Vehicle and _id should retain source values: numeric-looking identifiers are not measurements.', '',
              'All four _id columns are individually unique, sequential from 1 to their row count. IDs overlap between modes and are not globally unique. Snapshot uniqueness does not establish persistent incident identity across refreshes.', '',
              '| Mode | Exact duplicate excess (all columns) | Duplicate groups excluding _id | Rows in those groups | Excess excluding _id | Potential key excess |', '|---|---:|---:|---:|---:|---:|']
    for mode,p in profiles.items():
        st=p['duplicates_excluding_id'];lines.append(f"| {mode.title()} | {p['exact_duplicates']['excess_rows']} | {st['repeated_groups']} | {st['rows_in_groups']} | {st['excess_rows']} | {p['potential_key_duplicates']['excess_rows']} |")
    lines += ['', 'Potential key = Date, Time, Station, Code, Bound, Line. This is a profiling hypothesis, not a proven incident key. Repeated rows may include legitimate repeated events. No records were removed.', '',
              '## Recorded duration observations', '', '| Mode | Zero Min Delay | Negative | Median | P99 | Max | >60 | >120 | Raw sum Min Delay | Vehicle 0 |', '|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
    for mode,p in profiles.items():
        st=p['durations']['Min Delay'];lines.append(f"| {mode.title()} | {st['zero']:,} | {st['negative']} | {st['nearest_rank_percentiles']['50']} | {st['nearest_rank_percentiles']['99']} | {st['maximum']} | {st['greater_than_60']} | {st['greater_than_120']} | {st['total']} | {p['zero_vehicle']} |")
    lines += ['', 'Counts and recorded minutes measure different things. These uncleaned sums retain zero-duration and possible duplicate records; they are not rankings of reliability or passenger impact. No Min Delay or Min Gap value exceeds 1,440 minutes. Min Gap is separate and is never added to Min Delay. Their intended relationship is unverified; Min Gap is smaller than Min Delay in '+', '.join(f"{m}: {p['min_gap_less_than_min_delay']} rows" for m,p in profiles.items())+'.', '',
              '## Labels, locations and source concerns', '']
    for mode,p in profiles.items():
        cats=p['categories'];nonblank_codes=len([c for c in cats['Code'] if c.strip()])
        lines += [f"- **{mode.title()}:** {nonblank_codes} nonblank codes; {len(cats['Line'])} Line labels including blank; {len(cats['Station'])} Station values. Non-cardinal nonblank Bound values: `{details[mode]['non_cardinal_bound']}`."]
    lines += ['',
              '- Bus Line contains route names, numeric-only labels, branches, shuttles and operational labels. Examples include `100 FLEMINGDON PARK` vs `100 FLEMINGTON PARK`, `999`, `FLEET VEHICLE` and `LINE 1 SHUTTLE`. Streetcar similarly mixes `504 KING`, `504 AKING`, `TRACK 11`, `CARHOUSE` and Bus-like labels. Do not infer physical vehicle mode from route names alone.',
              '- Subway Line has combined or inconsistent abbreviations and other-route labels; its completed report preserves examples. LRT includes EC/FW combinations and generic LRT labels; EC and FW meanings require official confirmation.',
              '- Bus code `XXXXX` occurs once; Streetcar has `XXXXX` 53 times and one empty Code. LRT contains `MFUIR` once alongside predominantly other code families. Treat these as review candidates; no dictionary validation was performed.',
              '- Station contains location strings, not verified station IDs. Observed maxima for Station and Line lengths are in the comparison JSON. Apparent truncation, spelling variants, intersections, facilities and route combinations make location grouping uncertain.',
              '- Weekday/date conflicts recur across modes. All four have conflicts on 2026-04-26; LRT also has conflicts on other dates. These overlaps warrant source investigation; they do not establish a shared cause or which field is correct.', '',
              'Observed LRT coverage by exact Line label:', '', '| Line (blank shown explicitly) | Rows | First observed | Last observed |', '|---|---:|---|---|']
    for label,st in details['lrt']['line_coverage'].items():lines.append(f"| {label or '(blank)'} | {st['rows']} | {st['minimum']} | {st['maximum']} |")
    lines += ['', 'These are record endpoints, not independently verified dates of service availability.', '',
              '## What may support shared analysis, and what must remain mode-specific', '',
              'Date/Time may support calendar/hour patterns after resolving timestamp, timezone and service-day meaning. Recorded row counts and Min Delay distributions are candidates for within-mode analysis after recording definitions and duplicate treatment are agreed. Source mode, raw value and snapshot identity must remain traceable. These are possibilities supported by the schema, not implemented transformations.', '',
              'Code meanings, route/line interpretation, direction conventions, location normalization and Vehicle placeholders require mode-specific review. Shared spellings or columns do not establish equivalent event definitions, thresholds or collection practices. Comparing raw totals across unequal coverage or exposure would not answer which service is more reliable.', '',
              '## Questions for official documentation and code dictionaries', '',
              '1. What constitutes a recorded incident in each mode? Which events are omitted, and can several records describe one incident?',
              '2. What do Min Delay and Min Gap measure, including zeros, extreme values and Gap smaller than Delay? Are 999-like values valid durations or sentinels?',
              '3. Which date/day field is authoritative? Are dates calendar or operating-service dates, and what timezone applies?',
              '4. Are code dictionaries mode-specific/versioned? How should XXXXX, blank codes and codes shared between packages be interpreted?',
              '5. What do Bound B and unexpected numeric/letter values mean? Do Vehicle 0 and blank Line mean unknown or not applicable?',
              '6. Are Station/Line strings length-limited? How should combined lines, shuttle labels, facilities and apparent misspellings be interpreted?',
              '7. What is the LRT reporting start, which lines are included, why is 2026-01-23 absent, and what explains the shorter observed period?',
              '8. Are exports complete and current? Can older rows be revised or IDs reassigned? A single snapshot cannot establish safe update behavior.', '',
              'No official dictionaries or extra resources were downloaded. Apparent completeness remains a reporting question, not a conclusion from these CSVs.', '',
              '## Acquisition inventory and verification', '', '| Mode | Bytes | SHA-256 | Provenance |', '|---|---:|---|---|']
    for mode,p in profiles.items():lines.append(f"| {mode.title()} | {p['bytes']} | `{p['sha256']}` | `{provenance_files[mode]}` |")
    lines += ['', 'Resource IDs and full URLs, retrieval timestamps, HTTP headers, Python version, CA-bundle path/hash and TLS flags are in each provenance record. Raw paths and exact columns are in each profile. Raw data are Git-ignored; provenance/reports are versionable.', '',
              'Executed acquisitions: `python3 scripts/acquire_subway_tracer.py --mode bus`, then `--mode streetcar`, then `--mode lrt` (elevated network access).', '',
              'Executed profiles: `python3 scripts/profile_subway_tracer.py <provenance>` for each of the three new provenance paths above. Existing Subway results were read and independently reconciled, not regenerated.', '',
              'Verification/comparison command: `python3 scripts/verify_and_compare_modes.py`. It independently checks bytes/hash against provenance and HTTP Content-Length, exact manifest URLs and size, raw schema/row count, blanks/distinct values, numeric parsing, ISO dates/times, monthly counts, missing dates, weekday conflicts, both duration fields and percentiles, all category frequencies, _id sequence and four duplicate definitions. Every check passed for all four modes. All raw row counts match their manifest datastore counts.', '',
              'Reports refuse overwrite. No completed milestone documents, discovery metadata, Subway raw/provenance or Subway reports were changed. Git has no commits; session hashes provide the before/after comparison. No commit or push was performed. Stop here for review.']
    for path,value in [(ROOT/'reports/cross_mode_assessment.md','\n'.join(lines)+'\n'),(ROOT/'reports/cross_mode_verification.json',json.dumps(details,indent=2)+'\n')]:
        with path.open('x') as f:f.write(value)
    print('Wrote reports/cross_mode_assessment.md and reports/cross_mode_verification.json')

if __name__=='__main__':main()

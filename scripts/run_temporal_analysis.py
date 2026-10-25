"""Two monthly category profiles; reuse the existing read-only analytical contracts."""
import argparse
import json
import sqlite3
from pathlib import Path
try:
    from .run_core_analysis import ROOT, analyze, export, digest, require
except ImportError:
    from run_core_analysis import ROOT, analyze, export, digest, require

SQL_DIR=ROOT/'sql/analysis/persistence'


def nullable_sum(values):
    known=[v for v in values if v is not None]
    return sum(known) if known else None


def headline_audit(db):
    """Independently accumulate actual row values, not historical rounded percentages."""
    totals={}
    partitions={}
    for row in db.execute('''SELECT source_mode,code_raw,delay_minutes,scoped_delay_minutes_eligible
        FROM curated_records WHERE scope_eligible=1 AND incident_count_eligible=1
        ORDER BY snapshot_id,record_ordinal'''):
        mode,code,minutes,eligible=row
        t=totals.setdefault(mode,dict(incidents=0,duration_eligible=0,duration_ineligible=0,minutes=None,zeros=0))
        t['incidents']+=1;t['duration_eligible']+=eligible;t['duration_ineligible']+=1-eligible
        if eligible:
            t['minutes']=(t['minutes'] or 0)+minutes;t['zeros']+=int(minutes==0)
        if mode=='bus':
            # Both sets count source rows; >60 requires valid eligible duration, MFDV requires literal Code.
            key=('MFDV' if code=='MFDV' else 'other')+('__over60' if eligible and minutes>60 else '__not_over60')
            p=partitions.setdefault(key,dict(incidents=0,eligible_minutes=None,duration_eligible=0))
            p['incidents']+=1;p['duration_eligible']+=eligible
            if eligible:p['eligible_minutes']=(p['eligible_minutes'] or 0)+minutes
    return dict(mode_totals=totals,bus_disjoint_partitions=partitions)


def verify_profiles(results, core):
    expected={(r['source_mode'],r['month']):r for r in core['monthly']}
    for name, rows in results.items():
        groups={}
        for r in rows:groups.setdefault((r['source_mode'],r['month']),[]).append(r)
        require(groups.keys()==expected.keys(),'Mode-month coverage differs')
        for key, group in groups.items():
            target=expected[key]
            for metric in ['recorded_incidents','duration_eligible_incidents','duration_ineligible_incidents','zero_minute_incidents','duplicate_candidate_records']:
                column='duplicate_candidate_incidents' if metric=='duplicate_candidate_records' else metric
                require(sum(r[column] for r in group)==target[metric],f'{name}/{key}/{metric} mismatch')
            require(nullable_sum(r['recorded_delay_minutes'] for r in group)==target['recorded_delay_minutes'],'Category minute reconciliation failed')
            require(len({(r['category_eligible'],r['category_raw']) for r in group})==len(group),'Repeated category bucket')
            for r in group:
                require(r['mode_month_incidents']==target['recorded_incidents'],'Wrong incident denominator')
                require(r['mode_month_minutes']==target['recorded_delay_minutes'],'Wrong minute denominator')
                require(r['mode_month_duration_eligible']==target['duration_eligible_incidents'],'Wrong eligible denominator')
                require(r['mode_month_observed_dates']==target['observed_dates'],'Wrong coverage metadata')
                require(r['share_monthly_mode_incidents']==r['recorded_incidents']/target['recorded_incidents'],'Wrong count share')
                expected_share=(r['recorded_delay_minutes']/target['recorded_delay_minutes']
                                if r['recorded_delay_minutes'] is not None and target['recorded_delay_minutes'] not in (None,0) else None)
                require(r['share_monthly_mode_minutes']==expected_share,'Wrong minute share')
                missing=[x for x in group if not x['category_eligible']]
                require(r['mode_month_missing_category_incidents']==sum(x['recorded_incidents'] for x in missing),'Missing count metadata differs')
                require(r['mode_month_missing_category_minutes']==nullable_sum(x['recorded_delay_minutes'] for x in missing),'Missing minute metadata differs')
                require(r['category_eligible']==int(r['category_raw'] is not None),'Missing/raw bucket ambiguity')
                if r['category_eligible']==0:require(r['incident_rank'] is None and r['minute_rank'] is None,'Missing bucket ranked as raw category')
                n=r['duration_eligible_incidents']
                require(n+r['duration_ineligible_incidents']==r['recorded_incidents'],'Duration eligibility partition failed')
                require(r['zero_minute_incidents']<=n and r['over120_incidents']<=r['over60_incidents']<=n,'Duration subsets failed')
                require((r['recorded_delay_minutes'] is None)==(n==0),'Unknown duration converted to zero')
        # Independently check aggregate raw-category eligibility against existing full-period queries.
        old_name='raw_codes' if name=='monthly_codes' else 'raw_lines'
        old_key='code_raw' if name=='monthly_codes' else 'line_raw'
        old={(r['source_mode'],r[old_key]):r for r in core[old_name]}
        grouped={}
        for r in rows:
            if r['category_eligible']:grouped.setdefault((r['source_mode'],r['category_raw']),[]).append(r)
        require(grouped.keys()==old.keys(),'Raw eligible labels differ')
        for key,group in grouped.items():
            require(sum(r['recorded_incidents'] for r in group)==old[key]['recorded_incidents'],'Raw eligible count differs')
            require(nullable_sum(r['recorded_delay_minutes'] for r in group)==old[key]['recorded_delay_minutes'],'Raw eligible minutes differ')
    return dict(monthly_count_minutes_zero_eligibility_and_duplicate_reconciliation='passed',raw_category_reconciliation='passed')


def run(database,selection,staging=None):
    core,manifest=analyze(database,selection,staging)
    before=digest(database)
    with sqlite3.connect(Path(database).resolve().as_uri()+'?mode=ro',uri=True) as db:
        db.row_factory=sqlite3.Row;db.execute('PRAGMA query_only=ON');db.execute('BEGIN')
        require(json.loads(db.execute('SELECT selection_json FROM curated_metadata').fetchone()[0])==json.loads(Path(selection).read_text()),'Selection changed')
        results={};columns={}
        for path in sorted(SQL_DIR.glob('*.sql')):
            cursor=db.execute(path.read_text());columns[path.stem]=[c[0] for c in cursor.description]
            rows=[dict(r) for r in cursor]
            require(rows==[dict(r) for r in db.execute(path.read_text())],'Monthly queries not deterministic')
            results[path.stem]=rows
        checks=verify_profiles(results,core)
        headlines=headline_audit(db)
        for row in core['mode_summary']:
            actual=headlines['mode_totals'][row['source_mode']]
            require(actual['incidents']==row['recorded_incidents'] and actual['minutes']==row['recorded_delay_minutes'] and actual['zeros']==row['zero_minute_incidents'],'Independent headline audit differs')
    require(before==digest(database)==manifest['curated_sha256'],'Curated bytes changed')
    manifest['core_query_sha256']=manifest.pop('query_sha256')
    manifest['core_tooling_sha256']=manifest.pop('tooling_sha256')
    manifest.update(result_columns=columns,query_sha256={p.name:digest(p) for p in sorted(SQL_DIR.glob('*.sql'))},
                    tooling_sha256=digest(__file__),headlines=headlines)
    manifest['verification'].update(checks)
    return results,manifest


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--database',type=Path,default=ROOT/'data/local/ttc_curated.sqlite3')
    parser.add_argument('--selection',type=Path,default=ROOT/'config/curated_snapshots.json')
    parser.add_argument('--staging',type=Path,default=ROOT/'data/local/ttc.sqlite3')
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();results,manifest=run(args.database,args.selection,args.staging)
    export(results,manifest,args.output)
    print(json.dumps(dict(verification=manifest['verification'],headlines=manifest['headlines'],rows=manifest['result_row_counts']),indent=2))

if __name__=='__main__':main()

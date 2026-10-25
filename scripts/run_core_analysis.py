"""Execute read-only analytical SQL and export typed JSON plus CSV aggregates."""
import argparse
import csv
import hashlib
import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUERY_DIR = ROOT / 'sql/analysis'


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def query_results(db, columns=None):
    results = {}
    for path in sorted(QUERY_DIR.glob('*.sql')):
        cursor = db.execute(path.read_text())
        if columns is not None:
            columns[path.stem] = [c[0] for c in cursor.description]
        results[path.stem] = [dict(row) for row in cursor]
    return results


def require(condition, message):
    if not condition:
        raise ValueError(message)


def reconcile(db, results):
    """Check independent eligible totals and compatible aggregation partitions."""
    metrics = ['recorded_incidents', 'duration_eligible_incidents', 'recorded_delay_minutes',
               'zero_minute_incidents', 'positive_minute_incidents', 'duration_ineligible_incidents']
    by_mode = {r['source_mode']: r for r in results['mode_summary']}
    audit = {r['source_mode']: r for r in results['eligibility_audit']}
    independent = db.execute('''SELECT source_mode,COUNT(*) AS records,
      SUM(scoped_delay_minutes_eligible) AS eligible,
      SUM(CASE WHEN scoped_delay_minutes_eligible=1 THEN delay_minutes END) AS minutes,
      SUM(CASE WHEN scoped_delay_minutes_eligible=1 AND delay_minutes=0 THEN 1 ELSE 0 END) AS zeros
      FROM curated_records WHERE scope_eligible=1 AND incident_count_eligible=1 GROUP BY source_mode''')
    for raw in independent:
        summary = by_mode[raw['source_mode']]
        for key, actual in [('recorded_incidents',raw['records']),('duration_eligible_incidents',raw['eligible']),
                            ('recorded_delay_minutes',raw['minutes']),('zero_minute_incidents',raw['zeros'])]:
            require(summary[key] == actual, f'Independent totals differ: {key}')
        require(summary['zero_minute_incidents']+summary['positive_minute_incidents']==summary['duration_eligible_incidents'], 'Duration partition failed')
        require(summary['duration_eligible_incidents']+summary['duration_ineligible_incidents']==summary['recorded_incidents'], 'Eligibility partition failed')
    for mode, summary in by_mode.items():
        a = audit[mode]
        require(a['inventory_incidents']==a['scoped_incidents']+a['outside_or_unallocated_scope'], 'Scope partition failed')
        for name in ['monthly','duration_distribution','hourly','raw_lines','raw_codes','weekday_hour']:
            rows = [r for r in results[name] if r['source_mode']==mode]
            if name=='weekday_hour':
                rows = [r for r in rows if r['analysis_variant']=='all_date_derived_exploratory']
            predicate = {'hourly':'scoped_hour_eligible=1', 'raw_lines':'scoped_raw_line_eligible=1',
                         'raw_codes':'scoped_raw_code_eligible=1',
                         'weekday_hour':'scoped_hour_eligible=1 AND weekday_exploratory_eligible=1'}.get(name,'1=1')
            expected = db.execute(f'''SELECT COUNT(*),SUM(scoped_delay_minutes_eligible),
              SUM(CASE WHEN scoped_delay_minutes_eligible=1 THEN delay_minutes END),
              SUM(CASE WHEN scoped_delay_minutes_eligible=1 AND delay_minutes=0 THEN 1 ELSE 0 END),
              SUM(CASE WHEN scoped_delay_minutes_eligible=1 AND delay_minutes>0 THEN 1 ELSE 0 END),
              SUM(scoped_delay_minutes_eligible=0)
              FROM curated_records WHERE incident_count_eligible=1 AND scope_eligible=1 AND source_mode=? AND {predicate}''',(mode,)).fetchone()
            for index, key in enumerate(metrics):
                values = [r[key] for r in rows if r[key] is not None]
                total = sum(values) if values else (None if key=='recorded_delay_minutes' else 0)
                wanted = expected[index]
                if key!='recorded_delay_minutes' and wanted is None: wanted=0
                require(total==wanted, f'{mode}/{name}/{key}: {total} != {wanted}')
        sensitivity=[r for r in results['weekday_hour'] if r['source_mode']==mode and r['analysis_variant']=='conflict_excluded_exploratory']
        expected_sensitivity=db.execute('''SELECT COUNT(*),SUM(CASE WHEN scoped_delay_minutes_eligible=1 THEN delay_minutes END)
          FROM curated_records WHERE source_mode=? AND incident_count_eligible=1 AND scope_eligible=1
          AND scoped_hour_eligible=1 AND weekday_conflict_excluded_eligible=1''',(mode,)).fetchone()
        require(sum(r['recorded_incidents'] for r in sensitivity)==expected_sensitivity[0], 'Weekday sensitivity count failed')
        sensitivity_minutes=[r['recorded_delay_minutes'] for r in sensitivity if r['recorded_delay_minutes'] is not None]
        require((sum(sensitivity_minutes) if sensitivity_minutes else None)==expected_sensitivity[1], 'Weekday sensitivity minutes failed')
        for name, excluded in [('raw_lines','line'),('raw_codes','code')]:
            rows=[r for r in results[name] if r['source_mode']==mode]
            require(sum(r['recorded_incidents'] for r in rows)+a['excluded_raw_'+excluded]==summary['recorded_incidents'], 'Category exclusions failed')
            known_minutes=[r['recorded_delay_minutes'] for r in rows if r['recorded_delay_minutes'] is not None]
            excluded_minutes=a['excluded_'+excluded+'_minutes']
            available=known_minutes+([excluded_minutes] if excluded_minutes is not None else [])
            require((sum(available) if available else None)==summary['recorded_delay_minutes'], 'Category minute reconciliation failed')
        for r in [r for data in results.values() for r in data if r.get('source_mode')==mode and 'average_recorded_minutes' in r]:
            n=r['duration_eligible_incidents']
            require((r['average_recorded_minutes'] is None and r['median_recorded_minutes'] is None and r['zero_minute_share'] is None) if not n else abs(r['average_recorded_minutes']-r['recorded_delay_minutes']/n)<1e-9, 'Mean/NULL contract failed')
    return {'compatible_aggregation_partitions':'passed','independent_eligibility_totals':'passed'}


def analyze(database, selection_path, staging=None):
    database=Path(database).resolve()
    before=digest(database)
    config=json.loads(Path(selection_path).read_text())
    with sqlite3.connect(database.as_uri()+'?mode=ro',uri=True) as db:
        db.row_factory=sqlite3.Row
        db.execute('PRAGMA query_only=ON')
        db.execute('BEGIN')
        metadata=dict(db.execute('SELECT * FROM curated_metadata').fetchone())
        require(json.loads(metadata['selection_json'])==config, 'Explicit selection does not match curated build')
        actual=[dict(r) for r in db.execute('SELECT * FROM curated_selection ORDER BY snapshot_id')]
        selected={s['snapshot_id']:s for s in config['snapshots']}
        require(len(actual)==len(selected), 'Selection cardinality mismatch')
        for s in actual:
            expected=selected.get(s['snapshot_id'])
            require(expected is not None and all(s[k]==expected[e] for k,e in [('source_mode','mode'),('resource_id','resource_id'),('sha256','sha256')]), 'Snapshot identity mismatch')
            count=db.execute('SELECT COUNT(*) FROM curated_records WHERE snapshot_id=? AND source_mode=?',(s['snapshot_id'],s['source_mode'])).fetchone()[0]
            require(count==s['staged_record_count'], 'Selected snapshot count differs')
        require(db.execute('SELECT COUNT(*) FROM curated_records').fetchone()[0]==sum(s['staged_record_count'] for s in actual), 'Unselected or extra records')
        require(db.execute('PRAGMA integrity_check').fetchone()[0]=='ok','Integrity failure')
        require(not db.execute('PRAGMA foreign_key_check').fetchall(),'Foreign-key failure')
        lineage_count=None
        if staging is not None:
            db.execute('ATTACH DATABASE ? AS staging',(Path(staging).resolve().as_uri()+'?mode=ro',))
            lineage_count=db.execute('''SELECT COUNT(*) FROM curated_records c JOIN staging.staged_delay_records s
               ON c.snapshot_id=s.snapshot_id AND c.record_ordinal=s.record_ordinal''').fetchone()[0]
            require(lineage_count==sum(s['staged_record_count'] for s in actual),'Staging lineage mismatch')
            for s in actual:
                source=db.execute('SELECT resource_id,sha256,source_mode FROM staging.raw_snapshots WHERE snapshot_id=?',(s['snapshot_id'],)).fetchone()
                require(source is not None and all(source[k]==s[k] for k in source.keys()), 'Staging snapshot identity mismatch')
        columns={}
        results=query_results(db,columns)
        verification=reconcile(db,results)
        require(results==query_results(db), 'Repeated query results differ')
    require(digest(database)==before,'Curated database changed')
    verification.update(integrity_check='ok',foreign_key_violations=0,repeat_results_identical=True,
                        selected_records=sum(s['staged_record_count'] for s in actual),staging_lineage_records=lineage_count,
                        curated_bytes_unchanged=True)
    return results,dict(result_columns=columns,curated_sha256=before,selection=config,curated_metadata=metadata,verification=verification,
                       query_sha256={p.name:digest(p) for p in sorted(QUERY_DIR.glob('*.sql'))},
                       tooling_sha256=digest(__file__),
                       null_encoding='JSON null is authoritative; CSV empty cells represent SQL NULL. No missing duration is converted to zero.')


def export(results, manifest, output):
    output=Path(output)
    require(not output.exists(), 'Export directory already exists; choose a new directory to avoid silent overwrite')
    output.mkdir(parents=True)
    for name, rows in results.items():
        with (output/(name+'.csv')).open('w',newline='',encoding='utf-8') as f:
            writer=csv.DictWriter(f,fieldnames=manifest['result_columns'][name])
            writer.writeheader();writer.writerows(rows)
    (output/'results.json').write_text(json.dumps(results,indent=2,allow_nan=False)+'\n')
    manifest['result_row_counts']={k:len(v) for k,v in results.items()}
    manifest['export_sha256']={p.name:digest(p) for p in sorted(output.iterdir())}
    (output/'manifest.json').write_text(json.dumps(manifest,indent=2,allow_nan=False)+'\n')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--database',type=Path,default=ROOT/'data/local/ttc_curated.sqlite3')
    parser.add_argument('--selection',type=Path,default=ROOT/'config/curated_snapshots.json')
    parser.add_argument('--staging',type=Path,default=ROOT/'data/local/ttc.sqlite3')
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    results,manifest=analyze(args.database,args.selection,args.staging)
    export(results,manifest,args.output)
    print(json.dumps(manifest['verification'],indent=2))

if __name__=='__main__':main()

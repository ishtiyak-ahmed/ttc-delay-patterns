"""Package verified analytical aggregates for a bounded Power BI model; no database writes."""
import argparse
import hashlib
import json
import sqlite3
from pathlib import Path
try:
    from .run_core_analysis import ROOT, digest, export, require
    from .run_temporal_analysis import run, nullable_sum
    from .enrich_code_dimension import load_reference, enrich_dimension, REFERENCE, RECOVERY
except ImportError:
    from run_core_analysis import ROOT, digest, export, require
    from run_temporal_analysis import run, nullable_sum
    from enrich_code_dimension import load_reference, enrich_dimension, REFERENCE, RECOVERY

SQL=ROOT/'sql/power_bi/monthly_duration.sql'
MEASURES=['recorded_incidents','duration_eligible_incidents','duration_ineligible_incidents','recorded_delay_minutes','zero_minute_incidents']
BANDS=['zero','positive_0_to_5','over_5_to_15','over_15_to_30','over_30_to_60','over_60_to_120','over_120','unavailable_or_ineligible']


def load_bundle(folder):
    folder=Path(folder);manifest=json.loads((folder/'manifest.json').read_text())
    for name,h in manifest['export_sha256'].items():
        require(digest(folder/name)==h,f'Export checksum mismatch: {name}')
    return json.loads((folder/'results.json').read_text()),manifest


def category_key(mode,eligible,raw):
    encoded=json.dumps([mode,eligible,raw],ensure_ascii=False,separators=(',',':')).encode('utf-8')
    return hashlib.sha256(encoded).hexdigest()


def package(core,temporal,duration,manifest):
    """Only project existing measures/keys; do not clean raw labels or duplicate source facts."""
    modes=[]
    for selected in manifest['selection']['snapshots']:
        mode=selected['mode'];coverage=next(x for x in core['coverage'] if x['source_mode']==mode)
        quality=next(x for x in core['eligibility_audit'] if x['source_mode']==mode)
        modes.append(dict(source_mode=mode,snapshot_id=selected['snapshot_id'],resource_id=selected['resource_id'],raw_sha256=selected['sha256'],
             **{k:v for k,v in coverage.items() if k!='source_mode'},
             **{k:quality[k] for k in ['selected_records','outside_or_unallocated_scope','missing_date','invalid_date','missing_time','invalid_time','missing_delay','invalid_delay','negative_delay_records','validated_weekday_records']}))
    months=sorted({x['month'] for x in core['monthly']})
    data=dict(dim_mode=sorted(modes,key=lambda x:x['source_mode']),
        dim_month=[dict(month_start=m+'-01',month_label=m,year=int(m[:4]),month_number=int(m[5:])) for m in months],
        dim_duration_band=[dict(duration_band=b,sort_order=i,is_over60=int(b in ['over_60_to_120','over_120']),is_zero=int(b=='zero'),is_duration_eligible=int(b!='unavailable_or_ineligible')) for i,b in enumerate(BANDS)],
        fact_month=[],fact_duration=duration)
    for old in core['monthly']:
        candidates=[x for x in temporal['monthly_codes'] if x['source_mode']==old['source_mode'] and x['month']==old['month']]
        meta=candidates[0]
        line_meta=next(x for x in temporal['monthly_lines'] if x['source_mode']==old['source_mode'] and x['month']==old['month'])
        data['fact_month'].append(dict(source_mode=old['source_mode'],month_start=old['month']+'-01',
            **{k:old[k] for k in MEASURES+['observed_dates','weekday_conflicts','duplicate_candidate_records']},
            first_observed_date=meta['mode_month_first_date'],last_observed_date=meta['mode_month_last_date'],calendar_month_days=meta['calendar_month_days'],
            missing_code_incidents=meta['mode_month_missing_category_incidents'],missing_line_incidents=line_meta['mode_month_missing_category_incidents']))
    for kind,singular in [('codes','code'),('lines','line')]:
        dims={};facts=[]
        for old in temporal['monthly_'+kind]:
            key=category_key(old['source_mode'],old['category_eligible'],old['category_raw'])
            dims[key]=dict(**{singular+'_key':key},source_mode=old['source_mode'],category_eligible=old['category_eligible'],**{'raw_'+singular:old['category_raw']})
            facts.append(dict(source_mode=old['source_mode'],month_start=old['month']+'-01',**{singular+'_key':key},
                **{k:old[k] for k in MEASURES+['category_observed_dates','category_first_date','category_last_date']}))
        data['dim_'+singular]=[dims[k] for k in sorted(dims)]
        data['fact_'+singular]=facts
    # These are distinct source dates with NO selected records, not fabricated incident rows.
    data['reporting_gaps']=[dict(source_mode=x['source_mode'],month_start=x['calendar_date'][:7]+'-01',calendar_date=x['calendar_date']) for x in core['dates_without_records']]
    return data


def verify(data):
    mode_keys={x['source_mode'] for x in data['dim_mode']};month_keys={x['month_start'] for x in data['dim_month']}
    targets={(x['source_mode'],x['month_start']):x for x in data['fact_month']}
    require(len(targets)==len(data['fact_month']),'Duplicate mode-month')
    for kind in ['code','line']:
        dims=data['dim_'+kind];keys={x[kind+'_key']:x for x in dims}
        require(len(keys)==len(dims),'Duplicate dimension key')
        for row in data['fact_'+kind]:
            require(row[kind+'_key'] in keys and keys[row[kind+'_key']]['source_mode']==row['source_mode'],'Cross-mode category relationship')
    require(len({x['source_mode'] for x in data['dim_mode']})==len(data['dim_mode']),'Duplicate mode')
    require(len(month_keys)==len(data['dim_month']),'Duplicate month')
    for name in ['fact_code','fact_line','fact_duration']:
        groups={};seen=set()
        for row in data[name]:
            key=(row['source_mode'],row['month_start'])
            require(key[0] in mode_keys and key[1] in month_keys,'Invalid mode/month relationship')
            identity=key+((row['duration_band'],row['is_bus_mfdv']) if name=='fact_duration' else (row[name[5:]+'_key'],))
            require(identity not in seen,'Duplicate fact grain');seen.add(identity)
            groups.setdefault(key,[]).append(row)
            if name=='fact_duration':
                require(row['duration_band'] in BANDS,'Unknown duration band')
                require(row['is_bus_mfdv'] in (0,1) and (not row['is_bus_mfdv'] or row['source_mode']=='bus'),'Invalid MFDV membership')
        require(groups.keys()==targets.keys(),'Fact mode-month coverage mismatch')
        for key,group in groups.items():
            for metric in MEASURES:
                total=nullable_sum(x[metric] for x in group) if metric=='recorded_delay_minutes' else sum(x[metric] for x in group)
                require(total==targets[key][metric],f'{name}/{key}/{metric}: reconciliation failed')
    require(len({x['duration_band'] for x in data['dim_duration_band']})==len(data['dim_duration_band']),'Duplicate duration dimension')
    seen_gaps=set()
    for row in data['reporting_gaps']:
        require(row['source_mode'] in mode_keys and row['month_start'] in month_keys,'Invalid gap relationship')
        require(row['calendar_date'][:7]+'-01'==row['month_start'],'Gap month mismatch')
        key=(row['source_mode'],row['calendar_date'])
        require(key not in seen_gaps,'Duplicate gap date');seen_gaps.add(key)
    return dict(fact_grains_unique=True,dimension_keys_unique=True,relationships_valid=True,all_three_partitions_match_monthly_totals=True)


def build(database,selection,staging,core_folder,temporal_folder):
    core,cm=load_bundle(core_folder);temporal,tm=load_bundle(temporal_folder)
    require(cm['selection']==tm['selection']==json.loads(Path(selection).read_text()),'Export selection mismatch')
    require(cm['curated_sha256']==tm['curated_sha256']==digest(database),'Export artifact mismatch')
    for name,h in cm['query_sha256'].items():require(digest(ROOT/'sql/analysis'/name)==h,'Core SQL changed; regenerate source exports')
    for name,h in tm['query_sha256'].items():require(digest(ROOT/'sql/analysis/persistence'/name)==h,'Temporal SQL changed; regenerate source exports')
    require(cm['tooling_sha256']==digest(ROOT/'scripts/run_core_analysis.py'),'Core tooling changed')
    require(tm['tooling_sha256']==digest(ROOT/'scripts/run_temporal_analysis.py'),'Temporal tooling changed')
    fresh,verified=run(database,selection,staging)
    require(fresh==temporal,'Existing temporal values differ from actual database queries')
    with sqlite3.connect(Path(database).resolve().as_uri()+'?mode=ro',uri=True) as db:
        db.row_factory=sqlite3.Row;db.execute('PRAGMA query_only=ON');db.execute('BEGIN')
        duration=[dict(x) for x in db.execute(SQL.read_text())]
        require(duration==[dict(x) for x in db.execute(SQL.read_text())],'Duration export differs on rerun')
    require(digest(database)==cm['curated_sha256'],'Curated data changed')
    data=package(core,temporal,duration,verified)
    lookup,reference_manifest=load_reference()
    data['dim_code'],code_enrichment=enrich_dimension(data['dim_code'],data['fact_code'],lookup)
    code_enrichment.update(reference_version=reference_manifest['reference_version'],
        reference_manifest='references/ttc_delay_codes/2026-10-26/manifest.json',
        reference_manifest_sha256=digest(REFERENCE),
        recovery_evidence='config/code_description_recovery.json',
        recovery_evidence_sha256=digest(RECOVERY),
        implementation_sha256=digest(Path(__file__).with_name('enrich_code_dimension.py')))
    checks=verify(data)
    p=verified['headlines']['bus_disjoint_partitions']
    long_bands={'over_60_to_120','over_120'}
    overlap=[x for x in duration if x['source_mode']=='bus' and x['is_bus_mfdv'] and x['duration_band'] in long_bands]
    require(sum(x['recorded_incidents'] for x in overlap)==p.get('MFDV__over60',{'incidents':0})['incidents'],'Overlap counts differ')
    require(nullable_sum(x['recorded_delay_minutes'] for x in overlap)==p.get('MFDV__over60',{'eligible_minutes':None})['eligible_minutes'],'Overlap minutes differ')
    # Reconcile every disjoint Bus cohort, plus the original mode/band distribution.
    for is_mfdv in (0,1):
        for is_long in (False,True):
            key=('MFDV' if is_mfdv else 'other')+('__over60' if is_long else '__not_over60')
            group=[x for x in duration if x['source_mode']=='bus' and x['is_bus_mfdv']==is_mfdv and (x['duration_band'] in long_bands)==is_long]
            expected=p.get(key,dict(incidents=0,eligible_minutes=None))
            require(sum(x['recorded_incidents'] for x in group)==expected['incidents'],'Disjoint cohort counts differ')
            require(nullable_sum(x['recorded_delay_minutes'] for x in group)==expected['eligible_minutes'],'Disjoint cohort minutes differ')
    for target in core['duration_distribution']:
        group=[x for x in duration if x['source_mode']==target['source_mode'] and x['duration_band']==target['duration_band']]
        for metric in MEASURES:
            total=nullable_sum(x[metric] for x in group) if metric=='recorded_delay_minutes' else sum(x[metric] for x in group)
            require(total==target[metric],'Existing duration distribution differs')
    checks['duration_bands_and_all_bus_cohorts_reconciled']=True
    manifest=dict(contract_version='milestone5-v1',selection=verified['selection'],curated_sha256=verified['curated_sha256'],
        input_manifest_sha256=dict(core=digest(Path(core_folder)/'manifest.json'),temporal=digest(Path(temporal_folder)/'manifest.json')),
        source_query_sha256=dict(core=cm['query_sha256'],temporal=tm['query_sha256']),
        query_sha256={SQL.name:digest(SQL)},tooling_sha256=digest(__file__),
        result_columns={name:list(rows[0]) if rows else ['source_mode','month_start','calendar_date'] for name,rows in data.items()},
        verification=dict(**verified['verification'],**checks,bus_overlap_records=sum(x['recorded_incidents'] for x in overlap),bus_overlap_minutes=nullable_sum(x['recorded_delay_minutes'] for x in overlap)),
        code_enrichment=code_enrichment,
        null_encoding='CSV empty cell = SQL NULL; typed JSON is authoritative. No missing duration is zero-filled.')
    return data,manifest


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--database',type=Path,default=ROOT/'data/local/ttc_curated.sqlite3')
    p.add_argument('--selection',type=Path,default=ROOT/'config/curated_snapshots.json')
    p.add_argument('--staging',type=Path,default=ROOT/'data/local/ttc.sqlite3')
    p.add_argument('--core',type=Path,default=ROOT/'results/core_analysis')
    p.add_argument('--temporal',type=Path,default=ROOT/'results/temporal_persistence')
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args();data,m=build(args.database,args.selection,args.staging,args.core,args.temporal)
    export(data,m,args.output)
    print(json.dumps(dict(rows=m['result_row_counts'],verification=m['verification']),indent=2))

if __name__=='__main__':main()

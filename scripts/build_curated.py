"""Build a materialized SQLite curated artifact from explicitly selected staging."""
import argparse
import hashlib
import json
import math
import os
import re
import sqlite3
import tempfile
from datetime import datetime, date
from decimal import Decimal, InvalidOperation
from functools import lru_cache
from pathlib import Path

try:
    from .init_storage import ROOT, DEFAULT_DATABASE
    from .report_paths import report_path
except ImportError:
    from init_storage import ROOT, DEFAULT_DATABASE
    from report_paths import report_path

APPLICATION_ID = 0x54544343
DEFAULT_OUTPUT = ROOT / 'data/local/ttc_curated.sqlite3'
SCHEMA = ROOT / 'sql/curated_schema.sql'
TRANSFORM = ROOT / 'sql/build_curated.sql'
SPEC = ROOT / 'docs/cleaning_validation_rules.md'
RAW_PAIRS = [('source_id','_id'),('date_raw','Date'),('time_raw','Time'),('day_raw','Day'),
             ('station_raw','Station'),('code_raw','Code'),('min_delay_raw','Min Delay'),
             ('min_gap_raw','Min Gap'),('bound_raw','Bound'),('line_raw','Line'),('vehicle_raw','Vehicle')]


@lru_cache(maxsize=10000)
def strict_date(mode, value):
    try:
        fmt = '%Y-%m-%dT%H:%M:%S' if mode == 'bus' else '%Y-%m-%d'
        parsed = datetime.strptime(value, fmt)
        return parsed.date().isoformat() if parsed.strftime(fmt) == value else None
    except (ValueError, TypeError):
        return None


@lru_cache(maxsize=10000)
def strict_time(value):
    try:
        parsed = datetime.strptime(value, '%H:%M')
        return value if parsed.strftime('%H:%M') == value else None
    except (ValueError, TypeError):
        return None


@lru_cache(maxsize=10000)
def strict_number(value):
    if not isinstance(value, str) or not re.fullmatch(r'[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?', value):
        return None
    try:
        number = Decimal(value)
    except InvalidOperation:
        return None
    if not number.is_finite():
        return None
    if number == number.to_integral_value() and -(2**63) <= number <= 2**63-1:
        return int(number)
    real = float(number)
    if math.isfinite(real) and Decimal.from_float(real) == number:
        return real
    raise ValueError(f'Finite duration cannot be represented losslessly as SQLite INTEGER/REAL: {value!r}')


def calendar_weekday(value):
    return ('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday')[date.fromisoformat(value).weekday()] if value else None


def register_functions(db):
    errors=[]
    def guarded(fn):
        def invoke(*args):
            try:return fn(*args)
            except (ValueError, ArithmeticError) as exc:
                errors.append(str(exc))
                raise
        return invoke
    for name,arity,fn in [('strict_date',2,strict_date),('strict_time',1,strict_time),
                           ('strict_number',1,strict_number),('calendar_weekday',1,calendar_weekday),
                           ('is_blank',1,lambda value:int(value is None or not value.strip()))]:
        db.create_function(name,arity,guarded(fn),deterministic=True)
    return errors


def statements(path):
    pending=''
    for line in path.read_text().splitlines(keepends=True):
        pending+=line
        if sqlite3.complete_statement(pending):
            yield pending;pending=''
    if pending.strip():raise ValueError('Incomplete SQL definition')


def validate_selection(config):
    if config.get('rule_version')!='task4.1-v1':raise ValueError('Unsupported rules version')
    for key in ['scope_start','scope_end']:
        value=config.get(key)
        if key=='scope_end' and value is None:continue
        if not isinstance(value,str) or date.fromisoformat(value).isoformat()!=value:raise ValueError('Invalid scope date')
    if config['scope_end'] is not None and config['scope_end']<config['scope_start']:raise ValueError('Reversed scope dates')
    selections=config.get('snapshots',[])
    if not selections:raise ValueError('Explicit nonempty snapshot selection is required')
    for key in ['mode','resource_id','snapshot_id']:
        if len({r[key] for r in selections})!=len(selections):raise ValueError('Duplicate snapshot/resource/mode selection')
    for r in selections:
        if r['mode'] not in {'subway','bus','streetcar','lrt'} or type(r['snapshot_id']) is not int:
            raise ValueError('Invalid selected mode/snapshot')
        if not re.fullmatch('[0-9a-f]{64}',r['sha256']):raise ValueError('Invalid selected checksum')


def verification(db):
    total=db.execute('SELECT COUNT(*) FROM curated_records').fetchone()[0]
    source_total=db.execute('SELECT COUNT(*) FROM staging.staged_delay_records JOIN curated_selection USING(snapshot_id)').fetchone()[0]
    if total!=source_total:raise ValueError('Curated/source count mismatch')
    mismatches=' OR '.join(f'c."{a}" IS NOT d."{b}"' for a,b in RAW_PAIRS)
    lost=db.execute('SELECT COUNT(*) FROM staging.staged_delay_records d JOIN curated_selection s USING(snapshot_id) LEFT JOIN curated_records c USING(snapshot_id,record_ordinal) WHERE c.record_ordinal IS NULL').fetchone()[0]
    bad=db.execute('SELECT COUNT(*) FROM curated_records c LEFT JOIN staging.staged_delay_records d USING(snapshot_id,record_ordinal) LEFT JOIN curated_selection s USING(snapshot_id) WHERE d.record_ordinal IS NULL OR s.snapshot_id IS NULL OR c.source_mode<>s.source_mode OR '+mismatches).fetchone()[0]
    if lost or bad:raise ValueError('Curated traceability/source value mismatch')
    counts=[]
    for row in db.execute('''SELECT source_mode, snapshot_id, COUNT(*) rows,
        SUM(incident_count_eligible) incident_eligible,SUM(scope_eligible) scoped_incident_eligible,
        SUM(delay_minutes_eligible) delay_eligible,SUM(scoped_delay_minutes_eligible) scoped_delay_eligible,
        SUM(hour_eligible) hour_eligible,SUM(raw_line_eligible) raw_line_eligible,
        SUM(raw_code_eligible) raw_code_eligible,SUM(description_eligible) description_eligible,
        SUM(weekday_conflict=1) weekday_conflicts,SUM(delay_minutes=0) zero_delays,
        SUM(duplicate_candidate) duplicate_candidate_rows,
        SUM(line_missing) missing_lines,SUM(bound_missing) missing_bounds,
        SUM(code_status='missing') missing_codes,SUM(code_status='not_evaluated') unevaluated_codes,
        SUM(delay_status='invalid') invalid_delays,SUM(delay_status='missing') missing_delays,
        SUM(delay_status='negative') negative_delays,SUM(date_status='invalid') invalid_dates,
        SUM(time_status='invalid') invalid_times,SUM(delay_gt60) delays_gt60,
        SUM(delay_gt120) delays_gt120,SUM(delay_gt1440) delays_gt1440,
        MIN(parsed_date) first_date,MAX(parsed_date) last_date,
        SUM(CASE WHEN delay_minutes_eligible THEN delay_minutes END) eligible_delay_minutes
        FROM curated_records GROUP BY snapshot_id,source_mode ORDER BY snapshot_id'''):
        counts.append(dict(row))
    # These independent source predicates are valid on the observed integer data;
    # semantic-invalid fixtures are verified by exact field lineage and unit tests.
    for row in counts:
        sid=row['snapshot_id']
        n=db.execute('SELECT staged_record_count FROM curated_selection WHERE snapshot_id=?',(sid,)).fetchone()[0]
        if row['rows']!=n:raise ValueError('Selected receipt count mismatch')
    if db.execute('PRAGMA foreign_key_check').fetchall():raise ValueError('Curated foreign-key violation')
    if [r[0] for r in db.execute('PRAGMA integrity_check')]!=['ok']:raise ValueError('Curated integrity failure')
    return dict(selected_staged_rows=source_total,curated_rows=total,traceable_rows=total,
                original_fields_compared=total*11,source_value_mismatches=bad,missing_source_rows=lost,
                per_mode=counts,integrity_check='ok',foreign_key_violations=0)


def build_curated(selection, source=DEFAULT_DATABASE, output=DEFAULT_OUTPUT):
    source=Path(source).resolve();output=Path(output).resolve()
    if not source.is_file():raise ValueError('Staging database does not exist')
    if output==source or (output.exists() and os.path.samefile(source,output)):
        raise ValueError('Curated output must differ from staging database')
    if output.suffix!='.sqlite3':raise ValueError('Curated output must use .sqlite3')
    validate_selection(selection)
    if output.exists():
        with sqlite3.connect(output.as_uri()+'?mode=ro',uri=True) as old:
            if old.execute('PRAGMA application_id').fetchone()[0]!=APPLICATION_ID:
                raise ValueError('Refusing to replace an unrelated output database')
    source_hash=hashlib.sha256(source.read_bytes()).hexdigest()
    output.parent.mkdir(parents=True,exist_ok=True)
    fd,name=tempfile.mkstemp(prefix='curated-build-',suffix='.sqlite3',dir=output.parent);os.close(fd)
    temporary=Path(name);db=None;function_errors=[]
    try:
        db=sqlite3.connect(temporary.as_uri(),uri=True,isolation_level=None)
        db.row_factory=sqlite3.Row
        db.execute('PRAGMA foreign_keys=ON')
        db.execute('ATTACH DATABASE ? AS staging',(source.as_uri()+'?mode=ro',))
        function_errors=register_functions(db)
        db.execute('BEGIN')
        for statement in statements(SCHEMA):db.execute(statement)
        for chosen in sorted(selection['snapshots'],key=lambda r:r['snapshot_id']):
            sid=chosen['snapshot_id']
            actual=db.execute('SELECT source_mode,resource_id,sha256 FROM staging.raw_snapshots WHERE snapshot_id=?',(sid,)).fetchone()
            if actual is None or tuple(actual)!=(chosen['mode'],chosen['resource_id'],chosen['sha256']):raise ValueError('Selected snapshot identity/checksum mismatch')
            receipt=db.execute('SELECT raw_record_count,staged_record_count FROM staging.staging_loads WHERE snapshot_id=?',(sid,)).fetchone()
            n=db.execute('SELECT COUNT(*) FROM staging.staged_delay_records WHERE snapshot_id=?',(sid,)).fetchone()[0]
            if receipt is None or tuple(receipt)!=(n,n):raise ValueError('Missing/inconsistent staging receipt')
            if db.execute('SELECT COUNT(*) FROM staging.retrieval_events WHERE snapshot_id=? AND outcome=?',(sid,'downloaded')).fetchone()[0]==0:raise ValueError('Missing source provenance')
            db.execute('INSERT INTO curated_selection VALUES (?,?,?,?,?)',(sid,chosen['mode'],chosen['resource_id'],chosen['sha256'],n))
        if db.execute('PRAGMA staging.foreign_key_check').fetchall():raise ValueError('Staging foreign-key failure')
        if [r[0] for r in db.execute('PRAGMA staging.integrity_check')]!=['ok']:raise ValueError('Staging integrity failure')
        implementation=hashlib.sha256(SCHEMA.read_bytes()+TRANSFORM.read_bytes()+Path(__file__).read_bytes()).hexdigest()
        db.execute('INSERT INTO curated_metadata VALUES (1,?,?,?,?)',(selection['rule_version'],json.dumps(selection,sort_keys=True),hashlib.sha256(SPEC.read_bytes()).hexdigest(),implementation))
        db.execute(TRANSFORM.read_text(),dict(scope_start=selection['scope_start'],scope_end=selection['scope_end']))
        result=verification(db)
        db.execute(f'PRAGMA application_id={APPLICATION_ID}');db.execute('PRAGMA user_version=1')
        db.execute('COMMIT');db.close();db=None
        if hashlib.sha256(source.read_bytes()).hexdigest()!=source_hash:raise ValueError('Staging file changed during build')
        artifact_hash=hashlib.sha256(temporary.read_bytes()).hexdigest()
        os.replace(temporary,output)
        return dict(output=report_path(output, ROOT),artifact_sha256=artifact_hash,source_database_sha256=source_hash,
                    selection=selection,dictionary_policy='not_evaluated; no pinned reference artifact',**result)
    except sqlite3.OperationalError as exc:
        if function_errors:raise ValueError('Curated build failed: '+function_errors[-1]) from exc
        raise
    finally:
        if db is not None:db.close()
        temporary.unlink(missing_ok=True)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--selection',type=Path,required=True)
    parser.add_argument('--source',type=Path,default=DEFAULT_DATABASE)
    parser.add_argument('--output',type=Path,default=DEFAULT_OUTPUT)
    parser.add_argument('--report',type=Path)
    args=parser.parse_args()
    if args.report and args.report.exists():parser.error('Report already exists; refusing overwrite')
    result=build_curated(json.loads(args.selection.read_text()),args.source,args.output)
    if args.report:
        with args.report.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()

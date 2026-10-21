"""Independently compare staged SQLite rows to preserved raw CSVs, read-only."""
import argparse
import csv
import hashlib
import json
import sqlite3
from collections import Counter
from itertools import zip_longest
from pathlib import Path

try:
    from .init_storage import ROOT, DEFAULT_DATABASE
except ImportError:
    from init_storage import ROOT, DEFAULT_DATABASE


def verify_database(database=DEFAULT_DATABASE, root=ROOT):
    root = Path(root).resolve()
    db = sqlite3.connect(Path(database).resolve().as_uri() + '?mode=ro', uri=True)
    db.row_factory = sqlite3.Row
    try:
        db.execute('BEGIN')  # consistent read view across all snapshots
        snapshots = db.execute('SELECT * FROM raw_snapshots ORDER BY snapshot_id').fetchall()
        results = []
        for snapshot in snapshots:
            snapshot_id = snapshot['snapshot_id']
            events = db.execute('SELECT * FROM retrieval_events WHERE snapshot_id = ? AND outcome = ?', (snapshot_id,'downloaded')).fetchall()
            if not events:
                raise ValueError('Snapshot has no successful preserved retrieval')
            for event in events:
                matching_paths=db.execute('SELECT COUNT(*) FROM retrieval_events WHERE provenance_path = ?', (event['provenance_path'],)).fetchone()[0]
                if matching_paths != 1:
                    raise ValueError('Duplicate or rebound provenance path')
                provenance=json.loads((root/event['provenance_path']).read_text())
                body=(root/event['raw_path']).read_bytes()
                checksum=hashlib.sha256(body).hexdigest()
                if checksum != snapshot['sha256'] or checksum != provenance['sha256']:
                    raise ValueError('Raw/snapshot/provenance checksum mismatch')
                if len(body) != snapshot['file_size_bytes'] or len(body) != provenance['file_size_bytes']:
                    raise ValueError('Raw byte count mismatch')
                for key in ['resource_id','package_id']:
                    if snapshot[key] != provenance[key]:raise ValueError('Snapshot identity mismatch')
                if (provenance['status'] != 'downloaded' or event['resource_id'] != provenance['resource_id']
                        or event['source_url'] != provenance['source_url'] or event['raw_path'] != provenance['raw_path']
                        or event['final_url'] != provenance.get('final_url')
                        or event['started_at_utc'] != provenance['attempt_started_at_utc']
                        or event['finished_at_utc'] != provenance['retrieved_at_utc']
                        or event['http_status'] != provenance['http_status'] or event['http_status'] != 200
                        or json.loads(event['response_headers_json']) != provenance['response_headers']):
                    raise ValueError('Retrieval provenance mismatch')
            # Every retrieval has the same verified content hash. Compare source
            # rows once, not once per retrieval (which would multiply counts).
            event=events[0]
            body=(root/event['raw_path']).read_bytes()
            checksum=hashlib.sha256(body).hexdigest()
            with (root/event['raw_path']).open(encoding='utf-8-sig',newline='') as stream:
                reader=csv.DictReader(stream,strict=True)
                columns=reader.fieldnames
                if columns != json.loads(snapshot['original_columns_json']):raise ValueError('Header order mismatch')
                quoted=', '.join('"'+name.replace('"','""')+'"' for name in columns)
                cursor=db.execute(f'SELECT record_ordinal, {quoted} FROM staged_delay_records WHERE snapshot_id = ? ORDER BY record_ordinal',(snapshot_id,))
                count=0;blanks=Counter();zero_delays=0
                for count,(source,staged) in enumerate(zip_longest(reader,cursor),1):
                    if source is None or staged is None or None in source or any(v is None for v in source.values()):
                        raise ValueError(f'Source/staged row count or width mismatch in snapshot {snapshot_id}')
                    if staged[0] != count or list(staged)[1:] != [source[c] for c in columns]:
                        raise ValueError(f'Field mismatch in snapshot {snapshot_id}, record {count}')
                    blanks.update({c:int(source[c]=='') for c in columns})
                    # Exact retained zero text: no numeric cast or replacement.
                    zero_delays += source['Min Delay']=='0'
            receipt=db.execute('SELECT raw_record_count, staged_record_count FROM staging_loads WHERE snapshot_id = ?',(snapshot_id,)).fetchone()
            if receipt is None or tuple(receipt)!=(count,count):raise ValueError('Receipt count mismatch')
            results.append(dict(mode=snapshot['source_mode'],snapshot_id=snapshot_id,source_rows=count,staged_rows=count,
                                fields_compared=count*len(columns),exact_field_match=True,blank_strings=dict(blanks),
                                original_zero_delay_strings=zero_delays,sha256=checksum,checksum_verified=True,
                                provenance_path=event['provenance_path'],
                                provenance_paths=[e['provenance_path'] for e in events], retrieval_count=len(events)))
        foreign_keys=db.execute('PRAGMA foreign_key_check').fetchall()
        integrity=[row[0] for row in db.execute('PRAGMA integrity_check')]
        if foreign_keys or integrity!=['ok']:raise ValueError('Integrity or foreign-key check failed')
        traced=db.execute('SELECT COUNT(*) FROM staged_delay_records d WHERE EXISTS '
                         '(SELECT 1 FROM raw_snapshots s JOIN retrieval_events e USING(snapshot_id) '
                         'WHERE s.snapshot_id=d.snapshot_id AND e.outcome=?)',('downloaded',)).fetchone()[0]
        total=db.execute('SELECT COUNT(*) FROM staged_delay_records').fetchone()[0]
        if traced!=total or total!=sum(r['source_rows'] for r in results):raise ValueError('Untraced/unexpected staging rows')
        return dict(results=results,total_source_rows=sum(r['source_rows'] for r in results),total_staged_rows=total,
                    traced_records=traced,foreign_key_violations=0,integrity_check='ok',access='read-only',
                    scope='all preserved snapshot versions; totals are storage checks, not a current analytical dataset')
    finally:
        db.close()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--database',type=Path,default=DEFAULT_DATABASE)
    parser.add_argument('--report',type=Path)
    args=parser.parse_args()
    if args.report and args.report.exists():parser.error('Report already exists; refusing overwrite')
    result=verify_database(args.database)
    if args.report:
        with args.report.open('x',encoding='utf-8') as output:json.dump(result,output,indent=2);output.write('\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()

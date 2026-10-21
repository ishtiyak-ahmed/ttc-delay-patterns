"""Load explicitly selected local TTC snapshots into lossless SQLite staging."""
import argparse
import csv
import hashlib
import io
import json
import sqlite3
from collections import Counter
from datetime import date, datetime, timezone
from decimal import Decimal, InvalidOperation
from itertools import zip_longest
from pathlib import Path

try:
    from .init_storage import ROOT, DEFAULT_DATABASE, initialize_database
except ImportError:  # direct script invocation
    from init_storage import ROOT, DEFAULT_DATABASE, initialize_database

COLUMNS = ('_id', 'Date', 'Time', 'Day', 'Station', 'Code', 'Min Delay', 'Min Gap', 'Bound', 'Line', 'Vehicle')
QUOTED_COLUMNS = ', '.join('"' + name + '"' for name in COLUMNS)
PARSER_VERSION = 'ttc-csv-utf8-sig-v1'


def local_path(root, value):
    path = (root / value).resolve()
    try:
        relative = path.relative_to(root)
    except ValueError as exc:
        raise ValueError('Input paths must stay inside the project root') from exc
    if not path.is_file():
        raise ValueError(f'Required input file is missing: {relative}')
    return path, relative.as_posix()


def csv_reader(body):
    reader = csv.reader(io.StringIO(body.decode('utf-8-sig'), newline=''), strict=True)
    try:
        header = next(reader)
    except StopIteration as exc:
        raise ValueError('CSV has no header') from exc
    if len(header) != len(COLUMNS) or set(header) != set(COLUMNS):
        raise ValueError(f'Unexpected or duplicated CSV columns: {header!r}')
    return header, reader


def source_rows(body):
    header, reader = csv_reader(body)
    positions = [header.index(column) for column in COLUMNS]
    for ordinal, row in enumerate(reader, 1):
        if len(row) != len(header):
            raise ValueError(f'Malformed CSV data record {ordinal}: expected 11 fields, got {len(row)} (physical line {reader.line_num})')
        yield ordinal, tuple(row[position] for position in positions)


def summarize(rows):
    """Reconciliation diagnostics only: never alter or exclude staged values."""
    blanks = Counter(); empty = Counter(); duplicate_values = Counter()
    numeric = {c: dict(valid=0, blank=0, invalid=0, zero=0, negative=0, total=Decimal(0)) for c in ['Min Delay', 'Min Gap']}
    count = 0; dates = []; invalid_dates = 0
    for ordinal, values in rows:
        count += 1
        if ordinal != count:
            raise ValueError(f'Missing or unexpected record ordinal: {ordinal}, expected {count}')
        for column, value in zip(COLUMNS, values):
            if not isinstance(value, str):
                raise ValueError(f'Non-text staging value at record {ordinal}, column {column}')
            blanks[column] += not value.strip()
            empty[column] += value == ''
        duplicate_values[values[1:]] += 1
        try:
            dates.append(date.fromisoformat(values[1].split('T')[0]))
        except ValueError:
            invalid_dates += 1
        for column in numeric:
            value = values[COLUMNS.index(column)]; stats = numeric[column]
            if not value.strip():
                stats['blank'] += 1
                continue
            try:
                number = Decimal(value)
                if not number.is_finite():
                    raise InvalidOperation
            except InvalidOperation:
                stats['invalid'] += 1
                continue
            stats['valid'] += 1
            stats['zero'] += number == 0
            stats['negative'] += number < 0
            stats['total'] += number
    for stats in numeric.values():
        stats['total'] = str(stats['total'])
    return dict(row_count=count, blank_counts=dict(blanks), empty_string_counts=dict(empty), numeric=numeric,
                minimum_date=min(dates).isoformat() if dates else None,
                maximum_date=max(dates).isoformat() if dates else None, invalid_dates=invalid_dates,
                duplicate_groups_excluding_id=sum(n > 1 for n in duplicate_values.values()),
                duplicate_excess_excluding_id=sum(n - 1 for n in duplicate_values.values()))


def reconcile_snapshot(connection, snapshot_id, body):
    def database_rows():
        cursor = connection.execute(
            f'SELECT record_ordinal, {QUOTED_COLUMNS} FROM staged_delay_records WHERE snapshot_id = ? ORDER BY record_ordinal',
            (snapshot_id,))
        for row in cursor:
            yield row[0], tuple(row[1:])
    for source, staged in zip_longest(source_rows(body), database_rows()):
        if source != staged:
            ordinal = source[0] if source else staged[0]
            raise ValueError(f'Exact source/staging mismatch at record {ordinal}')
    raw_summary = summarize(source_rows(body))
    staged_summary = summarize(database_rows())
    if raw_summary != staged_summary:
        raise ValueError('Source and staged reconciliation metrics differ')
    return dict(exact_field_comparison=True, source=raw_summary, staged=staged_summary)


def prepare_input(provenance_path, root):
    path, provenance_relative = local_path(root, provenance_path)
    provenance_bytes = path.read_bytes()
    p = json.loads(provenance_bytes)
    if p.get('status') != 'downloaded' or p.get('http_status') != 200:
        raise ValueError('Only successful HTTP 200 download provenance can be ingested')
    manifest = json.loads((root / 'source_manifest.json').read_text())
    matches = [(package, resource) for package in manifest['packages'] for resource in package['resources']
               if resource['resource_id'] == p.get('resource_id') and package['package_id'] == p.get('package_id')]
    if len(matches) != 1:
        raise ValueError('Provenance package/resource identity does not match manifest')
    package, resource = matches[0]
    mode = package['package_name'].removeprefix('ttc-').removesuffix('-delay-data')
    if (mode not in {'subway', 'bus', 'streetcar', 'lrt'} or p.get('package_name') != package['package_name']
            or p.get('resource_name') != resource['name'] or resource['format'] != 'CSV'
            or p.get('source_url') != resource['url']):
        raise ValueError('Provenance source metadata disagrees with the selected manifest CSV')
    datastores = [r for r in package['resources'] if r['datastore_active'] and 'Code' not in r['name']]
    if len(datastores) != 1:
        raise ValueError('Cannot unambiguously resolve the related delay datastore')
    raw_path, raw_relative = local_path(root, p['raw_path'])
    body = raw_path.read_bytes()
    checksum = hashlib.sha256(body).hexdigest()
    if checksum != p.get('sha256') or len(body) != p.get('file_size_bytes') or not body:
        raise ValueError('Raw checksum/size mismatch against provenance')
    headers = p.get('response_headers')
    if not isinstance(headers, dict):
        raise ValueError('Expected recorded HTTP headers')
    content_lengths = [v for k, v in headers.items() if k.lower() == 'content-length']
    if content_lengths and int(content_lengths[0]) != len(body):
        raise ValueError('Raw size differs from recorded HTTP Content-Length')
    started, finished = p['attempt_started_at_utc'], p['retrieved_at_utc']
    times = [datetime.fromisoformat(v) for v in [started, finished]]
    if any(t.utcoffset() is None for t in times) or times[1] < times[0]:
        raise ValueError('Invalid retrieval timestamps')
    header, _ = csv_reader(body)
    return dict(provenance=p, provenance_bytes=provenance_bytes, provenance_path=path,
                provenance_relative=provenance_relative, raw_path=raw_path, raw_relative=raw_relative,
                body=body, header=header, mode=mode, datastore_id=datastores[0]['resource_id'])



def register_retrieval(connection, snapshot_id, prepared, allow_create=True):
    """One event per immutable provenance path, separate from snapshot identity.

    BEGIN IMMEDIATE in the caller serializes query/insert across loaders. A
    previously registered path must never be rebound to different metadata.
    """
    p = prepared['provenance']
    values = (snapshot_id, p['resource_id'], p['source_url'], p.get('final_url'),
              p['attempt_started_at_utc'], p['retrieved_at_utc'], 'downloaded', 200,
              json.dumps(p['response_headers']), prepared['raw_relative'], prepared['provenance_relative'])
    events = connection.execute(
        'SELECT retrieval_id, snapshot_id, resource_id, source_url, final_url, started_at_utc, finished_at_utc, '
        'outcome, http_status, response_headers_json, raw_path, provenance_path '
        'FROM retrieval_events WHERE provenance_path = ?', (prepared['provenance_relative'],)).fetchall()
    if events:
        if len(events) != 1:
            raise ValueError('Ambiguous duplicate provenance events; refusing repair')
        event = events[0]
        if (tuple(event[1:9]) != values[:8] or json.loads(event[9]) != p['response_headers']
                or tuple(event[10:]) != values[9:]):
            raise ValueError('Stored retrieval event disagrees with selected provenance; refusing overwrite')
        return event[0], False
    if not allow_create:
        raise ValueError('Selected provenance event is not registered; verify-only cannot insert it')
    cursor = connection.execute(
        'INSERT INTO retrieval_events (snapshot_id, resource_id, source_url, final_url, started_at_utc, '
        'finished_at_utc, outcome, http_status, response_headers_json, raw_path, provenance_path) '
        'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', values)
    return cursor.lastrowid, True


def ingest_snapshot(provenance_path, database=DEFAULT_DATABASE, root=ROOT, verify_only=False):
    root = Path(root).resolve()
    prepared = prepare_input(provenance_path, root)
    p = prepared['provenance']; body = prepared['body']
    if not Path(database).is_file():
        raise ValueError('Initialize the storage database before ingestion')
    # Verify the existing foundation; no migrations or schema changes.
    initialize_database(database)
    connection = sqlite3.connect(database, isolation_level=None, timeout=10)
    try:
        connection.execute('PRAGMA foreign_keys = ON')
        connection.execute('BEGIN IMMEDIATE')
        metadata = (p['package_id'], p['resource_id'], prepared['datastore_id'], prepared['mode'],
                    p['sha256'], p['file_size_bytes'], json.dumps(prepared['header']))
        existing = connection.execute(
            'SELECT snapshot_id, package_id, resource_id, datastore_resource_id, source_mode, sha256, file_size_bytes, original_columns_json '
            'FROM raw_snapshots WHERE resource_id = ? AND sha256 = ?', (p['resource_id'], p['sha256'])).fetchone()
        retrieval_registered = False
        if existing:
            snapshot_id = existing[0]
            if tuple(existing[1:]) != metadata:
                raise ValueError('Existing snapshot metadata conflict; refusing overwrite')
            receipt = connection.execute('SELECT parser_version, raw_record_count, staged_record_count, reconciliation_json FROM staging_loads WHERE snapshot_id = ?', (snapshot_id,)).fetchone()
            if not receipt or receipt[0] != PARSER_VERSION:
                raise ValueError('Existing snapshot has no compatible complete staging receipt')
            outcome = 'verified_existing'
        else:
            if verify_only:
                raise ValueError('Snapshot is not staged')
            snapshot_id = connection.execute(
                'INSERT INTO raw_snapshots (package_id, resource_id, datastore_resource_id, source_mode, sha256, file_size_bytes, original_columns_json) VALUES (?, ?, ?, ?, ?, ?, ?)', metadata).lastrowid
            retrieval_id, retrieval_registered = register_retrieval(connection, snapshot_id, prepared)
            statement = f'INSERT INTO staged_delay_records (snapshot_id, record_ordinal, {QUOTED_COLUMNS}) VALUES ({", ".join("?" for _ in range(13))})'
            # Streaming parser: a later malformed row rolls back earlier inserted rows too.
            connection.executemany(statement, ((snapshot_id, ordinal, *values) for ordinal, values in source_rows(body)))
            outcome = 'loaded'
        reconciliation = reconcile_snapshot(connection, snapshot_id, body)
        count = reconciliation['source']['row_count']
        if existing:
            if (receipt[1], receipt[2]) != (count, count) or json.loads(receipt[3]) != reconciliation:
                raise ValueError('Existing staging receipt differs from actual source/staged data')
        else:
            connection.execute(
                'INSERT INTO staging_loads (snapshot_id, parser_version, completed_at_utc, raw_record_count, staged_record_count, reconciliation_json) VALUES (?, ?, ?, ?, ?, ?)',
                (snapshot_id, PARSER_VERSION, datetime.now(timezone.utc).isoformat(), count, count, json.dumps(reconciliation)))
        retrieval_id, added = register_retrieval(connection, snapshot_id, prepared, allow_create=not verify_only)
        retrieval_registered = retrieval_registered or added
        if prepared['raw_path'].read_bytes() != body or prepared['provenance_path'].read_bytes() != prepared['provenance_bytes']:
            raise ValueError('Raw/provenance file changed during ingestion')
        if connection.execute('PRAGMA foreign_key_check').fetchall():
            raise ValueError('Foreign-key check failed')
        if connection.execute('PRAGMA integrity_check').fetchall() != [('ok',)]:
            raise ValueError('Database integrity check failed')
        connection.execute('COMMIT')
        return dict(mode=prepared['mode'], snapshot_id=snapshot_id, retrieval_id=retrieval_id,
                    retrieval_registered=retrieval_registered, resource_id=p['resource_id'],
                    sha256=p['sha256'], file_size_bytes=len(body), raw_path=prepared['raw_relative'],
                    provenance_path=prepared['provenance_relative'], outcome=outcome, reconciliation=reconciliation)
    except BaseException:
        if connection.in_transaction:
            connection.execute('ROLLBACK')
        raise
    finally:
        connection.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--database', type=Path, default=DEFAULT_DATABASE)
    parser.add_argument('--provenance', type=Path, nargs='+', required=True)
    parser.add_argument('--verify-only', action='store_true', help='Verify previously staged snapshots without inserting rows')
    parser.add_argument('--report', type=Path, help='Create a JSON report; refuse to overwrite')
    args = parser.parse_args()
    if args.report and args.report.exists():
        parser.error('Report already exists; refusing overwrite before any load')
    results = [ingest_snapshot(p, args.database, verify_only=args.verify_only) for p in args.provenance]
    selected_counts = {r['snapshot_id']: r['reconciliation']['source']['row_count'] for r in results}
    report = dict(parser_version=PARSER_VERSION, database=str(args.database.resolve()),
                  totals_scope='unique selected snapshot versions; not a current analytical dataset',
                  transaction_scope='one snapshot; earlier successful snapshots remain if a later snapshot fails',
                  results=results, total_source_rows=sum(selected_counts.values()),
                  total_staged_rows=sum(selected_counts.values()))
    if args.report:
        with args.report.open('x', encoding='utf-8') as output:
            json.dump(report, output, indent=2); output.write('\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()

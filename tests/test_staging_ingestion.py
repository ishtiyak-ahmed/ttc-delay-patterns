"""Offline staging tests: isolated fixtures, no network or real raw-file writes."""
import csv
import hashlib
import io
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.ingest_staging import COLUMNS, QUOTED_COLUMNS, ROOT, ingest_snapshot
from scripts.init_storage import initialize_database


class StagingFixture(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'data/raw').mkdir(parents=True)
        (self.root / 'data/provenance').mkdir(parents=True)
        self.manifest = json.loads((ROOT / 'source_manifest.json').read_text())
        (self.root / 'source_manifest.json').write_text(json.dumps(self.manifest))
        self.database = self.root / 'fixture.sqlite3'
        initialize_database(self.database)
        self.values = [
            ('0001', '2025-01-01', '02:10', ' Wednesday ', ' A, B\r\nSTOP ', 'UNKNOWN', '00', '', '', 'YU / BD', '0007'),
            ('0001', '2025-01-01', '02:10', ' Wednesday ', ' A, B\r\nSTOP ', 'UNKNOWN', '00', '', '', 'YU / BD', '0007'),
            ('9', 'not-a-date', 'bad-time', '', 'LOC', '', 'not-numeric', '-1', '8', '999', '0'),
        ]
        self.provenance = self.write_fixture(self.values)

    def write_fixture(self, values, header=COLUMNS, body=None, name="fixture"):
        if body is None:
            stream = io.StringIO(newline='')
            writer = csv.writer(stream)
            writer.writerow(header)
            for row in values:
                writer.writerow([row[COLUMNS.index(c)] for c in header] if len(row)==11 else row)
            body = stream.getvalue().encode('utf-8')
        (self.root / f'data/raw/{name}.csv').write_bytes(body)
        package = self.manifest['packages'][0]
        resource = next(r for r in package['resources'] if r['name']=='TTC Subway Delay Data since 2025.csv')
        p = dict(status='downloaded', http_status=200, package_id=package['package_id'], package_name=package['package_name'],
                 resource_id=resource['resource_id'], resource_name=resource['name'], source_url=resource['url'], final_url=resource['url'],
                 raw_path=f'data/raw/{name}.csv', sha256=hashlib.sha256(body).hexdigest(), file_size_bytes=len(body),
                 response_headers={'Content-Length': str(len(body))}, attempt_started_at_utc='2026-10-21T10:00:00+00:00',
                 retrieved_at_utc='2026-10-21T10:00:01+00:00')
        path = self.root / f'data/provenance/{name}.json'
        path.write_text(json.dumps(p))
        return path

    def load(self, **kwargs):
        return ingest_snapshot(self.provenance, self.database, root=self.root, **kwargs)

    def assert_empty(self):
        with sqlite3.connect(self.database) as db:
            for name in ['raw_snapshots','retrieval_events','staging_loads','staged_delay_records']:
                self.assertEqual(db.execute(f'SELECT COUNT(*) FROM {name}').fetchone()[0], 0, name)


class StagingIngestionTests(StagingFixture):
    def test_success_preserves_strings_blanks_duplicates_and_traceability(self):
        result = self.load()
        self.assertEqual(result['reconciliation']['source']['row_count'], 3)
        self.assertEqual(result['reconciliation']['source']['numeric']['Min Delay']['invalid'], 1)
        self.assertEqual(result['reconciliation']['source']['numeric']['Min Delay']['zero'], 2)
        with sqlite3.connect(self.database) as db:
            actual = db.execute(f'SELECT {QUOTED_COLUMNS} FROM staged_delay_records ORDER BY record_ordinal').fetchall()
            self.assertEqual(actual, self.values)
            trace = db.execute(
                'SELECT r.record_ordinal, s.source_mode, e.provenance_path FROM staged_delay_records r '
                'JOIN raw_snapshots s USING (snapshot_id) JOIN retrieval_events e USING (snapshot_id) ORDER BY r.record_ordinal').fetchall()
            self.assertEqual(trace, [(i,'subway','data/provenance/fixture.json') for i in range(1,4)])
            self.assertEqual(db.execute('PRAGMA foreign_key_check').fetchall(), [])

    def test_reordered_header_is_mapped_by_exact_names(self):
        self.provenance = self.write_fixture(self.values, header=tuple(reversed(COLUMNS)))
        self.load()
        with sqlite3.connect(self.database) as db:
            self.assertEqual(db.execute(f'SELECT {QUOTED_COLUMNS} FROM staged_delay_records ORDER BY record_ordinal').fetchall(), self.values)
            self.assertEqual(json.loads(db.execute('SELECT original_columns_json FROM raw_snapshots').fetchone()[0]), list(reversed(COLUMNS)))

    def test_checksum_mismatch_rejected_before_writes(self):
        with (self.root / 'data/raw/fixture.csv').open('ab') as output:
            output.write(b'changed')
        with self.assertRaisesRegex(ValueError, 'checksum/size mismatch'):
            self.load()
        self.assert_empty()

    def test_missing_raw_file_is_clear_failure(self):
        (self.root / 'data/raw/fixture.csv').unlink()
        with self.assertRaisesRegex(ValueError, 'missing'):
            self.load()
        self.assert_empty()

    def test_malformed_later_record_rolls_back_entire_snapshot(self):
        self.provenance = self.write_fixture([self.values[0], ('too','short')])
        with self.assertRaisesRegex(ValueError, 'Malformed CSV data record 2'):
            self.load()
        self.assert_empty()

    def test_unclosed_quote_rolls_back(self):
        body = (','.join(COLUMNS) + '\n"unterminated').encode()
        self.provenance = self.write_fixture([], body=body)
        with self.assertRaises(csv.Error):
            self.load()
        self.assert_empty()

    def test_invalid_encoding_is_not_replaced(self):
        self.provenance = self.write_fixture([], body=b'\xffbad')
        with self.assertRaises(UnicodeDecodeError):
            self.load()
        self.assert_empty()

    def test_duplicate_header_is_rejected(self):
        self.provenance = self.write_fixture([], header=('_id',)*11)
        with self.assertRaisesRegex(ValueError, 'duplicated CSV columns'):
            self.load()
        self.assert_empty()

    def test_inconsistent_source_identity_is_rejected(self):
        p=json.loads(self.provenance.read_text());p['source_url']='https://example.invalid/wrong.csv'
        self.provenance.write_text(json.dumps(p))
        with self.assertRaisesRegex(ValueError, 'disagrees'):
            self.load()
        self.assert_empty()

    def test_reconciliation_failure_rolls_back_inserted_rows_and_metadata(self):
        def fail_after_inserts(db, snapshot_id, body):
            self.assertEqual(db.execute('SELECT COUNT(*) FROM staged_delay_records').fetchone()[0], 3)
            self.assertEqual(db.execute('SELECT COUNT(*) FROM retrieval_events').fetchone()[0], 1)
            raise ValueError('Injected reconciliation failure')
        with patch('scripts.ingest_staging.reconcile_snapshot', side_effect=fail_after_inserts):
            with self.assertRaisesRegex(ValueError, 'Injected reconciliation failure'):
                self.load()
        self.assert_empty()

    def test_existing_snapshot_is_verified_without_overwrite(self):
        first=self.load();before=self.database.read_bytes()
        result=self.load(verify_only=True)
        self.assertEqual(result['outcome'], 'verified_existing')
        self.assertEqual(first['snapshot_id'], result['snapshot_id'])
        self.assertEqual(before, self.database.read_bytes())

    def test_same_count_but_changed_staged_value_is_rejected_not_repaired(self):
        self.load()
        with sqlite3.connect(self.database) as db:
            db.execute('UPDATE staged_delay_records SET "Code" = ? WHERE record_ordinal = 1', ('TAMPERED',))
        before=self.database.read_bytes()
        with self.assertRaisesRegex(ValueError, 'Exact source/staging mismatch'):
            self.load(verify_only=True)
        self.assertEqual(before,self.database.read_bytes())


if __name__ == '__main__':
    unittest.main()

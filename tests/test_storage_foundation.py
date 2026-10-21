"""Foundation tests use disposable databases, with no CSV or staging ingestion."""
import sqlite3
import tempfile
import unittest
from pathlib import Path

from scripts.init_storage import initialize_database, schema_signature


class StorageFoundationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.database = Path(self.temp.name) / 'test.sqlite3'

    def test_repeat_initialization_preserves_empty_database(self):
        first = initialize_database(self.database)
        original = self.database.read_bytes()
        second = initialize_database(self.database)
        self.assertEqual(first, second)
        self.assertEqual(original, self.database.read_bytes())
        self.assertEqual(first['row_counts'], {
            'raw_snapshots': 0, 'retrieval_events': 0,
            'staged_delay_records': 0, 'staging_loads': 0,
        })
        with sqlite3.connect(self.database) as db:
            fields = db.execute('PRAGMA table_info(staged_delay_records)').fetchall()
            source_fields = fields[2:]
            self.assertEqual(len(source_fields), 11)
            self.assertTrue(all(field[2] == 'TEXT' and field[3] == 1 for field in source_fields))
            self.assertEqual(db.execute('PRAGMA foreign_key_check').fetchall(), [])

    def test_unrelated_database_is_rejected_without_changes(self):
        with sqlite3.connect(self.database) as db:
            db.execute('CREATE TABLE unrelated (value TEXT)')
        original = self.database.read_bytes()
        with self.assertRaisesRegex(RuntimeError, 'mismatch'):
            initialize_database(self.database)
        self.assertEqual(original, self.database.read_bytes())

    def test_changed_schema_is_rejected_without_repair(self):
        initialize_database(self.database)
        with sqlite3.connect(self.database) as db:
            db.execute('ALTER TABLE staged_delay_records ADD COLUMN unwanted TEXT')
        original = self.database.read_bytes()
        with self.assertRaisesRegex(RuntimeError, 'mismatch'):
            initialize_database(self.database)
        self.assertEqual(original, self.database.read_bytes())

    def test_unsupported_version_is_rejected(self):
        initialize_database(self.database)
        with sqlite3.connect(self.database) as db:
            db.execute('PRAGMA user_version = 2')
        original = self.database.read_bytes()
        with self.assertRaisesRegex(RuntimeError, 'mismatch'):
            initialize_database(self.database)
        self.assertEqual(original, self.database.read_bytes())


if __name__ == '__main__':
    unittest.main()

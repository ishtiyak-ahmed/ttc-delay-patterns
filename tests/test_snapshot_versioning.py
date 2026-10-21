"""Offline versioning and interruption tests, entirely in disposable fixtures."""
import json
import io
from contextlib import redirect_stdout
import sqlite3
import subprocess
import sys
from unittest.mock import patch

from test_staging_ingestion import StagingFixture
from scripts.ingest_staging import COLUMNS, QUOTED_COLUMNS, ROOT, ingest_snapshot, source_rows
from scripts.verify_staging import verify_database


class SnapshotVersioningTests(StagingFixture):
    def counts(self):
        with sqlite3.connect(self.database) as db:
            return tuple(db.execute(f'SELECT COUNT(*) FROM {table}').fetchone()[0]
                         for table in ['raw_snapshots','retrieval_events','staging_loads','staged_delay_records'])

    def rows(self, snapshot_id):
        with sqlite3.connect(self.database) as db:
            return db.execute(f'SELECT {QUOTED_COLUMNS} FROM staged_delay_records WHERE snapshot_id=? ORDER BY record_ordinal', (snapshot_id,)).fetchall()

    def revision(self):
        changed=list(self.values[0]);changed[COLUMNS.index('Min Delay')]='18'
        return [tuple(changed),self.values[2]]  # same IDs, changed values, fewer records

    def test_identical_normal_rerun_is_byte_preserving_no_op(self):
        original=self.load();before=self.database.read_bytes()
        again=self.load()
        self.assertEqual(again['outcome'],'verified_existing')
        self.assertFalse(again['retrieval_registered'])
        self.assertEqual(original['snapshot_id'],again['snapshot_id'])
        self.assertEqual(original['retrieval_id'],again['retrieval_id'])
        self.assertEqual(self.counts(),(1,1,1,3))
        self.assertEqual(before,self.database.read_bytes())

    def test_revised_resource_coexists_and_keeps_both_versions_traceable(self):
        old=self.load();original_raw=(self.root/'data/raw/fixture.csv').read_bytes()
        revised=self.write_fixture(self.revision(),name='revision')
        new=ingest_snapshot(revised,self.database,root=self.root)
        self.assertEqual(old['resource_id'],new['resource_id'])
        self.assertNotEqual(old['sha256'],new['sha256'])
        self.assertNotEqual(old['snapshot_id'],new['snapshot_id'])
        self.assertEqual(self.rows(old['snapshot_id']),self.values)
        self.assertEqual(self.rows(new['snapshot_id']),self.revision())
        self.assertEqual(self.counts(),(2,2,2,5))
        self.assertEqual(original_raw,(self.root/'data/raw/fixture.csv').read_bytes())
        verified=verify_database(self.database,self.root)
        self.assertEqual(verified['total_staged_rows'],5)  # all stored versions, never claimed as current
        self.assertEqual({r['provenance_path'] for r in verified['results']},
                         {'data/provenance/fixture.json','data/provenance/revision.json'})
        before=self.database.read_bytes()
        ingest_snapshot(revised,self.database,root=self.root)
        self.assertEqual(self.counts(),(2,2,2,5))
        self.assertEqual(before,self.database.read_bytes())

    def test_reordering_is_distinct_content_without_incident_identity_claims(self):
        old=self.load()
        reordered=self.write_fixture(list(reversed(self.values)),name='reordered')
        new=ingest_snapshot(reordered,self.database,root=self.root)
        self.assertNotEqual(old['sha256'],new['sha256'])
        self.assertCountEqual(self.rows(old['snapshot_id']),self.rows(new['snapshot_id']))
        self.assertEqual(self.rows(new['snapshot_id']),list(reversed(self.values)))
        self.assertNotIn('new_incidents',new)
        self.assertEqual(self.counts(),(2,2,2,6))

    def test_second_retrieval_same_bytes_adds_only_one_event(self):
        old=self.load()
        later=self.write_fixture(self.values,name='later_retrieval')
        p=json.loads(later.read_text());p['attempt_started_at_utc']='2026-10-22T10:00:00+00:00';p['retrieved_at_utc']='2026-10-22T10:00:01+00:00'
        later.write_text(json.dumps(p))
        new=ingest_snapshot(later,self.database,root=self.root)
        self.assertEqual(old['snapshot_id'],new['snapshot_id'])
        self.assertTrue(new['retrieval_registered'])
        self.assertEqual(self.counts(),(1,2,1,3))
        again=ingest_snapshot(later,self.database,root=self.root)
        self.assertFalse(again['retrieval_registered'])
        self.assertEqual(self.counts(),(1,2,1,3))
        verified=verify_database(self.database,self.root)
        self.assertEqual(verified['total_staged_rows'],3)
        self.assertEqual(verified['results'][0]['retrieval_count'],2)
        self.assertEqual(len(verified['results'][0]['provenance_paths']),2)

    def test_verify_only_cannot_register_a_new_retrieval(self):
        self.load();later=self.write_fixture(self.values,name='not_registered')
        before=self.database.read_bytes()
        with self.assertRaisesRegex(ValueError,'verify-only cannot insert'):
            ingest_snapshot(later,self.database,root=self.root,verify_only=True)
        self.assertEqual(before,self.database.read_bytes())

    def test_midstream_exception_rolls_back_revision_then_retry_succeeds(self):
        old=self.load();revised=self.write_fixture(self.revision(),name='retry')
        before=self.database.read_bytes()
        def interrupt(body):
            for ordinal,values in source_rows(body):
                if ordinal==2:
                    raise OSError('Simulated read interruption after first inserted record')
                yield ordinal,values
        with patch('scripts.ingest_staging.source_rows',side_effect=interrupt):
            with self.assertRaisesRegex(OSError,'Simulated read interruption'):
                ingest_snapshot(revised,self.database,root=self.root)
        self.assertEqual(before,self.database.read_bytes())
        self.assertEqual(self.counts(),(1,1,1,3))
        new=ingest_snapshot(revised,self.database,root=self.root)
        self.assertEqual(self.counts(),(2,2,2,5))
        self.assertEqual(self.rows(old['snapshot_id']),self.values)
        self.assertEqual(self.rows(new['snapshot_id']),self.revision())

    def test_abrupt_process_exit_mid_load_recovers_and_retries(self):
        old=self.load();revised=self.write_fixture(self.revision(),name='process_exit')
        code='''
import os,sys
from pathlib import Path
from scripts import ingest_staging as loader
original=loader.source_rows
def interrupt(body):
    for ordinal,values in original(body):
        if ordinal==2:os._exit(73)
        yield ordinal,values
loader.source_rows=interrupt
loader.ingest_snapshot(Path(sys.argv[1]),Path(sys.argv[2]),root=Path(sys.argv[3]))
'''
        result=subprocess.run([sys.executable,'-c',code,str(revised),str(self.database),str(self.root)],cwd=ROOT,capture_output=True,text=True,timeout=15)
        self.assertEqual(result.returncode,73,result.stderr)
        self.assertEqual(self.counts(),(1,1,1,3))  # reopening performs SQLite recovery if needed
        new=ingest_snapshot(revised,self.database,root=self.root)
        self.assertEqual(self.counts(),(2,2,2,5))
        self.assertEqual(self.rows(old['snapshot_id']),self.values)
        self.assertEqual(self.rows(new['snapshot_id']),self.revision())
        self.assertEqual(verify_database(self.database,self.root)['integrity_check'],'ok')

    def test_revised_checksum_mismatch_preserves_previous_snapshot(self):
        old=self.load();revised=self.write_fixture(self.revision(),name='bad_checksum')
        with (self.root/'data/raw/bad_checksum.csv').open('ab') as out:out.write(b'changed')
        before=self.database.read_bytes()
        with self.assertRaisesRegex(ValueError,'checksum/size mismatch'):
            ingest_snapshot(revised,self.database,root=self.root)
        self.assertEqual(before,self.database.read_bytes())
        self.assertEqual(self.counts(),(1,1,1,3))
        self.assertEqual(self.rows(old['snapshot_id']),self.values)

    def test_reusing_provenance_path_for_changed_content_is_rejected(self):
        old=self.load();self.provenance=self.write_fixture(self.revision())  # intentional invalid fixture overwrite
        before=self.database.read_bytes()
        with self.assertRaisesRegex(ValueError,'refusing overwrite'):
            self.load()
        self.assertEqual(before,self.database.read_bytes())
        self.assertEqual(self.counts(),(1,1,1,3))
        self.assertEqual(self.rows(old['snapshot_id']),self.values)

    def test_external_partial_state_requires_review_not_silent_repair(self):
        self.load()
        with sqlite3.connect(self.database) as db:db.execute('DELETE FROM staging_loads')
        before=self.database.read_bytes()
        with self.assertRaisesRegex(ValueError,'no compatible complete staging receipt'):
            self.load()
        self.assertEqual(before,self.database.read_bytes())

    def test_duplicate_cli_inputs_do_not_double_count_selected_totals(self):
        from scripts.ingest_staging import main
        def fixture_load(provenance, database, verify_only=False):
            return ingest_snapshot(provenance, database, root=self.root, verify_only=verify_only)
        output=io.StringIO()
        argv=['ingest_staging.py','--database',str(self.database),'--provenance',str(self.provenance),str(self.provenance)]
        with patch('sys.argv',argv), patch('scripts.ingest_staging.ingest_snapshot',side_effect=fixture_load), redirect_stdout(output):
            main()
        result=json.loads(output.getvalue())
        self.assertEqual(result['total_source_rows'],3)
        self.assertEqual(result['total_staged_rows'],3)
        self.assertEqual(self.counts(),(1,1,1,3))

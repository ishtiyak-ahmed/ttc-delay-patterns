"""Offline curated contracts and version isolation using disposable SQLite files."""
import json
import sqlite3
from pathlib import Path
from test_staging_ingestion import StagingFixture
from scripts.ingest_staging import ingest_snapshot
from scripts.build_curated import build_curated, strict_date, strict_time, strict_number


class CuratedLayerTests(StagingFixture):
    def selection(self, result):
        return dict(rule_version='task4.1-v1',scope_start='2025-01-01',scope_end=None,
                    snapshots=[dict(mode=result['mode'],snapshot_id=result['snapshot_id'],
                                    resource_id=result['resource_id'],sha256=result['sha256'])])

    def build(self, selection=None):
        if selection is None:selection=self.selection(self.load())
        return build_curated(selection,self.database,self.root/'curated.sqlite3')

    def records(self):
        with sqlite3.connect(self.root/'curated.sqlite3') as db:
            db.row_factory=sqlite3.Row
            return [dict(r) for r in db.execute('SELECT * FROM curated_records ORDER BY record_ordinal')]

    def test_strict_parsing_and_lossless_numeric_representation(self):
        self.assertEqual(strict_date('subway','2024-02-29'),'2024-02-29')
        self.assertIsNone(strict_date('subway','2025-02-29'))
        self.assertIsNone(strict_date('subway','2025-1-01'))
        self.assertEqual(strict_date('bus','2025-01-01T12:34:56'),'2025-01-01')
        self.assertIsNone(strict_date('bus','2025-01-01'))
        self.assertEqual(strict_time('00:00'),'00:00')
        for value in ['24:00','7:10','00:60','bad','']:self.assertIsNone(strict_time(value))
        for value in ['', ' ', 'NaN', 'Infinity', '1_000', '12oops']:self.assertIsNone(strict_number(value))
        self.assertEqual(strict_number('00'),0)
        self.assertEqual(strict_number('-2'),-2)
        self.assertEqual(strict_number('1.25'),1.25)
        with self.assertRaisesRegex(ValueError,'losslessly'):strict_number('0.1')

    def test_zero_blank_duplicates_source_strings_and_lineage(self):
        result=self.build();rows=self.records()
        self.assertEqual(result['curated_rows'],3)
        self.assertEqual([r['record_ordinal'] for r in rows],[1,2,3])
        self.assertEqual(rows[0]['source_id'],'0001')
        self.assertEqual(rows[0]['station_raw'],' A, B\r\nSTOP ')
        self.assertEqual(rows[0]['delay_minutes'],0)
        self.assertIsNone(rows[0]['gap_value'])
        self.assertEqual(rows[0]['gap_status'],'missing')
        self.assertEqual(rows[0]['bound_raw'],'')
        self.assertEqual([r['duplicate_group_size'] for r in rows],[2,2,1])
        self.assertEqual([r['duplicate_candidate'] for r in rows],[1,1,0])
        self.assertEqual(rows[0]['code_status'],'not_evaluated')
        self.assertIsNone(rows[0]['code_description'])
        self.assertEqual(rows[0]['description_eligible'],0)
        self.assertEqual(rows[0]['gap_semantic_status'],'unresolved')

    def test_analysis_specific_eligibility_preserves_invalid_records(self):
        self.build();rows=self.records();bad=rows[2]
        self.assertEqual(bad['incident_count_eligible'],1)
        self.assertEqual(bad['date_status'],'invalid')
        self.assertEqual(bad['scope_eligible'],0)
        self.assertEqual(bad['time_status'],'invalid')
        self.assertIsNone(bad['hour_of_day'])
        self.assertEqual(bad['hour_eligible'],0)
        self.assertEqual(bad['delay_status'],'invalid')
        self.assertIsNone(bad['delay_minutes'])
        self.assertEqual(bad['delay_minutes_eligible'],0)
        self.assertEqual(bad['raw_line_eligible'],1)
        self.assertEqual(bad['raw_code_eligible'],0)
        self.assertEqual(bad['code_status'],'missing')
        self.assertEqual(bad['gap_value'],-1)
        self.assertEqual(bad['canonical_route_eligible'],0)
        self.assertEqual(rows[0]['delay_minutes_eligible'],1)
        self.assertEqual(rows[0]['hour_of_day'],2)

    def test_weekday_conflict_retains_original_and_derived(self):
        self.build();row=self.records()[0]
        self.assertEqual(row['day_raw'],' Wednesday ')
        self.assertEqual(row['derived_weekday'],'Wednesday')
        self.assertEqual(row['day_status'],'unrecognized')
        self.assertEqual(row['weekday_conflict'],1)
        self.assertEqual(row['weekday_exploratory_eligible'],1)
        self.assertEqual(row['weekday_conflict_excluded_eligible'],0)
        self.assertEqual(row['validated_weekday_eligible'],0)

    def test_snapshot_version_isolation_and_explicit_checksum(self):
        first=self.load();old_selection=self.selection(first)
        modified=list(self.values[0]);modified[6]='18'
        provenance=self.write_fixture([tuple(modified)],name='revision')
        revised=ingest_snapshot(provenance,self.database,root=self.root)
        source_bytes=self.database.read_bytes()
        self.build(old_selection)
        self.assertEqual(len(self.records()),3)
        self.assertEqual({r['snapshot_id'] for r in self.records()},{first['snapshot_id']})
        self.build(self.selection(revised))
        self.assertEqual(len(self.records()),1)
        self.assertEqual(self.records()[0]['delay_minutes'],18)
        self.assertEqual(source_bytes,self.database.read_bytes())
        bad=self.selection(first);bad['snapshots'][0]['sha256']='0'*64
        with self.assertRaisesRegex(ValueError,'identity/checksum'):self.build(bad)
        self.assertEqual(len(self.records()),1)
        duplicate=self.selection(first);duplicate['snapshots'].append(self.selection(revised)['snapshots'][0])
        with self.assertRaisesRegex(ValueError,'Duplicate'):self.build(duplicate)

    def test_repeat_build_is_deterministic_and_staging_loader_still_works(self):
        selection=self.selection(self.load());source=self.database.read_bytes()
        first=self.build(selection);output=(self.root/'curated.sqlite3').read_bytes()
        second=self.build(selection)
        self.assertEqual(first,second)
        self.assertEqual(output,(self.root/'curated.sqlite3').read_bytes())
        self.assertEqual(source,self.database.read_bytes())
        self.assertEqual(self.load(verify_only=True)['outcome'],'verified_existing')

    def test_unrepresentable_decimal_fails_without_replacing_previous_artifact(self):
        self.build();before=(self.root/'curated.sqlite3').read_bytes()
        value=list(self.values[0]);value[6]='0.1'
        provenance=self.write_fixture([tuple(value)],name='precision')
        result=ingest_snapshot(provenance,self.database,root=self.root)
        with self.assertRaisesRegex(ValueError,'losslessly'):self.build(self.selection(result))
        self.assertEqual(before,(self.root/'curated.sqlite3').read_bytes())
        self.assertEqual(list(self.root.glob('curated-build-*.sqlite3')),[])

    def test_negative_delay_and_missing_line_have_separate_eligibility(self):
        value=list(self.values[0]);value[6]='-2';value[9]='';value[3]='Wednesday'
        self.provenance=self.write_fixture([tuple(value)])
        self.build();row=self.records()[0]
        self.assertEqual(row['delay_minutes'],-2)
        self.assertEqual(row['delay_status'],'negative')
        self.assertEqual(row['incident_count_eligible'],1)
        self.assertEqual(row['delay_minutes_eligible'],0)
        self.assertEqual(row['hour_eligible'],1)
        self.assertEqual(row['raw_code_eligible'],1)
        self.assertEqual(row['raw_line_eligible'],0)
        self.assertEqual(row['weekday_conflict'],0)

    def test_output_cannot_replace_source(self):
        selection=self.selection(self.load())
        with self.assertRaisesRegex(ValueError,'differ from staging'):
            build_curated(selection,self.database,self.database)

    def test_blank_delay_does_not_erase_hour_or_incident_eligibility(self):
        value=list(self.values[0]);value[6]='';value[3]='Wednesday'
        self.provenance=self.write_fixture([tuple(value)])
        self.build();row=self.records()[0]
        self.assertEqual(row['min_delay_raw'],'')
        self.assertIsNone(row['delay_minutes'])
        self.assertEqual(row['delay_status'],'missing')
        self.assertEqual(row['delay_minutes_eligible'],0)
        self.assertEqual(row['incident_count_eligible'],1)
        self.assertEqual(row['hour_eligible'],1)
        self.assertEqual(row['raw_code_eligible'],1)

    def test_explicit_scope_filters_eligibility_not_record_preservation(self):
        selection=self.selection(self.load());selection['scope_start']='2026-01-01'
        self.build(selection);rows=self.records()
        self.assertEqual(len(rows),3)
        self.assertTrue(all(row['scope_eligible']==0 for row in rows))
        self.assertTrue(all(row['incident_count_eligible']==1 for row in rows))
        self.assertEqual(rows[0]['delay_minutes_eligible'],1)
        self.assertEqual(rows[0]['scoped_delay_minutes_eligible'],0)

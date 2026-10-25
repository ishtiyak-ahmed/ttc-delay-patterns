"""Offline SQL measure and aggregation invariants on synthetic curated builds."""
import json
import sqlite3
from test_staging_ingestion import StagingFixture
from scripts.ingest_staging import ingest_snapshot
from scripts.build_curated import build_curated
from scripts.run_core_analysis import analyze, export


class CoreAnalysisTests(StagingFixture):
    def prepare(self, durations, blank_categories=False, invalid_time=False, same_weekday=False):
        values=[]
        for i, duration in enumerate(durations):
            values.append((str(i),'2025-01-01','bad' if invalid_time else '02:10',
                           'Tuesday' if i==0 and not same_weekday else 'Wednesday','LOC',
                           '' if blank_categories else 'UNKNOWN',duration,'','','' if blank_categories else 'RAW / A','0'))
        self.provenance=self.write_fixture(values)
        loaded=self.load()
        self.selection=dict(rule_version='task4.1-v1',scope_start='2025-01-01',scope_end=None,
            snapshots=[dict(mode=loaded['mode'],snapshot_id=loaded['snapshot_id'],resource_id=loaded['resource_id'],sha256=loaded['sha256'])])
        self.config=self.root/'selection.json';self.config.write_text(json.dumps(self.selection))
        self.curated=self.root/'curated.sqlite3'
        build_curated(self.selection,self.database,self.curated)
        return analyze(self.curated,self.config,self.database)

    def test_measures_zero_missing_invalid_negative_and_even_median(self):
        r,m=self.prepare(['0','2','4','10','','bad','-2'])
        s=r['mode_summary'][0]
        self.assertEqual(s['recorded_incidents'],7)
        self.assertEqual(s['duration_eligible_incidents'],4)
        self.assertEqual(s['duration_ineligible_incidents'],3)
        self.assertEqual(s['recorded_delay_minutes'],16)
        self.assertEqual(s['average_recorded_minutes'],4)
        self.assertEqual(s['median_recorded_minutes'],3)
        self.assertEqual(s['zero_minute_incidents'],1)
        self.assertEqual(s['zero_minute_share'],.25)
        self.assertEqual(sum(x['recorded_incidents'] for x in r['monthly']),7)
        self.assertTrue(m['verification']['repeat_results_identical'])

    def test_odd_median_and_conflict_sensitivity(self):
        r,_=self.prepare(['0','6','12'])
        self.assertEqual(r['mode_summary'][0]['median_recorded_minutes'],6)
        self.assertEqual(r['mode_summary'][0]['weekday_conflicts'],1)
        variants={x['analysis_variant']:x['recorded_incidents'] for x in r['weekday_hour']}
        self.assertEqual(variants,{'all_date_derived_exploratory':3,'conflict_excluded_exploratory':2})

    def test_all_unknown_durations_are_null_not_zero_and_empty_csv_has_header(self):
        r,m=self.prepare(['','bad'],blank_categories=True,invalid_time=True)
        s=r['mode_summary'][0]
        for key in ['recorded_delay_minutes','average_recorded_minutes','median_recorded_minutes','zero_minute_share']:
            self.assertIsNone(s[key])
        self.assertEqual(s['zero_minute_incidents'],0)
        self.assertEqual(r['raw_lines'],[]);self.assertEqual(r['raw_codes'],[]);self.assertEqual(r['hourly'],[])
        self.assertEqual(r['eligibility_audit'][0]['excluded_raw_line'],2)
        out=self.root/'exports';export(r,m,out)
        self.assertTrue((out/'raw_lines.csv').read_text().startswith('source_mode,line_raw,'))
        with self.assertRaisesRegex(ValueError,'already exists'):export(r,m,out)

    def test_revised_staging_snapshot_does_not_enter_analysis(self):
        first,_=self.prepare(['0','10'])
        changed=list(self.values[0]);changed[6]='999'
        provenance=self.write_fixture([changed],name='revision')
        ingest_snapshot(provenance,self.database,root=self.root)
        second,_=analyze(self.curated,self.config,self.database)
        self.assertEqual(first,second)
        self.selection['snapshots'][0]['snapshot_id']+=1
        self.config.write_text(json.dumps(self.selection))
        with self.assertRaisesRegex(ValueError,'selection'):analyze(self.curated,self.config,self.database)

    def test_duplicate_candidates_and_exact_labels_retained_repeat_exports(self):
        r,m=self.prepare(['0','0','10'],same_weekday=True)
        self.assertEqual(r['mode_summary'][0]['duplicate_candidate_records'],2)
        self.assertEqual(r['raw_lines'][0]['line_raw'],'RAW / A')
        self.assertEqual(r['raw_codes'][0]['code_raw'],'UNKNOWN')
        self.assertEqual(r['raw_lines'][0]['recorded_incidents'],3)
        r2,m2=analyze(self.curated,self.config,self.database)
        out1=self.root/'a';out2=self.root/'b'
        export(r,m,out1);export(r2,m2,out2)
        self.assertEqual({p.name:p.read_bytes() for p in out1.iterdir()}, {p.name:p.read_bytes() for p in out2.iterdir()})

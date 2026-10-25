"""Offline monthly category shares, eligibility, coverage and lineage tests."""
import json
import sqlite3
from test_staging_ingestion import StagingFixture
from scripts.build_curated import build_curated
from scripts.ingest_staging import ingest_snapshot
from scripts.run_temporal_analysis import run, headline_audit
from scripts.run_core_analysis import export


class TemporalAnalysisTests(StagingFixture):
    def prepare(self, values):
        self.provenance=self.write_fixture(values)
        loaded=self.load()
        self.config=self.root/'selection.json'
        self.selection=dict(rule_version='task4.1-v1',scope_start='2025-01-01',scope_end=None,
          snapshots=[dict(mode=loaded['mode'],snapshot_id=loaded['snapshot_id'],resource_id=loaded['resource_id'],sha256=loaded['sha256'])])
        self.config.write_text(json.dumps(self.selection));self.curated=self.root/'curated.sqlite3'
        build_curated(self.selection,self.database,self.curated)
        return run(self.curated,self.config,self.database)

    def value(self,day='2025-01-01',code='A',line=' RAW / X ',minutes='0',id='1'):
        return (id,day,'02:10','Wednesday','LOC',code,minutes,'','',''+line,'0')

    def test_monthly_shares_missing_buckets_zero_and_invalid_duration(self):
        r,_=self.prepare([self.value(),self.value(code='',line=' ',minutes='10',id='2'),
                         self.value(code='A',minutes='bad',id='3'),self.value(day='2025-02-01',code='B',minutes='4',id='4')])
        for name in r:
            jan=[x for x in r[name] if x['month']=='2025-01']
            named=next(x for x in jan if x['category_eligible'])
            missing=next(x for x in jan if not x['category_eligible'])
            self.assertEqual(named['recorded_incidents'],2)
            self.assertEqual(named['duration_eligible_incidents'],1)
            self.assertEqual(named['duration_ineligible_incidents'],1)
            self.assertEqual(named['zero_minute_incidents'],1)
            self.assertEqual(named['share_monthly_mode_incidents'],2/3)
            self.assertEqual(named['share_monthly_mode_minutes'],0)
            self.assertEqual(missing['recorded_delay_minutes'],10)
            self.assertEqual(missing['share_monthly_mode_minutes'],1)
            self.assertIsNone(missing['category_raw']);self.assertIsNone(missing['minute_rank'])
            self.assertEqual(named['mode_month_missing_category_incidents'],1)
        self.assertEqual(next(x for x in r['monthly_lines'] if x['category_eligible'])['category_raw'],' RAW / X ')

    def test_unknown_and_zero_denominators_remain_null(self):
        r,_=self.prepare([self.value(minutes=''),self.value(day='2025-02-01',minutes='0')])
        for name in r:
            jan=next(x for x in r[name] if x['month']=='2025-01');feb=next(x for x in r[name] if x['month']=='2025-02')
            self.assertIsNone(jan['recorded_delay_minutes']);self.assertIsNone(jan['share_monthly_mode_minutes'])
            self.assertIsNone(jan['minute_rank'])
            self.assertEqual(feb['recorded_delay_minutes'],0);self.assertIsNone(feb['share_monthly_mode_minutes'])

    def test_tied_ranks_partial_date_coverage_and_duplicate_retention(self):
        r,_=self.prepare([self.value(minutes='61'),self.value(minutes='61'),self.value(code='B',line='B',minutes='122'),self.value(code='B',line='B')])
        for name in r:
            self.assertEqual([x['incident_rank'] for x in r[name]],[1,1])
            self.assertEqual([x['minute_rank'] for x in r[name]],[1,1])
            self.assertEqual(sum(x['recorded_incidents'] for x in r[name]),4)
            self.assertEqual(sum(x['duplicate_candidate_incidents'] for x in r[name]),2)
            self.assertEqual(sum(x['over60_incidents'] for x in r[name]),3)
            self.assertEqual(sum(x['over120_incidents'] for x in r[name]),1)
            self.assertEqual(r[name][0]['mode_month_observed_dates'],1)
            self.assertEqual(r[name][0]['calendar_month_days'],31)

    def test_selected_version_isolation_and_wrong_selection(self):
        self.prepare([self.value()])
        p=self.write_fixture([self.value(minutes='999')],name='revision')
        ingest_snapshot(p,self.database,root=self.root)
        r,_=run(self.curated,self.config,self.database)
        self.assertEqual(r['monthly_codes'][0]['recorded_incidents'],1)
        self.assertEqual(r['monthly_codes'][0]['recorded_delay_minutes'],0)
        self.selection['snapshots'][0]['snapshot_id']+=1;self.config.write_text(json.dumps(self.selection))
        with self.assertRaisesRegex(ValueError,'selection'):run(self.curated,self.config,self.database)

    def test_bus_overlap_partitions_are_disjoint(self):
        self.prepare([self.value(code='MFDV',minutes='61'),self.value(code='MFDV',minutes='0'),self.value(code='A',minutes='90'),self.value(code='A',minutes='bad')])
        # Only disposable fixture values are adapted to exercise Bus-specific audit logic.
        with sqlite3.connect(self.curated) as db:
            db.execute("UPDATE curated_records SET source_mode='bus'")
            h=headline_audit(db)
        self.assertEqual(sum(x['incidents'] for x in h['bus_disjoint_partitions'].values()),4)
        self.assertEqual(h['bus_disjoint_partitions']['MFDV__over60']['eligible_minutes'],61)
        self.assertEqual(h['bus_disjoint_partitions']['other__not_over60']['duration_eligible'],0)
        self.assertIsNone(h['bus_disjoint_partitions']['other__not_over60']['eligible_minutes'])

    def test_exports_repeat_byte_for_byte_and_refuse_overwrite(self):
        r,m=self.prepare([self.value()]);r2,m2=run(self.curated,self.config,self.database)
        a=self.root/'a';b=self.root/'b';export(r,m,a);export(r2,m2,b)
        self.assertEqual({p.name:p.read_bytes() for p in a.iterdir()},{p.name:p.read_bytes() for p in b.iterdir()})
        with self.assertRaisesRegex(ValueError,'already exists'):export(r,m,a)

"""Offline Power BI bundle grains, filter keys, NULLs and export integrity."""
import copy
import json
import sqlite3
from test_staging_ingestion import StagingFixture
from scripts.build_curated import build_curated
from scripts.run_core_analysis import analyze, export
from scripts.run_temporal_analysis import run
from scripts.export_power_bi import build, verify, category_key


class PowerBIContractTests(StagingFixture):
    def prepare(self):
        # Two named categories and one missing category; zero, positive, and unknown durations.
        values=[('1','2025-01-01','00:00','Wednesday','LOC','MFDV','0','','','A','0'),
                ('2','2025-01-02','01:00','Thursday','LOC','X','61','','',' A ','0'),
                ('3','2025-02-01','02:00','Saturday','LOC','','','','','','0')]
        self.provenance=self.write_fixture(values);loaded=self.load()
        selection=dict(rule_version='task4.1-v1',scope_start='2025-01-01',scope_end=None,
          snapshots=[dict(mode=loaded['mode'],snapshot_id=loaded['snapshot_id'],resource_id=loaded['resource_id'],sha256=loaded['sha256'])])
        self.config=self.root/'selection.json';self.config.write_text(json.dumps(selection))
        self.curated=self.root/'curated.sqlite3';build_curated(selection,self.database,self.curated)
        self.core=self.root/'core';self.temporal=self.root/'temporal'
        r,m=analyze(self.curated,self.config,self.database);export(r,m,self.core)
        r,m=run(self.curated,self.config,self.database);export(r,m,self.temporal)
        self.args=(self.curated,self.config,self.database,self.core,self.temporal)
        return build(*self.args)

    def test_partitions_zero_null_and_raw_key_preservation(self):
        data,m=self.prepare()
        for name in ['fact_month','fact_code','fact_line','fact_duration']:
            self.assertEqual(sum(x['recorded_incidents'] for x in data[name]),3)
            self.assertEqual(sum(x['zero_minute_incidents'] for x in data[name]),1)
            self.assertEqual(sum(x['duration_eligible_incidents'] for x in data[name]),2)
            unknown=[x for x in data[name] if x['month_start']=='2025-02-01']
            self.assertTrue(all(x['recorded_delay_minutes'] is None for x in unknown))
        self.assertEqual({x['raw_line'] for x in data['dim_line']},{'A',' A ',None})
        self.assertEqual(m['verification']['bus_overlap_records'],0)
        # Literal MFDV outside Bus is not in the Bus-MFDV cohort.
        self.assertTrue(all(x['is_bus_mfdv']==0 for x in data['fact_duration']))

    def test_mode_and_missing_keys_cannot_collide(self):
        self.assertNotEqual(category_key('bus',1,'A'),category_key('subway',1,'A'))
        self.assertNotEqual(category_key('bus',0,None),category_key('bus',1,'(Missing raw Code)'))
        self.assertNotEqual(category_key('bus',1,'A'),category_key('bus',1,' A '))
        self.assertNotEqual(category_key('bus',1,'a|b'),category_key('bus|a',1,'b'))

    def test_duplicate_fact_or_orphan_dimension_rejected(self):
        data,_=self.prepare();bad=copy.deepcopy(data)
        bad['fact_duration'].append(copy.deepcopy(bad['fact_duration'][0]))
        with self.assertRaisesRegex(ValueError,'Duplicate fact grain'):verify(bad)
        bad=copy.deepcopy(data);bad['fact_code'][0]['code_key']='orphan'
        with self.assertRaisesRegex(ValueError,'relationship'):verify(bad)
        bad=copy.deepcopy(data);bad['fact_line'][0]['recorded_incidents']+=1
        with self.assertRaisesRegex(ValueError,'reconciliation'):verify(bad)

    def test_input_corruption_rejected_before_export(self):
        self.prepare()
        p=self.core/'monthly.csv';p.write_text(p.read_text()+'bad\n')
        with self.assertRaisesRegex(ValueError,'checksum mismatch'):build(*self.args)

    def test_repeated_build_exports_identical_and_protect_inputs(self):
        data,m=self.prepare();before=self.curated.read_bytes();staging=self.database.read_bytes()
        data2,m2=build(*self.args)
        a=self.root/'a';b=self.root/'b';export(data,m,a);export(data2,m2,b)
        self.assertEqual({p.name:p.read_bytes() for p in a.iterdir()},{p.name:p.read_bytes() for p in b.iterdir()})
        self.assertEqual(before,self.curated.read_bytes());self.assertEqual(staging,self.database.read_bytes())
        with self.assertRaisesRegex(ValueError,'already exists'):export(data,m,a)

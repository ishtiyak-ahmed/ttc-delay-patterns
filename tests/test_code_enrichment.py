"""Offline, fail-closed official-reference enrichment and dimension preservation."""
import copy
import json
import tempfile
import unittest
from pathlib import Path
from scripts.enrich_code_dimension import (prepare_lookup, enrich_dimension, load_reference,
    REFERENCE, ORIGINAL_COLUMNS, ADDED_COLUMNS, encoding_defect)


class CodeEnrichmentTests(unittest.TestCase):
    def dimension(self, mode='bus', code='A', key='k', eligible=1):
        return dict(code_key=key, source_mode=mode, category_eligible=eligible, raw_code=code)

    def enrich(self, rows, refs):
        facts=[dict(code_key=r['code_key'], recorded_incidents=3) for r in rows]
        return enrich_dimension(rows, facts, prepare_lookup(refs))

    def test_exact_cross_mode_lookup_and_original_columns_preserved(self):
        rows=[self.dimension(),self.dimension('streetcar','A','s')]
        original=copy.deepcopy(rows)
        out,audit=self.enrich(rows,{'bus':[dict(CODE='A',DESCRIPTION='BUS DESCRIPTION')],
                                  'streetcar':[dict(CODE='A',DESCRIPTION='STREETCAR DESCRIPTION')]})
        self.assertEqual(rows,original)
        self.assertEqual([r['code_description'] for r in out],['BUS DESCRIPTION','STREETCAR DESCRIPTION'])
        self.assertEqual(out[0]['code_display_label'],'A — BUS DESCRIPTION')
        for before,after in zip(rows,out):
            self.assertEqual(list(after),ORIGINAL_COLUMNS+ADDED_COLUMNS)
            self.assertEqual({k:after[k] for k in ORIGINAL_COLUMNS},before)
        missing,_=self.enrich([self.dimension(code=' A ')],{'bus':[dict(CODE='A',DESCRIPTION='KNOWN')]})
        self.assertIsNone(missing[0]['code_description'])
        self.assertEqual(missing[0]['code_display_label'],' A  — Description unavailable')

    def test_missing_mapping_blank_code_and_missing_description_stay_unresolved(self):
        rows=[self.dimension(code='ABSENT',key='a'),self.dimension(code=None,key='b',eligible=0),self.dimension(code='EMPTY',key='c')]
        out,audit=self.enrich(rows,{'bus':[dict(CODE='EMPTY',DESCRIPTION=' ')]})
        self.assertTrue(all(r['code_description'] is None for r in out))
        self.assertEqual([r['code_display_label'] for r in out],
                         ['ABSENT — Description unavailable',
                          'Code not recorded — Description unavailable',
                          'EMPTY — Description unavailable'])
        self.assertEqual({r['status'] for r in audit['unresolved_codes']},{'unmapped','missing_code','missing_description'})

    def test_identical_reference_duplicates_collapse_without_incident_deduplication(self):
        refs={'lrt':[dict(CODE='TXSUP',DESCRIPTION='SUPERVISORY ERROR')]*2}
        lookup=prepare_lookup(refs)
        self.assertEqual(lookup[('lrt','TXSUP')]['source_rows'],2)
        rows=[self.dimension('lrt','TXSUP','x'),self.dimension('lrt','TXSUP','y')]
        out,audit=self.enrich(rows,refs)
        self.assertEqual(len(out),2)
        self.assertTrue(all(r['code_description']=='SUPERVISORY ERROR' for r in out))
        self.assertEqual(audit['coverage']['lrt']['accepted']['incident_records'],6)

    def test_conflicting_reference_is_not_resolved_by_first_match(self):
        refs={'lrt':[dict(CODE='EXVE',DESCRIPTION='WORK VEHICLE'),dict(CODE='EXVE',DESCRIPTION='VEHICLE (SOURCE OF PROBLEM NOT KNOWN)')]}
        out,audit=self.enrich([self.dimension('lrt','EXVE')],refs)
        self.assertIsNone(out[0]['code_description'])
        self.assertEqual(out[0]['code_display_label'],'EXVE — Description unavailable')
        self.assertEqual(audit['unresolved_codes'][0]['status'],'ambiguous')

    def test_encoding_defects_are_not_repaired_or_published_as_accepted(self):
        for description in ['BAD \ufffd TEXT','BAD â\x80\x93 TEXT','BAD â€“ TEXT','BAD Ã© TEXT']:
            self.assertTrue(encoding_defect(description))
            out,audit=self.enrich([self.dimension()],{'bus':[dict(CODE='A',DESCRIPTION=description)]})
            self.assertIsNone(out[0]['code_description'])
            self.assertEqual(out[0]['code_display_label'],'A — Description unavailable')
            self.assertEqual(audit['unresolved_codes'][0]['status'],'encoding_defect')
        self.assertFalse(encoding_defect('ÉQUIPMENT – OTHER'))

    def test_null_empty_and_whitespace_codes_have_readable_labels_without_source_changes(self):
        rows=[self.dimension(code=code,key=str(i),eligible=0)
              for i,code in enumerate([None, '', ' \t '])]
        original=copy.deepcopy(rows)
        out,_=self.enrich(rows,{})
        self.assertEqual(rows,original)
        for before,after in zip(original,out):
            self.assertEqual({k:after[k] for k in ORIGINAL_COLUMNS},before)
            self.assertIsNone(after['code_description'])
            self.assertEqual(after['code_display_label'],'Code not recorded — Description unavailable')

    def test_fallback_is_display_only_for_every_actual_dimension_entry(self):
        dimension=json.loads((REFERENCE.parents[3]/'results/power_bi/results.json').read_text())['dim_code']
        rows=[{k:r[k] for k in ORIGINAL_COLUMNS} for r in dimension]
        out,_=enrich_dimension(rows,[],load_reference()[0])
        self.assertEqual(len(out),479)
        self.assertEqual(sum(r['code_description'] is not None for r in out),342)
        for before,after in zip(dimension,out):
            self.assertEqual([before[k] for k in ORIGINAL_COLUMNS],[after[k] for k in ORIGINAL_COLUMNS])
            self.assertEqual(before['code_description'],after['code_description'])
            if before['code_description'] is not None:
                self.assertEqual(before['code_display_label'],after['code_display_label'])
            else:
                self.assertTrue(after['code_display_label'].endswith(' — Description unavailable'))

    def test_real_pinned_reference_all_modes_and_known_issues(self):
        lookup,manifest=load_reference()
        self.assertEqual({r['mode'] for r in manifest['resources']},{'bus','lrt','streetcar','subway'})
        self.assertEqual(lookup[('bus','MFDV')]['description'],'ON DIVERSION')
        self.assertEqual(lookup[('lrt','EXVE')]['status'],'ambiguous')
        self.assertEqual(lookup[('lrt','TXSUP')]['status'],'accepted')
        self.assertEqual(lookup[('bus','MFUIR')]['description'],'ILL CUSTOMER – TRANSPORTATION DECLINED')

    def test_incomplete_reference_and_checksum_mismatch_rejected(self):
        original=json.loads(REFERENCE.read_text())
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'manifest.json'
            incomplete=copy.deepcopy(original);incomplete['resources'].pop()
            path.write_text(json.dumps(incomplete))
            with self.assertRaisesRegex(ValueError,'complete'):load_reference(path)
            for r in original['resources']:
                (Path(directory)/r['file']).write_bytes((REFERENCE.parent/r['file']).read_bytes())
            path.write_text(json.dumps(original))
            first=Path(directory)/original['resources'][0]['file']
            first.write_bytes(first.read_bytes()+b'\n')
            with self.assertRaisesRegex(ValueError,'integrity'):load_reference(path)

    def test_duplicate_dimension_key_or_orphan_fact_is_rejected(self):
        lookup=prepare_lookup({})
        with self.assertRaisesRegex(ValueError,'duplicate key'):
            enrich_dimension([self.dimension(),self.dimension()],[],lookup)
        with self.assertRaisesRegex(ValueError,'absent original code key'):
            enrich_dimension([self.dimension()],[dict(code_key='orphan',recorded_incidents=1)],lookup)

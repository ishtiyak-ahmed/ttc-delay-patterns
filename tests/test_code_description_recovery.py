"""Pinned, reversible punctuation recovery; no network or local database required."""
import copy
import hashlib
import json
import unittest

from scripts.enrich_code_dimension import (
    REFERENCE, RECOVERY, ORIGINAL_COLUMNS, apply_reviewed_recoveries,
    enrich_dimension, load_reference, prepare_lookup, recover_dash,
)


class DescriptionRecoveryTests(unittest.TestCase):
    def setUp(self):
        self.raw, self.manifest = load_reference(recover=False)
        self.evidence = json.loads(RECOVERY.read_text(encoding='utf-8'))
        self.manifest_hash = hashlib.sha256(REFERENCE.read_bytes()).hexdigest()
        self.rows = {r['mode']: [] for r in self.manifest['resources']}
        for (mode, code), entry in self.raw.items():
            self.rows[mode].extend(dict(CODE=code, DESCRIPTION=d) for d in entry['source_descriptions'])

    def test_all_56_reviewed_originals_and_exact_expected_recoveries(self):
        recovered, _ = load_reference()
        self.assertEqual(len(self.evidence['entries']), 56)
        for entry in self.evidence['entries']:
            key = entry['source_mode'], entry['raw_code']
            self.assertEqual(self.raw[key]['source_descriptions'], [entry['original_text']])
            self.assertEqual(recovered[key]['status'], 'accepted')
            self.assertEqual(recovered[key]['description'], entry['recovered_text'])
            self.assertEqual(entry['recovered_text'].encode('utf-8').decode('latin1'), entry['original_text'])
        self.assertEqual(recovered['subway', 'PUTSC']['description'], 'SIGNALS–CONTROL PROBLEM–TRACK')
        self.assertEqual(recovered['bus', 'TFPD']['description'], 'TTC COLLISION – PROPERTY DAMAGE')
        self.assertEqual(recovered['streetcar', 'MTUI']['description'], 'INJURIED/ILL CUSTOMER – TRANSPORTED')
        self.assertEqual(recovered['streetcar', 'MTESA']['description'], 'NO OPERATOR/CREW AVILABLE – ESA RELATED')

    def test_479_keys_original_fields_and_286_accepted_descriptions_unchanged(self):
        # The checked-in dimension supplies identity only; rebuild both versions independently.
        dimension = json.loads((REFERENCE.parents[3] / 'results/power_bi/results.json').read_text())['dim_code']
        original = [{k: r[k] for k in ORIGINAL_COLUMNS} for r in dimension]
        before, _ = enrich_dimension(original, [], self.raw)
        after, _ = enrich_dimension(original, [], load_reference()[0])
        self.assertEqual(len(after), 479)
        self.assertEqual([{k: r[k] for k in ORIGINAL_COLUMNS} for r in after], original)
        accepted = [(a, b) for a, b in zip(before, after) if a['code_description'] is not None]
        self.assertEqual(len(accepted), 286)
        self.assertTrue(all(a == b for a, b in accepted))
        self.assertEqual(sum(a != b for a, b in zip(before, after)), 56)

    def test_ambiguity_unmapped_and_unreviewed_corruption_remain_unresolved(self):
        recovered, _ = load_reference()
        self.assertEqual(recovered['lrt', 'EXVE'], self.raw['lrt', 'EXVE'])
        self.assertNotIn(('subway', 'SUL'), recovered)
        self.assertEqual(recovered['subway', 'MUFM']['status'], 'encoding_defect')
        self.assertEqual(recovered['streetcar', 'MTUD']['status'], 'encoding_defect')
        self.assertEqual(prepare_lookup({'bus': [dict(CODE='NEW', DESCRIPTION='BAD â\x80\x93 TEXT')]})
                         ['bus', 'NEW']['status'], 'encoding_defect')

    def test_native_unicode_other_corruption_and_mixed_text_are_not_recovered(self):
        for text in ['NATIVE – DASH', 'ÉQUIPMENT – OTHER', 'BAD � TEXT', 'BAD â€“ TEXT',
                     'BAD Ã© TEXT', 'ÉQUIPMENT â\x80\x93 OTHER', 'BAD â\x80\x93 Ã© TEXT']:
            with self.subTest(text=text), self.assertRaises(ValueError):
                recover_dash(text)

    def test_wrong_version_hash_method_size_and_duplicate_allowlist_fail_closed(self):
        for field, value in [('reference_version', 'future'), ('reference_manifest_sha256', '0' * 64),
                             ('method', 'guess'), ('entries', self.evidence['entries'][:-1]),
                             ('entries', [self.evidence['entries'][0]] * 56)]:
            evidence = copy.deepcopy(self.evidence); evidence[field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                apply_reviewed_recoveries(self.rows, self.manifest, self.manifest_hash, evidence)

    def test_changed_original_result_resource_or_mode_code_rejected(self):
        for field, value in [('original_text', 'CHANGED'), ('recovered_text', 'EDITORIAL CHANGE'),
                             ('reference_sha256', '0' * 64), ('source_mode', 'lrt'), ('raw_code', 'NEW')]:
            evidence = copy.deepcopy(self.evidence); evidence['entries'][0][field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                apply_reviewed_recoveries(self.rows, self.manifest, self.manifest_hash, evidence)

    def test_conflicting_or_already_accepted_source_cannot_be_recovered(self):
        entry = self.evidence['entries'][0]
        for replacement in [entry['recovered_text'], 'A DIFFERENT DESCRIPTION']:
            rows = copy.deepcopy(self.rows)
            if replacement == entry['recovered_text']:
                for r in rows[entry['source_mode']]:
                    if r['CODE'] == entry['raw_code']: r['DESCRIPTION'] = replacement
            else:
                rows[entry['source_mode']].append(dict(CODE=entry['raw_code'], DESCRIPTION=replacement))
            with self.assertRaises(ValueError):
                apply_reviewed_recoveries(rows, self.manifest, self.manifest_hash, self.evidence)

    def test_recovery_does_not_mutate_source_rows_and_is_deterministic(self):
        before = copy.deepcopy(self.rows)
        first = apply_reviewed_recoveries(self.rows, self.manifest, self.manifest_hash, self.evidence)
        second = apply_reviewed_recoveries(self.rows, self.manifest, self.manifest_hash, self.evidence)
        self.assertEqual(self.rows, before)
        self.assertEqual(first, second)

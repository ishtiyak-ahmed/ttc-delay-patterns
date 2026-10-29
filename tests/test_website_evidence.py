"""Offline website evidence projection and protection of authoritative exports."""
import hashlib
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.export_website_evidence import ROOT, build_evidence, serialized_evidence


class WebsiteEvidenceTests(unittest.TestCase):
    def test_deterministic_projection_totals_coverage_and_source_protection(self):
        files = list((ROOT/'results/power_bi').iterdir())
        before = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
        first = serialized_evidence()
        self.assertEqual(first, serialized_evidence())
        data = json.loads(first)
        self.assertEqual(data['totals'], dict(recorded_incidents=176004, recorded_delay_minutes=2740515, zero_minute_incidents=49830))
        self.assertEqual(data['enrichment']['after_records'], 165124)
        self.assertEqual(data['enrichment']['before_records'], 133713)
        self.assertEqual(data['enrichment']['recovered_codes'], 56)
        self.assertEqual(data['enrichment']['unresolved_codes'], 137)
        self.assertEqual(data['bus']['long']['recorded_incidents'], 4209)
        self.assertEqual(data['bus']['overlap']['recorded_delay_minutes'], 777169)
        self.assertEqual(data['bus']['union']['recorded_delay_minutes'], 947874)
        self.assertEqual(len(data['monthly']), 20)
        self.assertTrue(all(r['count_leaders'] == ['YU'] for r in data['monthly']))
        self.assertEqual([r['month_start'] for r in data['monthly'] if r['minute_leaders'] == ['BD']],
                         ['2025-03-01', '2026-03-01', '2026-04-01'])
        self.assertEqual(before, {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in files})

    def test_corrupt_source_bundle_is_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            bundle = Path(folder)/'bundle'
            shutil.copytree(ROOT/'results/power_bi', bundle)
            path = bundle/'fact_month.csv'; path.write_bytes(path.read_bytes()+b'corrupt')
            with self.assertRaisesRegex(ValueError, 'checksum'):
                build_evidence(bundle=bundle)

    def test_checked_in_evidence_matches_projection(self):
        self.assertEqual((ROOT/'website/src/data/evidence.json').read_bytes(), serialized_evidence())

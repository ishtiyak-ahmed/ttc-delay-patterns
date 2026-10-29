"""Offline checks for the v2 website manuscript and rendering contract."""
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "website/content/ttc-case-study-v2.md"
APP = ROOT / "website/src/App.tsx"


class WebsiteV2ContentTests(unittest.TestCase):
    def test_final_manuscript_has_exact_six_section_sequence(self):
        text = MANUSCRIPT.read_text()
        headings = re.findall(r"^# (0[1-6] — .+)$", text, re.MULTILINE)
        self.assertEqual(headings, [
            "01 — Project Overview",
            "02 — Data & Methodology",
            "03 — Data Enrichment & Validation",
            "04 — Analytical Findings",
            "05 — Discussion & Limitations",
            "06 — Conclusion & Next Steps",
        ])

    def test_renderer_uses_v2_manuscript_without_copying_section_bodies(self):
        app = APP.read_text()
        self.assertIn("../content/ttc-case-study-v2.md?raw", app)
        self.assertIn("<Narrative body={section.body} />", app)
        self.assertNotIn("../content/ttc-case-study.md?raw", app)
        self.assertEqual(app.count("<DashboardPlaceholder page="), 3)

    def test_unfinished_destinations_are_explicit_placeholders(self):
        app = APP.read_text()
        self.assertIn("Personal portfolio URL pending", app)
        self.assertIn("Verified asset pending", app)
        self.assertIn("No dashboard image or interaction has been fabricated", app)
        self.assertNotRegex(app, r"<img[^>]+dashboard")


if __name__ == "__main__":
    unittest.main()

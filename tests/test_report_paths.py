"""Privacy-safe serialization independent of local usernames and temporary roots."""
import tempfile
import unittest
from pathlib import Path
from scripts.report_paths import report_path


class ReportPathTests(unittest.TestCase):
    def test_project_path_is_portable(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.assertEqual(report_path(root/'data/local/ttc.sqlite3', root),
                             'data/local/ttc.sqlite3')
            self.assertEqual(report_path(root/'data/../reports/check.json', root),
                             'reports/check.json')

    def test_external_path_omits_directory_and_filename(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)/'project'
            private = Path(directory)/'personal-name'/'private-name.sqlite3'
            self.assertEqual(report_path(private, root), '[external location omitted]')

    def test_sibling_prefix_is_not_inside_project(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)/'project'
            self.assertEqual(report_path(Path(directory)/'project-private'/'db.sqlite3', root),
                             '[external location omitted]')

    def test_symlink_escape_is_not_disclosed(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            root = base/'project'
            root.mkdir()
            external = base/'private'
            external.mkdir()
            (root/'linked').symlink_to(external, target_is_directory=True)
            self.assertEqual(report_path(root/'linked'/'db.sqlite3', root),
                             '[external location omitted]')

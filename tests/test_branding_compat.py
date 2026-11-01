import tempfile
import unittest
from pathlib import Path

from backend.app.branding_compat import database_path, session_token


class BrandingCompatibilityTests(unittest.TestCase):
    def test_existing_database_is_reused_without_modifying_it(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            legacy = root / 'siarad.sqlite'
            legacy.write_bytes(b'existing database sentinel')
            self.assertEqual(database_path(root), legacy)
            self.assertEqual(legacy.read_bytes(), b'existing database sentinel')
            self.assertFalse((root / 'saer.sqlite').exists())

    def test_fresh_install_and_current_database_use_current_name(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            self.assertEqual(database_path(root), root / 'saer.sqlite')
            (root / 'saer.sqlite').touch()
            (root / 'siarad.sqlite').touch()
            self.assertEqual(database_path(root), root / 'saer.sqlite')

    def test_existing_session_remains_readable_and_current_session_wins(self):
        self.assertEqual(session_token({'siarad_session': 'old'}), 'old')
        self.assertEqual(session_token({'saer_session': 'new', 'siarad_session': 'old'}), 'new')
        self.assertIsNone(session_token({}))


if __name__ == '__main__':
    unittest.main()

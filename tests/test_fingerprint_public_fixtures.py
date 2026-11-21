"""Tests for stable identification of public evaluation fixtures."""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "fingerprint-public-fixtures.py"
SPEC = importlib.util.spec_from_file_location("fingerprint_public_fixtures", SCRIPT)
assert SPEC and SPEC.loader
FINGERPRINT = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = FINGERPRINT
SPEC.loader.exec_module(FINGERPRINT)


class PublicFixtureFingerprintTests(unittest.TestCase):
    def test_lists_fixture_id_path_and_stable_hash_in_path_order(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "z.json").write_text(json.dumps({"id": "z"}), encoding="utf-8")
            (root / "a.json").write_text(json.dumps({"id": "a"}), encoding="utf-8")
            (root / "README.md").write_text("not a fixture", encoding="utf-8")
            first = FINGERPRINT.fingerprints(root)
            second = FINGERPRINT.fingerprints(root)
        self.assertEqual(first, second)
        self.assertEqual(["a", "z"], [row["id"] for row in first])
        self.assertTrue(all(len(row["sha256"]) == 64 for row in first))

    def test_rejects_a_fixture_without_an_id(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "bad.json").write_text("{}", encoding="utf-8")
            with self.assertRaises(ValueError):
                FINGERPRINT.fingerprints(root)


if __name__ == "__main__":
    unittest.main()

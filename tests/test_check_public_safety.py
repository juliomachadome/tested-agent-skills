"""Tests for the release safety checker.

The fixtures are created temporarily so no secret-like examples are committed.
"""

from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check-public-safety.py"
SPEC = importlib.util.spec_from_file_location("check_public_safety", SCRIPT)
assert SPEC and SPEC.loader
CHECKER = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = CHECKER
SPEC.loader.exec_module(CHECKER)


class PublicSafetyCheckTests(unittest.TestCase):
    def scan(self, relative_path: str, content: str):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            target = root / relative_path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
            return CHECKER.scan_tree(root)

    def test_accepts_safe_public_markdown(self):
        findings = self.scan("README.md", "# Public documentation\\nUse environment variables for secrets.\\n")
        self.assertEqual([], findings)

    def test_flags_a_personal_local_path_without_echoing_the_value(self):
        local_path = "/" + "Users" + "/example/private-project"
        findings = self.scan("notes.md", f"Saved locally under {local_path}.\\n")
        self.assertEqual([("local-path", "notes.md")], [(item.rule, item.path) for item in findings])

    def test_flags_personal_mail_domains(self):
        address = "person" + "@" + "gmail.com"
        findings = self.scan("notes.md", f"Contact: {address}\\n")
        self.assertEqual([("personal-email", "notes.md")], [(item.rule, item.path) for item in findings])

    def test_flags_credential_markers(self):
        token = "gh" + "p_" + "abcdefghijklmnopqrstuvwxyz1234567890ABCD"
        findings = self.scan("config.txt", f"token={token}\\n")
        self.assertEqual([("credential-marker", "config.txt")], [(item.rule, item.path) for item in findings])

    def test_ignores_git_and_binary_files(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / ".git").mkdir()
            (root / ".git" / "config").write_text("person" + "@" + "gmail.com", encoding="utf-8")
            token = "gh" + "p_" + "abcdefghijklmnopqrstuvwxyz1234567890ABCD"
            (root / "image.bin").write_bytes(b"\x00" + token.encode())
            self.assertEqual([], CHECKER.scan_tree(root))


if __name__ == "__main__":
    unittest.main()

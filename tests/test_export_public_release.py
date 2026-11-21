"""Tests for the filtered fresh-history public release export."""

from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "export-public-release.py"
SPEC = importlib.util.spec_from_file_location("export_public_release", SCRIPT)
assert SPEC and SPEC.loader
EXPORT = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = EXPORT
SPEC.loader.exec_module(EXPORT)


class PublicReleaseExportTests(unittest.TestCase):
    def test_export_omits_history_private_evidence_and_internal_notes(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "source"
            root.mkdir()
            (root / "README.md").write_text("public", encoding="utf-8")
            (root / ".git").mkdir()
            (root / ".git" / "config").write_text("history", encoding="utf-8")
            (root / "skills" / "example" / "evals").mkdir(parents=True)
            (root / "skills" / "example" / "SKILL.md").write_text("public skill", encoding="utf-8")
            (root / "skills" / "example" / "evals" / "compare-results.json").write_text("raw answer", encoding="utf-8")
            (root / "evals" / "public").mkdir(parents=True)
            (root / "evals" / "public" / "fixture.json").write_text("synthetic public fixture", encoding="utf-8")
            (root / "docs" / "superpowers").mkdir(parents=True)
            (root / "docs" / "superpowers" / "plan.md").write_text("internal", encoding="utf-8")
            (root / "CATALOGO.md").write_text("historical portuguese catalog", encoding="utf-8")
            (root / "catalog").mkdir()
            (root / "catalog" / "index.html").write_text("public english catalog", encoding="utf-8")
            (root / "catalog" / "descriptions.json").write_text("historical portuguese source", encoding="utf-8")
            (root / "catalog" / "status.json").write_text("historical portuguese status", encoding="utf-8")
            (root / "catalog" / "template.html").write_text("historical portuguese template", encoding="utf-8")
            (root / "scripts").mkdir()
            (root / "scripts" / "build-catalog.py").write_text("historical Portuguese generator", encoding="utf-8")
            (root / "scripts" / "build-evaluation-summary.py").write_text("private-status generator", encoding="utf-8")
            (root / "scripts" / "build-public-catalog.py").write_text("private-status generator", encoding="utf-8")
            (root / "scripts" / "skill-eval.py").write_text("historical runner", encoding="utf-8")
            (root / "scripts" / "codex-skill-eval.py").write_text("public adapter", encoding="utf-8")
            (root / "tests").mkdir()
            (root / "tests" / "test_build_evaluation_summary.py").write_text("private status test", encoding="utf-8")
            (root / "tests" / "test_build_public_catalog.py").write_text("private status test", encoding="utf-8")
            (root / "README.md").write_text("Public releases exclude the full historical benchmark runner and holdout tasks.\n", encoding="utf-8")
            destination = Path(temporary) / "release"
            copied = EXPORT.export_tree(root, destination)
            self.assertTrue((destination / "README.md").exists())
            self.assertTrue((destination / "skills" / "example" / "SKILL.md").exists())
            self.assertFalse((destination / ".git").exists())
            self.assertFalse((destination / "skills" / "example" / "evals").exists())
            self.assertTrue((destination / "evals" / "public" / "fixture.json").exists())
            self.assertFalse((destination / "docs" / "superpowers").exists())
            self.assertFalse((destination / "CATALOGO.md").exists())
            self.assertTrue((destination / "catalog" / "index.html").exists())
            self.assertFalse((destination / "catalog" / "descriptions.json").exists())
            self.assertFalse((destination / "catalog" / "status.json").exists())
            self.assertFalse((destination / "catalog" / "template.html").exists())
            self.assertFalse((destination / "scripts" / "skill-eval.py").exists())
            self.assertFalse((destination / "scripts" / "build-catalog.py").exists())
            self.assertFalse((destination / "scripts" / "build-evaluation-summary.py").exists())
            self.assertFalse((destination / "scripts" / "build-public-catalog.py").exists())
            self.assertTrue((destination / "scripts" / "codex-skill-eval.py").exists())
            self.assertFalse((destination / "tests" / "test_build_evaluation_summary.py").exists())
            self.assertFalse((destination / "tests" / "test_build_public_catalog.py").exists())
            self.assertIn("Public releases exclude", (destination / "README.md").read_text(encoding="utf-8"))
            self.assertGreater(copied, 0)


if __name__ == "__main__":
    unittest.main()

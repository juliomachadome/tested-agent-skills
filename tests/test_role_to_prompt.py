"""Tests for portable role briefs used by Codex and raw-model workflows."""

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "role-to-prompt.py"
SPEC = importlib.util.spec_from_file_location("role_to_prompt", SCRIPT)
assert SPEC and SPEC.loader
ROLE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = ROLE
SPEC.loader.exec_module(ROLE)


class RoleToPromptTests(unittest.TestCase):
    def test_lists_portable_profiles(self):
        self.assertIn("code-reviewer", ROLE.role_names())
        self.assertIn("sales-rep", ROLE.role_names())

    def test_brief_keeps_portable_contract_and_drops_claude_mapping(self):
        brief = ROLE.render("code-reviewer")
        self.assertIn("# Role brief: code-reviewer", brief)
        self.assertIn("Core knowledge: `code-review-criteria`", brief)
        self.assertIn("## Output contract", brief)
        self.assertNotIn("## Claude Code mapping", brief)
        self.assertIn("Project instructions and host permissions win", brief)

    def test_optional_skill_is_included_without_reference_dump(self):
        brief = ROLE.render("code-reviewer", include_skills=True)
        self.assertIn("# Skill: code-review-criteria", brief)
        self.assertNotIn("## Reference:", brief)

    def test_unknown_role_has_a_safe_error(self):
        with self.assertRaisesRegex(ValueError, "no role named not-a-role"):
            ROLE.render("not-a-role")


if __name__ == "__main__":
    unittest.main()

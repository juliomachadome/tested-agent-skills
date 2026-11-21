"""Dry-run coverage for selective installation without touching a real home folder."""

from __future__ import annotations

import os
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INSTALL = ROOT / "scripts" / "install.sh"


class InstallSelectionTests(unittest.TestCase):
    def run_install(self, *args: str) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as home:
            environment = os.environ | {"AGENTS_HOME": str(Path(home) / ".agents")}
            return subprocess.run(
                [str(INSTALL), "--dry-run", "--target", "agents", *args],
                cwd=ROOT,
                env=environment,
                text=True,
                capture_output=True,
                check=False,
            )

    def test_one_skill_installs_without_default_profile_or_agents(self):
        result = self.run_install("--skill", "copywriting")
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("copywriting", result.stdout)
        self.assertNotIn("offers", result.stdout)
        self.assertNotIn("code-reviewer", result.stdout)

    def test_skill_can_be_combined_with_a_profile(self):
        result = self.run_install("--profile", "marketing", "--skill", "engineering-playbook")
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("copywriting", result.stdout)
        self.assertIn("engineering-playbook", result.stdout)

    def test_unknown_skill_is_rejected(self):
        result = self.run_install("--skill", "not-a-real-skill")
        self.assertNotEqual(0, result.returncode)
        self.assertIn("no skill named not-a-real-skill", result.stderr)

    def test_claude_agent_is_not_silently_ignored_by_another_target(self):
        result = self.run_install("--agent", "code-reviewer")
        self.assertNotEqual(0, result.returncode)
        self.assertIn("Claude Code only", result.stderr)
        self.assertIn("role-to-prompt.py", result.stderr)


if __name__ == "__main__":
    unittest.main()

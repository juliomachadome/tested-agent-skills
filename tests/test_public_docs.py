"""High-confidence checks for the public landing documentation."""

from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class PublicDocsTests(unittest.TestCase):
    def test_readme_has_no_stale_fixture_or_private_history_copy(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8").lower()
        self.assertNotIn("forthcoming synthetic", readme)
        self.assertNotIn("private working history", readme)
        self.assertIn("docs/codex.md", readme)
        self.assertIn("docs/claude-code.md", readme)

    def test_claude_guide_covers_focused_install_and_native_agents(self):
        guide = (ROOT / "docs" / "claude-code.md").read_text(encoding="utf-8").lower()
        self.assertIn("--skill", guide)
        self.assertIn("--agent", guide)
        self.assertIn("native", guide)

    def test_llms_index_points_to_install_and_harness_guides(self):
        index = (ROOT / "llms.txt").read_text(encoding="utf-8")
        self.assertTrue(index.startswith("# Tested Agent Skills\n"))
        base = "https://raw.githubusercontent.com/juliomachadome/tested-agent-skills/main/"
        links = dict(re.findall(r"\[([^\]]+)\]\(([^)]+)\)", index))
        self.assertEqual(links["Claude Code guide"], base + "docs/claude-code.md")
        self.assertEqual(links["Codex guide"], base + "docs/codex.md")
        self.assertEqual(links["Installation script"], base + "scripts/install.sh")
        for url in links.values():
            self.assertTrue(url.startswith(base), url)
            self.assertTrue((ROOT / url.removeprefix(base)).is_file(), url)

    def test_evaluation_summary_does_not_expose_portuguese_status_labels(self):
        summary = (ROOT / "docs" / "evaluation-summary.md").read_text(encoding="utf-8").lower()
        self.assertNotIn("`vence`", summary)
        self.assertNotIn("`empata`", summary)

    def test_codex_guide_describes_portable_roles_directly(self):
        guide = (ROOT / "docs" / "codex.md").read_text(encoding="utf-8").lower()
        self.assertIn("role-to-prompt.py", guide)
        self.assertNotIn("fake native", guide)

    def test_contributing_only_lists_available_python_checks(self):
        contributing = (ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
        commands = re.findall(r"python3 (scripts/[a-z0-9-]+\.py)", contributing)
        missing = [command for command in commands if not (ROOT / command).is_file()]
        self.assertEqual(missing, [])


    def test_evaluation_matrix_covers_each_public_skill_once(self):
        matrix = (ROOT / "docs" / "skill-evaluation-matrix.md").read_text(encoding="utf-8")
        rows = re.findall(r"^\| `([a-z0-9-]+)` \|(?:[^|\n]*\|){4}$", matrix, re.MULTILINE)
        public_skills = [file.parent.name for file in (ROOT / "skills").glob("*/SKILL.md")]
        self.assertCountEqual(rows, public_skills)


if __name__ == "__main__":
    unittest.main()

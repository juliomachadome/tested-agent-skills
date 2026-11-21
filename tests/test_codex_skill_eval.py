"""Tests for the isolated Codex smoke evaluator."""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "codex-skill-eval.py"
SPEC = importlib.util.spec_from_file_location("codex_skill_eval", SCRIPT)
assert SPEC and SPEC.loader
EVAL = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = EVAL
SPEC.loader.exec_module(EVAL)


class CodexSkillEvalTests(unittest.TestCase):
    def test_command_is_ephemeral_config_free_read_only_and_jsonl(self):
        command = EVAL.build_command(Path("/tmp/project"), "test prompt")
        self.assertEqual("codex", command[0])
        self.assertIn("--ephemeral", command)
        self.assertIn("--ignore-user-config", command)
        self.assertIn("--sandbox", command)
        self.assertEqual("read-only", command[command.index("--sandbox") + 1])
        self.assertIn("--json", command)
        self.assertNotIn("--full-auto", command)

    def test_workspace_contains_only_the_requested_skill_and_no_fixture_answer_key(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            skills = root / "skills"
            source = skills / "example"
            (source / "evals").mkdir(parents=True)
            (source / "SKILL.md").write_text("# Example\n", encoding="utf-8")
            (source / "reference.md").write_text("Reference\n", encoding="utf-8")
            (source / "evals" / "answers.json").write_text('{"answer":"private"}', encoding="utf-8")
            fixture = root / "fixture.json"
            fixture.write_text(json.dumps({"id": "smoke", "skill": "example", "prompt": "Synthetic prompt", "answer": "never copy"}), encoding="utf-8")
            project = root / "project"
            EVAL.prepare_workspace(project, fixture, skills)
            self.assertTrue((project / ".agents" / "skills" / "example" / "SKILL.md").exists())
            self.assertTrue((project / ".agents" / "skills" / "example" / "reference.md").exists())
            self.assertFalse((project / ".agents" / "skills" / "example" / "evals").exists())
            self.assertFalse((project / "fixture.json").exists())
            self.assertNotIn("never copy", "\n".join(p.read_text() for p in project.rglob("*") if p.is_file()))

    def test_jsonl_parser_redacts_final_text(self):
        events = '\n'.join((
            '{"type":"thread.started","thread_id":"abc"}',
            '{"type":"item.completed","item":{"type":"agent_message","text":"answer that must stay private"}}',
        ))
        result = EVAL.parse_jsonl(events)
        self.assertTrue(result["thread_started"])
        self.assertNotIn("thread_id", result)
        self.assertNotIn("answer", result)
        self.assertEqual(2, result["events"])

    def test_dry_run_reports_fixture_fingerprint_without_answer_text(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            skills = root / "skills" / "example"
            skills.mkdir(parents=True)
            (skills / "SKILL.md").write_text("# Example\n", encoding="utf-8")
            fixture = root / "fixture.json"
            fixture.write_text(json.dumps({"id": "smoke", "skill": "example", "prompt": "Synthetic prompt", "answer": "never copy"}), encoding="utf-8")
            value = EVAL.load_fixture(fixture)
            result = EVAL.report(value, fixture)
        self.assertEqual(64, len(result["fixture_sha256"]))
        self.assertNotIn("never copy", json.dumps(result))


if __name__ == "__main__":
    unittest.main()

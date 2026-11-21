"""Deterministic tests for the paired runner, with no model calls."""

import importlib.util
import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("skill_compare", ROOT / "scripts" / "codex-skill-compare.py")
compare = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(compare)


class SkillCompareTests(unittest.TestCase):
    def test_exposure_differs_by_condition_and_natural_discovery_does_not_direct_a_read(self):
        fixture = {"skill": "qa-verification", "prompt": "Evaluate a synthetic release.",
                   "expected_fields": {"marker": "grader-only"}}
        source = ROOT / "skills" / fixture["skill"]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in ("baseline", "explicit", "natural", "forced"):
                (root / name).mkdir()
            baseline, no_target = compare.prepare(root / "baseline", source, fixture, "without", "forced")
            explicit, _ = compare.prepare(root / "explicit", source, fixture, "with", "explicit")
            natural, target = compare.prepare(root / "natural", source, fixture, "with", "natural")
            forced, _ = compare.prepare(root / "forced", source, fixture, "with", "forced")
            self.assertIsNone(no_target)
            self.assertEqual(list((root / "baseline").iterdir()), [])
            self.assertTrue(explicit.endswith(baseline))
            self.assertEqual(natural, baseline)
            self.assertEqual(forced, baseline)
            self.assertTrue(target.is_file())
            self.assertFalse((root / "natural" / "AGENTS.md").exists())
            self.assertTrue((root / "forced" / "AGENTS.md").is_file())
            self.assertNotIn("grader-only", explicit)

    def test_private_answers_cannot_be_saved_in_a_checkout_or_overwritten(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            checkout = root / "checkout"
            checkout.mkdir()
            (checkout / ".git").touch()
            child = checkout / "answers"
            child.mkdir()
            with self.assertRaisesRegex(ValueError, "outside Git"):
                compare.private_batch(child)
            output = compare.private_batch(root) / "A.txt"
            compare.write_answer(output, "private fixture output")
            self.assertEqual(output.stat().st_mode & 0o777, 0o600)
            with self.assertRaises(FileExistsError):
                compare.write_answer(output, "replacement")

    def test_parser_requires_a_matching_read_and_returns_no_tool_output(self):
        target = Path("/isolated/.agents/skills/qa-verification/SKILL.md")
        events = [
            {"type": "item.completed", "item": {"type": "command_execution", "exit_code": 0,
                                               "command": "sed -n '1,8p' " + str(target),
                                               "aggregated_output": "name: qa-verification\nPRIVATE_MARKER"}},
            {"type": "item.completed", "item": {"type": "agent_message", "text": '{"result":true}'}},
            {"type": "turn.completed", "usage": {"input_tokens": 20, "private": "PRIVATE_MARKER"}},
        ]
        raw = "\n".join(map(json.dumps, events))
        _, report = compare.parse_output(raw, target)
        self.assertEqual(report["project_file_read"], "observed")
        self.assertNotIn("PRIVATE_MARKER", json.dumps(report))
        self.assertEqual(compare.parse_output(raw, target.with_name("other.md"))[1]["project_file_read"], "not_observed")
        other_copy = raw.replace("/isolated/", "/unrelated/")
        self.assertEqual(compare.parse_output(other_copy, target)[1]["project_file_read"], "not_observed")

    def test_field_checks_distinguish_json_types_and_invalid_output(self):
        self.assertEqual(compare.evaluate('{"flag":1,"result":"hold"}', {"flag": True, "result": "hold"}),
                         {"flag": False, "result": True})
        self.assertEqual(compare.evaluate("not JSON", {"flag": False}), {"flag": False})
        self.assertIsNone(compare.evaluate("free text", {}))

    def test_rejects_path_segments_in_skill_names(self):
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory) / "fixture.json"
            fixture.write_text(json.dumps({"id": "case", "skill": "../outside", "prompt": "Synthetic."}))
            with self.assertRaisesRegex(ValueError, "slug"):
                compare.load_fixture(fixture)

    def test_repeated_pairs_have_fresh_invocations_and_indexed_labels(self):
        fixture = ROOT / "evals/public/qa-stale-release.json"
        version = SimpleNamespace(stdout="codex-cli test")
        with patch.object(compare.subprocess, "run", return_value=version), patch.object(
            compare, "invoke", return_value=("answer", {"status": "completed"})
        ) as invoke, redirect_stdout(io.StringIO()) as output:
            status = compare.main(["--fixture", str(fixture), "--model", "example", "--runs", "3", "--live"])
        self.assertEqual(status, 0)
        self.assertEqual(invoke.call_count, 6)
        runs = json.loads(output.getvalue())["runs"]
        self.assertEqual([run["run_index"] for run in runs], list(range(1, 7)))
        for index in range(0, 6, 2):
            self.assertEqual({run["condition"] for run in runs[index:index + 2]}, {"with", "without"})
            self.assertEqual({run["pair_index"] for run in runs[index:index + 2]}, {index // 2 + 1})

    def test_routing_exposes_the_alternative_in_both_arms_and_records_its_observed_read(self):
        fixture = compare.load_fixture(ROOT / "evals/public/copywriting-offers-routing.json")
        source = ROOT / "skills" / "offers"
        args = SimpleNamespace(discovery="natural", timeout=10, model="example")

        def run(argv, **kwargs):
            project = Path(argv[argv.index("-C") + 1])
            skills = project / ".agents/skills"
            alt = skills / "copywriting/SKILL.md"
            self.assertTrue(alt.is_file())
            self.assertFalse((project / "AGENTS.md").exists())
            self.assertEqual((skills / "offers/SKILL.md").is_file(), condition == "with")
            raw = [
                {"type": "item.completed", "item": {
                    "type": "command_execution", "exit_code": 0, "command": "cat " + str(alt),
                    "aggregated_output": "name: copywriting"}},
                {"type": "item.completed", "item": {"type": "agent_message", "text": "reply"}},
                {"type": "turn.completed"},
            ]
            return SimpleNamespace(stdout="\n".join(map(json.dumps, raw)), returncode=0)

        for condition in ("with", "without"):
            with self.subTest(condition=condition), patch.object(compare.subprocess, "run", side_effect=run):
                _, report = compare.invoke(fixture, source, condition, args)
                self.assertEqual(report["routing_file_reads"], {"copywriting": "observed"})
                self.assertEqual(report["project_file_read"], "not_observed" if condition == "with" else None)

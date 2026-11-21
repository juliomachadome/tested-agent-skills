"""Tests for portable role-profile generation."""

from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "build-agent-profiles.py"
SPEC = importlib.util.spec_from_file_location("build_agent_profiles", SCRIPT)
assert SPEC and SPEC.loader
PROFILES = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = PROFILES
SPEC.loader.exec_module(PROFILES)


class AgentProfileTests(unittest.TestCase):
    def test_folded_agent_description_survives_profile_generation(self):
        root = Path(__file__).resolve().parents[1]
        media = next(agent for agent in PROFILES.read_agents(root / "agents") if agent["name"] == "media-producer")
        self.assertIn("Production role for images, video, 3D, voice and music", PROFILES.render_profile(media))

    def test_all_claude_agents_receive_a_portable_profile(self):
        agents = PROFILES.read_agents(Path(__file__).resolve().parents[1] / "agents")
        self.assertEqual(26, len(agents))
        self.assertEqual({agent["name"] for agent in agents}, {path.stem for path in (Path(__file__).resolve().parents[1] / "agents").glob("*.md")})

    def test_profile_marks_all_claude_specific_capabilities(self):
        agent = {
            "name": "example",
            "description": "Example role.",
            "tools": ["Read", "WebSearch", "mcp__browser__open"],
            "skills": ["example-skill"],
            "model": "sonnet",
            "memory": "project",
            "mcp_servers": ["browser"],
        }
        rendered = PROFILES.render_profile(agent)
        self.assertIn("## Claude Code mapping", rendered)
        self.assertIn("`Read`", rendered)
        self.assertIn("`WebSearch`", rendered)
        self.assertIn("`mcp__browser__open`", rendered)
        self.assertIn("model: `sonnet`", rendered)
        self.assertIn("memory: `project`", rendered)

    def test_generated_profiles_cover_each_source_tool(self):
        root = Path(__file__).resolve().parents[1]
        agents = PROFILES.read_agents(root / "agents")
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "profiles"
            generated = PROFILES.build(root / "agents", output)
            self.assertEqual(len(agents), len(generated))
            for agent in agents:
                profile = (output / f"{agent['name']}.md").read_text(encoding="utf-8")
                for tool in agent["tools"]:
                    self.assertIn(f"`{tool}`", profile)


if __name__ == "__main__":
    unittest.main()

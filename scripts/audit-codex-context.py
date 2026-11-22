#!/usr/bin/env python3
"""Audit Codex on GitHub without credentials or model calls."""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import tempfile
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CANARY = "synthetic-skill-isolation-canary"
TASK = "Synthetic context audit marker. Reply with OK."
FLAGS = ("--disable", "plugins", "-c", 'web_search="disabled"')


def context(folder: Path, *, skip_host_skills: bool) -> str:
    flags = ("--enable", "skip_host_skill_discovery") if skip_host_skills else ()
    result = subprocess.run(
        ["codex", "debug", "prompt-input", *FLAGS, *flags, TASK],
        cwd=folder, text=True, capture_output=True, timeout=35, check=True,
    )
    return json.dumps(json.loads(result.stdout), ensure_ascii=False)


class CaptureServer(HTTPServer):
    def __init__(self) -> None:
        super().__init__(("127.0.0.1", 0), CaptureHandler)
        self.requests: list[dict] = []


class CaptureHandler(BaseHTTPRequestHandler):
    def do_POST(self) -> None:
        if self.path == "/v1/responses":
            self.server.requests.append(json.loads(self.rfile.read(int(self.headers["Content-Length"]))))
        self.send_response(400)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"error":{"message":"Synthetic capture only","type":"invalid_request_error"}}')

    def log_message(self, format: str, *args: object) -> None:
        pass


def capture_pair(project: Path) -> dict:
    spec = importlib.util.spec_from_file_location("compare", ROOT / "scripts/codex-skill-compare.py")
    assert spec and spec.loader
    runner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(runner)
    fixture = runner.load_fixture(ROOT / "evals/public/lume-02-motion.json")
    source = ROOT / "skills" / fixture["skill"]
    skill_block = "<reference_skill>\n" + (source / "SKILL.md").read_text(encoding="utf-8") + "\n</reference_skill>\n\n"

    with CaptureServer() as server:
        worker = threading.Thread(target=server.serve_forever, daemon=True)
        worker.start()
        try:
            provider = [
                "-c", 'model_provider="capture"',
                "-c", 'model_providers.capture.name="Synthetic capture"',
                "-c", f'model_providers.capture.base_url="http://127.0.0.1:{server.server_port}/v1"',
                "-c", 'model_providers.capture.wire_api="responses"',
                "-c", "model_providers.capture.requires_openai_auth=false",
            ]
            texts = {}
            payloads = {}
            for arm in ("without", "with"):
                folder = project / arm
                folder.mkdir()
                prompt, _ = runner.prepare(folder, source, fixture, arm, "explicit")
                assert not list(folder.iterdir()), f"{arm}: unexpected project files"
                count = len(server.requests)
                run = subprocess.run(
                    ["codex", "exec", *runner.FLAGS, *provider, "-m", "gpt-5.4", "-C", str(folder), "-"],
                    input=prompt, text=True, capture_output=True, timeout=35, check=False,
                )
                assert len(server.requests) == count + 1, f"{arm}: expected one request on loopback; CLI exit {run.returncode}"
                payloads[arm] = server.requests[-1]
                texts[arm] = json.dumps(payloads[arm], ensure_ascii=False)
                assert CANARY not in texts[arm], f"{arm}: synthetic user skill leaked"
                assert fixture["prompt"] in texts[arm], f"{arm}: task missing from request"
        finally:
            server.shutdown()
            worker.join()

    encoded_block = json.dumps(skill_block, ensure_ascii=False)[1:-1]
    assert encoded_block not in texts["without"], "Control got the target SKILL.md block"
    assert encoded_block in texts["with"], "Treatment missed the target SKILL.md block"
    assert payloads["without"]["model"] == payloads["with"]["model"] == "gpt-5.4"
    assert payloads["without"].get("tools") == payloads["with"].get("tools")
    return {
        "fixture": fixture["id"],
        "outbound_requests_captured_locally": len(payloads),
        "target_skill_present_only_in_treatment": True,
        "same_model_and_tools_in_both_requests": True,
        "tool_count": len(payloads["without"].get("tools", [])),
        "model_calls": 0,
    }


def main() -> None:
    if os.environ.get("RUNNER_ENVIRONMENT") != "github-hosted":
        raise RuntimeError("Run the synthetic canary on a fresh GitHub-hosted runner")
    skill = Path.home() / ".agents" / "skills" / CANARY
    skill.mkdir(parents=True)
    with tempfile.TemporaryDirectory(prefix="codex-context-audit-") as temp:
        project = Path(temp)
        try:
            (skill / "SKILL.md").write_text(
                f"---\nname: {CANARY}\ndescription: Synthetic discovery marker for CI.\n---\n\nCanary only.\n",
                encoding="utf-8",
            )
            assert CANARY in context(project, skip_host_skills=False), "Positive control did not discover the synthetic skill"
            diagnostic_leak = CANARY in context(project, skip_host_skills=True)
        finally:
            (skill / "SKILL.md").unlink(missing_ok=True)
            skill.rmdir()
        assert CANARY not in context(project, skip_host_skills=True), "Removed canary persisted in prompt diagnostic"
        print(json.dumps({
            "canary_visible_with_default_discovery": True,
            "canary_visible_in_debug_with_skip_host_skill_discovery": diagnostic_leak,
            "canary_visible_in_debug_after_removal": False,
            **capture_pair(project),
        }, indent=2))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""One-pass generator for the real-output review (owner plan 19/11).

For each skill: take its hardest task (narrowest old margin in compare-results.json), run ONE
with-skill answer with a lean system prompt (about 1.5k tokens of fixed context instead of 17.7k),
save it to docs/real-output-pass/<skill>.md with a header (skill loaded, references opened, tokens,
free regex scorecard). No judge calls: the main model reads the answers and decides the fixes.
Usage: python3 scripts/gen-pass.py [skill ...]   (no args = every skill not yet in the folder)
       Create /tmp/STOP to stop cleanly. --workers N (default 3).
"""
import json
import re
import subprocess
import sys
import tempfile
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "docs" / "real-output-pass"
SYS = ("You are a senior specialist answering a customer. Before answering, load the skill named in the task note "
       "with the Skill tool and open the reference files it points to that fit the task. Your final answer is the "
       "deliverable for a customer who never sees skills, files or searches: do not mention them. "
       "Compute numbers with arithmetic shown if you have no code tool.")
LEAK = re.compile(r"SKILL\.md|references/|playbook|\bskill\b|\.md\b", re.I)
TELLS = re.compile(r"\b(unlock|elevate|seamless|streamline|leverage|holistic|robust|delve|tapestry|game-changer)\b", re.I)


def make_plugin(tmp: Path, skill: str) -> Path:
    """Plugin with ONLY this skill (copy without evals/): one listing entry instead of 35, and the
    model cannot Grep other skills' saved answers or this skill's answer key."""
    import shutil
    plug = tmp / skill
    (plug / ".claude-plugin").mkdir(parents=True, exist_ok=True)
    (plug / ".claude-plugin" / "plugin.json").write_text(json.dumps({"name": "evalpkg", "version": "0.0.1"}))
    shutil.copytree(REPO / "skills" / skill, plug / "skills" / skill, ignore=shutil.ignore_patterns("evals"))
    return plug


def importlib_spec():
    import importlib.util
    s = importlib.util.spec_from_file_location("skill_eval", REPO / "scripts" / "skill-eval.py")
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


def margin(row):
    def n(x):
        try:
            return int(str(x).split("/")[0])
        except ValueError:
            return 0
    return n(row.get("with_pass")) - n(row.get("without_pass"))


def hardest(skill):
    ev = json.loads((REPO / "skills" / skill / "evals" / "evals.json").read_text())["evals"]
    p = REPO / "skills" / skill / "evals" / "compare-results.json"
    if p.exists():
        rows = json.loads(p.read_text())["rows"]
        pick = sorted(rows, key=lambda r: (margin(r), str(r["id"])))[0]["id"]
        for e in ev:
            if str(e["id"]) == str(pick):
                return e
    return ev[0]


def generate(skill, tmp, timeout=420):
    plug = make_plugin(tmp, skill)
    e = hardest(skill)
    prompt = f"(Task note: the relevant skill is `{skill}`.)\n\n{e['prompt']}"
    work = tempfile.mkdtemp(prefix="gen-pass-")
    cmd = ["claude", "-p", prompt, "--model", "claude-sonnet-5-5", "--setting-sources", "project",
           "--output-format", "stream-json", "--verbose", "--strict-mcp-config", "--plugin-dir", str(plug),
           "--tools", "Skill,Read",
           "--allowedTools", "Skill,Read", "--system-prompt", SYS, "--max-turns", "6"]
    loaded, reads, text, usage, cost, turns = False, [], "", {}, 0, 0
    proc = subprocess.Popen(cmd, cwd=work, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
    t = threading.Timer(timeout, proc.kill)
    t.start()
    try:
        for line in proc.stdout:
            try:
                ev = json.loads(line)
            except ValueError:
                continue
            if ev.get("type") == "assistant":
                for c in ev["message"].get("content", []):
                    if c.get("type") == "tool_use":
                        if c["name"] == "Skill":
                            loaded = True
                        if c["name"] == "Read":
                            reads.append(str(c["input"].get("file_path", "")).split("/skills/")[-1])
            elif ev.get("type") == "result":
                text = ev.get("result") or text
                usage = ev.get("usage", {})
                cost = ev.get("total_cost_usd", 0)
                turns = ev.get("num_turns", 0)
    finally:
        t.cancel(); proc.kill(); proc.wait()
    tok = sum(usage.get(k, 0) or 0 for k in ("input_tokens", "cache_creation_input_tokens",
                                                "cache_read_input_tokens", "output_tokens"))
    leaks = LEAK.findall(text)
    head = (f"<!-- skill={skill} task={e['id']} loaded={loaded} refs={sorted(set(reads))} tokens={tok} "
            f"turns={turns} cost_usd={cost:.3f} in={usage.get('input_tokens')} cache_create={usage.get('cache_creation_input_tokens')} cache_read={usage.get('cache_read_input_tokens')} out={usage.get('output_tokens')} leak_hits={len(leaks)} ai_tell_hits={len(TELLS.findall(text))} emdash={text.count('—')} -->\n")
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{skill}.md").write_text(head + f"# {skill}, task {e['id']}\n\n## Task\n\n{e['prompt']}\n\n## Answer\n\n{text}\n")
    return skill, loaded, len(set(reads)), tok, len(leaks)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    skills = args or sorted(p.name for p in (REPO / "skills").iterdir()
                            if (p / "evals" / "evals.json").exists() and not (OUT / f"{p.name}.md").exists())
    tmp = Path(tempfile.mkdtemp(prefix="gen-pass-plug-"))
    stop = Path("/tmp/STOP")

    def one(s):
        if stop.exists():
            return None
        try:
            r = generate(s, tmp)
        except Exception as ex:  # keep the batch alive
            r = (s, False, 0, 0, -1)
            print(f"{s}: ERROR {ex}", flush=True)
        print(f"{r[0]}: loaded={r[1]} refs={r[2]} tokens={r[3]} leak_hits={r[4]}", flush=True)
        return r

    with ThreadPoolExecutor(3) as ex:
        res = [r for r in ex.map(one, skills) if r]
    toks = [r[3] for r in res if r[3]]
    if toks:
        print(f"done {len(res)} skills; tokens per answer avg {sum(toks)//len(toks)}, total {sum(toks)}", flush=True)


if __name__ == "__main__":
    main()

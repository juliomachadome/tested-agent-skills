#!/usr/bin/env python3
"""Print one skill as a single prompt, for any model or tool that has no skill loader.

Usage: scripts/skill-to-prompt.py <skill>                 SKILL.md only
       scripts/skill-to-prompt.py <skill> --refs          plus every references/*.md (can be large)
       scripts/skill-to-prompt.py <skill> --refs NAME...  plus the references whose path contains NAME
       scripts/skill-to-prompt.py --list                  skill names

Send the output as the system message, or paste it at the top of a chat.
The bibliography is left out: it is for people checking sources, not for the model.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS = os.path.join(ROOT, "skills")


def body(path):
    text = open(path, encoding="utf-8").read()
    m = re.match(r"^---\n.*?\n---\n?", text, re.S)
    return text[m.end():].strip() if m else text.strip()


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        sys.exit(__doc__)
    names = sorted(n for n in os.listdir(SKILLS) if os.path.exists(os.path.join(SKILLS, n, "SKILL.md")))
    if argv[0] == "--list":
        print("\n".join(names))
        return
    skill = argv[0]
    if skill not in names:
        sys.exit(f"no skill named {skill} (try --list)")
    want_refs = "--refs" in argv
    filters = [a for a in argv[1:] if a != "--refs"]
    if filters and not want_refs:
        sys.exit("reference names need --refs")
    base = os.path.join(SKILLS, skill)
    out = [f"# Skill: {skill}", "", "Follow the rules below for this topic. Project rules given by the user win over them.", "", body(os.path.join(base, "SKILL.md"))]
    if want_refs:
        ref_dir = os.path.join(base, "references")
        found = []
        for dp, _, files in os.walk(ref_dir):
            for f in sorted(files):
                rel = os.path.relpath(os.path.join(dp, f), base)
                if not f.endswith(".md") or f == "BIBLIOGRAPHY.md":
                    continue
                if filters and not any(x.lower() in rel.lower() for x in filters):
                    continue
                found.append(rel)
        if filters and not found:
            sys.exit(f"no reference in {skill} matches {' '.join(filters)}")
        for rel in sorted(found):
            out += ["", "---", "", f"## Reference: {rel}", "", body(os.path.join(base, rel))]
    print("\n".join(out))


if __name__ == "__main__":
    main(sys.argv[1:])

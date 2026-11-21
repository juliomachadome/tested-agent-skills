#!/usr/bin/env python3
"""Turn Claude Code plugins on or off in ~/.claude/settings.json (user level), with a backup.
Usage: scripts/plugins.py status
       scripts/plugins.py on  expo supabase stripe     (enable before working on that stack)
       scripts/plugins.py off expo supabase stripe     (disable again afterwards)
Then run /reload-plugins in Claude Code (or start a new session). MCP servers inside a plugin
cost context on every turn while the plugin is on, so keep only what the day's work needs.
Claude.ai connectors (Figma, Gmail, Drive, ...) are account-level: use /mcp or claude.ai settings."""
import json, os, shutil, sys, time
P = os.path.expanduser("~/.claude/settings.json")
s = json.load(open(P)); ep = s.setdefault("enabledPlugins", {})
cmd, names = (sys.argv[1] if len(sys.argv) > 1 else "status"), sys.argv[2:]
if cmd == "status":
    for k in sorted(ep): print(("ON  " if ep[k] else "off ") + k)
    sys.exit()
if cmd not in ("on", "off") or not names:
    sys.exit(__doc__)
shutil.copy(P, P + ".bak-" + time.strftime("%Y%m%d-%H%M"))
for n in names:
    keys = [k for k in ep if k.split("@")[0] == n]
    if not keys: print("not found:", n); continue
    for k in keys: ep[k] = (cmd == "on"); print(cmd.upper(), k)
json.dump(s, open(P, "w"), indent=2, ensure_ascii=False)
print("now run /reload-plugins")

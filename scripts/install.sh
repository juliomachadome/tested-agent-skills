#!/usr/bin/env bash
# Links skills (and, for Claude Code, agents) of this repo into the tool's home folder, so all
# projects on this machine use them and a `git pull` updates them everywhere. Anything already there with
# the same name is moved to a dated backup folder first (never deleted).
# Usage: scripts/install.sh [--dry-run] [--target claude|codex|agents] [--profile NAME[,NAME...]] [--skill NAME[,NAME...]] [--agent NAME[,NAME...]] [--prune] [--set-budget]
#   claude (default): skills -> ~/.claude/skills, agents -> ~/.claude/agents   (CLAUDE_HOME overrides)
#   codex:            skills -> ~/.codex/skills (agents have no Codex equivalent) (CODEX_HOME overrides)
#   agents:           skills -> ~/.agents/skills, the shared Agent Skills folder that Codex, Cursor and others read (AGENTS_HOME overrides)
#   --profile all (default): every skill outside quarantine and default.skills_excluded, and the default agents. A profile from scripts/profiles.json links only its skills and
#             agents; profiles combine with commas. Links outside the profile are left untouched unless --prune.
#   --agent   also links these agents by name (repeatable or comma separated). Without --profile or --skill, the default set is installed too; use --profile none for only agents.
#   --skill   links only these skills when used alone; combine with --profile to add named skills to an area, e.g. --skill copywriting.
#   --prune   removes links in the target folder that point into this repo but are not part of this install.
#             With --dry-run it only lists them. Links to other places are never touched.
#   --set-budget  (claude) sets "skillListingBudgetFraction": 0.02 in the target settings.json when it is not set,
#             so all skill descriptions fit the listing. Without this option settings.json is never changed.
set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
DRY=0; TARGET=claude; PROFILE=all; PROFILE_SET=0; PRUNE=0; SET_BUDGET=0; EXTRA_SKILLS=(); EXTRA_AGENTS=()
while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run) DRY=1 ;;
    --target) TARGET="${2:-}"; shift ;;
    --profile) PROFILE="${2:-}"; PROFILE_SET=1; shift ;;
    --skill) IFS=, read -r -a _s <<< "${2:-}"; EXTRA_SKILLS+=("${_s[@]}"); shift ;;
    --agent) IFS=, read -r -a _a <<< "${2:-}"; EXTRA_AGENTS+=("${_a[@]}"); shift ;;
    --prune) PRUNE=1 ;;
    --set-budget) SET_BUDGET=1 ;;
    *) echo "unknown option: $1" >&2; exit 2 ;;
  esac; shift
done
case "$TARGET" in
  claude) DEST="${CLAUDE_HOME:-$HOME/.claude}" ;;
  codex)  DEST="${CODEX_HOME:-$HOME/.codex}" ;;
  agents) DEST="${AGENTS_HOME:-$HOME/.agents}" ;;
  *) echo "unknown target: $TARGET (use claude, codex or agents)" >&2; exit 2 ;;
esac
if [[ $TARGET != claude && ${#EXTRA_AGENTS[@]} -gt 0 ]]; then
  echo "--agent is native to Claude Code only; use scripts/role-to-prompt.py NAME for a portable role brief." >&2
  exit 2
fi
if [[ ${#EXTRA_SKILLS[@]} -gt 0 && $PROFILE_SET == 0 ]]; then PROFILE=none; fi
BACKUP="$DEST/backup/agents-and-skills-$(date +%Y%m%d-%H%M%S)"
run() { if [[ $DRY == 1 ]]; then echo "[dry-run] $*"; else "$@"; fi; }

link() { # $1 source, $2 target
  local src="$1" dst="$2"
  if [[ -L "$dst" && ( "$(readlink "$dst")" == "$src" || "$(cd -P "$(readlink "$dst")" 2>/dev/null && pwd || readlink "$dst")" == "$(cd -P "$src" 2>/dev/null && pwd || echo "$src")" ) ]]; then echo "ok      $dst"; return; fi
  if [[ -e "$dst" || -L "$dst" ]]; then
    run mkdir -p "$BACKUP/$(basename "$(dirname "$dst")")"
    run mv "$dst" "$BACKUP/$(basename "$(dirname "$dst")")/"
    echo "backup  $dst -> $BACKUP"
  fi
  run ln -s "$src" "$dst"; echo "linked  $dst"
}

# Which sources to link: everything (all), or the names a profile lists (checked to exist in the repo).
SKILL_SRCS=(); AGENT_SRCS=()
if [[ $PROFILE == all ]]; then
  # Skills and agents in profiles.json "quarantine" are skipped by default (a skill that failed its eval).
  QUAR="$(python3 -c 'import json,sys; d=json.load(open(sys.argv[1])).get("quarantine",{}); print(" ".join(d.get("skills",[])+d.get("agents",[])))' "$REPO/scripts/profiles.json")"
  # Skills in profiles.json "default.skills_excluded" (tied or lost against no skill) are not linked by default either.
  DEFX="$(python3 -c 'import json,sys; print(" ".join(json.load(open(sys.argv[1])).get("default",{}).get("skills_excluded",[])))' "$REPO/scripts/profiles.json")"
  for s in "$REPO"/skills/*/; do s="${s%/}"; n="$(basename "$s")"; [[ " $QUAR " == *" $n "* ]] && { echo "skip    $n (quarantine)"; continue; }; [[ " $DEFX " == *" $n "* ]] && continue; [[ -f "$s/SKILL.md" ]] && SKILL_SRCS+=("$s"); done
  # Default install links only the agents in profiles.json "default.agents" (others: use --profile).
  DEFA="$(python3 -c 'import json,sys; print(" ".join(json.load(open(sys.argv[1])).get("default",{}).get("agents",[])))' "$REPO/scripts/profiles.json")"
  for a in "$REPO"/agents/*.md; do n="$(basename "$a" .md)"; [[ " $QUAR " == *" $n "* ]] && { echo "skip    $n (quarantine)"; continue; }; if [[ -n "$DEFA" && " $DEFA " != *" $n "* ]]; then continue; fi; AGENT_SRCS+=("$a"); done
elif [[ $PROFILE != none ]]; then
  RESOLVED="$(python3 - "$REPO" "$PROFILE" <<'PY'
import json, os, sys
repo, arg = sys.argv[1], sys.argv[2]
with open(os.path.join(repo, "scripts", "profiles.json")) as f:
    data = json.load(f)
profiles = data["profiles"]
out, seen = [], set()
for p in [x.strip() for x in arg.split(",") if x.strip()]:
    if p not in profiles:
        sys.exit(f"unknown profile: {p} (available: {', '.join(profiles)}, all)")
    for kind, key in (("skill", "skills"), ("agent", "agents")):
        for n in data["always"][key] + profiles[p][key]:
            if (kind, n) in seen:
                continue
            seen.add((kind, n))
            path = os.path.join(repo, "skills", n, "SKILL.md") if kind == "skill" else os.path.join(repo, "agents", n + ".md")
            if not os.path.isfile(path):
                sys.exit(f"profile {p}: no {kind} named {n} in the repo")
            out.append(f"{kind} {n}")
if not out:
    sys.exit("empty --profile")
print("\n".join(out))
PY
)"
  while read -r kind name; do
    case "$kind" in
      skill) SKILL_SRCS+=("$REPO/skills/$name") ;;
      agent) AGENT_SRCS+=("$REPO/agents/$name.md") ;;
    esac
  done <<< "$RESOLVED"
fi

for n in ${EXTRA_SKILLS[@]+"${EXTRA_SKILLS[@]}"}; do
  [[ -z "$n" ]] && continue
  [[ -f "$REPO/skills/$n/SKILL.md" ]] || { echo "no skill named $n in skills/" >&2; exit 2; }
  SKILL_SRCS+=("$REPO/skills/$n")
done

for n in ${EXTRA_AGENTS[@]+"${EXTRA_AGENTS[@]}"}; do
  [[ -z "$n" ]] && continue
  [[ -f "$REPO/agents/$n.md" ]] || { echo "no agent named $n in agents/" >&2; exit 2; }
  AGENT_SRCS+=("$REPO/agents/$n.md")
done

run mkdir -p "$DEST/skills"
for s in ${SKILL_SRCS[@]+"${SKILL_SRCS[@]}"}; do link "$s" "$DEST/skills/$(basename "$s")"; done
if [[ $TARGET == claude ]]; then
  run mkdir -p "$DEST/agents"
  for a in ${AGENT_SRCS[@]+"${AGENT_SRCS[@]}"}; do link "$a" "$DEST/agents/$(basename "$a")"; done
fi
if [[ $PRUNE == 1 ]]; then
  KEEP="$(printf '%s\n' ${SKILL_SRCS[@]+"${SKILL_SRCS[@]}"} ${AGENT_SRCS[@]+"${AGENT_SRCS[@]}"})"
  while read -r l; do
    [[ -z "$l" ]] && continue
    run rm "$l"; if [[ $DRY == 1 ]]; then echo "would prune $l"; else echo "pruned  $l"; fi
  done < <(python3 - "$REPO" "$DEST" "$TARGET" "$KEEP" <<'PY'
import os, sys
repo, dest, target, keep = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
real = lambda p: os.path.normcase(os.path.realpath(p))
repo_r = real(repo)
keep_r = {real(k) for k in keep.split("\n") if k}
for sub in (["skills", "agents"] if target == "claude" else ["skills"]):
    d = os.path.join(dest, sub)
    if not os.path.isdir(d):
        continue
    for name in sorted(os.listdir(d)):
        p = os.path.join(d, name)
        if not os.path.islink(p):
            continue
        t = os.readlink(p)
        t_abs = t if os.path.isabs(t) else os.path.join(d, t)
        t_r = real(t_abs)
        if (t_r == repo_r or t_r.startswith(repo_r + os.sep)) and t_r not in keep_r:
            print(p)
PY
)
fi
if [[ $TARGET == claude ]]; then
  SETTINGS="$DEST/settings.json"
  HAS_BUDGET="$(python3 - "$SETTINGS" <<'PY'
import json, sys
try:
    print("yes" if "skillListingBudgetFraction" in json.load(open(sys.argv[1])) else "no")
except FileNotFoundError:
    print("no")
except Exception:
    print("unreadable")
PY
)"
  if [[ $HAS_BUDGET == no && $SET_BUDGET == 0 ]]; then
    echo "note    skillListingBudgetFraction is not set in $SETTINGS; with many skills some descriptions get dropped. Rerun with --set-budget to set 0.02."
  elif [[ $HAS_BUDGET == no && $SET_BUDGET == 1 ]]; then
    if [[ $DRY == 1 ]]; then echo "[dry-run] set skillListingBudgetFraction 0.02 in $SETTINGS"; else
      python3 - "$SETTINGS" <<'PY'
import json, os, sys, shutil, time
p = sys.argv[1]
data = {}
if os.path.exists(p):
    shutil.copy2(p, p + ".bak-" + time.strftime("%Y%m%d-%H%M%S"))
    data = json.load(open(p))
data["skillListingBudgetFraction"] = 0.02
tmp = p + ".tmp"
with open(tmp, "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False); f.write("\n")
if os.path.exists(p):
    os.chmod(tmp, os.stat(p).st_mode & 0o777)
os.replace(tmp, p)
PY
      echo "set     skillListingBudgetFraction 0.02 in $SETTINGS (backup next to it)"
    fi
  elif [[ $HAS_BUDGET == unreadable ]]; then
    echo "note    could not read $SETTINGS as JSON; skillListingBudgetFraction not checked."
  fi
fi
echo "Done ($TARGET, profile $PROFILE). Restart the tool's sessions to load new skills."

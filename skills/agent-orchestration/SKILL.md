---
name: agent-orchestration
description: Plan and dispatch Claude Code agents without wasting quota - choose model and effort per task type, decide whether to spawn at all, write short self-contained briefs, forbid nested subagents, cap parallelism by machine RAM, run one heavy job at a time, use worktrees for parallel edits, supervise drift and loops, verify agent reports, diagnose why agents burn quota or stall, pace by quota. Use it whenever someone says "which model for this", "should I spawn an agent", "split this across agents", "run these in parallel", "write the brief for the agent", "my quota burns too fast", "agents are slow or stuck", "the agent says it is done but nothing changed", "background or foreground", or is about to dispatch more than one agent. Not for the agent loop inside a product you are building (llm-engineering), system design (software-architecture) or reviewing a diff (code-review-criteria).
license: CC-BY-SA-4.0
metadata:
  author: Júlio Machado
  source: https://github.com/juliomachadome/tested-agent-skills
---

# Agent orchestration

An agent is a cost, not a default. Each one re-reads context, burns quota and returns a summary that may be wrong. Spawn only when it saves more than it costs, and write the brief so the first run is the last. Evidence tags: **[C]** official docs or consensus, **[M]** published engineering report, **[F]** practitioner or house rule, **[X]** myth. Never copy source text; apply the idea. Estimates (tokens, RAM, minutes) are planning ranges to replace with a local measurement.

## 1. Start: project first, then data
Read the current project's CLAUDE.md or AGENTS.md, agent roster files, task and state docs, machine limits, test and commit policy, forbidden commands. Project rules win over this skill. Check what already exists (a running or finished agent can be continued instead of respawned) and which model names the project actually offers.
Ask for, or measure, before planning: **tasks** (outputs, which files each touches, what depends on what); **machine** (RAM, containers or servers running, `ps -o rss`); **quota** (remaining percent, reset time, `/usage`); **history** (what already failed, what is ruled out). If data is missing, state the assumption instead of inventing it.

## 2. Spawn or do it inline?
Inline when: about 5 tool calls; you know the file; a lookup; the task needs your full conversation; the steps are one tight chain **[F]**. Spawn when: independent outputs can run in parallel; the output is large and you need only the conclusion; a fresh unbiased read is the point (review); the work is long and you can do something else **[M]**. Multi-agent runs used about 15x the tokens of a chat and fit breadth-first work, not coding with shared context **[M]**. Test: could a competent person take a two-paragraph note and return what you need? If not, do it inline. Full flow: `references/playbooks.md` section 1.

## 3. Model and effort
Haiku low for mechanical work; Sonnet medium to write; Sonnet high to review or debug; the top model (Opus, or the alias the project names) high only for architecture and hard decisions. Start low, escalate on evidence, never run the top model on repeats, never let the author be the only reviewer, set `model` and `effort` in the agent definition **[F]/[C]**. Names, aliases and prices change: the table is dated and sourced in `playbooks.md` section 3 (checked 2026-11-15); confirm before quoting.

## 4. No nested subagents; cap parallelism
By default a subagent can spawn subagents several layers deep, multiplying cost **[C]**. House rule **[F]**: workers never spawn workers. Enforce twice: leave Agent out of the worker's tools, and write "do NOT spawn subagents" in the brief. Live agents: 2-3 is the normal ceiling, fewer on a low-RAM machine; one heavy job (build, full test run, headless browser, container, model run) at a time; read-only research may run wider. A 16 GB machine has roughly 7 GB left after the system and a container VM, which fits one heavy job plus three agent CLIs and not eight test runs (est.; measure locally; `diagnosis-playbook.md` item 6). Coordination paths grow as n(n-1)/2 (3 workers: 3; 8 workers: 28) **[C]**.

## 5. The brief
Goal and why; done-when as a testable condition; what is known or ruled out; exact files to read and to change; forbidden actions (spawn, commit, heavy commands); caps on turns and web calls; output size and format with guesses marked; effort. Pointers to files, never pasted contents. Template, a weak and a strong example, and common failures: `playbooks.md` section 2.

## 6. Parallel edits and pipelines
Disjoint files or one worktree each **[C]**; one owner for shared files (lockfiles, schemas, indexes); commit with explicit paths, never add-all, stash or reset someone else's work **[F]**. Patterns: writer then independent verifier; capped fan-out; background plus notification; read-only helper that writes findings to a file; handoff state file. Details: `playbooks.md` section 4.

## 7. Foreground, background, pacing
Foreground when you need the result to continue and it is short; background when it is long and independent, and wait for the notification instead of polling **[C]**. Pre-approve the tools a background worker needs or a permission prompt stalls it. Pace by remaining quota, not the clock: compute allowed burn per day, order by value, keep a 10-15% reserve, check after each wave, hand off cleanly with a state file when a window is nearly spent **[F]**. A run during a usage-limit cut-off returns nothing and looks like a score of 0; check quota first. Routine: `playbooks.md` section 8.

## 8. Diagnose when it goes wrong
Run `references/diagnosis-playbook.md` top-down. Step 0: is the evidence real (a report is a claim until the diff and the proving command confirm it; a failed harness is not a zero; a parser that finds nothing must not overwrite data)? Then the symptom tree: quota burning, scope drift, loops, success with no change, two agents on one file, machine swapping, nested spawns, bad brief, contradicting results, silent background task, permission denied, wrong model, routing to the generic agent, false zero scores. Each branch gives causes, the check and the fix, with worked token, RAM and wall-time numbers.

## 9. Verify before trusting
Before relaying a report: `git status` and `git diff --stat` against the declared scope; read the diff for skipped tests, loosened assertions and hard-coded values; rerun the proving command and read passed, failed and skipped; compare numbers with the source; scan for "should work"; confirm heavy processes stopped. Verdict: accepted, accepted with caveats, or rejected. Checklist: `playbooks.md` section 5. Supervision ladder (nudge, contain, stop) and rate-limit handling: section 6.

## 10. Test only what changed; evaluate your setup
Per diff: unit tests of touched packages and the one flow touched; the full gate belongs to CI **[F]**. During a build-heavy batch, workers write and compile, then one test pass and one batch of fixes. To evaluate skills and agents: trigger tests with several runs and all skills loaded together, blind with/without comparison, agent routing test stopped at the tool call, and harness checks that prevent false zeros (`playbooks.md` section 7).

## 11. Output
A dispatch plan table: task, why separate, agent and model, effort, files in scope, depends on, heavy yes or no, expected output, verification step; then the order, live-agent count, estimated cost (relative) and stop condition. Say what you chose not to spawn and why, which numbers are estimates to measure, and what you could not verify.

## Smells that mean stop and re-plan
Three agents on one chain of steps; a brief longer than the task; an agent told to "check everything"; reruns on the top model; waiting loops on a process that is not yours; reports without evidence; eight agents each running the test suite. Worked example: four independent tasks of 3 min writing plus 3 min of heavy tests, 2 min each to verify, take 32 min one after another and about 23 min with parallel writers and one heavy slot, because the heavy job and your verification are the bottleneck, not the agent count (Little's law **[C]**).

## AI tells to avoid (check while answering, not after)
- Spawning agents by default instead of doing a short task inline.
- Vague briefs with no done-when, files or forbidden actions.
- Trusting an agent's report without the diff and the proving command.
- Parallelism with no RAM or quota check.
- Top model and high effort on mechanical work.
Fix: use the user's case and data, sources actually read, one recommendation with its reason and how to verify it. Say what you chose and why in one line; a choice without a reason is removed.

## Which reference to open
- Something went wrong, or a number is needed (quota, RAM, time): `references/diagnosis-playbook.md`
- Deciding, writing a brief, picking a model, pipelines, verifying, supervising, evaluating, pacing: `references/playbooks.md`
- Sources and their status: `references/BIBLIOGRAPHY.md`
Related skills: llm-engineering, software-architecture, code-review-criteria, qa-verification.

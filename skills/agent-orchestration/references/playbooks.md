# Playbooks

Routines to copy and fill. Tags: **[C]** official docs or consensus, **[M]** published report, **[F]** practitioner or house rule. Pair with `diagnosis-playbook.md` when something already went wrong. Merged from the former brief template, dispatch checklist and supervision notes.

## 1. Decide to spawn (flow)
Ask in order; stop at the first yes.
1. Can I finish in about 5 tool calls, or is it a lookup of a known file? **Inline.**
2. Does the task need my full conversation context, or are its steps a tight chain (each needs the last)? **Inline** (or one agent for the whole chain) **[M]**.
3. Does a running or finished agent already hold the context? **Continue it** (SendMessage) instead of spawning.
4. Is the output big and I only need the conclusion (wide search, long logs)? **One read-only agent.**
5. Are there independent outputs that do not share files? **Parallel agents, capped** (section 4).
6. Do I want an unbiased read of finished work? **A fresh reviewer**, never the author.
7. Would the money matter? Estimate cost (diagnosis-playbook, worked numbers). If it costs more than the time it saves, **inline**.
Test: could a competent person take a two-paragraph note and return what I need? If not, it is not ready to delegate. Multi-agent runs cost about 15x a chat and fit breadth-first work better than coding **[M]**.

## 2. Writing the brief
A brief is the worker's whole world. Pointers to files, never pasted contents.

```
Goal: <one or two sentences, with the reason>
Done when: <testable condition: command and expected result>
Already known or ruled out: <bullets, so it does not rediscover>
Read first: <exact paths and sections>; project rules that apply: <paths>
Files you may change: <list>   Files you must not touch: <list>
Do: <numbered steps, only what is needed>
Do NOT: spawn subagents or use Agent/Task/Workflow tools; commit or push; run <heavy or forbidden commands>; exceed <N> web calls or <N> turns.
Machine limits: <one heavy job at a time, no browser, no containers>
Output (under <N> lines): <table or list>; facts separate from guesses; unverified items marked; absolute paths of files created or changed.
Effort: <quick lookup | normal | deep review>
```
Weak: "Look at the checkout code and fix whatever is wrong." Strong: "Goal: the discount rounds half up, the spec says half even (docs/pricing.md section 3). Done when `npm test -- pricing` passes and no other test changes status. Ruled out: the currency table (checked). Files: src/pricing/round.ts, its spec. No commit. Report: the diff stat and the test summary, under 15 lines." Common failures: no done-when (the agent decides), no ruled-out list (rediscovery), no output cap (a 3,000-word report to read), the same brief sent to two agents (duplicated work) **[M]**.

## 3. Model and effort by task type (checked 2026-11-15)
Names and prices drift; confirm in the Claude Code model configuration page and the pricing page before relying on this table. On 2026-11-15 the aliases resolved on the Anthropic API to Haiku 5.5 (`claude-haiku-5-5`), Sonnet 5.5, Opus 5.5 and the `fable` alias to Fable 5.2; `medium` is the default effort on all four **[C]**.
| Task type | Model | Effort | Why |
|---|---|---|---|
| Collect facts, rename, format, rerun a known command, classify | Haiku | low | no judgement; about 1/20 the Sonnet price |
| Implement against a clear design, write tests, docs, scripts | Sonnet | medium | best cost and quality for building |
| Debug a hard failure, security-sensitive change | Sonnet | high | edge cases matter; verifying costs more than thinking |
| Review a diff or a document | Sonnet | high | a different model instance than the author **[F]** |
| Architecture, trade-offs, ambiguous requirements, plan review | Opus, or the top alias if the project names it | high | rare and expensive; wrong here costs weeks |
| Hard open-ended problem you leave alone | top model | xhigh or max | max can overthink; test before adopting **[C]** |
Rules: start low and escalate on evidence of failure; the same level name is calibrated per model, so do not copy a level across models **[C]**; set `model` and `effort` in the agent definition (a subagent with no effort of its own inherits the session level only on the session's model) **[C]**; never run the top model on repeats.

## 4. Pipeline patterns
- **Writer then verifier.** Agent A changes code; agent B (read-only, fresh context, different brief) runs the checks and reports PASS, FAIL or NOT VERIFIED with output. A never grades itself.
- **Capped fan-out.** Split by independent outputs (one package, one document), at most 2-3 live, one heavy job. Queue the rest; a queued task holds no slot. Merge in a fixed order and resolve conflicts yourself.
- **Background plus notification.** Long, independent work runs in the background while you do other work; wait for the notification, never poll in a loop **[C]**. Pre-approve the tools it needs, or a permission prompt stalls it.
- **Read-only parallel helper.** Researchers read widely and write findings to a file (path in the brief); the owner reads the file and applies the change. No helper edits shared files.
- **Parallel writers.** One worktree each or disjoint files; shared files (lockfiles, schemas, indexes) have one owner.
- **Handoff file.** Every long job keeps a state file: done, half-done, decisions, next step. A fresh agent can resume from it.

## 5. Verifying an agent report
Before relaying anything as true:
1. `git status` and `git diff --stat`: are the changed paths inside the declared scope? Anything unexpected (lockfile, config, another package)?
2. `git diff`: skipped or deleted tests, loosened assertions, hard-coded expected values, edited fixtures, catch-all error handling.
3. Rerun the proving command yourself; read passed, failed and skipped, not only the last line.
4. Check numbers against the source file or command.
5. Language scan: "should work", "likely", "I believe", unmarked guesses, no command output.
6. Are heavy processes, containers and servers stopped? Temp files removed?
7. Is the report's size and format what the brief asked for?
Verdict, one of: **accepted** (evidence seen), **accepted with caveats** (list), **rejected** (what failed, the output). A report without evidence is a claim **[F]**. For high-risk work escalate to a stronger or different reviewer instead of rerunning the same agent.

## 6. Supervising a running worker
| Drift | What you see | First response |
|---|---|---|
| Role | a read-only researcher edits files | block the action, restate allowed tools and paths |
| Scope | refactors or features nobody asked for | quote the goal, drop the side work |
| Loop | the same call three to five times | stop it; different approach or inline |
| Invented progress | "done" with no diff or output | reject, demand the command and its output |
Ladder: **nudge** once (goal plus the exact deviation), **contain** (revert out-of-scope files, drop the polluted context, resend a lean summary), **stop** (end it, note what went wrong, fresh worker or inline). Give each worker a turn ceiling (`maxTurns` **[C]**); at 80 percent without a changed file or passing check, inspect instead of extending. Ledger: running, queued, done, failed (logic or drift), paused (rate limited). On a 429 or quota message: stop, keep the task text, back off (a few seconds, doubling, about a minute cap, about five tries), then report as failed and continue; never auto-retry non-rate-limit failures; do not raise the cap to clear a backlog.

## 7. Evaluating skills and agents
Method that avoids fooling yourself **[F]**, consistent with the skill-evaluation guidance of the Agent Skills project **[C]**:
- **Trigger test.** 10 queries (5 should trigger, 5 near-misses that should not); load every skill together as one plugin so the target competes with its neighbours; run each query 3 times and count a trigger when it fires in most runs; use a small model and a 2-turn cap; stop the run at the first Skill call. Pass: at most one miss and at most one false trigger.
- **With and without, blind.** Answer each task once with the skill and once without any skill; a judge that does not know which is which scores both against written assertions; shuffle the order. Ask the judge for JSON and parse the first JSON object; on a parse failure keep the raw text and rerun the judge, not the answers.
- **Agent routing test.** Load all agent files (copy them; symlinks are not loaded); tell the main model to delegate; stop the run at the first Agent call so the chosen subagent does not do the task; compare the pick with the expected agent; several runs per task.
- **Run the checks that prevent false zeros.** The harness runs in an empty temporary directory; a directory that must be read is added explicitly with the read tool allowed; count empty results; confirm quota before starting; a parser that finds zero entries stops and leaves the data alone.
- Report n/runs, the date, the model and what could not be tested.

## 8. Quota pacing
1. Read the remaining quota and the reset time (`/usage`); compute allowed burn per day = remaining % / days left. Example: 38% left with 5 days is 7.6% a day.
2. List the work with an estimated cost in percent; most valuable first; route cheap models to routine work.
3. Hold back a reserve (10-15%) for fixes and verification **[F]**.
4. Check at fixed points (after each wave), not by the clock; if the burn rate is above plan, drop the lowest-value item or move work to a cheaper model before the next wave.
5. Near the limit, stop cleanly: write the handoff file (done, half-done, decisions, next), stop background work, confirm nothing is half-written.
6. After a cut-off, treat empty results as a pause, not a failure (diagnosis-playbook Step 0).

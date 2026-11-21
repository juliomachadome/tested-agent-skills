---
name: redigir
description: Guided copywriting command. Collects the brief, then writes with the existing offers, storytelling and copywriting skills.
disable-model-invocation: true
argument-hint: "[what to write, for whom]"
license: CC-BY-SA-4.0
metadata:
  author: Júlio Machado
  source: https://github.com/juliomachadome/tested-agent-skills
---

# /redigir

No new knowledge here: collect the brief, then hand off to existing skills.

1. **Fill from context.** Read $ARGUMENTS and the current project (CLAUDE.md or AGENTS.md, README, existing pages). Fill what you can: product, audience, offer, tone.
2. **Ask only what is missing**, with AskUserQuestion (tap options, at most 4 questions per call). Topics: format; audience and what they already tried; offer; proof; goal (one action); objections; tone; limits (what must not be said or changed).
3. **Proof.** Without a real number or testimonial from the user, record "no proof" and never invent one.
4. **Show the brief in 8 lines** (format, audience, offer, proof, goal, objections, tone, limits) and wait for an explicit ok.
5. **Write in the main session, no subagent.** Sales page: load `offers`, then `storytelling`, then `copywriting`. Any other format: `copywriting` only.
6. **Deliver** 3 versions of headline and call to action, each with its bet in one line (which reader and which objection it targets); then the full piece in the version the user picks.

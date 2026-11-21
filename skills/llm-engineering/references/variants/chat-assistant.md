# Variant: chat assistant with memory

Use for: multi-turn assistants in a product (support, coaching, onboarding, internal help), with persona, history and possibly retrieval or tools.

## Architecture choice
A stateless call per turn with a context you assemble: system prompt, a rolling summary, the last few turns, retrieved facts and the user's profile fields, in that order for a stable cacheable prefix. Keep memory as data you control (a table or documents the user can see and delete), not an invisible growing transcript. Add RAG (`rag-qa.md`) or tools (`agents-tools.md`) only for the turns that need them; route small talk and simple intents to a small model. Detail: `../agents-tools.md` (memory), `../use-cases.md` section 6.

## Prompt pattern
Role and tone in a few specific sentences; scope and refusals with reasons; when to ask a clarifying question; the format of answers (short by default); the escalation rule to a human; user data in a fenced block, never mixed with rules. Provider notes: current Claude models reject assistant prefill, so steer format with instructions or structured output; Gemini and Claude sampling parameters may be fixed on reasoning models, so check the docs rather than assuming `temperature` works (`../prompting-context.md`).

## Eval metrics
- Conversation-level task success and resolution without escalation, on scripted multi-turn test dialogues plus a monthly sample of real ones (consented, de-identified).
- Turn-level groundedness where facts are retrieved; refusal correctness; tone and policy rubric with a calibrated judge.
- Memory tests: remembers a stated fact after 20 turns, forgets on request, does not leak across users.
- Cost per conversation and p95 time to first token; abandonment and thumbs as outcome signals.

## Failure modes
Persona drift over long chats; context growing until cost and latency explode; stale or wrong memory stated as fact; leakage of one user's memory or documents into another's session; over-agreeing with the user; prompt injection through pasted text; revealing the system prompt (OWASP LLM07); the assistant promising things the business cannot do.

## Cost notes
Input dominates because history is re-sent every turn. Cache the stable prefix (the cache refreshes on use; default lifetime is minutes, so idle conversations pay the write again), summarise old turns on a schedule, cap history by tokens, cap output length, stream for perceived speed, per-user daily quota. Compute cost per conversation as average turns times tokens per turn times price (`../diagnosis-playbook.md` shows the arithmetic).

## Checklist
- [ ] Memory is explicit, visible, deletable, per user, with retention limits.
- [ ] Tenant and user filters in code on every retrieval and memory read.
- [ ] Context budget and summarisation rule written down.
- [ ] Escalation path to a human and a way to see the transcript.
- [ ] Rate limits, quotas and abuse handling.
- [ ] Multi-turn eval dialogues, including adversarial and injection ones.
- [ ] Personal data policy and provider retention terms checked.

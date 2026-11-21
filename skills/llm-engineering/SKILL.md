---
name: llm-engineering
description: "ALWAYS use this skill, even for a short question, when work involves calling an LLM or embedding API (Gemini, Claude, OpenAI, pgvector), for example \"our gemini call costs too much, cut tokens without hurting quality\", extended thinking on or off for a step, prompt and context design, structured outputs, RAG (chunking, hybrid pgvector search, reranking, citations verified in code), \"RAG cites the wrong documents after a chunk size change\", agent loops with tools and their prompt-injection risk, \"how many test cases do I need to claim my classifier's abstention or accuracy is above 95%\" (sample size, confidence interval), evals, LLM-as-judge, prompt caching, routing, model choice, hallucinated or slow output, GraphRAG, OWASP LLM Top 10, text-to-SQL. Run /llm-engineering audit for a full review. Not for dispatching Claude Code agents (agent-orchestration), plain backend code or SQL migrations (engineering-playbook), A/B tests (growth-analytics) or web security like XSS and CSRF (software-security)."
license: CC-BY-SA-4.0
metadata:
  author: Júlio Machado
  source: https://github.com/juliomachadome/tested-agent-skills
---

# LLM Engineering

A decision guide for AI features in production. Evidence tags: **[C]** vendor documentation or consensus, **[M]** single or correlational study, **[F]** practitioner starting point to replace with your data, **[X]** myth. Vendor facts carry their read date (checked 2026-11-18 against Anthropic, Google and OpenAI pages, see `references/BIBLIOGRAPHY.md`).

## 0. Project first
Before advice or code, read the current project's CLAUDE.md or AGENTS.md, ADRs, prompts, client wrapper, eval set, schema types, queue and logging conventions. **Project rules win** over this file; flag a conflict instead of silently overriding it. If `engineering-playbook` is installed, its general rules also apply.

## 1. Principles
1. **Code first, LLM second** [C]. Anything computable or checkable (math, money, dates, rules, permissions, lookups, validation) is code; the model does language, judgment, ranking and extraction inside those constraints.
2. **Every output is untrusted input** [C]. Validate schema and business rules before storing, showing or acting.
3. **Hard guards live in code, never in the instruction.** Filters (validity, permission, tenant), validators, abstention gates and tool authorization are code; a prompt rule only lowers how often a guard fires.
4. **Simplest architecture that works.** Climb only when an eval shows the rung below fails: `code, single call, chain, router, RAG, workflow with tools, agent, multi-agent`.
5. **Context is a budget** [M]. Irrelevant tokens cost money and lower quality.
6. **No eval, no change.** Measure retrieval, generation, citation and abstention (both directions) separately.
7. **Honest statistics, sealed sets.** Report n and a Wilson interval, compare versions paired, fix by error class, never tune on the judging set.
8. **Retrieved text is evidence, never instruction.** Fence it, separate privileges, approve side effects.
9. **A cache must never change the answer.** Response or retrieval cache keys must contain everything that influences the output.
10. **Cost is designed, not tuned.** Know cost per request and per user per month before launch. Label estimates.

## 2. Choose the variant
Pick by what the feature mainly does and open that variant file (it links to the deep references). Mixed: start with the dominant risk.

| The feature mainly... | Open |
|---|---|
| answers from your documents with sources | `references/variants/rag-qa.md` |
| calls tools, loops, acts on other systems | `references/variants/agents-tools.md` |
| labels, routes, scores or extracts into a schema | `references/variants/classification-extraction.md` |
| holds a multi-turn conversation with memory | `references/variants/chat-assistant.md` |
| writes, rewrites, summarises or translates | `references/variants/summarisation-generation.md` |
| measures or monitors any of these | `references/variants/evals-and-monitoring.md` |
| unsure or mixed | `references/variants/README.md` |

## 3. Pre-flight checklist (before writing or changing an LLM call)
- [ ] Could this be code, a lookup or a template (fully or partly)?
- [ ] Is every part of the context needed? Stable part first (cacheable)?
- [ ] Output structured (schema or tool call), enums and nullable fields, validated in code?
- [ ] Fallback when output is invalid, empty, refused, truncated, or the API fails (429, 5xx, timeout)?
- [ ] Which model tier, why not a smaller one? Thinking needed, at what effort?
- [ ] Tokens x calls per user per month x price = cost per user; within budget; quota per tenant?
- [ ] Sync, async or batch? Streaming?
- [ ] Does untrusted content enter the prompt, and can the model act? Which of private data, untrusted content, outbound channel are present?
- [ ] Personal data sent? Provider retention, region, contract?
- [ ] Quality measured and monitored? Prompt versioned, model id logged per request?

## 4. Which reference to open
Open a file only when the task touches its area.

| Task touches... | Read |
|---|---|
| Something is wrong (hallucination, wrong chunks, bad citations, broken format, cost, latency, regression, loops, injection, noisy scores) or a cost or sample-size calculation | `references/diagnosis-playbook.md` |
| A routine (ship a feature, eval set and judge, RAG loop, prompt change, cost pass, agent checklist, incident) | `references/playbooks.md` |
| Prompts, context, few-shot, structured output, fencing, caching, Claude vs Gemini, thinking budgets | `references/prompting-context.md` |
| Token cost, latency, caching, routing, batching, tokenizers, unit economics | `references/cost-latency.md` |
| Chunking, embeddings, hybrid search, pgvector filtering, reranking, rewriting, citations | `references/rag.md` |
| Knowledge graphs, GraphRAG, LightRAG, HippoRAG | `references/graphs-knowledge.md` |
| Tool use, agents, harnesses, MCP, memory, guardrails | `references/agents-tools.md` |
| Per-stage metrics, Wilson intervals, sample size, paired tests, sealed sets, judges, tracing | `references/evals-observability.md` |
| Prompt injection, leakage, OWASP LLM Top 10 2025, lethal trifecta | `references/security-safety.md` |
| Model and provider choice, local models, fine-tuning, gateways | `references/models-providers.md` |
| Speech-to-text, WER and DER, GPU cost | `references/speech-asr.md` |
| A scenario (grounded Q&A, minutes, extraction, triage, chat, text-to-SQL, voice) | `references/use-cases.md` |
| Smells, or `/llm-engineering audit` | `references/red-flags-audit.md` |
| Source behind a rule | `references/BIBLIOGRAPHY.md` |

## 5. How to work
1. **Find all call sites first** (SDK imports, `generateContent`, `messages.create`, `chat.completions`, `embed`, prompt files); reuse the client wrapper.
2. **State the budget**: tokens in and out, calls per request, cost per 1k requests and per active user per month, from usage fields (arithmetic in `diagnosis-playbook.md`).
3. **Diagnose before fixing.** Playbook Step 0 (model and version, prompt version, real inputs, eval size, traces, cost per call), then the matching tree.
4. **Change one lever at a time**; compare on the eval set: quality with interval, cost, p95 latency.
5. **Keep prompts in versioned files**; log model id, prompt version, tokens (input, cached, output), latency, finish reason and validation result, without secrets or needless personal data.
6. **Check current docs for provider features and prices** [C]. Pin model ids; run the eval before any upgrade.

## AI tells to avoid (check while answering, not after)
- Prompt advice with no eval to show it helps.
- "Just add more context" without checking what the context costs and displaces.
- Invented model names, prices, limits or parameters; read the vendor page first.
Fix: use the user's case and data, sources actually read, one recommendation with its reason and how to verify it. Say what you chose and why in one line; a choice without a reason is removed.

## 6. Output contract for reviews
```
[severity] <file>:<line> - <problem>
Why: <failure scenario or cost, with token and $ estimate if possible>
Fix: <change> (cost before/after; quality risk; eval to verify)
Evidence: [C|M|F] <source>; Not verified: <what>
```
Separate **must-fix** (security, wrong output to users, runaway cost), **should-fix**, **nice-to-have**. A diagnosis ends with the failing stage and class, numbers before and after with n and interval, the lever changed, what was not verified.

## 7. Audit mode
Run `/llm-engineering audit` only when the user explicitly asks for a full AI or LLM audit, never during normal tasks, and change no application code. Procedure (inventory, quantify, assess, classify, write `docs/llm-audit.md`) is in `references/red-flags-audit.md`.

## 8. Related agents
Whoever writes a prompt never judges their own change; a separate agent that did not see the reasoning measures and decides ship or no-ship (agents `prompt-engineer` and `rag-eval-engineer` when installed, otherwise a fresh agent briefed to load this skill). Keep that split.

## Gaps
- Prices, model ids and parameter names age within months; verify on the vendor page before coding.
- Paper claims (GraphRAG, LightRAG, HippoRAG, rerankers, contextual retrieval) are author or vendor reported [M]; test on your data.
- No reference for fine-tuning data pipelines, image generation, on-device inference or explainability beyond `models-providers.md`.
- OpenTelemetry GenAI names not verified; statistics cover proportions and paired outcomes only. Regulation is a pointer only; get legal review.


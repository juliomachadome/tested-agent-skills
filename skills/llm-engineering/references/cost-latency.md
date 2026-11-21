# Cost & Latency Optimization

Prices change often: keep prices as configuration, check current provider pricing pages, and compute with real token counts from API `usage` fields.

## 1. Unit economics first

```
cost_per_call   = in_tokens × in_price + cached_tokens × cached_price + out_tokens × out_price (+ thinking tokens, usually billed as output)
cost_per_user_m = Σ_features (calls_per_user_per_month × cost_per_call)
gross_margin    = (price_per_user_m − ai_cost_per_user_m − infra − payment fees) / price_per_user_m
```

- Define a **target AI cost per active user per month** (e.g. ≤ 10–20% of the subscription price) and design features to fit it.
- Track the distribution, not just the average: heavy users can cost 10–50× the median → quotas, fair-use limits, or usage-based tiers.
- Output tokens are typically several times more expensive than input tokens and generated sequentially (latency). Reducing output is often the biggest lever.

## 2. Levers ranked (do the cheap, safe ones first)

| # | Lever | Typical effect | Quality risk |
|---|---|---|---|
| 1 | **Don't call the LLM** (code, lookup, template, cache of final result) | −100% for that path | none if deterministic |
| 2 | **Prompt caching**: stable prefix first; explicit cache where the provider offers it; implicit/automatic caching benefits from identical prefixes | large discount on cached input tokens; lower latency | none |
| 3 | **Cap and shrink output**: `max_tokens`, concise formats, ids instead of repeated text, no prose wrappers around JSON | −20–70% output | low |
| 4 | **Trim context**: remove unused instructions, dedupe retrieved chunks, fewer/better examples, summaries instead of raw history | −20–80% input | low–medium (eval) |
| 5 | **Batch / flex / async tiers** for non-interactive work (nightly regeneration, backfills, evals, embeddings) | commonly ~50% cheaper | none (latency only) |
| 6 | **Model routing / cascade**: small model first; escalate on low confidence or validation failure | −50–90% on routed traffic | medium (needs eval) |
| 7 | **Reasoning budget control**: disable/low thinking for simple tasks | large on thinking-heavy calls | medium |
| 8 | **Precompute & reuse**: generate templates/blocks once, personalize with code; reuse across users with same profile bucket | −80–99% | medium (personalization) |
| 9 | **Exact-result cache**: hash(normalized input + prompt version + model) → stored output | −100% on hits | none |
| 10 | **Semantic cache** (embedding similarity of queries) | variable | high: wrong answers for "similar but different" — use only for FAQ-like, non-personal queries with high thresholds |
| 11 | **Fine-tune / distill** a small model on outputs of a large one | big at scale | needs data, evals, maintenance |
| 12 | **Self-host open-weight models** | only wins at high, steady volume or for privacy | ops burden; quality gap varies |

## 3. Prompt caching details

- Caches match on an **exact prefix**. Order: tools/function definitions → system prompt → static documents/examples → (cache breakpoint) → dynamic content (user profile, date, question).
- Anything that changes per request (timestamps, request ids, user name, shuffled examples) placed early **destroys** caching.
- Providers differ: some cache automatically above a minimum prompt length (implicit), some require explicit cache markers/objects with a TTL and may charge for cache writes/storage. Check current docs and measure `cached_tokens` in usage to confirm hits.
- Keep a cache-friendly design for multi-turn chat: append-only history; avoid editing earlier turns.

## 4. Model routing patterns

- **Static routing by task:** classification/extraction/formatting → small/fast model; planning/complex generation → larger model.
- **Cascade:** try small model → validate (schema, rules, judge score, self-reported confidence with calibration) → escalate only failures.
- **Router model/classifier:** cheap classifier decides the path (FAQ cache, small model, large model, human).
- Always measure the escalation rate; if most traffic escalates, the cascade costs more.

## 5. Latency

- **Stream** tokens to the UI; show partial structured results progressively (e.g. day 1 of a plan first).
- **Parallelize** independent calls (`Promise.all` / `Task.WhenAll` with limits).
- **Shorter outputs** = faster (output is sequential).
- Smaller model / lower thinking budget for interactive paths; heavy work async with notifications.
- Prompt caching also reduces time-to-first-token.
- Keep connections warm; region close to the provider endpoint; avoid cold starts in serverless for latency-critical AI endpoints.
- Measure **time to first token** and **total time** separately; p95, not average.
- Speculative UI: show deterministic parts immediately (computed by code), LLM fills the rest.

## 6. Embeddings cost

- Embed once, store with model+version; re-embed only changed content (content hash).
- Use batch endpoints for bulk embedding.
- Smaller embedding dimensions (Matryoshka/truncatable embeddings) reduce storage and search cost with small quality loss — evaluate.
- Don't embed boilerplate (headers/footers/navigation).

## 7. Budgets & guardrails

- Per-request: max input size, max output tokens, max tool steps, timeout.
- Per-user/tenant: daily/monthly token or call quotas; soft limit → degrade (smaller model, cached results), hard limit → block with clear message.
- Global: provider spend alerts; circuit breaker on anomalous spend (e.g. bug causing loops).
- Idempotency keys on generation jobs so retries don't regenerate (and re-bill).

## 8. Measure

- Log per call: feature, model, prompt version, input/cached/output/thinking tokens, latency (TTFT, total), finish reason, validation pass/fail, retries, cost (computed), tenant/user (pseudonymous).
- Dashboards: cost per feature/day, cost per active user, cache hit rate, escalation rate, validation failure rate, p95 latency.
- Every optimization: compare **before/after on the eval set** (quality) and on real traffic (cost, latency).

## 9. Product-level levers

- Generate on demand, not eagerly (don't generate 12 weeks of plans if users churn in week 2 — generate the next block when needed).
- Let users regenerate with limits; cache the last result.
- Prefer edit/patch operations ("swap this exercise") over full regeneration.
- Use deterministic substitutions from a catalog where possible; LLM only explains or handles unusual cases.

## Sources

See BIBLIOGRAPHY.md (vendor documentation, guides and papers for this area).

## Tokens, tokenizers and the prefix cache (fundamentals)
- A token is a sub-word unit of the provider's tokenizer; prices, limits and latency are all in tokens, so count tokens, not words or characters. Use the vendor's token-counting endpoint or the usage fields of a real call; local estimates drift between models and languages (non-English text and code usually need more tokens per word).
- A tokenizer change is a cost change at constant text: Anthropic's models overview (read 2026-11-18) says the tokenizer introduced with Claude Opus 4.7 fits about 555k words in 1M tokens, against about 750k words for earlier models, so the same prompts cost more tokens after a migration. Re-measure input tokens when you change model family, and budget with the new count.
- Prefix caching works because the provider keeps the already-computed attention state (key-value cache) for a byte-identical prompt prefix; that is why the stable part must come first and why any change before the breakpoint (tool list, system text, thinking setting) forces a full recompute. Output generation is sequential, so latency grows with output tokens; prompt processing is parallel and cheaper per token.
- Context windows are limits, not targets: 1M-token windows exist on current Claude models, but quality and cost both degrade with irrelevant tokens (see `rag.md` and the position-effect note in `prompting-context.md`).

See also: `diagnosis-playbook.md` (worked cost per request, cache-hit savings, trees for cost and latency), `playbooks.md` section 5 (optimisation pass), `variants/` for per-feature cost notes.

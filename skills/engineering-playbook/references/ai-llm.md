# AI / LLM Features

## 1. Decide if an LLM is the right tool

- Deterministic rules, calculations (calories, macros, money), validation, and anything with a correct answer computable in code → **code**, not the LLM. Use the LLM for language, judgment, personalization, extraction from unstructured input, and ranking — then validate its output with code.
- Hybrid pattern: code computes the constraints/numbers → LLM composes/explains/chooses within them → code validates the result (schema + business rules) → fallback if invalid.

## 2. Prompting (production)

- System prompt: role, task, constraints, output format, examples; keep stable parts first (enables prompt caching).
- Be explicit and specific; give context about why; use XML tags or clear sections to separate instructions from data.
- Few-shot examples covering edge cases; positive and negative examples.
- **Structured output:** JSON schema/tool use (structured outputs) instead of parsing free text; validate with a schema (zod, System.Text.Json + validation); retry with the error message on invalid output (bounded).
- Version prompts in code; changes go through evals (section 6).
- Temperature low for extraction/classification; higher for creative variety.

## 3. Cost & latency

- Cost ≈ input tokens + output tokens × price per model. Output tokens are slower and usually pricier — cap `max_tokens`, ask for concise formats.
- **Prompt caching** for long, repeated prefixes (system prompt, documents, tool definitions) — large savings on cost and latency.
- Model routing: small/fast model for simple classification/extraction; larger model only where quality requires it.
- **Batch APIs** for offline/bulk work (typically ~50% cheaper, async).
- Cache final results for identical inputs (hash of normalized input + prompt version + model).
- Stream responses to the UI for perceived latency.
- Generate once and reuse (e.g., template plans adapted by code) instead of generating everything per user per request.
- Track tokens/cost per feature and per tenant; enforce per-tenant quotas.

## 4. Reliability

- Timeouts, retries with backoff on 429/5xx/overloaded, fallback model/provider, circuit breaker.
- Run long generations as background jobs (queue) with status polling/push, not inside a synchronous HTTP request.
- Idempotency for generation jobs (don't bill or create duplicates on retry).
- Log prompts/responses (with PII controls and retention limits) for debugging and evals.

## 5. RAG (retrieval-augmented generation)

- Pipeline: ingest → clean → **chunk** (by structure/semantics, ~200–800 tokens with overlap) → embed → store (pgvector, Azure AI Search, Qdrant) with metadata (tenant, source, date, permissions) → retrieve (vector + keyword **hybrid**, metadata filters) → **rerank** → build prompt with citations → generate → cite sources.
- Filter by tenant/permissions **at retrieval time** (never rely on the LLM to hide data).
- Evaluate retrieval separately (recall@k) from generation quality.
- Keep embeddings model/version with vectors; re-embed on model change.
- ANN indexes (HNSW, IVF) trade recall for speed — tune parameters.
- Fine-tuning changes behavior/style; RAG supplies knowledge. Prefer RAG + good prompts first.

## 6. Evals (testing LLM features)

- Build an eval set from real cases (inputs + expected properties/reference answers), including edge and adversarial cases.
- Score with code where possible (schema valid, constraints satisfied, numbers match), then **LLM-as-judge** with a clear rubric for subjective qualities; spot-check judges against humans.
- Run evals on every prompt/model/version change; track scores over time; block regressions.
- Monitor production: user feedback, validation failure rates, fallback rates, cost, latency.

## 7. Security (OWASP Top 10 for LLM Applications)

- **Prompt injection** (direct and indirect via retrieved documents, web pages, emails, file uploads): treat model output as untrusted; never give the model more privileges than the user; tools with side effects need authorization checks in code and, for risky actions, human confirmation; separate instructions from untrusted data; don't put secrets in prompts.
- **Insecure output handling:** encode/sanitize LLM output before rendering (XSS), never `eval` it or pass it to SQL/shell.
- **Sensitive data disclosure:** minimize PII sent; check provider data retention/training terms and region (GDPR); redact logs.
- **Excessive agency:** least-privilege tools, scoped credentials, rate limits, audit logs.
- **Denial of wallet:** per-user/tenant rate limits and token budgets; input size limits.
- **Hallucination:** ground in sources, ask for citations, validate facts/numbers in code, allow "I don't know".
- Health/fitness/finance advice: add guardrails and disclaimers; route risky cases (medical conditions, injuries, eating disorder signals) to safe responses and professionals.

## 8. Agents & tool use

- Define small, well-described tools with strict input schemas; validate inputs server-side.
- Cap steps/iterations and total cost; log traces of tool calls.
- Prefer deterministic workflows (fixed chains) over open-ended agents when the steps are known.

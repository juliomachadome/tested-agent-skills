# Models & Providers

Model names, prices and features change monthly. Snapshot checked 2026-11-18 (vendor pages, see BIBLIOGRAPHY 1-14): Anthropic lists claude-fable-5-2, claude-opus-5-5, claude-sonnet-5-5 and claude-haiku-5-5 as current; Google lists Gemini 4 and 3.x models and has scheduled price increases for 2026-12-01 and 2027-01-01; OpenAI lists its GPT-6 family. Treat this paragraph as dated. Keep model ids in configuration, read the provider's current docs before relying on a feature, and re-run evals before switching.

## 1. Choosing a model per task

| Task | Typical choice |
|---|---|
| Classification, routing, extraction, formatting, short rewrites | smallest/fastest tier (flash/lite/haiku/mini class) |
| Grounded Q&A over provided sources | small–mid tier; larger only if evals show misses |
| Complex planning/generation with many constraints | mid–large tier, possibly with reasoning |
| Hard reasoning, ambiguous analysis, agents with many tools, coding | frontier tier with reasoning |
| Embeddings | dedicated embedding model (multilingual when content is not English) |
| Speech-to-text | dedicated STT with diarization (provider STT, Whisper-class models) |
| Reranking | dedicated reranker (cross-encoder) or small LLM |

Pick by **evals on your data**: quality, cost, latency, structured-output reliability, quality in your users' language, context length, tool-use reliability.

## 2. Provider features to check (names vary)

- Structured output with JSON Schema (and which schema features are supported).
- Tool/function calling (parallel calls, forced tool choice).
- Prompt caching: implicit vs explicit, minimum length, TTL, pricing of writes/reads/storage.
- Batch / flex / async processing discounts.
- Reasoning controls (thinking budget/level/effort) and how thinking tokens are billed.
- Context window and output limit; long-context pricing tiers.
- Multimodal inputs (image, PDF, audio, video) and their token accounting.
- Data retention / training use / regions / zero-retention options.
- Rate limits and quota tiers; regional endpoints.
- Model versioning: dated snapshots vs moving aliases; deprecation schedule.

### Notes per ecosystem (verify current docs)
- **Google Gemini API / Vertex AI:** structured output via response schema; implicit caching on recent models plus explicit context caching on some older ones (not on Gemini 4, 2026-11-18); batch mode at a discount; thinking budget/level controls on reasoning models; Flash/Flash-Lite tiers for cheap high-volume work; Vertex for enterprise data controls and EU regions.
- **Anthropic Claude API:** prompt caching with explicit cache breakpoints and TTL options; Message Batches API at a discount; structured outputs / tool use with JSON schema; extended thinking with budget/effort controls; Haiku/Sonnet/Opus tiers; also available via AWS Bedrock and Google Vertex.
- **OpenAI API:** automatic prompt caching (1,024-token minimum on the newest family); Batch API and flex tiers; strict JSON schema structured outputs; reasoning effort control.

## 3. Provider abstraction

- Wrap calls in **one internal client** (`llm.generate({feature, model, messages, schema, ...})`) that handles: retries with backoff, timeouts, fallbacks, logging of usage/cost, prompt version, caching headers, budget checks.
- Gateways/SDKs that unify providers: Vercel AI SDK (TS), LiteLLM (proxy/Python), OpenRouter, cloud gateways (Cloudflare AI Gateway, Azure API Management AI policies). Useful for fallbacks, caching, cost tracking — but structured-output and caching features differ per provider, so test each path.
- **Fallback provider/model** for outages; keep prompts portable (avoid provider-specific tricks unless worth it); evaluate the fallback too.

## 4. Open-weight and local models

- When: privacy/data residency requirements, very high steady volume, offline/edge, fine-tuning control.
- Serving: vLLM, SGLang, TGI for servers; Ollama/llama.cpp for local dev and small deployments.
- **Context truncation trap:** local runtimes may default to a small context window (e.g. Ollama's `num_ctx`) and silently truncate prompts — set it explicitly and verify.
- Quantization (4–8 bit) cuts memory/cost with some quality loss — evaluate.
- Total cost includes GPUs, ops, monitoring, upgrades; compare against API batch prices honestly.

## 5. Fine-tuning, distillation, adapters

- Order of attempts: better prompt + examples → retrieval → structured outputs/validation → fine-tuning.
- Fine-tune for **format/style/behavior consistency** or to make a small model do a narrow task well (distillation from a large model's outputs). Not for injecting frequently changing knowledge (use RAG).
- Needs: hundreds–thousands of high-quality examples, held-out eval set, retraining plan when base models change.
- LoRA/adapters for open-weight models; provider fine-tuning APIs for hosted models.

## 6. Versioning & upgrades

- Pin dated model versions in production; record model id per output.
- Upgrade process: run eval suite on new model → compare quality/cost/latency → canary on a slice of traffic → full rollout → keep rollback.
- Watch deprecation notices; schedule migrations.

## Sources

See BIBLIOGRAPHY.md (vendor documentation, guides and papers for this area).

See also: `diagnosis-playbook.md` Tree 7 (regression after a model change) and `playbooks.md` section 4 (model upgrades follow the prompt change protocol).

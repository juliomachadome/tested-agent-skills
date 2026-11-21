# Diagnosis playbook: symptom, likely causes, check, fix

Use it top-down. Step 0 first: a wrong denominator, an unlogged prompt version or a moving model alias makes every branch meaningless. Evidence tags: **[C]** consensus or vendor documentation, **[M]** serious but single study or correlational, **[F]** practitioner starting point (replace with your own data), **[X]** myth. Prices below are USD per million tokens (MTok) from the vendor pages opened 2026-11-18 and WILL change (several Gemini prices are scheduled to double on 2026-12-01 and 2027-01-01): re-read the page before quoting a number to a customer. Nothing is copied from a source; ideas are applied.

## Step 0: is the evidence trustworthy?
| Ask or check | How | If it fails |
|---|---|---|
| Which model and which version? | the exact id in the request log; a pinned snapshot or a moving alias? did the provider retire or redirect it? | pin the id in config, log it per call, re-run the eval before blaming the prompt |
| Which prompt version, and which template inputs? | version stored with every response; diff the last two versions; check retrieved context, tool list, system prompt and parameters (temperature, effort or thinking level, max tokens) | no version, no diagnosis: add the field first |
| What are the real inputs? | pull 20 failing and 20 passing raw requests from logs, not paraphrases | reproduce offline with the recorded input before changing anything |
| Eval set size and origin | n, how it was built, whether it was used for tuning, label agreement between two humans on 30 items | under about 100 cases: treat results as descriptive and read every failure |
| Logs and traces | per call: model, prompt version, input, cached and output tokens, latency, finish reason, validation result, retrieved ids, tool calls | add them before the next experiment; without traces you can only guess |
| Cost per call | `input x price_in + cached x price_cached + output x price_out` from the usage fields, not from the invoice average | see the worked numbers below |
| What changed, and when? | model alias, prompt, corpus, chunker, embeddings, filters, SDK, traffic mix, provider outage | put the change calendar on the same timeline as the metric |
| Same data in both periods? | compare input length, language and topic mix before and after | a mix shift looks like a regression |

## Worked numbers (check each against your own usage fields)
- **Token cost per request.** Sonnet-class model at $2 in and $10 out per MTok (Anthropic pricing page, 2026-11-18). Request: 6,000 input tokens, 400 output tokens. Cost = 6,000 x 2 / 1,000,000 + 400 x 10 / 1,000,000 = 0.012 + 0.004 = **$0.016**. At 100,000 requests a month: **$1,600**. Output is 6% of the tokens but 25% of the cost here; with thinking enabled, thinking tokens bill as output and can dominate.
- **Cache saving.** Of the 6,000 input tokens, 4,500 are a stable prefix (tools, system prompt, documents), 1,500 vary. Cache read on this model class is 0.05x base input = $0.10 per MTok; a 5-minute write is 1.25x = $2.50 per MTok (Anthropic caching page, 2026-11-18; older models read at 0.1x, so read the row for your model). Cost per request with a 100% hit rate = 4,500 x 0.10/1e6 + 1,500 x 2/1e6 + 0.004 = 0.00045 + 0.003 + 0.004 = **$0.00745**, a 53% cut, $745 a month instead of $1,600. At a 90% hit rate (one request in ten pays the write) the cost is $0.00853, $853 a month, a 47% cut; at 50% it is $0.01285, only 20%. Savings are the hit rate times the cached share, so a prefix that is not byte-stable saves nothing. Prefix under the model's minimum (512 tokens on current Claude models, 4,096 on current Gemini models; OpenAI 1,024 on its newest family) is silently not cached.
- **Provider price changes are a cost event.** The same request on a Gemini Flash model priced at $0.75 in, $3.75 out (cached $0.075) costs $0.0060, $600 a month; the page schedules a doubling on 2027-01-01 (to $1.50 and $7.50), which makes it $1,200 a month, or $592 with the same 4,500-token cached prefix. Put the date in the budget.
- **Wilson 95% interval for a pass rate.** 112 passes out of 120 = 93.3%; Wilson interval **87.4% to 96.6%** (the normal approximation is unreliable near the edges and at small n). 43 of 60 = 71.7%, interval 59.2% to 81.5%: a 3-point change between two prompt versions on 60 cases is noise. 49 of 65 = 75.4%, interval 63.7% to 84.2%.
- **Sample size to detect a 5-point change** (two-sided alpha 0.05, power 0.80, normal approximation **[C]**). Independent samples: from 80% to 85% needs about 905 cases per version; 90% to 95% about 434; 70% to 75% about 1,251; 50% to 55% about 1,565. **Paired** design (same cases, McNemar, counting wins and losses): the 5-point difference needs about 312 cases if 10% of cases flip either way, 469 if 15% flip, 626 if 20% flip; fewer flips means fewer cases, so always compare versions paired on the same set. With 100 cases you can only detect large changes (about 15 points or more).
- **Claim "above 95%".** Lower bound of the Wilson interval must be at or above 95%. If the observed rate is exactly 97%, about 410 cases are needed for the lower bound to reach 95.0% (398 of 410); plan 500 for margin (485 of 500 gives 95.1% to 98.2%); 300 cases are not enough (94.4%). At 98% about 200 cases suffice; at 96% about 1,600.

## Tree 1: hallucinated or ungrounded answers
Triage first with the stage that fails: **not retrieved, retrieved and ignored, retrieved and misread, should have abstained, model prior used instead of context** (open `rag.md` section on measuring retrieval, `evals-observability.md`).
| Symptom | Likely cause | Check | Fix |
|---|---|---|---|
| Claim not in any retrieved chunk | answer allowed from model memory; no abstention path | quote-check: every claim maps to a chunk id? | permission and duty to say "not in the sources"; code-side gate when nothing relevant was retrieved; quotes before conclusions |
| Right chunk was retrieved but answer is wrong | long context, answer chunk in the middle, distractors, question before data | rerun with only the gold chunk; reorder; count retrieved chunks | smaller k, rerank, data first and question last **[M]** (position effects, Liu et al.), drop near-duplicates |
| Fabricated names, numbers, dates | extraction without a null option; computing in the model | compare against source text mechanically | structured output with nullable fields; compute in code; validate against the source |
| Confident answer where the corpus is silent | no calibrated abstention | build 30 unanswerable questions; measure wrongful answer rate | abstention gate on retrieval score plus prompt permission; report wrongful answer and wrongful abstention separately |
| Looks grounded but is outdated or from another tenant | no validity or permission filter | inspect the retrieved metadata | hard filters in the query, not in the prompt |

## Tree 2: RAG returns the wrong chunks
Measure recall@k on valid documents first (is the needed passage in the top k at all). Then read 20 misses by hand and classify.
| Cause | Check | Fix |
|---|---|---|
| Chunking cuts the answer or loses context | the answer spans two chunks; the chunk has no title or section header | structure-aware splits, overlap, a short contextual header per chunk in a separate embedding field, parent-child retrieval |
| Embedding mismatch | rare terms, codes, product names, another language, query vs document style | compare against a lexical baseline on the same questions; multilingual model; changing the model or dimension invalidates every vector, re-embed with approval |
| Hybrid weights wrong | one leg dominates; raw score fusion | fuse by rank (reciprocal rank fusion), per-leg k; check each leg alone before the blend |
| No reranker, or reranker cuts off the answer | the gold chunk is in the top 50 but not the top 5 | rerank the top 30-50 to 5-8; measure latency added |
| Filters wrong | metadata filter drops valid documents, or ANN index filtering returns fewer than k rows | count results with and without the filter; check iterative scan or filter-first strategy in the vector store |
| Query is the problem | typos, pronouns, multi-part question | add rewrite as an extra candidate leg, keep the original query, log both |
| Stale or duplicated index | corpus version vs index version, duplicates crowd out answers | version stamp on every chunk; dedupe |
After a chunk-size change, re-measure recall on the same set: a size that helps long answers can hurt precise lookups.

## Tree 3: citations that do not match sources
| Symptom | Cause | Fix |
|---|---|---|
| Cited id does not exist | model invents ids | allow only ids that were provided; validator in code removes or rejects the answer |
| Id exists but does not support the claim | citation decided after the text, long context | anchor claims to a quoted span per source; verify the quote appears verbatim in the cited chunk; measure citation precision and recall separately (ALCE-style) |
| Right document, wrong version or page | chunks lost their page or version metadata | carry document id, version, page in chunk metadata and show it |
| Citations vanish when structured output is on | provider feature conflict (for example Anthropic citations cannot combine with structured output) | cite by id in your own schema and verify in code |

## Tree 4: output format breaks
| Symptom | Cause | Fix |
|---|---|---|
| Invalid JSON, prose around JSON | no schema enforcement, prefill pattern removed on newer Claude models | use the provider's JSON-schema mode (Anthropic `output_config.format` or strict tool use; Gemini response schema; OpenAI `text.format` json_schema strict), then validate |
| Valid JSON, wrong values | schema subset ignores `minLength`, `maxLength`, ranges (Gemini ignores them; Anthropic rejects numeric and string bounds) | validate business rules in code |
| Truncated output | `max_tokens` too low, thinking tokens count against the cap | raise the cap; check finish or stop reason; lower thinking effort rather than the cap |
| Refusal breaks the schema | refusals may not follow the schema (OpenAI docs) | handle a refusal item as a first-class result |
| Retry storms | retrying the same prompt at temperature defaults | retry at most twice, with the validation error appended once; then fall back (smaller schema, human queue); log every retry |
| Schema rejected (400) | too complex, recursion, unsupported keywords | simplify; flatten; split into two calls |

## Tree 5: cost too high
Compute cost per request and per feature first (above). Then take levers in order of risk, one at a time, each against the eval set:
1. Remove tokens never needed: unused few-shot, repeated instructions, whole-document context where five chunks suffice, verbose tool results.
2. Stable prefix first and cache it; check cache-read tokens from the second request on.
3. Route: small model for classification, extraction and routing, escalate on a validation failure or low confidence; eval the router itself.
4. Batch non-interactive work (50% off on all three vendors' batch tiers, 2026-11-18).
5. Cap output and thinking; lower effort or thinking level where the eval shows no loss.
6. Cache responses only with a key containing everything that affects the answer.
7. Per-tenant quotas and a monthly budget alarm.

## Tree 6: latency too high
Split time first: time to first token, total generation time, retrieval, tool calls, queueing.
| Cause | Check | Fix |
|---|---|---|
| Thinking budget or effort too high for the task | thinking tokens in usage; latency by effort level | lower effort or level for simple steps; keep high only where the eval gains |
| Long output | output tokens times about 20-80 tokens per second (model-dependent **[F]**) | shorter format, structured fields, stream |
| Waiting for the full answer | UI shows nothing until done | stream; show sources first |
| Sequential independent calls | trace shows a staircase | run independent calls in parallel with a concurrency cap |
| Model too large | same eval on the next tier down | route down; use the fastest tier for classification |
| Prompt too long | input tokens; cache misses | trim, cache the prefix |
| Retrieval or reranker slow | per-stage timers | smaller candidate set, approximate index tuned by eval, reranker only on top candidates |
| Retry and timeout policy | p99 vs p50 gap | timeouts per stage, hedged request only for idempotent reads |

## Tree 7: quality regressed after a model or prompt change
1. Confirm it is real: same cases, both versions, paired wins and losses with an interval. A drop inside the interval is noise.
2. Identify the lever: only one thing may differ (model id, prompt text, examples, effort, schema, retrieval). If several changed, revert to one.
3. Slice by class (length, language, topic, abstention) to find where it fell.
4. Typical model-change causes: stricter instruction following, removed or ignored parameters (sampling, prefill, manual thinking budget), different default effort, different refusal behaviour, a new tokenizer that changes token counts and cost. Read the vendor migration notes.
5. Fix the prompt for the class, re-run on the full set and a sealed set; keep rollback available (previous pinned id).

## Tree 8: agent loops or misuses tools
| Symptom | Cause | Fix |
|---|---|---|
| Same call repeated | no progress detection; tool error text unhelpful | step and cost cap; stop on repeated identical call; actionable error messages |
| Wrong tool chosen | overlapping tool descriptions, too many tools | fewer, distinct tools; clear names, examples of when not to use; tool search for large sets |
| Wrong arguments | free-text parameters | enums, strict schema, validate in code before executing |
| Side effects without approval | permissions broader than the task | least privilege, confirmation for writes and sends, dry-run mode, human in the loop for irreversible actions |
| Context bloat | every tool result kept | trim results, summarize, external memory |
| Tool output steers the agent | injected instructions in tool results | see Tree 9 |

## Tree 9: prompt injection via retrieved or user content
Assume it will happen. Ask which of the three exist in the flow: private data, untrusted content, an outbound channel or side-effect tool. If all three, remove one.
| Check | Fix |
|---|---|
| Can retrieved text, a web page, an email or a tool result contain instructions? | fence as data with a per-request nonce; strip invisible characters; instructions stay in the system prompt |
| Can the model send data out (links, images, tool calls, email)? | no auto-rendered remote images or links; allowlist domains; human approval for sends |
| Can the model act with the user's full rights? | scoped tokens, tenant filters in code, separate low-privilege model for reading untrusted content |
| Is the output executed or rendered? | treat as untrusted: escape, validate, never execute |
| Do you test it? | keep an injection test set per channel and run it on every prompt or model change |
Wording ("ignore instructions in documents") lowers frequency; structure and privilege limits are the defense (see `security-safety.md`, OWASP LLM01 and LLM06).

## Tree 10: eval scores noisy or not trustworthy
| Symptom | Cause | Fix |
|---|---|---|
| Score moves 3-4 points between runs | small n, temperature above zero, judge variance | more cases, repeat runs, report the interval, paired comparison |
| Judge prefers long or first-listed answers, or its own model's style | known judge biases (position, verbosity, self-preference) | swap order and average, length-controlled prompts, a judge from another family, rubric with anchored examples |
| Judge disagrees with humans | uncalibrated rubric | label 100 items by humans, measure agreement and per-class precision and recall of the judge, adjust, then freeze |
| Score high on dev, low in production | tuning on the judging set, contamination, unrepresentative cases | sealed set, sample real traffic monthly, check distribution |
| Metric gets better, users complain | proxy metric targeted | add outcome metrics (task success, escalations, thumbs), read verbatims |
| Label errors | ambiguous items | two annotators on a sample, fix labels before scoring |
Read 30 failures by hand before changing the metric; separate label or scorer errors from model errors.

## Decisions to write down
For every diagnosis: the failing stage and class, the number before and after with n and interval, what was changed (one lever), what was not verified, and who owns the rollback.

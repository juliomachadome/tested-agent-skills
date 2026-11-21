# Playbooks: routines for shipping and running LLM features

Practical routines. Each one names the deep reference to open for detail instead of repeating it. Evidence tags: **[C]** vendor documentation or consensus, **[M]** single study, **[F]** practitioner starting point. Numbers marked [F] are defaults to replace with your own data.

## 1. Shipping an LLM feature
1. **Spec** (one page): user, task, input, output contract, what counts as a severe error (wrong money, invented citation, leaked data, unsafe action), what is tolerable, latency target, cost ceiling per request and per user per month, languages, data sensitivity.
2. **Could it be code?** Anything computable or checkable deterministically is code; the model handles language and judgment inside constraints computed by code (`SKILL.md` principle 1).
3. **Eval set first**: 50 real or realistic cases to start, grow to 200-300 before launch; include abstention cases, hostile inputs, long inputs, each language. Freeze a sealed part nobody tunes on (playbook 2).
4. **Baseline**: the simplest version (one call, small model, no retrieval) scored on the set. Every later rung must beat it on quality, cost or latency.
5. **Prompt and schema**: stable prefix first, rules with reasons, closed enums, nullable fields, evidence before conclusion, 3-5 varied examples (`prompting-context.md`).
6. **Guardrails**: schema plus business validation in code, abstention gate in code, permission and tenant filters in the query, output escaping, rate limits and per-tenant quota, timeouts and a fallback for 429, 5xx and refusal (`security-safety.md`).
7. **Pre-launch gate**: quality at or above the bar with the interval's lower bound, severe-error count zero on the sealed set, injection set passes, cost per request within budget at expected volume, rollback tested.
8. **Monitoring**: log model id, prompt version, tokens (input, cached, output, thinking), latency, finish reason, validation result, retrieved ids; dashboards for cost per day, p50 and p95 latency, validation failure rate, abstention rate, cache-hit rate; sample 20-50 real outputs a week for human review; alarms on spend and on error spikes (`evals-observability.md`).
9. **Rollout**: internal, then 5% of traffic, then 25%, then all, each step with a stop rule written beforehand (for example validation failures above 2% or cost per request 30% over estimate [F]).
Done when: the spec, the set, the baseline numbers and the stop rules are in the repo.

## 2. Building an eval set and an LLM-as-judge with calibration
**Eval set**
1. Collect cases from real logs, support tickets and domain experts; stratify by class (topic, length, language, difficulty) and include 15-25% abstention or adversarial cases [F].
2. Write the expected result as checkable facts (required sources, required fields, forbidden claims) rather than one gold paragraph wherever possible.
3. Two people label 30-50 items; resolve disagreements; write the labelling rules down. Agreement low means the task is ambiguous, not that the model is weak.
4. Split: **tuning** set (you may read failures), **dev** set (for comparisons), **sealed** set (frozen by hash, opened once per milestone, built by someone who does not tune). Anything read while fixing is tuning data.
5. Size from the claim you need: see the sample-size numbers in `diagnosis-playbook.md`; 300-500 cases to see a 5-point change on paired runs, about 1,000 per arm on independent runs.
6. Deterministic checks first (schema, citations exist, numbers match source); the judge only for what code cannot decide.

**Judge with calibration** (method after the MT-Bench study by Zheng et al., which documents position, verbosity and self-preference biases **[M]**)
1. Write a rubric with one question per criterion and 2-3 anchored examples per score; binary or 3-level scores beat 10-point scales [F].
2. Ask for the reasoning or evidence before the verdict; temperature at the provider default or low.
3. Human-label 100+ items; run the judge; report agreement, and per-class precision and recall of the judge against humans, with Wilson intervals.
4. Neutralize bias: randomize and swap answer order, control length, use a different model family from the one being judged.
5. Freeze judge model id, prompt and rubric; a judge change is a new metric, so re-run baselines.
6. Recalibrate monthly on 30 fresh human labels; alarm if agreement drops.
7. Never gate a release on a judge alone when a deterministic check exists.

## 3. RAG pipeline build and tuning loop (`rag.md`)
1. **Corpus**: parse faithfully (tables, headings, page numbers), dedupe, stamp document id, version, validity dates, tenant and permission metadata.
2. **Chunk**: structure-aware, start at 300-800 tokens with 10-15% overlap [F], keep a short contextual header in a separate embedding field, keep the cited text verbatim.
3. **Index**: one lexical leg and one vector leg; hard filters in the query; record embedding model and dimension per row.
4. **Retrieve**: fuse by rank (reciprocal rank fusion), take 30-50 candidates, rerank to 5-8, abstain when scores are below a calibrated threshold.
5. **Generate**: data first, question last, quotes before the answer, cite by provided ids only, code validates citations.
6. **Measure per stage** on the dev set: recall@k on valid documents, answer faithfulness given perfect context, citation precision and recall, abstention both ways, cost and p95 latency.
7. **Tuning loop**: read 20 failures, classify (not retrieved, retrieved and ignored, cited wrong, should have abstained), pick the largest class, write one general hypothesis, change one lever, re-run paired, accept only with wins and no losses in other classes, then confirm once on the sealed set.
8. **Operate**: re-index on corpus change, monitor retrieval-score drift and abstention rate, re-evaluate when the model or embeddings change.

## 4. Prompt change protocol
1. **Version**: prompts live in files with a version string (`name/YYYY-MM-DD.n`), stored with every response; fixtures keyed by hash renamed with the change.
2. **Hypothesis in one sentence** plus the metric that would confirm it and the threshold that would reject it, written before running.
3. **One lever** per change (wording, examples, schema, effort, model, retrieval).
4. **Offline A/B on the eval set**: same cases, both versions, paired wins and losses with McNemar or a paired bootstrap, intervals, cost and p95 latency, per-class slice, injection set.
5. **Decision by someone other than the author** (`rag-eval-engineer` role); ship only if it beats the bar with no severe-error regression.
6. **Rollout**: shadow or 5% canary, compare live metrics (validation failures, abstention rate, thumbs, escalations, cost), step up, keep the previous version one flag away.
7. **Record**: change log entry with the numbers; delete rules that never changed a result.
Model upgrades follow the same protocol with a pinned id on both sides; read the vendor migration notes first (removed parameters, tokenizer changes, new defaults).

## 5. Cost and latency optimisation pass (`cost-latency.md`)
1. Instrument: cost and latency per feature, per step, per tenant; p50, p95, p99.
2. Rank steps by monthly cost (tokens x calls x price) and by contribution to p95.
3. Apply levers in risk order, one at a time, each on the eval set: trim context, cache the stable prefix, shorten outputs, lower thinking effort, route to a smaller model, batch background work, parallelize independent calls, stream.
4. Re-price with the vendor page dated today (batch tiers 50% off, cache reads at a fraction of input, scheduled price changes).
5. Report before and after: quality with interval, cost per request, cost per active user per month, p95.
6. Set alarms: daily spend, tokens per request, cache-hit rate, retries.
Stop when the next lever costs more engineering time than it saves per month.

## 6. Agent and tool design checklist (`agents-tools.md`, `security-safety.md`)
- [ ] Is a workflow (fixed steps) enough? Only add autonomy when an eval shows the workflow fails.
- [ ] Each tool: one purpose, a name and description that say when not to use it, closed enums, strict schema, validation in code.
- [ ] **Least privilege**: scoped credentials per tool and per user; read tools separate from write tools; no shell or arbitrary URL fetch unless sandboxed; tenant filters in code.
- [ ] **Confirmations** for irreversible or external effects (send, pay, delete, publish); show the exact action and arguments to the human; dry-run first.
- [ ] **Human in the loop** for high-stakes decisions: the model proposes, a person or deterministic rule decides.
- [ ] Untrusted content (web, email, files, tool output) never reaches a context that has both private data and an outbound channel.
- [ ] Limits: max steps, max tokens, max cost per run, timeout, loop detection, kill switch.
- [ ] Observability: every tool call logged with arguments, result size, latency, approval; traces replayable.
- [ ] Error messages written for the model: what failed, what to try next.
- [ ] An eval suite of tasks with checkable end states, plus an injection set, run on every prompt, tool or model change.

## 7. Incident response for a bad model output in production
1. **Triage (first 15 minutes)**: what was shown, to how many, severity (harm, legal, money, privacy, reputation). Name an incident owner.
2. **Contain**: switch the feature to a safe mode (feature flag off, abstain-only, or the previous prompt or model id), pause outbound actions, block the offending input pattern; do not wait for the root cause.
3. **Preserve evidence**: request id, model id, prompt version, full input, retrieved ids, output, tool calls, timestamps; restrict access if personal data is involved.
4. **Notify** per your policy and law (data protection authorities and affected users have deadlines when personal data leaked; ask legal) and tell support what to say.
5. **Diagnose** with `diagnosis-playbook.md`: Step 0, then the matching tree; reproduce offline.
6. **Fix at the right layer**: a code guard or filter first, prompt second, model third; add the case and its twins to the eval and injection sets.
7. **Verify and re-enable** through the prompt change protocol with a canary and the new cases.
8. **Review without blame** within a week: timeline, detection gap, what check would have caught it, owners and dates for actions. Keep the incident in the red-flags list (`red-flags-audit.md`).

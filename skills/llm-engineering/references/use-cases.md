# Use-Case Recipes

Each recipe: architecture → cost levers → quality levers → pitfalls → evals. Combine recipes for real products.

## 1. Personalized plan generation with constraints (schedules, itineraries, learning plans, training or meal plans)

**Architecture (workflow graph, not free agent):**
1. Code loads the user's profile, goals, history, progress and restrictions (time, budget, preferences, hard exclusions).
2. Code computes **targets and constraints**: quantities per category, frequency, duration, numeric targets, progression from history.
3. Code pre-filters the **catalog** to valid candidates (available, allowed, matching preferences) and passes ids + compact attributes.
4. LLM **selects and arranges** from candidates (structured output: ids, quantities, order, short rationale) — it never invents catalog items.
5. Validator checks constraints (ids exist, totals within ranges, no excluded items, balanced distribution); repair loop with errors (max 2); fallback to a template.
6. Code computes totals and renders; LLM output stores only decisions.

**Cost levers:** generate per block/week on demand, not months ahead; reuse plan templates per profile bucket and let the LLM only adapt; patch operations ("swap this item") with a small model instead of regeneration; cache-friendly prompt (rules + catalog schema first); batch nightly regeneration; small model for adaptations, larger model only for first plan or complex cases.

**Quality levers:** few-shot with good plans; explicit progression rules in code; feedback loop from progress (what was actually done) → next block; let the objective be measurable in data ("distance to goal") and computed by code.

**Item substitution ("I don't have X, I have Y"):** deterministic first — attribute similarity from the catalog to rank substitutes and compute quantities that keep totals on target; LLM only parses free-text intent and explains. Cheap and correct.

**Pitfalls:** LLM computing totals; inventing catalog items; ignoring hard exclusions; huge prompts with the entire catalog; regenerating everything on each small change.

**Evals:** constraint pass rate, first-try validator pass rate, repair rate, judge score on coherence/variety, user edit/regeneration rate, adherence over time.

## 2. Grounded Q&A with citations (legal/regulatory, policies, manuals, knowledge bases)

**Architecture:** RAG with structure-aware chunking (act → section → subsection → clause), metadata (jurisdiction, norm number, dates, in-force status, amendments), hybrid search + rerank, temporal filter (in force at the question date), answer with per-claim citations, citation verification in code, abstention.

**Output schema:** `answer`, `claims[] {text, source_ids[]}`, `risk_level` (enum, if analysis), `missing_information`, `confidence` (enum), `abstained` (bool).

**Cost levers:** small/mid model is often enough when retrieval is good; cache frequent queries per corpus version; rerank to send fewer chunks.

**Quality levers:** quote-first extraction; legal hierarchy rules in code (national/regional/local precedence, bylaws); in-force checks; graph of amendments/revocations for multi-hop.

**Pitfalls:** citing revoked norms; mixing jurisdictions or tenants (filters); answering without sources; paraphrasing law loosely.

**Evals:** recall@k on labeled questions; citation accuracy; abstention accuracy; expert review sample.

## 3. Long audio → transcript → structured minutes (meetings, sessions, calls)

**Architecture:**
1. STT with **diarization** and timestamps (dedicated speech model); custom vocabulary/glossary for names and terms.
2. Speaker identification: map diarized speakers to people using a roster + LLM on context cues + human confirmation.
3. Clean transcript in segments (punctuation, fillers) — small model, parallel by segment.
4. **Map–reduce summarization** into the minutes template (agenda items, speeches summary, votes, results) — structured output per section; vote counts and results extracted and checked by code.
5. Human review UI with links from each minutes sentence to transcript timestamps; approval/sign-off.

**Cost levers:** STT is often the main cost — choose model by accuracy/price on your audio; avoid sending raw audio to an LLM when text suffices; segment-level small models; only the final assembly with a larger model; batch processing (not real-time) unless needed.

**Pitfalls:** misattributed speakers; invented vote results; losing context across chunk boundaries (overlap + running summary).

**Evals:** WER on samples; speaker attribution accuracy; checklist coverage of key events; factual consistency judged against transcript.

## 4. Document extraction (contracts, invoices, forms, bids)

**Architecture:** parse → locate relevant sections (rules/keywords/retrieval) → structured extraction with nullable fields and evidence quotes (`value`, `quote`, `page`) → code validation (dates, totals, tax-id formats, cross-field consistency) → human review queue for low confidence.

**Findings/audits (e.g. compliance reviews):** each finding has `evidence[]` with quotes and an `evidence_grade` enum; no finding without evidence; neutral language.

**Cost levers:** extract from relevant pages only; small model + validation; batch.

**Evals:** field-level precision/recall; null correctness; evidence quote match rate.

## 5. Classification / triage / risk scoring

**Architecture:** enums with definitions; few-shot per class including borderline cases; low temperature; optional self-consistency (3 votes) for high stakes; calibrated thresholds; route uncertain cases to humans.

**Cost levers:** smallest model; or embeddings + classic classifier (logistic regression) trained on labeled data — far cheaper at volume; LLM only for low-confidence cases.

**Evals:** confusion matrix; per-class recall for critical classes (missing a "high risk" is worse than a false alarm).

## 6. Conversational assistant with memory

**Architecture:** intent router → (FAQ/cached answers | RAG | tools on user data | small talk with small model); rolling window + summary; profile facts from DB; tool calls for user data; guardrails per domain.

**Cost levers:** route simple turns to small models; cache-friendly system prompt; summarize history; limit turns per day on low-price plans.

**Evals:** task success on scripted conversations; groundedness; safety cases.

## 7. Semantic search & recommendations

**Architecture:** embeddings + hybrid search + filters + rerank; LLM optional for query understanding or explanation ("why this result").

**Cost levers:** no generation needed for most searches; cache embeddings of frequent queries.

## 8. Text-to-SQL / analytics over own data

**Architecture:** curated semantic layer (views with clear names/descriptions), read-only role, row-level security/tenant filter enforced by DB, query allow-list (SELECT only), timeout and row limits, explain-before-run, results summarized by LLM with numbers computed by SQL.

**Pitfalls:** direct access to raw schema; cross-tenant leaks; expensive queries.

**Evals:** execution accuracy against expected results on a question set.

## 9. Content generation & marketing copy

**Architecture:** brand/style guide in cached system prompt; structured brief input; generate N variants with a small/mid model; judge or rules for compliance (claims, forbidden words); human selection.

## 10. Translation / localization

Glossary of fixed terms; preserve placeholders/markup (validate); small model; batch; human review for legal/marketing text.

## 11. Voice agents

Streaming STT → LLM (small, fast) → streaming TTS; latency budget per turn (< ~1 s to first audio); barge-in handling; tools with fast responses; summaries after the call.

## 12. Moderation & safety filters

Provider moderation endpoints or small classifiers first; LLM review only for borderline cases; log decisions; appeal path.

## 13. Coding/automation agents inside a product

Sandboxed execution, allow-listed tools, diffs shown for approval, step/cost caps, trace logging.

## 14. Choosing the recipe

Ask: Is the answer computable? (code) → Does it need external knowledge? (RAG/graph) → Does it need actions/data access? (tools) → Are steps known? (workflow) → Are steps unknown? (agent with caps). Then size the model by evals and design cost per user to fit pricing.

## Sources

See BIBLIOGRAPHY.md (vendor documentation, guides and papers for this area).

See also: `variants/README.md` (choose the variant by feature type), `playbooks.md` (shipping routine).

# Variant: classification, triage and structured extraction

Use for: labelling tickets, routing, risk scores, moderation, pulling fields from invoices, contracts, forms or emails into a schema.

## Architecture choice
- Try rules and a classical model first if labels are stable and data is plentiful; use an LLM when input is messy language, labels change often or training data is thin.
- A single call with a JSON schema and the smallest model tier that passes the eval; escalate low-confidence or invalid cases to a larger model or a human queue (router or cascade).
- The model proposes; code decides anything with consequences (approval, legal class, money). Compute totals, dates and checksums in code and compare with what the model extracted.
- Provider structured output modes: Anthropic `output_config.format` or strict tool use, Gemini response schema, OpenAI `text.format` json_schema strict; each supports a subset of JSON Schema, so validate the rest in code. See `../prompting-context.md`.

## Prompt pattern
Label definitions with one boundary example per confusable pair; 3-5 varied examples in exactly the output format, including "none of the above" and an unreadable input; every field nullable with an explicit `unknown` or `not_present` value so the model never has to invent; evidence field (quote or span) before the label. For long documents put the document first and the instructions last.

## Eval metrics
- Per-class precision and recall and a confusion matrix, not only accuracy (a 95% accuracy on 95% majority class is a baseline).
- Field-level exact match and normalised match for extraction; "unknown" correctness.
- Wilson interval for every rate; to claim "above 95%" the lower bound must reach 95% (about 410-500 cases at an observed 97%; see `../diagnosis-playbook.md`).
- Calibration of confidence (if you use it to route), cost per 1,000 items, p95 latency.
- Paired comparison between prompt or model versions on the same items.

## Failure modes
Silent wrong label on an ambiguous item; label drift after a prompt or model change; schema constraints the provider ignores (lengths, ranges); hallucinated field values when the document lacks them; position or order bias in few-shot examples; class imbalance hiding rare but costly errors; injected text inside the document that steers the label.

## Cost notes
Cheapest tier first; cache the instructions and examples (large static prefix, tiny variable part); batch tiers (50% off, 2026-11-18, all three vendors) for backfills and nightly runs; short outputs by using enums and compact fields; skip the model for items rules can settle.

## Checklist
- [ ] Label guide written; two people agreed on a sample.
- [ ] Per-class metrics and a rare-class subset in the eval set.
- [ ] Nullable fields, `unknown` values, evidence before label.
- [ ] Schema and business-rule validation in code; invalid goes to repair once, then fallback.
- [ ] Human queue for low confidence; sample audit of confident labels.
- [ ] Prompt version and model id stored with every label.
- [ ] Injection case in the set.

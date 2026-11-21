# Variant: summarisation, rewriting and content generation

Use for: meeting minutes, document summaries, translation and localisation, email or marketing drafts, personalised plans, report writing.

## Architecture choice
- Short input: one call. Long input: map-reduce (summarise parts, then merge) or a single call on a long-context model when the whole document fits; compare both on the eval, since long inputs cost more per call and quality can vary with position.
- Transcripts and audio: transcribe first (`../speech-asr.md`), then summarise the text.
- Generation with hard constraints (dates, totals, quotas, allowed items): the code builds the constraints and verifies the result; the model only writes language inside them (`../use-cases.md` section 1).
- Human review before publishing anything customer-facing or legally relevant.

## Prompt pattern
State the audience, purpose, length and structure; provide the source in a fenced block, source first and instructions last for long inputs; require every claim to come from the source (extract quotes or key facts first, then write); ask for a fixed structure (sections or fields); give one good and one bad example of tone; put brand voice and forbidden claims in the system prompt. For translation give the glossary and a do-not-translate list.

## Eval metrics
- Faithfulness to the source: unsupported claims per summary (checked by sampling, or a calibrated judge on claim-level checks); omissions of must-keep facts (a checklist per document).
- Rubric scores for structure, tone, length with anchored examples; pairwise preference between versions with order swapped (judge biases are documented in the MT-Bench study).
- Deterministic checks: length limits, required sections, numbers and names present in the source, forbidden terms.
- Human acceptance rate (accepted without edits), edit distance, time saved.

## Failure modes
Invented facts or numbers; dropped negations and conditions; wrong speaker or attribution; merging two entities; over-confident tone where the source hedges; style drift from the brand; truncation by an output cap (thinking tokens count against it); translating names or codes that must stay; mid-document content lost in very long inputs.

## Cost notes
Cost scales with input length: summarise once and store the result; use a small model for the map step and a stronger one for the final merge; batch tiers for back-catalogue jobs (50% off, 2026-11-18); cache the instructions and style guide; cap output tokens; do not regenerate when only a small edit was requested (patch the output). Worked arithmetic: `../diagnosis-playbook.md`.

## Checklist
- [ ] Source-faithfulness rule and a sample audit each week.
- [ ] Must-keep facts list per document type.
- [ ] Constraints computed and verified in code.
- [ ] Glossary and do-not-translate list for localisation.
- [ ] Human approval step before publishing.
- [ ] Personal data in sources handled per policy; provider retention checked.
- [ ] Prompt and model versions stored with each output.

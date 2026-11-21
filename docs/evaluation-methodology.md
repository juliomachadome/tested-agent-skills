# Evaluation methodology

## What the historical results measure

The historical records compare a response produced with one skill against a response produced without repository skills for the same task. A blind judge sees the alternatives in both orders to reduce position bias. A win is recorded only when the judging process selects the skill-assisted response under its recorded rule; a tie is not treated as improvement.

Separate trigger checks ask whether a skill is selected when it should be and stays inactive when it should not. The aggregate report calls a trigger record **strong** only when it has at least four correct triggers, zero false triggers and three runs. Other recorded trigger tests are **limited**; an entry without a trigger record is **pending**.

See [Evaluation evidence](evaluation-summary.md) for the current aggregate counts.

## What the results do not measure

- They are historical Claude-based records, not a result for all models, providers or harnesses.
- The sample is small for some skills and does not establish statistical generalization.
- A blind judge is useful but not independent replication and can still be wrong or biased.
- The records do not prove tool safety, legal compliance, model reliability, or quality on an unseen production task.
- A portable `SKILL.md` does not imply equal discovery or behavior in another harness.

## Public and private split

| Public material | Private material |
| --- | --- |
| Aggregate counts, methodology, synthetic fixtures, fixture schemas, compatibility rules and redacted per-run metadata | Blind holdouts, full model responses, raw session traces, internal notes, costs, local configuration and connector details |

The private holdout helps avoid tuning a skill to public cases. It is not published because publishing it would weaken that check and would expose more operational detail than a public benchmark needs. Anyone can create an independent comparison with their own lawful, non-sensitive fixtures and report it using the fields in [Compatibility](compatibility.md#reporting-a-new-result).

## Reproducing public checks

Public fixtures are intentionally synthetic. They provide a shared smoke-test shape, not the exact historical benchmark. Run only with data you are permitted to send to the selected model provider, and record the exact model and harness.

The historical Claude runner is not included in the public release. The included Codex adapter prepares an ephemeral, read-only session and ignores normal user configuration. Its default is a dry run:

```bash
python3 scripts/codex-skill-eval.py --fixture evals/public/codex-smoke.json
```

Adding `--live` makes a model call and can incur provider charges. A successful process exit confirms execution only; the adapter does not score answer quality or prove that the skill was read.

## Decision rule for future claims

State a model/harness result only after a saved artifact exists for that exact pair. Label its fixture type and date. Do not collapse individual harness results into one cross-model score. Negative, tied and pending results remain visible.

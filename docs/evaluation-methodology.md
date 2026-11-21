# Evaluation methodology

## What the historical results measure

The historical records compare one answer with the target skill against an answer to the same task without repository skills. A blind judge sees the alternatives in both orders to reduce position bias.

### Comparison classification

For the main holdout protocol, each skill started with two tasks and one paired comparison per task. Two wins or two losses ended the comparison early. Other results led to two more comparisons per task, for six paired judgments in total. The judge had to agree across both orders. A second Claude judge adjudicated disagreements in that protocol. An unresolved pair counted as a tie.

The main holdout counted a skill as a win when its pairs contained more wins than losses. Equal counts were a tie. The public totals include 25 main holdout outcomes, 7 reused outcomes from an earlier holdout, and 1 outcome from a separate pilot. Those earlier runs had different procedures, so the README and catalog call the combined counts historical wins and ties.

The shorter `web-motion` check is counted separately as a limited comparison. The `redigir` command is outside this comparison protocol.

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

## Measuring what a skill adds to a short brief

Write the first prompt as someone outside the specialty might: give the goal, known facts and real constraints in ordinary language. Supply enough context to make the task feasible. Leave domain decisions and acceptance checks out of the prompt when those are the behaviours the skill is expected to add. Include both simple and complex tasks with short briefs when possible. A short brief can describe a complex outcome, such as cutting through an interactive 3D object to reveal its layers.

Define the scoring criteria before running the test and keep them outside the generation prompt. Compare independent sessions using the same prompt, model, files and tools. Give only one condition the target skill. Where possible, check the resulting artefact directly, such as by counting 3D requests before a visitor interacts. Use a separate discovery test if the skill text was supplied explicitly.

A detailed brief can also be useful as a control. Run both conditions again with the same details and checks. Report short- and detailed-brief results separately so readers can see which decisions the request supplied and which the skill helped surface.

## Decision rule for future claims

State a model/harness result only after a saved artifact exists for that exact pair. Label its fixture type and date. Do not collapse individual harness results into one cross-model score. Negative, tied and pending results remain visible.

# Evals & Observability

Contents: 1 Eval-driven development · 2 Metrics by task · 3 Non-determinism · 4 Online evaluation · 5 Tracing · 6 Tooling · 7 Starter · 8 Metric per stage · 9 Intervals and sample size · 10 Paired comparison · 11 Sealed sets · 12 Calibrated abstention · 13 Fix by error class · 14 Judge calibration · 15 A/B exit criteria · 16 Gaming defenses · 17 OpenTelemetry GenAI tracing · 18 Eval as a CI gate

## 1. Eval-driven development

1. **Collect real cases** (20–50 per feature to start; grow to hundreds): typical, edge, adversarial, and past failures. Anonymize.
2. **Define what "good" means** per feature as checkable properties, not vibes: valid schema, constraints satisfied, facts supported by sources, correct classification, tone/language, length.
3. **Graders**, cheapest and most reliable first:
   - **Code graders:** schema validity, enums, ranges, constraint checks (calories within target, weekly volume, no forbidden exercises), citation ids exist, exact/regex match, JSON diff against expected.
   - **LLM-as-judge:** for subjective or semantic properties (faithfulness, helpfulness, clarity). Use a clear rubric, binary or small-scale scores per criterion, ask for the reason before the verdict, pairwise comparison (A vs B) for prompt/model choices. Calibrate against human labels on a sample; watch for position and length bias (swap orders).
   - **Human review:** sample for calibration and high-stakes outputs.
4. **Run on every change** (prompt, model, retrieval, chunking, temperature) → compare to baseline: quality metrics, cost, latency. Gate merges on no regression beyond a threshold.
5. **Error analysis:** read failures, cluster them into categories, fix the biggest category, repeat. This beats generic metrics.

## 2. Metrics by task

| Task | Metrics |
|---|---|
| Classification / triage | accuracy, precision/recall/F1 per class, confusion matrix, calibration |
| Extraction | field-level precision/recall, exact match per field, null correctness |
| RAG retrieval | recall@k, hit rate, MRR, nDCG, context precision |
| RAG answer | faithfulness/groundedness, answer relevance, citation accuracy, abstention accuracy |
| Generation with constraints | constraint pass rate, validator pass rate on first try, repair rate, judge score |
| Summarization / minutes | coverage of key points (checklist), factual consistency, speaker attribution accuracy |
| Agents | task success, steps, tool-call accuracy, cost per task, safety violations |
| Ops | cost per request/user, p95 latency, error rate, validation failure rate |

## 3. Non-determinism

- Run each case several times (or at temperature 0 where supported) and report pass rates, not single outcomes.
- Pin model versions (dated snapshots) in production; re-run evals before upgrading.

## 4. Online evaluation & monitoring

- Log every call with: feature, prompt version, model, tokens, latency, finish reason, validation result, retries, user feedback (thumbs, edits, regenerations).
- **Implicit signals:** user edits to generated content, regenerations, abandonment, substitutions requested, support tickets.
- Sample production traffic for offline judging; feed failures back into the eval set.
- A/B or shadow test new prompts/models on a slice of traffic with guardrail metrics.
- Alerts: spikes in validation failures, refusals, latency, cost per user, provider errors.

## 5. Tracing

- See section 17 for the OpenTelemetry GenAI conventions. Or use LLM observability platforms: Langfuse (open source), Arize Phoenix (open source), LangSmith, Braintrust, Helicone, Weights & Biases Weave.
- Trace multi-step flows end to end (retrieval → generation → validation → tools) with a run id.
- Redact PII/secrets in traces; set retention.

## 6. Tooling

- Eval runners: promptfoo (config-driven, CI-friendly), DeepEval, Ragas (RAG metrics), Inspect (UK AISI), OpenAI Evals, Braintrust, LangSmith evals, Vitest/pytest with custom graders.
- Keep eval datasets in the repo (or a versioned store), with expected properties and tags.
- Cost: run cheap code graders on every commit; full LLM-judge suites on PRs touching prompts/models or nightly; use batch APIs for big eval runs.

## 7. Practical starter (any feature)

```
evals/<feature>/cases.jsonl     # input, context, expected properties, tags
evals/<feature>/graders.ts      # code graders + judge rubric
evals/<feature>/run.ts          # runs current prompt/model, writes results + summary (pass rate, cost, p95)
```
Report: pass rate per grader, failures listed with inputs/outputs, tokens and cost per case, diff vs baseline.

## 8. Measure each pipeline stage separately

An end-to-end "wrong answer" hides where it broke. Split the pipeline and give each stage its own number:

| Stage | Question | Metric | Typical culprit when low |
|---|---|---|---|
| Retrieval (R) | Is every passage needed to answer inside the context actually delivered to the model? | recall@k of expected passages; "all expected present" rate per question; MRR/nDCG for rank-sensitive comparisons | chunking, embeddings, filters, query wording |
| Generation (C) | Given the needed passage is in context, does the model use and cite it correctly? | citation recall (claims fully supported by what they cite), citation precision (citations that are not irrelevant), faithfulness | prompt, model, too much noisy context |
| Abstention | Does it refuse when it must, and answer when it can? | correct abstention rate and wrong abstention rate, reported separately (section 12) | threshold, prompt, retrieval signal |
| Verification | Does the code validator catch what the model got wrong? | validator catch rate on seeded bad citations | validator gaps |

- Compute C **only on questions where R succeeded**; otherwise a retrieval miss is blamed on the model. The ceiling of end-to-end citation accuracy is roughly R x C, so fix the lower factor first.
- Define citation quality with two numbers, as ALCE does: citation recall (is each statement fully supported by the passages it cites) and citation precision (does each citation add support). One blended "citation correct" mixes "no source" with "wrong source".
- Report a failure table per run: not retrieved / retrieved but ignored / cited wrong / should have abstained / validator missed. Fix the largest bucket.
- Reference-free judge metrics (faithfulness, context relevance, answer relevance, as in RAGAS) scale cheaply but depend on the judge prompt and domain; use them to triage errors, not as the ship decision.

## 9. Confidence intervals and sample size

Every proportion reported needs `k/n` and an interval. A point estimate from a small set is a rumor.

- Use the **Wilson score interval** (or Jeffreys); avoid the Wald interval `p +/- 1.96*sqrt(p(1-p)/n)`, whose coverage is erratic for small n or p near 0 or 1.
  - Wilson, z = 1.96: centre `(p + z^2/2n) / (1 + z^2/n)`, half-width `z/(1+z^2/n) * sqrt(p(1-p)/n + z^2/4n^2)`.
- Worked reading: 49/65 = 75.4%, Wilson 95% about [63.7, 84.2]. A target of 92% is outside the interval, but a 5-point gain would not be distinguishable from noise.
- Sample-size arithmetic (Wilson 95%, own calculation):

| Goal | Needed n |
|---|---|
| Even a perfect score on n = 26 only gives a lower bound near 87% | n = 26 can never prove a 95% target |
| Prove "at least 95%" with zero errors | n of about 73 |
| Half-width +/- 5 points near 92% | n of about 113; +/- 3 points: about 314 |
| Lower bound above 92% when the true rate is 95% | n of about 290 (about 110 if the true rate is 97%) |
| Zero events observed and upper bound at or below 0.5% (hallucination rate) | n of about 600 (rule of three: 3/n) |

- Slice by class for diagnosis, but do not claim a pass/fail on a subgroup with n of 15; say "consistent with the target / consistent with failure".
- Cases that share a source document or class are correlated; cluster errors when computing standard errors, or report per class with caution (Miller, "Adding Error Bars to Evals").
- Size the set before running: decide which claim you must be able to make, then compute the n that supports it.

## 10. Paired comparison between prompt or model versions

Run both versions on the **same cases** and compare per case, not two independent percentages.

- Build the 2x2 table of per-case outcomes (both pass, A only, B only, both fail). Only the discordant cells carry information.
- **McNemar's test** (exact binomial on the discordant counts when they are few): under "no difference", the A-only and B-only cells are split 50/50. 8 wins vs 2 losses is evidence; 5 vs 3 is not.
- For continuous scores or judge ratings use a **paired bootstrap**: resample cases with replacement, recompute the mean difference, read the 95% interval of the difference.
- Report wins, losses and the paired difference with its interval. Add a **no-loss rule per class**: a change that raises the average while a class drops stays out until the drop is explained.
- Repeat stochastic cases (N samples) so that sampling noise is not mistaken for a version effect.
- Compare per provider: a prompt tuned on one model family can behave differently on another; re-run the paired eval on the model that will actually answer.

## 11. Sealed (held-out) sets and how they get burned

- One set serves one function: **tune** sets fit retrieval and prompts, a **sealed** set measures generalization once. Contamination is any leak of evaluation data into whatever adjusts the system, including the engineer who reads failing cases to write a fix.
- Freeze the sealed set with a content hash before touching the system; have it authored by someone who did not write the fix; write it after the classes are defined, with enough n per class (section 9) and its own abstention and adversarial cases.
- **Burning:** opening the sealed set to read failures turns it into a tune set. Every case read "only to diagnose" counts. A tell-tale sign is a large gap between tune and sealed scores (for instance, retrieval recall 98% on tune vs 83% on sealed).
- Policy: each sealed set buys one decision. After it is read, write a fresh one; keep a log of which sets are burned and when.
- Never fine-tune embeddings or prompts on cases that also sit in the sealed set.
- Public benchmarks suffer the same contamination (training data overlap); prefer private domain sets for ship decisions and use public ones only to shortlist candidates.

## 12. Calibrated abstention

Abstention has two error directions and each needs its own metric:

| Metric | Definition | Failure it exposes |
|---|---|---|
| Correct abstention | of questions that should be refused (out of corpus, false premise, no source), the share the system refuses | hallucination, invented citations |
| Wrong abstention | of questions that could be answered from the corpus, the share the system refuses | an assistant that is safe but useless |

- Optimizing only the first yields an assistant that refuses everything; set a ceiling for the second (for example 5%) next to the floor for the first.
- Build abstention cases by type: out-of-scope topic, premise error (wrong year, non-existent act), partial coverage, sources present but non-responsive.
- Do not calibrate abstention from the model's self-reported confidence; self-knowledge calibration is decent with the source in context but generalizes poorly across tasks (Kadavath et al.). Use retrieval signals (reranker score, support thresholds) and code validators, choose thresholds from the precision-recall curve on a tune set, and confirm on the sealed set.
- A guard in code beats more prompt: if the passage needed was withheld by a filter, the answer path should be closed in code.

## 13. Fix by error class, not by case

1. Classify each failure by cause (section 8 buckets), then find its **family**: what the failing cases share (document type, jargon, premise, conflict between sources).
2. Fix only families with several cases or a general explanation. A special floor, glossary entry or pair for one case is a patch that the next sealed set will not inherit.
3. Prefer mechanisms that act on the whole distribution (chunk representation, second-stage reranker, query expansion) and test out of sample: gain on the tune set alone does not count.
4. Stacks of special-case rules become debt; periodically ablate each rule and keep only those whose removal loses cases.
5. Every fix ships with a regression case that stays in the suite.

## 14. LLM-as-judge calibration

- Judges are biased: position (prefers the first answer), length (prefers longer), self-preference (prefers its own family). Mitigate by swapping order and averaging, fixing length, using binary or 3-point rubrics per criterion, asking for the rationale before the verdict.
- **Calibrate against humans:** label 100-300 items by domain experts, run the judge, and report agreement: raw agreement, Cohen's kappa (chance-corrected; roughly 0.6 is substantial, 0.8 near-perfect on the Landis-Koch scale), and the confusion matrix, with the false-pass rate called out because it is the dangerous direction.
- Statistical correction: prediction-powered inference (PPI, as in ARES) combines a large judged set with a small human-labelled set to give intervals that account for judge error.
- Re-calibrate when the judge model, rubric or domain changes. Keep the judge model different from the model being judged where possible.
- A deterministic validator beats a judge wherever it can express the check (does the cited id exist, is the quote in the source).

## 15. A/B exit criteria

Write the decision rule **before** the test starts.

- **Primary metric** (one), **guardrail metrics** (hallucination, wrong abstention, latency p95, cost per request, safety violations), minimum detectable effect, and the n or duration it requires.
- **Ship** when the primary improves with the interval of the paired difference above zero (or above a stated margin) and no guardrail regresses beyond its limit. **Stop** early only for guardrail breaches, never for a lucky early lead (peeking inflates false positives; use sequential methods if you must peek).
- **Roll back** automatically on guardrail breach; keep the old prompt/model version addressable.
- Shadow mode (new version runs unseen on live traffic, outputs compared offline) before exposing users.
- Record the decision, numbers and version ids in the changelog.

## 16. Defenses against Goodhart and metric gaming

When a measure becomes a target it stops measuring (Goodhart). In LLM work it shows up as prompts overfitted to the eval set, thresholds tuned on the judging data, or judges that reward style.

- Keep tune and sealed sets apart (section 11); refresh sets from real traffic so the system cannot memorize them.
- Track several metrics that pull against each other (correct abstention vs wrong abstention, citation recall vs precision, quality vs cost).
- Add adversarial and "canary" cases whose right answer is unusual; inspect samples by hand regularly rather than trusting aggregates.
- Rotate or ensemble judges, hide judge rubrics from the system under test, and audit a sample of passes, not only failures.
- Watch for degenerate wins: shorter answers that omit content, over-refusal, copying source text verbatim to pass a support check.
- Review the distribution of changes: a gain concentrated in one class or one document is a red flag.

## 17. Tracing with OpenTelemetry GenAI semantic conventions

- OpenTelemetry defines GenAI semantic conventions for spans, metrics and events (model calls, agent steps, tool execution, MCP). The conventions live in a dedicated repository, and their stability status was still "development" when read: pin the version of the convention you emit and expect attribute renames.
- Emit one trace per user request with child spans for retrieval, rerank, each model call, validation, and each tool call; carry the request id, tenant id and prompt version as attributes.
- Typical attributes per model call: operation name, provider, requested and responding model, input/output token usage, finish reason, error type. Cost can be derived downstream from token usage and a price table.
- Message content (prompts, completions) is sensitive: capture it only behind an explicit opt-in, redact PII, set short retention, and prefer storing content in a separate, access-controlled store referenced by id.
- Backends: any OTLP-compatible store, or LLM observability tools (Langfuse, Phoenix, LangSmith and others) that ingest OTel traces. Join traces with eval results by prompt version to see which version caused a regression.
- Add dashboards and alerts on validation-failure rate, refusal rate, abstention rate, p95 latency per stage, cost per request and per tenant.

## 18. Eval as a CI gate

- Make the eval a **merge gate** with written thresholds (for example citation correctness, correct abstention, hallucination rate, and a zero-tolerance invariant such as "no citation of an unusable passage"). Below the bar the change does not ship; accepted exclusions are recorded in the PR with the exact count, so a newly excluded case fails the gate.
- Two tiers: **offline** (fake or scripted model, zero cost, runs on every PR) proves the plumbing and the invariants (zero hallucinated ids, zero filter violations); **real-model** runs (paid) only when the change touches the answer path (prompts, retrieval, embeddings, model or provider, citation validation, ingestion) and once per milestone. Report "offline passed" and "real passed" separately; offline results are not evidence of model quality.
- Do not cache test results across runs that touch a database or a model: a cache hit can hide a regression. Cache dependency installs, not verdicts.
- A scheduled nightly run is an alert, not proof of a commit: always check which commit it ran on.
- Keep a failure taxonomy per class (section 8, 13) in the report, and a table of wins and losses per class from the paired comparison.

## Sources (read 2026-11-15 unless noted)

- ALCE, Gao et al., citation recall/precision definitions: https://arxiv.org/abs/2305.14627 (study notes, read 2026-11-13; not re-verified)
- RAGAS, Es et al.: https://arxiv.org/abs/2309.15217 (study notes, 2026-11-13; not re-verified)
- ARES, Saad-Falcon et al., PPI: https://arxiv.org/abs/2311.09476 (abstract, 2026-11-13; not re-verified)
- Brown, Cai, DasGupta, Interval Estimation for a Binomial Proportion, Statistical Science 2001: https://projecteuclid.org/journals/statistical-science/volume-16/issue-2/Interval-Estimation-for-a-Binomial-Proportion/10.1214/ss/1009213286.full (2026-11-13; not re-verified)
- Miller, Adding Error Bars to Evals: https://arxiv.org/abs/2411.00640 (abstract, 2026-11-13; not re-verified)
- Xu et al., Benchmark Data Contamination survey: https://arxiv.org/abs/2406.04244 (abstract, 2026-11-13; not re-verified)
- Thakur et al., BEIR (heterogeneity across collections): https://arxiv.org/abs/2104.08663 (2026-11-13; not re-verified)
- Kadavath et al., Language Models (Mostly) Know What They Know: https://arxiv.org/abs/2207.05221 (abstract, 2026-11-13; not re-verified)
- Wen et al., Know Your Limits: A Survey of Abstention in LLMs: https://arxiv.org/abs/2407.18418 (abstract, 2026-11-13; not re-verified)
- Landis and Koch kappa scale, McNemar test, rule of three: standard statistics (own summary, not fetched)
- OpenTelemetry GenAI semantic conventions (moved to a dedicated repository; attribute details not retrievable on 2026-11-15, so attribute names above are described generically): https://github.com/open-telemetry/semantic-conventions-genai

See also: `diagnosis-playbook.md` Tree 10 (noisy or untrusted scores) and the sample-size numbers, `playbooks.md` sections 2 and 4 (eval set, judge calibration, prompt change protocol), `variants/evals-and-monitoring.md`.

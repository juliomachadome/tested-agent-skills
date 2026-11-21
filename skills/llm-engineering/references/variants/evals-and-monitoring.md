# Variant: evals and monitoring

Use for: building the measuring stick for any LLM feature before and after launch: eval sets, judges, statistics, CI gates, production monitoring.

## Architecture choice
Three layers. (1) Deterministic checks in code (schema, ids exist, numbers match, forbidden strings) on every output in production. (2) An offline eval set run in CI on every prompt, model, retrieval or schema change, with a sealed part opened per milestone. (3) Production monitoring on logged traces plus a weekly human review of a random sample. Use a hosted tracing tool or OpenTelemetry-style traces; the point is to have model id, prompt version, tokens, latency and validation result on every call. Detail: `../evals-observability.md`; build routine: `../playbooks.md` section 2.

## Prompt pattern (for a judge)
A rubric of single-criterion questions with anchored examples; evidence first, verdict after; binary or three-level scores; order of candidates randomised; judge from another model family than the system under test; judge id, prompt and rubric frozen and versioned. Treat the judge as a guard calibrated against human labels, not as ground truth.

## Metrics and statistics
- Report n, rate and Wilson 95% interval for every proportion (112 of 120 is 93.3%, interval 87.4% to 96.6%).
- Compare versions paired on the same cases: count wins and losses, McNemar or paired bootstrap. A 5-point change needs roughly 300-600 paired cases or about 900 per independent arm near 80-85% (`../diagnosis-playbook.md`).
- Per-stage metrics, per-class slices, abstention both ways; cost and p95 latency beside quality.
- Never tune on the set that judges; a sealed set that has been read is burned. Run-to-run noise: repeat runs or fix temperature, and report the spread.
- Production: drift in input mix, validation failure rate, abstention rate, cache-hit rate, spend per day, user signals.

## Failure modes
Tiny sets treated as proof; tuning on the judging set; judge biases (position, length, self-preference); contamination from public benchmarks; label errors; metric chosen because it is easy; proxy metric gamed; dashboards with no alarm thresholds; eval harness differing from production (different prompt, parameters or retrieval). See `../diagnosis-playbook.md` Tree 10.

## Cost notes
Offline measures first (replayed contexts, recorded vectors) before paid generation runs; run the full set only for candidates that pass cheap checks; use batch tiers for eval runs (50% off, 2026-11-18); cap judge tokens; cache the shared prompt prefix; log with sampling for high-volume features, full capture for errors.

## Checklist
- [ ] Eval set with tuning, dev and sealed parts; sealed one frozen by hash.
- [ ] Baseline scored before any change.
- [ ] Deterministic checks in production, not only offline.
- [ ] Judge calibrated against 100+ human labels; recalibrated monthly.
- [ ] CI gate: paired comparison with intervals and a no-severe-regression rule.
- [ ] Dashboards with alarms; weekly human sample review.
- [ ] Incident cases added to the sets (`../playbooks.md` section 7).

# Tail latency, external-signal sync, repository hygiene

## Tail latency and load models
- Utilisation drives latency non-linearly: queueing delay grows roughly with 1/(1 - utilisation). Keep latency-critical services well below saturation (a common ceiling is 70-80% of measured capacity) and size pools with Little's law (concurrency = latency x throughput).
- Optimise and alert on p99 or p99.9, not the mean. Fan-out multiplies the tail: a request that waits on ten dependencies is slow whenever any one is slow.
- Coordinated omission: a load generator that waits for each response before sending the next hides stalls and understates the tail. Use an open-loop (fixed arrival rate) test or a tool that corrects for it, and say which one you used.
- Head-of-line blocking: one slow request in a single queue or single-threaded loop delays everything behind it. Isolate slow work in its own pool or queue, set timeouts per class, and bound queue length.
- Hedged requests (send a second copy to another replica after a high percentile threshold) cut the tail for idempotent reads; cap them so they do not amplify load during an incident.
- Batching raises throughput and adds latency: choose a short time window and a size cap, and measure both.
- Before optimising: write the latency target per operation, measure with tracing, find the bottleneck with a profile, remove work before speeding work up, then validate under realistic load and keep watching in production.
- Consistency costs latency: synchronous replication or consensus pays a round trip per write; asynchronous replication is faster and can serve stale reads. State which one the feature needs.

## Syncing from an external stream (mailbox, webhook queue, partner API)
- Query by exclusion (skip drafts and sent items) rather than by one folder; people archive and filter incoming items.
- Keep an append-only record of processed ids and write an id only after every resulting change is saved, so a crash replays safely instead of dropping work.
- Read the full body before classifying; subjects and snippets mislead (a scheduling link is not a decision).
- Signals that imply a sensitive outcome (offer, settlement, cancellation, terms change) become a "review needed" state, never an automatic status change.
- If an incoming signal contradicts a final local state, stop and show the conflict; do not overwrite silently.
- Present discovered updates as one table (item, current state, proposed state, evidence snippet, confidence) and apply only what the operator confirms: all, a chosen subset, or none.
- When writing third-party text into delimited files, strip or escape quotes, line breaks and delimiters first, or one value will shift every later column; also neutralise leading `= + - @` for spreadsheet opening.

## Repository hygiene
- Classify before deleting: source (including fixtures the tests read), generated files the project commits (regenerate, never hand-edit), working material (plans, scratch notes), local state (caches, build output).
- Working material lives in one ignored folder; promote a durable conclusion into a committed document instead of committing the scratch version.
- When removing a file, repair every reference to it (links, scripts, CI paths) in the same change.

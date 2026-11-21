# Backend latency, queues and tail

## Contents
1. Measuring latency
2. p95 per stage
3. Utilization, Little's law, queueing
4. Amdahl
5. Tail latency
6. Node event loop
7. Cold start and regions
8. Timeouts and external calls

## 1. Measuring latency

- Latency is a distribution. Report p50, p95, p99 and max; mean only as a helper column. Source: Google SRE Book, "Service Level Objectives", https://sre.google/sre-book/service-level-objectives/ (input, read 2026-11-13; not re-fetched).
- Record counts per latency bucket (histogram) with roughly exponential bounds, so any percentile can be recomputed later and bimodality (cold vs warm) becomes visible. Source: SRE Book, "Monitoring Distributed Systems" (same status).
- Separate latency of successes from latency of errors. A fast 500 pulls the mean down; a slow error is worse than a fast one. Never mix a timeout-ended request into the good ones, and never drop it from the sample.
- USE method (Brendan Gregg): for every resource check utilization, saturation and errors; saturation is the work queued beyond what the resource can service. Source: https://www.brendangregg.com/usemethod.html (fetched 2026-11-15). Pair it with the request-oriented golden signals below.
- Four golden signals: latency, traffic, errors, saturation. Many systems degrade well before 100 percent utilization.
- Choose targets from what users care about, not what the system happens to do; fewer, meaningful objectives.
- Aggregation window matters: a long average hides bursts; a short-window p99 is an earlier saturation signal. Measure under burst, not only under steady load.
- Closed-loop load generators (send the next request only after the previous returns) hide tail latency because the client waits out the slow response (coordinated omission). For API routes, use a fixed arrival rate. For human-sequential flows a closed loop is realistic. (Attributed to G. Tene; no primary source fetched.)
- Sample size: p95 of 8 runs is essentially the second-largest value; p95 of 40 is the third. Operational rule: at least 30 samples for a route p95; at least 100 for p99, otherwise call it "max observed".

## 2. p95 per stage

Instrument each stage of a request or job (auth, cache lookup, DB, external call, render, serialize) with a duration number and a small enum, never with content or personal data. Then budget per stage so the stage budgets sum to the end-to-end p95. A request that crosses stages needs the stage timings in one trace to see where p95 is spent; the sum of per-stage p95s overstates the end-to-end p95, so measure the end-to-end separately. Fix the stage with the biggest share of the tail, not the biggest share of the mean.

## 3. Utilization, Little's law, queueing

- Little's law: L = lambda x W (average items in the system = arrival rate x average time in system). It holds for any stable system, no distribution assumptions. Use it to size concurrency: 200 requests per second at 0.25 s each means about 50 in flight; a pool of 20 will queue. Source: J.D.C. Little, "A Proof for the Queuing Formula L = lambda W", Operations Research 1961 (not re-verified).
- For a single-server queue with random arrivals (M/M/1), mean waiting time grows like rho / (1 - rho) times the service time, where rho is utilization. At 50 percent the wait equals one service time; at 90 percent it is nine; at 95 percent nineteen. Latency is not linear in load: a system at 85 percent utilization is already near the knee. This is a textbook result (not re-verified against a primary page); real systems are burstier than M/M/1, so the knee comes earlier.
- Consequences: leave headroom (target peak utilization well under 80 percent for latency-sensitive paths); cap queue length and reject or shed early rather than queue unboundedly; separate fast and slow work in different pools or queues so slow jobs do not starve interactive ones; scale on saturation signals (queue depth, event loop delay, pool wait), not on CPU alone.
- Job queues: measure queue wait separately from run time. Rising wait with flat run time means too few workers or arrival above capacity.

## 4. Amdahl

Speedup of the whole = 1 / ((1 - p) + p / s), where p is the fraction of time in the part you speed up and s the speedup of that part. Making a stage that takes 10 percent of the request 10 times faster saves at most 9 percent. Always compute the share of the stage first; this is why you split before you fix. The same law bounds parallelization: the serial fraction caps the gain.

## 5. Tail latency

Source: Jeffrey Dean and Luiz Andre Barroso, "The Tail at Scale", Communications of the ACM 56(2), 2013, https://research.google/pubs/the-tail-at-scale/ (abstract fetched 2026-11-15): rare slow episodes that do not matter in small systems dominate performance at scale; the paper proposes building a predictably responsive whole from less predictable parts, using techniques that mostly reuse fault-tolerance resources.

- Fan-out arithmetic: if each of N backends is slow with probability 1 percent, a request touching all N is slow with probability 1 - 0.99^N: about 63 percent at N = 100. The p99 of one backend becomes the median of the front end (SRE Book, input, not re-fetched).
- Techniques named in the paper (from the full article, not re-verified in this round): hedged requests (send a duplicate after a short delay, take the first answer, cancel the other), tied requests, micro-partitioning, selective replication, good-enough partial results, and keeping background work from colliding with interactive work. Hedging requires idempotent reads and a cap so retries do not become a load multiplier.
- Retries add load exactly when the system is slow. Use jittered backoff, a retry budget and a ceiling.

## 6. Node event loop

Source: Node.js docs, perf_hooks and "Don't Block the Event Loop" (input, read 2026-11-13; not re-fetched).
- `perf_hooks.monitorEventLoopDelay()` returns a histogram (nanoseconds) with percentiles; `performance.eventLoopUtilization()` gives idle, active and utilization between two samples. Event loop delay is the saturation signal for a Node API.
- Node is fast while the work per client at any moment is small. Blockers: synchronous crypto, zlib, fs and child_process calls, vulnerable regex (ReDoS), parsing or stringifying very large JSON, algorithms whose cost grows with client input. Bound the size of client JSON or stream it.
- Mark stages with `performance.mark` and `measure`; disconnect observers you do not use.

## 7. Cold start and regions

- A cold start (new serverless instance, scaled-to-zero container) adds a one-off delay to the first request; it shows as bimodal latency (first of the day vs the rest). Measure cold and warm separately and report both; a p50 hides it. Vendor docs often give no number; measure on your platform and region.
- Mitigations in order of simplicity: smaller bundles and fewer imports at module load, lazy initialization of heavy clients, minimum instances or keep-warm only if the cost fits, and moving work off the request path.
- Put the database, the backend and most users on the same continent; each cross-region round trip adds to TTFB. Chatty code (N+1) multiplies that cost.

## 8. Timeouts and external calls

Every outbound call (HTTP, model, storage) needs a timeout, a retryable-error classification and a ceiling. Do not hold a database transaction open across external I/O: it pins a connection and a snapshot. Run independent awaits in parallel. Do not call your own HTTP route from inside a server render; call the function.

## Sources

- https://www.brendangregg.com/usemethod.html (fetched 2026-11-15)
- https://research.google/pubs/the-tail-at-scale/ (abstract fetched 2026-11-15)
- https://sre.google/sre-book/service-level-objectives/, /monitoring-distributed-systems/, https://nodejs.org/api/perf_hooks.html (input file, read 2026-11-13, not re-fetched)
- Little 1961 (not re-verified)

# Scaling and load balancing

Use when someone says "we need to scale", "add a load balancer", "autoscale" or "it falls over under load". Tags: `[n]` = source in BIBLIOGRAPHY.md; `(calc)` = arithmetic shown here; `(assumed)` = illustrative number, replace with yours. Facts about vendors dated 18/11/2026.

## 1. Do you need it? Measure first
- Little's law (a standard queueing identity, not tied to one source here): concurrent requests in flight L = arrival rate (RPS) x mean latency (s). 200 RPS at 150 ms means about 30 in flight (calc).
- Utilisation: queueing delay grows sharply above about 70-80% of a resource. A node at 90% CPU has little room for a burst, so look at p95/p99, not the mean. Fast-failed requests must not be mixed into success latency `[35]`.
- Find the bottleneck first (CPU, DB connections, a slow query, a lock, an external API). More instances in front of a saturated database make it worse.
- Order: fix the hot query or cache, then a bigger instance (no new failure modes), then more instances (needs stateless design), then partition data.
- You do NOT need this when: one instance plus a managed platform meets the SLO at peak with 2x headroom; the platform already balances and autoscales (see `cloud-deploy-ops` playbooks, section 10). Two instances for availability is redundancy, not scale.

## 2. Stateless services, and where state goes
Any instance must handle any request. Sessions go to a signed short-lived cookie/JWT or Redis; uploads to object storage; jobs to a queue; locks to the database or a lease with a fencing token (`data-systems.md`). Usual leaks: in-memory counters, local files, a cron in every replica (runs N times).

## 3. Load balancer types
- **L4 (TCP/UDP)**: forwards connections by address and port, cheap, protocol-agnostic, no HTTP awareness. Hash or connection tracking keeps a connection on one backend `[33]`. Good for databases, gRPC passthrough, TLS passthrough.
- **L7 (HTTP)**: terminates TLS, reads path, host, headers and cookies, so it can route by path, retry idempotent requests, add headers, rate limit and compress. Costs more CPU and is one more hop. Default for web APIs.
- DNS is coarse: resolvers cache and some ignore TTL; use it for region steering, not fast failover `[33]`.

## 4. Algorithms: when to use which
| Algorithm | Behaviour | Use when |
|---|---|---|
| Round robin | rotates | requests are similar in cost and backends equal (can leave a 2x CPU gap when cost varies `[34]`) |
| Weighted round robin | share by weight | mixed instance sizes, canary at 5% `[39][40]` |
| Least connections / least request | fewest active | variable request cost, long calls; needs the balancer to see all traffic `[39]` |
| Least response time | fewest active, fastest | latency varies by backend; risk: a failing backend that answers fast with errors attracts traffic, so count errors `[34][39]` |
| Random with two choices (P2C) | sample 2, take the less loaded | many balancers or clients sharing backends; avoids herding on one "least loaded" node; near-best balance at O(1) cost `[36][40]` |
| Consistent / rendezvous hashing | key -> same backend, few keys move when the pool changes | caches, sharded in-memory state, per-key affinity; removing one of N hosts moves about 1/N of keys `[37][40]`. Never `hash mod N` with changing N |
| Random | simple | no health data, many clients `[40]` |
Default for HTTP APIs: least request or P2C. Hash a key only when locality is the point; hot keys need salting (`data-systems.md`).

## 5. Sticky sessions: avoid
Affinity (cookie, IP hash) pins users to a node: uneven load, sessions lost on deploy, crash or scale-in. Move session state out (section 2). Unavoidable cases: WebSockets/SSE and long-lived streams (the connection is the affinity) and in-memory game or editor rooms. Then either shard by room key with consistent hashing, or let any node accept the socket and fan out through a pub/sub backplane (Redis, NATS, a managed broker) so that a message to a room reaches every node holding members. Reconnect with jitter after a deploy.

## 6. Health checks, draining, graceful shutdown
- **Liveness**: "restart me if this fails" (deadlock, wedged process). Keep it local and cheap; never check the database in liveness, or a DB blip restarts every instance `[38]`.
- **Readiness**: "send me traffic" (warm, dependencies reachable, not overloaded). A failing readiness removes the instance from rotation without a restart `[38]`.
- **Startup** probe for slow boots, so liveness does not kill them `[38]`.
- Keep enough capacity to answer health checks under load; if the check fails during a brownout the balancer removes capacity and makes it worse `[35]`.
- **Draining**: on shutdown, fail readiness (or enter a "lame duck" state), stop accepting new work, finish in-flight requests, then exit `[34][38]`. On Kubernetes the order is endpoints removal, `preStop`, SIGTERM, then SIGKILL after `terminationGracePeriodSeconds` (default 30 s) `[38]`. Grace period must exceed your longest request plus the balancer's propagation delay (a `sleep` of a few seconds in preStop is common).

## 7. Timeouts, retries, retry budgets
Set each timeout below the caller's own deadline and propagate it down the chain. Retry only idempotent calls, with exponential backoff and jitter, and cap retries as a budget (for example retries <= 10% of requests, and one retry layer per chain) `[29][28]`. Three layers retrying 3 times each turn one failure into 27 calls (calc). Retries during overload are the classic cascade trigger. Passive ejection (N failures in a window removes a backend) complements active checks `[39]`.

## 8. Autoscaling
- Signals: CPU for CPU-bound work, concurrency per instance for I/O-bound, queue age for workers.
- Scale out fast, in slowly: a cool-down of 3-10 minutes (assumed) avoids flapping; scale in by a fraction, not to zero at once.
- Minimum instances: at least 2 across zones if an outage matters; min 0 (scale to zero) saves money on idle services but adds cold starts (seconds for containers, tens to hundreds of ms for pre-warmed functions); pick min 0 only for tolerant or internal workloads.
- Boot time bounds reaction: with 60 s to ready, headroom must cover 60 s of growth.
- Load shedding and CPU autoscaling can mask each other: shedding keeps CPU low so scaling never fires, and the fleet runs closer to rejection than it looks `[35]`. Scale on a signal that shedding does not suppress (requests, concurrency, rejects).

## 9. Global load balancing
GeoDNS answers with the nearest region from the resolver's location (coarse; resolvers hide the user's address) `[33]`. Anycast announces one IP from many sites; the network picks the nearest (CDNs, stateless edges). Multi-region writes are the hard part: one write region plus read replicas unless you accept conflict handling (`data-systems.md`).

## 10. Database scaling
- **Read replicas**: scale reads, not writes. Replication is asynchronous, so a read after a write may miss it. Lag impact (calc): lag 200 ms, a user saves and the next page loads in 80 ms from a replica = stale read. Fixes: read from the primary for a few seconds after that user's write, or pass a log position, or keep read-your-writes paths on the primary `[1]`.
- **Connection pooling**: 20 app instances x 20 connections = 400 connections, often beyond what Postgres handles well; use a pooler (transaction mode) or cap the pool per instance. Autoscaling multiplies connections, so size the pool as `max_connections / max_instances`.
- **Partitioning/sharding** only after indexes, caching, replicas and vertical size are spent; it is a one-way door (`data-systems.md`, `[1]` ch. 5-6).

## 11. Caching and CDN
Layers: browser (`Cache-Control`), CDN, application cache, database buffer. A CDN with a 95% hit ratio sends 5% of requests to origin: 2,000 RPS at the edge is 100 RPS at origin (calc). Coalesce requests so a cold key does not stampede; include tenant or user in the key when content varies.

## 12. Rate limiting, load shedding, backpressure
Rate limit per client at the edge to protect fairness; shed load at the server when it nears capacity: reject early with 429/503 and `Retry-After`, drop stale queued work, prefer finishing work already started and shed low-priority traffic (crawlers) first `[35][29]`. Cap queues by wait time, not only by length; unbounded queues turn overload into timeouts for everyone. Load test past the break point; goodput should plateau, not collapse `[35]`.

## 13. Worked sizing
Target: 600 RPS peak, p95 latency 250 ms, mean 120 ms, each instance safely handles 16 concurrent requests (measured by load test; assumed here).
1. In flight at peak: 600 x 0.12 = 72 (calc).
2. Instances at 60% target utilisation: 72 / (16 x 0.6) = 7.5, so 8.
3. Add N+1 for a failed zone or deploy surge: 9 instances.
4. If one instance dies, 8 remain: 72 / (8 x 16) = 56% utilisation, still fine.
5. If a downstream slows to 600 ms mean, in flight becomes 360 and needs 38 instances: latency dependencies change capacity more than traffic does (calc).
Redo with measured concurrency.

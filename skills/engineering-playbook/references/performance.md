# Performance

## 1. Method (always in this order)

1. **Define the goal** in user terms: p95 latency < X ms, throughput Y req/s, memory < Z, cost per request.
2. **Measure** the current state with production-like data. Averages lie — use **p50/p95/p99** and max.
3. **Find the bottleneck** (profile, trace, query plan). Usually: DB round-trips, missing index, over-fetching, external calls, serialization, allocations/GC, lock contention, event-loop blocking.
4. **Fix the biggest one**, re-measure, stop when the goal is met.
5. **Guard it**: benchmark or load test in CI for critical paths; alert on regressions.

**Amdahl's law:** speeding up a part that is 10% of the time can at most save 10%. Optimize where the time actually goes.
**Little's law:** `concurrency = throughput × latency`. Use it to size pools, queues and instances (e.g. 200 req/s × 0.25 s = 50 requests in flight).

## 2. Latency numbers (orders of magnitude)

| Operation | ~Time |
|---|---|
| L1 cache reference | 1 ns |
| Branch mispredict | ~3–5 ns |
| L2 cache | ~4 ns |
| Main memory | ~100 ns |
| Compress 1 KB (fast codec) | ~2 µs |
| SSD random read | ~16–100 µs |
| Round-trip within a datacenter / same region | ~0.5 ms |
| Read 1 MB sequentially from SSD | ~0.2–1 ms |
| Typical indexed DB query incl. network | ~1–5 ms |
| Cross-region / cross-continent round-trip | ~70–150 ms |

Implication: a loop doing 100 sequential 2 ms queries spends 200 ms waiting — more than almost any CPU work in a request.

## 3. I/O first

- **N+1:** one query per item → batch (`Include`, join, `IN (...)`, DataLoader pattern for GraphQL).
- **Chatty APIs:** multiple sequential calls → parallelize independent calls (`Task.WhenAll`, `Promise.all`) with a concurrency limit; or add a batch endpoint.
- **Over-fetching:** project only needed columns/fields; paginate; compress large responses (Brotli/gzip).
- **Under-fetching from the client:** BFF/aggregated endpoint instead of 10 calls from the browser/mobile.
- **Payload size:** avoid returning huge JSON; stream large results (`IAsyncEnumerable<T>` in ASP.NET Core streams JSON arrays).
- **Connection reuse:** HTTP keep-alive, connection pooling (DB, HTTP). Never create clients per request.

## 4. Caching

| Strategy | How | Use when |
|---|---|---|
| Cache-aside | read cache → miss → load → set | default for read-heavy data |
| Read-through / write-through | cache layer loads/writes the store | library support exists |
| Write-behind | write to cache, flush async | high write rates, can tolerate loss risk |
| HTTP caching | `Cache-Control`, `ETag`/`If-None-Match`, CDN | public or per-user GET resources |
| Memoization | in-process function cache | pure, expensive, repeated computations |

Rules:
- Every cache needs: **key design** (include tenant/user/culture/version), **TTL**, **invalidation** strategy, **size bound**, and a plan for **cold start**.
- **Stampede protection:** when a hot key expires, many requests recompute at once → single-flight/locking per key, early refresh, jittered TTLs. .NET 9 `HybridCache` provides stampede protection and L1+L2.
- Never cache per-user/tenant data under a shared key (data leak).
- In-memory caches are per instance; multi-instance apps need a distributed cache (Redis) or accept inconsistency between instances.
- Cache negative results briefly to avoid hammering on misses, but beware of caching errors.
- "There are only two hard things: cache invalidation and naming things." Prefer short TTL + event-based invalidation for correctness-critical data.

## 5. .NET specifics

**Allocations & GC**
- Allocations are cheap; **collections** are not. Reduce allocations on hot paths.
- Objects ≥ 85,000 bytes go on the **Large Object Heap** (collected with Gen2, not compacted by default) → reuse large buffers with `ArrayPool<T>.Shared`.
- `Span<T>`/`ReadOnlySpan<T>`/`Memory<T>` for slicing without copying; `stackalloc` for small, bounded buffers.
- Avoid **boxing** (value types to `object`/non-generic interfaces, `string.Format` with value types in hot loops, enum `HasFlag` on old runtimes).
- `struct` for small (≤ ~16 bytes), immutable, short-lived values; otherwise `class`. `readonly struct`, `record struct` where appropriate.
- `string`: use `StringBuilder` in loops, `string.Create`, interpolated string handlers; `StringComparison.Ordinal` for non-linguistic comparisons (faster and correct).
- Server GC for ASP.NET Core (default); consider `DOTNET_GCConserveMemory`/DATAS (.NET 8+, default in .NET 9) for container memory.

**LINQ**
- Fine in most code; on hot paths it allocates enumerators/delegates. Avoid multiple enumeration of `IEnumerable` (materialize once with `ToList()`/`ToArray()` if reused).
- `Any()` not `Count() > 0`; `TryGetNonEnumeratedCount`; `ToDictionary`/`ToLookup` for repeated lookups.
- On `IQueryable` (EF Core), LINQ becomes SQL — see databases.md. Calling `.ToList()` too early pulls everything into memory.

**Async**
- `async`/`await` all the way; never `.Result`/`.Wait()`.
- `ValueTask` only for hot paths that often complete synchronously, and never await it twice.
- Pass `CancellationToken` everywhere so abandoned requests stop work.

**Collections & helpers**
- Pre-size: `new List<T>(capacity)`, `new Dictionary<K,V>(capacity)`.
- `FrozenDictionary`/`FrozenSet` for read-only lookup tables.
- `SearchValues<T>` for fast multi-value searches.
- `[GeneratedRegex]` source-generated regexes; `[LoggerMessage]` source-generated logging (avoids allocations and boxing).
- System.Text.Json source generation (`JsonSerializerContext`) for faster, AOT-friendly serialization.

**HTTP & hosting**
- `IHttpClientFactory` or a long-lived `HttpClient` with `SocketsHttpHandler.PooledConnectionLifetime` (DNS changes).
- Response compression, output caching (`AddOutputCache`), response caching headers.
- Minimal APIs/native AOT reduce startup for serverless; trimming has compatibility costs.
- Azure Functions: reuse static clients across invocations; cold starts on Consumption plan — use Flex Consumption always-ready / Premium for latency-critical paths.

**Measure**
- **BenchmarkDotNet** (`[MemoryDiagnoser]`) for micro-benchmarks — never `Stopwatch` around a single call.
- `dotnet-counters`, `dotnet-trace`, `dotnet-gcdump`, Visual Studio/Rider profilers, PerfView, Application Insights profiler.

## 6. Node.js / TypeScript specifics

- **Never block the event loop:** CPU-heavy work (large JSON parse/stringify, crypto sync APIs, image processing, big loops, sync fs) stalls *all* requests. Use streaming, chunking with `setImmediate`, `worker_threads`, or a job queue.
- Use async fs/crypto APIs (`crypto.scrypt` async, not `scryptSync`, in request paths).
- **Concurrency limits:** `Promise.all` over 10k items opens 10k connections → use `p-limit`/batching.
- `Promise.allSettled` when partial failures are acceptable.
- **Streams** with backpressure (`pipeline` from `node:stream/promises`) for large files/responses.
- Avoid `array.shift()` in hot loops (O(n)), `delete obj.key` on hot objects (deopt), megamorphic objects with changing shapes.
- `JSON.parse` of untrusted large bodies: set body size limits.
- Measure with `--cpu-prof`, `clinic.js`, Chrome DevTools inspector, `performance.now()`, `autocannon`/`k6` for load.
- Cluster/multiple processes or containers to use all cores.

## 7. Frontend performance (summary — details in frontend.md)

- Core Web Vitals targets: **LCP ≤ 2.5 s, INP ≤ 200 ms, CLS ≤ 0.1** (75th percentile of real users).
- Ship less JS: code splitting, lazy routes, tree shaking, analyze bundle; prefer server rendering for content.
- Images: correct size, modern formats (AVIF/WebP), `loading="lazy"` below the fold, explicit width/height (CLS).
- Virtualize long lists; debounce search inputs; avoid unnecessary re-renders.

## 8. Serialization & payloads

- JSON is fine for most APIs; consider Protobuf/gRPC, MessagePack for high-throughput internal traffic.
- Avoid serializing entire entity graphs (cycles, over-exposure); use DTOs.
- Compress responses > ~1 KB; don't compress already-compressed data (images, zips).

## 9. Concurrency & resource limits

- Bound everything: thread pools, connection pools, queue lengths, request body sizes, page sizes, batch sizes, retries.
- Contention on a single lock/row/key serializes the system → shard the key, use optimistic concurrency, or redesign the hot spot.
- See concurrency.md for async/thread pitfalls.

## 10. Load testing

- Tools: **k6**, Azure Load Testing (JMeter/Locust-based), NBomber (.NET), autocannon (Node).
- Test realistic mixes, think time, data sizes; ramp gradually; watch p95/p99, error rate, saturation (CPU, DB DTU/vCore, connections).
- Find the knee of the curve (where latency explodes) and keep production below it with headroom.

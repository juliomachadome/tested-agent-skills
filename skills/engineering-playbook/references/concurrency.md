# Concurrency & Async

## 1. Core concepts

- **Concurrency** = dealing with many things at once (interleaving); **parallelism** = doing many things at the same time (multiple cores).
- **I/O-bound** work → async (frees threads while waiting). **CPU-bound** work → parallelism (more cores), not async.
- **Race condition:** result depends on timing of interleaved operations on shared state.
- **Deadlock:** circular waiting on locks/resources. **Livelock:** threads keep reacting without progress. **Starvation:** a task never gets the resource.
- **Thread pool starvation:** pool threads blocked (sync-over-async, `Thread.Sleep`, sync I/O) → new work waits → latency spikes across the whole app.

## 2. .NET async rules

1. **Async all the way.** Never `.Result`, `.Wait()`, `.GetAwaiter().GetResult()` in app code — risk of deadlock (UI/legacy ASP.NET contexts) and thread-pool starvation (everywhere).
2. **No `async void`** except event handlers — exceptions crash the process and can't be awaited.
3. **Propagate `CancellationToken`** through every async method and into EF/HTTP calls; honor `HttpContext.RequestAborted`.
4. **`ConfigureAwait(false)`** in reusable libraries; unnecessary in ASP.NET Core app code (no SynchronizationContext).
5. **Don't fire-and-forget** with `_ = DoAsync()` in request handlers — the scope (DbContext) is disposed and exceptions vanish. Use a queue (`Channel<T>` + `BackgroundService`, Service Bus, Hangfire).
6. **Parallel independent I/O:** `await Task.WhenAll(a, b, c)`; for many items bound the concurrency:

```csharp
await Parallel.ForEachAsync(items,
    new ParallelOptions { MaxDegreeOfParallelism = 8, CancellationToken = ct },
    async (item, token) => await ProcessAsync(item, token));
```

   or `SemaphoreSlim(8)` around each call.
7. **CPU-bound** work: `Parallel.For`/PLINQ for data parallelism; `Task.Run` only to offload from a UI thread, not inside ASP.NET request handlers (just moves work to another pool thread).
8. **`ValueTask`**: only await once; don't store or `.Result` it.
9. **Async streams:** `IAsyncEnumerable<T>` + `await foreach` for incremental processing.
10. Timeouts: `CancellationTokenSource.CancelAfter`, `Task.WaitAsync(timeout, ct)` (.NET 6+).

## 3. Shared state (C#)

| Need | Use |
|---|---|
| Avoid sharing | immutable data, message passing, per-request state (best option) |
| Simple counters/flags | `Interlocked.Increment`, `Interlocked.CompareExchange`, `Volatile` |
| Short critical section (sync) | `lock` on a private readonly object (.NET 9: `System.Threading.Lock`) |
| Critical section containing `await` | `SemaphoreSlim(1,1)` with `await WaitAsync()` / `try…finally Release()` (`lock` cannot contain `await`) |
| Thread-safe map | `ConcurrentDictionary` — note `GetOrAdd(key, factory)` may run the factory more than once; wrap value in `Lazy<T>` if it must run once |
| Producer/consumer | `System.Threading.Channels` (bounded for backpressure) |
| One-time init | `Lazy<T>` (thread-safe by default), static readonly initializer |
| Read-mostly | `ReaderWriterLockSlim` (sync only), or immutable snapshot swapped with `Interlocked.Exchange` |

- Never lock on `this`, `typeof(...)`, or strings.
- Avoid holding locks while calling external code/I/O.
- Acquire multiple locks in a consistent global order.
- **Distributed state** (multiple instances): in-process locks don't help → DB constraints/row locks, optimistic concurrency, Redis/Blob lease locks with expiry, or single-consumer queues/partitions.

## 4. DI lifetimes & thread safety (ASP.NET Core)

- Singleton services must be thread-safe and must not capture scoped services (**captive dependency**) — enable `ValidateScopes`/`ValidateOnBuild`.
- `DbContext` is scoped and not thread-safe → one per unit of work; for parallel work, create scopes (`IServiceScopeFactory`) or `IDbContextFactory<T>`.
- `HttpClient` from `IHttpClientFactory` is safe to share.

## 5. Background work

- `BackgroundService`/`IHostedService` for in-process workers; handle `stoppingToken` for graceful shutdown.
- Durable/reliable jobs → a real queue (Azure Service Bus, Storage Queues, RabbitMQ) or job system (Hangfire, Quartz, Azure Functions/Durable Functions). In-memory queues lose work on restart.
- Make jobs **idempotent** (they will run more than once) and **resumable**.
- Scheduled jobs on multiple instances run N times unless coordinated (distributed lock or single scheduler).

## 6. JavaScript/Node

- Single-threaded event loop: no data races on JS objects, but **logical races** across `await` points still happen (read → await → write).
- Don't block the loop (see performance.md). CPU work → `worker_threads`.
- Bound concurrency of promises (`p-limit`); handle rejections (`unhandledRejection` crashes the process in modern Node).
- `AbortController` for cancellation/timeouts of `fetch` (`AbortSignal.timeout(ms)`).
- React: race conditions when an older request resolves after a newer one → abort previous requests or ignore stale responses; TanStack Query handles this.

## 7. Testing concurrency

- Reproduce with many parallel requests (k6, `Parallel.ForEachAsync` in an integration test) against a real DB.
- Assert invariants (no negative balance, no duplicate rows) after concurrent runs.
- Use DB constraints so violations fail loudly instead of corrupting data.

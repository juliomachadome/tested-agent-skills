# Algorithms, Complexity & Data Structures

## 1. Big O essentials

- **What:** Big O describes how cost (time or memory) **grows** as input size `n` grows. It is not a time in seconds. Real time ≈ `c · f(n) + overhead`; Big O keeps only `f(n)`.
- **Why it matters:** it predicts whether code survives 10× or 100× more data. Measured 50 ms at n=1,000 for O(n²) → ~5 s at n=10,000.
- **Rules:** drop constants (O(2n)=O(n)); drop lower terms (O(n²+n)=O(n²)); sequential steps add; nested steps multiply; different inputs get different letters (O(n·m), not O(n²)); halving per step → log n.
- **Cases:** best / average / worst (quicksort avg O(n log n), worst O(n²); hash map avg O(1), worst O(n)). **Amortized:** dynamic array append is O(1) amortized despite occasional O(n) resize.
- **Formal:** O = upper bound, Ω = lower bound, Θ = tight bound. Industry says "O" meaning Θ.
- **Space complexity counts too**, including recursion stack depth (recursion over n items → O(n) stack → possible stack overflow).

### Growth table (n × 10 → time ×)

| Class | Name | ×10 input → time | Feasible n in ~1 s (≈10⁸ simple ops) |
|---|---|---|---|
| O(1) | constant | ×1 | any |
| O(log n) | logarithmic | +small | any |
| O(n) | linear | ×10 | ~10⁸ |
| O(n log n) | linearithmic | ~×13 | ~10⁶–10⁷ |
| O(n²) | quadratic | ×100 | ~10⁴ |
| O(n³) | cubic | ×1000 | ~500 |
| O(2ⁿ) | exponential | explodes | ~25 |
| O(n!) | factorial | explodes | ~11 |

**Empirical check:** run with n, 2n, 4n. Time doubles → O(n); quadruples → O(n²); barely changes → O(1)/O(log n).

## 2. Lower bounds — know when to stop

- Reading/summing/validating all items: Ω(n).
- Comparison sorting: Ω(n log n). (Counting/radix sort beat it only for bounded integer keys.)
- Searching unsorted data once: Ω(n). Repeated searches → pay O(n) once to index, then O(1)/O(log n) per query.
- "O(1)" answers almost always mean cost was **paid earlier** (index, precomputation, cache) or traded for memory.

## 3. Optimization patterns (the toolbox)

| Pattern | Turns | When | Example |
|---|---|---|---|
| **Hash index** | O(n·m) → O(n+m) | lookup by key inside a loop | `accounts.ToDictionary(a => a.Id)`; `new Map(users.map(u => [u.id, u]))` |
| **HashSet membership** | O(n²) → O(n) | `contains`/dedupe/intersection | `new HashSet<int>(ids)`; `new Set(arr)` |
| **Group once** | O(n·k) → O(n) | filter by category repeatedly | `ToLookup` / `GroupBy` once; `Object.groupBy`/`Map` of arrays |
| **Sort + two pointers** | O(n²) → O(n log n) | pairs summing to X, merging sorted lists, dedupe sorted | |
| **Sliding window** | O(n·k) → O(n) | rolling sums/averages, longest substring under constraint | moving average over last k days |
| **Prefix sums** | O(n) per query → O(1) | many range-sum queries on static data | `prefix[to+1]-prefix[from]` |
| **Binary search** | O(n) → O(log n) | sorted data; "find smallest x that satisfies" (search on answer) | `Array.BinarySearch`, `List.BinarySearch` |
| **Memoization / DP** | exponential → polynomial | overlapping subproblems | fib, edit distance, knapsack, pricing tiers |
| **Greedy** | — | local optimum provably global (interval scheduling, coin change for canonical systems) | prove or test it |
| **Heap / priority queue** | O(n log n) sort → O(n log k) | top-k, k smallest, scheduling, Dijkstra | `PriorityQueue<TElement,TPriority>` (.NET 6+) |
| **Union-Find** | — | connected groups, dedupe of merged identities | near O(1) per op with path compression |
| **Topological sort** | — | dependency ordering, build/migration order, cycle detection | Kahn's algorithm O(V+E) |
| **BFS** | — | shortest path in unweighted graph, levels | O(V+E) |
| **Dijkstra / A\*** | — | weighted shortest path (non-negative weights) | O((V+E) log V) |
| **Precompute / cache** | O(work) per call → O(1) | same input repeatedly, read ≫ write | memo dictionary, materialized view |
| **Batching** | n round-trips → n/b | I/O per item | `WHERE Id IN (...)`, bulk insert |
| **Early exit / short-circuit** | avg case | first match is enough | `Any()` instead of `Count() > 0` |
| **Lazy / streaming** | O(n) memory → O(1) | huge files/results | `IAsyncEnumerable`, Node streams, `yield return` |

### Canonical example (C#) — O(n·m) → O(n+m)

```csharp
// BAD: O(movements * accounts)
var rows = movements.Select(m => new { m.Id, Account = accounts.First(a => a.Id == m.AccountId) });

// GOOD: O(movements + accounts), O(accounts) extra memory
var byId = accounts.ToDictionary(a => a.Id);
var rows = movements.Select(m => new { m.Id, Account = byId[m.AccountId] });
```

### Kadane (maximum subarray) — O(n³) → O(n)

```csharp
static int MaxSubarray(int[] a)
{
    int best = a[0], current = a[0];
    for (int i = 1; i < a.Length; i++)
    {
        current = Math.Max(a[i], current + a[i]);
        best = Math.Max(best, current);
    }
    return best;
}
```

## 4. Choosing a data structure

| Need | .NET | TypeScript/JS | Ops |
|---|---|---|---|
| Index access, iteration | `T[]`, `List<T>` | `Array` | get O(1), append O(1)*, insert/remove middle O(n), search O(n) |
| Key → value | `Dictionary<K,V>` | `Map` (prefer over plain object for dynamic keys) | O(1) avg |
| Read-only lookup built once, read many | `FrozenDictionary`, `FrozenSet` (.NET 8+) | `Map`/`Set` | faster reads, slower build |
| Membership / dedupe | `HashSet<T>` | `Set` | O(1) avg |
| Sorted keys, range queries | `SortedDictionary` (tree), `SortedSet`; `SortedList` (array, small n) | sorted array + binary search, or a lib | O(log n) |
| FIFO queue | `Queue<T>`, `Channel<T>` (async producer/consumer) | array with head index (avoid `shift()` in hot loops: O(n)) | O(1) |
| LIFO | `Stack<T>` | `Array` push/pop | O(1) |
| Priority | `PriorityQueue<T,P>` | binary heap (lib or hand-rolled) | push/pop O(log n), peek O(1) |
| Thread-safe map | `ConcurrentDictionary` | n/a (single-threaded) | O(1) avg |
| Immutable snapshots | `ImmutableArray`, `ImmutableDictionary` | frozen objects / structural sharing libs | |
| Prefix/autocomplete | Trie | Trie | O(length) |
| Many group-merge ops | Union-Find | Union-Find | ~O(1) amortized |
| Approximate membership at scale | Bloom filter | Bloom filter | O(k), false positives, no false negatives |
| Approximate distinct count | HyperLogLog (e.g. Redis `PFADD`) | | tiny memory, ~1–2% error |
| Approximate frequencies | Count-Min Sketch | | |
| Bounded recent items | ring buffer | ring buffer | O(1) |
| LRU cache | `Dictionary` + `LinkedList`, or `MemoryCache` with size limit | `Map` (insertion-ordered) delete+set | O(1) |

Notes:
- Arrays win for small n due to cache locality; a linear scan over 20 contiguous items can beat hashing.
- Hash keys must have stable, well-distributed hashes and correct equality (`record`/`IEquatable<T>` in C#). Mutating a key after insertion breaks the map.
- JS objects as maps: prototype keys (`__proto__`, `constructor`) cause bugs and security issues — use `Map` or `Object.create(null)`.

## 5. Sorting & searching facts

- Library sorts: .NET `Array.Sort`/`List.Sort` = introsort (unstable); LINQ `OrderBy` = stable. JS `Array.prototype.sort` = stable (ES2019+), TimSort in V8. Default JS sort compares **strings** — always pass a comparator for numbers.
- Sort once outside loops; if you need repeated "top k", use a heap.
- Stable sort matters when sorting by multiple keys sequentially.
- For culture-aware string ordering use a collation/`StringComparer` (see money-time-text.md).

## 6. Strings

- Repeated concatenation in a loop: O(n²) copies in some runtimes → `StringBuilder` (C#), `array.join('')` (JS, though modern V8 ropes help).
- Substring search: built-ins are optimized; KMP/Rabin–Karp/Aho–Corasick for many-pattern or streaming cases. .NET 8+ `SearchValues<T>` for fast multi-char/multi-string search.
- Edit distance (Levenshtein): O(n·m) DP — fine for short strings; use trigram/full-text indexes for fuzzy search at scale.
- Regex: can be exponential with nested quantifiers (catastrophic backtracking, ReDoS). Use timeouts (`new Regex(p, opts, TimeSpan.FromMilliseconds(100))`), `RegexOptions.NonBacktracking` (.NET 7+), or `[GeneratedRegex]`; never run user-supplied patterns without limits.

## 7. Recursion

- Each call costs a stack frame; deep recursion → stack overflow. Convert to iteration with an explicit stack for unbounded depth.
- Naive recursion with overlapping subproblems is exponential → memoize or use bottom-up DP.

## 8. Complexity classes of hard problems

- NP-hard problems (TSP, general scheduling, bin packing, knapsack variants, constraint-heavy meal/workout planning) have no known polynomial exact algorithm. Use: heuristics, greedy + local search, constraint solvers (Google OR-Tools, OptaPlanner/Timefold), integer linear programming, or approximation with a quality bound. Limit input size if exact is required.

## 9. Distributed/data-scale algorithms

- **Consistent hashing:** distribute keys across nodes with minimal remapping when nodes change.
- **Reservoir sampling:** uniform sample of k items from a stream of unknown length in O(n), O(k) memory.
- **Fisher–Yates:** unbiased shuffle in O(n). (`array.sort(() => Math.random() - 0.5)` is biased.) .NET 8+: `Random.Shared.Shuffle`.
- **External sort / merge:** sort data larger than memory by sorting chunks and k-way merging.
- **MapReduce-style aggregation:** partition → local aggregate → merge.

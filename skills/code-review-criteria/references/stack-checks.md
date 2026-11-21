# Stack-specific checks (TypeScript, React, server frameworks)

Format: **rule** · why · bibliography number (see `BIBLIOGRAPHY.md`) · example.

## 1. TypeScript

1. **The finding is whatever punches through the type system:** `as X`, `as unknown as X`, non-null `!`, `any`, `@ts-ignore` used to silence the compiler. Each one moves a compile-time error to production. · [12]
2. **`strict` turns on a family of flags** (`noImplicitAny`, `strictNullChecks`, `useUnknownInCatchVariables`, …); `noUncheckedIndexedAccess` is not part of `strict` and adds `undefined` to indexed access. Know which are on before judging a diff; a diff that relies on a disabled flag deserves a note. · [12]
3. **`catch (e)` is `unknown`: narrow before use** (`e instanceof Error`). `(e as Error).message` is a finding. · [12]
4. **Model states as discriminated unions and check exhaustiveness with `never` in the `default` branch,** so a new state fails to compile instead of falling through silently. Optional fields that force `!` usually mean two types should be separated. · [13] · e.g. `switch (order.status)` without `const _x: never = order.status` lets a new `REFUNDED` state slip through.
5. **Truthiness skips valid falsy values:** `if (x)` drops `0` and `""`; use `!= null` when those are valid. `!` does not check anything at runtime. · [13]
6. **One source of truth for types:** schemas shared between client and server (e.g. a validation library generating types) instead of hand-duplicated interfaces. · engineering practice

## 2. React

1. **Rules of Hooks:** call hooks only at the top level of components and custom hooks; never in conditions, loops, nested functions, `try/catch`, after an early return, or inside `useMemo`. The lint plugin catches most; if the project lacks it, read for it manually and propose the plugin. · [14]
2. **You might not need an Effect:** derive values during render instead of `useEffect` + `setState`; put logic caused by a user action in the event handler; reset state on prop change with a `key`; replace chains of effects with render-time computation plus handlers; notify the parent in the same handler; subscribe to external stores with `useSyncExternalStore`. Data fetching in an effect is legitimate but needs cleanup (an `ignore` flag or abort) against races. · [15] · e.g. an effect that POSTs when a "submitted" flag flips belongs in the submit handler.
3. **Components are pure:** props, state and context are read-only; no mutation of pre-existing objects during render; `Date.now()`, `Math.random()` or module counters during render make output unstable (Strict Mode double render exposes this). · [16]
4. **Screen states are explicit values** (empty, loading, error, no permission, offline, confirmation) computed in a view model or hook and testable without the DOM, not scattered `&&` in JSX. · [15] (derive in render); engineering practice
5. **In layered front-ends (MVVM or similar), views do not call services or fetch data directly;** UI strings come from the message catalog; colors and spacing come from design tokens. · engineering practice

## 3. Server frameworks and runtime

1. **Shared instances:** singleton-scoped services (default in many DI frameworks) and module scope in serverless runtimes with concurrency are shared across simultaneous requests; never store per-request data there. · [17], [19]
2. **Central error mapping:** a global filter/handler decides what clients see; handlers throw typed domain errors; no raw message passthrough. · [17], [9]
3. **Authorization at the start of each use case or handler,** not only in middleware that a direct call can bypass (server actions and RPC endpoints are reachable directly). · [8]
4. **Timeouts and cancellation:** outbound calls take an abort signal with a timeout; framework timeout middleware may return an error without cancelling the underlying work. · engineering practice

## 4. SQL and data access

1. **Parameterized queries only;** unsafe raw APIs (`queryRawUnsafe` and similar) with interpolation are blocking. · [8] (injection sink)
2. **Transaction scope:** tenant/role settings with `SET LOCAL` inside the transaction; no network calls inside; keep it short. · [10]
3. **Race-safe invariants:** conditional updates with row-count check, unique constraints, `SELECT … FOR UPDATE` within a short transaction, or SERIALIZABLE with retry on serialization failure. · [11]

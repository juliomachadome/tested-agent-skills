# Mobile and native clients, startup, offline sync

General rules for apps (React Native or similar) and heavy client screens. Platform APIs differ by framework and version; check the docs of the one in use. This file has no vendor-verified numbers; treat figures as starting points to measure.

## Lists

- Unbounded data: paginate on the server with a cap the client cannot raise, then render with a virtualized list component and a stable key per item. A plain scroll container is acceptable only when the design bounds the count.
- Keep row components cheap: no inline heavy work in render, memoize only where a profile shows re-renders, give rows fixed or estimated heights so the list can skip measuring.
- Do not let one state change re-render the whole list: keep selection and per-row state local or keyed.
- Requests for list data run in parallel, not in a cascade of waterfalls.

## Startup

- Define the startup budget as time to the first useful screen on a mid-range device, cold and warm separately.
- Defer everything not needed for the first screen: lazy screens, lazy heavy libraries, deferred analytics initialization, no synchronous storage reads or large JSON parsing on the startup path.
- Each new dependency that runs at module load adds to startup; measure with and without.

## Responsiveness

- Visible feedback to a tap within roughly 100 to 400 ms (animation or state change), even if the work continues; use skeletons shaped like the content.
- Keep heavy work off the UI or JS thread (workers, native modules, chunking); run animations on the thread that is not blocked, using transform and opacity style properties.
- Clean up listeners, timers and subscriptions on unmount; leaks show as memory growth in repeated runs.
- Use correctly sized images and lazy screens; decode and resize on the server or at upload, not on the device.

## Offline and sync

- Treat offline as best effort unless there is proven demand; full offline for per-user paid content is costly and risky.
- Writes made offline are queued with an idempotency key so a replay after reconnect cannot duplicate them.
- Define a conflict rule per entity (last write wins, server wins, merge) and show the user when it applied.
- Sync in small batches with backoff and a ceiling; do not sync large payloads on cellular without consent; stop polling when the state is final.
- Never keep per-user secrets or signed URLs in a cache shared across users of one device.

## Backend calls from clients

Server pagination with a hard maximum, timeouts on every outbound call, bounded request and response sizes, and compression for large JSON responses (a list page of a hundred items can already be tens of KB uncompressed; measure it).

## Sources

- Synthesized from general engineering practice and from project-level performance guides that were read as data on 2026-11-15; no external page fetched for this file (not re-verified).

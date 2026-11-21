# Front-end and mobile observability

Goal: know within minutes that real users are hurting, find the release and route responsible, and connect the browser to the backend trace. Tags: **[F]** read this pass, **[M]** model judgement. Project tooling wins; the examples use Sentry and OpenTelemetry because their docs were read.

## 1. Error tracking
- Upload source maps in the build so stack traces are readable; Sentry recommends doing it in the build, and by default links maps to errors through injected Debug IDs **[F]**. Check that artifacts exist before errors arrive, or traces stay minified **[F]**. Do not serve maps publicly unless you accept exposing source **[M]** (the Sentry page does not discuss this).
- Tag every event with release (git SHA or version) and environment so errors map to a deploy **[M]**.
- Grouping: rely on fingerprints from the stack, then merge or split manually; add custom fingerprints for errors that differ only by message ids.
- Alert noise: drop third-party and extension errors (`ResizeObserver loop`, `Script error.`, browser extensions) with `ignoreErrors` and `denyUrls`; alert on new issues in the latest release and on regressions, not on every event **[M]**. Sampling affects events, not session counts **[F]**.
- Scrub personal data before send (see section 5).

## 2. Real-user monitoring (RUM)
- Use the `web-vitals` library: `onLCP`, `onINP`, `onCLS` each fire when the value is ready; INP is not reported if the user never interacts, and CLS/INP can fire again when the page is hidden **[F]**. Use the `attribution` build to see which element or interaction caused it **[F]**.
- Send with `navigator.sendBeacon` and flush on `visibilitychange` to `hidden`, not `unload` **[F]**. Deduplicate with the metric `id`; a back/forward cache restore gives a new id **[F]**. Use the supplied `rating` rather than hand-copied thresholds **[F]**.
- Report the 75th percentile, split by route template (not raw URL), device class, connection and release **[M]**; the web-vitals page did not state p75, the pass threshold is in `core-web-vitals.md`.
- Sampling: send 100% at low traffic, then sample by session (not by event) so one session keeps all its metrics; document the rate so counts can be rescaled **[M]**.
- Field data beats lab data for decisions; lab runs explain why (`diagnosis-playbook.md`).

## 3. Release health and crash-free sessions
Sentry release health tracks adoption, crash-free sessions (share of sessions not ended by a crash) and crash-free users per release **[F]**. JavaScript apps create one session per page load and per SPA navigation **[F]**. Adoption uses the last 24 hours of sessions; mobile stages mark a release adopted at 10% of sessions **[F]**. Use it as the rollout gate: ship to a small share, compare crash-free rate against the previous release, roll back or stop the ramp if it drops **[M]**. Sessions are recorded without sampling or quota, so rates stay reliable when events are sampled **[F]**. For incident steps see `skills/cloud-deploy-ops/references/incident-response.md`.

## 4. Session replay
Replay shows what the user did before an error. Sentry's defaults mask all text and all input values and block media (`maskAllText`, `maskAllInputs`, `blockAllMedia`); turning them off is advised only for sites with no sensitive data **[F]**. Mark sensitive areas with `mask` or `block` selectors; use `unmask` sparingly; `beforeAddRecordingEvent` can drop console and network data **[F]**. Network bodies are opt-in, and the safest route is not to add endpoints that carry personal data **[F]**. Replay is personal data processing: it needs a lawful basis, consent where the banner rules require it, a retention limit and a notice. See the privacy law of the data subject's country (official regulator pages). Sample replays (for example 10% of sessions, 100% on error) to control cost **[M]**.

## 5. Logs and traces correlation
Put the trace ID in the browser so a user report leads to the backend request. OpenTelemetry browser instrumentation is labelled experimental and mostly unspecified, so expect API changes **[F]**. The documented pattern: the server renders a `traceparent` meta tag per request (version, trace ID, parent span ID, sampled flag) and the browser links its document-load span to it, using W3C Trace Context and Baggage **[F]**. For fetch calls to your API, send `traceparent` as well (cross-origin calls need the header allowed in CORS; the OTel page does not cover CORS, so test it) **[M]**. Log the trace ID with every server log line, show a short request ID in error screens so support can quote it, and attach it to Sentry events as a tag. Backend side: `skills/engineering-playbook/references/reliability-ops.md` (observability).

## 6. Mobile notes
Crash reporting needs symbol files (dSYM, ProGuard/R8 mappings, Hermes source maps) uploaded in CI, tagged with app version and build number. Track crash-free sessions and users per version, ANR and hangs, cold start time and app size. Staged rollout on the store plus a remote kill switch is the mobile equivalent of rollback, because users update slowly. Offline queues hide errors; log sync failures. Details in `skills/mobile-app-engineering` and `clients-mobile-offline.md`.

## 7. Dashboards and alerts that matter
Page on symptoms users feel, not on causes **[F]**. Four golden signals (latency, traffic, errors, saturation) apply to the client too: page load and INP percentiles, request volume, JavaScript error rate and failed API calls, and device memory or main-thread long tasks as saturation **[F, adapted]**. Every page must be urgent, actionable and user-visible; remove alerts that can be ignored, and send non-urgent items to a dashboard because email is ignored **[F]**.

Starter set **[M]**: (1) crash-free sessions below the previous release minus a margin, (2) new issue in latest release above N users, (3) p75 LCP or INP regressing on top routes for 2 days, (4) API failure rate from the browser above baseline, (5) error rate for checkout or login. One dashboard: vitals by route and release, errors by release, adoption, top issues by users affected.

## Sources
Sentry release health, source maps and session replay privacy docs; OpenTelemetry browser getting started; GoogleChrome/web-vitals README; Google SRE *Monitoring Distributed Systems*. Status in `BIBLIOGRAPHY.md`.

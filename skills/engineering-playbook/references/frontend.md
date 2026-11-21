# Frontend & Mobile (React, Next.js, React Native/Expo)

## 1. State architecture

- **Server state** (data from APIs) ≠ **client state** (UI: modals, form drafts, selections). Use a server-state library (**TanStack Query**, SWR, RTK Query) for caching, dedupe, retries, background refetch, invalidation, race handling. Don't copy server data into Redux/Zustand/context.
- Client state: local `useState` first; lift up only as needed; Zustand/Jotai/Redux Toolkit for truly global UI state; URL as state for filters/pagination (shareable, back button works).
- **Derive, don't duplicate:** compute values from state during render instead of syncing with `useEffect`.
- Forms: React Hook Form + zod schema (same schema can validate on server in TS backends); validate on server regardless.

## 2. React correctness & performance

- `useEffect` is for synchronizing with external systems — not for data transformations or event responses ("You might not need an effect").
- Effects that fetch must handle cleanup/abort and stale responses (or use TanStack Query).
- Keys: stable unique ids, never array index for reorderable/dynamic lists.
- Re-render costs: measure with React DevTools Profiler before memoizing. Then: split components, move state down, `memo`, `useMemo`/`useCallback` for expensive computations or referential stability passed to memoized children. React Compiler (where adopted) automates much of this.
- Virtualize long lists (TanStack Virtual, react-window; `FlashList`/`FlatList` tuned in React Native).
- Debounce search input (~200–300 ms); throttle scroll/resize handlers.
- Avoid layout thrashing (reading layout then writing styles in loops).
- Transitions (`useTransition`, `useDeferredValue`) to keep input responsive during heavy updates.
- Error boundaries around risky subtrees; Suspense for loading states.

## 3. Next.js / rendering strategies

- **SSR/RSC** for content and SEO, **SSG/ISR** for mostly static pages, **CSR** for highly interactive authenticated dashboards.
- React Server Components: fetch on the server, send less JS; keep secrets server-side; mark client components minimal (`'use client'` at leaves).
- Server Actions/route handlers are public endpoints — authenticate and authorize them like any API, validate input.
- Caching semantics in Next.js changed across versions — check the version's docs before relying on defaults.

## 4. Web performance (Core Web Vitals)

| Metric | Good | Main levers |
|---|---|---|
| **LCP** (largest contentful paint) | ≤ 2.5 s | fast server/TTFB, CDN, preload hero image, optimized images, avoid render-blocking CSS/JS |
| **INP** (interaction to next paint) | ≤ 200 ms | less JS on main thread, break long tasks, avoid heavy re-renders, web workers |
| **CLS** (cumulative layout shift) | ≤ 0.1 | width/height on media, reserve space for ads/embeds, font loading strategy (`font-display`, size-adjust) |

- Bundle: code split by route, dynamic `import()` for heavy components, tree-shake (ESM imports, avoid barrel files importing everything), analyze (`@next/bundle-analyzer`, `vite-bundle-visualizer`), replace heavy libs (moment → date-fns/Temporal; lodash → per-function or native).
- Images: `next/image` or responsive `srcset`, AVIF/WebP, lazy below the fold, CDN.
- Fonts: self-host, subset, preload critical.
- HTTP: compression (Brotli), caching with hashed filenames + long `max-age, immutable`, HTTP/2+.
- Measure real users (RUM: `web-vitals` library, Vercel/App Insights) plus Lighthouse in CI.

## 5. Accessibility (WCAG 2.2 AA)

- Semantic HTML first (`button`, `a`, `label`, headings in order, landmarks); ARIA only when no native element fits ("no ARIA is better than bad ARIA").
- Keyboard: everything operable via keyboard, visible focus, logical tab order, focus management in modals/route changes, no keyboard traps.
- Contrast ≥ 4.5:1 normal text, 3:1 large text and UI components; don't convey info by color alone.
- Labels for every input; error messages associated (`aria-describedby`); announce async changes (`aria-live`).
- Alt text for meaningful images, empty alt for decorative.
- Respect `prefers-reduced-motion`; target sizes adequate (WCAG 2.2: at least 24×24 CSS px).
- React Native: `accessibilityLabel`, `accessibilityRole`, test with VoiceOver/TalkBack; dynamic font sizes.
- Test: axe (jest-axe, @axe-core/playwright), Lighthouse, manual screen reader pass.
- Legal: the **European Accessibility Act** applies since 28 June 2025 to many consumer digital services (e-commerce, banking) in the EU — see compliance-eu.md.

## 6. Security in the client

- Anything in the bundle is public. No secrets in `NEXT_PUBLIC_*`/`EXPO_PUBLIC_*`.
- Avoid `dangerouslySetInnerHTML` with untrusted content (sanitize with DOMPurify).
- Tokens: prefer HttpOnly cookies/BFF on web; secure storage on mobile.
- CSP headers; validate redirects; don't trust client-side checks for authorization.

## 7. React Native / Expo

- Performance: `FlashList` for long lists; avoid anonymous functions/inline objects in hot list items; memoize row components; images cached and sized (`expo-image`); keep JS thread free (move heavy work native or to background); Hermes engine; Reanimated for animations on the UI thread.
- **Offline-first:** local DB (SQLite/WatermelonDB/MMKV for small kv), optimistic updates, sync queue with idempotent mutations, conflict resolution strategy (last-write-wins vs merge), retry on reconnect (NetInfo).
- Networking: timeouts, retries with backoff, handle flaky connectivity; TanStack Query works in RN with `onlineManager`.
- **OTA updates** (EAS Update): only JS/assets; native changes need a store build; use runtime versions/channels; staged rollouts; rollback plan.
- Push notifications: request permission in context; handle tokens per device; server-side fan-out via provider (Expo push, FCM/APNs); deep links on tap.
- Deep links / universal links; validate parameters.
- App store review rules (in-app purchases for digital goods, privacy labels/data safety forms, account deletion requirement).
- Crash and performance monitoring (Sentry, Expo Insights/observability).
- Secure storage for tokens (`expo-secure-store`), certificate pinning only if you can manage rotation.

## 8. UX fundamentals for developers

- Loading, empty, error and partial states for every data view; skeletons over spinners for content.
- Optimistic UI for fast feedback with rollback on failure.
- Prevent double submits (disable while pending + server idempotency).
- Clear error messages with next action; preserve user input on errors.
- Consistent spacing/typography scale; design tokens; component library (shadcn/ui, Radix primitives, MUI) instead of ad-hoc styles.

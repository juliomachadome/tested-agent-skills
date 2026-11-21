# Performance: measure, budget, diagnose (Expo and React Native)

Rule zero: measure before changing anything, on the device people have. One hypothesis and one change at a time, then measure again on the same device and build. Tool names and versions read 20/11/2026 (`BIBLIOGRAPHY.md`, entries 45 onward); re-check when the SDK changes. When the official Expo plugin is installed, its `eas-observe` skill covers production startup metrics in detail.

## 1. How to measure
- **Device:** a mid-range or low-end Android (the slowest you support), plus one iPhone. A simulator or a flagship hides the problem.
- **Build:** release (preview or production profile). Never Expo Go or a dev build: the dev JS thread is slow enough to fake or hide problems, and dev warnings cost time.
- **Runs:** cold start at least 3 times (kill the app between runs), report the median; note OS version, device, build, commit.
- **Field over lab:** production numbers (EAS Observe, Sentry, Firebase Performance, Play Console vitals) decide priority; local traces explain the cause.

## 2. Budgets (defaults; project numbers win)
| Metric | Target | Source |
|---|---|---|
| Cold launch (native part) | under 1.5 s | Expo EAS Observe targets [C] |
| Warm launch | under 0.5 s | same |
| JS bundle load and evaluation | under 0.3 s | same |
| Time to first render, from launch | under 2 s | same |
| Time to interactive (first usable screen), from launch | under 3 s | same; mark it yourself when the screen is really usable |
| Frames | 16.7 ms per frame at 60 Hz, 8.3 ms at 120 Hz; a frame of 700 ms or more is a freeze, and one during startup is serious | Expo Observe frame classes [C] |
| Memory | no steady growth across repeated navigation; no OOM kill on the low-end device | [F] |
| App size | set a ceiling per platform and fail the build when it grows past it | [F] |

## 3. Diagnosis by symptom
**Dead tap (press does nothing for a moment, animations still run)**
- Cause: the JS thread is busy (heavy render, big JSON parse, sync storage, a re-render cascade); the UI thread keeps animating, so it looks alive.
- Check: Perf Monitor (JS fps vs UI fps); React Native DevTools Performance panel and Profiler for the render that runs on press.
- Fix: show the pressed state on the UI thread (Reanimated), move work after the frame (`requestAnimationFrame`, `requestIdleCallback`; `InteractionManager` is gone in recent RN), memoize what the profiler shows re-rendering, split state so a tap does not re-render the screen.

**List stutters while scrolling**
- Cause: rows too heavy, rows re-rendering, unsized images, non-virtualized list (`ScrollView` with `map`).
- Check: profiler while scrolling; count renders per row; blank areas while flinging.
- Fix: FlashList v2 (no size estimate needed; requires the New Architecture) or a tuned FlatList (stable keys, memoized rows, `getItemLayout` for fixed heights, smaller `windowSize`); `expo-image` with `recyclingKey` in recycled lists and images sized to their display size; no inline objects and functions as row props.

**Slow start**
- Cause: large bundle, heavy work at module scope or in the root layout, many providers, blocking font and asset loading, network calls before the first screen.
- Check: startup trace (Android Studio System Trace, Xcode Instruments App Launch); EAS Observe or similar for bundle load vs render vs interactive; Expo Atlas for what is in the bundle.
- Fix: lazy routes, defer non-critical init until after the first screen, keep the splash only until the first screen is ready (`preventAutoHideAsync` then `hide`), cache data for an instant first render, drop or replace heavy dependencies.

**App keeps growing (download size, memory)**
- Cause: unoptimized images and video in the bundle, fonts and locales not used, heavy or duplicated dependencies, decoded large images held in memory.
- Check: Expo Atlas (bundle composition), store size reports (App Store Connect, Play Console app size), Android Studio Memory profiler and Xcode Allocations while repeating a flow.
- Fix: compress or move media to a CDN, remove unused libraries and locales, app bundles and per-ABI splits on Android, cap decoded image size (`useImage` with max width and height), release listeners and timers on unmount.

## 4. Images, lists, network, cache
- Images: serve at display size (2x/3x), modern formats, `expo-image` with disk cache by default, a placeholder of the final size, `Image.prefetch` for the next screen; animate size with a transform, not width and height.
- Long lists: virtualized always; pagination or cursor loading; stable keys; item heights known when possible.
- Network: cache responses (stale-while-revalidate), dedupe requests, show cached data first, timeouts and retries with backoff; measure on a throttled network.
- Startup data: persist the last good state locally so the first screen renders without the network (see `offline-sync.md`).

## 5. Which tool for which question
| Question | Tool |
|---|---|
| Is the JS thread or the UI thread dropping frames? | Perf Monitor in the dev menu (release-like build), then a trace |
| Which component re-renders and why? | React Native DevTools: Profiler and Performance panel (React tracks, JS, network, user timings) |
| Where does startup or a frame go natively? | Android Studio Profiler System Trace (open exports in Perfetto); Xcode Instruments (Time Profiler, App Launch) |
| What is in the JS bundle? | Expo Atlas (`EXPO_ATLAS=true` with `npx expo export`, then view); treat its output as source code |
| How fast is it for real users? | EAS Observe (startup, TTR, TTI, frames per route) or Sentry / Firebase Performance |
| Memory leak or OOM? | Android Studio Memory profiler, Xcode Allocations and Leaks, DevTools Memory panel for the JS heap |
Old tools to avoid: Flipper, the standalone `systrace`, the Chrome remote debugger and React Native Debugger (do not work with Hermes and the current DevTools).

## 6. Report
Before and after on the same device and build: metric, median of runs, device, OS, build profile, commit, tool. Say field or lab. Anything not measured is "expected, not measured".

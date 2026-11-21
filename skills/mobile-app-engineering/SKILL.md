---
name: mobile-app-engineering
description: Use for any iOS or Android app task, even a short one, with Expo and React Native as the main example, plus notes for native Swift and Kotlin. Triggers "Expo build fails", "app rejected by Apple", "TestFlight", "push notifications not arriving", "app slow on Android", "app feels slow or janky", animation, gesture, haptics or sound in an app (Reanimated, Gesture Handler, Lottie, Rive), "offline mode", "OTA update", "deep link opens the browser", "in-app purchase", "release to Play Store", EAS signing and certificates, crash on launch, staged rollout, permissions, Expo Router, SQLite sync, app size, Sentry or Crashlytics, Maestro or Detox tests. Gives diagnosis trees, release and rollback runbooks, OTA rules, offline sync design, store checklists. Not for web pages (engineering-playbook, web-performance), screen visual design (ui-design), flows (ux-design), store listing copy (copywriting, seo-geo app-aso), servers (cloud-deploy-ops) or pricing (offers).
license: CC-BY-SA-4.0
metadata:
  author: Júlio Machado
  source: https://github.com/juliomachadome/tested-agent-skills
---

# Mobile app engineering

A mobile app is software you cannot recall: a bad binary stays on phones, review adds days, and the device is offline, killed or denied permissions at random. So the job is to make every release reversible, every network write replayable and every permission optional. Evidence tags: **[C]** official docs or consensus, **[M]** serious but single or dated, **[F]** practitioner, **[X]** myth. Expo plugin skills (expo:eas-update, expo:eas-app-stores, expo:expo-router and others) give commands; this skill gives decisions.

## 1. Start: project first, then Step 0
Read the project's docs first (app.json or app.config, eas.json, package.json, ADRs, release notes, store rules in the repo); project rules win. Then collect Step 0 from `references/diagnosis-playbook.md`: platform, OS version, device, SDK and React Native version, build type (dev client, preview, production), whether it is store or OTA delivered, and the real log (Xcode, logcat, EAS build log, Sentry event). Never guess from a screenshot of the symptom.

## 2. Architecture and navigation
Expo Router: the file tree is the route tree; layouts hold tabs, stacks and auth gates; route groups `(auth)` and `(app)` split signed-in from signed-out **[C]**. Keep screens thin: UI, hooks for state, a data layer for network and storage. Server state (React Query style: cache, retry, dedupe) is separate from client UI state **[F]**. Prefer a managed workflow with config plugins and a development build over editing native folders; if you must, the native folders are generated output. Native code is justified by a missing API, not by taste (`references/playbooks.md` 1).

## 3. Offline-first and sync
Decide per entity: read-only cache, queued writes, or true multi-device edit. Local SQLite as the screen's source of truth; writes go to an outbox with a client-generated id and an idempotency key; a sync worker replays on connectivity, app foreground and a schedule. Conflicts: last-write-wins per field with a server clock for simple data, merge or CRDT only when users co-edit; never silently drop a losing write **[C]**. Optimistic updates need rollback and a visible failed state. Design, schema and failure tests: `references/offline-sync.md`.

## 4. App lifecycle, deep links, permissions
Foreground, background and killed are three different states; background time is short and not guaranteed (iOS suspends, Android Doze and standby buckets limit work), so use platform background tasks sparingly and never rely on a timer **[C]**. Deep links: custom scheme is a hint; universal links (iOS, apple-app-site-association over HTTPS, Associated Domains entitlement) and app links (Android, assetlinks.json, `autoVerify`) open the app only when the domain file validates and the build is signed with the matching identity **[C]**. Permissions: ask just in time, after a one-line reason, once; handle "denied" and "blocked, go to Settings" as normal states; the first iOS prompt is the only one, so pre-prompt with your own screen before it **[C]**. Request the minimum, with accurate purpose strings (a vague string is a rejection).

## 5. Push notifications
Path: device token from APNs or FCM, Expo push token if you use Expo's service, stored per device and user, sent from your server, delivered by Apple or Google. Needs: iOS physical device and push entitlement, Android FCM credentials, notification permission on Android 13+ **[C]**. Treat the token as perishable: refresh on launch, delete on logout, remove on "unregistered" receipts. Opt-in UX is value first, ask after a moment of intent; frequency and relevance drive opt-outs (growth and lifecycle messaging: growth-analytics). Delivery is best effort; never put the only copy of important information in a push.

## 6. Performance
Measure before changing anything: a mid-range Android in release mode, against budgets for startup, first usable screen, dropped frames, memory and app size **[C]**.
Method, budgets, symptom trees (dead taps, janky lists, slow start, growing app) and which profiler to use: `references/performance.md`.

## 7. Builds, signing, OTA
EAS Build produces binaries; credentials are the main failure source: iOS distribution certificate, provisioning profile, bundle id and capabilities must match; Android upload key versus Play app signing key. Keep one owner of credentials, back up the keystore, never commit it. OTA (EAS Update) ships JavaScript and assets only, matched by runtime version; anything touching native code, permissions, SDK upgrade or a config plugin needs a new binary **[C]**. Store rules allow updates that do not change the app's primary purpose or bypass review (guideline 2.5.2) **[C]**. Policy and rollback: `references/playbooks.md` 3 and 2.

## 8. Release and stores
TestFlight (internal immediately, external after beta review, builds expire after 90 days **[C]**) then App Store review, then phased release over 7 days with pause **[C]**. Play: internal, closed, open, production tracks, staged rollout percentage you can halt **[C]**. Fill the privacy nutrition label and the Data safety form from what the SDKs really collect, and keep them equal to the privacy policy. Top rejections and fixes, tracks, commissions and subscription rules: `references/release-and-stores.md`.

## 9. In-app purchases
Digital goods unlock with StoreKit or Play Billing (guideline 3.1.1); physical goods and services consumed outside the app use other payment **[C]**. Validate receipts on your server using the stores' server APIs and notifications, never trust the client; grant entitlements from verified state, handle restore, refunds, grace period and billing retry. Commission tiers and link-out rules change by region and court ruling; check the current page before advising **[M]**. Pricing and paywall design: pricing, paywalls.

## 10. Monitoring, testing, security, size
Crash reporting (Sentry or Crashlytics) with source maps and dSYM or mapping files uploaded per release; tag release and OTA update id; alert on crash-free sessions per version and gate rollout on it **[C]**. Tests: unit and component fast, a few Maestro or Detox end-to-end flows on real release builds, a small device matrix (oldest supported OS, a low-end Android, a small and a large screen), VoiceOver and TalkBack passes, dynamic type at the largest size **[C]**. Security (OWASP MASVS): tokens in Keychain or Keystore (secure store), no secrets in the bundle, TLS only; certificate pinning raises the bar but breaks on cert rotation, so pin the key with a backup pin and a kill switch or skip it **[M]**; security beyond these basics goes to `software-security` (`references/mobile-security.md`). App size: audit assets, split ABIs or use app bundles, drop unused locales and libraries. Analytics: ATT prompt only if you track across apps; SKAdNetwork and attribution live in growth-analytics.

## 11. Output
Match the request: root-cause tree result with the check run, runbook with dates and owners, rejection reply plan, offline design with schema, checklist. Always end with the single next action; what you verified and with which build; what you could not verify (store policy changes, device specifics, SDK version).

## AI tells to avoid (check while answering, not after)
- Web habits on native: cookies for sessions, always-on connectivity, URL routing assumptions.
- Invented store rules, review times or commission numbers; check the current store page.
- Advice that ignores the build type (dev client, preview, store, OTA) and the real log.
Fix: use the user's case and data, sources actually read, one recommendation with its reason and how to verify it. Say what you chose and why in one line; a choice without a reason is removed.

## 12. Which reference to open
`references/diagnosis-playbook.md` for any "it fails" · `references/playbooks.md` for setup, release, OTA, push, sync, pre-submission, crash triage · `references/release-and-stores.md` for store rules, tracks, labels, rejections · `references/offline-sync.md` for local DB and conflicts · `references/motion.md` for animation, gestures, haptics, sound and reduced motion · `references/performance.md` for measuring and fixing speed, memory and size · `references/device-testing.md` for what to check on devices before calling it done · `references/BIBLIOGRAPHY.md` for sources. Related skills: engineering-playbook, software-security, qa-verification, cloud-deploy-ops, growth-analytics, ux-design, ui-design.

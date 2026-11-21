# Playbooks

Checklists and runbooks. Tags: **[C]** official or consensus, **[F]** practitioner. Replace example numbers with your own data.

## 1. New app setup checklist
1. Pick the workflow: Expo managed with a development build and config plugins; add native code only through a module or plugin, never a one-off edit in generated folders.
2. Create the project with Expo Router; groups `(auth)` and `(app)`; a typed route helper; one root layout for providers, splash and error boundary.
3. Data layer: one HTTP client, one query cache, one local database (expo-sqlite) behind a repository interface. Secrets: secure store for tokens, none in the bundle.
4. Environments: development, preview, production with separate bundle ids or suffixes, separate push credentials and API URLs; `eas.json` profiles for each.
5. Identity: bundle id and package name chosen once (cannot change after release), app icon, privacy policy URL, support URL.
6. Observability on day one: Sentry or Crashlytics with source maps upload, release and update id tags.
7. CI: lint, types, unit tests, then an EAS build per branch or tag; Maestro smoke flow on the preview build.
8. Accessibility baseline: labels on touchables, roles, minimum touch targets, text that scales.
9. Store accounts and credentials: Apple Developer Program, Play Console, one owner plus a recovery path, keystore backed up in a password manager.
10. Define "done": release-notes template and the pre-submission checklist (section 6).

## 2. Release runbook with staged rollout and rollback
Roles: release owner, one reviewer, one on-call. Times are examples.
- **T-3 days**: freeze scope; bump version and build number; run full tests; build production binaries; upload to TestFlight internal and Play internal track; smoke test on the device matrix.
- **T-2 days**: submit to App Review with notes and working demo credentials; for Play promote to closed testing or straight to production in a staged rollout draft. Choose manual release on iOS so approval does not equal publication.
- **Day 0 (approved)**: iOS release with phased release on (7 days: 1, 2, 5, 10, 20, 50, 100 percent of automatic updaters **[C]** per Apple's phased schedule, check the current page). Play: start at 1-5 percent.
- **Watch gates** at each step (every 2-4 hours day 0, then daily): crash-free sessions per version versus the previous version (stop if more than 0.5 point worse, example), ANR rate, error budget for new Sentry issues, support tickets mentioning the version, purchase success rate, push opt-in.
- **Increase**: Play 5 → 20 → 50 → 100 percent when gates hold for 24 hours each. Apple phased release proceeds by day; pause if gates fail (pause up to 30 days **[C]**).
- **Halt**: Play: halt rollout (existing users keep the version); iOS: pause phased release. Neither pulls the version back from installed phones.
- **Rollback**: stores cannot downgrade users. Options in order: (1) server kill switch or feature flag; (2) OTA hotfix if JS-only and within policy (section 3); (3) a new build with a higher version code, fast-tracked with an expedited review request on iOS; (4) remove from sale only for serious harm. Pre-write the flags, so option 1 exists.
- **After**: post a short note with the metrics, close issues, archive the dSYM and mapping files, update the runbook with what was slow.

## 3. OTA policy (EAS Update)
Allowed in the sense of the store rules **[C]**: bug fixes, copy, style, layout and logic in the JavaScript bundle that keep the app's reviewed purpose. Not allowed or not possible: changes to native code, new permissions or capabilities, SDK upgrades, anything that adds a major feature the review never saw, changes that circumvent payment rules or the age rating (guideline 2.5.2; Play's policy on code from outside the store has similar spirit **[C]**).
Rules for the team:
1. One runtime version per native fingerprint; never reuse a runtime version across binaries with different native code.
2. Publish to a preview channel, test on a release build, then to production with a rollout percentage (EAS rollouts) rising by gates as in section 2.
3. Tag the update id in the crash tool; a bad update is rolled back or replaced within the hour.
4. Every OTA message states what changed and its risk; no OTA for a Friday evening unless it is a hotfix.
5. Keep a list of what requires a binary (permission, plugin, SDK, native dependency).
Hotfix decision: JS-only, fix does not add features, crash or data-loss class → OTA to 10 percent, check, 100 percent, then ship the binary through normal review so stores and users converge.

## 4. Push setup
1. Credentials: APNs auth key (p8) and FCM credentials (service account) uploaded to EAS or your provider.
2. Build a development build; push does not work in the Expo Go client for production use **[C]**.
3. Android: create a default notification channel; request POST_NOTIFICATIONS on Android 13+.
4. Permission UX: ask after the user reaches a moment of intent; explain the benefit in one line; if denied, show an in-app switch that links to Settings.
5. Token lifecycle: register on login, upsert by device id, refresh on launch, delete on logout, prune on "unregistered".
6. Server: queue sends, batch, read receipts later, retry with backoff, respect user time zones and quiet hours.
7. Handler: foreground behaviour, tap routing to a deep link, cold-start tap.
8. Test matrix: iOS and Android, foreground, background, killed, battery saver.
9. Measure: opt-in rate, delivery receipts, open rate, opt-out rate after each campaign (lifecycle messaging: growth-analytics).

## 5. Offline sync design
See `offline-sync.md` for the full design. Checklist: entity classification, outbox table, idempotent endpoints, conflict rule per entity, server clock or version, tombstones for deletes, initial and incremental pull with a cursor, schema migration tests, failure tests (airplane mode mid-write, kill mid-sync, double submit).

## 6. Pre-submission checklist
- Version and build number incremented; the build is the one tested.
- Privacy policy URL works; account deletion is possible in-app if accounts exist **[C]**; purpose strings clear.
- Privacy nutrition label and Data safety form match SDK behaviour; ATT prompt only when tracking.
- Demo credentials and review notes include steps for hidden or gated features, sandbox purchase path, hardware requirements.
- In-app purchase products approved, restore button present, subscription terms visible near the buy button.
- No placeholder content, broken links, crashes on a clean install of the exact build; works on the smallest and largest supported screens and with dynamic type at largest.
- Third-party login rule satisfied (4.8); user-generated content has report and block (1.2).
- Screenshots and text match the build; ratings answers accurate.
- Target API level and required SDK versions meet the current store requirement (check the current page; numbers change yearly).

## 7. Crash triage
1. Open the top crash by affected users, not by event count.
2. Group by release and OTA update id: new in this version, or old?
3. Confirm symbolication; if unreadable, fix the upload before reading.
4. Reproduce with the breadcrumbs, OS and device; check memory and connectivity state.
5. Decide: halt rollout, kill switch, OTA hotfix, or next release; write the decision with the metric that triggers it.
6. Fix with a regression test (unit or Maestro flow); mark the issue resolved in the release that carries it.
7. Report: users affected, first seen version, status, owner.

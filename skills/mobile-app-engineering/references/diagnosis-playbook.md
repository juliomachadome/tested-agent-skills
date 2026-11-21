# Diagnosis playbook: symptom, likely cause, check, fix

Use top-down. Step 0 first: a fix applied to the wrong build, OS or SDK is noise. Tags: **[C]** official docs or consensus, **[M]** serious but single or dated, **[F]** practitioner. Store policy and SDK behaviour change; re-check the linked page for anything dated.

## Step 0: is the evidence trustworthy?
| Check | How | If it fails |
|---|---|---|
| Platform and OS version | device settings, crash report header | reproduce on that OS or an emulator image of it |
| App version, build number, update id | About screen, Sentry release tag, `eas update:list` | confirm the user runs the build you are reading |
| SDK and React Native version | package.json lockfile, `npx expo-doctor` | align versions before debugging (mismatched native modules are a top cause) |
| Build type | dev client, preview, production; debug vs release | reproduce in a release build; dev mode hides and creates problems |
| Delivery | store binary, TestFlight, Play track, OTA channel and branch | a bug may be in an OTA bundle on an old binary |
| Real log | Xcode device log, `adb logcat`, EAS build log (the first red error, not the last), Sentry event | get it; do not infer from the symptom |
| Device and state | real device vs simulator, fresh install vs upgrade, offline, low storage | reproduce the state, not only the screen |

## 1. Build fails (EAS Build or local)
| Where it fails | Likely cause | Check | Fix |
|---|---|---|---|
| Install dependencies | lockfile or peer conflict, private registry token missing, wrong Node | build log install phase; same Node as local | pin Node in eas.json, commit lockfile, add token as EAS secret |
| Config or prebuild | invalid app.json, a config plugin throws | `npx expo prebuild --clean` locally | fix plugin options; remove plugins one by one |
| iOS signing | no valid distribution certificate, profile lacks a capability or device, bundle id mismatch | `eas credentials`, Apple Developer portal | regenerate profile after adding capability; match bundle id **[C]** |
| iOS compile | pod conflict, Xcode too old for SDK, deployment target | first error in Xcode phase | set the image to the SDK's required Xcode; align deployment target |
| Android Gradle | JDK mismatch, duplicate class, out of memory | Gradle error above the stack | use the SDK's JDK, add exclusions, raise heap in gradle.properties |
| Android signing | wrong keystore or alias, upload key not registered with Play | `eas credentials`, Play Console app signing page | use the registered upload key; if lost, request upload key reset in Play |
| Works locally, fails on EAS | untracked file, env var only on your machine, cached native folders | `git status`, `eas build --clear-cache` | commit the file; move vars to EAS env; ignore native folders consistently |
Worked check: a build that passes locally but fails on EAS in 3 of 3 tries with "no such file" means the file is gitignored; a one-in-five failure is flaky network or cache.

## 2. Crash on launch
1. Release or debug? Crash only in release: missing Hermes source maps hide the line, or minification stripped a class (Android proguard rules), or an env var is undefined.
2. Native symbolication: iOS needs the dSYM, Android the mapping file; upload per release or the stack is unreadable **[C]**.
3. Started after an OTA update: roll back that update (section 7) before reading code; check that the update's runtime version matched the binary.
4. Started after an OS release: check the module's issue tracker; test on the beta image.
5. Only on some devices: memory (large images at launch), 32-bit or old Android WebView, missing Google Play services.
6. Crash before JS runs (no JS stack): native module missing from the build (added after the binary was built), a config plugin not applied, or an entitlement missing. Rebuild the binary.

## 3. App rejected
Step 0 addendum: copy the full message, guideline number, build number and any screenshots Apple attached. Do not resubmit before you know which rule.
| Message | Cause | Fix |
|---|---|---|
| 2.1 App completeness | crash during review, placeholder content, demo account does not work | test the exact build on a clean device; give working credentials and a test path in review notes |
| 2.3 or 4.0 metadata, screenshots | screenshots show features not in the build, or misleading text | align listing with the build (copy: copywriting) |
| 3.1.1 In-App Purchase | digital content unlocked without store billing, or a link to external purchase where not allowed | route digital purchases through StoreKit; remove the link or use an allowed region path |
| 4.8 Login services | third-party login offered without an equivalent privacy-preserving option | add Sign in with Apple or an equivalent option satisfying the rule **[C]** |
| 5.1.1 Data collection | no privacy policy link, no account deletion path, purpose strings vague | add policy URL, in-app account deletion, rewrite purpose strings |
| 5.1.2 and ATT | tracking without prompt or label mismatch | align label, prompt and SDKs; remove the SDK if unneeded |
| 2.5.2 code | downloads code that changes features | restrict OTA to fixes within the reviewed purpose; see `playbooks.md` 3 |
| 4.2 Minimum functionality | a web wrapper with no native value | add real native features, or reconsider the product shape |
Play: policy violation email names the policy; typical causes are Data safety mismatch, a permission without a core use case, a missing privacy policy, or an unsafe target API level **[C]**. Reply in the console with what changed, one change set per appeal.

## 4. Push notifications not arriving
| Step | Check | Fix |
|---|---|---|
| Permission | iOS Settings, Android 13+ POST_NOTIFICATIONS granted, channel not muted | prompt flow; deep link to Settings |
| Token | token stored for this device, not stale, right environment (APNs sandbox vs production) | refresh on launch; separate dev and prod tokens |
| Credentials | APNs key or FCM credentials uploaded for the right bundle id and project | re-upload; for Expo, `eas credentials` |
| Device | physical iOS device, not simulator; Android has Google Play services | test on a real device |
| Send result | Expo push ticket then receipt (`DeviceNotRegistered`, `MessageRateExceeded`); FCM or APNs response | read the receipt, delete dead tokens |
| Payload | iOS silent push needs `content-available` and background mode, is throttled; Android data vs notification message | match payload type to intent |
| Device state | battery saver, background restrictions, force-stopped Android app, iOS Focus | tell users; never rely on delivery for critical paths |
| Foreground | no banner while the app is open unless a handler shows it | set the notification handler |
Delivery is best effort **[C]**; measure sent, delivered receipts and opened separately.

## 5. Slow lists and app slow on Android
| Symptom | Cause | Check | Fix |
|---|---|---|---|
| Janky scroll | heavy row render, inline functions and objects, images unsized | Perf monitor: JS fps vs UI fps; React profiler | memoize rows, stable keys, FlashList, fixed `getItemLayout`, smaller `windowSize` |
| Blank areas while scrolling | rows too heavy or batch too small | measure render time per row | lighter rows; raise `maxToRenderPerBatch` only with data |
| Tap lag, animation fine | JS thread busy | JS fps drops | move computation off render; defer with interactions API; batch state updates |
| Animation stutters | animating on JS thread | UI fps drops | Reanimated worklets, native driver |
| Slow only on low-end Android | memory, large JSON, big images, dev mode | profile release build on that device | paginate, resize, cache; verify Hermes enabled |
| Slow start | huge bundle, work in root layout, many providers, blocking fonts | startup trace; bundle visualizer | lazy routes, defer non-critical init, keep splash until first screen ready |
Worked number: a 60 fps budget is 16.7 ms per frame; a row render of 8 ms with 4 rows entering per frame already misses the budget **[F]**.

## 6. Offline data loss
| Symptom | Cause | Check | Fix |
|---|---|---|---|
| Edits vanish after reconnect | server response overwrites local pending edit | log of local writes vs pull order | outbox first, then pull; apply remote only to rows without pending local ops |
| Duplicates after retry | no idempotency key | server table for repeated client ids | client-generated id, unique constraint, idempotent endpoint |
| Data gone after update | schema migration dropped table, or wrong storage location cleared by OS | migration code, app data path | versioned migrations that copy, test upgrade from oldest version |
| Lost on logout or reinstall | outbox not flushed | outbox length at logout | block logout with pending ops, warn user |
| Silent failures | catch-and-ignore on sync | error telemetry | surface a failed state and retry count |
Full design: `offline-sync.md`.

## 7. OTA update not applied
1. Runtime version: update and binary must match; a new binary with a different runtime version never receives the old update **[C]**.
2. Channel and branch: the build's channel points to the branch you published to (`eas channel:view`).
3. Platform: you published both iOS and Android?
4. Check strategy: updates download on launch and apply on the next launch by default; test with two cold starts.
5. Code signing or fingerprint mismatch, or the app was built before updates were enabled.
6. Disabled in dev client or debug build.
7. Rollback needed: republish the last good update to the channel or roll back through the EAS dashboard, then fix forward.

## 8. Deep link opens the browser
| Platform | Cause | Check | Fix |
|---|---|---|---|
| iOS | apple-app-site-association missing, wrong content type, redirects, wrong appID or paths; entitlement not in build; link typed in Safari bar or tapped within same domain | open the file URL, check team id plus bundle id; Notes app tap test | serve over HTTPS without redirect, fix paths, rebuild with the entitlement **[C]** |
| Android | assetlinks.json missing or wrong SHA-256, `autoVerify` not set, Play app signing certificate not the one listed | `adb shell pm get-app-links <package>` | list the Play signing SHA-256 as well as upload key; reinstall to re-verify **[C]** |
| Both | Expo Router route missing or auth gate swallows the link | open the URL with `npx uri-scheme` or simulator command | handle the initial URL after auth; test cold and warm start |
Social apps open links in an in-app browser; the fix is a landing page with an "open in app" action, not code.

## 9. In-app purchase not completing
| Symptom | Cause | Fix |
|---|---|---|
| Product not found | product not approved or in wrong status, bundle id mismatch, agreements unsigned, Play app not published to a test track | complete agreements and product setup; wait for propagation |
| Sandbox purchase works, production fails | different environment for validation | try production verification then sandbox, or use the transaction API environment field |
| Paid but no entitlement | client-only unlock, webhook missed | server verifies via store notifications and reconciles on launch |
| Pending purchases (Play) | not acknowledged within 3 days gets refunded | acknowledge after granting **[C]** |
| Restore fails | no restore path, or account differs | add restore button and server link of purchase to user |
| Refund not honoured | ignoring refund notifications | handle refund and revoke events |

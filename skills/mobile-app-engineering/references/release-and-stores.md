# Release and stores

Store rules change often. Everything here is a structure to check against the current pages in `BIBLIOGRAPHY.md`; items tagged **[unverified]** were not read this pass.

## 1. Apple path
1. Developer Program account, App Store Connect record, bundle id, certificates and profiles (EAS can manage them).
2. Upload a build (EAS Submit, Xcode, Transporter); wait for processing; export compliance answers.
3. TestFlight: internal testers (team members) get builds quickly; external testers need beta app review for the first build of a version; builds expire after 90 days **[C]**.
4. Version page: screenshots, text, privacy label, age rating, review notes, demo account, release option (manual, automatic, scheduled); phased release over 7 days with pause up to 30 days **[C]**.
5. Review: usually hours to a couple of days **[unverified timing]**; a rejection names a guideline; reply in Resolution Center or fix and resubmit; use an appeal if you believe the rule is misapplied; expedited review is requested for critical fixes.

## 2. Google Play path
1. Developer account, app record, Play app signing enrolled (Google holds the app signing key; you keep an upload key).
2. Tracks: internal testing (fast, up to a small tester list), closed testing, open testing, production **[C]**. New personal accounts may be required to run a closed test with a minimum number of testers for a minimum number of days before production **[unverified, check the current requirement]**.
3. Releases: upload an app bundle (AAB), release notes, a staged rollout percentage; you can raise, halt and resume; countries can be limited at start **[C]**.
4. Declarations: Data safety form, content rating, target audience, ads, permissions that need a declaration (background location, SMS, all files), financial or health declarations when relevant.
5. Review times vary; first submissions and sensitive permissions take longest **[unverified]**.

## 3. Privacy labels and Data safety
- List every data type any SDK collects (analytics, crash, ads, attribution, push token), whether it is linked to identity, used for tracking, and its purpose. Read each SDK's privacy documentation and its privacy manifest.
- Keep three things equal: the label or form, the privacy policy, the actual network traffic (check with a proxy on a clean install).
- Change with every SDK change; a mismatch is a common rejection and takedown cause **[C]**.
- Legal basis, consent and deletion rights: the privacy law of the data subject's country (official regulator pages). Apple requires an in-app way to initiate account deletion for apps with account creation **[C]**; Play requires a deletion path and a web link for it **[unverified detail]**.
- ATT: required only to track users across other companies' apps and sites; if you do not, do not prompt. Attribution after ATT uses SKAdNetwork or AdAttributionKit aggregate postbacks; planning and measurement: growth-analytics.

## 4. Common rejections and fixes (quick table)
| Cause | Fix |
|---|---|
| Crash or bug during review (2.1) | test the exact build on a clean device on cellular and wifi; stage backend; working demo account |
| Incomplete metadata or screenshots not matching | match the build; no other platform names in text |
| Purchases outside store billing (3.1.1) | StoreKit for digital goods; remove purchase links where disallowed |
| Subscriptions unclear | show price, period, renewal and cancellation near the button; offer restore |
| Missing login alternative (4.8) | add an equivalent option |
| Privacy policy or label mismatch (5.1.1) | align, add policy link, add deletion |
| Permission purpose vague | one honest sentence per permission, specific to the feature |
| Web wrapper (4.2) | add native functionality or remove the app |
| User generated content without moderation (1.2) | report, block, filter, contact |
| Play: permission or API not justified | remove or submit declaration with video and use case |
| Play: target API too old | raise target SDK and test the behaviour changes |
Reply discipline: quote the guideline, say what changed, attach evidence, one reply per submission; never argue tone.

## 5. Commissions and subscriptions
- Digital goods inside the app use store billing; stores take a share (a standard rate and a reduced rate for small developers and for subscription renewals after the first year) **[M; verify current rates on the store pages]**.
- External purchase links and alternative billing differ by country and by court or regulator decisions (US, EU, Korea, Japan); a feature that is allowed in one region may be rejected in another. Check the current guideline text and the region **[M]**.
- Subscriptions: product groups, trial and intro offers, grace period and billing retry, upgrade, downgrade and crossgrade rules, refunds. Your server stores the entitlement keyed to your user id and updates from the stores' notifications.
- Server security: verify purchases server-side with signed transaction data (App Store Server API) and Play Developer API purchase tokens; reject replay by checking the transaction id was not seen for another user; never ship the verification secret in the app; rate-limit the endpoint. Web security details: software-security.
- Paywall copy and tests: paywalls, pricing, copywriting.

## 6. Versioning and cadence
Semantic version for people, monotonic build number for stores; keep native version and runtime version rules in one document. Ship small and often: smaller diffs, faster review, easier rollback. Keep a list of "needs a binary" changes so web-like deployment instincts do not leak into the app.

## 7. Size and startup budgets
Track download size per release; on Android use app bundles, ABI splits and compressed assets, remove unused libraries and locales; on iOS audit asset catalogs and on-demand resources. Set a regression threshold in CI (for example fail if the bundle grows more than 5 percent without a note) **[F]**.

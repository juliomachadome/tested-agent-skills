# Business logic, race conditions, payments and webhooks

Format: **rule** · why · source id (see `sources.md`) · example.

Business-logic flaws pass every input validator and every scanner: each request is well-formed, the sequence or the volume is the attack. Test them by writing abuse cases next to use cases.

## 1. Abuse-case classes (test each one that applies)

The OWASP testing guide groups them as WSTG-BUSL-01 data validation, 02 forged requests, 03 integrity checks, 04 process timing, 05 function-use limits, 06 workflow circumvention, 07 defenses against misuse, 08/09 unexpected and malicious file uploads, 10 payment functionality. · W16

1. **Trusting client values.** Price, discount, quantity, role, tenant or "isPaid" in a body or hidden field. Recompute from server data. · W16 (BUSL-02, 03), W15 · e.g. a `discount: 100` field accepted by the cart endpoint.
2. **Race (TOCTOU): two requests pass the same check.** Double spend, coupon reused twice, last item sold twice, two approvals of the same document. Make check-and-change one atomic statement and require one affected row; use a unique constraint for uniqueness invariants; row lock (`SELECT ... FOR UPDATE`) inside a short transaction when a multi-step decision needs it; or SERIALIZABLE with retry on serialization failure. · W16 (BUSL-04), W28 · e.g. `UPDATE stock SET qty = qty - 1 WHERE id = $1 AND qty > 0` and check `rowCount = 1`.
3. **Replay.** A valid request or one-time credential reused for profit. Accept each authorization credential once: atomically check unused and mark used, in state shared by every server. Expiry alone does not stop replay within the window. · W15
4. **State machine out of order.** Skip payment, approve your own request, edit after final approval. Transition with `UPDATE ... WHERE status = <expected origin>` and check the row count; the server never trusts the state the client claims. · W16 (BUSL-06), W3 V2 (2.3.1)
5. **Partial completion.** A business transaction that writes several tables must commit or roll back as a whole. · W3 V2 (2.3.3)
6. **Unlimited use of a function.** Free trial created repeatedly, referral credit farmed with fake accounts, codes requested in a loop, expensive AI or GPU job triggered at will. Limit per account, per device signal and per flow. · W16 (BUSL-05), W2a
7. **Automation of a sensitive flow (API6).** Scalping, seat hoarding, referral abuse. Identify which flows hurt the business if over-used, then add controls proportional to the harm: per-account quotas, behavior that is faster than a human, CAPTCHA after signals, stricter rules for machine-facing APIs. · W2a
8. **What You See Is What You Sign.** For a high-value confirmation (transfer, payout change), the user confirms the significant data (target, amount), and the server binds the confirmation to exactly that data so it cannot be swapped between steps. · W15

Idempotency prevents duplicates of one operation; it does not replace concurrency control between two distinct actors. · engineering judgment based on W28, W39

## 2. Payment rules (provider-neutral, Stripe examples)

1. **Price on the server; access granted only by a verified event or an API lookup, never by the success redirect.** The user may close the tab before the redirect; redirect-based methods (bank redirects, app approvals) often never return. · W38
2. **Use low-risk integrations** (hosted checkout, embedded payment element): card data goes from the browser to the provider and never touches your server. You may store brand, last 4, expiry. · W40
3. **Saved-card charges off-session need a path back for the customer to authenticate** when the bank asks; exemptions are not guaranteed. · W40
4. **Keys:** restricted keys with only the permissions a service uses; live keys never in QA; rotate the live key and the live webhook secret together. · W40, W38

## 3. Webhooks

1. **Verify with the provider's library over the raw body.** For Stripe use only the `t` and `v1` parts of the signature header; ignore `v0` and debug fields (not covered by the HMAC). Do not parse JSON before verifying. · W38
2. **Keep the timestamp tolerance (default 5 min; never 0) and a synced clock.** · W38
3. **No secret configured → refuse (5xx), never "process without verifying".** An unverified endpoint lets anyone grant access by posting a fake event. · W38
4. **Dedupe by event id; never assume order; `created` is not for ordering.** For two distinct events about the same fact, key on object id + type; when in doubt fetch the current object from the API. "Thin" events that make the handler fetch the current object avoid stale payloads. · W38
5. **Return 2xx fast and do the work from a queue.** Redirect (3xx) counts as failure. Retries last up to 3 days in production with exponential backoff, so handlers must be idempotent. · W38
6. **Subscribe only to the event types you handle; pin the API version of the endpoint and test before upgrading** (events take the account's API version at the time they occur). · W38
7. **Secret rotation overlaps:** the old secret stays valid for up to 7 days and the header carries one signature per secret; one matching `v1` is enough. · W38
8. **Same rules for any signed callback** (scheduler or queue push services): verify signature on the raw body with the current and next key, check issuer, audience/URL, expiry and body hash; make handlers idempotent because every non-2xx is retried. · W38 (pattern)

## 4. Idempotency keys

1. **Every POST to a payment API should carry an idempotency key** (up to 255 chars at Stripe). The provider stores status and body of the first execution, including a 500, for at least 24 h; reusing the key with different parameters errors. · W39
2. **Results are not stored when validation fails or a concurrent request uses the same key:** a retry may execute. · W39
3. **No personal data in the key** (not an email). Use internal order id + operation, or a UUID v4. · W39
4. **After 24 h the key may be gone and the same request creates a new object:** a late job retry must first check your own database for whether the operation already happened. · W39

## 5. Refunds and disputes

1. **Handle refund, dispute opened, dispute won/lost and failed refund** (a failed refund returns funds to your balance and needs another method). · W41
2. **Card disputes: one submission, no edits, a deadline of roughly 7 to 21 days by network, a total evidence size limit (4.5 MB at Stripe); issuers do not open links, audio or video.** Pre-dispute inquiries should be answered: they can end before a chargeback. · W41
3. **Keep proof of digital delivery:** acceptance of terms (and of any withdrawal-right waiver) with timestamp, IP at purchase, confirmation email, content access records. · W41
4. **Revoke access when a dispute opens and restore if you win; do not refund separately a disputed charge** (the issuer already returned the money). For low amounts accepting may cost less than contesting (dispute fee is not returned; the counter fee is, if you win). · W41

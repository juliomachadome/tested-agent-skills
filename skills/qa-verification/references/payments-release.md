# Payment path, release gate and quality metrics

Format: **rule** · why · source id (ids in `BIBLIOGRAPHY.md`).

## 1. Payment testing (Stripe examples; any expiry in the future, any CVC)

| Scenario | Test card |
|---|---|
| Approved | 4242 4242 4242 4242 |
| Generic decline | 4000 0000 0000 0002 |
| Insufficient funds | 4000 0000 0000 9995 |
| Expired card | 4000 0000 0000 0069 |
| Incorrect CVC | 4000 0000 0000 0127 |
| 3D Secure required | 4000 0000 0000 3220 |
| 3D Secure always | 4000 0027 6000 3184 |
| Fraudulent dispute | 4000 0000 0000 0259 |

Source: Q23 (re-check the list before relying on a number).

1. **In code use test payment method ids (`pm_card_visa` and similar), not card numbers. Never real card data, not in sandbox and not "just to test" in live mode;** sandbox is not for load tests. · Q23
2. **Minimum checkout script:** approved · declined (clear message, retry without retyping) · 3DS completed and 3DS abandoned · double click on pay (one charge) · back from checkout without paying · pay and close the tab before the redirect (access must come from the webhook) · refund. · Q23
3. **Webhooks:** test with the provider CLI (`stripe listen --forward-to …`, `stripe trigger <event>`); the endpoint must handle delayed, duplicated and out-of-order events (this is in the official go-live checklist). Send the same event twice and verify the effect happened once. · Q23
4. **Access is proven in the database and on screen, not on the success page:** after the event, the entitlement exists exactly once and the user gets in. · Q23
5. **Redirect or out-of-page approval methods:** the test that matters is the user who never comes back to the site. · Q23
6. **Go-live essentials:** API version pinned · errors handled including "impossible" ones · logs without sensitive data · no test object ids in production code · production webhook registered and equal to test · keys rotated and out of code. · Q23
7. **In production you do not test with fake purchases:** follow the first real sale (event delivered, access granted, email sent, amount and currency right) and alert on webhook failures. · Q23

## 2. Release gate

Before deploy
- [ ] Full suite green once on the shipping commit (count and commit recorded).
- [ ] Production build without new warnings; production env vars checked by name, never by value.
- [ ] Migration applied and compatible with the running code; recent backup and a restore tested at least once.
- [ ] No test keys, ids or URLs in the production build; production webhooks registered.
- [ ] Database and provider security reviewed (RLS on exposed tables, SSL, auth rate limits, own SMTP, CAPTCHA on signup and login where needed). · Q27
- [ ] Custom error and 404 pages; metadata and robots files; Core Web Vitals measured on a production build. · Q27
- [ ] Rollback plan: how to revert and who decides.

After deploy
- [ ] Read-only smoke in production: entry page, login, one product screen, API health. No fake purchases.
- [ ] Error monitor without a new spike; webhooks delivering; transactional email arriving.
- [ ] First real transaction followed end to end.

## 3. Quality metrics for a small team

Few, cheap, decision-changing:

| Metric | What it says | How to collect |
|---|---|---|
| Escaped defects (found by customers or in production), by severity | Whether the gate catches what matters | simple list per release |
| Change failure rate (deploys needing an urgent fix or rollback) | Delivery stability | count per month (DORA) |
| Time to restore from a bad deploy | Whether rollback works | note per incident (DORA) |
| Known flaky tests | Trust in red | list; goal zero in the gate |
| Duration of the full gate | Whether it keeps being run | CI time |
| Payment success and webhook failures | Health of the money path | provider dashboard |

1. **DORA metrics** (lead time, deploy frequency, time to restore, change failure rate, rework rate) track one product over time; used as targets or to compare different products they turn into noise (Goodhart). · Q26
2. **Do not measure** number of tests, open bugs as a target, or "% automation". · Q26, Q20

# Diagnosis playbook: symptom, likely causes, check, fix

Use it top-down. Step 0 always comes first, because a wrong denominator makes every other branch meaningless. Thresholds are **[F]** starting points unless tagged; the account's own 4-week baseline replaces them. "BE" = break-even CPA.

## Step 0: is the measurement even right? (do this before blaming the ad)
| Check | Metric and threshold | If it fails |
|---|---|---|
| Same period, same timezone, same currency in platform and backend | day boundaries line up | align the report before comparing |
| Platform purchases ÷ backend purchases (same window, click-only column) | stable ratio 0.6-1.3 is normal; a sudden shift of ±25% is a tracking event, not a performance event | go to node M1 |
| Share of backend orders with no campaign/UTM | above 33%: per-creative reading is unreliable, decide at campaign level and MER | node M4 |
| Attribution window or reporting change in the period | since 12/01/2026 7-day and 28-day view windows are gone from reports (default 7-day click + 1-day view): history before and after is not comparable [search, secondary] | compare click-only columns; restate the baseline |
| Test or promo running in the backend (coupon, price change, outage, payment gateway down) | any change in price, checkout, payment methods in the same week | fix cause, not the ad |

## Tree A: CPA went up
`CPA = CPM ÷ 1000 ÷ (CTR × visit rate × page conversion)`. Decompose; the factor that moved tells you where to look.

| Which factor moved (vs previous 7 days or baseline) | Likely causes | Check | Fix |
|---|---|---|---|
| CPM +20% or more, rest flat | season (Q4, Black Friday, holiday peak), narrower audience, more competition, fatigue-driven delivery penalty | CPM trend by day, country, placement; compare with last year's same weeks; did audience controls change? | accept in season and lower the target volume; broaden audience; new concept batch. Do not "fix" with budget cuts alone |
| CTR (link) down 20%+ with frequency up, CPM up | creative fatigue (Tree C) | frequency trend, hook and hold rate by ad, age of the top-spend ad | weekly batch with a new concept; cap age of top ad |
| CTR flat, **visits ÷ clicks** below 75% | slow page, in-app browser breakage, consent banner blocking, broken redirect | open the ad link inside the Instagram/Facebook/TikTok in-app browser on a mid-range phone; speed test; analytics sessions vs link clicks | Tree F |
| Visits fine, page conversion down 25%+ | ad-page mismatch, price change, checkout error, payment method issue, traffic mix shift (new cold audience) | funnel step by step: checkout starts ÷ visits, purchases ÷ checkout starts; mix by placement/age/country | restore the promise on first screen; fix payment; revert the change |
| Everything flat but CPA up | attribution loss: fewer purchases reported (consent drop, CAPI broken, window change) while backend is fine | node M1 | repair tracking; read CPA from backend |
| CPA up only after a budget increase | marginal cost: new money buys worse people; or edits reset learning | compute marginal CPA = Δspend ÷ Δpurchases for the last step; edit history | step down one step; apply the scale rules in `optimization-playbook.md`; do not scale on average CPA |
| CPA up on small spend, few purchases | noise | purchases per compared item below 10: 95% range for true CPA is roughly 54% to 209% of observed at 10 purchases (table in `testing-and-scaling.md`) | write "not enough volume to conclude"; wait for the kill rule |

## Tree B: CTR down (link CTR)
| Cause | Check | Fix |
|---|---|---|
| Fatigue | frequency up, CPM up, CTR falling over 2+ weeks; same ad old | new concept batch (Tree C) |
| Audience saturated (small country, narrow age) | reach growth flat, new-reach share falling, 7-day frequency high | widen controls; horizontal scale; accept lower volume |
| Placement mix shifted (more low-CTR placements) | CTR by placement | judge at ad-set level; remove only formats that do not exist for a placement |
| Creative recently swapped or a new ad took delivery | ad-level spend share this week vs last | read by ad, not by ad set |
| CTR measured on "all clicks" instead of link clicks | column used | use link clicks; all-clicks includes reactions and profile taps |
| Seasonal attention (holidays) | same weeks last year | wait; do not rewrite on one week |

## Tree C: frequency and fatigue
- Signal that counts: **frequency rising AND link CTR falling AND cost per visit rising AND page conversion stable.** If page conversion falls too it is not fatigue.
- No magic frequency threshold [X]. Compare with the account's own 4-week trend; Meta also shows "creative limited/fatigue" labels [search].
- Check also: spend concentrated in one ad (one piece carries 70%+ of spend) means the fatigue risk is one piece; age of that piece; small universe (country x language x age).
- Fix: weekly batch, at least one new concept (not a colour swap); keep the old winner alive until the new one has read at 2.5x CPA; if the universe is tiny, treat refresh as a fixed cost or widen the market.

## Tree D: CPM spike
| Cause | Check | Fix |
|---|---|---|
| Calendar: Q4 and Black Friday raise auction prices, January usually relaxes [F] | compare with own CPM for same weeks last year and with the previous 4 weeks | schedule sales volume outside peaks or accept a higher BE-margin; do not judge creatives in peak weeks against off-peak baselines |
| Narrow audience / tight controls | audience size, exclusions added recently | widen; remove stacked exclusions |
| Low ad quality signals (negative feedback, hides) | feedback columns; comments | change concept; moderate comments |
| New country or placement | breakdown by country, placement | read separately; CPM differs structurally by country |
| Competitor surge, a news event | no direct check; CPM across all your campaigns rises together | wait one week before restructuring |

## Tree E: stuck in learning / learning limited
- Meta: an ad set leaves learning after about 50 optimisation events in the 7 days following the last significant edit; otherwise it is "learning limited" [Meta Help Center, read 15/11/2026, see `platforms.md`].
- Check: events per ad set per week = weekly budget ÷ CPA (use the optimised event, not purchases if it is another event); number of significant edits in the last 7 days (budget jumps, new ads, audience, bid, event); number of ad sets splitting the budget.
- Causes ranked: (1) budget ÷ CPA < 7 per day-equivalent, so the 50 events/week are not affordable [MATH: daily budget needed ≈ 50 × CPA ÷ 7]; (2) too many ad sets; (3) edits every few days; (4) a high-CPA event chosen; (5) very narrow audience; (6) bid/cost cap too tight.
- Fix order: merge ad sets; stop drip edits (batch weekly); optimise a more frequent event only if purchases are under ~10 per week per ad set for two weeks, judging by backend purchases; loosen the cap; accept "limited" where the math says the budget cannot fund 50 events, because CPA in the backend is the judge, not the label.
- Google: Smart Bidding shows "Learning" after structural changes (new or reactivated bid strategy, adding or removing campaigns, ad groups, keywords, big conversion-goal changes) and it can last up to 7 days; budget, target, creative and targeting changes do not trigger it; judge over 2 conversion cycles or 2 weeks, whichever is longer [C, Google Ads Help "Smart Bidding", read 15/11/2026]. A Google Display Smart Bidding page gives volume bands (under 30 conversions: swings up to 100% and learning up to 4 weeks; 100 conversions: swings up to 20%) [C for that campaign type only].
- TikTok: stabilises after about 25 results or 7 days; avoid edits meanwhile [C per earlier read; not re-opened 15/11].

## Tree F: landing page speed and drop-off
| Check | Threshold [F] unless tagged | Fix |
|---|---|---|
| Link clicks vs landing sessions (analytics, consented plus server-side page-view log) | visits ÷ clicks below 75% = leak before the page loads | speed, redirects, in-app browser |
| Largest Contentful Paint on mobile 4G | under 2.5 s is the Core Web Vitals "good" bar [C, web.dev] | compress hero, remove third-party scripts above the fold, preconnect |
| First screen repeats the ad's promise (same words/offer/price) | manual 5-second test | rewrite first screen (copywriting skill) |
| Cookie banner covering the CTA on mobile | screenshot in in-app browser | reduce banner height; neutral design, never push consent |
| Checkout starts ÷ visits and purchases ÷ checkout starts | project baseline; no reliable public number | payment method mix, bank-app return flow in in-app browser, error logs |

## Tree G: audience overlap and fragmentation
- Symptom: several ad sets with the same country/age target, each with CPM rising and delivery uneven; or ad sets competing against each other.
- Check: Meta's audience overlap tool on custom/lookalike audiences; for broad ad sets, count how many ad sets target the same people; compare each ad set's weekly events with the 50-event bar.
- Fix: merge into one broad ad set; split only on structural differences (country, offer, page). Duplicating a winning campaign to "scale" makes copies compete in the same auction [F].

## Tree H: budget too thin per ad set
- Rule: ad sets that fit = weekly budget ÷ (50 × CPA). Below 1 means one ad set, 3-5 ads, and expect "limited".
- Check: ad sets × CPA × 50 ÷ 7 vs daily budget; ads per ad set vs 2.5 × CPA per ad per period.
- Fix: cut ads and ad sets to what the budget reads; test fewer things for longer.

## Tree I: delivery stopped or collapsed
| Check | Cause | Fix |
|---|---|---|
| Ad status (rejected, limited, in review), account status, payment failure, spend limit reached | policy or billing | read the reason; fix the piece once; request review once; never re-upload unchanged or open another account |
| Budget/schedule/end date, daily cap | settings | correct |
| Learning reset after a big edit, audience too small, caps too tight (cost or bid cap below the market) | low delivery without error | loosen cap by 20-30% or switch to highest-volume; widen audience |
| Pixel/CAPI stopped, or domain verification lost | zero purchases reported but spend continues | Tree M1 |
| Ad account restricted after policy strikes | account quality page | stop circumvention; appeal through official form |
Spend flat at 0 with no status error for 24 h: check payment method and schedule before anything else.

## Tree P: policy rejections
- Read the exact policy named in the notice. Frequent triggers: personal-attribute claims ("you are 50..."), before/after or health/finance claims, unrealistic earnings promises, misleading urgency, landing page that does not match the ad, prohibited content.
- Fix the piece or the page, request review once, keep the record. Hand the creative rewrite to ad-creatives. Never open a new account to bypass (account-circumvention policy).
- In the EU, ads need beneficiary and payer fields; wrong or missing ones block delivery [C per earlier read].

## Tree M: measurement problems
**M1: conversions mismatch, pixel versus backend**
| Pattern | Likely cause | Check | Fix |
|---|---|---|---|
| Platform shows far fewer purchases than backend (ratio under ~0.5) | consent refusals; browser blockers; CAPI missing or failing; wrong event name; purchase fires only on a thank-you page that people do not reach (bank-app return, closed tab) | Events Manager test events; compare event counts per source (browser vs server); backend orders by source | send server event from the order-paid webhook with consent check; keep pixel too; fix thank-you reach |
| Platform shows more than backend | duplicate counting (pixel and server without dedup), refunds/cancellations not netted, view-through, test orders, multiple fires per order | count events per `order_id`; check dedup keys | dedup by identical event name + `event_id`; exclude test orders; compare click-only column |
| Ratio swings suddenly | window change, consent banner change, release broke the tag, iOS/browser update | release log; date of the swing | repair; restate baseline |

**M2: CAPI deduplication and Event Match Quality**
- Dedup (Meta): the browser `eventID` and the server `event_id` must be identical for the same action, with the same event name; events arriving within 48 hours of the first with the same key are treated as duplicates and later ones are discarded. A second route matches `fbp` or `external_id` consistently from browser and server, but only for browser-first-then-server sequences [C, Meta for Developers, "Deduplicate pixel and server events", read 15/11/2026]. TikTok likewise needs the same `event_id` through pixel and Events API [C, TikTok Help "About event deduplication", search summary 15/11/2026].
- Symptom of broken dedup: platform purchases about 2x backend; Events Manager shows "duplicate" warnings or a very high server-plus-browser overlap. Fix: use the order id as `event_id` in both.
- Symptom of weak matching: low Event Match Quality. Meta shows a 0-10 score in Events Manager; vendors treat 6+ as acceptable and 8+ as good, but Meta's own page with thresholds could not be confirmed [unverified thresholds]. Improve by sending, with consent, `client_user_agent`, IP, `fbp`, `fbc` (from the `fbclid` cookie), hashed `em`, `ph`, `external_id`, country, consistent between browser and server; hashing per Meta's spec [C for the parameters list].
- Under consent law (EU) never send a refuser's data via the server. Expect partial visibility.

**M3: attribution window changes.** Since 12/01/2026 Meta reports no 7-day or 28-day view windows; defaults 7-day click + 1-day view; some sources disagree on whether 28-day click remains in the API [search, secondary; unconfirmed]. Check what window the baseline used; compare click-only vs backend; rebuild the baseline instead of reading a "drop".

**M4: broken UTMs.** Check: orders with empty source; `utm_*` lost on redirects, payment gateway or in-app browser; links with different case (`Meta` vs `meta`); campaign names that do not match the naming convention; one link per ad. Fix: set UTMs in the ad's URL parameter field, persist at first touch on the order, test one purchase per ad link without accepting cookies.

**M5: iOS and consent signal loss.** Symptoms: CPA on the dashboard 30%+ above backend CPA; delivery slower; EMQ down; small remarketing lists. Check: consent accept rate by source (own data; one vendor's 2025 benchmark ~56% W. Europe accept [M][1-SRC]); share of iOS traffic. Fix: honest banner; server events with consent; decide on backend and MER; shrink remarketing ambitions.

**M6: Advantage+ / Performance Max black-box effects.** Symptoms: spend drifts to brand or retargeting; good platform ROAS but flat total revenue; creative reporting thin. Checks: new-customer share where reported; branded vs non-branded split (Google search terms/insights); compare MER and incrementality (reading-data.md); in PMax keep brand exclusions and asset-group-level reports. Fix: feed it more different creative, strengthen conversion data (value, enhanced conversions, consent signals), judge on total revenue, and run a holdout when spend justifies. Google Smart Bidding volume advice: Target ROAS typically wants at least ~15 conversions in 30 days (Google Ads Help, via search 15/11/2026; PMax's own stability figure of 15 per 30 days is from secondary reporting, unconfirmed).

## Tree S: seasonality and auction
Before declaring a creative or structure failed: compare with the same calendar weeks last year and with your own CPM; note holiday/pay-day cycles; read 14-day windows across the event; in peak weeks accept CPA up to BE only when the baseline says conversion holds.

## Priority order when several things look wrong
1. Tracking/consent integrity (Step 0, M)  2. Delivery and policy (I, P)  3. Page and funnel (F)  4. Creative fatigue and concept (B, C)  5. Structure and budget (E, G, H)  6. Auction/season (D, S). Fix upstream causes first; downstream metrics often recover alone.

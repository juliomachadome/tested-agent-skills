# Measurement, attribution and diagnosis

## Stage metrics
Reference values are **[F]** starting points; the project's own two-week baseline replaces them.

| Stage | Metric | Formula | Starting reference [F] | If bad, look at |
|---|---|---|---|---|
| Auction | CPM | spend ÷ impressions × 1000 | depends on country and month | audience too narrow, season, ad quality |
| Attention | hook rate | 3-s plays ÷ impressions | 25%+ | frame 0 and first line |
| Attention | hold rate | ThruPlays ÷ 3-s plays | 25%+ | body of the video |
| Click | link CTR | link clicks ÷ impressions | 1%+ | reason to click, CTA |
| Click | link CPC | spend ÷ link clicks | CPM ÷ (10 × CTR%) | both above |
| Arrival | visits ÷ clicks | landing visits ÷ link clicks | 75%+ | speed, in-app browser, cookie banner |
| Arrival | **cost per visit** | spend ÷ visits | ≤ max cost per visit | everything above |
| Page | checkout starts ÷ visits | | no reliable public reference | first screen, price, proof |
| Free funnel | start, completion, e-mail | per step | project baseline | step 1 and e-mail ask |
| Checkout | purchases ÷ checkout starts | | no reliable public reference | payment method, errors, bank-app return |
| Sale | entry conversion | purchases ÷ visits | ≥ minimum conversion | page, offer, ad-page match |
| Sale | CPA | spend ÷ backend purchases | ≤ break-even | |
| Sale | AOV | revenue ÷ orders | | bump and upsell (offers) |
| Decision | **net RPV** | margin per order × conversion | ≥ cost per visit | |
| Health | refunds by source | refunds ÷ cohort orders | own history | ad over-promising |
| Health | 7-day frequency | impressions ÷ people | trend, not threshold | fatigue |
| Cross-check | MER | total revenue ÷ total ad spend | ≥ break-even ROAS | attribution |

**Quick read**
- High CPM, rest fine: expensive auction (season, country, narrow audience); not the creative.
- Good CTR, low visits/clicks: page slow or broken in the Instagram/Facebook/TikTok in-app browser. Test on a phone, inside the app.
- Good cost per visit, bad conversion: page, offer, or an ad promise the page does not repeat.
- Good checkout starts, bad purchases: payment. Where payment goes through a bank app, "leave, approve, come back" must work inside the in-app browser.
- All on target, CPA rises with budget: marginal cost or fatigue.
- Dashboard good, backend bad (or reverse): attribution. The backend wins.

## Attribution and tracking
- **[C] Three sources, one hierarchy:** backend orders > consented site analytics > platform dashboard. Divergence is expected; decisions come from the first.
- **[C] Fixed UTM scheme and one ID per creative:** `utm_source`, `utm_medium`, `utm_campaign`, `utm_content` from a closed list, lowercase, stored on the order at first touch. Without it there is no per-creative CPA outside the dashboard. If links are visible in a public ad library, use an opaque code instead of readable UTMs.
- **[C][EU] Pixel and server events only with marketing consent.** Store the consent proof linked to the order and decide at send time with the latest consent.
- **[F] Expect the platform to see only part of purchases.** One consent vendor's 2025 benchmark: accept rate over all banners shown ~56% in Western Europe and ~68% in Eastern Europe, with 22-27% making no choice. Measure your own rate by source. Effects: dashboard CPA higher than real; slower learning. An honest banner (does not cover the button, "accept" and "reject" equal weight) is the limit: never push consent. [1-SRC]
- **[C] Server API done right:** the platform's requirements plus a retry queue for transient errors, an idempotency key per event, and test codes removed after verification.
- **Cookieless gaps:** refusers who come back another day arrive as "direct". Track the share of orders without source; above a third, per-creative reading is compromised and decisions move up to campaign level and MER.
- **[M] The dashboard over- and under-states.** View-through inflates; cross-device or later purchases vanish. Compare "click only" with the backend per campaign; if the ratio is stable, use it as a correction factor for intraday reads.
- **Cheap incrementality, when spend justifies it:** pause media in some regions for two weeks, or pause everything 5-7 days off-peak, and see how much total revenue drops. For small spend, MER and backend suffice.
- **Do not stack tools.** Third-party trackers, server-side tag managers and "AI attribution" add scripts, cost and personal-data surface. For low ticket, backend + UTM + the platform's official API is enough.

## Researching a country (method)
1. Audience size and age per platform: public reach reports (ad reach is not active users; not comparable across years), monthly user-by-age panels, national audience panels where they exist.
2. Auction prices: no official CPM per country; vendor tables disagree [F]. The account's first week replaces everything.
3. Who needs the product: national statistics, Eurostat, national polls. Proficiency indices from private schools sample volunteers: for comparing groups, not as a population portrait.
4. Why they buy: motivation surveys with declared method and sample; studies sponsored by competitors are [F].
5. How they pay and on what device: national e-commerce reports, payment processor docs.
6. Calendar: holidays, back-to-school, gift dates, resolution month; confirm with 5 years of search trends, then own data.
7. Competition: ad libraries (Meta's EU library shows targeting and reach), TikTok creative center, Google ads transparency. Automated reading is often blocked: a 15-minute manual task. An ad running for months is the best public signal that it sells.
8. Consent: typical regional accept rate, then your own.
9. Local law: price, urgency, testimonials, commercial communications (offers, copywriting skills).
Write each audience as a hypothesis: who, how many, why they would buy, which entry point, which creative concept finds them, source and date.

## Myths and numbers not to repeat
| Claim | Status |
|---|---|
| "Raising more than 20% resets everything" | [F] conservative step, not law |
| "You must exit learning to succeed" | [F] a label; limited is normal on small budgets |
| "Cap existing customers at 20-30% in Advantage+" | [X] feature removed |
| "60% similarity score suppresses ads" | [X] no Meta source |
| "50 ads per ad set" | [F] one practitioner's experiment |
| "TikTok needs 50 conversions" | [X] official help says ~25 results or 7 days |
| "At least two ad accounts" | [X] for small sellers; policy risk |
| "Optimise for leads, they are cheaper" | [F] cheap leads are not buyers |
| "Switch off the ad with the worst average CPA" | [X] breakdown effect |
| "3 sales vs 5 means we have a winner" | [X] noise |
| "Hook rate above 30% = good ad" | [X] attention is not sales |
| "Dashboard ROAS is the return" | [X] window, view-through, consent |
| "Server API removes the need for consent" | [X] same infringement, other path |
| "Frequency above 2.5 = fatigue" | [X] no source; watch the trend |
| "CPM in country X is Y" | [F] vendors disagree |
| "Duplicating the winning campaign scales" | [F] internal auction |

## Book and study rules
1. **Reach beats frequency (Sharp, *How Brands Grow*, 2010) [M]:** growth mostly comes from many light buyers, not a loyal few; keep reach broad and avoid over-narrow targeting that caps the buyer pool. Test narrow audiences against broad before assuming they win. Evidence is from repeat-purchase consumer categories; check it fits your product.
2. **Brand and activation both matter (Binet and Field, *The Long and the Short of It*, 2013) [M]:** IPA effectiveness data show long-term brand building works over months and short-term activation works now; a commonly cited split is about 60 brand to 40 activation, but it is an average across mostly large consumer brands, not a rule for a small account. Judge a campaign on cost per acquisition and on whether top-of-funnel demand grows.
3. **Experiments (Kohavi et al., 2020) [M]:** same rules as in `testing-and-scaling.md` (primary metric and guardrails before launch, sample-ratio check, no early peeking).

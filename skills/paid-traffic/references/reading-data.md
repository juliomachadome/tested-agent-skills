# Reading exported data and reconciling with the backend

## 1. Reading an ads-manager CSV or screenshot
Ask for: date range and timezone, currency, attribution setting used, level (campaign / ad set / ad), breakdown, and a backend export for the same dates (orders, net revenue, refunds, source, campaign, ad/UTM). Without these, say what is unknown.

| Column | Use | Trap |
|---|---|---|
| Amount spent | denominator | currency/timezone; "spend" may include tax |
| Impressions, Reach, Frequency | CPM = spend ÷ impressions × 1000; frequency = impressions ÷ reach | reach is de-duplicated per report window and not additive across rows |
| Link clicks (not "clicks (all)") | link CTR = link clicks ÷ impressions | all-clicks includes reactions and profile taps |
| Landing page views | visit rate = LPV ÷ link clicks | LPV needs the pixel to fire; consent loss lowers it |
| Results / Purchases, Purchase conversion value | CPA, platform ROAS | window, view-through, consent, modelled data |
| Attribution setting column | what window produced the number | changed since 12/01/2026 [search, secondary] |
| Delivery / learning status, quality ranking | context only | labels are not proof |
| Video plays, 3-second plays, ThruPlays | hook and hold | attention is not sales |

**Sanity checks (do all before analysing)**
1. Totals row = sum of rows? (reach and frequency will not sum).
2. CTR, CPM and CPC recompute from the raw columns; if they do not, the file mixes levels.
3. Any row with zero spend or zero impressions but conversions: attribution lag.
4. Purchases ÷ link clicks above 15% or ROAS above 10: suspect duplicate counting or a mislabelled column.
5. Date range includes today (incomplete) or an edit date (learning reset).
6. Breakdown rows add to the campaign total? If not, filtered.
7. Compare platform conversion value with backend gross revenue for the same days: ratio stable in time is a calibration factor; a jump is a tracking event.

## 2. Reconciling platform ROAS with backend
- **Platform ROAS** = platform conversion value ÷ spend (gross, own window, own counting).
- **Backend ROAS (blended or MER)** = total net revenue ÷ total ad spend, all sources, same period. MER includes organic and returning customers, so use it as an upper-level health check, not as a channel ROAS.
- **Channel backend ROAS** = backend net revenue of orders carrying that channel's UTM ÷ spend. Needs a first-touch UTM on the order.
- **Decision hierarchy:** backend orders > consented analytics > dashboard.
- **Reconciliation worksheet:** for each campaign: platform purchases, backend purchases with UTM, ratio, orders with no source, refunds. If the unsourced share is above a third, decide at campaign level and MER.
- Gap decomposition [F]: (a) consent loss and blockers (backend higher), (b) view-through and multi-window double counting (platform higher), (c) refunds and tax (platform higher, gross), (d) cross-device and delay (backend higher), (e) duplicates from pixel plus server without dedup (platform higher). Quantify each with the checks in `diagnosis-playbook.md` M1-M5.
- Worked example: platform says 120 purchases, 2.4 ROAS; backend shows 70 orders with the campaign UTM, 22 without source, and net revenue gives ROAS 1.1. Platform includes view-through (about 25%) and gross revenue; unsourced orders may belong to the ads: the true channel ROAS lies between 1.1 and ~1.5. Decide on 1.1 until the source gap is closed.

## 3. Incrementality: is the channel causing sales?
| Method | How | Cost | Use when |
|---|---|---|---|
| Platform conversion lift (user-based holdout) | randomised test vs control by the platform | needs minimum spend (platform sets it) and 2-4+ weeks | one channel is large (e.g. above ~30% of revenue) and platform ROAS disagrees with backend |
| Geo holdout / geo experiment | turn ads off or down in matched regions for 2-4 weeks, compare sales vs control regions | no tool cost, needs enough regions and seasonality control; Google documents an open-source geo incrementality tool (Meridian GeoX) [C, read via search 15/11/2026] | spend high enough that a drop is visible above noise |
| Pause test | pause 5-7 days off-peak, watch total revenue | cheap; confounded by trend | very small accounts as a smoke test |
| MMM (marketing mix model) | regression on spend vs sales by channel; Google's Meridian is open source | data and skills | multi-channel, 2+ years data |
- **Worth it when** monthly spend is large enough that a 10-20% error in channel value is expensive (rule of thumb: spend above ~10-20% of monthly net revenue or above ~5-10k per month on one channel [F]); otherwise MER plus backend UTM is enough.
- Results: report lift %, incremental CPA = spend ÷ incremental purchases, confidence interval; compare to dashboard CPA to get a calibration factor; re-run when mix changes. Studies on large advertisers show platform dashboards err in both directions [M][1-SRC]; treat as warning, not expected values.
- Avoid overlapping lift studies on the same campaign (Google's GeoX guidance) and read lag: very short tests understate effect on long conversion cycles.

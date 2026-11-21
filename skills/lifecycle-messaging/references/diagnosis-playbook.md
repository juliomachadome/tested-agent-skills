# Diagnosis playbook: symptom, likely causes, check, fix

Use top-down. Step 0 first: a broken trigger or a flattering attribution makes every branch meaningless. Thresholds are **[F]** unless tagged; the sender's own last 8-12 weeks replace them. Tags: **[C]** law, standard or platform rule read on the official page; **[M]** serious but single or correlational; **[F]** practitioner or vendor; **[X]** myth. Ideas are applied, not copied.

## Step 0: is the evidence trustworthy?
| Check | How | If it fails |
|---|---|---|
| Trigger fires once per real event | count sends per person per event; look for the same user in a flow twice | add entry limits and a re-entry rule before reading any result |
| Bot and scanner clicks | clicks within seconds of delivery, many links clicked in the same second, security-gateway user agents | filter them; re-read click rate |
| Apple Mail Privacy Protection | share of opens from Apple clients; opens with no click and no session | treat opens as noise **[C]**; use clicks, conversions, holdout |
| Attribution window | write the window and model (last touch, days) beside every revenue number | recompute with one window; compare with holdout |
| Holdout exists | is any random share of eligible people not sent the flow? | no holdout = revenue is "touched", not "caused"; start one |
| Denominators | rates per delivered message, not per sent; per 1,000 sends for unsubscribes and complaints | recompute and label |
| Sample size | under about 30 events in a cell moves wildly (roughly +/-14 points at n=30, 50%) | report "not enough"; widen the window |
| Change calendar | domain, tool or template changes, big sends, price or policy changes, store or app releases in the window | line them up before naming a cause |

## Core arithmetic
- **Incremental effect**: lift = treated rate - holdout rate; incremental orders = lift x treated audience; incremental revenue = incremental orders x average order value (margin, not revenue, for a discounted flow). Worked example (cart flow): 11,160 treated carts, 1,240 held out. Treated bought 11.4% (1,272 orders), holdout 9.8% (122 orders). Lift 1.6 points = 179 incremental orders, at 62 per order = 11,071 vs 78,879 reported as flow revenue: only about 14% is caused. Check the noise: pooled rate 10.5%, standard error of the difference about 0.95 points, z = 1.7: not significant at 95%, so keep the holdout running (growth-analytics for sample size) before declaring a winner **[C]**.
- **Complaint rate**: complaints / delivered to that mailbox provider. If 21,000 messages a day reach Gmail and the spam rate is 0.34%, about 71 users a day mark spam; the 0.10% aim is about 21, and 0.30% is the line to stay under **[C]** (Gmail sender page). Cutting the least-engaged segment usually moves this faster than rewriting.
- **Dunning recovery**: failed = renewals x first-attempt failure rate; recovered = failed x recovery rate; lost MRR = (failed - recovered) x price. 1,800 renewals, 6.5% fail = 117; 55% recovered = 64; lost = 53 x 19 = about 1,000 per month; +7 points of recovery adds about 156 per month.
- **Cap budget**: a person's weekly messages = sum across flows and broadcasts; if a user can be in 4 flows plus 2 broadcasts, the worst week is 6+ messages even when each flow "looks gentle".

## Symptom trees
**Low clicks on a flow.** Causes: wrong trigger timing (message arrives after the moment passed); sender name unfamiliar; two goals in one message; mobile layout broken; image-only content blocked. Check: time from event to send; click map by device; render test; sender field. Fix: move send to the moment, one button, plain-text part, human sender.

**Mail lands in spam or promotions.** Causes (check in this order): authentication missing or unaligned (SPF over 10 DNS lookups gives permerror **[C]**, DKIM key under 1024 bits, DMARC absent or From domain not aligned **[C]**); spam rate above 0.10% to 0.30% **[C]**; no one-click unsubscribe headers for bulk senders **[C]**; new domain or IP blasted at volume; old or bought addresses (bounces, spam traps); shared domain with a bad neighbour; link or image domain with poor reputation. Check: Postmaster reports, DMARC aggregate reports, bounce codes by provider, seed test, DNS lookup count. Fix: authenticate and align, add List-Unsubscribe and List-Unsubscribe-Post signed by DKIM **[C]** (RFC 8058), suppress inactive and bounced, warm up in batches of engaged users, split marketing and transactional subdomains **[F]**. Promotions tab is a classification, not a failure; judge by clicks and conversions.

**Unsubscribes or complaints rising.** Causes: frequency above what the person expects; broadcast to a stale segment; consent unclear at collection (surprise); hard-to-find unsubscribe, so people press spam instead; flow ignores that the person already acted. Check: unsubscribes and complaints per 1,000 sends by flow, by signup source, by tenure; the unsubscribe path in two taps. Fix: preference centre with frequency options, exit conditions, cap, cut the weakest flow first, confirm opt-in for sources that complain.

**Flow shows revenue but nothing changed in the total.** Causes: attribution counts buyers who would have bought; discount trains customers to wait; flow overlaps with a broadcast; no holdout. Check: holdout lift (above), revenue per eligible person, discount rate before and after. Fix: holdout 5-10% (larger for low volume), margin-based reading, remove the discount from the first message, suppression between flows.

**Abandoned cart flow underperforms.** Causes: cart event fires for people who bought later (no purchase exit); first message too late or too early; email only when push or SMS has consent and fits; shipping cost shown late is the real reason. Check: purchase-exit logic, time-to-first-send, reasons from exit surveys. Fix: exit on purchase, first send within hours, show cost earlier on the site; reserve any incentive for a later step (offers sets the rules).

**Welcome or onboarding flow does not activate.** Causes: messages tell features instead of pushing the one step; send ignores what the user already did; trigger starts at signup when the first value needs data the user has not added. Check: activation event rate by message, days to activation. Fix: event-driven nudges that stop when the step is done; in-app prompt where the user already is (onboarding skill for product flows).

**Trial does not convert.** Causes: no value before the trial ends; reminder only on the last day; payment friction; wrong plan shown. Check: activation by day 3, sessions in trial, conversion by cohort. Fix: nudge to value moment, reminders with the date and what happens next (clear about charge), easy path to pick plan.

**Push opt-in is low.** Causes: native permission asked at first launch; no value shown; iOS denial is not shown again, Android 13 off by default **[C]**. Check: prompt-to-allow rate by placement; share never asked. Fix: ask after a value moment from a user action, with a soft prompt that can be dismissed without spending the native prompt **[F]**; offer provisional delivery on iOS to show value first (the Apple permission API doc was not read; confirm).

**Push opt-outs or uninstalls spike.** Causes: promotions mixed with service alerts; frequency; generic content; sends at night in the user's time zone. Check: opt-out per 1,000 sends by category, time of send in local time. Fix: categories with their own switch, quiet hours, cap, relevance filter.

**WhatsApp template paused or number limited.** Causes: recurring negative feedback or low read rate **[C]**; marketing sent under a utility label; no real opt-in; copy-pasted broadcast. Check: template status and quality in the manager, block and report counts, opt-in evidence per number. Fix: stop the template, re-collect opt-in per category, use the right category, send fewer and more relevant; human escalation path inside automated chats **[C]**.

**Dunning recovers little.** Causes: retries on the wrong days (payday, card expiry month), generic decline treated alike (hard declines need a new card, soft declines need a retry), email only and no in-app banner, card-update link needs login, tone is threatening. Check: recovery by decline code and by day since failure; time to click update. Fix: classify declines, retry schedule on days that match the biller's data, a one-tap update link, in-app banner, a grace period that is stated, a clear last notice (support owns individual cases).

**Cancellation save fails or annoys.** Causes: offer shown before the reason; no real pause or downgrade path; making cancel hard (illegal or fined in some places; check the recipient's country). Check: reason split, accepted-offer rate, complaint tickets. Fix: reason first, then a matching option (pause, downgrade, skip, help), then an easy exit; discount rules in offers.

**Win-back list is dead.** Causes: sending to people who left long ago; address no longer valid; no new reason to return. Check: bounce rate, last-activity histogram, product changes since churn. Fix: sunset policy, one or two re-permission messages with a plain "stay or go", then suppress; keep a product-news reason, not a guilt message.

## Report format
Data used and its quality; the holdout result or the missing holdout; likely and second cause; the check done or to do; the fix with owner; what could not be verified (provider limits, country law, small samples).

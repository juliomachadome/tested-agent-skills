# Playbooks: practical routines

Timings are **[F]** starting points to test against a holdout, not rules. Law and platform rules are tagged **[C]** only where read on the official page (see BIBLIOGRAPHY). Consent and anti-spam rules depend on the recipient's country; check them before sending. Words and tone: copywriting skill.

## 1. Flow spec template (one per flow)
Name and goal (one metric) / entry event and audience / exit conditions (goal done, unsubscribed, open support case, plan changed) / re-entry rule / suppression against other flows / channel order and consent needed per channel / messages (offset, channel, one action, subject idea, fallback if channel fails) / cap and quiet hours / holdout share / owner and review date. A flow without an exit and a holdout is not finished.

## 2. Journey routines (moment, trigger, first messages, exit)
| Moment | Trigger and rhythm | Content job | Exit |
|---|---|---|---|
| Welcome and onboarding | signup; first within minutes, then tied to progress, not a fixed calendar | confirm, set expectation, one first step | first value event |
| Activation nudge | a step not done after N days (N from your median time-to-step) | the user's own unfinished step, with the shortcut | step done |
| Trial to paid | day of start, a value moment, a reminder before end with date and what is charged, a last day note | show progress and result, make plan choice easy | paid or ended |
| Abandoned cart or checkout | cart or checkout event without purchase; first within hours, second next day, third later | the item, delivery and return facts, one link back | purchase |
| Post-purchase and delivery | order, shipped, out for delivery, delivered (transactional, no promotion inside) | status and how to get help; later a how-to-use note | delivered |
| Review ask | days after delivery or after first success, never before the product could be used | one question, one link; ask all buyers, not only the happy; no reward conditional on a positive rating | asked once or twice |
| Referral ask | after a clear success moment | simple mechanic, rule text visible; check the rules for incentives in your country | asked |
| Win-back | inactive N days (your own churn curve) | what is new, an easy return, honest "stay or go" | active or suppressed |
| Renewal notice | before renewal as the law or contract requires, with date and amount | no surprise; how to change or cancel | renewed |
| Failed-payment dunning | payment failed (see section 3) | fix the card quickly | paid |
| Cancellation save | cancel intent in product | reason first, matching option, easy exit | saved or left |
| Re-permission | old list with unclear consent (section 6) | ask once clearly, then suppress non-responders | answered |

## 3. Dunning ladder (subscription payment failed)
Day 0 transactional email and in-app banner with a one-tap card-update link, no login wall if secure to do so. Retries on days chosen from the biller's data; hard declines (stolen, closed) skip retries and ask for a new card; soft declines retry. Day 3-4 second notice with the date service will pause; day 7 or end of grace a last notice stating what happens next. Keep access in a stated grace period. Push or WhatsApp only with consent for that purpose (a utility-type template for a payment notice is not marketing, but check the category rules and your recipient's country). Individual angry replies go to customer-support. Measure recovered share by decline code and by day, plus involuntary churn per month.

## 4. Channel selection
Email: default for explanations, receipts, longer content. Push: time-critical or habit moments, only after permission, value in the preview. In-app: help while the person is there; does not need a permission. SMS: high-value, time-critical, consent explicit, short, stop path. WhatsApp: customer-service conversations and approved templates for opted-in people; marketing templates are paid and reviewed, quality affects limits **[C]**. Rule: use the least intrusive channel that works, and fall back one step at a time, never fan out to every channel at once.

## 5. Frequency, cap and priority
Set a per-person weekly cap across channels (start from the median engaged user's current rate and move in small steps). Priority order: security and payment, order status, activation help, relationship, promotion; lower priorities are dropped first when the cap is hit. Quiet hours in the person's local time. A frequency test: cap A vs cap B with a holdout of no promotions; judge by incremental revenue per 1,000 persons minus unsubscribes and complaints per 1,000, over at least a full buying cycle. Offer a preference centre: topics and frequency, not only on/off.

## 6. Re-permission and consent checklist
Before any send ask: who is the recipient's country; is there prior consent, or a lawful exception in that country; where, when and for what purpose was it given; can I show it; is the unsubscribe one step; is the global suppression list honoured by every tool (including broadcasts made by hand). Examples read: EU ePrivacy art. 13 requires prior consent for marketing email with a narrow own-customer exception; CAN-SPAM requires an opt-out honoured within 10 business days and a postal address; LGPD asks specific, provable, revocable consent unless another legal basis applies **[C]**. For re-permission: send one or two clear messages ("keep getting X? yes/no"), record answers, suppress the rest; do not send a promotion disguised as a re-permission ask. Depth: the privacy law of the data subject's country (official regulator pages); this is not legal advice.

## 7. Deliverability audit
1. Domains: marketing and transactional on separate subdomains; From domain aligned. 2. SPF: one record, under 10 lookups, ends with a clear policy. 3. DKIM: 2048-bit if the provider supports it (1024 minimum on the Gmail page), selectors per provider. 4. DMARC: start p=none with rua reports, read them, move to quarantine then reject when all legitimate senders align. 5. Headers: List-Unsubscribe and List-Unsubscribe-Post (RFC 8058) signed by DKIM; visible link in body. 6. DNS: PTR and forward-confirmed reverse DNS for own IPs, TLS. 7. Reputation: Postmaster-type spam rate under 0.10% target, never 0.30%. 8. List: suppress hard bounces at once, sunset inactive, no purchased lists. 9. Warm-up: new domain or IP starts with engaged users in small batches, grows over weeks, watch each provider. 10. Alerting: weekly review of bounce, complaint and delivery by provider. Gmail's bulk rules apply above 5,000 messages a day to Gmail; below that SPF or DKIM, TLS and low spam rate still apply **[C]**.

## 8. Push and WhatsApp launch checklist
Push: value-first soft prompt after a value moment; separate marketing consent and a way to opt out in settings (Apple guideline 4.5.4); app works without push; categories with their own switch; deep links tested; no sensitive data; local-time quiet hours; Android 13 runtime permission asked in context. WhatsApp: opt-in captured per category with evidence; template category chosen honestly (authentication, marketing, utility); templates tested for variable fill and links; stop keywords handled and synced to the suppression list; human escalation path; weekly template status and block-rate review. Verify current pricing and window rules on the platform page, which were not read here.

## 9. Measurement plan and weekly review
Plan: metric moved; eligible population; holdout share and how people are assigned (random, stable per person); window; guardrails (unsubscribes, complaints, support contacts); stop rule; who reads it. Do not use opens as the goal after Apple Mail Privacy Protection **[C]**. Weekly agenda (30 min): deliverability by provider; each flow's incremental lift and guardrails; new or changed triggers; cap breaches (people over the cap); suppression and consent issues; one test to run next, one flow to cut. Test design and statistics: growth-analytics.

## 10. Message review checklist
One goal and one action; trigger matches the moment; subject and preview say what is inside; works with images off; plain-text part; unsubscribe and preference link visible; no promotion inside a transactional message; sender identity and address as the country requires; links on a reputable domain with tracking set per class; tested on two clients and a phone; claims provable; discount is cleared with offers; copy is cleared with copywriting.

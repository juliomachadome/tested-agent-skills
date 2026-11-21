---
name: lifecycle-messaging
description: Use for any lifecycle or CRM message sent to existing users or customers by email, push, in-app, SMS or WhatsApp - design the journey map and triggers, "welcome email sequence", "abandoned cart flow", "trial to paid emails", "push notifications strategy", "failed payment emails" (dunning), "win back churned users", cancellation save, review and referral asks, re-permission, "how often should we email", send time, segmentation, "our emails go to spam" (SPF, DKIM, DMARC, Gmail and Yahoo bulk-sender rules, bounces, complaints, warm-up), "WhatsApp messages to customers" (templates, opt-in), consent and unsubscribe by country, and measuring with holdouts instead of last-click or open rate. Country-neutral. Not for the wording and tone of the message (copywriting), tests and metric design (growth-analytics), law in depth, support replies (customer-support), discount and price rules (offers) or screen design (ux-design).
license: CC-BY-SA-4.0
metadata:
  author: Júlio Machado
  source: https://github.com/juliomachadome/tested-agent-skills
---

# Lifecycle messaging

A lifecycle message earns its place when it moves one person one step (use, buy, pay, return, refer), judged by the extra behaviour it causes, not clicks. Tags: **[C]** law, standard or platform rule read on the official page; **[M]** single, old or correlational; **[F]** practitioner or vendor guidance; **[X]** myth.

## 1. Start: project first, data before tactics
Read project docs first (brand voice, consent records, event list, provider setup, terms, past campaigns); project rules win. Then fix: the money model (one-off, subscription, marketplace); the recipient's country (law follows the recipient); which channels have stored consent; which events exist; who sends today (tool, domain, volume per day); the one metric this message must move. If missing, ask or state the assumption.

Ask, by task: **flow** - event definitions, send rules, last 8 weeks of sends, clicks, orders, unsubscribes, complaints per flow. **Deliverability** - sending domains, DNS records, Postmaster reports, daily volume per mailbox provider, bounce and complaint rates, how the list was built. **Dunning** - failure rate, retry schedule, recovery by day. **Push or WhatsApp** - opt-in rate, when consent is asked, template status, block rate.

## 2. Diagnose first
Open `references/diagnosis-playbook.md`: Step 0 (are sends, events, attribution trustworthy: duplicate triggers, bot clicks, Apple opens, no holdout), then symptom trees: low clicks, spam folder, high unsubscribes or complaints, revenue flat, cart flow cannibalising, low push opt-in, WhatsApp template paused, weak dunning recovery, trial not converting, dead win-back list.

## 3. Triggers, broadcasts, and the journey map
A **trigger** fires from a person's event and is relevant by construction; a **broadcast** fires from your calendar and needs segmentation **[F]**. Build triggers first, then a small calendar. Every flow needs: entry event, exit condition (goal reached, unsubscribed, support open), a re-entry rule, a suppression rule against other flows, and a cap. Moments: welcome and onboarding; activation nudge (the user's own unfinished step); trial to paid; abandoned cart or checkout; post-purchase and delivery; review and referral ask; win-back; renewal notice and failed-payment dunning; cancellation save; re-permission of old lists. Routines: `references/playbooks.md` 1-4. Transactional (receipt, reset, delivery status, account or payment notice) and promotional are different classes in most laws; never slip promotion into a transactional message **[C]** (section 8).

## 4. Segmentation, frequency, timing
Segment by behaviour (did or did not do X in N days, plan, stage), not demographics **[F]**. Caps are per person across all flows and channels, with quiet hours and priority (payment and safety first, promotion last). Send-time optimisation: small gain after targeting and cap **[F]**. "How often" has no universal number: raise cadence only while unsubscribes and complaints per 1,000 sends and incremental revenue stay healthy (`playbooks.md` section 5).

## AI tells to avoid (check while creating, not after)
- Subject lines with emoji and urgency by reflex.
- "We miss you!" and "Just checking in" templates.
- Em-dash and exclamation overuse.
- The same structure in every email of a flow.
- Personalisation by first name only; use what the person did (the step left unfinished, the item viewed).
- Fake deadlines; a deadline must be real and stated once.
- Robotic sign-offs; sign as the person or team who answers replies.
- Say what you chose and why in one line (audience, moment in the journey, data); a choice without a reason is removed.

## 5. Anatomy of one message
One goal, one primary action, one reason now. Recognisable sender, subject and preview that say what is inside, readable without images, one button, plain-text part, visible unsubscribe. Push: title and body carry the value in the lock-screen preview, deep link to the exact screen, no sensitive data **[C]** (Apple guideline 4.5.4). In-app: next-step help while the person is in the product.

## 6. Deliverability (email)
Authenticate and align: SPF, DKIM, DMARC (p=none at least), From domain aligned **[C]** (RFC 7208, 6376, 7489; Gmail and Yahoo pages). Gmail's bulk-sender rules (over 5,000 messages a day to Gmail) add DMARC, one-click unsubscribe headers (RFC 8058) and a spam rate under 0.30%, aiming under 0.10% **[C]**; Yahoo asks for SPF and DKIM for bulk senders, DMARC pass, one-click unsubscribe, spam rate under 0.3% and unsubscribes honoured within 2 days **[C]**. Send marketing from a subdomain apart from transactional to isolate reputation **[F]**. Hygiene: suppress hard bounces, drop long-inactive addresses and complainers, never buy lists, warm up new domains or IPs with small engaged batches **[F]**.

## 7. Push, in-app, SMS, WhatsApp rules
- **Push**: iOS and Android both need user permission; promotion needs explicit consent and an opt-out; the app must work without push **[C]** (Apple guideline 4.5.4; Android 13 POST_NOTIFICATIONS: off by default for new installs, ask in context). Never ask at first launch: soft prompt after a value moment; a denied iOS prompt is not shown again **[F]**.
- **WhatsApp**: message only people who gave their number and agreed to hear from you; honour every stop request; outside the customer-service window only approved templates (categories authentication, marketing, utility); templates can be paused for low read rates or negative feedback; blocks and reports can limit sending **[C]** (Business Messaging Policy and template docs; the window is 24 hours from the user's last message, bib. 26; price amounts not read).
- **SMS**: consent rules are strict in many countries (US TCPA: marketing calls or texts by autodialer or prerecorded voice need prior express written consent, source 28) and carriers add rules; keep SMS for time-critical, high-value events; give a stop path.

## 8. Consent, unsubscribe, law (check the rules of the recipient's country)
Rules differ by recipient country and channel: opt-in needed, existing-customer exceptions, opt-out speed, identification and address to show. Read on official pages: EU ePrivacy art. 13 (prior consent for marketing email, narrow exception for a seller's own similar products if opt-out was offered at collection and in each message; no disguised sender) **[C]**; US CAN-SPAM (no deceptive headers or subjects, identify as an ad, postal address, working opt-out honoured within 10 business days, penalties per email, transactional exemption only for narrow categories) **[C]**; Brazil LGPD (consent specific, provable, revocable freely; other legal bases exist) **[C]**. UK PECR reg. 22 (consent, soft opt-in for own similar products, source 27) **[C]**; US TCPA (written consent for autodialed marketing texts, 8 a.m.-9 p.m., do-not-call, source 28) **[C]**. GDPR depth: the privacy law of the data subject's country (official regulator pages) or counsel. Record who consented, when, to what and where; one-step unsubscribe; global suppression list; not legal advice.

## 9. Measurement
Last-click flow revenue overstates impact: it counts buyers who would have bought anyway. Keep a **holdout** (random share who get nothing) and compare behaviour; incremental revenue = (treated rate - holdout rate) x treated audience x value **[C]** (Kohavi et al. on controlled experiments). Apple Mail Privacy Protection can block tracking images, so opens are unreliable as a goal or test metric **[C]** (Apple newsroom 2021); use clicks, conversions, replies, unsubscribes, complaints and holdout lift. Tests and sample size: growth-analytics.

## 10. Output
Match the request: journey map table, flow spec with timing, deliverability audit, consent plan by country, dunning ladder, cap rules, measurement plan with holdout size. End with: metric moved, holdout that proves it, consent basis per channel, evidence level of rules cited, what you could not verify (country legal detail, provider limits, small samples).

## Which reference to open
`references/diagnosis-playbook.md` (Step 0 and symptom trees, worked numbers) - `references/playbooks.md` (journey routines, flow specs, dunning ladder, cap and priority rules, deliverability audit, consent checklist, review agenda) - `references/BIBLIOGRAPHY.md` (sources and status). Related: copywriting (words), growth-analytics (tests and metrics) (law depth), customer-support (support replies), offers (discount rules), onboarding (in-product activation).

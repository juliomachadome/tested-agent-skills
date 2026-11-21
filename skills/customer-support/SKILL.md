---
name: customer-support
description: >-
  Customer support - invoke this skill FIRST, before answering, for any support question, even a short one - replies to customers (angry, refund, cancellation, outage), macros, help-center and how-to articles ("write a help article for resetting a password"), refund or cancellation requests ("customer wants a refund 40 days after buying, what do I answer"), ticket triage and severity, SLAs, escalation to engineering with reproducible bug reports, deflection versus human care, diagnosing support metrics (CSAT falling, backlog, reopens, repeat contacts, bot "resolved" but customers giving up, chargebacks), CSAT/CES/NPS limits, voice-of-customer reports, consumer law for refunds and cancellations. Also when someone pastes a ticket thread without saying "support". Ethical: no dark patterns in cancellation. Not for marketing text (copywriting) or acquiring customers (sales).
license: CC-BY-SA-4.0
metadata:
  author: Júlio Machado
  source: https://github.com/juliomachadome/tested-agent-skills
---

# Customer support

Support is the product speaking when something went wrong. Goal: the customer's problem solved with the least effort on their side, and the cause fed back to the team so the ticket does not come again.

Evidence tags: **[C]** consensus or law · **[M]** serious but single or correlational · **[F]** practitioner or vendor claim · **[X]** myth.

## 1. Start: read the project

Read the current project's docs first: product limits, pricing and refund policy, brand voice, languages and country (consumer law), existing macros, severity definitions, who owns escalations. Project rules override this skill. If the policy is missing, state the assumption and flag it for the owner rather than inventing a promise.

## 2. Reply principles

1. First line answers or acts. Acknowledge feeling in one short sentence, not three **[M]**.
2. Say what you did and what happens next, with a date or a condition. Never promise what you do not control.
3. Own the problem; do not blame the customer, vendor or "the system". Apologise once, specifically.
4. One reply, one ask. If you need information, ask all of it at once, as a numbered list.
5. Plain words, short sentences, the customer's language and register; no jargon.
6. Never lie to close a ticket (fake "fixed" or ETAs). Unknown is an acceptable answer when paired with when you will know.
7. Never expose other customers' data or internal ids.

Effort matters more than delight **[M]**: customers punished high-effort experiences (repeating themselves, channel switching, being bounced) more than they rewarded exceeding expectations (*The Effortless Experience*; one vendor-led study, figures indicative). Moves: solve in first contact, anticipate the next question, keep case history so nobody asks twice.

## 3. Triage

Classify each ticket on two axes: **impact** (who and how many are blocked; data loss, money, security) and **urgency** (deadline, workaround exists). Suggested severities:

| Sev | Meaning | First response target | Update cadence |
|---|---|---|---|
| 1 | Outage, data loss, security, payments broken for many | minutes, 24x7 if promised | every 30-60 min |
| 2 | Core feature broken for some, no workaround | hours | every few hours |
| 3 | Degraded or workaround exists | 1 business day | on change |
| 4 | Question, request, cosmetic | 1-2 business days | on resolution |

Tag by area and cause so trends show. Security and privacy reports (incl. data-subject requests) go to their owners at once, under legal clocks (see references/refunds-consumer-law.md).

## 4. SLAs

Promise only what staffing can meet; measure first response and resolution separately, by severity **[C]**. Pause the clock only for waiting on the customer. Publish real numbers; keep internal targets stricter. Tell the customer when an SLA is missed.

## 5. Help center and KCS

Knowledge-centered service **[M]**: capture and improve knowledge as part of solving the ticket, not afterwards. Loop: capture (in the customer's words), structure (problem, environment, resolution, cause), reuse (search first, link the article in the reply), improve (fix the article if it was wrong or missing). Article rules: title is the customer's problem phrase; steps numbered and testable; screenshots dated or avoided; owner and review date; retire stale articles. Measure link rate, reuse and ticket volume per topic, not article count.

## 6. Deflection versus care

Deflect repeatable, low-emotion, well-documented questions (status, how-to, reset). Do not deflect: payments and money, safety, privacy, cancellation, complaints, any message with strong emotion or a second contact on the same issue. A bot or form always shows a clear path to a human and says when it is a bot **[C]** (disclosure rules vary, verify locally). Judge deflection by resolved-without-recontact; a customer who gave up is not a deflection.

## 7. Escalation to engineering

A bug report that engineers can act on, in this order: title (symptom, where), severity and customer impact (count, revenue, deadline), environment (version, platform, account/plan, locale), steps to reproduce numbered, expected versus actual, evidence (request id, timestamp with timezone, logs without personal data, screenshot), workaround, what was already tried, frequency. If you cannot reproduce, say so and attach what you have; do not guess a cause. Link all tickets to one issue; tell customers when it ships. See references/escalation-template.md.

## 8. Metrics and their limits

CSAT (satisfaction with one interaction), CES (effort), NPS (likelihood to recommend) **[M]**. Limits: low response rates and bias toward extremes; scores differ by channel and culture; NPS predicts growth less reliably than first claimed in independent studies; scores are easy to game (asking only happy customers, coaching agents to beg for 5s). Pair a number with the free-text reason and never tie agent pay to one score. Operational metrics: first response time, time to resolution, reopen rate, contacts per resolved issue, contact rate (tickets per active customer), backlog age. Check definitions, denominators and sample size before reading a trend; for a falling or odd number open `references/diagnosis-playbook.md` (tree per symptom, staffing arithmetic).

## 9. Refunds, cancellation, complaints

Follow the project's policy and the consumer law of the customer's country; when they conflict, the law wins. Typical constraints **[C]**: statutory withdrawal rights for distance sales (for example 14 days in the EU, 7 days in Brazil's consumer code, with exceptions for digital content once performance started with consent), remedies for faulty goods or digital content, clear cancellation as easy as sign-up (rules vary and have changed recently, verify). Never hide the cancel path, guilt-trip, or tie a refund to a review. Offer an alternative (pause, downgrade) once, politely, then do what was asked. Record decision and reason. Rule status (read or unverified) is in references/refunds-consumer-law.md. EU withdrawal button (Directive 2023/2673) applies from 19 June 2026; the US 2024 click-to-cancel amendments are not in force, new rulemaking only at notice stage. Not legal advice.

## AI tells to avoid (check while writing, not after)
- "We apologize for any inconvenience" and "I understand your frustration" as filler; "rest assured".
- Long replies that bury the answer under pleasantries.
- Canned macros that ignore what the customer wrote.
- Passive voice that hides who will do what ("the issue will be looked into").
- Promising what policy does not allow, to sound kind.
- Em dashes, rule-of-three lists, upbeat padding.
Fix: answer first, the customer's own details, who does what by when, plain words. Say what you chose and why in one line; a choice without a reason is removed. If a humanizer skill is installed, run it as a final pass on the finished text, then re-check facts and numbers it may have touched.

## 10. Output

Match the request: a reply draft (with a variant if tone is delicate), macro set (name, when to use, body, placeholders, when not to use), triage table (ticket, sev, area, owner, next action), SLA proposal, KCS article, escalation report, or a metrics readout. End with the follow-up that stops recurrence (article, fix, policy). State evidence level of any claim about metrics or law and mark what you could not verify.

## 11. Which reference to open
- A metric moved, a queue is late, deflection or the bot looks suspicious, volume spiked, agents are leaving, NPS and churn disagree: `references/diagnosis-playbook.md`.
- Hard reply (angry, refund outside policy, bug without fix, outage, cancellation, privacy request, abusive, VIP), triage routine, weekly review, voice-of-customer report, incident text: `references/playbooks.md`.
- Writing or maintaining macros, choosing tone, angry customers, saying no, apologies (Nonviolent Communication lens): `references/tone-and-macros.md`.
- Bug report for engineering: `references/escalation-template.md`.
- Refund, withdrawal, cancellation, chargeback, data-subject request: `references/refunds-consumer-law.md`.
- Sources and verification status: `references/BIBLIOGRAPHY.md`.

## 12. Honest limits
Vendor benchmarks are indicative **[F]**; small samples move scores more than anyone can act on. The skill does not replace counsel for law, nor access to the customer's real data for a diagnosis: when export fields, definitions or the change calendar are missing, say what is missing and what would change the answer.

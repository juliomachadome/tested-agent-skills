# Playbooks: reply recipes and routines

Templates are drafts: adapt to the project's voice, policy and law (`refunds-consumer-law.md`), and to the customer's language. Brackets are placeholders. Evidence tags as in SKILL.md. Tone rules and macro writing live in `tone-and-macros.md`; engineering reports in `escalation-template.md`; metric problems in `diagnosis-playbook.md`.

## 1. Reply recipes for hard cases
Each: goal, moves, a skeleton, what to avoid.

### 1.1 Angry customer
Goal: move from emotion to action in one reply. Moves: answer or act in the first line; one short acknowledgement tied to a fact ("you were charged twice on 3 March"); verify, then say exactly what you did and when the next thing happens; no "calm down", no "as per policy" as the opener, no three apologies. If the anger is justified by our error, say so plainly. Skeleton: "[Fact of what went wrong] and I am sorry. I have [action]. You will see [result] by [date]. If it is not there by then, reply here and I will [next step]." Avoid: defending the company, arguing about tone, long paragraphs. If the customer repeats after two exchanges, hand to a senior owner who can decide, not another script. Reading the message as observation, feeling, need and request, and a one-line check for understanding: `tone-and-macros.md` (Nonviolent Communication lens).

### 1.2 Refund request outside the policy window
Goal: honest decision, with the law checked first. Steps: (1) does a statutory right apply (EU 14-day withdrawal, conformity remedy, Brazil 7 days)? If yes, grant it. (2) If not, is there a fault on our side (bug, outage, misleading page, repeat failure)? Goodwill is justified. (3) Decide by a written rule (for example full goodwill refund up to [N] days for first-time customers, prorated after), not mood, and log it. Skeleton if granted: "I have refunded [amount] to [method]; it should show in [bank timing, not under our control]." If declined: say no in the first line, give the one reason, offer the nearest alternative (credit, downgrade, extension, data export), and name who reviews appeals; name the value behind the limit (fairness to all customers) instead of "policy", and offer an alternative that serves the customer's need (`tone-and-macros.md`, saying no). Never make the refund conditional on a review, on silence, or on a deadline you invented.

### 1.3 Bug we cannot fix yet
Goal: trust despite no fix. Moves: confirm you reproduced it or that others hit it (without detail on other customers); give the workaround with steps; state what you do not know ("I cannot give a date yet; the next update from me will be by [date]"); log the ticket on the engineering issue; offer a compensation only if the policy provides. When it ships, write to every linked customer. Avoid fake ETAs, "soon", and blaming the customer's device without evidence.

### 1.4 Outage communication and status-page cadence
Roles in a serious incident: one incident lead and one communications owner so engineers are not writing customer text (the same split appears in public incident-management guidance, Google SRE book chapter read this pass). Cadence (adjust to promised SLAs): first public acknowledgement within 15-30 minutes of confirmation, "investigating"; then updates every 30-60 minutes during Sev 1 even if nothing changed ("no change, next update at 14:30") **[F]**; state "identified", "fix in progress", "monitoring", "resolved" as separate stages. Each update has: what is affected, since when (with timezone), what customers can do, next update time. Facts only; no speculation about cause; no promises of root cause before it is known. After resolution: a short written post-incident summary within a few days: timeline, impact, cause in plain words, what changes, any credit under the SLA or terms. Pre-write the templates:
- Investigating: "We are investigating [symptom] affecting [who]. Since [time, TZ]. Workaround: [x/none]. Next update by [time]."
- Resolved: "[Service] is working again as of [time, TZ]. Cause: [one sentence]. Who was affected: [scope]. What we are changing: [one line]. [Credit, if applicable]. Details: [link]."
Reply to individual tickets in the incident with the macro and the status link; tag them to one parent so volume is countable; merge duplicates.

### 1.5 Cancellation
Goal: easy exit, one honest alternative. Confirm identity, confirm effective date and what is owed or refunded, state what happens to the data, then do it. Offer pause or downgrade once, only if relevant to the stated reason, in one sentence. No guilt, no hiding the button, no "call us to cancel" when sign-up was online, no retention loop longer than the sign-up. Skeleton: "Done: your subscription ends on [date]; you will not be charged again. [Refund, if any.] Your data is [kept until / deleted on]. If you would rather [pause / switch to X], reply and I will switch it, otherwise nothing more is needed." Record the reason in a tag for the VoC report. Law: `refunds-consumer-law.md` section 4 and 6.

### 1.6 Data-subject or privacy request (access, deletion, correction)
Do not answer substance from the queue. Same day: tag as privacy, forward to the privacy owner with the request text and receipt date; reply to the customer: "We received your request on [date], we will respond within [one month under the GDPR, art. 12(3), extendable if complex; the local deadline may differ]." Verify identity in proportion (ask the account owner via the login e-mail, not new documents unless needed). Never send data to an unverified requester, and never reveal another person's data in a response. After completion, confirm in writing what was done.

### 1.7 Abusive customer
Separate hard topic from abuse. Level 1: one calm boundary: "I want to help, and I will keep working on this; I will not continue if the messages contain insults." Level 2: written warning citing the policy, still resolve the underlying issue. Level 3: restrict channel or end the relationship per the written policy, approved by a lead. Threats of violence or self-harm go to the owner and safety path, not the normal queue. Protect agents: they may pause the chat and hand off; track abuse as a burnout signal (`diagnosis-playbook.md` Tree J). Do not retaliate, do not mock publicly.

### 1.8 VIP or B2B account
Same truth, faster routing. A named owner, direct channel, a shared incident status, a written escalation path, quarterly review of tickets by cause. Contracts may set SLAs and credits: read the contract before promising. Do not give VIPs facts others are denied; do give priority within published tiers. Keep a customer-visible log of open items with dates.

## 2. Macro writing and maintenance
Detail in `tone-and-macros.md`. Routine: every macro has an owner, a tag, a usage count, and a review date; monthly review of the top 10 by use and of those with low CSAT; delete if an article answers it; test each with a real ticket before release; version in a shared document, not personal snippets; never auto-send for money, privacy, safety, cancellation or emotional topics.

## 3. Triage routine (per shift, 15 minutes at the start)
1. Sort by oldest and by severity; check SLA due times for the next 2 hours.
2. Sev 1 and security or privacy tags first; page the owner.
3. Merge duplicates, link to open incidents, apply the macro.
4. Classify each new ticket: severity (impact and urgency), area, cause tag, owner, next action with date.
5. Spot spikes: more than [2x] the hourly baseline on a tag means look for a release or outage (`diagnosis-playbook.md` Tree E).
6. End of shift: hand-off note with open Sev 1 and 2, promises due tomorrow, and anything waiting on engineering.

## 4. Weekly support review (45 minutes)
Agenda: (1) numbers with definitions (volume, contact rate, backlog and age, first response and resolution median and p90, reopen and repeat rates, CSAT with n and reasons, refund and dispute counts); (2) the 5 biggest causes by tag and what happened since last week; (3) escalations open longer than the agreed age and linked customers; (4) macro and article changes (new, retired, wrong); (5) 3 tickets read aloud: one good, one bad, one unclear policy; (6) risks next week: releases, campaigns, holidays, staffing; (7) decisions and owners. Rule: end with at most 3 actions; leave out any metric nobody acted on.

## 5. Voice-of-customer report to product (monthly)
One page plus links. Content: period and volume vs contact rate; top 5 causes by ticket count and by customers affected (not only tickets), each with a representative anonymised quote, a link to the tickets or the engineering issue, an estimate of impact (customers, revenue at risk, agent hours using the staffing formula), and the proposed fix (product change, copy, article, policy); what was fixed since last report and the measured effect on contacts; trends in cancellation reasons; what support could not determine. Rules: customer words, no personal data, no verdicts on roadmap; separate facts from interpretation; the same format each month so changes are visible. Sizing: hours saved per month = tickets per month on the cause × minutes per ticket ÷ 60.

## 6. Incident communication template (internal handoff)

Incident: [id, title]. Severity: [N]. Start: [time TZ]. Status: investigating / identified / monitoring / resolved. Impact: [who, what, count]. Cause (known/unknown): [text]. Customer-facing text: [link]. Next public update: [time]. Support instruction: [macro name, tag, workaround]. Owners: incident lead, comms, support lead. Open questions: [list]. After: summary date, credits, follow-up issues.

Engineering side of the same incident (severity, roles, mitigation order, postmortem): `skills/cloud-deploy-ops/references/incident-response.md`.

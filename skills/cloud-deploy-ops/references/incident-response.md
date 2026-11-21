# Incident response (one owner for outages, data problems and breaches)

Use when production is down, degraded, leaking or losing data. Evidence tags: **[F]** read in a source this pass, **[M]** model judgement, **[U]** unverified. Project runbooks and on-call rules win over this file.

## 1. Declare early
Google SRE says to declare an incident when any of these holds: a second team is needed, customers can see the outage, or the problem is unsolved after about an hour of focused work **[F]**. Declaring costs little; a late declaration costs hours. Start the timeline at the moment of declaring, not when you feel organised.

## 2. Severity levels
Define them once, by customer impact, not by cause. A workable set **[M]** (PagerDuty and Atlassian publish similar ladders; the exact PagerDuty definitions were not read, Atlassian page not read):

| Level | Meaning | Response |
|---|---|---|
| Sev 1 | Core function down for most users, data loss or exposure, payments failing | Wake someone now; all hands; public status within 15-30 min |
| Sev 2 | Major feature degraded or one segment down, workaround exists | Respond within the hour; status update if customers notice |
| Sev 3 | Minor degradation, few users | Next working block; ticket, no status page |

When unsure, pick the higher level and downgrade later.

## 3. Roles
Google SRE separates four roles: incident command (holds state, assigns work, removes blockers; holds any role not delegated), operations (the only people changing the system), communication (updates stakeholders, keeps the incident document current) and planning (bugs, handoffs, tracking changes to revert) **[F]**. PagerDuty adds a scribe, a deputy and a customer liaison **[F]**.

Solo-founder version **[M]**: you are commander and ops. Do not also write customer text while debugging. Pre-write the status templates, set a 20-minute timer for each update, and if you have a second person (a friend, a contractor, support), give them comms and the timeline. Name who has authority to roll back without asking.

Handoff: the outgoing commander briefs the incoming one and stays until the new commander says "I have command" **[F]**. Rotate after a long incident; tired commanders decide badly.

## 4. Command post, timeline and decision log
One channel or document is the command post; keep it logged for the postmortem **[F]**. Put the current state at the top, then a time-stamped list (use one timezone, state it):

```
14:02 UTC alert: checkout 5xx > 5%
14:05 declared Sev 1, IC=A, ops=B, comms=C
14:09 hypothesis: deploy 8f3c; evidence: errors start 14:01, deploy 14:00
14:11 decision: roll back 8f3c (owner B); reason: fastest reversible step
14:16 rollback done; 5xx falling
14:30 monitoring; status page: monitoring
```
Log decisions with the reason and who decided, and log what you rejected. Record every manual change so it can be reverted later (the planning role) **[F]**.

## 5. Mitigate first, diagnose second
Stop the damage and preserve evidence before hunting the root cause **[F]**. Prefer reversible, fast steps in this order **[M]**:
1. Roll back the last deploy or config change (see `playbooks.md` for the platform rollback steps).
2. Turn off a feature flag or the failing integration; degrade gracefully (read-only mode, queue instead of call).
3. Scale or restart only if saturation is proven; scaling a bug just costs money.
4. Block: rate limit, firewall rule, disable a key or account, pause a cron or queue consumer.
5. Fix forward only when rollback is impossible (migration already applied, data format changed).
Before destructive actions (delete, restore over data) take a snapshot first. Capture logs, request IDs and a database snapshot before restarts erase them.

## 6. Communication cadence
- First public acknowledgement within 15-30 minutes of confirming customer impact, saying "investigating" **[M]**, consistent with `skills/customer-support/references/playbooks.md` sections 1 and 6.
- Update every 30-60 minutes in Sev 1 even with no news ("no change, next update 15:30").
- Each update: what is affected, since when (with timezone), what users can do, next update time. No speculation on cause.
- Stages are separate: investigating, identified, fix in progress, monitoring, resolved.
- Internal stakeholders get their own shorter channel so support does not guess. Wording, macros and credit policy live in `skills/customer-support`; do not duplicate them here.

## 7. Security incidents
If the cause may be an attacker, leaked secret or data exposure, change the posture: preserve evidence (do not wipe), limit who is in the channel, rotate exposed credentials after capturing state, and follow the containment and eradication playbooks in `skills/software-security`. NIST SP 800-61 Rev. 3 (April 2025) frames incident response inside CSF 2.0 risk management, with emphasis on preparation as well as detection, response and recovery **[F]** (landing page and abstract only; the full text was not read).
Legal clocks: if personal data is involved, start the notification analysis immediately; GDPR gives the controller 72 hours from awareness to notify the authority where required, and LGPD asks for notification within a reasonable time. Details, thresholds and templates are in the privacy law of the data subject's country (official regulator pages) **[M; not re-read here]**. Write down the moment of awareness in the timeline.

## 8. Close the incident
Resolved means metrics are back to baseline and stayed there for a defined window (for example 30 minutes), the temporary changes are listed, and customers were told. Then set the postmortem date (within 5 working days while memory is fresh) **[M]**.

## 9. Blameless postmortem
Triggers decided in advance: user-visible downtime above a threshold, any data loss, an on-call intervention such as rollback, long resolution time, or a failure of monitoring that needed manual discovery **[F]**. Blameless means assuming good faith with the information people had: "you can't fix people, but you can fix systems" **[F]**. Blame hides problems and stops escalation **[F]**. Still be direct about weaknesses.

Template:
```
Title, date, authors, status (draft/reviewed)
Summary (3 lines): what broke, impact, duration
Impact: users affected, revenue/data, support tickets
Timeline (UTC): detection, declare, mitigation, resolution
Detection: how found; how long before a human knew
Root causes and contributing factors (ask why five levels deep; systems, not people)
What went well / what went badly / where we got lucky
Action items: owner, due date, priority, ticket link, type (prevent/detect/mitigate)
Lessons and open questions
```
Follow-up: every action item has an owner and a date in the tracker; review open items weekly until closed; an unreviewed postmortem is effectively not written **[F]**. Share it with the team, and a customer-safe summary with customers when they were affected (never user data in it). Practise: run a tabletop or "wheel of misfortune" role play once a quarter **[F]**.

## Sources
Google SRE book, *Managing Incidents* and *Postmortem Culture* (sre.google); PagerDuty incident response guide (docs.pagerduty.com, table of contents only); NIST SP 800-61 Rev. 3. Status in `BIBLIOGRAPHY.md`.

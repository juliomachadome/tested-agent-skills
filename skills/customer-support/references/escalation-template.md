# Escalation to engineering: template and rules

Use for any problem support cannot solve alone. Engineers act faster on reproducible facts than on urgency words. Related: `playbooks.md` (incident text, triage), `diagnosis-playbook.md` (spikes).

## Template
- **Title**: [symptom] on [screen/endpoint] for [segment]. Not "urgent" or "broken".
- **Severity and impact**: Sev N; number of customers affected (and how counted), revenue or deadline at risk, data loss, money or security involved yes/no.
- **Environment**: app version or build, platform and OS or browser, plan, locale and timezone, feature flags, account id (internal only).
- **Steps to reproduce**: numbered, from a clean state; preconditions (account type, data).
- **Expected vs actual**: one sentence each.
- **Evidence**: timestamp with timezone, request or trace id, error message exactly as shown, log lines without personal data, screenshot or recording link.
- **Frequency**: always / intermittent (N of M tries) / first seen at [date, release].
- **Scope**: who is not affected (to narrow the cause); since which release if known.
- **Workaround**: yes/no and what.
- **Tried**: what support already did (reinstall, other device).
- **Customer promise**: what we told the customer and when the next update is due.
- **Linked tickets**: ids and count; the count is updated as new tickets arrive.
- **Guesses**: labelled as guesses, separate from facts.

## Rules
One issue per report. If you cannot reproduce, say so and attach what you have, including what you tried; do not guess a cause. Never paste secrets, tokens or full personal data. Set a review time: if engineering has not triaged a Sev 1 or 2 within the agreed window, escalate to the owner by name. When resolved, engineering updates the issue so support can notify every linked customer and update the macro and article. Keep a list of known issues for the whole team, visible in the triage view.

## Worked mini-example (vague ticket turned into a report)
Ticket: "app broken since yesterday". Questions to ask the customer in one message: which device and OS version, app version, what exactly happens (screen, message), time of last success, whether another device works, and a screenshot. Report after answers: Title: purchase restore fails on iOS [version], Sev 2, 14 customers in 3 days (count by tag), steps 1-4, expected "purchases restored" vs actual "no purchases found", request ids, workaround: reinstall did not help, tried: logout/login; first seen after release [x] (verify), linked tickets [ids].

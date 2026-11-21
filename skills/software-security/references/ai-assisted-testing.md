# AI-assisted security testing of your own app

An AI agent is a tireless junior tester for software you own or are engaged to test: it widens coverage between human reviews and replaces none. Defensive use only; no payloads, no evasion. Tags as in `SKILL.md`. Sources: B7, B8, B10, B80 to B83 in `BIBLIOGRAPHY.md`.

## 1. Authorisation and scope (before anything runs)

Open-source agent projects of this kind state the same rule: test only systems you own or have explicit written permission to test, inside the agreed scope, and the operator carries the responsibility [B80, B81] **[C]**. Write a one-page rules of engagement and keep it with the run:

- **Who authorised, for what:** owner name, date, signed engagement letter for third-party systems. Hosting and SaaS providers have testing policies; third-party APIs your app calls are out of scope unless their terms allow it.
- **Targets allowlist:** exact hostnames, base URLs, API specs, repos. Everything else is denied, including links the agent discovers. Enforce this in the network (egress allowlist), not only in the prompt.
- **Environment:** an isolated staging or preview deployment with seeded fake data and its own credentials. Never production data, never a shared database, never real payment keys or real e-mail/SMS senders (use sandbox modes or sinks).
- **Accounts:** one test account per role and two tenants (A and B), giving access-control checks a victim and an attacker.
- **Limits:** request-rate cap, a maximum run time and token budget, a named human who can stop the run, and forbidden actions (mass deletion, messages to real people, load or denial-of-service tests, third-party hosts).
- **Agent hygiene:** run the agent in a disposable container with no access to your source-control credentials, cloud keys or personal files. Its secrets are test-only and short-lived. Target responses are untrusted input to the agent: a page can try to instruct it (`llm-engineering`).

## 2. What agents do well and badly

| Does well [F] | Does poorly [F] |
|---|---|
| Recon: route and parameter inventory from OpenAPI, a sitemap, the repo or the browser; forgotten debug and old-version paths | Business logic: pricing rules, refund and entitlement state machines, "who is allowed to do this in our company" (`business-logic-payments.md`); it lacks your intent |
| Broken access control and IDOR: replay each request as role B, tenant B, anonymous, and compare | Severity in context: a real bug behind an unused feature flag reads like a critical |
| Injection probes and error-handling differences across many inputs; authentication and session flow checks (cookies flags, token reuse, logout, reset links) | Long chains needing human judgment or out-of-band access (e-mail, hardware, a second device) |
| Breadth across OWASP Top 10 and API Top 10 classes [B7, B8] | Honest negatives: "found nothing" proves little unless the log lists what was tried |
| Writing a reproduction as a script or an HTTP trace you can re-run | False positives: a plausible bug it never confirmed, or a 200 with an error body taken as success |

Agent projects in this space give specialised agents a request proxy, a browser, a shell and a scratch interpreter, and share findings between them [B80] **[M]**. Idea worth taking: real tools, and a validator separate from the finder.

## 3. Proof before report

A finding exists once someone other than the finder reproduces it. Gate every candidate:

1. **Reproduce** in a fresh session with the stated accounts; two successes out of two tries (a race needs more).
2. **Minimal proof:** the smallest request sequence showing the impact on your own test data (A's row visible to B; a state changed that should not). Use benign markers and stop: at most one record, no persistence, no pivoting.
3. **Root cause in code:** file:line, or "not located". An agent finding with no code location goes to "not verified".
4. **Severity:** a simple scale as in `SKILL.md`, or CVSS v4.0 if a consumer needs a number; label it with the metric groups used (Base-only says little about your setting); bands: Low 0.1 to 3.9, Medium 4.0 to 6.9, High 7.0 to 8.9, Critical 9.0 and up [B82] **[C]**. Then adjust for data class, tenant crossing, auth needed and internet exposure.
5. **Dedupe** by route plus root cause against open tickets and earlier runs.
6. **Record failed validations;** they feed the false-positive rate (section 6).

Report per finding: title, category (A01:2025, API1:2023), route, accounts, steps, observed versus expected, impact, location, severity with reasoning, fix, regression test, run log and commit hash for replay. Store reports like any vulnerability list (restricted access, short retention).

## 4. Triage and fix verification loop

1. Human triage within a working day: confirm, downgrade, mark duplicate, or reject with a reason fed back to the agent's instructions.
2. Open a ticket per confirmed finding with owner and due date by severity; Critical or High blocks release (`playbooks.md` 8).
3. Fix at the class level where possible (central guard, default-deny policy, allowlist), written as a test that failed before.
4. **Re-run the exact proof** against the fixed build; then rerun the neighbouring routes (bugs have siblings). Close only when the proof fails and the regression test is in CI.
5. Keep a ledger (finding, status, fix commit, re-test date); suppressions carry an owner and expiry.

## 5. Putting it in CI on preview deployments

- Run on each preview or a nightly staging build, not on production and not on every commit. A pull-request run can focus on changed routes; give the job full history so it can see what changed [B80] **[M]**.
- The preview must be isolated: its own database and fake data, secrets distinct from production, and an egress allowlist.
- Fail the job only on confirmed findings of Medium or above; send unconfirmed candidates to a report, not to the merge button. Failing on every unproven suspicion trains people to ignore the job.
- The agent's API key is a CI secret with a spend cap; the job cannot write to the repository or production.

## 6. Cost and noise control

- Budget per run: maximum tokens, wall-clock time and requests; stop the run, do not extend it silently. Quick profile on pull requests, deep one weekly on staging.
- Narrow the target: API spec, role matrix and the three riskiest flows (payment, invite, export), not "test everything".
- Record per run: findings confirmed, rejected, duplicates, cost, minutes of human triage. Track precision (confirmed / reported); under about half, tighten instructions or narrow the classes **[F]**.
- Keep rejections as short exclusions ("route X is public by design") in version control.

## 7. How it fits with the rest

| Layer | Finds | The agent adds |
|---|---|---|
| Code review and threat model (`playbooks.md` 1, 2) | design flaws, intent, missing checks | cheap second look at runtime behaviour |
| SAST, secret scan, SCA (`supply-chain-secrets-logging.md`) | patterns, leaked keys, known-vulnerable packages | confirms whether a pattern is reachable from outside |
| DAST and header scan | known misconfigurations, scripted probes | adaptive login flows, role comparison, chained steps |
| Human pentest | creative chains, business abuse, social and physical paths | more regression coverage between engagements |

None substitutes for another. A clean agent run is not a security statement; say "no confirmed findings in the tested scope on date X with version Y" and list what was not covered **[F]**. Keep the human pentest for major releases, new trust boundaries and compliance, and hand the tester the agent's last report so paid hours go where agents are weak. Planned assessments follow classic testing guidance [B83] **[C]**; test cases from [B10].

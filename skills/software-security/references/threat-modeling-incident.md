# Threat modeling and incident response

Format: **rule** · why · source id (see `sources.md`) · example.

## 1. Threat model in 30 minutes

Meeting format and abuse-case worksheet: `playbooks.md` 1; breach run sheet: `playbooks.md` 7. Use it for a new feature, a new integration, a new trust boundary (a new provider, a new upload path, an AI step), not for every diff.

1. **Answer the four questions:** what are we working on, what can go wrong, what are we going to do about it, did we do a good enough job. · W17
2. **Sketch the data flow:** external entities (browser, partner, provider), processes (front-end server, API, worker), data stores (database, bucket, cache, vector index), flows, and **trust boundaries** (browser ↔ server, server ↔ provider, tenant ↔ tenant, user content ↔ instructions). Most high-impact bugs sit on a boundary. · W17
3. **Walk STRIDE per element and flow:** Spoofing (authentication), Tampering (integrity), Repudiation (accountability), Information disclosure (confidentiality), Denial of service (availability), Elevation of privilege (authorization). · W17
4. **Rank by likelihood and impact, consider the cost of the fix, choose a response:** mitigate, eliminate, transfer or accept, and write the residual risk. Turn each mitigation into a testable requirement. · W17
5. **For personal data, add LINDDUN:** Linking, Identifying, Non-repudiation, Detecting, Data disclosure, Unawareness, Non-compliance. It finds privacy harms STRIDE misses (e.g. joining two "anonymous" datasets re-identifies people). Hand the legal side to the privacy law of the data subject's country (official regulator pages). · W18
6. **Update the model when the system changes;** keep it next to the design doc, one page. · W17

Template (keep it short):

```
Feature: <name>        Date: <yyyy-mm-dd>
Flow: browser -> API -> DB / bucket / provider X
Boundaries: browser|API, API|provider X, tenant|tenant
Threats (STRIDE): S: ...  T: ...  R: ...  I: ...  D: ...  E: ...
Top 3 by risk: 1) ... -> mitigation + test   2) ...   3) ...
Accepted: ... (why, review trigger)
```

Typical abuse cases to seed the list: user of tenant A requests B's object by id, search, reused URL; role without permission approves or reads a draft; tenant or role sent in the body; document or message with embedded instructions; huge or mislabeled upload; duplicate parallel approvals and job replays; personal data sent to a provider that trains on it.

## 2. Incident response for a small team

NIST SP 800-61r3 (April 2025) frames incident response inside the CSF 2.0 functions and lets each organization use the life cycle that fits. Below, the one-person version. · W24

**Before (one afternoon):**
- Contact list and dashboards: database, hosting, payments, email, DNS, registrar; where each "rotate key" button is.
- Secrets inventory (see `supply-chain-secrets-logging.md`) and one tested backup restore.
- Alerts that reach a phone: API down, webhook failing, error spike, media-issuance spike.
- Access to the data-protection authority's breach form tested (check the data-protection authority of the data subject's country).

**During (in this order):**
1. **Contain:** revoke the suspicious credential, switch off the route or feature by configuration, block the account. Containment comes before understanding.
2. **Preserve:** export logs and note times before retention deletes them. Do not "clean" anything yet.
3. **Measure:** which data, how many people, for how long, who accessed it.
4. **Start the legal clock:** when you have reliable knowledge that personal data was affected, the notification deadlines start (GDPR 72 hours to the authority; Brazil: LGPD art. 48 leaves the time to the ANPD, whose Res. 15/2024 sets 3 business days). Decide and write down why you notify or not. Details in the privacy law of the data subject's country (official regulator pages).
5. **Fix** the cause with a test that reproduces it; **rotate** every secret the compromised credential could reach.
6. **Notify** affected people when risk is high; tell the payment provider if charges are involved.

**After:** an incident record (facts, effects, measures, including incidents you did not notify), one new rule or test, no blame. · W24, W11

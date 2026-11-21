---
name: growth-analytics
description: Use for any product or growth analytics task, even short ones - North Star and input metrics, tracking plans and event naming, funnels, activation and retention cohorts, A/B tests ("is this significant", "sample size", peeking, sample-ratio mismatch, guardrails), unit economics (CAC, LTV, payback), attribution limits (platform vs analytics vs holdout tests), and privacy-safe measurement with consent. Triggers - "why did conversion drop", "signups up but activation down", "the A/B winner did not hold", "dashboards disagree", "CAC is rising", "which metric should we track", "analytics without cookies", or pasted numbers or a metrics export, even without the word growth. Diagnoses data trust first, shows the arithmetic, states uncertainty, no p-hacking. Not for buying media or ad structure (paid-traffic), feature discovery and roadmap (product-management), page copy (copywriting), price design (offers), or general SQL, data cleaning and ad-hoc analysis (data-analysis).
license: CC-BY-SA-4.0
metadata:
  author: Júlio Machado
  source: https://github.com/juliomachadome/tested-agent-skills
---

# Growth analytics

Measure to decide something. A metric without a decision attached is decoration. A few trusted numbers with definitions beat many dashboards. Most "growth problems" that arrive as a chart are first data problems, so check the data before explaining it.

Evidence tags: **[C]** consensus or law · **[M]** serious but single, practitioner or correlational · **[F]** vendor claim or rule of thumb · **[X]** myth. Loop and growth-model frameworks from vendors are vocabulary **[F]**. Sources and their check status: `references/BIBLIOGRAPHY.md`.

## 1. Start: project first, then the data
Read the current project's docs first: business model, glossary and metric definitions, existing events, analytics tool and warehouse, consent setup, legal context (GDPR, LGPD, CCPA). Project rules override this skill. Then fix in five lines: the decision this analysis serves; the metric with definition and period; the population (who, where, when); the change calendar (releases, campaigns, price, banner, outages); the second source of truth (database counts).

Ask for, by task: **metrics question** - event export or SQL access, definitions, period, calendar of changes. **A/B test** - design split, unit, planned n and duration, metrics, counts per arm, daily readings if peeked. **Tracking** - product flows, existing events, tool, consent banner. **Unit economics** - ARPA, gross margin, churn by cohort, full CAC components, cash. If missing, state the assumption; small traffic changes what is testable (section 6).

## 2. Which reference to open
| Situation | Open |
|---|---|
| Something moved or looks wrong (conversion, activation, retention, CAC, test winner, SRM, dashboards disagree, seasonality) | `references/diagnosis-playbook.md` (Step 0 data trust, then the tree, worked math) |
| Build a routine (North Star tree, tracking plan, experiment design doc, weekly review, cohort and funnel SQL, attribution reading, consent checks) | `references/playbooks.md` |
| Event table and naming template | `references/tracking-plan.md` |
| Quick test rules, sample size formula, ship criteria | `references/experimentation-notes.md` |
| CAC, LTV, payback, cohort economics, cash, lifecycle triggers | `references/unit-economics-lifecycle.md` |

## 3. Diagnose first
Run `diagnosis-playbook.md` top-down. **Step 0**: is the data trustworthy: tracking breaks, consent drops, bot traffic, timezone, double counting, UTM loss, ad blockers, sampling, definition drift. When the export and the database disagree by more than about 5%, explain the gap before the metric **[F]**. Then pick the tree (conversion drop; signups up but activation down; worse retention in newer cohorts; test winner did not hold; SRM; attribution disagreement; rising CAC; LTV:CAC fine but cash short; North Star up and revenue flat; sudden step drop after a release; dashboards disagree; seasonality). Each gives causes, the check that separates them and the fix.

## 4. North Star, activation, retention, funnels
- **North Star**: one number for value delivered per period, a lead of revenue, movable by the team, hard to game; 3-5 inputs (breadth, depth, frequency, efficiency) with owners and guardrails; one page **[M]**. Routine: `playbooks.md` 1.
- **Activation**: found from data (which early actions separate retained from churned users), confirmed qualitatively, reported in a fixed window. Correlation is a hypothesis until tested.
- **Retention**: cohort table by signup week on the core action, not login; read the shape (flattening is a retained base, a curve to zero is no fit); compare equal ages only; never read incomplete cells; segment by channel and plan **[C]**.
- **Funnels**: ordered steps with a window, step and cumulative rate, median time between steps; the largest absolute loss first. A funnel shows where, not why. Show denominators and intervals; hide cells under about 30 users.

## 5. Tracking, attribution, privacy
- **Tracking plan** in the repo: event, trigger, typed properties, side (server for money and state, client for UI), consent category, PII flag, owner, decision served, version. object_action, past tense, few events, rich properties; identity rules written; CI schema checks; volume alerts; weekly reconcile with the database **[C]**. `playbooks.md` 2.
- **Attribution**: platform numbers overlap and self-attribute; last-click over-credits the bottom; consent and blockers lose data **[C]**. Triangulate platform, first-party analytics, self-reported source, and holdout or geo tests and media-mix models when spend allows **[M]**. Report a range and the method. Spend decisions: `skills/paid-traffic`.
- **Privacy**: non-essential device storage or access needs consent in the EU (ePrivacy art. 5(3)); some regulators exempt strictly limited audience measurement, check the local text **[C]**; GDPR names online identifiers, LGPD covers identifiable people (art. 5 I); server-side tracking is not a consent bypass; log consent state with events; minimise. Checks: `playbooks.md` 7; law: the privacy law of the data subject's country (official regulator pages). Not legal advice; flag doubts for the owner or counsel.

## 6. Experimentation
Core from Kohavi, Tang and Xu **[M]**: (1) hypothesis, one primary metric, guardrails and decision rule written before launch; (2) randomise at the unit of the metric; (3) compute n per arm from baseline, MDE, alpha 5% and power 80% (4% to 5% needs about 6,745 per arm; formula in `diagnosis-playbook.md`); (4) whole weeks, stop at the planned size, no early stop on a lucky p-value, use a sequential design if looking early is required **[C]**; (5) check SRM first (chi-square, alarm p < 0.001) and fix before reading anything **[C]**; (6) guardrails and segments as hypotheses, correct for many metrics; (7) novelty, winner's curse and Twyman's law: a too-good result is a bug until shown otherwise; (8) confirm with a post-launch holdout; record nulls. Variance reduction (CUPED) and sequential testing are options, see `playbooks.md` 3. Low traffic: bigger changes, qualitative evidence, pre/post with a matched control, stated as such. Do not test legal or consumer-protection text for conversion at the expense of clarity.

## 7. Unit economics and growth process
CAC loaded and cohort-matched; LTV = ARPA x gross margin / churn, a model, cap the horizon; payback simple and churn-adjusted; read ratio, payback and cumulative cash together **[C]**. Ranges (LTV:CAC near 3, payback under about 12 months) are rules of thumb **[F]**. Details: `unit-economics-lifecycle.md`. Process from *Hacking Growth*: align on the North Star, weekly cadence of ideas, prioritise, test, analyse, systematise **[M]**; fix activation and retention before spending on acquisition **[M]**. Loops are modelled by conversion per step and cycle time **[F]**.

## AI tells to avoid (check while answering, not after)
- Generic advice ("improve onboarding", "segment your users") not tied to the user's numbers.
- Benchmarks (conversion, retention, LTV:CAC) stated as fact without source and date.
- "Significant" or "the variant won" with no test, n, interval or planned stopping rule.
- Listing AARRR, North Star and every metric without applying one to this product's decision.
- "Test everything": no hypothesis, primary metric, MDE or stop rule.
- Option lists with no prioritised pick.
Fix: use the user's data, show the arithmetic, state the uncertainty, give one recommendation with its reason and the next check.
Say what you chose and why in one line; a choice without a reason is removed.

## 8. Output
Match the request: metric tree, tracking-plan table, diagnosis (data used and trust level, numbers with intervals, most likely and second cause with the check that separates them), experiment design or readout (effect with interval, SRM check, guardrails, decision, caveats), or a unit-economics table. Always end with: the decision or next action with owner; the cheapest next test; evidence level of each claim; what you could not verify (missing data, consent effect, unverified source). Never present a number without its definition and period.

## References
`references/BIBLIOGRAPHY.md`. Related skills: data-analysis, paid-traffic, product-management, pricing, copywriting, customer-support, sales.

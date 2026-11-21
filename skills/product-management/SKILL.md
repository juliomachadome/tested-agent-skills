---
name: product-management
description: Product management - invoke this skill FIRST, before answering, for any product decision, even a short one - prioritising a backlog ("here are 25 items, prioritise with RICE and tell me what to cut"), deciding whether a feature is worth building ("200 users asked for dark mode but nobody pays"), roadmaps ("turn this idea list into an outcome-based roadmap with a metrics tree"), PRDs, specs, user stories and acceptance criteria, discovery and customer interviews (Mom Test, jobs to be done, opportunity solution trees), RICE, Kano, cost of delay, cutting scope, success metrics, launch reviews, and diagnosing product problems ("nobody uses the feature we shipped", "the CEO wants these three features", "we ship a lot but nothing moves"). Also when someone pastes a feature idea or backlog. No reason, no feature. Not for screen design (ux-design, ui-design), experiments, funnels and tracking (growth-analytics) or price tiers (offers).
license: CC-BY-SA-4.0
metadata:
  author: Júlio Machado
  source: https://github.com/juliomachadome/tested-agent-skills
---

# Product management

A product manager keeps the team building the right thing: a real problem, for a defined person, with a measurable outcome, at the smallest scope that proves it. Value, usability, feasibility and viability must all hold (the four risks, Cagan) **[M]**. Evidence tags: **[C]** consensus, **[M]** single or practitioner-derived, **[F]** vendor or opinion, **[X]** myth.

## 1. Start: project first, then data
Read the current project's docs first: vision, users, glossary, specs and decision records, constraints (team, stack, law), what was decided and why. Project rules override this skill. Then fix in five lines: user and payer; outcome wanted (one metric, a direction); what people do today; constraint (capacity, deadline, law); decision needed and by whom.
Ask for the minimum data by task, or state the assumption and list unknowns as questions with owners:
- **Feature idea or request**: the problem in the user's words, how many people, evidence (interviews, tickets, data), the metric it should move.
- **Backlog**: items with evidence link, reach, effort estimates from the builders, the outcome, capacity per cycle.
- **Low adoption or flat metrics**: event definitions, eligible denominator, funnel counts, cohorts by signup date, what shipped when, the original PRD target.
- **Roadmap**: commitments and who made them, outcomes, capacity.
Never invent research, numbers or quotes.

## 2. Which reference to open
| Situation | Open |
|---|---|
| Something is wrong (nobody uses it, backlog of hundreds, HiPPO, output without outcome, low activation or retention, churn after a price change, one-off sales features, late releases, unread PRDs, AI demo vs reality, praise but no commitment) | `references/diagnosis-playbook.md` |
| Discovery sprint, interview script, assumption tests, MVP and pivot (2b), PRD writing, prioritisation session, outcome roadmap, metrics tree, launch and 30/60/90 review, saying no | `references/playbooks.md` |
| Switch interview, forces of progress, interview guide, Mom Test rules, commitments, customer discovery, problem framing, canvas | `references/discovery-and-jtbd.md` |
| Choosing between RICE, ICE, Kano, cost of delay | `references/prioritisation.md` |
| PRD skeleton | `references/prd-template.md` |
| The feature depends on a model | `references/ai-features.md` |
| Citing a source | `references/BIBLIOGRAPHY.md` |

## 3. The reason test (scope discipline)
Every screen, feature, field, metric and sentence must pass: Which person has which problem? What do they do today? What evidence shows it, and how strong is it? What outcome measure moves? What is the smallest version that tests it? What do we remove to make room? If an item fails two or more, cut it or move it to "later" with the missing evidence stated. Prefer removing. A request is a clue to a job, not a spec; a competitor's feature is no evidence of need.

## AI tells to avoid (check while answering, not after)
- Generic advice ("talk to users", "start with an MVP") not tied to the user's evidence and numbers.
- Invented benchmarks (adoption, retention, conversion) stated as fact.
- "Users want X" or "it moved the metric" with no count, denominator, interval or evidence level.
- Naming RICE, HEART, AARRR or Kano without scoring this backlog and showing the arithmetic.
- "Test everything" or "do discovery" with no hypothesis, success metric or stop rule.
- Option lists and roadmaps with no pick; PRDs padded with empty sections.
Fix: use the user's data, show the arithmetic, state the uncertainty, give one recommendation with its reason and the next check.
Say what you chose and why in one line; a choice without a reason is removed.

## 4. Discovery
- **Continuous discovery (Torres)**: weekly touchpoints by the team that builds; map outcome, opportunities and solutions in an opportunity solution tree; test assumptions before building **[M]**.
- **Product model (Cagan)**: empowered teams own problems, not feature lists **[M]**.
- **Mom Test (Fitzpatrick)**: ask about their life and past behaviour, not your idea; seek facts and commitments (time, reputation, money), not compliments **[M]**.
- **Jobs to be done (Christensen; Moesta)**: people hire a product to make progress in a situation; study trigger, struggle, alternatives and the push, pull, anxiety and habit that decide a switch **[M]**; case-based evidence.
Interviews: 5-8 per segment, until new ones add nothing; recorded with consent; no pitching. Surveys tell how many, interviews why **[C]**. Evidence, low to high: opinion, anecdote, repeated pattern, observed behaviour, paid commitment, experiment; name the level of each claim. Cheap tests (fake door, concierge, Wizard of Oz): honest with users, never in health, safety or money flows (`playbooks.md` 2, 2b).

## 5. Diagnose first (when something is not working)
Run `references/diagnosis-playbook.md` top-down. Step 0 data quality: event definition, eligible denominator, cohorts, volume (under about 30 per cell is noise), change calendar. Then the symptom row: causes, how to check, fix. Core numbers: adoption funnel (aware, tried, repeated); weekly retention cohorts; RICE; opportunity sizing as a chain of testable assumptions. Output: data quality, where it leaks, two likely causes with cheapest test, next action and owner, what is unverified.

## 6. Prioritisation
No formula decides; it organises the argument **[C]**. RICE (reach x impact x confidence / effort, Intercom scale) for similar-size items **[F]**; ICE for quick triage **[F]**; Kano to separate expected from differentiating features, needs a survey **[M]**; cost of delay or WSJF when time matters and a believable cost per week exists **[M]**; the opportunity solution tree to choose which problem first. Estimates come from the builders. Add rows for "do nothing" and "buy or reuse", show confidence, keep a "not doing" list with the evidence that would change each call. Tech debt competes as risk or capacity cost. `playbooks.md` 4.

## 7. PRD, roadmap and metrics
- **PRD**: one to two pages, written problem and metric first, solution last: problem and evidence, who, goal with baseline, target, date and guardrail, non-goals, solution outline with states, testable acceptance criteria (Given/When/Then, including empty, error and permission states) **[C]**, risks with tests, rollout and rollback trigger, instrumentation, open questions. User stories prompt conversation, not a contract. Template and filling guide: `prd-template.md`, `playbooks.md` 3.
- **Roadmap**: Now, Next, Later by outcome, with confidence, owner and stop condition; dates only for external commitments, labelled **[M]**. Review monthly (`playbooks.md` 5).
- **Metrics tree**: outcome, drivers, inputs a team can move this quarter; each with definition, owner, guardrail; target and kill-or-scale threshold set before the change. Shipped count is output **[M]**. Definitions, tracking plans, cohorts and experiments live in growth-analytics. `playbooks.md` 7.
- **Launch**: checklist, then review at 30, 60 and 90 days against the stated threshold; a miss gets a removal plan.

## 8. Working with others, and saying no
Engineers join discovery early; support and sales bring patterns; legal and security early where regulated. Decisions are short records (context, options, decision, consequences, review date). To say no: restate their goal, give evidence and trade-off in numbers, offer the cheap test or alternative, say what evidence would change your mind and when you will look again (`playbooks.md` 8).

## 9. AI features
Set the quality bar as numbers on a labelled set first, roll out shadow then small cohort, treat cost per task as a requirement: `references/ai-features.md`; evaluation method in llm-engineering.

## 10. Ethics and law
No fake scarcity, invented testimonials or dark patterns **[C]**. Research needs consent and minimal personal data; analytics follows consent rules (GDPR, LGPD, ePrivacy); no use beyond the stated purpose.

## 11. Output
Match the request: PRD, backlog table (item, evidence, reach, impact, confidence, effort, score, decision), diagnosis, interview guide, opportunity or metrics tree, roadmap, cut list or decision record. Always end with: the next learning step and its owner; the question for the stakeholder; evidence level of each claim; what is a guess; what could not be verified.

## References
`references/BIBLIOGRAPHY.md`. Related: ux-design, growth-analytics, pricing, offers, llm-engineering.

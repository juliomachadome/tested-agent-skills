---
name: ux-design
description: Usability and accessibility of flows and screens - invoke this skill FIRST, before answering, whenever someone asks to review a screen, form or flow, rate usability problems by severity, check WCAG or keyboard and screen-reader access, or decide an interaction (confirm dialog vs undo, empty, loading and error states), even a short one. Examples - "review this settings screen for usability problems and rate each by severity", "our signup form has 11 fields and users bounce", "delete selected, confirm dialog or undo toast", "check the dashboard against WCAG 2.2 AA, target size 2.5.8", "how should our chatbot show sources", "why do users drop off at checkout", "make this form accessible". Also usability tests, heuristic evaluation, card sort, forms (Baymard), ARIA patterns, SUS, product-type variants (SaaS, e-commerce, mobile, marketplace, AI chat). Not for colours, type or tokens (ui-design), speed (web-performance), activation metrics (growth-analytics) or free aesthetic direction (frontend-design).
license: CC-BY-SA-4.0
metadata:
  author: Júlio Machado
  source: https://github.com/juliomachadome/tested-agent-skills
---

# UX design: flows, screens, accessibility, AI features

A screen is good when a person finishes the task, knows the state, and recovers from mistakes without help. Laws of UX are heuristics; when a law and a real-user test disagree, the test wins.

## Principles (the why)

1. **One focus per screen.** Decision time grows with the number and complexity of options (Hick); a highlight works only if little else is highlighted (Von Restorff). One primary action, the recommended option marked; never cut options the task needs.
2. **State is shape plus icon plus color, never color alone** (WCAG 1.4.1).
3. **Show status, give a way out.** Over about 1 s show activity; over 10 s show percent or named steps and a way to interrupt (NN/g). Reversible actions get Undo; irreversible ones get a confirm that names the effect.
4. **Prevent first, explain second.** Constraints, safe defaults, a preview of consequences; when errors still happen, say what, why and what to do, next to the field, with input preserved.
5. **Preview before writing in bulk:** how many, which, remove items, write once, one undo.
6. **The model proposes, the person decides.** AI output is a sourced, editable, dismissible draft; uncertainty and abstention are information.
7. **Native first.** Use the platform control before ARIA (first rule of ARIA). A role is a promise of keyboard behavior you must build.
8. **Say it once, name it once.** One fact in one place, one verb per act (Occam, Jakob, Norman).
9. **Cite evidence grade.** Many "rules" are myths (7 plus or minus 2, 3 clicks); give source and limit.

## Step 1: project first, then product type

1. Read the project's CLAUDE.md or AGENTS.md, design system, glossary, ADRs and last UX review. Project rules win; say which you applied.
2. Choose the product type from the repository and the request (`references/product-types/README.md`): saas-b2b, ecommerce, mobile-app-consumer, marketplace, content-media, education-learning, fintech-health-regulated, developer-tools, games-gamified, ai-assistant-chat. Open it (jobs, pitfalls, metrics, checklist). Mixed: regulated rules win. None fits: say so.
3. For a symptom (drop-off, tickets, "nobody finds it"), do Step 0 of `references/diagnosis-playbook.md` (who, task, context, evidence) before designing.

## Which reference to open

Checkout and paywalls: by the pay button show item, total today with tax, renewal price and date, how to cancel; official wallet buttons (source 111); a bare "you agree to the Terms" is not enough (real test, 18/11) **[C]**; law to offers.
AI tells to avoid (while reviewing or designing): generic heuristic lists not tied to this screen, severities with no user impact, invented stats, "best practice" with no evidence, one-size answers ignoring the product type. Say what you chose and why in one line; a choice without a reason is removed.

| Situation | Open |
|---|---|
| Symptom: drop-off, not found, tickets, mis-taps, a11y complaint, empty search, notification fatigue, dark pattern; funnel and SUS maths | `references/diagnosis-playbook.md` |
| Usability test, heuristic evaluation, form checklist, accessibility audit, card sort, tree test, flow copy, critique, handoff | `references/playbooks.md` |
| Citing a law or heuristic, severity, is it a myth, classics | `references/laws-and-heuristics.md` |
| WCAG criteria, keyboard, focus, targets, dialog, combobox, status messages, ARIA | `references/accessibility-wcag22.md` |
| Forms, checkout, tables and bulk actions, empty, loading, error states, undo vs confirm | `references/forms-states-feedback.md` |
| AI output on screen: citations, confidence, abstention, drafts, streaming | `references/ai-features-ux.md` and `product-types/ai-assistant-chat.md` |
| Running a review, finding format, per-screen checklist, mobile vs desktop, habit ethics | `references/review-method.md` |
| Recurring defects (28 anti-patterns) | `references/real-screen-lessons.md` |
| The without-reading test, script, pass/fail | `references/understand-without-reading.md` |
| A tour, spotlight or first-run hint is proposed | `references/guided-tours.md` |
| Source, edition, read date, V/P status | `references/BIBLIOGRAPHY.md` |

Evidence tags in the references: [C] consensus or standard, [M] single or correlational study, [F] practitioner rule, [X] myth.

## Workflow

**Designing**
1. Write the goal in one sentence, the starting state (knowledge, device, interruptions) and one observable success criterion.
2. List steps and count them; drop every step and field with no use. Ask only for what you cannot derive (WCAG 3.3.7).
3. Per screen: the one primary action, then every state (empty, loading, partial, error, success, offline, denied). A missing state is a defect.
4. Name dangerous actions and choose Undo or confirm for each.
5. Run the checklist and the without-reading test on the mock or build; hand styling to `ui-design`.

**Reviewing**
1. Capture each relevant state at about 390 px and 1280 px; do a keyboard-only pass, 200 percent zoom and 320 px reflow.
2. Run the without-reading test on the screenshots.
3. Walk the 10 heuristics, then the checklist, then `real-screen-lessons.md`, then the accessibility criteria that apply.
4. Write findings below with severity 0-4 and evidence; verdict per platform. Severity 3 or 4 blocks approval.

## Quick decision rules

- **Confirm or undo?** Reversible: do it and offer Undo (also in history). Irreversible, costly or affecting others: confirm, naming item and effect, buttons as outcomes, safe choice focused. Many confirms get clicked through.
- **Toast or inline?** Toasts only for passive success; errors stay inline.
- **Spinner or progress?** Under 1 s nothing; 2-10 s labeled spinner; over 10 s percent or named steps plus cancel. Never invent estimates.
- **Disabled button?** Prefer active with errors on press, or disabled with the first missing thing stated beside it.
- **AI answer without a source?** Abstain or label it an unsourced draft.

## Checklist (every screen)

- [ ] In 3 seconds: where am I, what is the one primary action; the without-reading test passes.
- [ ] States designed: empty (distinct from loading), loading, error, success, offline.
- [ ] State by shape or icon plus color plus text; contrast 4.5:1 text, 3:1 components.
- [ ] Keyboard reaches everything; focus visible, not hidden by fixed bars; order matches visual order.
- [ ] Targets at least 24x24 CSS px (WCAG), about 44 px on touch.
- [ ] Forms: visible labels, correct `type`/`autocomplete`, inline errors, input kept, no redundant entry.
- [ ] Dangerous actions per the rules above; the destructive one is never the default or primary.
- [ ] No contradicting counters or repeated facts; one verb per act.
- [ ] AI output: sources one step away, uncertainty visible, editable, person confirms.
- [ ] 320 px reflow, 200% zoom, reduced motion, `lang` set.

## Finding format

```
UX-<n> | severity <0-4> | <screen / state / viewport>
Problem: what the person experiences
Cited: heuristic or law, WCAG criterion if any
Evidence: screenshot path or steps
Fix: one concrete change
Accept when: observable criterion
```
End with a verdict per platform (good / acceptable / weak; ship / ship after fixes / block) and what was not checked. Keep it ranked, separate code reading from screen observation, never claim an unmade observation.

## Boundaries

- Colors, type scale, tokens, dark mode, motion style: `ui-design`. Page speed and Core Web Vitals: `web-performance`. Free aesthetic direction: `frontend-design`.
- How feedback, animation and interface sound move and are built: `web-motion` (which feedback to give stays here).
- Activation metrics, funnels, lifecycle messaging: `onboarding`, `growth-analytics` (this skill covers screen-level UX). Persuasive copy: `copywriting`.
- Automated browser accessibility audits: the chrome-devtools a11y-debugging skill; this one covers manual judgment.

## Gaps

- Apple HIG (44 pt) and Material 3 (48 dp) read by browser pass, one page each; other platform claims rest on earlier notes.
- Not read in full: most APG pages, NN/g heuristic-evaluation figures, the Nielsen and Landauer paper, critiques of the 5-user model, Mathur et al. prevalence. Automated-tool coverage and first-click claims are [F], unverified.
- No controlled evidence that the without-reading test predicts task success; validate with real users.
- Gamification effect sizes and dark-pattern law: secondary notes; compliance is for counsel.
- Tabs, tree, grid keys and RTL or CJK layout not in depth. Discovery research: `product-management`.

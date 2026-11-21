# Playbooks: routines, templates, agendas

Practical routines. Deeper rules live in the other references: heuristic list and finding format in `review-method.md`, forms and states in `forms-states-feedback.md`, WCAG and ARIA in `accessibility-wcag22.md`. Numbers and trees: `diagnosis-playbook.md`. Evidence tags: **[C]** consensus, **[M]** single study, **[F]** practitioner rule of thumb.

## Contents
1. Usability test: plan and script
2. Heuristic evaluation
3. Form design checklist
4. Accessibility audit routine
5. Information architecture: card sorting and tree testing
6. UX writing for flows
7. Design critique agenda
8. Handoff with acceptance criteria

## 1. Usability test: plan and script
**Plan (one page).** Goal and the decision it informs; the user groups; 5-8 users per round per group [F] (NN/g: 5 find most problems of a group, then fix and retest; Nielsen and Landauer model and limits in `diagnosis-playbook.md`); 3-6 tasks; the prototype or build and its state (test data reset); device and place; metrics (success, time, errors, one satisfaction question: SEQ after each task, SUS at the end); recording consent; who observes and who takes notes; schedule with a pilot.

**Recruiting.** Recruit by behavior (does the task today), not by age. Exclude employees and friends. Offer an incentive. Screen out professional testers. Plan one extra participant for no-shows.

**Tasks.** Write scenarios, not instructions (NN/g): a realistic reason, a goal, no interface words. Bad: "Click Settings and change your plan." Good: "You are moving to a bigger team next month and want to pay less per person. Find out if that is possible." Define success before testing: the end state, the allowed paths, partial credit rules, and a time limit after which you stop and mark failure. Order tasks from easy to hard, but randomize if they interact.

**Script (about 45 min).**
1. Welcome, 3 min: "We test the product, not you. Nothing you do is wrong. Say what you think as you go. I may not answer questions, because I want to see what you would do alone. You can stop any time." Consent and recording.
2. Warm-up, 5 min: background questions on current habits (no opinions on the design).
3. Tasks, 25-30 min: hand over one task at a time, read aloud and give on paper. Think-aloud (NN/g): remind with neutral prompts ("what are you thinking now?"); never help, never defend, never lead ("did you see the button?"). If stuck for the time limit, ask "what would you do next?", then end the task and record failure.
4. After each task: SEQ (1-7, "how easy was this?").
5. Wrap-up, 5 min: SUS, "what was the hardest part?", "what would you change?", thanks.

**Notes.** One log per participant: task, outcome (success, partial, fail, assisted), time, path, errors, quotes, observed vs inferred. Observer notes in separate columns for what happened and what the observer thinks.

**Severity and report.** Rate each problem 0-4 (NN/g: frequency, impact, persistence; 0 not a problem, 4 catastrophe) using the same scale as heuristic evaluations. Report: top 5 problems with a clip or quote, rate of users affected (counts, "4 of 6", not percent), fixes, what was not tested. Small n: never write "67% of users" [C].

**Moderated vs unmoderated.** Moderated finds the why; unmoderated gives volume and time data with less depth. Remote moderated works for most flows; in-person for hardware, accessibility with assistive technology setups, or when the context matters.

## 2. Heuristic evaluation
Use when there are no users yet, as a pre-test filter, or between rounds. Procedure: 3-5 evaluators work alone [C] (one evaluator finds only a fraction of the problems; the NN/g article on problems found by heuristic evaluation covers aggregation, exact figures not re-read here), at least two passes: first the flow, then screen by screen against the 10 heuristics (Nielsen): visibility of system status; match with the real world; user control and freedom; consistency and standards; error prevention; recognition rather than recall; flexibility and efficiency; aesthetic and minimalist design; help recognize, diagnose and recover from errors; help and documentation. Each finding gets the heuristic, a screenshot, a severity 0-4 and a fix, in the format in SKILL.md. Merge in a meeting: dedupe, agree severity, then rank by severity times frequency.
Limits: it finds usability problems, not whether people need the product; evaluators disagree on severity; false alarms exist, so label them "predicted" until tested. A heuristic evaluation plus a 5-user test beats either alone [F]. Add the without-reading test (`understand-without-reading.md`) and the WCAG pass (section 4).

## 3. Form design checklist
Evidence: Baymard (field count, inline validation, mobile and autofill research) and NN/g (form errors, placeholders).
- **Need.** Every field maps to a use; derive what you can (postcode to city); remove or defer the rest. Baymard average 11.3 checkout fields, ideal about 8 [M]. WCAG 3.3.7: do not ask twice for the same data in one process.
- **Labels.** Visible label above the field, not placeholder-only (NN/g: placeholders are harmful); mark optional rather than required if most are required; hint text stays visible. WCAG 1.3.1, 3.3.2.
- **One column**, logical order, group related fields, related fields side by side only if they are short and obvious (zip + city). Never split a phone, card or date into chunks without need.
- **Types and keyboards.** Right `type` (email, tel, url), `inputmode` (numeric, decimal), `autocomplete` token on every personal field (given-name, family-name, email, tel, street-address, postal-code, cc-number, one-time-code, new-password, current-password) [C: WCAG 1.3.5]. Allow paste. Accept format variants (spaces in card numbers, dashes in phones) and normalize server-side.
- **Inline validation** (Baymard): validate on blur after the person typed, not on the first keystroke; clear the error the moment it is fixed; show positive confirmation only where it helps (username free); never block the field with a pattern the person cannot discover.
- **Errors** (NN/g 10 guidelines, WCAG 3.3.1 and 3.3.3): next to the field, text plus icon plus color, say what is wrong and how to fix it in plain words, keep the input, summary at the top for long forms with links to fields, move focus to the summary or first error, announce with a status region (4.1.3). Hand the exact wording to the copywriting skill when it is marketing-grade.
- **Buttons.** One primary, labeled with the outcome ("Pay 59 EUR"), not "Submit"; secondary is visually weaker; the button stays active or states the first missing item beside it.
- **Autofill and wallets.** Offer them first on mobile where supported. Passwords: allow managers, show/hide, no paste blocking, no cognitive test as the only way (3.3.8).
- **Progress.** Multi-step: name the steps, allow back with data kept, show a summary before commit; collapse completed steps into summaries (Baymard).
- **Recovery.** Save drafts; session timeout warns and keeps data; undo or a visible edit route after submit; a confirmation page or email says what happened and what is next.
- **Test.** Fill the form with a real long name, an apostrophe, an accented letter, an unusual address, a pasted value, by keyboard only, on a phone with the keyboard open.

## 4. Accessibility audit routine
Target WCAG 2.2 AA [C]. Automated tools (axe, Lighthouse) are commonly reported to find only part of the issues [F, not verified here], so run the manual pass; sample pages by template, not all pages (WCAG-EM: sample representative pages and states).
1. **Scope.** List templates and critical flows (sign-in, search, checkout, key task). For each, capture default, error, empty, loading, dialog and menu states.
2. **Automated scan** first; fix the obvious; note it as the floor only.
3. **Keyboard pass** (no mouse): Tab and Shift+Tab reach every control in a logical order (2.1.1, 2.4.3); a visible focus indicator that is not hidden by sticky bars (2.4.7, 2.4.11); no traps (2.1.2); Enter and Space activate; Esc closes dialogs and menus and returns focus to the trigger; skip link works (2.4.1); targets at least 24x24 CSS px (2.5.8); every drag has a single-pointer alternative (2.5.7).
4. **Screen reader pass.** One desktop pair (e.g. NVDA with Firefox or Chrome, VoiceOver with Safari) and one phone (TalkBack or VoiceOver). Check: page title and language; landmark and heading structure; every control has a name, role, state (4.1.2); names contain the visible text (2.5.3); form errors and status messages announced without moving focus (3.3.1, 4.1.3); dynamic updates announced politely; dialogs trap focus and label themselves; tables have headers.
5. **Visual pass.** Zoom 200% and 320 px width without loss or two-way scroll (1.4.4, 1.4.10); text spacing override; contrast 4.5:1 text, 3:1 large text and components (1.4.3, 1.4.11); color is never the only signal (1.4.1); reduced motion honored; content on hover or focus dismissible and persistent (1.4.13).
6. **ARIA review** (APG): first, can a native element do it? If a custom widget exists, compare with the APG pattern for roles, states, and keys (dialog, combobox, tabs, menu, listbox). A role is a promise of keyboard behavior; remove roles you do not implement; no `aria-hidden` on focusable elements; `aria-live` sparingly.
7. **Content and cognitive.** Plain language, consistent help location (3.2.6), no redundant entry (3.3.7), authentication without memory tests (3.3.8), timeouts explained.
8. **Report.** Per issue: criterion, where, steps, expected, severity (blocks a task, hinders, annoys), fix. Include what was not tested (assistive technology versions, devices). A conformance claim needs a full evaluation; say "audit of sample X", never "compliant".

## 5. Information architecture: card sorting and tree testing
Use when findability fails (diagnosis 3.3). Rosenfeld and Morville: organization, labeling, navigation and search systems work together; Krug: judge by doubts per click.
- **Open card sort** (generative): 15+ participants per user group (NN/g) write groups and labels for 30-60 cards from real content; analyze with a similarity matrix and dendrogram; look at the labels people invent. Use it before you design the structure.
- **Closed card sort**: test a fixed set of categories; **hybrid**: allow new categories.
- **Tree test** (evaluative, text-only structure): give 8-10 task questions, record success, directness (no backtracking) and time; participants find where they would look first. Quantitative needs enough users for useful intervals (NN/g); qualitative tree tests find labeling problems with few users but give no rates. Run it before and after a restructure.
- **First-click test** on a screenshot: a widely cited finding is that a right first click predicts task success, but I did not verify the numbers [F].
- **Labels**: use the user's words from search logs and tickets, one name per thing across the product, no jargon, parent label covers children (information scent). Remove the "Other" and "More" buckets from main navigation.
- **Rules of thumb** with limits: depth vs breadth has no universal answer; "3 clicks" and "7 plus or minus 2" are [X]. Keep top-level items few enough to scan and test.
- **Deliverables**: sitemap, task-to-path table, labeling glossary, search synonym list.

## 6. UX writing for flows
Words in the interface are interface. Principles: say what the thing does; start with the verb; one name per concept; sentences the person would say; tell what happens next. For each flow list every string by state.
| Element | Rule |
|---|---|
| Button | Verb plus object ("Save changes", "Pay 59 EUR"); never "OK" or "Submit" alone; destructive says the effect ("Delete 12 files") |
| Error | What happened, why if known, what to do; no blame, no codes alone; keep input |
| Empty state | What goes here, why it is empty, one action |
| Confirmation | Names the item and effect; buttons as outcomes |
| Permission or consent | Why we ask, what we do not do, what happens if no |
| Loading or status | What is happening, not "Please wait" alone |
| Success | What changed and the next step; passive toast only for low stakes |
| Microcopy under fields | Format hint before the error, not after |
Test strings with the longest language and by reading aloud; run the without-reading test to check the layout works without the words. Plan localization (expansion of 30-40% is common [F], plural rules, no concatenated sentences). **Link copy for marketing:** descriptive link text ("See pricing for teams", not "Click here"); where the words persuade or sell, headlines, value claims and CTAs, hand off to the `copywriting` skill, which also holds the consumer-law limits; this skill keeps flow text clear, honest and accessible (2.4.4, 2.5.3).

## 7. Design critique agenda
(NN/g critiques: a facilitator, a scope and agenda sent in advance, feedback tied to goals.) 45 minutes.
1. 5 min: owner states the goal, user, task, constraints, and the kind of feedback wanted (flow, hierarchy, copy). No solution pitches.
2. 5 min: silent walkthrough of the artifact; everybody writes notes.
3. 20 min: feedback round, structured as "I notice / I wonder / what if", about the goal not taste; each point cites a heuristic, a user observation or data; no solutions in the first pass.
4. 10 min: group, rank by severity (0-4) and decide: change, test, ignore with reason.
5. 5 min: the owner restates decisions, owners, dates.
Rules: facilitator keeps time and tension down; the owner decides; record in the finding format; critique is not approval, see the approval criteria in `review-method.md`.

## 8. Handoff with acceptance criteria
A design is ready for build when this exists:
- The goal, user, success criterion and the metric to check later.
- Flow diagram with every state per screen: default, empty, loading, partial, error, success, offline, denied, long text, first run.
- Specs: spacing and type from the design tokens (see `ui-design`), component names, responsive rules at 390, 820 and 1440.
- Interaction notes: keyboard order, focus after open and close, animation and reduced motion, what is announced to a screen reader.
- Copy table by state in the product language with a faithful translation when needed.
- Data and rules the design depends on (validation, limits, permissions); anything that is a business rule is flagged for an owner.
- **Acceptance criteria**, in testable form: "Given a signed-out user on 390 px with a 200% text size, when they submit an invalid email, then an error with the text X appears next to the field, the input is kept, focus moves to the field, and a screen reader announces the error." Include: a state per criterion, the WCAG criteria that apply, the event names for tracking the funnel (handed to `growth-analytics`).
- Open questions and risks, and what was not user-tested.
- A review after build: screenshots at the three widths, keyboard pass, and a check against the criteria, not against the mock alone.

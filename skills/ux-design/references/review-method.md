# Review method, per-screen checklist, platforms, real-use testing, habit ethics

## Contents
1. Heuristic evaluation procedure
2. Finding format and severity
3. Per-screen checklist
4. Mobile vs desktop
5. Testing with real use
6. Approving a screen
7. Habit and gamification ethics
8. Sources

## 1. Heuristic evaluation procedure
1. Define the persona and the task (what is a successful session). Without a task you review decoration.
2. Walk the flow once, start to finish, as the person, without reading code.
3. Second pass per screen: the 10 heuristics in order, then the checklist below, then the accessibility criteria that apply.
4. Capture evidence in each state (empty, loading, partial, error, success) and at phone and desktop widths; keyboard-only; 200 percent zoom; 320 px reflow.
5. Run the without-reading test (`understand-without-reading.md`).
6. Write findings, rank, cut to the ones that matter, give a verdict per platform.
7. Say what you did not observe. Do not claim observations from code reading alone, and mark findings that need confirmation on a real screen.
Several independent evaluators find more problems than one; when you have only one, say so. After the walk, scan `real-screen-lessons.md` for recurring anti-patterns, and test situational limits (one hand, bright light, keyboard only, interrupted session) from the inclusive design toolkit.

## 2. Finding format and severity
```
UX-<n> | severity <0-4> | <screen / state / viewport>
Problem: what the person sees or fails to do
Cited: heuristic or law, plus WCAG criterion
Evidence: screenshot path or reproduction steps
Fix: one concrete change
Accept when: observable criterion
```
Severity 0-4 per NN/g (0 not a problem, 1 cosmetic, 2 minor, 3 major, 4 catastrophe) using frequency, impact, persistence. 3 and 4 block approval. A common alternative P1/P2/P3 mapping: P1 = blocks the task, induces a wrong decision or loses data (3-4); P2 = hinders (2); P3 = polish (1).

## 3. Per-screen checklist
Orientation: where am I, one primary action, breadcrumbs or title matching the nav label. Hierarchy: weight over size over color; secondary actions quiet. Content: person's words, no jargon; essential info for acting is visible, not hidden only behind an info icon or tooltip; also flag too much text where an icon with a label would do. States: empty, loading, error, offline, success, disabled, read-only, permission denied. Actions: dangerous ones not primary, Undo or confirm per rules, bulk preview. Forms: see forms reference. Feedback: response under 400 ms visible, long work has stages and cancel. Accessibility: contrast, focus visible and not obscured, 24 px target floor, keyboard path, status announcements, reflow, language attribute, reduced motion. Consistency: same word, icon and place for the same thing. Copy: states what will happen, button as verb, no promise the system does not keep.

## 4. Mobile vs desktop
Judge each platform by how it is used, and give a separate verdict.
- Phone: short sessions, one hand, interrupted; reading, deciding, quick capture. Primary action low and wide; content central; nothing important in corners; cards instead of wide tables; labels visible (no hover); on-screen keyboard and sticky bars can hide focus (2.4.11); thumb-friendly 44 px targets.
- Desktop: long sessions, keyboard and pointer; editing, comparing, bulk work. Dense tables with sticky headers, side panels, shortcuts with discoverable hints, hover help that is also reachable by focus.
- Tablet is its own platform: touch like a phone, screen like a laptop, often with a keyboard; no hover.
- Do not shrink the desktop layout to the phone: choose the subset of the task that phones do well.
- Do not assume desktop needs smaller or larger type than phone; use platform conventions (see `ui-design`).

## 5. Testing with real use
- Test the real path in the real environment, with timings and intermediate states, not only the happy final state. Quantity of clicks is not proof; say what remained unproven.
- Use a persona's device and language, include slow network and an interrupted session, and a keyboard-only run.
- Prefer a few focused sessions with the target task over broad scripted coverage. Aesthetic appeal can mask failure: record task success, not praise.
- Record: steps, time to complete, errors, abandonment point, quotes. Convert each problem to a finding with severity.
- Test only what changed plus flows never tested; do not re-test approved flows without a change.

## 6. Approving a screen
Approve only when: no open 3 or 4; the without-reading test passes; all states exist; the platform verdicts are at least acceptable; accessibility basics pass (keyboard, contrast, targets, focus, reflow); the copy states consequences of actions. "Tell me when it is final" is not approval. A fine adjustment of an approved screen can be done and shown; a new screen or state needs sign-off first.

## 7. Habit and gamification ethics
- Fogg: behavior = motivation x ability x prompt at the same moment; when people do not act, make it easier first; motivation is the least reliable lever. Start habits tiny, anchor them to an existing routine, celebrate right after.
- Eyal's hook (trigger, action, variable reward, investment) is defensible only in the "facilitator" quadrant: you would use it yourself and it improves users' lives.
- Evidence: a meta-analysis of gamification in education (38 publications, 40 experiments) found small positive effects on learning (g = 0.49), motivation (g = 0.36) and behavior (g = 0.25); only learning held in the most rigorous studies. Expected external rewards can reduce intrinsic motivation (Deci, Koestner and Ryan 1999). Public rankings demotivate people at the bottom; keep them optional or among close peers. (study notes; not re-verified)
- A streak shows progress; it becomes abuse when it makes people feel guilty, can only be saved by paying, nags at night, uses false countdowns or false scarcity, shames the refuse button (confirmshaming) or makes cancel hard. Build in slack (pause, freeze, return without blame): it improves retention without coercion.
- Vendor A/B results (for example streak freezes raising active users by 0.38 percent) are internal and unreviewed; use as inspiration only. Correlations (7-day streak and completion) are not causes.
- Notifications: ask permission after showing value, with a preview of content, user-chosen time, and a one-step way to turn off.
- In the EU, fake urgency and fake scarcity are unfair commercial practices; check local law.

## Sources
- https://www.nngroup.com/articles/how-to-rate-the-severity-of-usability-problems/ (read 2026-11-15)
- https://www.nngroup.com/articles/ten-usability-heuristics/ (read 2026-11-15)
- NN/g heuristic evaluation, mobile tables, ui-accelerators articles (study notes 2026-11-13, not re-fetched)
- Fogg Behavior Model https://behaviormodel.org/ ; Eyal, Hooked (2014); Deci, Koestner, Ryan 1999, Psychological Bulletin 125; Sailer and Homner 2020 meta-analysis (study notes; not re-verified)
- EU unfair commercial practices: Directive 2005/29/EC and Commission 2023 sweep on dark patterns (study notes; not re-verified)

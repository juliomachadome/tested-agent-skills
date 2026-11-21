# Lessons from real visual reviews: generic anti-patterns

Distilled from many rounds of screen-by-screen review of a large product design (several hundred frames, two form factors, three themes). Each lesson is stated as a rule with a generic example, the principle it breaks, and a check that finds it mechanically. Laws and heuristics are cited by name; sources are in BIBLIOGRAPHY.md.

## Contents
1. Dangerous or ending action styled as primary
2. One primary per list row
3. Waiting states that feel endless
4. Floating action bars with no common geometry
5. Hidden essentials (no exit, no signifier)
6. Low-contrast filled fields
7. Data that contradicts itself across screens
8. Consistency drift across components
9. Counters and states that do not come from the data
10. Copy and notes leaking into the screen
11. Layout glitches that eyes miss
12. Process lessons for reviewers
13. Mechanical sweep list

## 1. Dangerous or ending action styled as primary
Rule: the primary style belongs to the action that advances the task. Stop, pause, cancel, discard, end, archive, deactivate, delete and decline use a secondary style or a link, open a confirmation that states the consequence in plain words, and only inside that confirmation does the confirming button take the danger color.
Example: a recording screen whose largest filled button says "Stop and transcribe" invites an accidental tap; make it secondary, and have the dialog say what will happen to the captured audio.
Why: Von Restorff (the standout item is remembered and tapped), Nielsen error prevention, Norman's signifiers (the control must say what will happen). Keep destructive confirmations the same color in every dialog (Nielsen consistency); a dialog that confirms in black next to another that confirms in red teaches nothing.
Check: list every filled button; for each, ask whether it advances or ends the task.

## 2. One primary per list row
Rule: a table or list does not repeat a filled primary button on every row; nothing then stands out. Use the filled style only for the selected row or the single page-level action; other rows use secondary buttons or a row menu.
Example: nine "Release" buttons filled in black in one list.
Check: count filled buttons per screen; more than two is a smell.

## 3. Waiting states that feel endless
Rule: every wait screen answers four questions: what is happening, how far along (percent or "about N min"), what can I do meanwhile, where will I see the result. Say "you can leave" only if the work visibly continues elsewhere (a global indicator in the shell, a list row with progress); otherwise the promise is empty.
Example: a long-running task shows a chip "Processing" with no progress, and leaving the page gives no sign it is still running.
Why: Nielsen visibility of system status; Goal-Gradient effect; Doherty threshold (about 400 ms) for any acknowledgment. Progress bars should be determinate when possible, never stall, and keep the same style when switching from indeterminate to determinate (Apple HIG progress indicators, prior reading).
Check: each loading or processing frame has progress or estimate text and a "where to find it later" cue.

## 4. Floating action bars with no common geometry
Rule: a fixed action bar is a component with one geometry: same width and x as the content column, same distance from the bottom, content padded by the bar height plus clear space so the bar never touches text. When every screen draws its own bar, widths drift (640, 700, 720, 800) and alignment breaks.
Check: measure the bar's x, width and distance from the bottom on every screen; they should be identical per breakpoint. Verify its top edge does not overlap content.
Why: Gestalt alignment and proximity; Fitts (stable target position).

## 5. Hidden essentials
Rule: every essential action has a visible cue and a designed state. Sign out and account switching must be reachable; if the only cue is a 16 px chevron on a chip, add a larger affordance and a tooltip label; when the sidebar collapses, the avatar alone needs a label. Keyboard shortcuts get a persistent hint, not only a help overlay.
Why: Nielsen user control and recognition over recall; Norman signifiers.
Check: from each shell state (expanded, collapsed, mobile) find sign out, help, and the main navigation without hovering.

## 6. Low-contrast filled fields
Rule: a field with a very light fill on a white surface can sit near 1.1:1 against its surroundings. If the product chooses fields without a dark outline, then either darken the fill one step and always show a visible label, or draw a 1 px baseline at 3:1 or more; never let the field be identical to the background. WCAG 1.4.11 requires the boundary needed to identify a control to reach 3:1 against adjacent colors, with an exception only for inactive components.
Check: compute field fill vs surface and the boundary vs surface; compute for text too (a muted gray label on an active row can measure 4.3:1 and fail).

## 7. Data that contradicts itself across screens
Rule: sample data, counters and status labels come from one canonical dataset. Two screens that show different numbers of modules, different dates for the same event, different names for the same role, or different statuses for the same item look like bugs to a reviewer and to a customer.
Example: "1-8 of 8" on desktop and "1-6 of 6" on mobile for the same list; a status chip amber on one breakpoint and green on another.
Check: grep the design and code for every fact (name, date, count, status) and diff across frames; run it before delivery and attach the result.
Why: Nielsen consistency and standards.

## 8. Consistency drift across components
Rule: the same function keeps the same icon, label and position everywhere (Jakob's law, WCAG 3.2.4). A collapsed menu using a different icon than the expanded one for the same destination, a menu item whose label was copied from the wrong row, or the same chip colored differently by breakpoint all fail this.
Check: tabulate icon and label per destination across all shell variants.

## 9. Counters and states that do not come from the data
Rule: "n new", "n of m", filter chips and totals are computed from the visible rows. A filter that is shown active must filter; a summary row that sums 6 of 8 items must show the remaining states or say so; a message saying "2 points left" while one remains is a bug.
Check: recompute every counter from the visible list at each state.

## 10. Copy and notes leaking into the screen
Rule: no design notes, "to be decided", or placeholder instructions as visible text; no title that promises more than the screen delivers; no example data that tells an accidental story (a task "in progress" with a four-day-old date). Section titles are real titles, not the helper text.
Check: read every visible string once as a customer.

## 11. Layout glitches that eyes miss
Overlapping step indicator and helper text at narrow width; text clipped without a way to read it in full (use wrapping or a tooltip rather than a dead end "..."); a button left-aligned while everything else is centered; a bar at 0 or -4 px from the bottom when the system uses 68; headers that shift 23 px between tabs because a badge moved. A geometric sweep (bounding boxes and overlaps) finds many; the eye finds the rest.

## 12. Process lessons for reviewers
- Re-verify previous fixes; "fixed" claims drift. Re-read only touched frames once after a fix batch.
- Separate blockers (wrong or unsafe), fix-before-code, and polish; cap the polish list.
- A frame replaced by text is invisible to a geometric scan; look at the pictures too.
- When a defect repeats in many frames, fix the component, not the frames, and add a rule so the next screen starts right (a defect found twice becomes a lint or checklist item).
- Report "verified vs not verified" explicitly.

## 13. Mechanical sweep list
- filled buttons per screen; destructive confirm color consistent
- bar geometry per breakpoint (x, width, bottom offset)
- contrast pairs, including text on active and hover states
- field fill and boundary vs surface
- fact diff across frames; counters vs rows
- icon and label per destination across shell variants
- overlaps and clipped text at 390 and 320
- wait screens with the four answers

## Sources
- Nielsen Norman Group, 10 Usability Heuristics, https://www.nngroup.com/articles/ten-usability-heuristics/ (last updated 2024-01-30), read 2026-11-15
- Laws of UX, https://lawsofux.com/ (Von Restorff, Goal-Gradient, Doherty Threshold, Jakob, Proximity), read 2026-11-15
- W3C WCAG 2.2 Understanding Non-text Contrast, https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html, read 2026-11-15
- Norman, The Design of Everyday Things (revised 2013), book, signifiers (not fetched)
- Apple HIG Progress indicators and Alerts, https://developer.apple.com/design/human-interface-guidelines/ (prior reading, not re-fetched)
- Review rounds: internal, anonymized and generalized

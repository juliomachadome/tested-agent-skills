# Lessons from real screen reviews: generic anti-patterns

## Contents
1. How to use this file
2. Anti-patterns (A1-A28)
3. What good looked like (keep list)
4. Review process lessons
5. Sources

## 1. How to use this file
These patterns come up again and again when screens are reviewed with screenshots in several states and two viewports. Each entry has the symptom, why it hurts (heuristic or law), the fix and a typical severity. Use them as a second pass after the heuristic walk: scan the screen for these before writing findings. Severity follows the NN/g 0-4 scale; examples are generic.

## 2. Anti-patterns

**Decisions and actions**
- **A1. Two buttons for one decision.** A disabled "Confirm" sits next to an active "Confirm and continue" that skips the step. Hurts: error prevention, consistency, Hick. Fix: one primary per decision; the disabled state says the first missing thing beside the button, with a link to it. Sev 3-4 when the active one bypasses a required step.
- **A2. Primary action as a mute icon.** The main action is a bare check that looks disabled until a field is filled. Hurts: signifiers (Norman), recognition over recall. Fix: text label "Confirm name", full-size primary; secondary actions as text links.
- **A3. Primary styling when not ready.** A dark primary button is lit everywhere although preconditions are unmet, so it competes with the real final action. Fix: secondary style until ready, then primary, and only then; if disabled, the reason is visible text.
- **A4. Offering what cannot work.** "Pause" during a single-pass step, "Mark as filed" with eight blank fields, "Mark conclusion" with nothing chosen (error instead of prevention). Fix: do not offer, or disable with the stated reason.
- **A5. A convenience that skips review ("accept all").** Bulk confirm invites automation bias. Fix: show what will be accepted (count, doubts included), make the declaration name the person, keep the button secondary; the primary is the real final step.
- **A6. Partial undo.** Undo reverses part of a compound action and leaves residue (a split stays after the reassign is undone). Sev 3: trust in the whole history collapses. Fix: compound actions are one history entry; after undo the data equals the state before.
- **A7. Mutating actions without a guard on leaving.** Navigation mid-recording or mid-edit ends the work silently; a mode switch discards a live panel. Fix: guard exits (save and leave), keep long operations visible, disable conflicting mode switches.

**Counts, repetition, state**
- **A8. Counters that contradict.** "14 to check", "4 of 18 checked", "0 of 2 parts confirmed" and a filter "0" on the same screen. Fix: one primary progress, derived from one source; remove counters with no destination; filters that show zero disappear.
- **A9. Same fact in three to five places.** Status in the pill, the stepper, a banner and a result box; date and chair repeated in the header, a card and a form. Fix: say it once, where the decision happens (Occam, Nielsen 8).
- **A10. Stale or false state.** A job shown "in progress" for a day; "someone is viewing" after they left; "generated at 11:47" two days later with no date; "Waiting" with nothing running. Fix: show age and detect stuck work ("stopped 1 day ago", with an action); show the date when it is not today; end banners when the state ends.
- **A11. Same glyph, two meanings.** One check means "accept suggestion" and "mark reviewed", 48 px apart. Fix: different shape, label or place; reserve a verb for each act.
- **A12. One verb for review and finalize.** "Confirm" used for reading the text and for locking it. Fix: a glossary: "Review" for checking, "Confirm" only for the act that locks; align every string, tooltip and modal.
- **A13. Same command, different names by surface.** Toolbar says "Merge with row above", menu says "Merge with previous", sheet says "Join". Fix: one name per command in one string table.
- **A14. Provisional looks final.** Live draft text carries the same weight and the same per-item warnings as final text. Fix: a single provisional marker for the whole block, final styling only when final.

**Layout and overlays**
- **A15. Chrome before content.** Seven layers (back, action, title, step, hint, player, toolbar, filters) before the first row; on a laptop viewport no item is visible. Fix: keep the persistent strip to what is used constantly; merge filters; show a bar of icons only when something is selected.
- **A16. Fixed bars stacking at one position.** Undo bar, selection bar and action bar all use the same offset and layer; they cover each other and the focus (WCAG 2.4.11). Fix: one stack with a defined order, or one bar at a time; `scroll-padding` equal to the stack.
- **A17. Floating layers over the thing they describe.** A tooltip on the bottom of an icon covers the line being read; a second bar hides behind a menu; a toast covers the pay button. Fix: no layer covers the text it comments on; open to the side with flip, delay on first show, Esc closes, never above the primary control.
- **A18. Hover and cursor that lie.** Pointer cursor with no destination; locked text shows a "not allowed" cursor over text people want to copy. Fix: cursor and hover reflect real affordance; locked text keeps the text cursor and no hover fill.
- **A19. Menu overload.** A context menu with 13 items of equal weight, five dimmed; in a locked state the whole menu is dimmed. Fix: three groups by proximity; impossible items disappear, contextually unlockable items stay with a reason once, not three times; in a locked state show only the open path (reopen, copy).
- **A20. Icon-only toolbars.** Nine non-universal icons, mostly disabled; counters explained only in a tooltip, invisible on touch. Fix: label on touch, tooltip with shortcut on desktop, text for anything needed to act (the test: can someone act without hovering?).

**States and errors**
- **A21. Dead ends.** A waiting state with no exit and an "estimate" for nothing that is running; a failure card that also shows inert sibling sections; a "not found" error that talks about connection. Fix: every state has an exit; the error names the real cause and what was kept.
- **A22. Success without closure.** After a final approval the page reloads silently; the discreet link on the most important moment. Fix: status line (announced politely) with what happened, who and when, and the one next action as a primary (Peak-End).
- **A23. Essentials below bulk.** The approved document sits under the full transcript; metadata fields come before the file upload that is the task. Fix: order by importance (serial position); collapse the long item list behind "View".
- **A24. Raw internals.** Rule codes in English, model and prompt versions, a technical term for a step, a Markdown editor beside a block editor, date inputs in two formats. Fix: translate to the person's words; one component per data type; internals go to an audit view.

**Platforms**
- **A25. Desktop shrunk to the phone.** A document inside a card inside a page leaves 30 characters per line; sheets at full height 80 percent empty; the action bar clipped at the edge with no scroll cue; chips overlapping a link; a sticky pill partly behind the tab bar; primary action at the top far from the thumb. Fix: choose the phone subset (read and decide), fixed bottom primary, sheet height to content, wrap or scroll with a cue.

**Trust and promises**
- **A26. Promise beyond the product.** Copy promises a notification that does not exist, a demo timeframe nobody confirmed, a "live" feature still in development, a CTA verb that implies purchase when the action is a request. Fix: copy states only what the system does now; verbs match the real outcome.
- **A27. Dirty data in a demo.** Garbled seed text and half-filled records read as bugs and cost credibility (Aesthetic-Usability masks nothing here). Fix: clean the data before showing a client.
- **A28. A default with consequences.** A pre-selected option that changes a legal or procedural effect. Fix: nothing pre-selected where a person's responsibility is involved; if a safe default is unavoidable, state it in the interface and in the review.

## 3. What good looked like (keep list)
Reviews are more useful when they also record what must not regress: errors inline with the next step; irreversible acts with a named effect; "what was kept" in every failure; state by shape and label together (a check, a half circle, a dashed outline, a triangle, a lock); abstention as a first-class state with its own icon and next action; a status line that says one thing, the first missing item; panels that collapse when done; one provisional marker; a preview with count and items before a batch; counts that reconcile with the list.

## 4. Review process lessons
- State what was observed and what was not: which screens, states and widths, and which findings come only from code or old screenshots. Mark those findings as needing confirmation on the real screen.
- A designer reviewing their own work gives a conditional verdict; get a blind pass from someone else.
- Prefer a short ranked list; separate "what to remove" (a table of items with the screen and the reason) from "what to add".
- Every finding has a fix and an acceptance criterion in Given/When/Then form, checkable at both widths.
- Rate each platform separately: desktop and phone can differ by a full grade.
- Run the without-reading test on every state; it exposes hierarchy and state-by-color problems quickly.
- Mark questions that need a product decision separately, one per line, so they do not block fixes that are clear.

## 5. Sources
These are lessons distilled from internal screen reviews (generalized, no product details) and checked against:
- https://www.nngroup.com/articles/user-mistakes/ (Laubheimer, 2015; read 2026-11-15)
- https://www.nngroup.com/articles/confirmation-dialog/ (published 2018, reviewed 2026-08-07; read 2026-11-15)
- https://www.nngroup.com/articles/empty-state-interface-design/ (Kaplan, 2021; read 2026-11-15)
- https://www.nngroup.com/articles/data-tables/ (Laubheimer, 2022; read 2026-11-15)
- https://www.nngroup.com/articles/progress-indicators/ (Sherwin, 2014; read 2026-11-15)
- https://www.nngroup.com/articles/ai-chatbots-discourage-error-checking/ (Samsonov, 2025; read 2026-11-15)
- Norman, The Design of Everyday Things (revised and expanded 2013): signifiers, feedback, conceptual models (see bibliography).

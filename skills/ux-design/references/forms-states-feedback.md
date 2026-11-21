# Forms, checkout, tables and bulk actions, states, feedback, errors

## Contents
1. Response times and progress
2. Errors, confirm vs undo
3. Forms
4. Checkout
5. Onboarding steps
6. Tables, lists, bulk actions
7. Empty, loading, error states
8. Optimistic UI
9. Sources

## 1. Response times and progress
NN/g limits (read 2026-11-15): **0.1 s** feels instantaneous, nothing but the result is needed. **1 s** keeps the flow of thought; between 0.1 and 1 s the delay is noticed but needs no special feedback; beyond 1 s show that the system is working. **10 s** is the limit of focused attention; beyond it show percent-done and a clearly marked way to interrupt, and expect people to switch tasks and need re-orientation.

Rules that follow (progress-indicator guidance from NN/g, read in the study notes 2026-11-13, not re-fetched):
- 2-10 s: a spinner with a text label ("Loading comments"). Over 10 s: percent, or if no total is known, name the current item or step ("Part 2 of 4").
- Start the bar slower and speed up near the end; give conservative estimates; step counts can replace percentages. A bar that runs fast and stalls at the end destroys trust (NN/g, 2014). Never invent an estimate; an honest count beats a precise lie.
- Never say "do not click again": show that the first click was accepted and disable the control with the reason stated.
- In complex applications "please wait" is not enough beyond 10 s; list steps done and remaining, say it is safe to leave and come back, and offer cancel.
- On return to a running job, show the current step and what is already saved.
- Doherty's 400 ms is a guideline for visible reaction to input, not a replacement for the limits above.

## 2. Errors, confirm vs undo
- **Slips vs mistakes** (NN/g, user mistakes): a slip (autopilot) is fixed with validation and constraints; a mistake (wrong mental model) with conventions, clear signifiers and a **preview of the result** before committing, especially for slow or hard-to-reverse actions.
- **Prefer Undo to a dialog when the action is reversible.** It lowers anxiety and catches errors confirmation does not. A snackbar that disappears in a few seconds is easy to miss, so also keep the undo in history and on the platform shortcut. Undo should say what it undoes ("Undo merge of 3 rows"), bring the result into view (scroll to it), support several levels, and treat a batch as one entry. If undo cannot run, say it did not.
- **Confirm only serious, ideally irreversible, actions.** Restate the request and name the item and the effect; buttons are results ("Approve report", "Keep"), never Yes/No; no default on the destructive choice; for rare, dangerous acts require a deliberate step. Over-confirming trains people to click through; weigh severity against frequency and let people turn off routine ones.
- **Modal alerts only for the critical.** Title says what happened and why, never just "Error"; Cancel is not the default for destructive actions; the primary button is never the destructive one; destructive red only for what the person did not choose deliberately.
- WCAG 3.3.4: submissions with legal or financial effect or that change or delete data must be reversible, checked or confirmed.
- **Error message** (heuristic 9): what happened, why, what to do now; plain language, no code, no blame, mention what was preserved. Three or more repeated errors on one field in a test mean the design is failing, not the person.
- **Medium choice** (NN/g): indicators are passive and contextual, validations demand action, notifications report system events. A toast suits passive success and is wrong for errors because it vanishes.

## 3. Forms
Sources: NN/g and Baymard form guidance (read in study notes; Baymard checkout stats read 2026-11-12, see section 4).
- Visible label above the field. Placeholder is not a label: it disappears on typing, burdens memory, is hard to review, has low contrast and looks pre-filled. Floating labels are better than placeholder-only and worse than fixed labels.
- One column. Side by side only for one unit (expiry plus code).
- Ask for the minimum; each field needs a reason. Optional fields leave or collapse behind a link. When most fields are required, mark optional ones with the word "optional".
- Correct `type`, `inputmode` and `autocomplete` (`email`, `tel`, `one-time-code`, `cc-number`); font size at least 16 px on phone inputs so browsers do not zoom.
- Validate on leaving the field, not on every key and not only on submit. Error beside the field with icon and text, with the suggested fix; keep what was typed. A summary at the top alone is not enough; a tooltip is not an error channel.
- Submit button states the outcome ("Create account", "Pay 49"). Do not silently disable it: leave it active and show errors on press, or say what is missing.
- Accept varied formats (Postel) and echo your interpretation when a wrong reading is costly.
- Never ask again for what the process already has (3.3.7); never block paste in any code or password field (3.3.8).
- Progressive disclosure: at most two levels; the control that reveals says what comes next; in a stepper avoid forcing back-and-forth.

## 4. Checkout
Baymard "Cart Abandonment Rate Statistics" (read 2026-11-12 via study notes; US shoppers, physical goods): average cart abandonment 70.22 percent (50 studies, range 55-84). Reasons at checkout: extra costs too high 40 percent, slow delivery 20, did not trust the site with card 19, account creation required 18, checkout too long or complicated 17, site errors 17, return policy 13, could not see total upfront 12, card declined 10, too few payment methods 9. Average checkout shows 23.48 form items (14.88 fields); the measured ideal is 12-14 items (7-8 fields). Use as direction, not as your own conversion forecast.

Rules:
- Count the form items in the default flow; aim for 7-8 fields.
- Total visible before payment; no cost that appears at the end.
- Guest purchase; the account can be created afterwards with the purchase email.
- Local payment methods visible, the usual one preselected; trust signals near the sensitive field.
- Coupon and extras collapsed. Add-ons come before payment, one line, unchecked by default. A pre-checked box that charges is a prohibited practice in the EU (Directive 2011/83/EU art. 22; confirm local law).
- A payment error keeps all input and says nothing was charged. The pay button shows processing and ignores double taps.
- After paying, the next step is using the product.
- Countdown timers and scarcity messages only when true.

## 5. Onboarding steps
Screen-level UX only (activation metrics belong to the `onboarding` skill).
- One goal per step; a visible next step; progress that is honest; "Skip" always available; defaults preselected.
- Do the task rather than describe it: teach in context (Paradox of the Active User). Avoid a tour at the door that people dismiss.
- Back never loses data; the same position for "Next" at every step; the end has its own screen with result and one action (Peak-End).
- Ask for notification permission after value is shown, with a preview of what will be sent.

## 6. Tables, lists, bulk actions
NN/g data tables and bulk actions guidance (read in study notes 2026-11-13, not re-fetched):
- A table serves four tasks: find, compare, view or edit a row, act on records. First column is a human identifier, never a machine id; columns by importance; sticky header and first column; filters discoverable with visible active state.
- Lists are paginated or virtualized with a cap; never load unbounded lists.
- Deep editing in a side panel that does not cover neighboring rows; inline edit only in narrow tables with a visible edit mode.
- Mobile tables: design the desktop first; keep the header visible; freeze the left column; signal horizontal scroll; or switch to cards with the next action.
- **Bulk actions**: row selection, a contextual action bar, "select all" when the entire set is a valid target, feedback with Undo. Stronger rule used here: **before writing, show how many and which items, let the person remove items, then write once with a single undo.** The button that starts the batch opens the list; Confirm lives inside the list. Single-item actions stay direct.
- Keyboard accelerators: an extra path, discoverable in tooltips, never overriding copy and paste; hover-only reveals need another route.
- Complex apps serve three people: the efficient expert, the long-time user who dislikes sudden change, and the domain expert new to the software. Announce workflow changes and keep what works.

## 7. Empty, loading, error states
- An empty screen communicates status: finished with no result, or still loading? "No records" while loading is false and destroys trust. Use a skeleton while loading.
- Empty states teach (what this area does) and give a direct path (a button that opens the step, not only an instruction).
- "Nothing detected" after processing is an error of processing, not a success; say so and offer retry.
- Error states: say what failed, what is preserved, one next action. Offline, permission denied and read-only are separate states with their own copy.
- Design every state; mock-ups that show only the full screen hide most defects.

## 8. Optimistic UI
Update immediately only for actions that rarely fail, state what happens on failure (revert and tell the person), and take the real value from the server response. Prefer relative updates ("add 1") over absolute values read from stale state. Text input stays synchronous; only derived results (filtered lists) may be deferred.

## Sources
- https://www.nngroup.com/articles/response-times-3-important-limits/ (read 2026-11-15)
- https://www.nngroup.com/articles/progress-indicators/, /confirmation-dialog/, /user-control-and-freedom/, /user-mistakes/, /errors-forms-design-guidelines/, /indicators-validations-notifications/, /progressive-disclosure/, /data-tables/, /mobile-tables/, /empty-state-interface-design/, /ui-accelerators/, /complex-apps-users/, /usability-heuristics-complex-applications/ (read 2026-11-13 via study notes, not re-fetched)
- https://www.nngroup.com/videos/bulk-actions-design-guidelines/ (study notes, not re-fetched)
- https://baymard.com/lists/cart-abandonment-rate (read 2026-11-12 via study notes, not re-fetched)
- https://baymard.com/blog/checkout-flow-average-form-fields (11.3 average fields, target 8; read 2026-11-15)
- https://www.nngroup.com/articles/confirmation-dialog/ (published 2018, reviewed 2026-08-07), /errors-forms-design-guidelines/ (2019, reviewed 2024), /progress-indicators/ (2014), /user-mistakes/ (2015), /data-tables/ (2022), /progressive-disclosure/ (2006), /empty-state-interface-design/ (2021): re-read 2026-11-15, consistent with the summaries above
- https://developer.apple.com/design/human-interface-guidelines/undo-and-redo and /alerts (study notes, not re-fetched)
- https://react.dev/reference/react/useOptimistic (study notes, not re-fetched)
- https://www.w3.org/WAI/WCAG22/Understanding/error-prevention-legal-financial-data.html (study notes, not re-fetched)


## Checkout transparency (lesson from a real with/without test, 18/11/2026)
Beside the pay button: item and plan, price per period, total charged today including tax, promo applied and its duration, renewal price and date, how and until when to cancel, and the payment state after a decline (what happened, what to do, other method). The pay label repeats the amount ("Pay 47.99 EUR"). A link to the Terms alone hides the renewal; consumer law in many countries asks for these facts before payment (route to offers and customer-support).
- Wallet buttons: use the official Apple Pay and Google Pay buttons (logo plus "Pay", the provided black or white variants, minimum sizes and clear space from each brand's guidelines), never plain text in a box; a home-made payment button looks fake and lowers trust (owner review, 18/11/2026). Check the current Apple Pay and Google Pay brand guideline pages before shipping.

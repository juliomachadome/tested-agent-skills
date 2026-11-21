# Diagnosis playbook: symptom, likely cause, check, fix

Use it top-down. Step 0 first: the wrong person, task or denominator makes every branch meaningless. Evidence tags: **[C]** consensus or standard, **[M]** serious but single or correlational study, **[F]** practitioner starting point, **[X]** myth. Thresholds marked [F] are starting points; the product's own last 8-12 weeks replace them. Ideas are restated, not copied (sources in `BIBLIOGRAPHY.md`).

## Contents
1. Step 0: who, task, context, evidence
2. Worked numbers (funnel, success rate, small tests, SUS)
3. Trees: forms and checkout; onboarding; findability; errors and tickets; slow perceived speed; mobile; accessibility; permissions and empty states; search; notifications; dark-pattern accusation

## 1. Step 0: who, task, context, evidence
Ask before opining. Missing answers go in the "not verified" list of the final report.
| Question | Why | If unknown |
|---|---|---|
| Who is stuck (segment, new vs returning, language, assistive tech)? | An average hides a segment: a form can work for desktop and fail for 40% of mobile | Split every number by device and new/returning before reading it |
| Which task, with what goal and what counts as done? | "Drop-off" at a step is only a problem if the step was needed | Write the task as one sentence and one observable end event |
| Context: device, interruptions, one hand, bad network, time pressure | Situation changes the right design | Look at device and network mix in analytics; ask support |
| Analytics: event definitions, time window, bot filtering, consent loss | A step event that fires twice or only after consent skews the funnel | Compare 3 sessions by hand against the export; list events with no consent |
| Recordings and heatmaps | Show what people did, not why | Watch 10-20 sessions of the failing segment; note rage clicks, back, retype |
| Support tickets and reviews | Show why in the person's words | Tag 50 tickets by step and cause; count, do not cherry-pick |
| Accessibility needs | Failures here are invisible in averages | Run the keyboard and screen-reader pass (`playbooks.md` section 4) |
| What changed (release, copy, price, traffic source, campaign) | A new traffic source changes intent | Line changes up on the timeline before naming a cause |

Rule: analytics say where, recordings say what, interviews and tickets say why. Do not fix a "why" from analytics alone [C].

## 2. Worked numbers
**Funnel drop-off** (checkout, 10,000 carts started):
| Step | Reached | Next step | Step drop-off | Lost |
|---|---|---|---|---|
| Cart | 10,000 | Account | 38.0% | 3,800 |
| Account | 6,200 | Address | 25.0% | 1,550 |
| Address | 4,650 | Shipping | 5.8% | 270 |
| Shipping | 4,380 | Payment | 34.5% | 1,510 |
| Payment | 2,870 | Done | 16.0% | 460 |
Overall 2,410 / 10,000 = 24.1%. Step drop-off = 1 - next / reached. Rank by people lost and by how fixable: the 38% at cart-to-account is partly "just browsing" (not fixable), the 34.5% at shipping-to-payment suggests a surprise cost or a broken step. Check the reasons against Baymard's abandonment reasons (extra costs, forced account, complexity, errors) before choosing [M]. A drop at a step where the event can fire without a user action (auto-redirect) is a tracking bug until proven otherwise.

**Success rate with an interval** (small tests). Report counts with a Wilson interval, not a bare percent: z = 1.96, p = x/n, centre = (p + z²/2n) / (1 + z²/n), half-width = z·sqrt(p(1-p)/n + z²/4n²) / (1 + z²/n).
| Result | n | Rate | 95% interval |
|---|---|---|---|
| 4 of 5 | 5 | 80% | 38% - 96% |
| 12 of 15 | 15 | 80% | 55% - 93% |
| 5 of 6 | 6 | 83% | 44% - 97% |
Same 80%, but with 5 users the true rate could be under 40%. A small test finds problems, it does not measure rates [C]. Partial success: define credit in advance and report full-success separately.

**Time on task.** Times are right-skewed: use the geometric mean (mean of logs) and a t-interval on the log scale, and median as a cross-check. Example, 5 successful times (48, 62, 75, 51, 66 s): geometric mean 59.6 s, 95% interval 47.4 - 74.9 s (t = 2.776, 4 df). Exclude failed attempts from time, report them in success rate. Never average a time-out and a success.

**How many users: Nielsen and Landauer.** Model: found = 1 - (1 - L)^n, with L the share of problems one user finds (31% typical in their projects [M]):
n = 1: 31%; 3: 67%; 5: 84%; 10: 98%; 15: 99.6%. If L is 10% (rare problems, varied users, complex product) 5 users find only 41% and 15 find 79%. Limits [M]: L varies by project and task, problems are not equally findable, users are assumed similar, the model counts problems found not problems fixed. So: 5-8 users per round per distinct user group, test again after fixing, use 15+ per group for card sorting, 20+ for quantitative claims (NN/g) [F]; "5 users is enough" for a quantitative rate is [X].

**SUS scoring.** Ten items, 1-5. Odd items score (answer - 1), even items score (5 - answer), sum, times 2.5 gives 0-100. Answers 4,2,4,1,5,2,4,2,4,2: odd items give 3+3+4+3+3 = 16, even items give 3+4+3+3+3 = 16, total 32 x 2.5 = 80. The mean over many products is about 68 (MeasuringU benchmark of 500 studies, used by NN/g); a SUS is not a percentage and is not a diagnosis, it says "how bad", not "where". With 5-6 users report the range, not a decimal mean.

## 3. Trees

### 3.1 Users abandon a form or checkout
| Likely cause | Check | Fix |
|---|---|---|
| Too many fields (Baymard average 11.3 in 2024 checkouts, ideal about 8) [M] | Count visible fields and steps; per-field drop and time in analytics | Remove, derive (postcode to city), combine name; show optional fields collapsed |
| Forced account | Share of guest vs account; reasons in tickets | Guest checkout first, offer account after the order |
| Surprise costs or total hidden | Total visible from step 1? Tickets mentioning price | Show shipping, tax and total early |
| Errors only on submit or premature inline errors | Recordings: retype, error loops; inline validation timing | Validate on blur after typing, remove the error when fixed, preserve input [M] |
| Placeholder as label, wrong keyboard, no autofill | Inspect `autocomplete`, `type`, `inputmode` | Visible labels, correct attributes (`playbooks.md` 3) |
| Trust gap at payment | Payment step drop and tickets about security | Known payment methods, clear security and returns text, no new pop-ups |
| A bug (one browser, one field, a validator rejecting valid input) | Split by browser, country, field; error event counts | Fix and re-measure before any redesign |

### 3.2 Onboarding drop-off
| Likely cause | Check | Fix |
|---|---|---|
| Value arrives too late | Time and steps to first meaningful success | Cut to the first win; defer profile and setup |
| Setup before value (permissions, long forms, tour) | Per-step drop; skip rate of the tour | Ask later in context; replace the tour with in-context hints (NN/g: contextual help beats up-front tutorials [M]) |
| Wrong expectations from the marketing promise | Compare landing promise with first screen; interview | Align promise and first screen; hand copy to the copywriting skill |
| Empty first screen | Screen shows "no data" with no route | Designed empty state with one action and a sample (3.8) |
| Segment mismatch | Funnel by acquisition source and role | Branch the path by the one question that changes it |
Metrics and lifecycle messaging belong to the `onboarding` and `growth-analytics` skills; this file covers the screens.

### 3.3 Feature not found
| Likely cause | Check | Fix |
|---|---|---|
| Label uses the maker's words, not the user's | First-click test or tree test with the real task wording (`playbooks.md` 5) | Rename with the words from tickets and search queries |
| Wrong group in the information architecture | Open card sort (15+ users per group), then tree test | Regroup; put it where the majority looked first |
| Hidden behind an icon, hover or overflow menu | Recordings: do users scan past it? | Visible label; promote if used by many (frequency, not opinion) |
| Weak information scent (the link does not hint at the content) | Do labels on the path match the task words? | Make each level's label carry the target's words |
| The need is seasonal or role-bound | Segment usage | Contextual entry points; do not promote to everyone |

### 3.4 Errors and support tickets about the same step
1. Tag 50 tickets to find the step and the sentence people use. 2. Compare with error events at that step. 3. Reproduce as the person (device, locale, assistive tech). 4. Choose: prevent (constraint, default, preview), explain (what, why, next action, next to the field), or recover (undo, input kept, draft saved). A ticket spike right after a release is a regression until shown otherwise. Document the fix in the help article too; handing the article to support belongs to the customer-support skill. Measure: tickets per 1,000 users at that step, before and after.

### 3.5 Slow perceived performance
Actual speed is for `web-performance`; this is how it feels. Limits: about 0.1 s feels instant, 1 s keeps flow, 10 s loses attention (Nielsen) [C].
| Situation | Pattern |
|---|---|
| Under about 1 s | Nothing; do not flash a spinner |
| 2-10 s, layout known | Skeleton screen matching the real layout (NN/g: use under 10 s), no animated shimmer for reduced motion |
| Over 10 s | Determinate progress, named steps, a way to cancel, work continues in the background |
| Action with predictable success (like, rename, toggle) | Optimistic update plus visible rollback with an explanation if the server refuses [F] |
| Loading that is really an empty result | Distinct empty state, not a perpetual skeleton |
Check: record the screen at 3G throttling, count seconds to first useful content and to interactive. Never invent a percent or an estimate you do not have.

### 3.6 Mobile usability problems
| Symptom | Cause | Fix |
|---|---|---|
| Mis-taps, repeated taps | Targets under about 1 cm (NN/g), under 44 pt (Apple) or 48 dp (Material) [C], tight spacing | Enlarge hit area (padding counts), 8 px gaps; WCAG minimum is 24 CSS px [C] |
| Key actions out of reach | Primary action at the top on a tall phone | Bottom bar or sheet; keep destructive actions away from the thumb path |
| Typing is slow | Wrong keyboard | `type`, `inputmode` (numeric, decimal), `autocomplete`; paste allowed; no confirm-email fields |
| Keyboard covers the field or the button | Fixed bars, no scroll into view | Test with the keyboard open; sticky action above the keyboard |
| Content jumps while reading | Late images or banners | Reserve space; no banners that push content after load |
| Session lost on interruption | State in memory only | Save drafts; deep links return to the step |
Test on a real device, one-handed, outside, with a poor network; emulators do not show reach.

### 3.7 Accessibility complaints
| Complaint | Likely cause | Check | Fix |
|---|---|---|---|
| "I cannot reach it with the keyboard" | Click handler on a div, custom widget without keys | Tab through; Enter and Space on every control | Native element first; if custom, build the keyboard pattern (APG) |
| "I get lost" | Focus order differs from visual order; focus hidden by sticky bar or lost after a dialog closes | Tab order vs layout; 2.4.3, 2.4.7, 2.4.11 | Reorder DOM, scroll-padding, return focus to the trigger |
| Screen reader says "button" with no name or reads everything twice | Missing accessible name, duplicated label, `aria-label` that differs from visible text | Inspect the accessibility tree; 4.1.2, 2.5.3 | Name from visible text; remove redundant ARIA |
| ARIA made it worse | `role` without its keyboard behavior; `aria-hidden` on focusable content; wrong `aria-live` | "No ARIA is better than bad ARIA" (APG) | Remove the role or implement the full pattern |
| Errors not announced | Error shown visually only | 3.3.1, 4.1.3 | Text error linked with `aria-describedby`; status region; focus the first invalid field or an error summary |
| Cannot zoom or reflow | Fixed widths, viewport zoom disabled | 200% zoom and 320 px | Responsive layout; never disable zoom |
Detail and criteria: `accessibility-wcag22.md`. Automated tools cover only part of the criteria [F], so a manual pass is required.

### 3.8 Users confused by permissions and empty states
| Symptom | Cause | Fix |
|---|---|---|
| Users deny notification, camera or location | Asked at launch with no context (NN/g permission requests) | Ask at the moment of need, one line of why, a way to continue without it, explain how to change later |
| Feature "does nothing" | Disabled by role with no explanation | Show it disabled with the reason and who can grant access, or hide only if nobody would look for it |
| Blank screen on first use | Empty state is a dead end | Say what goes here, one primary action, optional sample data |
| Blank after a filter | Looks like a bug | "No results for these filters", show active filters, clear button |

### 3.9 Search returns nothing useful
| Likely cause | Check | Fix |
|---|---|---|
| Exact match only, no typo, plural or synonym handling | Top zero-result queries (Baymard: many sites mishandle query types) [M] | Typo tolerance, synonyms from the zero-result log |
| Zero-result page is a dead end | The page itself | Echo the query, suggest alternatives, show popular items, keep the box filled (Baymard) |
| Results order ignores intent | Click position of the chosen result | Tune ranking with click data; filters that fit the catalog |
| Search box is hard to find or too small | NN/g: visible and simple | Wide box at the usual place with a labeled icon |
Measure: zero-result rate, refinement rate, click position, exits after search.

### 3.10 Notification fatigue
Symptoms: opt-out rate rises, app uninstall after a push, ignored e-mails. Causes: sent for the company's goals, not the person's; no categories; no frequency cap; asked too early (NN/g push mistakes). Fix: categories the person chooses, per-category off switch, a cap, send only what is time-sensitive and personal, honor quiet hours, and ask for permission after value is shown. Check: opt-out and mute rate per category before and after; do not count opens as value.

### 3.11 "Your design is a dark pattern"
1. List the specific accusation (pre-ticked box, hard cancel, hidden costs, fake urgency, confirm-shaming, nagging). 2. Compare with the taxonomies (Gray et al. 2018; Mathur et al. 2019: a crawl of shopping sites that found dark patterns on a minority of them, urgency and scarcity messages among them; the exact share is not re-read here; deceptive.design list). 3. Test the symmetry: is declining as easy as accepting, is the cancel path as short as sign-up, is every claim true. 4. Fix: neutral defaults, equal-weight options, honest counters or none, plain wording. 5. Legal exposure (EU consumer law, DSA, state laws) is for counsel; flag it, do not rule on it. A metric win from a manipulative design is not a defense, and it borrows from retention.

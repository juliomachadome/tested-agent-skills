# UX writing: buttons, forms, checkout, states, e-mail, store listings

## Buttons and CTAs
- **[M] The button says what the person gets or what happens on tap**, not what the system does. "Submit" and "Learn more" are empty. The label completes "I want to…" or names the next step. Pattern: verb + what they get (+ qualifier).
- **[F] "First person in the button converts 90% more"** comes from one 2013 test. Do not generalise; test, and keep what sounds natural in the language. [1-SRC]
- **[C] One primary action per screen;** secondary actions exist with less weight. Legal exception: declining an offer cannot be hidden or shaming [EU].
- **[M] A support line glued to the button** answers that instant's fear in one line: total cost, one-off or recurring, when access arrives, how to undo. Not a slogan slot.
- **[C] Price is always complete:** final amount with taxes, local currency, periodicity ("one payment" or "per month"), and anything not included.

## Forms and checkout
- **[C] Surprise cost is the biggest avoidable abandonment reason.** Large US survey (excluding "just browsing"): extra costs 40%, did not trust the site with the card 19%, forced account 18%, long checkout 17%, could not see the total upfront 12%, too few payment methods 9%. (Baymard, read 07/11/2026)
- **[C] Labels outside the field, always visible.** Placeholder-as-label disappears while typing and hurts errors and accessibility. (NN/g)
- Say why you ask for any non-obvious field ("E-mail: where we send your access").
- **[C] Error message = what happened + how to fix it**, next to the field, no blame, no technical code. "Your bank declined the card. Try another card or payment method." Never "Error 402" or "You typed it wrong". (NN/g)
- **[C][EU] The pay button says it is a payment and how much** ("Pay 49 EUR", or the legal formula "order with obligation to pay"). Legal obligation, not a copy choice.
- After payment the screen confirms what was bought, how much was charged, what happens now and where the access is. The end of the purchase is what people remember (peak-end); "instant access" that lands on a broken login breaks trust at the worst moment.
- Empty, loading and success states are copy too: say what is happening and the next step, in one line.

## E-mail
- **[C] Separate transactional from marketing.** Transactional (confirmation, access, receipt, account notice) executes the contract and carries no offer or commercial P.S. Marketing needs the legal basis of the country [EU]. Mixing them turns the transactional e-mail into marketing.
- **[C] Open rate is unreliable since 2021** (mail clients pre-load images for privacy). Decide by clicks, replies and sales.
- **[F] No magic subject length.** Solid: phones cut around 30-40 characters, so the fact goes first; sender name weighs as much as the subject; the preheader continues the subject instead of repeating it; the subject promises only what the e-mail delivers.
- One e-mail, one goal, one main link; the first line says why the e-mail exists; short running text, person to person.
- **[C] Bulk-sender requirements** (major mailbox providers since Feb 2024): SPF, DKIM and DMARC; one-click unsubscribe header plus a visible link; spam complaint rate below 0.3%. Spammy copy (deceptive subject, fake urgency) hurts deliverability of every e-mail, including access e-mails.
- Sequences: each e-mail adds a new fact (proof, objection answered, product use). Repeating the offer with a louder subject is pressure, not argument.

## App-store listings
- Character limits change; check the current store docs and date the check. Values commonly cited as of late 2026: iOS app name and subtitle 30 characters each, iOS keyword field 100; Google Play short description 80. [verify before use]
- Listing copy follows the same rules: specific, provable, no outcome promises the store or the law would reject; in-app UI text lives in the app's i18n catalogue, not hard-coded.
- Stores forbid pointing to cheaper purchase paths outside the store from inside the app (check current guidelines).

**Count with a tool.** Notification, subject-line and SMS limits are checked with a real count (a script or the editor's counter), never by eye; report the numbers.

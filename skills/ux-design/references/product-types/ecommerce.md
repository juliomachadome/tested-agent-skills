# E-commerce

## Key jobs
A shopper finds the right product, trusts the seller, knows the total, pays without friction and knows what happens after. The store wants fewer abandoned carts and fewer returns and tickets.

## Critical flows
Search and filtering; product list and product page (images, size and fit, stock, delivery date, price with tax); cart; checkout; payment; confirmation and order tracking; returns.

## Typical pitfalls
- Hidden extra costs: the largest reported reason for abandonment (Baymard's list: extra costs, slow delivery, trust, forced account, complex checkout, errors, returns policy, total not visible).
- Forced account creation before payment; too many fields (Baymard 2024 average 11.3 checkout fields, ideal about 8); redundant entry.
- Placeholder-only labels, wrong keyboards, no autofill, errors only on submit.
- Pre-ticked add-ons, fake countdowns, fake scarcity, confirm-shaming: deceptive patterns; legal exposure for counsel.
- Search that fails on typos and synonyms; "no results" dead ends (Baymard).
- Delivery date missing on the product page; size and fit guidance absent, which drives returns.
- Filters that reset, product images that cannot zoom on mobile, sticky bars hiding the pay button.

## Metrics
Cart abandonment (Baymard average across studies about 70%, a reference, not a target; compare with your own); step drop-off; checkout completion by device; payment failure rate and reason; zero-result search rate; return rate by reason; tickets per 1,000 orders. Use Wilson intervals for small A/B segments (`../diagnosis-playbook.md`).

## Checklist
- [ ] Total, tax, shipping and delivery date visible before the last step.
- [ ] Guest checkout first; account offered after the order.
- [ ] Form checklist (`../playbooks.md` 3) passed; wallets and autofill on mobile.
- [ ] Order summary visible and editable; coupon field not a lure to leave (collapsed).
- [ ] Errors inline, input kept, payment retry without re-entering the cart.
- [ ] Zero-result search suggests alternatives; filters persist.
- [ ] Returns and cancel path easy to find; confirmation page says what happens next.
- [ ] Targets at least 44 px on mobile; pay button not covered by banner or keyboard.

## Worked check
Start a checkout on a phone with the keyboard open: count fields, note every field where the wrong keyboard appears, and note whether the total and delivery date are visible without scrolling at the pay step.

## Sources
Baymard cart abandonment statistics, checkout form fields, inline validation, no-results page, search UX, accordion checkout; NN/g form errors and placeholders; Mathur et al. 2019 and Gray et al. 2018 on dark patterns; WCAG 3.3.7, 3.3.8.

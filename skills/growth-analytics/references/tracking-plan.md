# Tracking plan template and rules

Full routine and rationale: `playbooks.md` 2. Consent rules: `playbooks.md` 7 and the privacy law of the data subject's country (official regulator pages).

| event | trigger | properties (type, allowed values) | side | consent category | PII | owner | decision served | version | status |
|---|---|---|---|---|---|---|---|---|---|
| account_created | account row committed | method (enum: email, google), plan (enum) | server | analytics | no | growth | activation rate by method | 1 | live |
| project_created | user confirms creation | template_used (bool), source (enum) | server | analytics | no | product | activation | 1 | live |
| checkout_started | checkout page rendered | plan (enum), price_minor (int), currency (ISO 4217) | client | analytics | no | growth | funnel step conversion | 2 | live |
| invoice_paid | payment confirmed by provider webhook | order_id (opaque), amount_minor (int), currency, plan | server | strictly necessary or business record | no | finance | revenue reconcile | 1 | live |

Naming: object_action, snake_case, past tense, no UI wording. Properties named the same across events. One event per meaning. Booleans start with is_ or has_.

Identity: anonymous id on first visit; on login, alias to user id once; never reuse ids across people; document merge rules, logout, shared devices, and the account id for B2B.

Quality gates: schema validation in CI; alert when an event volume falls below a floor or moves more than a set share day over day; dated changelog; deprecation window before removal; weekly reconcile of purchases and signups with the database (within 2-5%, effect of consent explained); test accounts excluded.

Privacy: no emails, names, free text or precise location in properties; a hash is not anonymisation; map each event to its lawful basis, consent category and retention; log the consent state with the event or session.

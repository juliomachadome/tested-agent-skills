# SaaS B2B

## Key jobs
A team gets recurring work done faster and with fewer mistakes; an admin controls access and cost; a buyer sees value before the trial or contract ends. Different people hold each job: the user who lives in the product, the admin who configures it, the buyer who pays.

## Critical flows
- **First value:** signup or invite, first successful outcome, invite teammates. Time to first value is the north star of onboarding.
- **Daily loop:** dense tables, filters, saved views, bulk actions, keyboard shortcuts.
- **Admin:** roles and permissions, billing, seats, SSO, audit log, data export.
- **Permission and empty states:** a feature unavailable by role or plan must say why and who can grant it.
- **Billing and trial end:** what happens to data, plain wording, easy cancel and export.

## Typical pitfalls
- Designing for the admin demo and not the daily user; a feature-per-menu navigation that mirrors the org chart of the vendor.
- Bulk actions without preview, count and a single undo on thousands of rows (`../forms-states-feedback.md`).
- Dense tables with sticky headers hiding focus, drag-only reordering, color-only status.
- Settings sprawl; permission errors with no next step; "contact your admin" with no admin named.
- Empty dashboards on day one; tours instead of contextual help (NN/g).
- Invited users landing in an empty account with no context of who invited them.

## Metrics
Time to first value; activation (the event that predicts retention, from the team's data); weekly active teams; invite acceptance rate; task success and time for the 3 core tasks; support tickets per 1,000 active users by area; SUS from admins and users separately (SUS average is about 68). Funnel arithmetic in `../diagnosis-playbook.md`.

## Checklist
- [ ] Three personas named (user, admin, buyer) and each core task mapped to one.
- [ ] Every table: filters, sort, empty, loading and error states, row selection by keyboard, 24 px minimum targets (2.5.8).
- [ ] Bulk write: preview, count, remove items, one write, one undo, announced result.
- [ ] Locked or hidden features explain reason and route.
- [ ] Destructive actions name the item and effect; roles can be tested by switching view.
- [ ] Export and cancel are discoverable; no dark patterns at downgrade.

## Sources
NN/g data tables, empty states, confirmation dialogs, onboarding vs contextual help; WCAG 2.2 2.5.7, 2.5.8, 2.4.11; Cooper About Face (goal-directed design, personas); Rubin and Chisnell for testing admin and user tasks separately.

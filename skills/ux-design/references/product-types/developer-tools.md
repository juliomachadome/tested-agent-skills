# Developer tools

## Key jobs
An engineer gets from "heard of it" to a working call, deploy or integration quickly, then debugs, monitors and upgrades with confidence. They judge in minutes whether the docs and the tool respect their time.

## Critical flows
Landing to docs to quickstart; sign-up and keys; first successful request ("time to first call"); console and dashboards; logs, errors and debugging; CLI help and output; migration and upgrades; billing limits and quotas.

## Typical pitfalls
- A quickstart that does not run as written; copy buttons missing; keys shown once without a warning; examples in one language only.
- Error messages without cause or next step (the same rules as forms: what, why, fix); status codes alone.
- Search in the docs that fails on the identifier a developer types; pages that move without redirects.
- Dashboards with color-only status and charts with no table alternative; dark mode that hurts code contrast.
- CLIs: no `--help` examples, no non-interactive mode, ANSI color only for meaning, unclear exit codes.
- Destructive operations (delete project, rotate key) without a named confirm and a preview.
- Sign-up walls before a sandbox.
- Pricing and rate limits discovered only when a limit is hit; no warning before the quota ends.
- Changelogs and deprecations announced where nobody looks.

## Metrics
Time to first successful call; docs search success and zero-result queries; quickstart completion; error rate by message and the share that leads to a ticket; support questions per docs page; upgrade completion; SUS from engineers (small n: ranges not decimals). Instrument with consent; docs analytics and funnels go to `growth-analytics`.

## Checklist
- [ ] Quickstart tested from a clean machine, by a person who did not write it, timed.
- [ ] Every error links to a doc and names a fix; request id is copyable.
- [ ] Code blocks: copy, language tabs, keyboard accessible, selectable text; syntax color is not the only signal.
- [ ] Console: keyboard access, status by shape plus color, table views for charts.
- [ ] CLI: `--help` with examples, scriptable output (JSON), predictable exit codes.
- [ ] Destructive actions: named effect, typed confirmation only for the rare catastrophic case; undo where possible.
- [ ] Docs navigation labeled with the words developers search for (tree test).

## Worked check
Hand the quickstart to an engineer who has never seen the product, say nothing, and time to the first successful call; note every pause longer than 30 seconds as a doc defect.

## Sources
NN/g errors in forms guidelines (transferable), confirmation dialogs, information scent, tree testing; WCAG 1.4.1, 2.1.1, 2.4.7; Krug; Cooper About Face (goal-directed design for experts); Hall Just Enough Research for learning from engineers cheaply.

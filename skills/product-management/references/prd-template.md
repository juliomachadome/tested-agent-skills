# PRD template (1-2 pages)

1. Title, owner, date, status.
2. Problem and evidence (links to interviews, tickets, data).
3. Who: segment and job to be done.
4. Goal: metric, baseline, target, date; guardrail metrics.
5. Non-goals.
6. Proposed solution: flow summary, states (empty, loading, error, permission), edge cases, copy owner, accessibility notes.
7. Acceptance criteria: numbered, testable. Example form: Given a signed-in user with no items, when they open the list, then an empty state with one primary action is shown.
8. Risks and assumptions: each with test and owner.
9. Rollout: flag, cohort, monitoring, rollback trigger.
10. Instrumentation: events and properties needed to read the goal.
11. Open questions and decisions needed, with deadline.
12. Reason test result: evidence, outcome, smallest scope, what was removed.

How to fill each section, the working-backwards variant and the review routine: `playbooks.md` 3. Decision record format: `playbooks.md` 8.

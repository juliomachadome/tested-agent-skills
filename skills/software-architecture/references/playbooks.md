# Playbooks: practical routines

Evidence tags as in SKILL.md. Ideas applied, not copied. Templates: `adr-template.md`; quick yes/no gates: `decision-checklists.md`; symptoms: `diagnosis-playbook.md`; style details: `styles/`.

## 1. Architecture review
Inputs to ask for (state which are missing, do not invent): repo layout or module list, deploy config, a dependency graph or import map, ADRs and glossary, traffic and data volume numbers, SLOs, incident list of the last 6 months, team size and on-call, cost per month.
Questions: What must stay changeable? What are the top 3 characteristics and their numbers? What fails first at 10x load? What is the failure story for each dependency (timeout, retry, fallback)? Who owns each table, queue and module? Where can one tenant or one bug hurt everyone? What was the cheapest option dismissed, and why? What is manual that should be a check?
Output (one page): findings by severity (blocker, risk, smell) each with evidence (file, trace, metric), the simplest fix, what to leave alone, 3 fitness functions, open questions, ADRs to write. Do not rewrite the system in a review.

## 2. Design doc / RFC
Sections: context and goals; non-goals; characteristics with numbers; quality scenarios ("when X, the system does Y within Z"); options (include "do the least") with cost, risk, reversibility; recommendation; data model and ownership; failure modes and rollout/rollback; security and privacy; observability and SLOs; cost estimate; open questions; decision deadline. Keep it to 2-4 pages; review asynchronously with a named decider; the result is an ADR, the RFC is the discussion record **[F]**.

## 3. Choose characteristics (Richards and Ford)
Pick at most 3-5 driving characteristics; the rest are "good enough" **[M]**. Score each candidate style 1 (poor) to 5 (strong) per characteristic, weight by importance (1-3), multiply and sum. The table is a thinking aid: the ranking matters less than the argument about weights.
| Characteristic (weight) | Modular monolith | Microservices | Event-driven | Serverless |
|---|---|---|---|---|
| Simplicity / cost to run (3) | 5 | 1 | 2 | 4 |
| Independent deploy (2) | 2 | 5 | 4 | 4 |
| Elasticity (1) | 2 | 4 | 4 | 5 |
| Consistency / correctness (3) | 5 | 2 | 2 | 3 |
| Tenant isolation (2) | 2 | 4 | 3 | 3 |
Weighted sums: monolith 5x3+2x2+2x1+5x3+2x2 = 40; microservices 3+10+4+6+8 = 31; event-driven 6+8+4+6+6 = 30; serverless 12+8+5+9+6 = 40. Scores are example values; replace them with the team's and show the working. A tie means pick the cheaper to reverse.

## 4. Extract a module or service safely
1. Reason test: independent scale, team, runtime, isolation or failure domain, with a metric. No reason, stay a module.
2. Find seams: where calls cross a narrow set of functions; tables read by only one module; events already emitted. Make the boundary real inside the monolith first (own folder, interface, own tables, lint rule).
3. Branch by abstraction (Fowler): put an interface in front of the old implementation, move callers to it, add the new implementation behind a flag, switch gradually, delete the old one.
4. Strangler fig (Fowler): route a slice of traffic (by endpoint, tenant or percentage) at the edge to the new component; grow the slice; retire the old path. Keep rollback to the old path until a full cycle (a month-end, a billing run) passes.
5. Data: expand/contract. Dual-write only behind a reconciliation job; prefer change data capture or read from the old store through an API during transition; copy, verify counts and checksums, cut over, keep the old table read-only for a period.
6. Prove it: contract tests, shadow traffic comparing responses, SLO and cost dashboard for the new unit, on-call named. Write the ADR and the revert plan.
Anti-patterns: extracting the database last, extracting the most entangled module first, big-bang cutover **[M]** (Newman, *Monolith to Microservices*).

## 5. Fitness functions: examples
Automated checks that guard a characteristic **[M]** (Ford et al.). Run in CI; fail the build; each has an owner.
- Dependency direction (JVM): ArchUnit `noClasses().that().resideInAPackage("..domain..").should().dependOnClassesThat().resideInAPackage("..infrastructure..")`.
- JS/TS: dependency-cruiser rule `forbidden: [{ name: "domain-no-infra", from: { path: "^src/domain" }, to: { path: "^src/infrastructure" } }]`; or eslint boundaries/`no-restricted-imports` for module-internal paths (only import a module's `index`).
- Python: import-linter contracts (layers, forbidden). .NET: NetArchTest or ArchUnitNET equivalents.
- Module owns its tables: a test or SQL-parse check that a module's queries only touch its schema or prefix; separate DB roles per module in staging.
- Latency budget: load test on a seeded dataset asserting p95 under the budget (for example 300 ms) and queries-per-request under N.
- Size and cost: bundle size limit; infra cost per tenant per month threshold alert.
- Resilience: a test that kills a dependency and asserts degraded mode; contract tests for events and APIs.
- Cycle detection: fail on circular module dependencies.

## 6. C4 diagram recipe
Level 1 context: the system as one box, people and external systems around it, arrows with purpose. Level 2 containers: deployable or runnable units (web app, API, worker, database, queue) each labelled with technology and responsibility; arrows with protocol and purpose. Level 3 components only for the one container that is being changed. Skip level 4 (use the code). Add a legend and a title with the date or version. Keep as text in the repo (Mermaid or Structurizr DSL) and review it in the PR that changes a boundary **[M]** (Brown).
Mermaid skeleton: `flowchart LR; user([Customer]) --> web[Web app: Next.js]; web --> api[API: Node, owns orders]; api --> db[(Postgres)]; api --> q[[Queue]]; q --> worker[Worker: emails]`.

## 7. ADR lifecycle
Create when a decision is costly to reverse, crosses teams, or someone asks "why did we do this?". Proposed (draft in PR, 2-3 reviewers, decider named) then accepted (merged, dated) then possibly superseded (new ADR links back; the old one is not edited except for the status line) or deprecated. Number sequentially; keep an index; one decision each, one page; add a "Revisit when" trigger with a number and review triggers in a quarterly pass. Link ADRs from code or module README, and from PR descriptions. Small reversible choices do not need an ADR; use a comment or the PR. Template: `adr-template.md`. Gates before writing: `decision-checklists.md`.

# ADR template (after Nygard, 2011)

# ADR-NNN: short title in the form of a decision
- Status: proposed | accepted | superseded by ADR-MMM | deprecated
- Date: YYYY-MM-DD
- Deciders: roles, not only names

## Context
Forces at play: needs, characteristics and numbers, constraints, what we know and do not know.

## Options considered
1. Option A (include "do nothing / do the least"): pros, cons, cost.
2. Option B: pros, cons, cost.

## Decision
We will ... because ...

## Consequences
Good, bad and neutral results; new risks; what becomes harder; what we will monitor.

## Revisit when
The measurable trigger that reopens this decision (for example "p95 above 400 ms for two weeks", "third team needs this module").

Rules: one decision per ADR; immutable once accepted (supersede, do not edit history); short (one page); live in the repo next to the code; link from the code or module README it affects.

Lifecycle, review cadence and when an ADR is not needed: `playbooks.md` section 7. Gates before writing: `decision-checklists.md`.

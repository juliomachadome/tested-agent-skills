# Decision checklists

Quick gates. Symptom-driven diagnosis: `diagnosis-playbook.md`; routines (review, RFC, extraction, fitness functions): `playbooks.md`; style details: `styles/README.md`; record the outcome with `adr-template.md`.

## Split or keep together?
Does it scale on a different axis? Different team or release rhythm? Different data store or compliance zone? Different failure tolerance? Can the boundary be a stable, versioned interface? If most answers are no, keep it a module.

## Queue or direct call?
Must the work survive a restart? Is retry needed? Can the caller proceed without the result? Are consumers idempotent? Is order required? Is there a dead-letter path and an owner who looks at it?

## Cache?
Which request is slow (measured)? Hit rate estimate? Staleness acceptable (seconds, minutes)? Invalidation event known? Stampede protection? Security: is the cached data tenant- and user-scoped?

## Consistency
Which invariants must hold at all times (single transaction), which may converge later (event, saga)? What does the user see in between? What reconciles errors?

## API and contracts
Version policy, error format, pagination with cap, idempotency keys for unsafe operations, backward-compatible changes by default, contract tests.

## Fitness function ideas
Dependency direction test; no import from module internals; query count per request budget; p95 latency in CI on a seeded dataset; bundle size limit; no table read outside its module; migrations reversible; secrets scan.

## Common smells
Shared database between services; synchronous chains of 4+ services; distributed transaction attempts; "utils" module that everything imports; config differences between environments that hide bugs; unbounded retries; one team owning ten services.

# Style: serverless (functions and managed services)

Code runs on demand on a managed platform (functions, edge, managed queues, databases) billed by use. Numbers [n] refer to `../BIBLIOGRAPHY.md`.

## When it fits
Spiky or low and unpredictable traffic; event-triggered glue and background tasks; small teams that want no server operations; prototypes; edge logic; scheduled jobs. Cost per request is low at low volume **[F]**.

## When it does not
Constant high load (a steady container or VM is often cheaper, compute the break-even: `../diagnosis-playbook.md` 9); long-running or stateful work beyond platform limits; strict tail latency where cold starts hurt; heavy connection use to a relational database; strong need for portability; deep local debugging needs.

## Core principles
Stateless handlers; one responsibility per function but not one function per line; state in managed stores; idempotent handlers (platforms retry); timeouts and concurrency limits set deliberately; infrastructure as code; least privilege per function; pay attention to the platform's limits (duration, memory, payload, concurrency).

## Structure
Per-capability folder with handler, domain code, and infrastructure definition; keep business logic in plain modules that handlers call (hexagonal, `hexagonal-clean.md`) so it runs without the platform; shared layer small; a queue between steps; a connection pooler or data API in front of relational databases.

## Data ownership and consistency
Same rules as services: one owner per data store; use queues with dead-letter, outbox or stream triggers for publish; conditional writes or unique keys for idempotency; remember retries cause duplicate invocations; per-invocation connections can exhaust a database, so pool or proxy.

## Operations and failure modes
Cold starts; throttling and concurrency limits; runaway cost (recursive triggers, retries, chatty function-to-function calls, egress); vendor lock-in; hard distributed tracing across many tiny functions; timeouts shorter than downstream; poison messages; noisy account-wide limits. Set budgets, alarms on invocations and spend, reserved concurrency for critical paths, and dead-letter queues.

## Migration in and out
In: peel off background jobs, webhooks, scheduled tasks from a monolith first. Out: because logic sits in plain modules, wrap them in a container and run it as a service when load is steady or limits bite.

## Checklist
Do: compute cost per request and per tenant monthly; set timeouts below the caller's; idempotent handlers; structured logs with correlation id; local test of core logic without the platform.
Avoid: functions calling functions synchronously; sharing a database connection per invocation unmanaged; business logic in handler files; unbounded fan-out; secrets in code.

## Fitness functions
Cost per request threshold and monthly budget alarm; max function duration vs timeout; cold-start p95 in a load test; test that core logic imports no platform SDK; concurrency-limit and dead-letter presence in IaC checks.

## Sources
Azure Architecture Center, architecture styles (web-queue-worker, event-driven) [26]; Nygard on stability [11]; Fowler and Newman for decomposition [9][15]. Price figures here are placeholders: check the provider's current price list.

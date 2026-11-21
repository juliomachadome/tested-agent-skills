# Style: hexagonal, clean and onion (dependencies point inward)

One family: the domain is at the centre and knows nothing about frameworks, databases or transport. Numbers [n] refer to `../BIBLIOGRAPHY.md`.

## When it fits
Real business rules that outlive frameworks; several entry points (HTTP, jobs, CLI, events) to the same logic; need for fast tests without a database; likely swap of an external provider; a team that will keep the code for years **[M]** [3][14].

## When it does not
Thin CRUD with few rules (the layers become ceremony); throwaway prototypes; a small script. Use a simpler layered or "vertical slice" layout and apply the pattern only to the modules with rules.

## Core principles
Hexagonal (Cockburn): the application core talks to the outside through ports (interfaces it defines); adapters implement them for a database, a queue, a UI or a test [14]. Clean Architecture (Martin): the dependency rule, source dependencies point inward; entities, then use cases, then interface adapters, then frameworks [3]. Onion is the same idea in rings. Shared point: invert dependencies so infrastructure depends on the domain.

## Structure
`domain` (entities, value objects, domain services, events) ; `application` (use cases, ports as interfaces, transactions) ; `adapters/inbound` (HTTP controllers, consumers) ; `adapters/outbound` (repositories, API clients, publishers) ; composition root wires them. Inside a modular monolith, each module has this shape. Code-level detail (naming, repositories, DTO mapping, lint rules): `skills/engineering-playbook`.

## Data ownership and consistency
Repository port returns aggregates; one transaction per use case, opened in the application layer; domain events collected by the aggregate and published after commit (outbox if leaving the process) [4][5]. Persistence models may differ from domain models; map at the adapter, do not leak ORM entities inward.

## Operations and failure modes
Cost is indirection: more files, mapping code, onboarding time. Failure modes: leaky ports shaped like the database; use cases that only forward calls; anaemic domain with rules in controllers; interface per class with one implementation and no reason; framework annotations creeping into the domain.

## Migration in and out
In: start at the edges, wrap the hardest external dependency behind a port, move rules inward use case by use case (branch by abstraction [20]). Out: collapse unused ports; flatten modules that stayed CRUD.

## Checklist
Do: define ports in the language of the domain; keep use cases small and named by intent; test the core with in-memory adapters; one composition root.
Avoid: ports that expose ORM types; a port for everything; domain importing the framework; transaction handling in controllers; premature generic repositories.

## Fitness functions
ArchUnit / dependency-cruiser / import-linter rule: `domain` and `application` do not import `adapters` or framework packages; test suite for the core runs without network or database under a time budget; no ORM entity in public use-case signatures.

## Sources
Cockburn, Hexagonal Architecture article [14]; Martin, Clean Architecture [3]; Evans and Vernon for domain modelling [4][5]; Fowler, BranchByAbstraction [20].

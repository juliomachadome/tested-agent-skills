# API Design (HTTP/REST, gRPC, GraphQL, Webhooks)

## 1. Resource modeling

- Nouns for resources, plural: `/customers/{id}/orders`. Avoid deep nesting (> 2 levels); use filters instead.
- Actions that don't map to CRUD: sub-resource or verb endpoint (`POST /orders/{id}/cancel`) — be explicit rather than overloading PATCH.
- Consistent naming (camelCase JSON in .NET/JS ecosystems), consistent date format (ISO 8601 with offset/UTC `Z`), ids as strings in JSON if they can exceed 2^53 (JS number precision).
- Money as `{ "amount": "12.30", "currency": "EUR" }` — string or integer minor units, never float.

## 2. Methods & semantics

| Method | Safe | Idempotent | Use |
|---|---|---|---|
| GET | yes | yes | read; never changes state |
| POST | no | no (make it so with Idempotency-Key) | create, actions |
| PUT | no | yes | full replace |
| PATCH | no | not necessarily | partial update (JSON Merge Patch / JSON Patch) |
| DELETE | no | yes | delete (repeat → 204 or 404, document which) |

## 3. Status codes

- **200** OK, **201** Created (+ `Location`), **202** Accepted (async processing; return status URL), **204** No Content.
- **400** malformed/validation, **401** not authenticated, **403** authenticated but not allowed, **404** not found (also use for "exists but you can't see it" to avoid leaking existence), **405**, **409** conflict (state/concurrency/duplicate), **412** precondition failed (ETag mismatch), **415**, **422** semantically invalid, **429** rate limited (+ `Retry-After`).
- **500** unexpected, **502/503/504** upstream/unavailable/timeout (+ `Retry-After` for 503).
- Never return 200 with `{ "success": false }`.

## 4. Errors — Problem Details (RFC 9457, obsoletes RFC 7807)

```json
{
  "type": "https://api.example.com/errors/insufficient-funds",
  "title": "Insufficient funds",
  "status": 422,
  "detail": "Balance 10.00 EUR is lower than 25.00 EUR.",
  "instance": "/transfers/abc",
  "traceId": "00-...",
  "errors": { "amount": ["Must be greater than zero."] }
}
```

- ASP.NET Core: `builder.Services.AddProblemDetails()`, `app.UseExceptionHandler()`, `IExceptionHandler`, `TypedResults.Problem/ValidationProblem`.
- Stable machine-readable `type`/code; human `title`/`detail`; include trace id; never stack traces in production.

## 5. Pagination, filtering, sorting

- Cursor (keyset) pagination for large/changing collections: `?limit=50&cursor=eyJ...` → response `{ items, nextCursor }`. Offset only for small, stable sets or when page jumps are required.
- Enforce max `limit`. Sorting by allow-listed fields only. Filtering with explicit params (`?status=active&createdFrom=...`).
- Consider total counts carefully — `COUNT(*)` on large tables is expensive; make it optional.

## 6. Idempotency & concurrency

- `Idempotency-Key` header for POSTs with side effects (see distributed-systems.md).
- **Optimistic concurrency over HTTP:** return `ETag` (row version); clients send `If-Match`; mismatch → 412.
- Conditional GET: `If-None-Match` → 304 saves bandwidth.

## 7. Versioning & evolution

- Prefer **additive, backward-compatible changes**: add optional fields, new endpoints; never change meaning/type of existing fields or remove them without a deprecation period.
- Clients must ignore unknown fields (tolerant reader).
- Version when breaking: URL (`/v2/`) is simplest and most visible; header/media type versioning is also valid. `Asp.Versioning` library in .NET.
- Deprecation: `Deprecation` and `Sunset` headers, changelog, usage monitoring before removal.
- Hyrum's law: undocumented behavior (ordering, error text) becomes depended upon — document what is guaranteed.

## 8. Contracts & documentation

- OpenAPI spec generated from code (`Microsoft.AspNetCore.OpenApi` in .NET 9+, Swashbuckle/NSwag) or design-first; publish it; generate typed clients (NSwag, Kiota, openapi-typescript, orval).
- Examples for every endpoint; document auth, rate limits, errors, pagination.
- Contract tests between services/consumers (Pact) for independently deployed parties.

## 9. Performance & limits

- Compression, caching headers, ETags, field selection (`?fields=`) for heavy resources, batch endpoints to avoid N calls.
- Request size limits, timeouts, rate limits per client.
- Long-running operations: `202 Accepted` + `Location: /operations/{id}`; client polls or receives webhook.

## 10. Security

- AuthN on all non-public endpoints; resource-level authZ; don't expose internal ids/fields unintentionally (DTOs, not entities).
- Validate everything (type, size, enums, ranges); reject unknown properties for sensitive endpoints.
- No secrets or PII in URLs.

## 11. Webhooks (sending and receiving)

**Sending:**
- Sign payloads: `HMAC-SHA256(secret, timestamp + "." + body)` in a header with the timestamp; receivers reject old timestamps (replay, e.g. > 5 min).
- At-least-once delivery with retries (exponential backoff over hours), unique event id, event type, created timestamp; endpoint for re-delivery; let customers rotate secrets.
- Keep payloads small or "thin" (id + type) and let receivers fetch current state.

**Receiving (e.g. Stripe, payment providers):**
- Verify signature with the raw body and constant-time compare; reject unsigned.
- **Respond 2xx fast**, enqueue processing; process idempotently by event id; handle out-of-order delivery (check current state/version rather than trusting arrival order).

## 12. gRPC vs REST vs GraphQL

| | REST/JSON | gRPC | GraphQL |
|---|---|---|---|
| Best for | public APIs, broad clients, caching | internal service-to-service, streaming, strict contracts, performance | client-driven data needs across many entities (mobile/web with varying screens) |
| Watch | over/under-fetching | browser support (gRPC-Web), debugging | N+1 (use DataLoader), query cost limits/depth limits, caching, authorization per field |

## 13. Real-time

- Polling (simple), long polling, **Server-Sent Events** (server → client, over HTTP, auto-reconnect), **WebSockets/SignalR** (bidirectional). Scale-out needs a backplane (Azure SignalR Service, Redis).

## 14. Domain error vs HTTP status vs problem details (RFC 9457)

Three separate layers; mixing them is the usual source of leaks and of use cases that "know HTTP".

1. **Domain error:** the use case throws or returns a typed error of its own (a class or a stable code such as `insufficient_funds`, `not_owned`, `locked`). It has no HTTP in it, so a worker, a CLI and a test can call the same use case. `domain/` and `application/` never import from the HTTP layer.
2. **HTTP status:** only the boundary decides. Typical mapping: rule violated or wrong source state = 409 or 422 with its own `type`; absent or belonging to another tenant = 404 (not 403, so existence is not revealed); not allowed = 403; not authenticated = 401; usage limit = 429 + `Retry-After`; retryable provider failure = 503; anything unexpected = generic 500.
3. **Problem details body** (`application/problem+json`): the wire format.

Members (RFC 9457 section 3.1; read 2026-11-15):

| Member | Meaning | Rule |
|---|---|---|
| `type` | URI reference identifying the problem type | the primary identifier; clients branch on it; defaults to `about:blank` (no semantics beyond the status) |
| `title` | short summary of the problem type | stable across occurrences (except localization) |
| `status` | HTTP status generated by the origin server | advisory, must equal the real response status |
| `detail` | explanation specific to this occurrence | should help the client correct the problem, not debug the server; clients must not parse it |
| `instance` | URI reference identifying this occurrence | useful as a correlation handle |
| extensions | your own members (`code`, `errors`, `traceId`) | clients must ignore extensions they do not know |

- RFC 9457 obsoletes RFC 7807. Section 5 encourages generators not to expose stack dumps or other implementation details.
- **Never leak** internal ids, table or constraint names, SQL, file paths or stack traces in `detail` or extensions. Driver messages often carry table names, constraints or emails: log the error class and origin (file:line), not the message, and return a fixed message.
- Give the client a **stable short code** (extension member or the last segment of `type`) and let the front end translate it; do not ship user-facing text from the server unless the product localizes there.
- Register one global exception filter/handler that converts any error into this shape; unknown errors become a generic 500 with only a correlation id. In NestJS, `HttpException` accepts an object that replaces the whole body, and `cause` is for logging and is never serialized.
- Once a streaming response has started the status cannot change: send an error event instead (see distributed-systems.md section 18).
- Validation errors: 422 (or 400) with an `errors` extension keyed by field, never echoing the rejected raw input.

## 15. Input validation and route pipeline

- **Validate on the server, by allow-list, for syntax and semantics, early, with size limits.** Cap body size and nesting before parsing; cap string length, array length and depth; run regexes only on bounded input and avoid catastrophic backtracking (ReDoS). Validation does not prevent injection: SQL still needs parameters. Source: OWASP Input Validation Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html (not re-verified).
- **One schema is the source of truth:** derive the static type from the schema (for example `z.infer`) instead of writing the type twice. Prefer the non-throwing parse that returns a discriminated result at boundaries; use the async variant when a refinement or transform is async. Share the schemas between front end and API in one package and validate at both edges.
- **Middleware order for a protected route:** body-size limit, request id and logging, authentication, rate limit, access guard, validation, use case. Authorize before validating parameters so the validation messages do not leak the input shape to someone with no access (OWASP API Security Top 10, not re-verified).
- **A thin route validates, calls one use case and maps the error;** business rules never live in the handler.
- **Single client = additive changes only:** when the only consumer is your own front end, you can skip API versioning and ship contract and client in the same deploy, as long as changes are additive.
- **Stable short error codes** (`locked`, `not_owned`) with a coherent status and no internal message; the front end translates the code.
- **Aggregation endpoint for a hot screen** (one call returning what the first view needs) beats N calls that each repeat authentication; a check repeated on every call (session, entitlement) can become one query or a seconds-long in-process cache, with the staleness written down and accepted.
- **Keep writes off read routes:** counters and "last seen" stamps are accumulated and flushed in batches (load shedding and back pressure, Nygard).
- **Logs:** one structured line per request (method, route pattern not the URL, status, duration, request id; no email, IP or query string) and one per business event; log what and who, never content; sanitize CR/LF; 5xx logs carry error class and origin, not the message. Source: OWASP Logging Cheat Sheet (not re-verified).

## Sources

- RFC 9457, Problem Details for HTTP APIs: https://www.rfc-editor.org/rfc/rfc9457.html (read 2026-11-15)
- NestJS, Exception filters: https://docs.nestjs.com/exception-filters (not re-verified)
- OWASP Logging Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html (not re-verified)
- IETF Idempotency-Key draft: https://datatracker.ietf.org/doc/draft-ietf-httpapi-idempotency-key-header/ (read 2026-11-15)

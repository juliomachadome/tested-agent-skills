# Access control, multi-tenancy and Postgres/Supabase

Format: **rule** · why · source id (see `sources.md`) · example.

## 1. Authorization model

1. **Deny by default; enforce centrally; check every request.** Checking "most" requests is not enough: one forgotten route exposes a resource. Use one guard/middleware/policy layer and test that access is denied by default. · W12, W1 A01 · e.g. a route list test fails when a new route has no guard entry.
2. **Three levels, three checks.** Object (BOLA, API1): can this caller touch this row? Property (BOPLA, API3): can they read or write this field? Function (BFLA, API5): can they call this operation at all? · W2, W3 V8 (8.2.1 to 8.2.3) · e.g. a user may update their profile but not the `role` field in the same payload (mass assignment).
3. **Unguessable ids are not authorization.** A UUID only slows enumeration. · W12 · e.g. a shared-link id still needs an expiry and a scope.
4. **A foreign id returns the same response as a missing one** (404, same body, similar time), so existence does not leak across users or tenants. · W3 V8 · e.g. tenant A asking for tenant B's invoice gets 404, not 403.
5. **Role and tenant come from the verified identity or the database, never from the request body, query, or user-editable metadata.** In Supabase `user_metadata` is user-editable; `app_metadata` is not. A JWT can be stale: role removal takes effect after refresh unless you check the database. · W29 · e.g. `tenant_id` in a POST body is ignored and re-derived from the session.
6. **Act with the end user's permission, not the intermediary's.** A backend, worker or AI agent acting for a user must carry that user's identity into the authorization decision. · W3 V8 (8.3.3) · e.g. an assistant that searches documents filters by the asking user's tenant, not the service account's.
7. **Server actions and direct POSTs need their own check.** A page-level or proxy/middleware check does not extend to them; they are reachable by direct POST. Values captured in a closure are sent to the client encrypted; do not rely on that to hide data, and pass to client components only what the screen shows. · W45
8. **Admin:** MFA always, re-authentication before sensitive actions (refund, export, email change), short sessions, every privileged action logged; when admins read the database directly, require `aal2` with a restrictive policy. · W5, W29

## 2. Multi-tenant isolation

1. **Explicit tenant filter in every repository query, even with RLS on.** RLS is the second wall: owners and `BYPASSRLS` roles skip it, and a filter-less query under a missing tenant setting silently returns nothing (looks fine in a test, fails in production). · W25
2. **Tenant setting only with `SET LOCAL` / `set_config(name, value, true)` inside a transaction.** `SET` (session) persists after commit; outside a transaction `SET LOCAL` only warns and does nothing. Behind a transaction-mode pooler the next request may get your session. · W26, W32 · e.g. a helper `withTenant(id, fn)` opens a transaction, sets the value locally, runs `fn`.
3. **Read the setting with the missing-ok form and treat empty as absent.** `current_setting(name, true)` returns NULL when unset; wrap as `NULLIF(current_setting('app.tenant_id', true), '')` and deny on NULL. · W26
4. **No external I/O inside the tenant transaction.** A model call or HTTP fetch inside it holds a pooled connection and can exceed the transaction timeout. Fetch first, then open the transaction. · W32 (pool behavior); engineering judgment.
5. **Unique keys include the tenant.** FK, unique and primary-key checks ignore RLS, so a global unique on a client-chosen value (slug, email, number) reveals existence in another tenant through the duplicate-key error. · W25 ("covert channel")
6. **Caches, search indexes, vector stores and object keys are partitioned by tenant too.** A cache key or embedding row without the tenant is a cross-tenant leak path. · W3 V8 (8.4.1)
7. **Prove isolation with presence and absence.** The test inserts a row for A and B, then as A sees A's row and not B's, and as A cannot write into B. "Empty result" alone proves nothing. · W29 (test pattern)

## 3. Postgres row-level security

1. **Enable RLS on every table in an exposed schema; with RLS on and no policy, everything is denied.** If the app connects as the table owner, add `FORCE ROW LEVEL SECURITY`. `TRUNCATE` and `REFERENCES` are not subject to RLS. · W25
2. **`USING` filters existing rows; `WITH CHECK` validates new or updated rows; without `WITH CHECK`, `USING` is used for both.** Permissive policies combine with OR, restrictive with AND. Always review the sum of policies, not only the new one: an extra permissive policy is the most common way to open a table by accident. · W25 · e.g. `WITH CHECK (tenant_id = current_tenant())` blocks moving a row to another tenant.
3. **Keep policies on the row itself.** A policy that queries another table or calls a function can race and leak; expressions run before user filters except `leakproof` functions. · W25
4. **Explicit `TO` on every policy.** `TO anon USING (true)` is public read: only for public data. · W29
5. **`auth.uid()` is NULL without a user, and `NULL = user_id` is silently false.** Write `TO authenticated` or `auth.uid() IS NOT NULL AND auth.uid() = user_id`. Anonymous sign-ins also use the `authenticated` role; distinguish with the `is_anonymous` claim. · W29
6. **Performance is part of correctness.** Index the policy column; wrap functions as `(select auth.uid())` so they are evaluated once per statement; add the same filter in the query; use `TO authenticated`. The vendor measured 170+ ms dropping to under 1 ms or ~9 ms with these. · W37
7. **Views bypass RLS by default.** Use `WITH (security_invoker = true)` (Postgres 15+) or keep the view out of the exposed schema. · W29
8. **Test RLS as the real role.** In pgTAP: denied write `throws_ok(..., '42501')`; filtered read `is_empty(...)` plus a check that the target row is intact; allowed write with `RETURNING` (a `lives_ok` passes with zero rows). · W29

```sql
alter table public.orders enable row level security;
revoke all on public.orders from anon, authenticated;
grant select on public.orders to authenticated;
create policy orders_select_own on public.orders
  for select to authenticated
  using ((select auth.uid()) = user_id);
create index if not exists orders_user_id_idx on public.orders (user_id);
```

## 4. Grants and functions

1. **Grant decides whether a role reaches the object; RLS decides the row.** Use both. A missing grant fails with `42501` before any policy. Creating a policy does not remove a grant. · W31, W29
2. **Defaults are wide.** In many existing projects a new table in `public` gets all privileges for the API roles and a new function is executable by `PUBLIC`. Revoke at the end of each migration or change default privileges. Internal tables (queues, logs, limits) go to a non-exposed schema. · W31
3. **If the browser never talks to the database API, the ideal grant surface for public roles is zero**; disable the data API entirely if nothing uses it. · W31
4. **`SECURITY DEFINER` safely:** pin `search_path` (empty, or trusted schemas with `pg_temp` last), schema-qualify every name, `REVOKE EXECUTE ... FROM PUBLIC` and grant to the one role **in the same transaction** as `CREATE`, never in an exposed schema, and check the caller inside the function (it runs with the creator's rights, which usually bypass RLS). · W27, W29

```sql
begin;
create or replace function private.revoke_access(p_order uuid)
returns void language plpgsql security definer set search_path = ''
as $$ begin
  update public.entitlements set revoked_at = now() where order_id = p_order;
end $$;
revoke all on function private.revoke_access(uuid) from public, anon, authenticated;
grant execute on function private.revoke_access(uuid) to service_role;
commit;
```

## 5. Supabase keys and advisors

1. **Publishable key (low privilege) is public by design; secret key (`service_role`) bypasses RLS and lives only on the server.** Legacy JWT `anon`/`service_role` keys are being retired; creating new keys does not revoke old ones, disabling them is a separate step. · W30
2. **One secret key per backend component** (API, worker, import CLI), so one leak rotates one key. Never log a key; to identify one, use at most a few characters of its random part or a hash. · W30
3. **The secret key bypasses RLS only when the request carries no user token;** with a user token, that user's policies apply. · W29
4. **On the server, decide access with a verified token** (`getClaims()` verifies the JWT signature, `getUser()` asks the auth server), never with `getSession()`, which only reads the cookie. · W36
5. **Run the security advisors after every migration** and treat these as errors: auth users exposed, security-definer view, RLS disabled in public, policy referencing user metadata, queue exposed in API, sensitive columns exposed. Warnings to fix or justify: per-row `auth.*` re-evaluation, multiple permissive policies, mutable function `search_path`, permissive policy, public bucket allowing listing, security-definer function executable by public roles. "RLS enabled, no policy" is often intentional (backend-only table). · W33

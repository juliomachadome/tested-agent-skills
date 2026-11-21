# Supabase (managed Postgres) operations

Format: **rule** · why · source `[n]` (see `BIBLIOGRAPHY.md`) · example. Numbers checked 15/11/2026 (page text read the same day).

## Connections

1. **Pick the connection by workload** `[30]`: direct (port 5432, `db.<ref>.supabase.co`) for persistent servers, migrations, `pg_dump` and restores, IPv6 on Free and Pro, IPv4 with the paid add-on (which replaces the IPv6 record); shared pooler session mode (5432) for IPv4-only persistent clients; shared pooler transaction mode (6543, user `postgres.<ref>`) for serverless and edge; a dedicated pooler (port 6543 on the db host) on Pro and above for high load.
2. **Transaction mode loses session state:** no session `SET`, no `LISTEN/NOTIFY`, no cursors beyond the transaction, no pipelining; prepared statements are unsupported on the shared pooler (driver flags: `prepare: false` for Postgres.js and Drizzle, `pgbouncer=true` for Prisma, `statement_cache_size=0` for asyncpg, `prepareThreshold=0` for JDBC) `[30]`. The dedicated pooler supports them on PgBouncer 1.21+.
3. **Per-request tenant or role context uses `SET LOCAL` inside a transaction** (a session `SET` leaks to the next client of the pooled connection); "one at a time per tenant" locks use `pg_advisory_xact_lock`.
4. **Serverless: one client per module and `max: 1` per instance.** Postgres.js defaults to 10 connections per client and each warm instance has its own pool, so the total multiplies (arithmetic in `diagnosis-playbook.md` section 7) `[30]`.
5. **Connection ceilings by compute** `[32]`: Micro 60 direct / 200 pooler clients; Small 90 / 400; Medium 120 / 600; Large 160 / 800. Pooler pool size must stay under 40% of max connections when the REST API is heavily used and under 80% otherwise, and applies per database role `[31]`.
6. **Statement timeouts** `[35]`: `anon` 3 s, `authenticated` 8 s, `service_role` falls back to the authenticator's 8 s, `postgres` is capped by the 2-minute global default. The HTTP client needs its own timeout.

## Backups and restore

7. **Daily backups:** Pro 7 days, Team 14, Enterprise up to 30; Free has no automatic backups, export with `supabase db dump` `[29]`.
8. **PITR is an add-on;** worst-case RPO 2 minutes (WAL archived about every 2 minutes, not while idle); enabling it stops daily backups; listed about USD 100/month for 7 days, USD 200 for 14, USD 400 for 28 `[29]`. Docs advise PITR above 4 GB or when a lower RPO is needed `[34]`.
9. **Not in the backup:** Storage objects (metadata only) and custom role passwords `[29]`. Deleting a project deletes its backups.
10. **The project is unavailable during a restore, longer for bigger databases;** subscriptions and replication slots must be dropped first and recreated. A PITR restore replaces the current state: to keep current data restore into a new project first `[29]`. Rehearse with production-sized data and record the time (`playbooks.md` section 5).
11. **Without a paid plan** schedule your own `pg_dump`, store it outside the provider, and prove it with a restore check.
12. **Free projects pause after about 7 days of low activity and cannot download backups** `[34]`; no free plan where there is customer data.

## Migrations and production

13. **Versioned files in `supabase/migrations/`, applied by the CLI;** applied versions live in `supabase_migrations.schema_migrations`. Dashboard edits on the remote database cause drift and break `db push`; capture with `db pull`. `migration repair` edits only the history table, it runs no SQL `[33]`.
14. **Production checklist** `[34]`: own SMTP (the built-in sender is rate limited), CAPTCHA on sign-up, sign-in and reset, RLS on exposed tables (details in `software-security`), PITR when the database is large or the RPO must be low.
15. **`pg_cron`** `[36]`: up to 8 concurrent jobs, each under 10 minutes, interval from 1 second to once a year; history in `cron.job_run_details`; good for cleanup, not for application logic.
16. **Regions include São Paulo and the EU** `[53]` (not re-read this pass): choose with the data-protection owner and keep compute close (a cross-ocean API adds about 100 ms per query). Changing region after creation is not documented on the pages read: plan a migration.

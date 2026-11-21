# Images, CI/CD and minimal observability

Format: **rule** · why · source `[n]` (see `BIBLIOGRAPHY.md`). Checked 15/11/2026. Secret rotation and the cost table now live in `playbooks.md` (sections 3 and 7); the file name is kept so old links still resolve.

## 1. Container images
1. **Pin the base image by digest; multi-stage builds; non-root `USER` with an explicit UID/GID; keep a `.dockerignore`.** Tags can be repointed; a digest pin means you update by hand or with an update bot, which is the trade-off to accept `[47]`.
2. **Never put secrets in `ENV` or `ARG`:** values persist in the layer even if unset later and can be dumped from the image `[47]`. Use build secret mounts or runtime variables `[12]`.
3. **Rebuild with `--pull` periodically** to get base fixes (it does not re-run steps; `--no-cache` does) `[47]`; no `latest` in production.

## 2. CI/CD
1. **What passed CI is what ships:** build once, promote the same artifact; do not rebuild per environment `[1]` `[4]`.
2. **Harden workflows** `[48]`: `GITHUB_TOKEN` read-only by default and widened per job; third-party actions pinned to a full commit SHA from the original repository; avoid `pull_request_target` and never check out untrusted pull request code under it; OIDC short-lived cloud credentials instead of stored keys; one secret per value (not a JSON blob) so redaction works; environments with required reviewers gate environment secrets; a secret seen in a log means delete the log and rotate.
3. **Cancel superseded runs** with `concurrency` and `cancel-in-progress: true`; without it a running job continues and only pending ones are replaced `[49]`. Group names are case insensitive.
4. **Caches** `[50]`: immutable (new key per change); entries not accessed for 7 days are removed; default 10 GB per repository, oldest evicted first; branch scoping applies (a run sees its own branch and the default branch; pull request caches are scoped to the merge ref); no secrets in caches. Scheduled-workflow limits (default branch only, delays, disabled after 60 days of inactivity in public repositories) come from an earlier pass and were not re-read `[54]`.
5. **A required check skipped by `paths` stays Pending and blocks the merge;** use one aggregating gate job (earlier pass, not re-read `[54]`).

## 3. Minimal observability for one owner
1. **Alert on symptoms users feel** (site down, main flow failing, queue stuck, webhooks failing, paid but no access); use causes (a refused database connection) for diagnosis, not paging `[2]`. Frame with the four golden signals: latency (successes and failures separately), traffic, errors (including wrong content with a 200), saturation `[2]`. Few alerts that reach a phone.
2. **Shallow health for the deploy, deep health for monitors:** `/health` fixed and fast for the platform; a protected deep check (queue age, stuck jobs, failures in 24 h, `select 1`) called by an external monitor, because platform healthchecks often stop after the deploy `[14]`.
3. **Logs as an event stream** `[1]`: one JSON line per request (method, route pattern, status, duration, request id) and one per business event; no emails, IPs, query strings or content (log hygiene: `software-security`). Release reports that list the commits in each release speed up diagnosis `[2]`.
4. **A sleeping service is not an outage:** alert on failed wakes, not on scale-to-zero `[18]`.
5. **Postmortem triggers decided in advance** (user-visible degradation, data loss, any manual rollback); blameless and systemic; template in `playbooks.md` section 8 `[2]`.

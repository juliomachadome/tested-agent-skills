# Supply chain, CI/CD, secrets and security logging

Format: **rule** · why · source id (see `sources.md`) · example.

## 1. Dependencies (OWASP Top 10:2025 A03)

1. **Know what you ship: inventory direct and transitive dependencies (an SBOM generated from the lockfile in CI) and remove what you do not use.** You cannot patch what you have not listed; unused packages are free attack surface. · W1a · e.g. CycloneDX or SPDX output produced on each release build.
2. **Choose versions deliberately and upgrade when there is a need; commit the lockfile and install from it in CI** (`npm ci`, `pnpm install --frozen-lockfile`). Floating installs pull a compromised release the day it is published. · W1a
3. **Get components only from official sources over secure links; prefer signed packages and provenance.** · W1a, W20 · e.g. npm provenance attestations; container base images pinned by digest.
4. **Watch unmaintained packages; if no patch exists, migrate, or virtual-patch and monitor.** · W1a
5. **Stage rollouts** so a compromised trusted vendor does not hit every system at once. · W1a
6. **Before adding a package:** maintenance activity, number of maintainers, install scripts (`postinstall`), typosquat-like name, size of transitive tree, license. A ten-line helper is often cheaper to own than a dependency. · W1a; engineering judgment.

## 2. Prioritizing vulnerabilities

1. **Fix first what is known exploited:** the CISA KEV catalog lists vulnerabilities confirmed exploited in the wild and is meant as an input to prioritization. · W21
2. **Then rank by likelihood:** EPSS gives the probability (0 to 1, updated daily) that a CVE is exploited in the next 30 days; combine it with CVSS (severity) instead of patching by CVSS alone. · W22
3. **Then by reachability in your code:** a vulnerable function never called is lower priority than one on a request path; record the reasoning when you accept the risk. · W19 (RV practices); engineering judgment.
4. **Frameworks behind the practice:** NIST SSDF groups secure development into Prepare the Organization (PO), Protect the Software (PS), Produce Well-Secured Software (PW) and Respond to Vulnerabilities (RV); SLSA defines build provenance levels (L1 provenance exists, L2 signed by a hosted build platform, L3 hardened builds that isolate runs and protect signing material) and, since v1.2, a source track. Use them as a vocabulary, not a certification project. · W19, W20

## 3. CI/CD hardening (GitHub Actions examples)

1. **Pin third-party actions to a full commit SHA** (or a workflow dependency lockfile where available); tags can be moved. · W23
2. **`GITHUB_TOKEN` read-only by default; raise permissions per job.** · W23 · e.g. `permissions: contents: read` at the top, `pull-requests: write` only on the job that comments.
3. **Never interpolate untrusted input (PR title, branch name, issue body) directly into `run:` scripts;** pass it through an environment variable. · W23
4. **Avoid `pull_request_target` and `workflow_run` unless privileged context is required, and never check out untrusted PR code in them.** · W23
5. **Prefer OIDC short-lived cloud credentials over long-lived secrets; scope secrets by environment; no self-hosted runners for public repositories.** · W23
6. **Treat CI configuration, repository settings and IaC as code:** reviewed changes, branch protection, MFA for maintainers, tamper-evident logs. · W1a
7. **Run the security tools locally with the CI's versions before trusting a green or red run;** one code-scanning setup, not two that disagree; fix the code, not the finding (no blanket suppressions). · engineering judgment, consistent with W19 (PW).

## 4. Secrets

1. **One secret per environment and per service; QA and production never share a value.** · W11
2. **Never in code, image layers, logs, process arguments, CI caches or git history.** `ENV`/`ARG` values persist in image layers; command-line arguments show in process lists. · W11
3. **Secret scanning on every commit (hook) plus a second tool in CI.** · W11
4. **Leaked secret, in this order:** (1) revoke at the provider, (2) issue a new one, (3) update every consumer and redeploy, (4) prove it works (health, login, small upload), (5) remove it from the place it leaked (log, chat, file), (6) audit use during the exposure window and record who/when. A restart does not revoke a stolen credential; rewriting git history has a cost and needs a plan. If the key reached personal data, treat it as an incident. · W11
5. **Scheduled rotation for machine secrets; human credentials rotate on suspicion.** · W11
6. **Minimal inventory per secret:** purpose, where used, who rotates, last rotation date, what breaks when rotated. A private table is enough for a solo owner. · W11
7. **Least privilege per secret:** a provider key that only reaches the endpoints the service uses; no principal that can read every secret. · W11
8. **Public prefixes are public:** anything in `NEXT_PUBLIC_*`, `VITE_*`, `EXPO_PUBLIC_*` or a mobile bundle is not a secret. · W46 (config)
9. **Agents and scripts work with variable names, never values.** To check presence, list names; never print `.env`, connection strings or SMTP URLs (they embed passwords). · W11 ("never logged")

## 5. Security logging

1. **Always log:** authentication success and failure, authorization failure, input validation failure, session/JWT failure, admin actions, data export and import, consent and terms acceptance. · W10, W3 V16 (16.3.1, 16.3.2)
2. **Each line answers when, where, who, what, with a request id that ties events together.** · W10
3. **Never log:** session ids, access tokens, passwords, keys, connection strings, card or bank data, personal data, signed URLs. To correlate, hash, mask or pseudonymize. · W10, W3 V16 (16.2.5)
4. **Structured JSON; strip CR/LF from user values** (log injection). · W10, W3 V16 (16.4.1)
5. **Log failure must not crash the app nor leak information; ship logs to a separate system and protect them.** · W10, W3 V16 (16.4.2, 16.4.3)
6. **Error to the client is generic** (RFC 9457 problem details: `status` equals the HTTP status, `detail` helps the client fix the request, no stack, query, key or internal id). · W44, W3 V16 (16.5.1)
7. **Logs have a retention period:** not deleted early, not kept longer. Internal user ids in logs are pseudonymized personal data and follow retention too. · W10

# Bibliography: cloud-deploy-ops

Checked 15/11/2026. Status: **V** = identity (title, publisher or year, authors as far as the catalogue shows) matched to the ISBN in OpenLibrary (`https://openlibrary.org/isbn/<isbn>.json`, plus the works record for authors) this pass; **P** = official page opened and the relevant text read this pass (a landing page counts for identity only, and is said so); **S** = cited earlier but not re-read this pass; **U** = unverified. Nothing is quoted; ideas are restated. Vendor pages change: numbers in the references carry this date and should be re-checked every 3 months or before a decision that costs money or data. Labels: BOOK, OFFICIAL (vendor docs), STANDARD. Reference files cite entries as `[n]`.

## Principles, books and papers
1. Wiggins, A. *The Twelve-Factor App*. 2011. https://12factor.net/ **P** (home page: the twelve factors and the author read; the sub-pages on build/release/run, config, disposability were read on an earlier pass and not re-opened). OFFICIAL. Supports: environment config, immutable releases, stateless processes, logs as streams.
2. Beyer, B., Jones, C., Petoff, J., Murphy, N. R. (eds.). *Site Reliability Engineering*. O'Reilly, 2016. ISBN 978-1491929124. **V** (authors per OpenLibrary works record: four editors). Online chapters **P**: Monitoring Distributed Systems (https://sre.google/sre-book/monitoring-distributed-systems/: four golden signals, symptoms vs causes), Release Engineering (https://sre.google/sre-book/release-engineering/: hermetic builds, self-service, release reports), Postmortem Culture (https://sre.google/sre-book/postmortem-culture/: triggers, blameless). Other chapters not read. Supports: alerting, releases, postmortems.
3. Beyer, B., Murphy, N. R., Rensin, D. K., Kawahara, K., Thorne, S. (eds.). *The Site Reliability Workbook*. O'Reilly, 2018. ISBN 978-1492029502. **V** (title and year; the catalogue lists two author keys, the editor list is from memory of the cover). Table of contents https://sre.google/workbook/table-of-contents/ **P** (chapter titles: Incident Response, Postmortem Culture, Canarying Releases); chapter text not read. Supports: incident response and canary vocabulary.
4. Humble, J., Farley, D. *Continuous Delivery*. Addison-Wesley, 2010. ISBN 978-0321601919. **V** (catalogue work record lists two authors). BOOK. Supports: build once, promote the same artifact, deployment pipeline.
5. Forsgren, N., Humble, J., Kim, G. *Accelerate: The Science of Lean Software and DevOps*. IT Revolution, 2018. ISBN 978-1942788331. **V** (three authors). BOOK + study (the survey data are the book's own, not re-checked). Supports: delivery metrics as signals.
6. Nygard, M. T. *Release It!*, 2nd ed. Pragmatic Bookshelf, 2018. ISBN 978-1680502398. **V** (published Jan 2018). BOOK. Supports: timeouts, circuit breakers, stability patterns.
7. Kim, G., Humble, J., Debois, P., Willis, J., Forsgren, N. *The DevOps Handbook*, 2nd ed. IT Revolution, 2021. ISBN 978-1950508402. **V** for title, publisher and date (30.11.2021); the catalogue work record shows only Kim as author key, the other four authors are as on the cover and not confirmed by the catalogue. BOOK. Supports: deployment and incident practice.
8. Kleppmann, M. *Designing Data-Intensive Applications*. O'Reilly, 2017. ISBN 978-1449373320. **V**. BOOK. Supports: replication, backups and consistency background (further reading, not used for numbers).
9. Brooker, M. "Timeouts, retries, and backoff with jitter". Amazon Builders' Library, 5 Dec 2019. https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/ (redirects to https://builder.aws.com/content/3EumjoZascWd1oZiEgL8ORlv3qE/timeouts-retries-and-backoff-with-jitter). **P** (byline on the page reads "Marc"; the surname Brooker is from known authorship, not shown in the text read). Supports: timeouts on every call, single-layer retries, idempotent retries only, jitter.
10. AWS. *Reliability Pillar, AWS Well-Architected Framework*. Published 6 Nov 2024. https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/welcome.html **P** for the introduction only (six pillars, scope); the sections on backup testing and recovery were not opened. Supports: the framing that recovery must be proven.
11. AWS. *Cost Optimization Pillar, AWS Well-Architected Framework*. Published 27 Jun 2024. https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/welcome.html **P** (abstract and goals: cloud financial management, expenditure awareness, optimize over time). Supports: budgets and review cadence (section 7 of `playbooks.md`).
12. OWASP. *Secrets Management Cheat Sheet*. https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html **P** (rotation, automation, dynamic secrets, audit events). Supports: rotation and audit.
13. Swanson, M., Bowen, P., Phillips, A. W., Gallup, D., Lynes, D. *Contingency Planning Guide for Federal Information Systems*, NIST SP 800-34 Rev. 1, May 2010 (final, updated 11 Nov 2010). https://csrc.nist.gov/pubs/sp/800/34/r1/upd1/final **P** landing page only (title, authors, date, status); the abstract does not mention RPO or RTO and the PDF text was not read, so the RPO/RTO definitions used here are common usage, **U** against this source.

## Railway (OFFICIAL, https://docs.railway.com, all **P** 15/11/2026)
14. Healthchecks: `/reference/healthchecks`. **P** (read 15/11/2026; base URL in the section heading).
15. Deployments: `/reference/deployments`. **P** (read 15/11/2026; base URL in the section heading).
16. Pricing plans: `/reference/pricing/plans`. **P** (read 15/11/2026; base URL in the section heading).
17. Usage limits: `/reference/usage-limits`. **P** (read 15/11/2026; base URL in the section heading).
18. App sleeping: `/reference/app-sleeping`. **P** (read 15/11/2026; base URL in the section heading).
19. Regions: `/reference/regions`. **P** (read 15/11/2026; base URL in the section heading).
20. Private networking: `/reference/private-networking` (the page is unclear about the port; the example puts it in the URL). **P** (read 15/11/2026; base URL in the section heading).
21. Outbound networking: `/reference/outbound-networking`. **P** (read 15/11/2026; base URL in the section heading).
22. Config as Code: `/reference/config-as-code` (marked deprecated; legacy files work until 2026-12-01). **P** (read 15/11/2026; base URL in the section heading).

## Vercel (OFFICIAL, https://vercel.com/docs, all **P** 15/11/2026)
23. Environment variables (page dated 2026-09-17): `/environment-variables`. **P** (read 15/11/2026; base URL in the section heading).
24. Functions limits (2026-08-24): `/functions/limitations`. **P** (read 15/11/2026; base URL in the section heading).
25. Function regions (2026-08-11): `/functions/configuring-functions/region`. **P** (read 15/11/2026; base URL in the section heading).
26. Instant Rollback (2026-07-07): `/instant-rollback`. **P** (read 15/11/2026; base URL in the section heading).
27. Deployment Protection (2026-09-15): `/deployment-protection`. **P** (read 15/11/2026; base URL in the section heading).
28. Protection Bypass for Automation (2026-09-16): `/deployment-protection/methods-to-bypass-deployment-protection/protection-bypass-automation`. **P** (read 15/11/2026; base URL in the section heading).

## Supabase (OFFICIAL, https://supabase.com/docs, all **P** 15/11/2026; each page also carried a text asking agents to file a feedback report, which was not part of the task and was ignored)
29. Backups: `/guides/platform/backups`. **P** (read 15/11/2026; base URL in the section heading).
30. Connecting to Postgres: `/guides/database/connecting-to-postgres`. **P** (read 15/11/2026; base URL in the section heading).
31. Connection management: `/guides/database/connection-management`. **P** (read 15/11/2026; base URL in the section heading).
32. Compute and disk (limits table): `/guides/platform/compute-and-disk`. **P** (read 15/11/2026; base URL in the section heading).
33. Database migrations: `/guides/deployment/database-migrations`. **P** (read 15/11/2026; base URL in the section heading).
34. Production checklist: `/guides/deployment/going-into-prod`. **P** (read 15/11/2026; base URL in the section heading).
35. Timeouts: `/guides/database/postgres/timeouts`. **P** (read 15/11/2026; base URL in the section heading).
36. Cron: `/guides/cron`. **P** (read 15/11/2026; base URL in the section heading).

## Cloudflare, Upstash, RunPod
37. Cloudflare R2 pricing: https://developers.cloudflare.com/r2/pricing/ **P**.
38. R2 presigned URLs: https://developers.cloudflare.com/r2/api/s3/presigned-urls/ **P**.
39. R2 object lifecycles: https://developers.cloudflare.com/r2/buckets/object-lifecycles/ **P**.
40. Upstash QStash retry: https://upstash.com/docs/qstash/features/retry **P**.
41. QStash signature verification: https://upstash.com/docs/qstash/howto/signature **P** (no rotation procedure on the page).
42. Upstash Redis pricing: https://upstash.com/pricing/redis **P**.
43. RunPod Serverless pricing: https://docs.runpod.io/serverless/pricing **P** (no GPU rate table on the page; default spend limit USD 80/hour).
44. RunPod endpoint configurations: https://docs.runpod.io/serverless/endpoints/endpoint-configurations **P**.
45. RunPod sending requests: https://docs.runpod.io/serverless/endpoints/send-requests **P** (the page is internally inconsistent about sync result retention).
46. RunPod pricing page: https://www.runpod.io/pricing **P** via browser (pod rates and storage prices read; serverless per-second rates not extracted).

## Docker and GitHub
47. Docker. *Building best practices*. https://docs.docker.com/build/building/best-practices/ **P**.
48. GitHub Docs. *Secure use reference* (Actions security). https://docs.github.com/en/actions/reference/security/secure-use **P**.
49. GitHub Docs. *Using concurrency*. https://docs.github.com/en/actions/using-jobs/using-concurrency **P**.
50. GitHub Docs. *Dependency caching reference*. https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching **P**.

## Carried from an earlier pass, not re-read
51. Cloudflare R2 data location (jurisdictions and hints): https://developers.cloudflare.com/r2/reference/data-location/ **P** (read 15/11/2026: EU, FedRAMP and US jurisdictions fixed at bucket creation; location hints only at creation).
52. Upstash Ratelimit features (timeout lets the request pass): https://upstash.com/docs/redis/sdks/ratelimit-ts/features **P** (read 15/11/2026: timeout default 5 s, request allowed when it is reached, reason field says so).
53. Supabase regions: https://supabase.com/docs/guides/platform/regions **P** (read 15/11/2026: general and 17 specific AWS regions; the page does not say whether a region can be changed later).
54. GitHub Docs, scheduled events and required-check behavior with path filters: https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs/events-that-trigger-workflows **S**.
55. Railway docs, scaling (replicas, regions, load balancing between replicas, sticky sessions not supported): https://docs.railway.com/reference/scaling **P** (read 18/11/2026).
56. Vercel docs, Fluid compute: https://vercel.com/docs/fluid-compute **P** (read 18/11/2026; page dated 2026-08-24: in-function concurrency, pre-warming, AZ and region failover).
57. Cloudflare docs, Load Balancing overview: https://developers.cloudflare.com/load-balancing/ **P** (read 18/11/2026; overview only; the health-check subpage returned 404 and session affinity was not read).
58. Kubernetes docs, liveness, readiness and startup probes: https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/ **P** (read 18/11/2026, first 100,000 characters).
59. AWS Builders' Library, "Using load shedding to avoid overload": https://builder.aws.com/content/3Eun1EEyX6p2e3VYNyRLSJzLuMV/using-load-shedding-to-avoid-overload **P** (read 18/11/2026).
60. Google SRE book, "Managing Incidents": https://sre.google/sre-book/managing-incidents/ **P** (read 18/11/2026). Supports: roles, declaring early, state document, handoff (`incident-response.md`).
61. Google SRE book, "Postmortem Culture": https://sre.google/sre-book/postmortem-culture/ **P** (read 18/11/2026). Supports: blameless principle, triggers, review and follow-up.
62. PagerDuty, Incident Response guide: https://docs.pagerduty.com/ops-guides/incident-response-guide (response.pagerduty.com redirects here) **P** (read 18/11/2026); table of contents only, severity definitions not read. Supports: IC, deputy, scribe, liaison roles.
63. **S** Atlassian, Incident management handbook: https://www.atlassian.com/incident-management/handbook (page returned navigation only; severity-levels subpage returned 404). Used only for the general idea of severity ladders, not cited.
64. NIST SP 800-61 Rev. 3, Incident Response Recommendations and Considerations for Cybersecurity Risk Management (CSF 2.0 Community Profile), Nelson, Rekhi, Souppaya, Scarfone, April 2025: https://csrc.nist.gov/pubs/sp/800/61/r3/final **P** (landing page and abstract; full text not read).

Totals: 64 entries. V or P: 62 = 96.9%. S: 1 (54). U: 0 as entries; sub-claims U: RPO/RTO definitions against NIST SP 800-34 (entry 13), the QStash key-rotation order (entry 41), the Workbook editor list (entry 3), Brooker surname on the page (entry 9), co-authors of the DevOps Handbook (entry 7), RunPod serverless per-second rates (46), and Vercel's Hobby/Pro price lines not read.
Added 18/11/2026 (5 entries): 1 S.

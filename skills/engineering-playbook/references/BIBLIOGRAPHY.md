# Bibliography: engineering-playbook

Checked 16/11/2026. Status: **V** = identity (title, authors as far as the catalogue shows, year) matched to the ISBN in OpenLibrary (`https://openlibrary.org/isbn/<isbn>.json`) this pass; **P** = official or primary page opened this pass and the terms the skill relies on were found in the fetched text (pages were checked by script, so "terms found" is weaker than a full read; a note says so where it matters), or, for papers, identity (title, authors, venue, year) matched in the DOI record; **S** = page or book exists but the text used was not read (or the ISBN record is unusable); **U** = not verified. Nothing is quoted; ideas are restated. Labels: BOOK, STUDY (data behind a book), PAPER, OFFICIAL (standard, vendor or project documentation), PRACTITIONER. Years are first publication; where the catalogue shows a later printing the note says so. Entries cited as "not re-read" in the previous edition were all re-checked this pass.


## Specifications and official documentation

1. IETF (Nottingham, M., Wilde, E., Dalal, S.). *RFC 9457 Problem Details for HTTP APIs*. 2023. https://www.rfc-editor.org/rfc/rfc9457.html. **P**. OFFICIAL. Supports: error body members, no internals in errors (`api-design.md` 4, 14). Page opened; title, authors and the "obsoletes RFC 7807" header found.
2. IETF (Fielding, R., Nottingham, M., Reschke, J.). *RFC 9110 HTTP Semantics*. 2022. https://www.rfc-editor.org/rfc/rfc9110.html. **P**. OFFICIAL. Supports: methods, idempotent methods, status codes (`api-design.md` 2, 3). Page opened; title and "idempotent" text found; section-level claims not re-read.
3. IETF HTTPAPI WG. *The Idempotency-Key HTTP Header Field*. Internet-Draft. https://datatracker.ietf.org/doc/draft-ietf-httpapi-idempotency-key-header/. **P**. OFFICIAL (draft, not a standard). Supports: key semantics, 409/422 on reuse (`distributed-systems.md` 2). Current revision read as -08; drafts change, recheck before citing a version.
4. PostgreSQL Global Development Group. *SET*. https://www.postgresql.org/docs/current/sql-set.html. **P**. OFFICIAL. Supports: `SET LOCAL` transaction scope for the RLS tenant setting (`databases.md` 18).
5. PostgreSQL. *Client Connection Defaults (lock_timeout, statement_timeout)*. https://www.postgresql.org/docs/current/runtime-config-client.html. **P**. OFFICIAL. Supports: migration timeouts, advice not to set them in postgresql.conf (`databases.md` 12).
6. PostgreSQL. *CREATE INDEX*. https://www.postgresql.org/docs/current/sql-createindex.html. **P**. OFFICIAL. Supports: CONCURRENTLY, INVALID indexes (`databases.md` 12).
7. PostgreSQL. *SELECT (locking clause, SKIP LOCKED)*. https://www.postgresql.org/docs/current/sql-select.html. **P**. OFFICIAL. Supports: queue consumers (`distributed-systems.md` 14).
8. PostgreSQL. *ALTER TABLE*. https://www.postgresql.org/docs/current/sql-altertable.html. **P**. OFFICIAL. Supports: NOT VALID then VALIDATE CONSTRAINT, SET NOT NULL (`databases.md` 12; `playbooks.md` 2). Terms found; the exact lock levels and the "skips the scan" rule not re-read this pass.
9. PostgreSQL. *Row Security Policies* and *CREATE POLICY*. https://www.postgresql.org/docs/current/ddl-rowsecurity.html and https://www.postgresql.org/docs/current/sql-createpolicy.html. **P**. OFFICIAL. Supports: RLS (`databases.md` 18; `saas-multitenancy.md` 9). Both pages opened; terms found.
10. PostgreSQL. *Range Types* (exclusion constraints). https://www.postgresql.org/docs/current/rangetypes.html. **P**. OFFICIAL. Supports: temporal exclusion (`databases.md` 14). Terms found only.
11. PostgreSQL. *Transaction Isolation*. https://www.postgresql.org/docs/current/transaction-iso.html. **P**. OFFICIAL. Supports: serialization failures and retry on 40001 (`databases.md` 5). Terms found only.
12. PostgreSQL. *INSERT* (ON CONFLICT). https://www.postgresql.org/docs/current/sql-insert.html. **P**. OFFICIAL. Supports: upsert and insert-or-ignore (`databases.md` 15). Terms found only.
13. PostgreSQL. *Explicit Locking*. https://www.postgresql.org/docs/current/explicit-locking.html. **P**. OFFICIAL. Supports: lock modes, deadlocks (`diagnosis-playbook.md` 7). Terms found only.
14. Prisma. *PgBouncer / connection pooling*. https://www.prisma.io/docs/orm/prisma-client/setup-and-configuration/databases-connections/pgbouncer. **P**. OFFICIAL. Supports: pooler, `pgbouncer=true`, Migrate needs a direct connection (`databases.md` 17). Read: Migrate does not support PgBouncer; current docs configure the direct connection in `prisma.config.ts` (the `directUrl` setting of older versions was not on the page).
15. Brown, S. *The C4 model*. https://c4model.com/. **P**. OFFICIAL (author site). Supports: four diagram levels (`architecture-design.md`).
16. Cockburn, A. *Hexagonal Architecture*. 2005. https://alistair.cockburn.us/hexagonal-architecture. **P**. OFFICIAL (author site). Supports: ports and adapters (`architecture-design.md`). Page opened; terms found.
17. NestJS. *Custom providers* (and the Modules, Exception filters, Lifecycle events and SSE pages). https://docs.nestjs.com/fundamentals/custom-providers. **P**. OFFICIAL. Supports: injection tokens (`architecture-design.md`). Only the custom-providers page was opened; the other pages are **S**.
18. Nygard, M. *Documenting Architecture Decisions*. 2011. https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions. **P**. PRACTITIONER. Supports: ADR format (`architecture-design.md`). Terms found.
19. Amazon Builders' Library. *Timeouts, retries, and backoff with jitter*. 2019. https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/. **P**. PRACTITIONER (vendor). Supports: retry budgets, jitter (`distributed-systems.md` 6; `playbooks.md` 4).
20. Beyer, B. et al. *Site Reliability Engineering* (free online). https://sre.google/sre-book/table-of-contents/. **P**. PRACTITIONER (vendor). Supports: cascading failures, monitoring (`reliability-ops.md`). Table of contents opened; chapters not read.
21. Microsoft. *Circuit Breaker pattern*. https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker. **P**. OFFICIAL (vendor). Supports: when to use a breaker (`distributed-systems.md` 6).
22. AWS. *Transactional outbox pattern*. https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html. **P**. OFFICIAL (vendor). Supports: outbox rules (`distributed-systems.md` 16).
23. Wiggins, A. *The Twelve-Factor App*. 2011. https://12factor.net/. **P**. PRACTITIONER. Supports: config, disposability, logs.
24. OWASP. *Cheat Sheet Series*. https://cheatsheetseries.owasp.org/. **P**. OFFICIAL. Supports: input validation, session management, logging (`security.md`). Landing page only; individual cheat sheets are **S**.
25. OWASP. *Top 10*. https://owasp.org/www-project-top-ten/. **P** (read 17/11/2026: the page states the 2025 edition is the current Top 10).
26. OWASP. *Application Security Verification Standard (ASVS)*. https://owasp.org/www-project-application-security-verification-standard/. **P**. OFFICIAL. Supports: verification levels (`security.md`). Landing page only.
27. OWASP. *API Security Top 10* (2023 edition). https://owasp.org/API-Security/editions/2023/en/0x11-t10/. **P**. OFFICIAL. Supports: broken object-level authorization (`security.md`). Page opened; BOLA category found.
28. OWASP GenAI. *Top 10 for LLM Applications*. https://genai.owasp.org/llm-top-10/. **P**. OFFICIAL. Supports: prompt injection (`ai-llm.md` 7). Page opened; term found; list version not checked.
29. W3C. *Web Content Accessibility Guidelines (WCAG) 2.2*. 2023. https://www.w3.org/TR/WCAG22/. **P**. OFFICIAL. Supports: accessibility targets (`frontend.md` 5).
30. Stripe. *Idempotent requests*. https://docs.stripe.com/api/idempotent_requests. **P**. OFFICIAL (vendor; design reference only). Supports: key retention and replay (`distributed-systems.md` 2). Page opened; a "24 hours" retention statement found; exact wording not copied.
31. pg-boss. *PostgreSQL job queue* (project page). https://github.com/timgit/pg-boss. **P**. OFFICIAL (project). Supports: queue defaults (`distributed-systems.md` 14). Page opened; option defaults not re-read. The old pgboss.io address was not tested.
32. Node.js. *Don't Block the Event Loop (or the Worker Pool)*. https://nodejs.org/en/learn/asynchronous-work/dont-block-the-event-loop. **P**. OFFICIAL. Supports: event loop stalls, worker threads (`performance.md` 6; `diagnosis-playbook.md` 1).
33. Microsoft. *TypeScript Handbook*. https://www.typescriptlang.org/docs/handbook/intro.html. **P** (read 17/11/2026: official handbook, sections Basics, Everyday Types, Narrowing, Functions, Object Types, Type Manipulation, Classes, Modules).
34. React team. *hydrateRoot*. https://react.dev/reference/react-dom/client/hydrateRoot. **P**. OFFICIAL. Supports: hydration mismatch causes (`diagnosis-playbook.md` 10; `frontend.md` 3). Page opened; "mismatch" text found.
35. React team. *You Might Not Need an Effect*. https://react.dev/learn/you-might-not-need-an-effect. **P**. OFFICIAL. Supports: effects discipline (`frontend.md` 2).
36. Microsoft. *IHttpClientFactory with .NET*. https://learn.microsoft.com/en-us/dotnet/core/extensions/httpclient-factory. **P**. OFFICIAL. Supports: HttpClient lifetime (`performance.md` 5). Page opened; term found.
37. Microsoft. *TimeProvider overview*. https://learn.microsoft.com/en-us/dotnet/standard/datetime/timeprovider-overview. **P**. OFFICIAL. Supports: injectable clock (`money-time-text.md` 2). Page opened; term found.
38. Fowler, M. *Yagni* (bliki). https://martinfowler.com/bliki/Yagni.html. **P**. PRACTITIONER. Supports: proportion (`architecture-design.md`).
39. Fowler, M., Sadalage, P. *Evolutionary Database Design*. https://martinfowler.com/articles/evodb.html. **P**. PRACTITIONER. Supports: additive schema change (`databases.md` 7). Page opened; Sadalage named as co-author.
40. Moseley, B., Marks, P. *Out of the Tar Pit*. 2006. https://curtclifton.net/papers/MoseleyMarks06a.pdf. **P**. PAPER. Supports: state and complexity. PDF fetched, title found; text not read.
41. Ongaro, D., Ousterhout, J. *In Search of an Understandable Consensus Algorithm (Raft)*. 2014. https://raft.github.io/raft.pdf. **S**. PAPER. Supports: consensus (`distributed-systems.md` 10). PDF fetched but text not extractable here; needs a PDF pass.
42. Drepper, U. *What Every Programmer Should Know About Memory*. 2007. https://akkadia.org/drepper/cpumemory.pdf. **S**. PAPER. Supports: cache behavior (`performance.md`). PDF fetched but text not extractable here.
43. Vaswani, A. et al. *Attention Is All You Need*. 2017. https://arxiv.org/abs/1706.03762. **P**. PAPER. Supports: transformers background (`ai-llm.md`). Landing page title and first author matched.
44. Deutsch, P. et al. *Fallacies of Distributed Computing* (secondary summary). https://en.wikipedia.org/wiki/Fallacies_of_distributed_computing. **P**. SECONDARY. Supports: network assumptions. Wikipedia article opened; it is a secondary source, not the original note.
45. Spolsky, J. *The Absolute Minimum Every Software Developer Must Know About Unicode*. 2003. https://www.joelonsoftware.com/2003/10/08/the-absolute-minimum-every-software-developer-absolutely-positively-must-know-about-unicode-and-character-sets-no-excuses/. **P**. PRACTITIONER. Supports: Unicode (`money-time-text.md` 3). The earlier short URL was not tested; use this one.
46. Winand, M. *Use The Index, Luke!* (free). https://use-the-index-luke.com/. **P** (read 17/11/2026: author Markus Winand; SQL indexing and tuning for developers).
47. Google. *The Site Reliability Workbook* (free). https://sre.google/workbook/table-of-contents/. **P**. PRACTITIONER (vendor). Supports: SLOs, alerting (`reliability-ops.md` 2). Table of contents opened.
48. Arpaci-Dusseau, R., Arpaci-Dusseau, A. *Operating Systems: Three Easy Pieces* (free). https://pages.cs.wisc.edu/~remzi/OSTEP/. **P**. BOOK. Supports: OS concepts. Landing page title matched.
49. Grigorik, I. *High Performance Browser Networking* (free). https://hpbn.co/. **P**. BOOK. Supports: network latency (`frontend.md` 4). Landing page title matched.
50. Toub, S. and the .NET team. *Performance Improvements in .NET* (annual posts). https://devblogs.microsoft.com/dotnet/. **S**. PRACTITIONER (vendor). Supports: runtime performance (`performance.md` 5). Blog index opened; no annual post read.
51. Nystrom, R. *Crafting Interpreters* (free). 2021. https://craftinginterpreters.com/. **P**. BOOK. Supports: language implementation. Landing page title matched.
52. Abelson, H., Sussman, G. *Structure and Interpretation of Computer Programs*. 1996. https://mitp-content-server.mit.edu/books/content/sectbyfn/books_pres_0/6515/sicp.zip/index.html. **P**. BOOK. Supports: abstraction. Landing page title matched (the old mitpress.mit.edu/sicp address was not tested).
53. Anderson, R. *Security Engineering* (free chapters). https://www.cl.cam.ac.uk/~rja14/book.html. **P**. BOOK. Supports: security design. Landing page title matched.
54. Wathan, A., Schoger, S. *Refactoring UI*. 2018. https://refactoringui.com/. **P**. BOOK. Supports: visual design basics. Landing page title matched.

## Papers (identity via DOI record)

55. Lamport, L. *Time, Clocks, and the Ordering of Events in a Distributed System*. Communications of the ACM 21(7), 1978. https://doi.org/10.1145/359545.359563. **P**. PAPER. Supports: ordering without wall clocks (`distributed-systems.md` 9). Identity only: title, author, venue and year matched in the Crossref DOI record; full text not read.
56. DeCandia, G. et al. *Dynamo: Amazon's Highly Available Key-value Store*. SOSP 2007. https://doi.org/10.1145/1294261.1294281. **P**. PAPER. Supports: eventual consistency (`distributed-systems.md` 1). Identity only (Crossref DOI record).
57. Saltzer, J., Reed, D., Clark, D. *End-to-End Arguments in System Design*. ACM TOCS 2(4), 1984. https://doi.org/10.1145/357401.357402. **P**. PAPER. Supports: where reliability belongs. Identity only (Crossref DOI record).
58. Knuth, D. *Structured Programming with go to Statements*. ACM Computing Surveys, 1974. https://doi.org/10.1145/356635.356640. **P**. PAPER. Supports: source of the "critical 3%" sentence quoted in `SKILL.md` 5. Identity only (Crossref DOI record: title, author, venue, year). The sentence itself was not located in the text this pass.

## Books

59. Evans, E. *Domain-Driven Design*. 2003. ISBN 978-0321125217. **V**. BOOK. Supports: aggregates, bounded contexts, ubiquitous language. Catalogue date is a later printing (2008).
60. Vernon, V. *Implementing Domain-Driven Design*. 2013. ISBN 978-0321834577. **V**. BOOK. Supports: tactical DDD, aggregate sizing. Catalogue date 2012.
61. Martin, R. C. *Clean Architecture*. 2017. ISBN 978-0134494166. **V**. BOOK. Supports: the dependency rule (`architecture-design.md`).
62. Ousterhout, J. *A Philosophy of Software Design*. 2018. ISBN 978-1732102200. **V**. BOOK. Supports: deep modules, complexity.
63. Fowler, M. *Patterns of Enterprise Application Architecture*. 2002. ISBN 978-0321127426. **V**. BOOK. Supports: repository, unit of work, money pattern. Catalogue date 2007 (a later printing).
64. Fowler, M. *Refactoring*, 2nd ed. 2018. ISBN 978-0134757599. **V**. BOOK. Supports: behavior-preserving steps (`playbooks.md` 1).
65. Feathers, M. *Working Effectively with Legacy Code*. 2004. ISBN 978-0131177055. **V**. BOOK. Supports: characterization tests, seams (`playbooks.md` 1).
66. Gamma, E., Helm, R., Johnson, R., Vlissides, J. *Design Patterns*. 1994. ISBN 978-0201633610. **V**. BOOK. Supports: pattern vocabulary. Catalogue date 1995 (first printing).
67. Richards, M., Ford, N. *Fundamentals of Software Architecture*. 2020. ISBN 978-1492043454. **V**. BOOK. Supports: trade-off analysis.
68. Khononov, V. *Learning Domain-Driven Design*. 2021. ISBN 978-1098100131. **V**. BOOK. Supports: strategic DDD.
69. Wlaschin, S. *Domain Modeling Made Functional*. 2018. ISBN 978-1680502541. **V**. BOOK. Supports: making illegal states unrepresentable.
70. Hunt, A., Thomas, D. *The Pragmatic Programmer*. 1999; 2nd ed. 2019. ISBN 978-0135957059. **S**. BOOK. Supports: craft habits. OpenLibrary returns a corrupted, unrelated record for this ISBN; title and authors (1999 edition) matched only in an OpenLibrary title search, so identity of the 2019 ISBN is not confirmed.
71. McConnell, S. *Code Complete*, 2nd ed. 2004. ISBN 978-0735619678. **V**. BOOK. Supports: construction practice.
72. Martin, R. C. *Clean Code* (read critically). 2008. ISBN 978-0132350884. **V**. BOOK. Supports: naming, small functions.
73. Brooks, F. *The Mythical Man-Month* (anniversary ed., includes *No Silver Bullet*). 1975; 1986. ISBN 978-0201835953. **V**. BOOK. Supports: essential versus accidental complexity. Catalogue shows the 1995 anniversary edition.
74. Kleppmann, M. *Designing Data-Intensive Applications*. 2017. ISBN 978-1449373320. **V**. BOOK. Supports: transactions, isolation, derived state (`distributed-systems.md`, `databases.md`).
75. Nygard, M. *Release It!*, 2nd ed. 2018. ISBN 978-1680502398. **V**. BOOK. Supports: timeouts, bulkheads, steady state (`distributed-systems.md` 6).
76. Hohpe, G., Woolf, B. *Enterprise Integration Patterns*. 2003. ISBN 978-0321200686. **V**. BOOK. Supports: messaging patterns. Catalogue date 2008 (a later printing).
77. Richardson, C. *Microservices Patterns*. 2018. ISBN 978-1617294549. **V**. BOOK. Supports: saga, outbox.
78. Newman, S. *Building Microservices*, 2nd ed. 2021. ISBN 978-1492034025. **V**. BOOK. Supports: service boundaries. Catalogue date 2020.
79. Petrov, A. *Database Internals*. 2019. ISBN 978-1492040347. **V**. BOOK. Supports: storage engines, replication.
80. Majors, C., Fong-Jones, L., Miranda, G. *Observability Engineering*. 2022. ISBN 978-1492076445. **V**. BOOK. Supports: tracing, high-cardinality events (`reliability-ops.md` 1).
81. Forsgren, N., Humble, J., Kim, G. *Accelerate*. 2018. ISBN 978-1942788331. **V**. BOOK + STUDY. Supports: delivery metrics (study figures are the book's own, not re-checked).
82. Humble, J., Farley, D. *Continuous Delivery*. 2010. ISBN 978-0321601919. **V**. BOOK. Supports: pipelines (`reliability-ops.md` 5).
83. Agans, D. *Debugging*. 2002. ISBN 978-0814474570. **V**. BOOK. Supports: measure before concluding (`diagnosis-playbook.md` Step 0). Catalogue date 2006.
84. Bhargava, A. *Grokking Algorithms*. 2016. ISBN 978-1617292231. **V**. BOOK. Supports: gentle introduction (`algorithms-complexity.md`).
85. Skiena, S. *The Algorithm Design Manual*, 3rd ed. 2020. ISBN 978-3030542559. **V**. BOOK. Supports: practical algorithms.
86. Cormen, T., Leiserson, C., Rivest, R., Stein, C. *Introduction to Algorithms*, 4th ed. 2022. ISBN 978-0262046305. **V**. BOOK. Supports: reference.
87. Sedgewick, R., Wayne, K. *Algorithms*, 4th ed. 2011. ISBN 978-0321573513. **V**. BOOK. Supports: data structures. Catalogue lists Sedgewick only.
88. Kleinberg, J., Tardos, E. *Algorithm Design*. 2005. ISBN 978-0321295354. **V**. BOOK. Supports: design techniques.
89. Knuth, D. *The Art of Computer Programming*. 1968 onward. ISBN 978-0321751041. **V**. BOOK. Supports: analysis of algorithms. Catalogue record is the volumes 1-4A boxed set (2011).
90. Okasaki, C. *Purely Functional Data Structures*. 1998. ISBN 978-0521663502. **V**. BOOK. Supports: persistent structures. Catalogue date 1999.
91. Bryant, R., O'Hallaron, D. *Computer Systems: A Programmer's Perspective*, 3rd ed. 2015. ISBN 978-0134092669. **V**. BOOK. Supports: hardware effects.
92. Gregg, B. *Systems Performance*, 2nd ed. 2020. ISBN 978-0136820154. **V**. BOOK. Supports: USE method, profiling (`performance.md` 1).
93. Kurose, J., Ross, K. *Computer Networking: A Top-Down Approach*. 2020 or 2021 printing. ISBN 978-0136681557. **V**. BOOK. Supports: networking. Catalogue shows a rental edition dated 2020 and lists Kurose only.
94. Cleary, S. *Concurrency in C# Cookbook*, 2nd ed. 2019. ISBN 978-1492054504. **V**. BOOK. Supports: async patterns (`concurrency.md` 2).
95. Herlihy, M., Shavit, N. *The Art of Multiprocessor Programming*, 2nd ed. 2020. ISBN 978-0124159501. **V**. BOOK. Supports: locks, lock-free.
96. Watson, B. *Writing High-Performance .NET Code*. 2018. ISBN 978-0990583486. **U**. BOOK. Supports: .NET performance. OpenLibrary returned 404 for this ISBN and a title search found nothing; treat as unverified.
97. Kokosa, K. *Pro .NET Memory Management*. 2018. ISBN 978-1484240267. **V**. BOOK. Supports: garbage collector.
98. Sipser, M. *Introduction to the Theory of Computation*. 2012. ISBN 978-1133187790. **V**. BOOK. Supports: theory. Catalogue date 2013.
99. Khorikov, V. *Unit Testing Principles, Practices, and Patterns*. 2020. ISBN 978-1617296277. **V**. BOOK. Supports: test quality pillars (`testing.md` 3).
100. Beck, K. *Test-Driven Development: By Example*. 2002. ISBN 978-0321146533. **V**. BOOK. Supports: TDD cycle (`playbooks.md` 1). Catalogue date 2006 (a later printing).
101. Meszaros, G. *xUnit Test Patterns*. 2007. ISBN 978-0131495050. **V**. BOOK. Supports: test doubles.
102. Aumasson, J.-P. *Serious Cryptography*. 2017. ISBN 978-1593278267. **V**. BOOK. Supports: applied cryptography (`security.md`).
103. Stuttard, D., Pinto, M. *The Web Application Hacker's Handbook*, 2nd ed. 2011. ISBN 978-1118026472. **V**. BOOK. Supports: web attacks (catalogue lists Stuttard only).
104. Richer, J., Sanso, A. *OAuth 2 in Action*. 2017. ISBN 978-1617293276. **V**. BOOK. Supports: OAuth flows.
105. Krug, S. *Don't Make Me Think, Revisited*. 2014. ISBN 978-0321965516. **V**. BOOK. Supports: usability.
106. Reis, J., Housley, M. *Fundamentals of Data Engineering*. 2022. ISBN 978-1098108304. **V**. BOOK. Supports: data pipelines.
107. Kimball, R., Ross, M. *The Data Warehouse Toolkit*, 3rd ed. 2013. ISBN 978-1118530801. **V**. BOOK. Supports: dimensional modeling. Catalogue lists Kimball only.
108. Turnbull, D., Berryman, J. *Relevant Search*. 2016. ISBN 978-1617292774. **V**. BOOK. Supports: search relevance.
109. Huyen, C. *AI Engineering*. 2025. ISBN 978-1098166304. **V**. BOOK. Supports: AI system design (`ai-llm.md`). Catalogue date 2024 (record may predate the print date).
110. Wayne, H. *Practical TLA+*. 2018. ISBN 978-1484238288. **V**. BOOK. Supports: formal specifications.
111. Larson, W. *Staff Engineer*. 2021. ISBN 978-1736417911. **V**. BOOK. Supports: engineering leadership. Catalogue lists Larson and a second name; cite Larson.
112. Skelton, M., Pais, M. *Team Topologies*. 2019. ISBN 978-1942788812. **V**. BOOK. Supports: team structure, Conway's law.
113. Cagan, M. *Inspired*. 2017. ISBN 978-1119387503. **V**. BOOK. Supports: product discovery.
114. Fitzpatrick, R. *The Mom Test*. 2013. ISBN 978-1492180746. **V**. BOOK. Supports: customer interviews. Catalogue date 2014.
115. McConnell, S. *Software Estimation*. 2006. ISBN 978-0735605350. **V**. BOOK. Supports: estimation.
116. Little, J. D. C. *A Proof for the Queuing Formula L = lambda W*. Operations Research 9(3), 1961. https://doi.org/10.1287/opre.9.3.383. **P**. PAPER. Supports: Little's law used in `diagnosis-playbook.md` Core arithmetic. Identity only (Crossref DOI record: title, author, venue, year 1961); full text not read.
117. Unicode CLDR, Plural rules: https://cldr.unicode.org/index/cldr-spec/plural-rules **P** (read 18/11/2026); Arabic and Polish categories not listed on the page.
118. ICU User Guide, Formatting messages (MessageFormat): https://unicode-org.github.io/icu/userguide/format_parse/messages/ **P** (read 18/11/2026); selectordinal not covered.
119. MDN, CSS logical properties and values: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_logical_properties_and_values **P** (read 18/11/2026); first 100,000 characters.
120. MDN, Intl: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl **P** (read 18/11/2026); index page, option details from general knowledge.
121. W3C Internationalization, HTML dir and bidi (qa-html-dir): https://www.w3.org/International/questions/qa-html-dir **P** (read 18/11/2026).
122. Next.js docs, Internationalization: https://nextjs.org/docs/app/guides/internationalization **P** (read 18/11/2026).

Totals: 116 entries; 111 V or P (96%); remaining S/U: NestJS custom providers page, Raft and Drepper PDFs (text not extractable), .NET blog index, Pragmatic Programmer ISBN record, Watson .NET book (ISBN not found).
Added 18/11/2026 (6 entries): 0 S.

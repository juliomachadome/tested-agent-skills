# EU Compliance Overview (engineering-relevant)

Not legal advice. Use this to recognize when a change has regulatory impact and to flag it; confirm specifics with legal/compliance.

## 1. GDPR (all products handling personal data of people in the EU)

- **Lawful basis** for each processing purpose (consent, contract, legal obligation, legitimate interest…). Consent must be specific, informed, freely given and as easy to withdraw as to give.
- **Special categories** (health data — including fitness/body/medical info — biometric, etc.) need explicit consent or another Art. 9 condition and stronger protection.
- **Data subject rights:** access/export (portability), rectification, erasure, restriction, objection. Engineering: build export and deletion flows that cover DB, blobs, backups policy, search indexes, caches, logs, analytics, third-party processors.
- **Privacy by design & default:** minimization, pseudonymization, encryption, least privilege, retention limits with automated deletion.
- **Records of processing**, DPIA for high-risk processing (large-scale health data, profiling).
- **Processors/sub-processors:** DPAs with vendors (cloud, email, analytics, LLM providers); international transfers outside the EEA need safeguards (adequacy decision such as the EU-US Data Privacy Framework, or SCCs).
- **Breach notification** to the authority within 72 hours where required → need logging and detection to know what happened.
- Cookies/trackers: ePrivacy rules → consent before non-essential cookies/analytics.
- Each member state has a national data protection authority; know which one is competent for you.

## 2. DORA — Digital Operational Resilience Act (Regulation (EU) 2022/2554)

- Applies since **17 January 2025** to EU financial entities (banks, investment firms, payment/e-money institutions, insurers, asset managers, crypto-asset service providers, etc.) and imposes obligations on their critical ICT third-party providers.
- Pillars: **ICT risk management framework**; **incident management, classification and reporting** of major ICT incidents; **digital operational resilience testing** (including threat-led penetration testing for some entities); **ICT third-party risk** (register of contractual arrangements, exit strategies, contract clauses); information sharing.
- Engineering implications: asset inventory, documented architecture and dependencies, access control and logging, backup/restore with tested RTO/RPO, change management, vulnerability management, incident detection and classification data, vendor/cloud exit plans, resilience tests.

## 3. MiFID II / MiFIR (investment services — relevant to wealth management)

- Investor protection: suitability/appropriateness assessments, product governance, best execution, cost and charges disclosure (ex-ante/ex-post), client categorization.
- **Record keeping:** orders, transactions, communications (including recording of telephone/electronic communications related to transactions) retained typically 5 years (up to 7 if requested by the authority).
- Transaction reporting and transparency obligations for certain entities.
- Engineering implications: immutable audit trails, accurate timestamps, retention and retrieval, report generation, data lineage for costs/charges calculations.
- National securities-market supervisors enforce it in each member state.

## 4. PSD2 (and the upcoming PSD3/PSR)

- Payments and open banking: **Strong Customer Authentication (SCA)** — two of knowledge/possession/inherence — with exemptions; dynamic linking for payments; regulated access to accounts via APIs for AIS/PIS providers.
- Relevant only if the product initiates payments, accesses bank accounts, or is a payment/e-money institution. Using a PSP (Stripe, Adyen) delegates most of it.

## 5. European Accessibility Act (Directive (EU) 2019/882)

- Applies since **28 June 2025** to many consumer-facing products and services, including e-commerce, consumer banking services, e-books, transport ticketing, and related websites/apps. Microenterprises providing services are exempt.
- Practical target: **WCAG 2.1/2.2 AA** via EN 301 549. See frontend.md for implementation.

## 6. EU AI Act (Regulation (EU) 2024/1689)

- Risk-based obligations phased in from 2025 onward: prohibited practices, transparency duties (e.g. disclose AI interaction, label synthetic content), stricter rules for high-risk systems (e.g. creditworthiness assessment), obligations for general-purpose AI model providers.
- Engineering implications: document AI features, inform users when they interact with AI, human oversight for consequential decisions, logging, data governance. Check the current application timeline — parts phase in through 2026–2027.

## 7. Other

- **NIS2** (cybersecurity for essential/important entities) — risk management and incident reporting.
- **PCI DSS** if handling card data — avoid by using hosted payment fields.
- **eIDAS** for electronic signatures/identification.
- Some member states require certified invoicing software and standard audit files (SAF-T) — relevant if the product issues invoices.

## 8. Engineering checklist when a change touches regulated data

- [ ] Is personal/special-category/financial data involved? Minimized? Retention defined?
- [ ] Audit trail: who, what, when (UTC), before/after, immutable?
- [ ] Access restricted and logged?
- [ ] Export/erasure paths still complete?
- [ ] New vendor/sub-processor or data transfer outside the EEA?
- [ ] Incident detection possible (logs/alerts) for this flow?
- [ ] Accessibility of new UI?
- [ ] Flag to compliance when unsure — say so in the PR description.

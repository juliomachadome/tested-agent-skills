# Tone: expert and technical

## When it fits
B2B software, developer tools, engineering, data, security and professional services, where the reader is a specialist who evaluates claims and distrusts marketing. Also documentation-adjacent pages (pricing, security, integrations).

## Word choices
- The field's exact terms, used correctly and consistently; define a new term once.
- Numbers with method: "p95 latency 180 ms on a 2-vCPU instance, measured 3 Nov, test script linked".
- Verbs that say what the system does ("validates", "queues", "encrypts at rest"), not what it "empowers".
- State limits and non-goals; experts trust a vendor who names them.

## Sentence rhythm
Dense but orderly: one claim, one qualifier, one piece of evidence. Short paragraphs, code or table where the reader would use one. Headings are descriptive nouns and verbs. No decorative metaphors.

## Do
- Lead with what it does and for whom; link to the docs and the changelog.
- Show an example, a command or a diagram of the real thing.
- Put the compatibility, version and pricing facts on the page.
- Use understated confidence: "Handles 10k events/s in our benchmark; here is the setup."

## Avoid
- "Revolutionary", "seamless", "robust", "world-class", "AI-powered" with no mechanism.
- Benchmarks without method; logos without permission; roadmap promises as features.
- Jargon to impress when a plain word is as exact.

## Before and after (same message: a log-search tool)
Before: "Unlock powerful, next-generation observability with our seamless AI-driven platform."
After: "Search 30 days of logs in under 2 seconds (p95, 1 TB/day, setup in the docs). Alerts, retention and a REST API on every plan; SSO on Team."

## Second example (same message: a pricing note)
Before: "Flexible, enterprise-grade pricing that scales with you."
After: "Free up to 5M events a month. Then EUR 0.40 per million, billed monthly in arrears. Volume discount above 500M by contract. Prices exclude VAT."

## Quick checks
- Can an engineer verify each number from the page or a linked doc?
- Are version, date and scope stated for every benchmark?
- Did you remove every adjective that has no number behind it?
- Is the first sentence of each section a claim, not a warm-up?

## Risks
- Legal: performance and security claims must be backed by tests; named customers and logos need written permission; compliance claims (SOC 2, GDPR) state scope and date (`../eu-consumer-law.md` covers consumers; B2B claims still fall under general misleading-advertising rules).
- Accessibility: tables and code need text alternatives and sufficient contrast.
- Translation: keep terms in English where the audience does; translate only what that audience translates.
- Failure mode: unreadable density. Layer it: one-line claim, then evidence.

## Sources
Mailchimp style guide (plainspoken, no fluffy metaphors); NN/g, concise scannable objective writing (credibility and objective language); GOV.UK content design (technical content for users). List: `../BIBLIOGRAPHY.md`.

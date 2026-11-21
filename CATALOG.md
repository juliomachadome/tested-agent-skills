# Catalog of Agent Skills

English-first discovery catalog for this repository: **35 skills** and **26 Claude Code agent definitions**. Skills are portable Markdown; agent files are Claude Code-specific. For portable role prompts, see [`agent-profiles/`](agent-profiles/).

## Evidence boundary

Historical Claude-based records show **31 full-protocol wins**, **2 ties**, **1 limited comparison**, **0 pending** and **1 not-applicable** entry. This is not a cross-model leaderboard. See [evaluation evidence](docs/evaluation-summary.md), [methodology](docs/evaluation-methodology.md) and [compatibility](docs/compatibility.md).

## Skills

### ad-creatives

Create, script, storyboard, review or analyse ad creatives for conversion - short vertical video for Reels, TikTok, Shorts and Stories, static images and carousels - covering the concept as the unit of testing, the first-3-seconds hook, structure by awareness level, formats and safe zones, sound and burned-in captions, test batches, reading hook/hold/CTR against purchases, fatigue and refresh, and ad policy plus EU law (fake urgency, testimonials, AI-generated faces and voices, stock and music licences). Use it whenever someone asks for ad ideas, hooks, a UGC-style script, "why is this ad not working", "make variations of this winner", a creative brief, or wants to render an ad by code, even without the word "creative". It produces the piece; budgets and kill rules live in paid-traffic, final words in copywriting, price/deadline claims in offers.

Historical comparison: **win**. Trigger record: 5/5 expected, 0/5 false, 3 run(s).

### agent-orchestration

Plan and dispatch Claude Code agents without wasting quota - choose model and effort per task type, decide whether to spawn at all, write short self-contained briefs, forbid nested subagents, cap parallelism by machine RAM, run one heavy job at a time, use worktrees for parallel edits, supervise drift and loops, verify agent reports, diagnose why agents burn quota or stall, pace by quota. Use it whenever someone says "which model for this", "should I spawn an agent", "split this across agents", "run these in parallel", "write the brief for the agent", "my quota burns too fast", "agents are slow or stuck", "the agent says it is done but nothing changed", "background or foreground", or is about to dispatch more than one agent. Not for the agent loop inside a product you are building (llm-engineering), system design (software-architecture) or reviewing a diff (code-review-criteria).

Historical comparison: **win**. Trigger record: 4/5 expected, 0/5 false, 3 run(s).

### business-model-finance

Use for the money side of a small digital business, product, course, app or SaaS run by a solo founder or small team, even for a quick question - "does this business make money", "how many sales to break even", "unit economics", "contribution margin after fees and refunds", "build a P&L", "cash flow forecast", "how much does Hotmart/Kiwify/Eduzz/Gumroad/Stripe/Paddle/App Store take", "MEI or Simples Nacional", "LTV CAC payback", "runway", "MRR and churn", "base/low/high scenarios", "launch budget", "should I reinvest or take profit", "selling but no money left", "ads profitable but not in the bank", EU VAT OSS basics, Business Model Canvas or Lean Canvas as thinking tools. Brings the arithmetic, dated fee tables and diagnosis trees. Not for price or offer design (offers), growth dashboards and experiments (growth-analytics), market sizing (market-research) or legal/tax advice for a specific case (accountant).

Historical comparison: **win**. Trigger record: 5/5 expected, 0/5 false, 3 run(s).

### cloud-deploy-ops

"Railway, Vercel, Supabase, Cloudflare R2, Upstash, RunPod, Docker, GitHub Actions - invoke this skill FIRST, before running commands or answering, for any deploy or cloud-operations question, however short. Examples - \"prod still shows the old version after I deployed on railway\", \"set up staging and production for next.js on vercel + api on railway + supabase, keep secrets separate\", \"we leaked the resend api key in a log, rotate it across railway and vercel without downtime\", \"our runpod serverless bill doubled, make it cost 0 when idle\". Also env vars, healthchecks, rollbacks, regions, backups and restores, cost caps. Rules - deploy by commit SHA, healthcheck closes the deploy, idle spend checked at zero, backup proven by restore. Not for app code (engineering-playbook), slow pages (web-performance), RLS flaws (software-security), local docker-compose or GDPR region law, mobile store releases and app builds (mobile-app-engineering)."

Historical comparison: **win**. Trigger record: 5/5 expected, 0/5 false, 3 run(s).

### code-craft

Use for code-level design craft in any language (examples in TypeScript and C#) - "is this clean code", "refactor this", "code smells in this file", "this class does too much", "too many ifs", "which design pattern", "should I use a repository", "value object or entity", "write this test-first", "TDD this feature", mocks vs fakes, SOLID that over-abstracts, aggregates and invariants, anemic domain model, characterization tests for legacy code, result types vs exceptions. Gives a decision per case with the cost of the abstraction, the evidence strength and a small safe step. Not for system design and architecture styles (software-architecture), production incidents and API or database practices (engineering-playbook), PR verdicts (code-review-criteria), test strategy and release gates (qa-verification), or speed (web-performance).

Historical comparison: **win**. Trigger record: 4/5 expected, 0/5 false, 3 run(s).

### code-review-criteria

"Pull request or diff in front of you, invoke this skill FIRST, before reading files or answering, whenever someone wants a verdict on code they did not write or are about to merge, even for one line. Examples \"can you review my PR, it's the diff in feature/bulk-archive vs main\", \"LGTM?\" with a pasted diff of a helper, \"my reviewer says this useEffect is wrong, who's right\", \"should I split this PR\", \"copilot left 30 comments, which are real\", \"approve or block\", \"reviews take days\", \"blocker or nit\". Gives the approval standard, per-diff Step 0 (what changed, risk class, evidence), risk order, concurrency and tenant checks, React pitfalls, test quality, finding format (file:line, scenario, severity, fix), labels, large-PR and AI-code routines, review-process diagnosis. Not for proving a change works end to end (qa-verification), attacker audits (software-security), refactoring or writing the feature (engineering-playbook) or profiling (web-performance)."

Historical comparison: **win**. Trigger record: 4/5 expected, 0/5 false, 3 run(s).

### copywriting

"Use whenever the task is words a customer reads to decide, buy or stay - landing and sales pages, homepage, headlines, value propositions, CTAs and button labels, app store descriptions (\"improve this app store description so more people install\"), checkout and form microcopy, error and empty states, onboarding and welcome e-mails (\"this email feels flat, make it compelling without hype\"), paywall text, tone of voice choices, and translating or adapting marketing text into another language (\"not word for word\"). Also diagnoses a page that gets traffic but no clicks or sales. Triggers include \"write copy for\", \"this copy is weak\", \"make it convert\", \"headline help\", \"what tone should we use\". Claims must be provable; EU consumer-law limits built in. Not for ad video scripts or hooks (ad-creatives), price, bonus or guarantee structure (offers), keyword briefs (seo-geo) or support replies (customer-support)."

Historical comparison: **win**. Trigger record: 4/5 expected, 0/5 false, 3 run(s).

### customer-support

>-

Historical comparison: **tie**. Trigger record: 5/5 expected, 0/5 false, 3 run(s).

### data-analysis

Use for any general data analyst task on a business or product dataset, even short ones - "analyse this CSV/spreadsheet", "write the SQL for", "why don't these numbers match", "the join doubled revenue", "dashboard disagrees with the database", "is this difference significant", "clean this data", "build a KPI dashboard", "what does this data say", "forecast next month", or a pasted table or query result. Covers framing the question, SQL (grain, joins, windows, NULLs, dedup, time zones), fact and dimension modelling, cleaning and data quality, exploratory statistics, simple forecasts, pandas and spreadsheets, KPI dashboards, memos and privacy in analysis. Checks data trust first, shows the arithmetic, states uncertainty. Not for experiments, funnels, cohorts of product use or attribution (growth-analytics), chart styling (ui-design), ML models or data platforms, or privacy law.

Historical comparison: **win**. Trigger record: 4/5 expected, 0/5 false, 3 run(s).

### data-engineering

Use for building, fixing or reviewing data pipelines and the warehouse behind the numbers, even for short questions - "build a data pipeline", "model this in the warehouse", "dbt model", "incremental model misses rows", "our numbers differ between dashboard and database", "events arrive late or duplicated", "warehouse bill is too high", "backfill", ingestion from APIs, webhooks, files or CDC, ELT vs ETL, Postgres vs BigQuery vs Snowflake vs DuckDB, facts, dimensions, grain, slowly changing dimensions, Kimball vs wide tables vs data vault, Airflow or Dagster or cron, data tests, freshness, schema drift, time zones, PII and retention in pipelines, partitioning and clustering, lineage. Small-team defaults first. Not for analysis and SQL questions (data-analysis), dashboards and charts (data-visualization-dashboards), app schema and migrations (engineering-playbook), system design (software-architecture) or privacy law.

Historical comparison: **win**. Trigger record: 4/5 expected, 0/5 false, 3 run(s).

### data-visualization-dashboards

Charts and dashboards people must read and decide from - invoke this skill FIRST, before answering, for any chart choice, dashboard review or data presentation, even a short one. Examples - "which chart for signups by channel over 12 months", "make this dashboard better, it has 22 tiles and nobody opens it", "design a KPI dashboard", "this chart is confusing", "present these numbers to the board", "pick colours that work for colour-blind readers and pass contrast", "Metabase or Looker Studio", pie vs bar, truncated or dual axis, takeaway titles, metric definitions and refresh. Owns the decision (which form, what to cut, honest scales, KPI hierarchy, board pack, BI tool); plotting-library code alone can use a general chart or dataviz skill. Not for the numbers, SQL or significance (data-analysis), which metrics or experiments (growth-analytics), story arc (storytelling), visual system and tokens (ui-design), or pipelines (data-engineering).

Historical comparison: **win**. Trigger record: 4/5 expected, 0/5 false, 3 run(s).

### engineering-playbook

Backend and full-stack code (TypeScript/Node/NestJS, React/Next.js, C#/.NET, SQL/Postgres) - invoke this skill FIRST, before answering, for any production code question, even a short one. Examples - "this endpoint takes 2s, it queries the customer for each order" (N+1), "the domain folder keeps importing from infrastructure" (Clean/Hexagonal boundaries, lint rules), "safe migration or index on a 30M-row table without blocking writes", duplicate charges after a webhook retry, validation errors as problem+json (RFC 9457), pagination, idempotency, retries, queues and outbox, money, time and Unicode, multi-tenant data, tests, observability, diagnosing a production code problem, routines (test-first change, new endpoint or job, hotfix, upgrade), "best practice way", "most performant". Not for narrow jobs a specialist owns (software-security, web-performance, code-review-criteria for a PR verdict, llm-engineering, cloud-deploy-ops, software-architecture for system design and ADRs).

Historical comparison: **win**. Trigger record: 4/5 expected, 0/5 false, 3 run(s).

### growth-analytics

Use for any product or growth analytics task, even short ones - North Star and input metrics, tracking plans and event naming, funnels, activation and retention cohorts, A/B tests ("is this significant", "sample size", peeking, sample-ratio mismatch, guardrails), unit economics (CAC, LTV, payback), attribution limits (platform vs analytics vs holdout tests), and privacy-safe measurement with consent. Triggers - "why did conversion drop", "signups up but activation down", "the A/B winner did not hold", "dashboards disagree", "CAC is rising", "which metric should we track", "analytics without cookies", or pasted numbers or a metrics export, even without the word growth. Diagnoses data trust first, shows the arithmetic, states uncertainty, no p-hacking. Not for buying media or ad structure (paid-traffic), feature discovery and roadmap (product-management), page copy (copywriting), price design (offers), or general SQL, data cleaning and ad-hoc analysis (data-analysis).

Historical comparison: **win**. Trigger record: 4/5 expected, 0/5 false, 3 run(s).

### lifecycle-messaging

Use for any lifecycle or CRM message sent to existing users or customers by email, push, in-app, SMS or WhatsApp - design the journey map and triggers, "welcome email sequence", "abandoned cart flow", "trial to paid emails", "push notifications strategy", "failed payment emails" (dunning), "win back churned users", cancellation save, review and referral asks, re-permission, "how often should we email", send time, segmentation, "our emails go to spam" (SPF, DKIM, DMARC, Gmail and Yahoo bulk-sender rules, bounces, complaints, warm-up), "WhatsApp messages to customers" (templates, opt-in), consent and unsubscribe by country, and measuring with holdouts instead of last-click or open rate. Country-neutral. Not for the wording and tone of the message (copywriting), tests and metric design (growth-analytics), law in depth, support replies (customer-support), discount and price rules (offers) or screen design (ux-design).

Historical comparison: **win**. Trigger record: 5/5 expected, 0/5 false, 3 run(s).

### llm-engineering

"ALWAYS use this skill, even for a short question, when work involves calling an LLM or embedding API (Gemini, Claude, OpenAI, pgvector), for example \"our gemini call costs too much, cut tokens without hurting quality\", extended thinking on or off for a step, prompt and context design, structured outputs, RAG (chunking, hybrid pgvector search, reranking, citations verified in code), \"RAG cites the wrong documents after a chunk size change\", agent loops with tools and their prompt-injection risk, \"how many test cases do I need to claim my classifier's abstention or accuracy is above 95%\" (sample size, confidence interval), evals, LLM-as-judge, prompt caching, routing, model choice, hallucinated or slow output, GraphRAG, OWASP LLM Top 10, text-to-SQL. Run /llm-engineering audit for a full review. Not for dispatching Claude Code agents (agent-orchestration), plain backend code or SQL migrations (engineering-playbook), A/B tests (growth-analytics) or web security like XSS and CSRF (software-security)."

Historical comparison: **win**. Trigger record: 4/5 expected, 0/5 false, 3 run(s).

### market-research

Use before building or launching any product (ebook or PDF, course, kit, community, service, app, SaaS, physical product) to decide whether the opportunity is worth pursuing - "is there a market for", "is this idea worth it", "validate this product idea", "how big is the market", "who are my competitors", "will people pay for", "this video went viral, should I sell something", "research the market for". Frames who, problem and current alternative, reads demand signals honestly (search trends, communities, competitor traction, waitlists, pre-sales), sizes the market bottom-up, tears down competitors, tests willingness to pay, runs cheap ethical validation, and scores go, pivot or no-go. Brazil and global sources. Not for discovery interviews or PRDs (product-management), price structure or guarantees (offers), building the product, or running the ads (paid-traffic).

Historical comparison: **win**. Trigger record: 5/5 expected, 0/5 false, 3 run(s).

### media-production

Use to make or choose how to make images, video, 3D, voice and music for any use (ads, organic posts, product pages, launch videos, series), and to check rights before publishing. Triggers "make a video for", "generate images for my ad", "keep the character consistent", "render this in Blender", "turn my site into a launch video", "which stock site", "AI voiceover", "can I use this music", "does this need an AI label", "cost per video". Picks the route by goal, deadline, budget and rights (AI, stock, live footage, 3D, video by code), then covers prompts, consistency, Blender JSON renders, Remotion and ffmpeg, captions, formats, loudness, QA and licences. Not for hooks and scripts (viral-content, ad-creatives), story structure (storytelling), page or ad copy (copywriting) or screen design (ui-design).

Historical comparison: **win**. Trigger record: 4/5 expected, 0/5 false, 3 run(s).

### mobile-app-engineering

Use for any iOS or Android app task, even a short one, with Expo and React Native as the main example, plus notes for native Swift and Kotlin. Triggers "Expo build fails", "app rejected by Apple", "TestFlight", "push notifications not arriving", "app slow on Android", "app feels slow or janky", animation, gesture, haptics or sound in an app (Reanimated, Gesture Handler, Lottie, Rive), "offline mode", "OTA update", "deep link opens the browser", "in-app purchase", "release to Play Store", EAS signing and certificates, crash on launch, staged rollout, permissions, Expo Router, SQLite sync, app size, Sentry or Crashlytics, Maestro or Detox tests. Gives diagnosis trees, release and rollback runbooks, OTA rules, offline sync design, store checklists. Not for web pages (engineering-playbook, web-performance), screen visual design (ui-design), flows (ux-design), store listing copy (copywriting, seo-geo app-aso), servers (cloud-deploy-ops) or pricing (offers).

Historical comparison: **win**. Trigger record: 4/5 expected, 0/5 false, 3 run(s).

### offers

Build, review or fix the offer behind a digital product, course, info-product, coaching or service, or a low-ticket funnel - what is sold, positioning and the claims you can prove, offer and mechanism naming, the promise, price and anchor, comparison ("was/now") price, guarantee and refunds, order bump, upsell/OTO and downsell, bonuses, promotions and urgency, gift codes, quiz funnels - and read the numbers (revenue per visitor, take rate, refunds, disputes). Use it whenever someone asks "what should I charge", "should I add a bonus/bump/upsell", "is this discount legal", "write a guarantee", "build a quiz funnel", "my offer converts badly", or plans a sale, Black Friday or launch price, even if they never say "offer". Brings the arithmetic, diagnosis trees and the EU consumer-law limits. For SaaS tiers and plans use pricing; for the words on the page use copywriting.

Historical comparison: **win**. Trigger record: 4/5 expected, 0/5 false, 3 run(s).

### paid-traffic

"Use to plan, diagnose, read and scale paid media on Meta, TikTok and Google/YouTube: break-even CPA and budget, account structure, test, kill and scale rules, and a symptom-to-cause diagnosis tree for CPA up, CTR down, CPM spike, fatigue, learning limited, delivery stopped, pixel vs backend gaps, CAPI dedup and Event Match Quality, attribution windows, UTMs, consent and Performance Max/Advantage+ effects; also reads pasted ads-manager CSVs and reconciles them with backend revenue (MER, incrementality). Triggers: \"why did CPA go up\", \"should I kill this ad\", \"how do I scale\", \"learning limited\", pasted ads numbers. Plans and reads; never operates an account. Not for what to charge or the offer itself (offers), ad concepts and scripts (ad-creatives), page copy (copywriting) or organic search (seo-geo)."

Historical comparison: **win**. Trigger record: 5/5 expected, 0/5 false, 3 run(s).

### process-improvement

Use when a company project or operation must be justified to a manager, director or committee - a business case for automating, fixing or speeding up a process (approvals, invoices, orders, hiring, stock, support, reports), an A3, a DMAIC or lean six sigma project or charter (scope, out of scope, assumptions, risks, constraints), a value stream map, AS IS and TO BE, lead time and waiting time, rework, or hours saved turned into money per month, payback and break-even month, cost reduction vs revenue growth vs innovation. Brings the method and the honest money model (hard vs soft savings, ramp-up, cumulative cash curve, the threshold where the case flips). Not for a new product or the business model of a venture (business-model-finance, product-creation), unit economics of a sale (business-model-finance), chart styling (data-visualization-dashboards), a data analysis (data-analysis) or code design (software-architecture).

Historical comparison: **win**. Trigger record: 4/5 expected, 0/5 false, 3 run(s).

### product-creation

Use to turn a validated opportunity or audience into a product and grow it in phases, for any product type - ebook, template, ready project folder, Notion, course, cohort, community, mentoring, done-for-you, no-code tool, app, SaaS, print on demand, dropshipping or own stock. Picks the build mode (fast, standard, polished), cuts the MVP, plans delivery, onboarding and support, versions it, and decides the next rung or when to kill it. Triggers "what product should I create", "turn this audience into a product", "ebook, course or SaaS", "how fast can I launch", "MVP for this", "should I make it simple or polished", "next product after this one", "product ladder", "physical product or digital", "refunds are high", "built too much before selling". Not for market validation (market-research), price design (offers), the numbers (business-model-finance), sales page (copywriting) or software PRDs (product-management).

Historical comparison: **win**. Trigger record: 4/5 expected, 0/5 false, 3 run(s).

### product-management

Product management - invoke this skill FIRST, before answering, for any product decision, even a short one - prioritising a backlog ("here are 25 items, prioritise with RICE and tell me what to cut"), deciding whether a feature is worth building ("200 users asked for dark mode but nobody pays"), roadmaps ("turn this idea list into an outcome-based roadmap with a metrics tree"), PRDs, specs, user stories and acceptance criteria, discovery and customer interviews (Mom Test, jobs to be done, opportunity solution trees), RICE, Kano, cost of delay, cutting scope, success metrics, launch reviews, and diagnosing product problems ("nobody uses the feature we shipped", "the CEO wants these three features", "we ship a lot but nothing moves"). Also when someone pastes a feature idea or backlog. No reason, no feature. Not for screen design (ux-design, ui-design), experiments, funnels and tracking (growth-analytics) or price tiers (offers).

Historical comparison: **win**. Trigger record: 5/5 expected, 0/5 false, 3 run(s).

### qa-verification

"ALWAYS use this skill, even for a short question, before saying a change is done and whenever someone asks to test it or decide if it ships, for example \"verify the fix works before I merge\", \"our e2e test for checkout is flaky on CI\", \"which tests should I run for this diff\", \"write test cases for this business rule\", \"CI is green but the bug is in production\", \"is the new onboarding flow ready to ship, I need a go/no-go with evidence\", \"run the tests\". Picks tests by risk and diff, writes stable Playwright E2E without sleeps, proves real flows in a deployed environment, checks accessibility, payments, webhooks, hunts false greens (zero tests ran, skipped, stale build, lying mocks). Reports PASSED, FAILED or NOT VERIFIED. Not for a plain unit test file for one utility, code quality review (code-review-criteria), authorization checks (software-security), slowness (web-performance), screen design (ux-design) or mobile store releases and app builds (mobile-app-engineering)."

Historical comparison: **win**. Trigger record: 4/5 expected, 0/5 false, 3 run(s).

### redigir

Guided copywriting command. Collects the brief, then writes with the existing offers, storytelling and copywriting skills.

Historical comparison: **not applicable**. Trigger record: pending/5 expected, pending/5 false, pending run(s).

### sales

Use for any B2B, B2G (public tender) or founder-led/self-serve sales task, even short ones - diagnose a stalled or lost deal ("no next step", "ghosted after the proposal", "too expensive", "they use a competitor", "procurement is slow"), prepare a discovery call, qualify with MEDDICC, handle objections, negotiate, write a proposal or follow-up cadence, answer a public tender or edital (Lei 14.133, EU 2014/24, FAR), review a pipeline and forecast, or read a call transcript or CRM export. Ethical by default. Not for page or ad copy (copywriting, ad-creatives), price tiers, bundles or guarantees (offers), or support replies and refunds (customer-support).

Historical comparison: **win**. Trigger record: 5/5 expected, 0/5 false, 3 run(s).

### seo-geo

Make pages findable and citable in Google, Bing/Copilot, local, app-store, YouTube and social search, AI Overviews and AI Mode, ChatGPT search and Perplexity, in any country and language, using only methods the search engines accept - query research in the audience's language, content briefs, helpful/people-first content and E-E-A-T without fake authors, titles and meta, canonical, sitemap, robots and AI crawlers, hreflang, internal links, JSON-LD and which rich results still exist, Next.js metadata pitfalls, A/B tests without hurting search, video/YouTube, and measurement in Search Console and Bing Webmaster. Use it whenever someone creates or publishes a content page, touches metadata or structured data, asks "why am I not ranking", "traffic dropped", "not indexed", "how do I show up in ChatGPT/AI Overviews", "do I need llms.txt", "is AI content penalised", or plans a blog or programmatic pages, even without saying SEO or GEO. Final article prose belongs to the writer and copywriting.

Historical comparison: **win**. Trigger record: 4/5 expected, 0/5 false, 3 run(s).

### software-architecture

Software architecture and system design - invoke this skill FIRST, before answering, for any system-level question, even a short one. Examples - "do we need a message queue for emails and PDFs or is a direct call fine", "write an ADR for row-level security versus schema-per-tenant", "draw the C4 context and container diagram from this repo structure", "should we split into microservices", "add a cache", "multi-tenant architecture", "noisy neighbour", "distributed monolith", "duplicate events", "this is getting hard to change", review this architecture, structure the modules. Picks a style from the project (modular monolith, microservices, event-driven, serverless, hexagonal/clean, CQRS, multi-tenant), trade-offs by characteristics, data and consistency, outbox and idempotency, stability patterns, 12-factor, fitness functions, strangler fig, ADRs. Prefers the simplest design that meets the stated needs. Not for code-level practices (engineering-playbook) or LLM features (llm-engineering).

Historical comparison: **win**. Trigger record: 5/5 expected, 0/5 false, 3 run(s).

### software-security

"ALWAYS use this skill, even for a short \"is this ok?\" question, when code touches auth, user data, uploads, money or a mobile app's secrets and storage. Triggers \"can user B read user A's orders through GET /api/orders/:id\", \"is the JWT in localStorage bad\", \"our Stripe webhook parses JSON before checking the signature, ok for launch?\", \"review my supabase migration or RLS policy for multi-tenant\", \"I save the original upload filename in /public/uploads\", \"we leaked a key\", \"is my Expo app safe to ship\". Think like an attacker on web, API and mobile app security, covering login, sessions, IDOR, tenant isolation, Postgres RLS, payments, webhooks, uploads, secrets, CORS/CSRF/CSP, SSRF, rate limits, deep links, certificate pinning and incident response. Returns findings by severity with file:line, exploit, fix and test. Not for legal basis or consent, PR review (code-review-criteria), prompt injection in LLM features (llm-engineering) or deploy mechanics (cloud-deploy-ops)."

Historical comparison: **tie**. Trigger record: 5/5 expected, 0/5 false, 3 run(s).

### storytelling

Use whenever the job is narrative craft, in any medium - "tell this as a story", "write a story-driven script", "my story is boring", "nobody cares about my story", "structure this pitch", "brand story", "storyboard a series", "make this presentation a story", "story arc for a season", "hero's journey or three acts?", "logline", "interactive or vote-driven series", a founder story, a data story, a 60-120 second AI-generated story. Gives the minimum story (a character who wants something, an obstacle, a change), structure options with their limits, stakes, scenes and turns, open questions and payoff, specificity, the psychology of transportation, and ethics (no invented testimonials, disclose fiction and AI). Diagnoses stories that bore, confuse, sag or feel generic. Not for final sales copy (copywriting), ad production specs (ad-creatives), data charts (data-analysis) or viral distribution metrics (viral-content).

Historical comparison: **win**. Trigger record: 5/5 expected, 0/5 false, 3 run(s).

### ui-design

"Use for the visual side of screens and design systems, including quick numeric questions such as \"compute the contrast ratio of #767676 on white, does it pass AA\", \"4px or 8px spacing scale\", \"type scale with body size, line height and line length for dense data tables\", dark mode and status colors (is inverting ok, red/green), grids, visual hierarchy (\"my settings screen looks amateur, too many things fight for attention\"), choosing or applying a visual style (Apple HIG, Material 3, Fluent, neo-brutalism, Swiss, editorial, minimalist, glass, Liquid Glass, retro, data-dense, playful), design tokens (DTCG), motion, touch targets, dashboards, brand colors that fail contrast, matching a mockup by computed CSS values. Not for flows, forms, heuristics or ARIA semantics (ux-design), load speed (web-performance) or bold free-form aesthetic direction (frontend-design)."

Historical comparison: **win**. Trigger record: 4/5 expected, 0/5 false, 3 run(s).

### ux-design

Usability and accessibility of flows and screens - invoke this skill FIRST, before answering, whenever someone asks to review a screen, form or flow, rate usability problems by severity, check WCAG or keyboard and screen-reader access, or decide an interaction (confirm dialog vs undo, empty, loading and error states), even a short one. Examples - "review this settings screen for usability problems and rate each by severity", "our signup form has 11 fields and users bounce", "delete selected, confirm dialog or undo toast", "check the dashboard against WCAG 2.2 AA, target size 2.5.8", "how should our chatbot show sources", "why do users drop off at checkout", "make this form accessible". Also usability tests, heuristic evaluation, card sort, forms (Baymard), ARIA patterns, SUS, product-type variants (SaaS, e-commerce, mobile, marketplace, AI chat). Not for colours, type or tokens (ui-design), speed (web-performance), activation metrics (growth-analytics) or free aesthetic direction (frontend-design).

Historical comparison: **win**. Trigger record: 5/5 expected, 0/5 false, 3 run(s).

### viral-content

Use for organic short-form video reach on Instagram Reels, TikTok and YouTube Shorts - why people stop, watch, rewatch, share, save, follow and buy, and how to build or diagnose a piece from that. Triggers "make this go viral", "why are my reels stuck at 200 views", "hook ideas for TikTok", "script a reel", "analyse this viral video", "posting frequency", "how does the Instagram/TikTok algorithm work", "views but no followers", "works on TikTok not Reels", pasted post stats (views, watch time, shares, saves, follows). Psychology first, formats second. Covers diagnosis by metric, scripting, testing routine, trend and music rights, AI labels, and the path from views to follows to sales. Not for paid ads (ad-creatives), landing or sales copy (copywriting), media buying and budgets (paid-traffic), keyword content (seo-geo) or dashboards (growth-analytics).

Historical comparison: **win**. Trigger record: 4/5 expected, 0/5 false, 3 run(s).

### web-motion

"Use when a web page or web app needs movement or sound, even for a short question - an animated landing page or hero, animation on scroll (scroll-driven CSS, ScrollTrigger), an interactive explainer or step-through diagram, a micro-interaction (button press, toggle, add-to-cart), animated SVG, canvas, Lottie or Rive, a three.js or WebGL scene, page or view transitions, interface sounds (click, success or error sounds, a mute toggle) or vibration. Examples - \"make this hero feel alive without hurting load time\", \"animate the steps as the user scrolls\", \"should I use three.js or CSS for this\", \"add a subtle click sound with a mute toggle\". Picks the lightest tool, keeps motion purposeful, pausable and reduced-motion safe, and checks it in a browser. Not for colours, type and tokens (ui-design), flows and accessibility (ux-design). Not for native iOS/Android apps, Expo or React Native (mobile-app-engineering). Not for form and submit states (ui-design)."

Historical comparison: **limited comparison**. Trigger record: 3/5 expected, 0/5 false, 1 run(s).

### web-performance

"Use when anything is slow or heavy, even a short question, for example \"this postgres query takes 3 seconds, how do I read EXPLAIN ANALYZE\", \"what Cache-Control for hashed JS bundles vs HTML\", \"should I add this charting library, worried about bundle size\", slow landing page or long list, Core Web Vitals (LCP, INP, CLS), JS budget per route, images, fonts, video, CDN and service worker caching, \"p99 spikes every few minutes, which stage is slow\" (tail latency, tracing), N+1, indexes, keyset pagination, cold start, cost per user. Always asks for a number before and after. Not for visual polish (ui-design), LLM token cost (llm-engineering), deploy mechanics (cloud-deploy-ops) or schema design (engineering-playbook)."

Historical comparison: **win**. Trigger record: 5/5 expected, 0/5 false, 3 run(s).

## Claude Code agents

### ad-creative-strategist

Strategist and producer of conversion ad creatives (short video for Reels, TikTok, Shorts and Stories; static image and carousel), in the audience's language and culture. Use proactively to create, script, review, produce or analyse ad creatives, build a test batch, read creative metrics (hook, retention, CTR, CPA, revenue) and refresh a fatigued piece; also organic short-form reach (hooks, scripts, why reels stall) with viral-content. Does not set price, write the sales page or manage the campaign on the platform.

Core skills: `ad-creatives`.

### bi-analyst

BI and dashboard analyst. Use proactively when a task needs a dashboard or report designed or reviewed, a KPI hierarchy and one governed metric definition sheet written, the right chart chosen, a confusing, cluttered or misleading chart fixed (truncated or dual axis, pie, too many tiles), a colour-blind safe palette picked, a board or investor pack laid out, a slow dashboard diagnosed, or a BI tool chosen and set up (Metabase, Looker Studio, Power BI, Tableau, Superset). Names one reader and one decision per page and checks honesty, accessibility and refresh. Does not build pipelines (data-engineer), run experiments or define the North Star (growth-analyst) or do ad-hoc analysis with no dashboard deliverable (data-analyst).

Core skills: `data-visualization-dashboards`.

### code-reviewer

Read-only code reviewer for a diff, commit range or pull request (back end and front end). Use proactively before merging to the main branch, and always when the change touches security, permissions, multi-tenant isolation, money, time or personal data; returns verified findings ordered by risk (correctness, security, data, performance, design, tests) with file:line, failure scenario, severity, fix and the test that reproduces it. Never edits. Does not run the whole test gate (qa-verifier) or do an attacker-style audit (security-reviewer).

Core skills: `code-review-criteria`.

### customer-support

Customer support specialist. Use proactively when a customer ticket arrives or support material is needed, to draft replies and macros, triage tickets by severity, set SLAs, write help-center articles, build reproducible escalations for engineering, handle refund and cancellation requests under consumer law, and read CSAT/CES/NPS honestly. Does not write marketing copy (that is the copywriting skill) and does not fix code.

Core skills: `customer-support`.

### data-analyst

Data analyst for business and product datasets. Use proactively when a task needs a CSV, spreadsheet, SQL result or table analysed, SQL written or reviewed, numbers that do not match reconciled, a join that inflated a sum, data cleaned or quality-checked, a difference or trend judged for significance, a simple forecast, a KPI dashboard specified, or a result written up for a decision. Checks data trust first and shows the arithmetic and the uncertainty. Does not design experiments (that is growth-analyst), design schemas or data platforms, or build ML models.

Core skills: `data-analysis`.

### data-engineer

Data engineer for pipelines and the warehouse behind the numbers. Use proactively when a task needs a data pipeline built or fixed, ingestion from an API, webhook, file or CDC, a dbt model or test written or reviewed, an incremental model that misses rows, an orchestration job that fails or runs late, a backfill made safe to rerun, late or duplicate events handled, data quality checks or contracts added, a warehouse bill reduced, or PII masked, retained or deleted inside the pipeline. Starts from the smallest stack that works and proves a fix with row counts. Does not answer business questions from the data (that is data-analyst), design dashboards (bi-analyst), change the app schema (fullstack-engineer) or decide architecture (nextjs-architect).

Core skills: `data-engineering`.

### finance-analyst

CFO-role analyst for the money side of a small digital business, product or app. Use proactively when someone asks if a product makes money, for unit economics and contribution per sale after fees and refunds, a P&L or cash-flow forecast, break-even, runway, base/low/high scenarios, what a platform or payment processor really takes, or the margin effect of a price or discount. Reads fee pages live and dates them; taxes only as general rules to confirm with a professional in the country. Does not set offer structure or price levels (offer-pricing-strategist), analyse raw datasets (data-analyst) or read funnels and experiments (growth-analyst); not tax or legal advice.

Core skills: `business-model-finance`.

### fullstack-engineer

Senior full-stack engineer that implements fixes and features end to end (front, API, database, jobs) in whatever stack the repository uses. Use proactively when there is a code change with defined items (file:line, test report, review finding, small spec); delivers green, verified commits, one per item, test-first, with the smallest safe diff. Does not decide architecture or scope (nextjs-architect, the brief) and does not review its own diff (code-reviewer).

Core skills: `engineering-playbook`.

### growth-analyst

Growth and product analyst. Use proactively when a task needs metrics, tracking or test results, to define the North Star and input metrics, write tracking plans, read funnels and cohorts, design and read A/B tests (sample size, peeking, sample-ratio mismatch, guardrails), judge attribution honestly, and check analytics against consent rules. Works with paid-traffic and seo-geo for acquisition channels. Does not buy media and does not write the copy.

Core skills: `growth-analytics`.

### media-producer

>-

Core skills: `media-production`.

### nextjs-architect

Web product architect for Next.js (App Router) with its own API, Postgres/Supabase and payments (e.g. Stripe). Use proactively before coding anything that changes an API contract, schema or migration, the server/client boundary, caching or proxy, a queue or job, region, cost or a platform limit, and whenever a measurement shows slowness or a ceiling. Delivers a short design with the simplest alternative, numbers and an ADR; does not implement the feature.

Core skills: `software-architecture`.

### offer-pricing-strategist

Offer, pricing and funnel specialist for low-ticket info products and digital products. Use proactively when setting or changing price, anchor or comparison price, guarantee, order bump, upsell/OTO, downsell, promotion, gift or customer discount, and when reading sales metrics (revenue per visitor, take rate, refunds). Delivers the recommendation with the math and the legal risk under EU consumer law. Does not write the final copy (that is the copywriting skill) and does not edit code.

Core skills: `offers`.

### paid-media-buyer

Paid traffic manager (media buyer) for low-ticket info products and digital products on Meta Ads (Facebook and Instagram), TikTok Ads and Google/YouTube. Use proactively to plan or review budget, account structure, audiences, creative, audience and landing page tests, cut and scale rules, measurement (pixel, conversions API, UTM, consent) and to read campaign results (CPM, CTR, cost per visit, CPA, ROAS, revenue per visitor). Delivers plan and reading with the math. Does not create or edit campaigns, does not access ad accounts, does not write creatives (ad-creative-strategist) or copy (copywriting skill), and does not set price (offer-pricing-strategist).

Core skills: `paid-traffic`.

### platform-engineer

Platform engineer for deploys and cloud operations - environments and env vars, regions, healthchecks, rollback, on-demand GPU, object storage and signed URLs, database pooler and backups, scheduled jobs, secret rotation and cloud cost. Use proactively when a task touches deploy, environment variables, a cloud service, GPU, region, schedules, secrets, backup or restore. Deploys by verified commit SHA; production, paid resources and destructive actions only with the owner's explicit OK. Does not build product features (fullstack-engineer) or review code (code-reviewer).

Core skills: `cloud-deploy-ops`.

### process-improvement-analyst

Process-improvement analyst that builds the case a manager or committee must approve for a cost-saving or efficiency project. Use proactively when someone asks for a business case for a project, an A3, a DMAIC project or charter (scope, out of scope, assumptions, risks, constraints), a value stream map, an AS IS and TO BE, hours turned into money per month, the break-even month, or whether a project is cost reduction, revenue growth or innovation. Delivers a one-sheet case with the honest money model (hard vs soft savings, ramp-up, cumulative cash curve, low case). Does not set up taxes, financing or cash forecasts (finance-analyst), design a new business model (venture-strategist), style the charts (bi-analyst), analyse raw datasets (data-analyst) or build the change.

Core skills: `process-improvement`.

### product-manager

Product manager. Use proactively when someone proposes a feature, idea or backlog, to run discovery, turn an idea into a PRD with acceptance criteria, prioritise a backlog, cut scope, define success metrics and metrics trees, and shape an outcome-based roadmap. Challenges every feature with the reason test. Does not design the UI (that is ui-ux) and does not write code.

Core skills: `product-management`.

### prompt-engineer

Prompt engineer that writes and changes prompts and LLM calls (system prompts, few-shot examples, structured output schemas, hostile-data fencing, model and parameter choice, prompt versioning). Use proactively when a task touches a prompt, an LLM call, ingested data reaching a model, output format or examples. Delivers diff, hypothesis, token estimate and an eval request; never measures or approves its own work. Does not build retrieval or evals (rag-eval-engineer).

Core skills: `llm-engineering`.

### qa-verifier

QA and delivery verification for web projects. Decides, with evidence, whether a change is ready - picks what to test by risk, runs only the tests proportional to the diff (lint, types, unit, integration, focused e2e), checks accessibility, screens at several sizes and the payment path, and hunts false greens. Use proactively when a feature or fix is finished, before any claim of "done" or "works", before merge and at the release gate. Does not fix code - reports PASSED, FAILED or NOT VERIFIED. Does not review code quality or security (code-reviewer, security-reviewer).

Core skills: `qa-verification`.

### rag-eval-engineer

ML and data engineer for LLM and RAG quality - builds and runs evals (retrieval recall, answer faithfulness, citation precision, calibrated abstention), sealed test sets, paired comparisons with Wilson intervals and sample-size checks, and tunes hybrid retrieval, embeddings, chunking, reranking and thresholds by error class. Use proactively when a change touches search, chunks, embeddings, thresholds, eval sets or quality gates, and to measure any prompt change written by someone else. Does not write prompts (prompt-engineer) or product features (fullstack-engineer).

Core skills: `llm-engineering`.

### real-user-tester

Real-use tester that walks a deployed test environment as the persona given in the brief (end user, admin, buyer), in a headless browser, with screenshots and reproducible bug reports. Use proactively after each deploy to a test environment to test only what changed, its neighbors and flows never tested, judging flow, broken UI, usability heuristics and WCAG 2.2 AA. Does not fix code or decide scope; reports findings only (qa-verifier owns the release gate).

Core skills: `ux-design`.

### sales-rep

Sales specialist for B2B, B2G (public tenders) and founder-led or self-serve sales. Use proactively when a deal, lead, tender or proposal is on the table, to prepare discovery calls, qualify leads, write proposals and tender responses, draft follow-up sequences, handle objections and negotiation, and review a pipeline. Does not write marketing pages (that is the copywriting skill) and does not set price or offer structure (that is offer-pricing-strategist).

Core skills: `sales`.

### security-reviewer

Security reviewer for web products on Postgres/Supabase (RLS and grants), payments (e.g. Stripe), paid media behind signed URLs and privacy law (GDPR and similar). Use proactively before pushing any change that touches login or session, purchase or access release, a policy or migration, media or upload, a webhook, admin, personal data or cookies. Returns findings by severity with file:line and a test that proves them; fixes only what the brief asks. Does not review general code quality (code-reviewer).

Core skills: `software-security`.

### seo-geo

SEO and GEO specialist for websites and web products (Google, Bing/Copilot, AI Overviews and AI Mode, ChatGPT, Perplexity), in any country and language, using only methods search engines accept. Use proactively to research real queries in the audience's language, write the brief for each content page, run the SEO/GEO gate before publishing, handle metadata, JSON-LD, sitemap, robots, canonical, hreflang and internal links (including in Next.js), assess the search impact of A/B tests and new pages, and measure in Search Console and Bing Webmaster Tools. Does not write the final article (that is the writer, with the copywriting skill) and does not implement features outside SEO.

Core skills: `seo-geo`.

### ui-ux-designer

Product UI/UX specialist (iOS/Android app, web and PWA) following Apple HIG, with Material 3, Laws of UX, NN/g, Baymard and WCAG 2.2 AA. Use proactively to design or review any screen, flow, form, checkout, landing page or design system, in a design tool or in code, before implementing and before approving. Delivers a plan with wireframe, a screen, or a review with measurements and screenshots at 390/820/1440. Does not write sales copy or implement business rules.

Core skills: `ux-design`, `ui-design`.

### venture-strategist

CEO-role strategist for a new product or venture (what to create and whether to keep it alive, not which features an existing product builds next). Use proactively when someone asks which opportunity or product to pursue, whether an idea is worth building, for a go/no-go or kill-or-continue call, which build mode fits (fast, standard, polished), for a phase review after first sales, or for the next rung of a product ladder. Validates demand, sets the kill threshold before spending, and decides with reasons. Does not set price or offer structure (offer-pricing-strategist), build the financial model (finance-analyst), prioritise features, roadmap or backlog of an existing product, or write the PRD (product-manager), write copy or code.

Core skills: `market-research`.

### web-performance-engineer

Performance specialist for websites, web apps and PWAs. Measures and fixes Core Web Vitals (LCP, INP, CLS), JS weight per route, images, fonts, audio and video, cache and CDN, service workers, Postgres queries (indexes, EXPLAIN, N+1, pagination) and infrastructure cost per user. Use proactively when creating or changing a landing page, list, heavy screen, media, data fetching, a new dependency or a database query, and whenever someone says something is slow. Always delivers a measured before and after. Does not redesign screens (ui-ux-designer) or decide architecture (nextjs-architect).

Core skills: `web-performance`.

## Historical PT-BR catalog

The earlier detailed catalog was authored in Brazilian Portuguese. It is retained as historical project material and should not be read as fresh English evaluation evidence. The English metadata above is generated from each canonical `SKILL.md` and agent definition.

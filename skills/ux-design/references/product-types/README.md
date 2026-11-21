# Product types: pick the variant

Choose the variant before designing or reviewing. Order: (1) the current project's rules, design system, glossary and ADRs win over everything here; (2) signals in the repository or the brief; (3) the user's own words. If two types fit, read both and name the primary one. If none fits, use the general skill only and say so.

| Signals in the project or request | Variant |
|---|---|
| Roles, seats, admin, tenants, tables, bulk actions, SSO, audit log, "dashboard", trial to paid | `saas-b2b.md` |
| Cart, catalog, product page, checkout, shipping, returns, promo codes | `ecommerce.md` |
| Native app or PWA for individuals, push, onboarding, permissions, store ratings, one-hand use | `mobile-app-consumer.md` |
| Two sides (buyers and sellers, hosts and guests), listings, reviews, messaging, payouts, disputes | `marketplace.md` |
| Articles, video, audio, feeds, subscription or ads, recommendations, comments | `content-media.md` |
| Courses, lessons, quizzes, progress, certificates, learners and teachers | `education-learning.md` |
| Payments, banking, insurance, health data, consent, KYC, legal or clinical duties | `fintech-health-regulated.md` |
| API, CLI, SDK, docs, console, onboarding by first call, dashboards for engineers | `developer-tools.md` |
| Points, streaks, levels, rewards, leaderboards, game loop | `games-gamified.md` |
| Chat, copilot, generated answers, citations, agents that act | `ai-assistant-chat.md` (plus `../ai-features-ux.md`) |

Mixed products are common (a fintech mobile app with a marketplace). Take the regulated variant as a constraint layer over the others: its rules win on consent, disclosure and errors. Each variant has: key jobs, critical flows, typical pitfalls, metrics, checklist, sources. They add to, never replace, the per-screen checklist in SKILL.md and the WCAG floor. Metric targets are starting points; the product's own baseline replaces them. Source names point to `../BIBLIOGRAPHY.md`.

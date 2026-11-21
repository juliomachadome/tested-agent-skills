# Publisher and content sites (blogs, magazines, news, guides)

## What matters most
Quality systems reward original, expert, current content that satisfies the reader; scaled, derivative, or ad-first pages lose after core updates. Trust is the centre of E-E-A-T: who wrote it, how it was made, why. [C #1, #15, #39]
- Fewer, better pages beat many thin ones; prune and merge.
- First-hand experience and original information (data, photos, tests, interviews) is the differentiator.
- Reader experience: fast, no intrusive interstitials, ads that do not push content out of sight.

## Page templates
- Article: answer first, byline linked to an author page with real credentials (or the organisation as author), date published and a visible updated date only for substantive changes, sources, related reading, clear sections.
- Hub or topic page: curated map of the topic with links to children.
- Category and tag archives: only if useful; noindex thin tags.
- News: timely items, corrections policy, clear separation from sponsored content.
- Evergreen guides with a refresh schedule.

## Structured data (candidates)
`Article`/`NewsArticle`/`BlogPosting` with headline, image, `datePublished`, `dateModified` (real), author and publisher [#9]; `BreadcrumbList`; `Organization`; `VideoObject` on watch pages [#29]; `Person` only for real people. FAQ and HowTo rich results are not shown, so write questions into the text instead.

## Pitfalls
- Invented authors or AI headshots; fake review expertise [#1].
- Third-party or sponsored content on the site purely to borrow reputation (site reputation abuse) [#36].
- Changing dates without real edits [#1].
- Mass-produced AI or spun posts; many near-identical "best X in city" pages [#2].
- Tag and date archives indexed by the thousand.
- Intrusive ads, interstitials, back-button hijacking (spam policy since Apr 2026).
- Affiliate pages with no first-hand testing.
- Relying on discover or social spikes; losing it on a core update.

## Metrics
Clicks and impressions by page group; share of traffic from non-brand queries; newsletter signups per 1,000 sessions; engaged reading time; returning readers; revenue per session; index coverage of archive templates; rate of pages with zero clicks in 12 months; citation in AI answers for topics you own.

## Checklist
- [ ] Every article has a real author or the organisation, a policy page and sources.
- [ ] Original asset in each piece; an editorial reason to exist.
- [ ] Update rule and quarterly refresh and prune (`../playbooks.md` 5).
- [ ] Thin archives noindexed or removed; sitemap lists real articles only.
- [ ] Ads and consent banners tested on mobile for CLS and overlay.
- [ ] No sponsored or third-party content outside the site's focus and control.
- [ ] Corrections and update notes visible when material.
- [ ] Core update drop procedure ready (`../diagnosis-playbook.md` tree 1).

## Sources
#1, #2, #9, #15, #29, #36, #39 (rater guideline sections on page quality and YMYL), #38, #32 generative AI content guidance.

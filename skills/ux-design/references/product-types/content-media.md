# Content and media

## Key jobs
A reader or viewer finds something worth their time, consumes it without friction, and comes back by choice. A publisher funds the work through subscription or ads without wrecking the experience.

## Critical flows
Discovery (home, feed, search, topics); the reading or viewing page; media controls; saving and continuing; subscription or paywall; comments and sharing; newsletter or notification subscribe; accessibility of media.

## Typical pitfalls
- Interstitials, auto-play with sound, cookie walls that cover content, ads that shift layout (reserve space).
- Paywalls with hidden cancel; dark patterns at subscribe and cancel (Gray et al.; deceptive.design).
- Infinite feeds with no position memory, no end, and no keyboard way to reach the footer.
- Recommendation opacity: the person cannot tell why they see something or fix it.
- Video without captions and transcripts (WCAG 1.2), auto-moving carousels without pause (2.2.2), low-contrast text on images.
- Search that returns only exact matches; categories by the publisher's org chart; unclear labels (information scent).
- Newsletter and consent pop-ups shown before the person has read anything, and again on every visit.
- Notification overload: breaking-news pushes for everything.

## Metrics
Engaged time and scroll depth (with caution: time is not value); return rate within 7 days; search success and zero-result rate; subscribe conversion and cancel flow completion; caption use; complaint themes. For paywalls, copy and offer are handled by `paywalls`, `offers` and `copywriting`.

## Checklist
- [ ] Reading width, size and line height comfortable; zoom to 200% without breaking.
- [ ] Media: captions, transcript, keyboard controls, no autoplay with sound, pause for moving content.
- [ ] Layout stable while ads and images load.
- [ ] Position is remembered; a footer or end is reachable.
- [ ] Recommendations explainable and adjustable ("show less of this").
- [ ] Subscribe and cancel are symmetrical in effort.
- [ ] Search with typo tolerance and a useful no-results page.
- [ ] Notification categories and frequency control.

## Worked check
Measure layout shift on an article page with ads: load it on a throttled connection and record any movement of the text after first paint; any shift of the line being read is a defect to fix with reserved space (speed numbers go to `web-performance`).

## Sources
NN/g information scent, progressive disclosure, push notification mistakes, deceptive patterns, mental models; Baymard no-results and search research; WCAG 1.2, 2.2.2, 1.4.x, 2.4.x; Gray et al. 2018; Krug (scanning, not reading).

# Local business (shops, clinics, restaurants, services with a place or service area)

## What matters most
Local results mix three things: the Business Profile and its signals (relevance, distance, prominence), the website, and reviews and citations. You cannot move distance; you can keep data accurate, earn reviews and give each real location a useful page. [C #48]
- One verified profile per real location, correct primary category, consistent name, address, phone (NAP) and hours everywhere.
- A location page per physical place with unique, true content; for service-area businesses, a page per area only where you genuinely serve and can say something specific.
- Reviews: ask all customers, reply to all, never gate by sentiment or buy them.

## Page templates
- Home: what, where, who, how to contact, with the main location linked.
- Location page: address, map link, opening hours (including holidays), phone, parking or access, services at this place, staff or team, photos of the actual place, reviews (real, with source), directions, one CTA (call, book, directions).
- Service page: what is done, who it is for, price range or process, proof (before/after, cases), local FAQs answered in text.
- Area page (service-area only): the area, travel time, local examples. Not one page per postcode with a swapped name (doorway, #2).

## Structured data (candidates; check the gallery)
`LocalBusiness` or a subtype (`Restaurant`, `Dentist`...) with `address`, `geo`, `openingHoursSpecification`, `telephone`, `url`, `image`, `sameAs`; `Organization` on the home page; `BreadcrumbList`; `Review`/`AggregateRating` only for reviews you own and show, never self-serving on your own business markup where the docs say it is not eligible [#8, #27]. The visible page must show the same data.

## Pitfalls
- NAP differences ("St." vs "Street" are fine; different phones or old addresses are not).
- Keyword-stuffed profile name, virtual office addresses, duplicate profiles [#48].
- City pages in bulk with the same text.
- Blocking the website behind a booking widget that is JavaScript-only with no text.
- Reviews markup copied from a third party.
- Forgetting Apple and Bing listings [#49, #50].

## Metrics
Profile: searches, calls, direction requests, website clicks, bookings. Site: Search Console clicks to location pages, branded vs non-brand, queries with "near me" or the town name. Business: calls and appointments with a source. Read rankings from physical points around the location, not from the office.

## Checklist
- [ ] Profile verified, primary category, hours (holidays), photos of the real place, services listed.
- [ ] Location page per location matches profile data exactly.
- [ ] Phone and address as text and tappable links.
- [ ] LocalBusiness data matches the page and validates.
- [ ] Review request flow after service; replies within days.
- [ ] Apple Business Connect and Bing Places claimed.
- [ ] Local backlinks that are real (chamber, suppliers, local press), none bought.
- [ ] Core Web Vitals on mobile, click-to-call works.

## Sources
#7-8 structured data, #27, #48 Business Profile guidelines, #49 Apple Business Connect, #50 Bing Places (not read), #2 spam policies, `../beyond-google.md` local section. See also `../diagnosis-playbook.md` tree 11.

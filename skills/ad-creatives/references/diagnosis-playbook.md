# Creative diagnosis playbook: symptom, cause, check, fix

Scope: why a creative underperforms and what to change in the creative. Budget, kill statistics, scaling and account structure live in paid-traffic (`../paid-traffic/references/testing-and-scaling.md`, `diagnosis-playbook.md`, `measurement-diagnosis.md`); link to them, do not copy their numbers. Thresholds here are **[F]** starting points unless tagged; the account's own 4-week baseline replaces them. Tags as in `SKILL.md`.

## Metric definitions (write the formula in every report)
Platform column names differ and change; **verify the exact name in the ads manager before reporting** (names below were not re-read on the platforms' help pages in the last pass).

| Metric | Formula | Platform name (verify) | Worked example (one ad) |
|---|---|---|---|
| Hook rate | 3-s video views ÷ impressions | Meta "3-second video plays"; TikTok has 2-s and 6-s view counts, so state which one you divide by | 2,625 ÷ 10,500 = 25.0% |
| Hold rate | ThruPlay (15 s, or the whole video if shorter) ÷ 3-s views | Meta "ThruPlay"; TikTok/YouTube differ, state the cut | 787 ÷ 2,625 = 30.0% |
| Link CTR | link clicks ÷ impressions | Meta "link clicks" (not "all clicks": it includes reactions and profile taps) | 189 ÷ 10,500 = 1.80% |
| Cost per visit | spend ÷ landing page visits (analytics, not clicks) | own analytics | 86 ÷ 160 = 0.54 |
| Visit ÷ click | visits ÷ link clicks | | 160 ÷ 189 = 85% (below ~75% is a leak before the page) |
| Page conversion | purchases ÷ visits | | 4 ÷ 160 = 2.5% |
| CPA | spend ÷ purchases | | 86 ÷ 4 = 21.5 |
| ROAS | whole-funnel revenue ÷ spend | | 116 ÷ 86 = 1.35 |
| Revenue per visitor | revenue ÷ visits | | 116 ÷ 160 = 0.73 |
| Frequency | impressions ÷ reach (state the window) | | 1.7 over 7 days |

Identity: `CPA = CPM ÷ 1000 ÷ (CTR × visit÷click × page conversion)`. Hook and hold are triage; the decision metric is purchases, CPA, ROAS, revenue per visitor of the whole funnel. Hook and hold are practitioner names built from platform columns.
Evidence: attention is not sales. One vendor dataset (≈88k Meta video ads, Jan-Jun 2026, method unpublished) ranked the highest-hook category 12th of 14 in ROAS **[F][1-SRC]**.

## Step 0: can this ad be judged at all?
Do every check before any tree. A wrong denominator makes every branch meaningless.

| Check | Rule | If it fails |
|---|---|---|
| Enough delivery | Impressions per ad for hook/hold/CTR: at least ~5,000 (a rate on 1,000 impressions moves several points on noise) **[F]**. For CPA: purchases per ad, and spend vs the kill rule in paid-traffic (`testing-and-scaling.md`) | Write "not enough volume to conclude". With under 10 purchases the CPA range is very wide (table in paid-traffic) |
| Same conditions | Compared ads ran in the same ad set or same dates, audience, placements, objective, optimisation event, budget | A "winner" under different conditions is delivery bias. Rerun or compare only the like for like |
| Delivery is not equal | The platform gives unequal spend to ads in one ad set; low spend share ≠ bad ad | Read rates per ad; judge spend-starved ads only on rates, not CPA |
| Attribution window | Same window and click-only vs view-through for all ads. Reporting windows changed on Meta in 2026 (paid-traffic notes the 7-day and 28-day view windows were removed from reports) **[search, secondary]**; history before and after is not comparable | Use one clicks-only column; restate the baseline |
| Learning phase | First days after launch or after a significant edit: delivery and CPM unstable | Do not judge CPA inside learning; rates after ~3 days and ≥5,000 impressions |
| Placement mix | Hook and hold differ by placement (Reels vs Feed vs Stories) | Compare by placement or at ad level with the same mix |
| Backend check | Platform purchases ÷ backend orders stable | If not, go to paid-traffic `measurement-diagnosis.md` first |
| Something else changed | Price, coupon, page, checkout, payment, outage in the same week | Not a creative problem; fix the cause |

## Tree 1: low hook rate (nobody stops)
Benchmark in your account first; as a rough bar, hook rate well below your account median on the same placement is weak **[F]**; "above 30% is good" is a myth **[X]**.

| Cause | Check | Fix (cheapest first) |
|---|---|---|
| Frame 0 is a logo, black, fade or slow intro | Pause at frame 0 and read it as a still thumbnail | Start on the situation or the result; first line on screen from frame 0 |
| Image, text and voice say different things at the start | Mute and read; then listen with no picture | One proposition in all three |
| Hook is about the brand, not the viewer's situation | Does it name a situation or a number a stranger recognises? | Rewrite as a situation, a question about the situation (not an assertion about the person) or a surprising real fact |
| Small text, low contrast, text under the UI | Check in the platform preview inside the safe zone | `specs-safe-zones-audio.md` |
| Same hook seen already (audience familiar) | Frequency, ad age, audience size | Tree 5 |
| Placement quirk | Hook by placement | Judge per placement |

## Tree 2: good hook, low hold (drop at 3-8 s)
| Cause | Check | Fix |
|---|---|---|
| Bait: the hook promises what the body does not pay | Read hook and body together; is the promised thing shown by 8 s? | Pay the promise early or soften the hook (policy also bans misleading hooks) |
| Slow setup after the hook | Count seconds from hook to product on screen | Product in use by ~5 s; cut the intro |
| Hook is a visual trick, body is a talking head | Retention curve step at the cut | Keep the same visual language across the cut |
| Length: the viewer cannot see the end | Hold by length across ads | Short version (6-10 s) of the same script |
| Audio mismatch: music or voice changes at the cut | Listen at the cut | Even audio bed; captions burned in |
| Hold is computed on a different cut (15 s vs full) | Same definition across ads | Fix the definition in the report |

## Tree 3: good hold, low CTR
| Cause | Check | Fix |
|---|---|---|
| No reason to leave the app now | Is there a stated next step and what the click gives? | One action, spoken and on screen, in the ad's own words |
| CTA hidden under the UI or only in the caption | Safe-zone preview | Move CTA; end card button label equals the platform button |
| Ad satisfies curiosity fully (content is the product) | Comments and saves high, clicks low | Leave the demo's last step for the page |
| Audience is entertained, not buying | Attention without purchase intent | Concept-level change (Tree 6) |
| Link CTR measured as all clicks | Column used | Link clicks only |

## Tree 4: high CTR, low conversion
Split first: visit ÷ click (page loads) and page conversion (page convinces).

| Cause | Check | Fix |
|---|---|---|
| Message-landing mismatch | Does the page's first screen repeat the ad's image, phrase, offer, price? | Align the page top; owner of the page changes it (copywriting) |
| Curiosity clickbait | Hook promised a reveal; the page does not give it | Lower the promise; if the hook is a tease, show the answer in the first screen |
| Price or deadline in the ad differs from the page | Compare that day | Same price and date; expired ad down (law: `policy-and-law.md`) |
| Wrong audience pulled by a broad hook | Which segments click vs buy (age, country, placement) | Narrow the hook to the real buyer's situation |
| Slow page or in-app browser break | Visit ÷ click below ~75% | paid-traffic Tree F; not the creative |
| Checkout problem | Checkout starts ÷ visits | Not the creative |

## Tree 5: winner fatigues fast
Signal that counts: frequency rising AND link CTR falling AND cost per visit rising with page conversion stable **[F]**. If page conversion also falls, the cause is elsewhere (offer, page, traffic mix, tracking). Magic thresholds ("frequency above 2.5", "CTR down 20% in a week") come from vendor blogs **[X]**; compare with your own history. Repetition lowers response is directionally supported but second-hand figures vary (45% to 60% at the fourth exposure) **[M]**.

| Cause | Check | Fix |
|---|---|---|
| Frequency in a small audience | Reach vs impressions by week; new-reach share; audience size vs spend | Widen audience, new concept (not another hook swap on the same body), lower spend on that ad set |
| Budget scaled faster than the audience grows | Spend vs reach growth | Step budgets by the rules in paid-traffic; spread across more concepts |
| Same body, new hook: viewers recognise the body | Hold on the swapped hook falls fast | New body or angle |
| Seasonal CPM | Same weeks last year; CPM across all campaigns | Wait; do not rewrite on one week |
| Only one creative carries the account | Spend share by ad | Keep 3-5 distinct concepts live |

Refresh order, cheapest first: new 3-s hook on the same body; same script in another format; same angle with another proof; new concept. See `playbooks.md` §5-7.

## Tree 6: all variations perform the same
| Cause | Check | Fix |
|---|---|---|
| Variations are one concept in different clothes (same persona, proof, angle) | Write each as the one-line concept (`SKILL.md` §2); do two lines match? | Change a higher level: persona, awareness stage, proof or format, not the hook |
| The real driver is outside the creative | Offer, audience, page, price | Test the offer or page (offers, copywriting), not more ads |
| Platform delivery clustered similar ads | Spend share concentrated in one ad | Fewer, more different ads per group |
| No volume to separate them | Purchases per ad | Say "no difference detectable"; pool by concept before comparing |

Concept vs iteration: concept = persona × angle × awareness × proof × format (batch question "which sells"); iteration = one change on a winner (question "why/how much").

## Tree 7: UGC looks fake or low trust
| Cause | Check | Fix |
|---|---|---|
| Script read from a paper, polished lines | Watch with sound off and on; does it sound like speech? | Brief the creator with beats, not lines (`playbooks.md` §3) |
| Over-produced stock look or obvious actor | Compare with the organic feed on that platform | Shoot native: phone, natural light, real room |
| Claims too large for a stranger | Comments ("scam", "ad") | Smaller, provable claim; show the product in use |
| AI-generated or paid faces presented as customers | See law | Do not present a person as a customer or expert unless true; disclose AI where required |
| No real proof on screen | Is the product visible and working? | Screen recording or real unboxing |

## Tree 8: ad rejected or account restricted
Do not edit and resubmit blindly; repeated violations raise account risk.

| Step | Action |
|---|---|
| 1 | Read the exact reason on the platform's notice; log date, ad ID, policy name |
| 2 | Match to a rule: misleading claim or hook, personal attribute, fake urgency, before/after, AI disclosure, music/IP, landing page mismatch (`policy-and-law.md`) |
| 3 | Fix the cause (not the wording only), then appeal via the platform's own form once with the fix described |
| 4 | Check other live ads for the same pattern before the account is flagged |
| 5 | If the account is restricted: stop new submissions with the same pattern; use the platform's account-quality page; do not open duplicate accounts to bypass (itself a violation) |
Evidence: Meta's policies cover personal attributes and prohibited commercial practices; TikTok's misleading-content policy requires an AI label or clear disclaimer for significantly AI-altered or generated media and warns of rejection (read 15/11/2026; see BIBLIOGRAPHY); Google disapproves and can suspend accounts for repeat violations.

## Tree 9: comments are negative
| Pattern | Likely cause | Action |
|---|---|---|
| "Scam", "fake" | Over-promising, stock people, countdowns | Remove the claim; show real product; check the page |
| "Where is the price?" | No price clarity | Price on the page and a line in the caption if lawful |
| "I did not know this was an ad" | Branded content not disclosed | Use the platform's partnership label (law playbook) |
| Many questions | Interest, unclear proof | Pin a clear answer; add the answer in the next cut |
| Hate for the creator | Creator mismatch | Replace the creator in the next batch |
Moderating negative comments by hiding true criticism is a reputation and sometimes legal risk; respond with facts; never delete real customer reports as policy.

## Tree 10: static beats video, or the reverse
Question is format, not quality. Same concept, same proof, one change: format. Images test cheaply and sometimes sell alone **[F]**; "video always beats image" is a myth **[F]**. Compare by cost per purchase and revenue per visitor at similar spend, not by hook rate (a static has no 3-s play). If the static wins: use it as a cheap tester, turn the winning image's phrase into a hook for video. If video wins: keep the static as retargeting or cut-down.

## Tree 11: works on one platform, not another
| Cause | Check | Fix |
|---|---|---|
| Native language of the platform: pace, sound, text style | Watch top organic content on that platform in the audience's country | Rebuild the first 3 s and rhythm for that platform; keep the concept |
| Different safe zones and UI | Preview on each | Compose for the most restrictive zone |
| Different audience and intent | Age/country mix | Different awareness stage or proof |
| Different metrics and attribution | Metric names, windows | Normalise with backend purchases by source |
| Sound-on habits differ | Hold with sound off | Burned-in captions on all |

## What to write in the report
Concept line, spend, impressions, hook, hold, CTR, visits, purchases, CPA, revenue per visitor, volume note, decision (scale, iterate, kill), the symptom row used, and next hypothesis with one change. State what could not be verified (tracking, windows, metric names).

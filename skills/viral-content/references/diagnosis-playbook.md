# Diagnosis playbook: symptom, likely causes, check, fix

Use it top-down. Step 0 first: a wrong denominator or one lucky post makes every branch meaningless. Thresholds here are **[F]** (practitioner starting points); your own last 10-20 posts replace them. Tags: **[C]** consensus or law, **[M]** serious but single or correlational, **[F]** practitioner or platform statement, **[X]** myth. Mechanism names (curiosity, expectation violation, transportation, social currency, utility) are defined in `SKILL.md` section 2.

## Step 0: is the evidence trustworthy?
| Check | How | If it fails |
|---|---|---|
| Which metric worries them | Reach, watch time, shares, follows or sales? Name one | Different symptoms have different trees; pick one |
| Platform and surface | Reels, TikTok, Shorts; Reel tab vs profile vs followers | Compare like with like; definitions differ (Shorts counts every start and replay since 31 Mar 2025, bib. 32) |
| Account age and size | Under about 30 posts or a few hundred followers: the system has little to learn from | Say "early data"; volume first, optimise later |
| Niche and audience | Who is the viewer, who is the follower, are they the same? | Off-niche reach explains "views but no follows" |
| Sample | At least 10 posts, same format and length range, same period | Under 10: do not conclude; review each post by hand |
| Posting time and promotion | Was any post boosted, cross-posted, or posted in an odd slot? | Remove boosted posts from the organic median |
| Median, not mean | Median of views over the sample; ratio best post / median | One outlier above about 5x the median is luck or a mechanism worth studying, not the norm |
| Definitions | "View" differs by platform; retention at 3 s may be "viewed past 3 s" or "stayed 3 s" | Write the definition beside every metric |
| Source | Native insights export vs a screenshot vs a third party | Prefer native export; note screenshots |
Worked example: 15 posts with views 180 to 400 have mean 279 and median 270; the best post is 1.5x the median. That is a flat account, not one with bad luck; the leak is systematic. If instead 14 posts sit near 250 and one reaches 90,000, the median is still 250: study the one hit for its mechanism, but plan with 250.

## Metric definitions (formulas and worked numbers)
| Metric | Formula | Worked example | Reads as |
|---|---|---|---|
| Hook rate (3-s hold) | viewers still watching at 3 s / plays | 4,200 / 10,000 = 42% | Did the opening stop them? Compare to your own median, not a global number |
| Average watch % | average watch time / video length | 18 s / 30 s = 60% | Pacing and payoff; can exceed 100% when videos loop or replay |
| Completion | views that reach the end / plays | 1,500 / 10,000 = 15% | Weaker for long videos; depends on length |
| Rewatch / loop rate | replays / plays (or average watch % above 100) | 2,000 / 10,000 = 20% | Short or looped videos; a strong signal where available |
| Shares per 1k views | shares / views x 1000 | 85 / 12,000 x 1000 = 7.1 | Social currency or utility |
| Saves per 1k views | saves / views x 1000 | 120 / 12,000 x 1000 = 10 | Utility, "later" value |
| Follows per 1k views | follows / views x 1000 | 30 / 24,000 x 1000 = 1.25 | Reason to follow; track against your own baseline |
| Profile visits per 1k | visits / views x 1000 | 60 / 24,000 x 1000 = 2.5 | Curiosity about you |
| Comments per 1k | comments / views x 1000 | 50 / 12,000 x 1000 = 4.2 | Participation; check sentiment |
No source read here gives universal good values; platforms say they weigh watching to the end, shares and likes (bib. 29, 30) but not how much. Read each post against your own median. Ratios on small bases are noisy: 3 shares on 400 views is 7.5 per 1k but one more share moves it by 2.5.

## Tree 1: views stuck low (for example 200-400 per post)
| Cause | Check | Fix |
|---|---|---|
| Few viewers get past the first seconds | Hook rate below your best posts, average watch under about 40% [F] | Rework the hook by mechanism (`playbooks.md` 1); one change per post |
| No clear topic or viewer | Can a stranger say in a sentence who it is for? | One viewer, one situation; stay in one niche for 10 posts |
| Post not eligible or restricted | Account status page, ineligible or recommendation limits (TikTok lists spam and under-review uploads as ineligible, bib. 30) | Fix the policy issue; do not repost the same file |
| Recycled or watermarked content | Other platform's mark, reposted clips | Re-make natively (`playbooks.md` 6) |
| Too little volume to learn | Under about 10 posts in a month | Raise cadence to what you can sustain; judge cadence by medians |
| Wrong length for the idea | Average watch % low and many viewers leave at a similar second | Cut to the beat that earns the second; see Tree 3 |
Do not conclude "shadow ban" **[X]** without a platform notice; first rule out Step 0 and the hook.

## Tree 2: drop in the first 3 s (hook)
Check: hook rate (3-s hold) below your median; the retention curve falls steeply before 3 s; the first frame is a logo, a title card, a greeting or a talking head without a reason.
| Cause | Fix |
|---|---|
| Opening does not violate any expectation or show a person or motion | Start on the strangest or most useful frame (the result, a contradiction, a question the viewer already has) |
| Promise unclear | One sentence on screen and in voice; concrete nouns and numbers |
| Slow start, intro, branding first | Cut to the first beat; logo at the end or as a corner mark |
| Hook and caption promise different things | Make the first 3 s deliver the caption's promise |
| Mismatch with the audience of the account | Test the hook with a person from the target niche, not a friend |
Test: change only the first 3 s on 3 similar posts, compare hook rate medians over a batch.

## Tree 3: good hook, drop mid-video (pacing, no open loop)
Check: hook rate normal, average watch % low, the curve has a cliff at a specific second.
| Cause | Fix |
|---|---|
| The question was answered too early, or never asked | Open a second question before closing the first; place the payoff after the middle |
| Slow stretch | Remove the sentence; cut pauses; add a change of scene, camera or caption at the cliff second |
| No stakes | State what the viewer gains or fears losing |
| Hook over-promises | Deliver a true, smaller promise (viewers leave and the system learns nothing good, bib. 29, 30) |
| Length not earned | Shorten to the shortest version that keeps the payoff |
Field-study link: the long videos in `field-study-10-reels.md` answer the previous question early and place the twist late, so the viewer always holds a pending question; that pattern is a hypothesis, not a rule.

## Tree 4: high views, no follows
Worked example: 1.8 million views and 40 follows is 0.022 follows per 1k views; the account's earlier posts were at 1.4 per 1k. The gap is the signal.
| Cause | Check | Fix |
|---|---|---|
| Off-niche audience | Audience demographics and comments differ from your target | Return to niche content; use the hit as an asset, not a template |
| One-off topic with nothing more to say | Profile has no similar posts | Make 3-5 follow-up pieces on the same idea |
| No reason to follow | The video ends with nothing promised next | Promise a series, a part 2, a recurring format |
| Profile is not a landing page | Bio unclear, grid unrelated | Rewrite bio in one line; pin 3 best posts (`virality-to-conversion.md`) |
| Content entertained but not related to you | Viewers liked the idea, not the creator | Add your voice or face and a point of view in the video |

## Tree 5: high views, no sales
Check the chain step by step (`virality-to-conversion.md`): follows per 1k, profile-visit to link click, click to purchase. If the profile clicks are fine and purchases are not, the issue is the offer and the page (`copywriting`, `offers`), not the video. If views are broad and entertainment-only, the audience may never have had the problem the product solves.

## Tree 6: low shares
| Cause | Fix |
|---|---|
| Nothing to pass on: no social currency (the sender looks no better) | Give a line, a fact or a feeling a viewer can use to look smart, funny or caring [M] |
| No utility | Add a concrete step, number or checklist worth sending to one person |
| Low arousal | Surprise, awe, humour or a bold position; not outrage for its own sake (arousal is a hypothesis, bib. 5, 6) |
| Too broad | Name a specific person or group in the hook so they tag each other |
| Call to action absent | Ask for one specific share ("send it to the person who...") once, without begging |

## Tree 7: one viral hit, then nothing
Causes: the hit came from a trend or a one-off topic; audience off-niche; no repeatable mechanism; the next posts changed format. Check which mechanism the hit used (hook, topic, format) and whether the next 5 posts repeated it. Fix: write the mechanism in a sentence, make 5 variants that keep it and change the topic, compare medians. Expect regression to the median: a few cascades grow large while most stay small (bib. 11).

## Tree 8: reach dropped suddenly
Check: change in posting, topic, length; reposts or watermarks; copyright or policy notice; a platform change (for example a new view definition, bib. 32); seasonality.
| Cause | Fix |
|---|---|
| Recycled or unoriginal content | Original footage and edit; remove foreign watermarks |
| Policy strike or limitation | Read the account status page; fix and wait |
| Music rights issue | Use licensed sounds for business accounts |
| Audience fatigue | New angle in the same niche; new format |
| Metric definition changed | Compare like with like only after the date of change |
Do not assume a penalty without evidence.

## Tree 9: negative comments
Read a sample of 50. Types: criticism of a claim (check the claim; correct publicly), confusion (the video promised something unclear), trolling (hide, do not feed), disagreement that fuels engagement (decide whether it fits your goal). Never delete valid corrections silently, never buy or fake comments.

## Tree 10: works on TikTok, not Reels (or the reverse)
Causes: different audience mix and age; the clip carries a watermark; length or pace suited to one platform; trending sounds not available on the business account; different default behaviours (Reels weigh reshares and the audio page, bib. 29). Check native insights per platform, not total views. Fix: native export and a small edit for each platform (`playbooks.md` 6), test one platform-specific change at a time.

## What you could not verify
List it every time: sample size, platform definition, any boosted posts, whether audience demographics were checked, and the fact that platform weights are not public.

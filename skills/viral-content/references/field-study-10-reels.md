# Field study: 10 vertical videos above 1 million views, read for mechanisms

Purpose: worked examples of WHY people stop, stay, vote, share and follow, not templates to imitate. A format copied without its mechanism does not transfer: the countdown, the caption style or the "you choose" ending only work here because of what they make the viewer feel and want to know. Read `SKILL.md` section 2 first for the mechanism names.

## Method and limits (read before using any number)
- Sample: 10 portrait videos (720x1280, 56 to 136 s), each reported above 1 million views, from one account in one niche (interactive serial fiction, Portuguese, animated, synthetic-looking narration). View counts were given by the owner, not re-checked. Nothing about watch time, shares, follows or reach was available.
- Measured by me: duration (ffprobe), scene-change count (ffmpeg `select='gt(scene,0.3)'`), a 6-frame hook strip (0, 0.5, 1, 1.5, 2, 3 s) viewed for all 10, an arc strip (12 frames) viewed for 1 (video 01; the others were left unviewed to save budget, so on-screen text beyond the first 3 s is from the transcript and the first video's arc), and speech-to-text with Whisper `base` (Portuguese; it mis-hears names and words, so beats are paraphrased, not quoted).
- Cuts per 10 s is a floor: animated scenes with only caption changes do not trigger the 0.3 scene threshold, and captions change about every half second in all 10.
- 10 winners, one niche, no losers: survivorship bias. Patterns below are hypotheses to test on your own account, never causes. I also cannot separate the effect of the format from the effect of the account's existing audience, posting history or paid promotion (unknown).
- No account or person is named. Episodes are labelled by series part. Video 05 is a different kind of piece (explainer and offer); the other nine are story episodes (parts 9, 8, 7, 6, 5, 4, 3, 2, 1 in that file order, newest first).

## Per-video table
| # | Part | Length | Cuts / 10 s | First 1-3 s hook | On-screen text | Voice | Beats and payoff timing | Loop? | CTA |
|---|---|---|---|---|---|---|---|---|---|
| 01 | 9 | 136 s | 3.8 | Counter falling from billions to 1 over a crowd, "all men vanished, except you" | Episode tag, counter, word-by-word captions (key words in colour) | Voice, second person | Recap of the audience's last choice (0-20 s), chase and hiding (20-110 s), twist at about 110 s (a hidden signal gives them away), new fork at the end | No loop; open loop to next part | Implicit: pick left or right in comments |
| 02 | 8 | 98 s | 4.7 | Same counter and line, new setting | Same system | Voice | Last choice resolved (0-15 s), phone call from the missing father (about 20 s), threat arrives (about 60 s), fork | No; series | Implicit vote |
| 03 | 7 | 80 s | 4.9 | Same | Same | Voice | Choice resolved: painful surgery (0-45 s), reveal of a tracker (about 50 s), ringing phone, fork "answer or destroy" | No; series | Implicit vote |
| 04 | 6 | 130 s | 2.5 | Same | Same | Voice | Result of the vote, a letter and photo (about 10 s), shooting chase (20-80 s), wound twist, fork | No; series | Implicit vote |
| 05 | explainer | 56 s | 5.0 | Phone mockups of four episodes plus "you vote, the story changes" | Large captions, then a fake chat bubble asking how it is made | Voice, first person | Promise (0-3 s), question from viewers (about 6 s), honest reveal that AI tools do the production (about 12 s), results claim, kit offer, price and date at the end | No | Link in bio, dated launch price, "message me if you get stuck" |
| 06 | 5 | 90 s | 2.2 | Same counter | Same | Voice | Trust-or-not recap, roadblock (about 25 s), letter and photo twist (about 70 s), five-second decision | No; series | Vote, with a time limit stated |
| 07 | 4 | 114 s | 2.4 | Same | Same | Voice | Social proof in the recap ("over 120 thousand votes"), car through a police line (about 30 s), call from mother turns suspicious (about 100 s), ten-second decision | No; series | Vote |
| 08 | 3 | 120 s | 2.0 | Same | Same | Voice | Recap with vote count and speed (about 15 s), ship and a childhood nickname (about 25 s), engine that will not start x3, stranger in the back seat (about 105 s) | No; series | Vote |
| 09 | 2 | 96 s | 3.0 | Same counter but opens with "imagine" | Same | Voice | Disguise and drones (0-50 s), the port at night (about 80 s), fork | No; series | Vote |
| 10 | 1 | 119 s | 3.9 | Notification counter rising on a man on a sofa, "imagine" | Location and time stamp, counter, captions | Voice | Premise, then numbered survival rules (phone, disguise), anonymous note (about 105 s), "what would you do" repeated | No; open loop | Question to the audience |

## Cross-video patterns (counts out of 10, or of the 9 story episodes where stated)
1. 9/10 open with an unmistakable "something impossible, and it is you" frame within 3 s, built on a counter that moves (8 falling to "1", 1 rising). Mechanism: expectation violation plus a number that cannot be ignored; see section 1 below.
2. 8/9 story episodes (all but part 1) start by re-stating the audience's earlier choice, and 2 of them add a vote count or speed ("over 100 thousand"). Mechanism: social proof and ownership (people see their input mattered).
3. 9/10 end on a forced binary choice or direct question to the viewer; 4 of the 9 add a stated time limit ("five seconds"). Mechanism: unresolved decision, commitment, comment production.
4. 10/10 are narrated speech with word-by-word burned-in captions, 9/10 in second person present tense ("you, ...", "imagine").
5. 7/10 are 90 s or longer (median 97 s; only 05 and 03 are under 85 s); no video is a seamless loop (0/10). The replay incentive is the next part, not the loop.
6. Cuts per 10 s range from 2.0 to 5.0 (median 3.4); the faster pieces are the shortest (05, 03, 02). Do not read this as an ideal rate.
7. 1/10 (video 05) is a conversion piece: first-person, discloses that AI tools make the series, states reach results, sells a kit with a dated launch price. It reuses the same hook idea (a promise and a participation line) and a plain call to action. Used in `virality-to-conversion.md`.
8. 10/10 use the same visual system (episode tag, fixed caption position, same hook line). Repetition makes the series recognisable in under a second.

## Which mechanism each video shows, and where
Mechanism names and evidence tags are defined in `SKILL.md` section 2 and cited in `BIBLIOGRAPHY.md`. Evidence here means evidence for the mechanism in general; whether it caused these views is untested.

### 1. Stop: expectation violation, salient motion
- Seen at 0-3 s in 01-04, 06-09: a peaceful crowd and a counter that collapses to 1 while a caption builds the sentence word by word. A moving number and a changing caption give the eye something to follow, and the sentence is a violation of what the viewer expects from a street scene. [M] (surprise attracts attention in lab models; the effect size in feeds is unknown).
- In 10: a rising notification counter over a sleeping character, the start of an alarm.
- Test: cover your first 3 s with your hand; does a stranger know what is odd, and is something moving?

### 2. Stay: curiosity gap, open loops
- The unanswered thing is stated early: who is hunting him, who is on the phone, who is in the back seat. Each episode closes one question and opens the next. Curiosity as a gap between what you know and what you want to know is well supported in lab work [M-C]; the "unfinished task is remembered" (Zeigarnik) account is weaker, with mixed replications (see bibliography), so I treat it as a hypothesis.
- Payoff placement: the first answer comes in the first 10 to 20 s (the result of the previous vote), the main twist at roughly 60-85 percent of the length, a new question in the last seconds. That spacing is the pattern, not the exact seconds. The 56 s explainer shows its answer ("it is AI tools") at about 12 s.

### 3. Finish: narrative transportation
- Second person plus present tense plus continuous voice puts the viewer inside the story. Being absorbed in a narrative lowers counter-arguing and raises engagement [M]. Cuts are modest (median 3.4 per 10 s) and the voice carries the story, which matches a story-first design, not a visual-spectacle one.

### 4. Share and comment: arousal, agency, social currency
- Danger and betrayal scenes are high-arousal; high-arousal emotion is associated with sharing in observational data [M]. The binary choice turns viewers into participants: commenting is cheap and public, and the recap rewards those who voted. Whether comments or shares drove reach here is unknown.
- Sending a friend "which one would you choose" is also self-presentation (social currency) [M]; untested here.

### 5. Rewatch and return: peak-end, fluency, repetition
- Each episode ends at a peak (tension plus decision), so the ending is what viewers carry to the next part [M]. The identical opening and layout make the series fluent to process, and repeat exposure raises familiarity [M].

### 6. Follow: promise of a series, parasocial voice
- A new part every couple of days (stated in 05) is a concrete reason to follow, more than a "follow for more". The first-person creator voice in 05 builds a one-to-one feel (parasocial) [M].

### 7. Buy: video 05 only
- A reach piece with a participation hook, then an honest "how it is made" curiosity payoff, evidence of results, and a low-ticket product with a deadline. The deadline must be a real one, and the claim "one person and AI tools" is disclosed. See `virality-to-conversion.md` for the path and the metrics to track.

## Using this study
1. Name the mechanism in each beat of your own script before you choose a format.
2. Test one mechanism at a time across a batch of 8-10 posts and compare medians (`playbooks.md` section 5).
3. Treat counts here as prompts for your hypotheses: "do my pieces that re-state a prior choice hold the first 10 s better?"

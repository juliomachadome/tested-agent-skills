# Laws of UX, Nielsen heuristics and severity

## Contents
1. How to use laws
2. Laws of UX with limits
3. Myths and weak evidence
4. Nielsen's 10 heuristics as design rules
5. Severity scale (0-4)
6. Concepts from the classics
7. Sources

## 1. How to use laws
A law is an argument, not proof. State which law you apply, what it predicts for this screen, and what would falsify it. If a usability test disagrees, trust the test. Laws describe tendencies in studies that often come from narrow populations and tasks, so keep claims proportional.

## 2. Laws of UX with limits
Definitions follow the lawsofux.com catalogue (30 entries, read 2026-11-15). The "limit" column is where the law misleads.

| Law | Says | Apply as | Limit: when it misleads |
|---|---|---|---|
| Hick's Law | Decision time grows with number and complexity of choices | One primary action; mark the recommended option; split long forms into steps | Applies to choosing among comparable options. In an ordered, familiar list (countries, alphabetical) many items are fine. Hiding a needed option behind a menu "to reduce choices" slows people. The site itself warns against over-simplifying |
| Fitts's Law | Time to reach a target depends on distance and size | Big primary action near where the hand is; destructive action smaller and away from it | "Thumb zone" heat maps come from observational data on 2013-era phones; weak evidence. Safe takeaway: main action large, nothing important in corners |
| Miller's Law | Working memory holds roughly 7 plus or minus 2 items | Chunk phone numbers, group lists into sections, never make people remember data from a previous screen | Does not mean "menus have at most 7 items". Miller (1956) is about immediate memory span; later estimates are nearer 4 chunks (Cowan 2001, cited by lawsofux) |
| Jakob's Law | People spend most time on other products and expect yours to work alike | Use platform conventions: close at top corner, logo goes home, back goes back | Innovate in content, not in controls. Convention can lock in a bad pattern: break it only with a tested gain |
| Doherty Threshold | Productivity rises when system and person respond within about 400 ms | Visible reaction to every input under 400 ms; skeletons; optimistic UI | A guideline from a 1982 study; for long work it does not apply, use the NN/g limits (0.1/1/10 s) |
| Tesler's Law | Every system has complexity that cannot be removed, only moved | Let the system carry it: default, calculate, remember, prefill | Over-simplifying pushes complexity onto the person (one free-text field for a whole address) |
| Peak-End Rule | Experiences are judged by the most intense moment and the end | Care about the worst moment (waiting without feedback) and the last screen | A memory effect; it does not excuse a mediocre middle |
| Goal-Gradient Effect | Effort rises as the goal nears | Visible progress, "2 left", a bar that does not start at zero | Fake progress is deception; bars that stall destroy trust |
| Zeigarnik Effect | Unfinished tasks are remembered better | "Continue where you left off", show what is missing | Replications of the original effect are inconsistent. Use as a product hint, not a fact |
| Von Restorff Effect | The item that differs is remembered | Reserve the accent color for the primary action | If everything stands out, nothing does |
| Postel's Law | Be liberal in what you accept | Accept spaces, case, phone and date formats; normalize | Do not accept ambiguous input silently when the wrong reading has a cost: echo back the interpretation |
| Aesthetic-Usability Effect | Attractive designs are judged easier to use | Polish buys tolerance for small problems | Hides problems in tests: people praise and still fail the task. Judge by task success |
| Proximity, Common Region, Similarity, Uniform Connectedness, Prägnanz | Near, enclosed, alike or connected things read as a group; ambiguous shapes read in the simplest form | Less space inside a group than between groups; a card or background to group | Over-boxing (a border around everything) adds noise; spacing alone often groups better |
| Serial Position Effect | First and last items are remembered best | Most important items at the ends of a tab bar or list | Does not apply to long scrollable content people scan by keyword |
| Choice Overload | Too many options can paralyze | Fewer plans, a default | Effect size varies widely between studies; never promise a number |
| Cognitive Load | Mental effort to use the interface | Remove what does not serve the task; recognize over recall | Not all load is bad: a necessary check on a legal act is useful load |
| Paradox of the Active User | People skip manuals and start using | Teach in context, not in a tour at the door | Does not mean no help: help must be where the task is |
| Flow | Deep focus during an activity | Do not interrupt a focused task with modals or upsells | A state, not a feature; do not engineer it with streak pressure |
| Pareto Principle | A few causes drive most effects | Optimize the common path first | A heuristic ratio, not a measurement of your product; check your data |
| Selective Attention, Mental Model, Cognitive Bias, Occam's Razor, Parkinson's Law, Working Memory | See lawsofux.com | Use as vocabulary in a critique, then reduce to a concrete change | Naming a bias is not a finding; the finding is what the person does on the screen |

## 3. Myths and weak evidence
| Claim | Status | Do instead |
|---|---|---|
| Menus/lists have at most 7 items | myth | Group; the limit is memory, not what is on screen |
| Everything within 3 clicks | myth | Count moments of doubt, not clicks |
| Thumb zone forbids the top of the screen | weak | Primary action low, content central, avoid corners |
| Hick says always cut options | weak | Cut the unnecessary, organize the necessary |
| Zeigarnik proves incomplete tasks engage | weak | Show progress because it orients, not for a promised effect |
| Button color X converts better | myth | Contrast with surroundings and a clear label |
| Users do not scroll | myth | They scroll, attention falls below the fold: essentials up top |
| Icons are universal | myth | Visible label unless truly universal (search, close, send) |
| Placeholder can serve as label | myth | Fixed label above the field |
| A 7-day streak causes course completion | correlation | Do not sell it as cause |

## 4. Nielsen's 10 heuristics as design rules
Names as published by NN/g (first published 1994, page last reviewed Jan 30, 2024; read 2026-11-15).

1. **Visibility of system status**: say what is happening, in time (loading, saved, step 2 of 5).
2. **Match between the system and the real world**: the person's words, not internal terms.
3. **User control and freedom**: exit, undo, back, always.
4. **Consistency and standards**: same word and place for the same thing; platform conventions.
5. **Error prevention**: constraints, safe defaults, confirmation before the irreversible.
6. **Recognition rather than recall**: options and instructions visible or retrievable.
7. **Flexibility and efficiency of use**: shortcuts for people who return (continue, repeat, keyboard).
8. **Aesthetic and minimalist design**: each extra item competes with what matters.
9. **Help users recognize, diagnose, and recover from errors**: plain language, say what and how to fix.
10. **Help and documentation**: short, in the task, in the same place.

Use them as a walk-through order in a heuristic evaluation, and map each finding to one heuristic.

## 5. Severity scale (0-4)
From NN/g "How to Rate the Severity of Usability Problems" (read 2026-11-15):

| Score | Meaning (NN/g wording) |
|---|---|
| 0 | I do not agree that this is a usability problem at all |
| 1 | Cosmetic problem only: need not be fixed unless extra time is available |
| 2 | Minor usability problem: low priority |
| 3 | Major usability problem: important to fix, high priority |
| 4 | Usability catastrophe: imperative to fix before release |

Rate with three factors: **frequency** (how often people meet it), **impact** (how hard it is to get past) and **persistence** (whether people learn to avoid it or are caught again and again). Add market impact when a problem hurts adoption even if it is easy to overcome. Rate each problem alone; rate more than one evaluator's view when possible and average, since single raters are unreliable.

## Sources
- https://lawsofux.com/ (catalogue and definitions; read 2026-11-15)
- https://www.nngroup.com/articles/ten-usability-heuristics/ (read 2026-11-15)
- https://www.nngroup.com/articles/how-to-rate-the-severity-of-usability-problems/ (read 2026-11-15)
- Bibliography with books, editions and read dates: `BIBLIOGRAPHY.md`.
- Miller 1956 and Cowan 2001 as cited on lawsofux.com; the thumb-zone and gamification claims in section 3 come from the study notes behind this skill (not re-verified).

# Bibliography: ux-design

Checked 18/11/2026. Status: **V** = identity matched to the ISBN in OpenLibrary (`https://openlibrary.org/isbn/<isbn>.json`) this pass; **P** = official page opened and the relevant text read this pass (for papers, the Crossref landing record matched title, authors, venue, year; paper text not read); **S** = exists, text not read; **U** = not verified. Nothing is quoted; ideas are restated. Pages that need JavaScript (Apple, Material) were read through an isolated browser pass. Contrast and target-size numbers follow WCAG 2.2; WCAG 3.0 is a draft and does not replace it.

## Books
1. Krug, S. *Don't Make Me Think, Revisited*. New Riders (Pearson), 2014. ISBN 978-0321965516. **V**. Supports: Self-evident screens, scanning not reading, count doubts not clicks; product-types README.
2. Norman, D. *The Design of Everyday Things, revised and expanded*. Basic Books, 2013. ISBN 978-0465050659. **V**. Supports: Signifiers, feedback, conceptual models, slips vs mistakes, forcing functions.
3. Cooper, A., Reimann, R., Cronin, D., Noessel, C. *About Face: The Essentials of Interaction Design (4th ed.)*. Wiley, 2014. ISBN 978-1118766576. **V**. Supports: Goal-directed design, personas, expert users (saas-b2b, developer-tools).
4. Yablonski, J. *Laws of UX, 1st ed.*. O'Reilly, 2020. ISBN 978-1492055310. **V**. Supports: Psychology-based heuristics (`laws-and-heuristics.md`).
5. Yablonski, J. *Laws of UX, 2nd ed.*. O'Reilly, 2024. ISBN 978-1098146962. **V**. Supports: Same, second edition (catalogue shows 2024).
6. Rubin, J., Chisnell, D. *Handbook of Usability Testing, 2nd ed.*. Wiley, 2008. ISBN 978-0470185483. **V**. Supports: Test plan, tasks, moderating, reporting (`playbooks.md` 1).
7. Sauro, J., Lewis, J.R. *Quantifying the User Experience, 2nd ed.*. Elsevier (Morgan Kaufmann), 2016. ISBN 978-0128023082. **V**. Supports: Intervals for small samples, task success and time, SUS (`diagnosis-playbook.md` 2).
8. Hall, E. *Just Enough Research*. A Book Apart, 2013. ISBN 978-1937557102. **V**. Supports: Cheap research choices, interviews.
9. Rosenfeld, L., Morville, P., Arango, J. *Information Architecture: For the Web and Beyond, 4th ed.*. O'Reilly, 2015. ISBN 978-1491911686. **V**. Supports: Organization, labeling, navigation, search systems (`playbooks.md` 5). Catalogue lists the first author only; the co-authors are from the book's cover, not the catalogue.
10. Brooke, J. *SUS: a quick and dirty usability scale, in Jordan, Thomas, McClelland, Weerdmeester (eds), Usability Evaluation in Industry*. Taylor & Francis, 1996. ISBN 978-0748404605. **V**. Supports: SUS origin; the catalogue shows the book and its editor, not the chapter author, so the chapter attribution is not machine-checked; scoring is confirmed on the MeasuringU page (entry below).
11. Tullis, T., Albert, B. *Measuring the User Experience, 2nd ed.*. Elsevier, 2013. ISBN 978-0124157811. **V**. Supports: Usability metrics (catalogue lists the first author only).
12. Garrett, J.J. *The Elements of User Experience*. New Riders, 2010. ISBN 978-0321683687. **V**. Supports: Five planes from strategy to surface.
13. Portigal, S. *Interviewing Users*. Rosenfeld Media, 2013. ISBN 978-1933820118. **V**. Supports: Interview technique.
14. Fitzpatrick, R. *The Mom Test*. CreateSpace, 2014. ISBN 978-1492180746. **V**. Supports: Asking about behavior, not opinions (discovery goes to `product-management`).
15. Wroblewski, L. *Web Form Design: Filling in the Blanks*. Rosenfeld Media, 2008. ISBN 978-1933820255. **V**. Supports: Form layout and labels (older research, check against Baymard).
16. Gothelf, J., Seiden, J. *Lean UX*. O'Reilly, 2016 (catalogue edition; first edition 2013). ISBN 978-1491953600. **V**. Supports: Hypotheses and outcomes; catalogue lists the first author only.
17. Torres, T. *Continuous Discovery Habits*. Product Talk, 2021. ISBN 978-1736633304. **V**. Supports: Weekly customer touchpoints (routing to `product-management`).
18. Tidwell, J., Brewer, C., Valencia, A. *Designing Interfaces, 3rd ed.*. O'Reilly, 2020. ISBN 978-1492051961. **V**. Supports: Interface pattern catalogue.

## Papers
19. Nielsen, J., Landauer, T.K. A mathematical model of the finding of usability problems. Proc. CHI '93, 1993. https://doi.org/10.1145/169059.169166 . **P** (landing page). Supports: Crossref landing record matched title, authors, venue, year; text not read. The 31% value and the 5-user curve are read on the NN/g article (entry below).
20. Gray, C.M., Kou, Y., Battles, B., Hoggatt, J., Toombs, A.L. The Dark (Patterns) Side of UX Design. Proc. CHI 2018, 2018. https://doi.org/10.1145/3173574.3174108 . **P** (landing page). Supports: Taxonomy of dark patterns (`diagnosis-playbook.md` 3.11).
21. Mathur, A., Acar, G., Friedman, M., Lucherini, E., Mayer, J., Chetty, M., Narayanan, A. Dark Patterns at Scale. Proc. ACM HCI (CSCW) 3, 2019. https://doi.org/10.1145/3359183 . **P** (landing page). Supports: Crawl of shopping sites for dark patterns; the share figure is not re-read.

## NN/g articles (nngroup.com/articles/...)
22. NN/g. 10 Usability Heuristics for User Interface Design. https://www.nngroup.com/articles/ten-usability-heuristics/ . **P** 18/11/2026. Supports: The ten heuristics.
23. NN/g. Why You Only Need to Test with 5 Users. https://www.nngroup.com/articles/why-you-only-need-to-test-with-5-users/ . **P** 18/11/2026. Supports: L = 31% typical, 5 users find about 85%, test again after fixing.
24. NN/g. How Many Test Users in a Usability Study?. https://www.nngroup.com/articles/how-many-test-users/ . **P** 18/11/2026. Supports: Quantitative 20+, card sorting 15+, 3 per group for a mixed audience.
25. NN/g (Nielsen). Severity Ratings for Usability Problems. https://www.nngroup.com/articles/how-to-rate-the-severity-of-usability-problems/ . **P** 18/11/2026. Supports: 0-4 scale: frequency, impact, persistence.
26. NN/g. Thinking Aloud: The #1 Usability Tool. https://www.nngroup.com/articles/thinking-aloud-the-1-usability-tool/ . **P** 18/11/2026. Supports: Think-aloud, neutral prompts, bias.
27. NN/g. Task Scenarios for Usability Testing. https://www.nngroup.com/articles/task-scenarios-usability-testing/ . **P** 18/11/2026. Supports: Realistic scenarios that do not give away the interface.
28. NN/g. Usability (User) Testing 101. https://www.nngroup.com/articles/usability-testing-101/ . **P** 18/11/2026. Supports: Test structure.
29. NN/g. Quantitative vs. Qualitative Usability Testing. https://www.nngroup.com/articles/quant-vs-qual/ . **P** 18/11/2026. Supports: When rates need larger samples.
30. NN/g. Success Rate: The Simplest Usability Metric. https://www.nngroup.com/articles/success-rate-the-simplest-usability-metric/ . **P** 18/11/2026. Supports: Partial credit; small tests lack tight intervals.
31. NN/g (Laubheimer). Beyond NPS: SUS, NASA-TLX, and the Single Ease Question. https://www.nngroup.com/articles/measuring-perceived-usability/ . **P** 18/11/2026. Supports: SUS average 68 from 500 studies; SEQ.
32. NN/g. Card Sorting: Uncover Users' Mental Models. https://www.nngroup.com/articles/card-sorting-definition/ . **P** 18/11/2026. Supports: Open and closed sorts; 15+ participants for the quantitative approach.
33. NN/g. Tree Testing: Evaluate Menu Labels and Categories. https://www.nngroup.com/articles/tree-testing/ . **P** 18/11/2026. Supports: Task-based tree tests; qualitative vs quantitative.
34. NN/g. How to Conduct a Heuristic Evaluation. https://www.nngroup.com/articles/how-to-conduct-a-heuristic-evaluation/ . **P** 18/11/2026. Supports: Evaluator procedure.
35. NN/g (Nielsen). Usability Problems Found by Heuristic Evaluation. https://www.nngroup.com/articles/usability-problems-found-by-heuristic-evaluation/ . **P** 18/11/2026. Supports: Opened; aggregation figures not read in detail.
36. NN/g. Design Critiques: Encourage a Positive Culture. https://www.nngroup.com/articles/design-critiques/ . **P** 18/11/2026. Supports: Facilitator, scope and agenda.
37. NN/g. Journey Mapping 101. https://www.nngroup.com/articles/journey-mapping-101/ . **P** 18/11/2026. Supports: Journey maps.
38. NN/g. User Interviews 101. https://www.nngroup.com/articles/user-interviews/ . **P** 18/11/2026. Supports: Interview basics.
39. NN/g. Mental Models and User Experience Design. https://www.nngroup.com/articles/mental-models/ . **P** 18/11/2026. Supports: Mental models.
40. NN/g. Information Scent. https://www.nngroup.com/articles/information-scent/ . **P** 18/11/2026. Supports: Labels carry the target words.
41. NN/g (Nielsen). Progressive Disclosure. https://www.nngroup.com/articles/progressive-disclosure/ . **P** 18/11/2026. Supports: Two levels, scent of the reveal control.
42. NN/g (Nielsen). Response Time Limits. https://www.nngroup.com/articles/response-times-3-important-limits/ . **P** 18/11/2026. Supports: 0.1 / 1 / 10 s.
43. NN/g. The Need for Speed, 23 Years Later. https://www.nngroup.com/articles/the-need-for-speed/ . **P** 18/11/2026. Supports: Perceived speed context.
44. NN/g. Skeleton Screens 101. https://www.nngroup.com/articles/skeleton-screens/ . **P** 18/11/2026. Supports: Skeletons for 2-10 s, progress bars beyond 10 s.
45. NN/g (Sherwin). Progress Indicators Make a Slow System Less Insufferable. https://www.nngroup.com/articles/progress-indicators/ . **P** 18/11/2026. Supports: Looped vs percent-done indicators.
46. NN/g. Confirmation Dialogs Can Prevent User Errors. https://www.nngroup.com/articles/confirmation-dialog/ . **P** 18/11/2026. Supports: Confirm sparingly, name the effect.
47. NN/g (Laubheimer). Preventing User Errors: Avoiding Conscious Mistakes. https://www.nngroup.com/articles/user-mistakes/ . **P** 18/11/2026. Supports: Slips vs mistakes, previews, undo.
48. NN/g. 10 Design Guidelines for Reporting Errors in Forms. https://www.nngroup.com/articles/errors-forms-design-guidelines/ . **P** 18/11/2026. Supports: Form error guidelines.
49. NN/g. Placeholders in Form Fields Are Harmful. https://www.nngroup.com/articles/form-design-placeholders/ . **P** 18/11/2026. Supports: Placeholder is not a label.
50. NN/g. Website Forms Usability: Top 10 Recommendations. https://www.nngroup.com/articles/web-form-design/ . **P** 18/11/2026. Supports: Form recommendations.
51. NN/g. Designing Empty States in Complex Applications. https://www.nngroup.com/articles/empty-state-interface-design/ . **P** 18/11/2026. Supports: Empty-state guidelines.
52. NN/g. Data Tables: Four Major User Tasks. https://www.nngroup.com/articles/data-tables/ . **P** 18/11/2026. Supports: Table tasks.
53. NN/g. Touch Targets on Touchscreens. https://www.nngroup.com/articles/touch-target-size/ . **P** 18/11/2026. Supports: 1 cm by 1 cm minimum.
54. NN/g. Mobile User Experience: Limitations and Strengths. https://www.nngroup.com/articles/mobile-ux/ . **P** 18/11/2026. Supports: Mobile context.
55. NN/g. 3 Design Considerations for Effective Mobile-App Permission Requests. https://www.nngroup.com/articles/permission-requests/ . **P** 18/11/2026. Supports: Ask in context, explain purpose.
56. NN/g (Kendrick). Five Mistakes in Designing Mobile Push Notifications. https://www.nngroup.com/articles/push-notification/ . **P** 18/11/2026. Supports: Ask after value, categories, settings, bursts.
57. NN/g. Onboarding Tutorials vs. Contextual Help. https://www.nngroup.com/articles/onboarding-tutorials/ . **P** 18/11/2026. Supports: Contextual help beats up-front tutorials.
58. NN/g. UX Writing: Study Guide. https://www.nngroup.com/articles/ux-writing-study-guide/ . **P** 18/11/2026. Supports: UX writing basics.
59. NN/g. Search: Visible and Simple. https://www.nngroup.com/articles/search-visible-and-simple/ . **P** 18/11/2026. Supports: Search box placement.
60. NN/g. Site Search Suggestions. https://www.nngroup.com/articles/site-search-suggestions/ . **P** 18/11/2026. Supports: Search suggestions.
61. NN/g. Deceptive Patterns in UX: How to Recognize and Avoid Them. https://www.nngroup.com/articles/deceptive-patterns/ . **P** 18/11/2026. Supports: Coined by Brignull 2010; examples.
62. NN/g (Samsonov). AI Chatbots Discourage Error Checking. https://www.nngroup.com/articles/ai-chatbots-discourage-error-checking/ . **P** 18/11/2026. Supports: Verification cost, halo effect, citations.
63. NN/g. Prompt Controls in GenAI Chatbots. https://www.nngroup.com/articles/prompt-controls-genai/ . **P** 18/11/2026. Supports: Prompt controls.
64. NN/g. The 6 Types of Conversations with Generative AI. https://www.nngroup.com/articles/ai-conversation-types/ . **P** 18/11/2026. Supports: Conversation types.

## Other open web sources
65. Baymard. Checkout Optimization: Minimize Form Fields. https://baymard.com/blog/checkout-flow-average-form-fields . **P** 18/11/2026. Supports: 2024 average 11.3 fields, 5.1 steps.
66. Baymard. Cart Abandonment Rate: 50 Statistics. https://baymard.com/lists/cart-abandonment-rate . **P** 18/11/2026. Supports: Average 70.22%; reasons list (extra costs, forced account, complexity, errors).
67. Baymard. Usability Testing of Inline Form Validation. https://baymard.com/blog/inline-form-validation . **P** 18/11/2026. Supports: Avoid premature validation, remove error when fixed, positive validation.
68. Baymard. Search UX: 5 Proven Strategies for Improving No Results Pages. https://baymard.com/blog/no-results-page . **P** 18/11/2026. Supports: No-results pages need new routes.
69. Baymard. Ecommerce Search UX Best Practices. https://baymard.com/blog/ecommerce-search-query-types . **P** 18/11/2026. Supports: Search issues across top sites.
70. Baymard. Always Collapse Completed Accordion Checkout Steps into Summaries. https://baymard.com/blog/accordion-checkout-usability . **P** 18/11/2026. Supports: Step summaries.
71. MeasuringU. Measuring Usability with the System Usability Scale (SUS). https://measuringu.com/sus/ . **P** 18/11/2026. Supports: Scoring: odd minus 1, even 5 minus, sum times 2.5; mean 68.
72. deceptive.design (Brignull). Deceptive Patterns. https://www.deceptive.design/ . **P** 18/11/2026. Supports: Types, addictive design, laws.
73. Yablonski. Laws of UX site. https://lawsofux.com/ . **P** 18/11/2026. Supports: Laws catalogue.
74. Mozilla MDN. inputmode HTML global attribute. https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Global_attributes/inputmode . **P** 18/11/2026. Supports: Keyboard hints.
75. GOV.UK Design System. Recover from validation errors. https://design-system.service.gov.uk/patterns/validation/ . **P** 18/11/2026. Supports: Validation pattern.
76. Google PAIR. Errors + Graceful Failure. https://pair.withgoogle.com/chapter/errors-failing/ . **P** 18/11/2026. Supports: Error types and recovery.
77. Google PAIR. Explainability + Trust. https://pair.withgoogle.com/chapter/explainability-trust/ . **P** 18/11/2026. Supports: Calibrating trust.
78. Google PAIR. Mental Models. https://pair.withgoogle.com/chapter/mental-models/ . **P** 18/11/2026. Supports: Setting expectations.
79. Apple. Human Interface Guidelines: Accessibility (browser pass). https://developer.apple.com/design/human-interface-guidelines/accessibility . **P** 18/11/2026. Supports: 44x44 pt hit regions.
80. Google. Material Design 3: Accessibility designing (browser pass). https://m3.material.io/foundations/designing/structure . **P** 18/11/2026. Supports: Touch targets at least 48x48 dp, about 9 mm.
81. Fogg, B.J.. Fogg Behavior Model. https://behaviormodel.org/ . **P** 18/11/2026. Supports: Motivation, ability, prompts (page opened, motivation text read).
82. Microsoft. Inclusive Design. https://inclusive.microsoft.design/ . **P** 18/11/2026. Supports: Recognize exclusion, learn from diversity (three principles read).
83. Frost, B.. Atomic Design, chapter 2. https://atomicdesign.bradfrost.com/chapter-2/ . **P** 18/11/2026. Supports: Atoms, molecules, organisms, templates, pages.
84. Wathan, A., Schoger, S.. Refactoring UI (book site). https://www.refactoringui.com/ . **P** 18/11/2026. Supports: Book site opened; authors read; book text not read.

## W3C: WCAG 2.2, Understanding pages, ARIA APG
85. W3C. WCAG 2.2 (Recommendation). https://www.w3.org/TR/WCAG22/ . **P** 18/11/2026. Supports: AA criteria.
86. W3C. Understanding 2.1.1 Keyboard. https://www.w3.org/WAI/WCAG22/Understanding/keyboard.html . **P** 18/11/2026. Supports: Keyboard operation.
87. W3C. Understanding 2.4.3 Focus Order. https://www.w3.org/WAI/WCAG22/Understanding/focus-order.html . **P** 18/11/2026. Supports: Focus order.
88. W3C. Understanding 2.4.11 Focus Not Obscured (Minimum). https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html . **P** 18/11/2026. Supports: Sticky bars and focus.
89. W3C. Understanding 2.5.8 Target Size (Minimum). https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html . **P** 18/11/2026. Supports: 24 by 24 CSS px.
90. W3C. Understanding 2.5.7 Dragging Movements. https://www.w3.org/WAI/WCAG22/Understanding/dragging-movements.html . **P** 18/11/2026. Supports: Single-pointer alternative.
91. W3C. Understanding 3.3.1 Error Identification. https://www.w3.org/WAI/WCAG22/Understanding/error-identification.html . **P** 18/11/2026. Supports: Errors in text.
92. W3C. Understanding 3.3.3 Error Suggestion. https://www.w3.org/WAI/WCAG22/Understanding/error-suggestion.html . **P** 18/11/2026. Supports: Suggest corrections.
93. W3C. Understanding 3.3.7 Redundant Entry. https://www.w3.org/WAI/WCAG22/Understanding/redundant-entry.html . **P** 18/11/2026. Supports: Do not ask twice.
94. W3C. Understanding 3.3.8 Accessible Authentication (Minimum). https://www.w3.org/WAI/WCAG22/Understanding/accessible-authentication-minimum.html . **P** 18/11/2026. Supports: No cognitive test only.
95. W3C. Understanding 3.2.6 Consistent Help. https://www.w3.org/WAI/WCAG22/Understanding/consistent-help.html . **P** 18/11/2026. Supports: Help in a consistent place.
96. W3C. Understanding 3.3.2 Labels or Instructions. https://www.w3.org/WAI/WCAG22/Understanding/labels-or-instructions.html . **P** 18/11/2026. Supports: Labels.
97. W3C. Understanding 1.3.1 Info and Relationships. https://www.w3.org/WAI/WCAG22/Understanding/info-and-relationships.html . **P** 18/11/2026. Supports: Structure in markup.
98. W3C. Understanding 1.3.5 Identify Input Purpose. https://www.w3.org/WAI/WCAG22/Understanding/identify-input-purpose.html . **P** 18/11/2026. Supports: autocomplete tokens.
99. W3C. Understanding 4.1.2 Name, Role, Value. https://www.w3.org/WAI/WCAG22/Understanding/name-role-value.html . **P** 18/11/2026. Supports: Accessible names.
100. W3C. Understanding 4.1.3 Status Messages. https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html . **P** 18/11/2026. Supports: Announce without focus.
101. W3C. ARIA APG: Read Me First. https://www.w3.org/WAI/ARIA/apg/practices/read-me-first/ . **P** 18/11/2026. Supports: No ARIA is better than bad ARIA.
102. W3C. ARIA APG: Dialog (Modal) Pattern. https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/ . **P** 18/11/2026. Supports: Dialog keys and focus.
103. W3C. ARIA APG: Combobox Pattern. https://www.w3.org/WAI/ARIA/apg/patterns/combobox/ . **P** 18/11/2026. Supports: Combobox keys.
104. W3C. ARIA APG: Patterns index. https://www.w3.org/WAI/ARIA/apg/patterns/ . **P** 18/11/2026. Supports: Pattern list.
105. W3C. Using ARIA. https://www.w3.org/TR/using-aria/ . **P** 18/11/2026. Supports: Native first.
106. W3C. WAI Easy Checks. https://www.w3.org/WAI/test-evaluate/easy-checks/ . **P** 18/11/2026. Supports: First review steps (draft page).
107. W3C. WCAG-EM Overview. https://www.w3.org/WAI/test-evaluate/conformance/wcag-em/ . **P** 18/11/2026. Supports: Sampling and evaluation method.

## Cited in older references, not re-verified this pass
108. Saffer, D. *Microinteractions*. O'Reilly, 2013. ISBN not matched this pass. **U**. Supports: trigger, rules, feedback, loops.
109. Eyal, N. *Hooked*. 2014. Not matched this pass. **U**. Supports: hook model and manipulation matrix.
110. Amershi et al. *Guidelines for Human-AI Interaction*, CHI 2019. The Microsoft Research page did not load (TLS error). **U**. Supports: 18 AI guidelines.

111. Google. *Google Pay brand guidelines* (web). https://developers.google.com/pay/api/web/guides/brand-guidelines . **P** 18/11/2026: dark or light button only; button types book, buy, checkout, donate, order, pay, plain, subscribe; use only Google-provided buttons (createButton); no custom or text-only buttons and no changes to font, colour, radius or padding; do not translate "Google Pay"; at least 8 dp clear space; the mark not smaller than other payment brands. Apple Pay HIG page returned only its title (needs a browser pass).

Totals: 111 entries. V 18, P 90, S 0, U 3. Verified (V or P): 108 = 97.3%. Sub-claims not verified: the Nielsen and Landauer 31% figure is read on the NN/g page, not in the paper; the Mathur et al. prevalence figure; critiques of the 5-user model (not read; limits stated in `diagnosis-playbook.md` are logical and from NN/g's own caveats); the NN/g aggregation figures for heuristic evaluation; automated-tool coverage and first-click claims in `playbooks.md` are tagged [F].

## Edition notes
- Baymard numbers change between releases: 2024 article reports 11.3 checkout fields (target about 8); the abandonment list is updated yearly (70.22% in the 2026 edition read). Quote the date with the number.
- Some NN/g pages carry a later reviewed date than publication; cite both when it matters.
- SUS benchmark 68 comes from MeasuringU, via NN/g; it is an average over many products, not a pass mark.

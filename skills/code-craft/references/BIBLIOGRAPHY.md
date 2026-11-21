# Bibliography: code-craft

Checked 18/11/2026. Status: **V** = identity (title, publisher, year as far as the catalogue shows) matched to the ISBN in OpenLibrary (`https://openlibrary.org/isbn/<isbn>.json`) this pass; **P** = official or primary page opened this pass (for a paper: the Crossref record at `https://api.crossref.org/works/<doi>` matched title, authors, venue and year; the paper text was not read); **S** = exists, text not read; **U** = unverified. Nothing is quoted; ideas are restated. The catalogue often omits author names, so authors come from prior knowledge. Catalogue years may belong to a later printing. Numbers are cited as [n] in the reference files.

## Books
1. Martin, R. C. *Clean Code: A Handbook of Agile Software Craftsmanship*. Prentice Hall, 2008. ISBN 978-0132350884. **V**. Supports: naming, functions, comments, errors; counterpoint in `clean-code-and-design.md`.
2. Ousterhout, J. *A Philosophy of Software Design*, 2nd ed. Yaknyam Press, 2021. ISBN 978-1732102217. **V** (catalogue: July 2021). Supports: deep modules, tactical vs strategic.
3. Beck, K. *Test-Driven Development: By Example*. Addison-Wesley, 2002. ISBN 978-0321146533. **V** (catalogue date 2006, a later printing). Supports: red-green-refactor, fake it, triangulate, test list.
4. Freeman, S., Pryce, N. *Growing Object-Oriented Software, Guided by Tests*. Addison-Wesley, 2009. ISBN 978-0321503626. **V** (catalogue: 2010). Supports: outside-in, mocking roles.
5. Meszaros, G. *xUnit Test Patterns: Refactoring Test Code*. Addison-Wesley, 2007. ISBN 978-0131495050. **V**. Supports: test double vocabulary, test smells.
6. Gamma, E., Helm, R., Johnson, R., Vlissides, J. *Design Patterns: Elements of Reusable Object-Oriented Software*. Addison-Wesley, 1994. ISBN 978-0201633610. **V** (catalogue: January 1995). Supports: `patterns.md`.
7. Freeman, E., Robson, E. *Head First Design Patterns*, 2nd ed. O'Reilly, 2020. ISBN 978-1492078005. **V** (catalogue: 2021). Supports: pattern intros in modern Java.
8. Fowler, M. *Patterns of Enterprise Application Architecture*. Addison-Wesley, 2002. ISBN 978-0321127426. **V** (catalogue: 2007 printing). Supports: transaction script, domain model, repository, unit of work, data mapper, active record, service layer.
9. Fowler, M. *Refactoring: Improving the Design of Existing Code*, 2nd ed. Addison-Wesley, 2018. ISBN 978-0134757599. **V**. Supports: smell and refactoring names in `diagnosis-playbook.md`.
10. Evans, E. *Domain-Driven Design: Tackling Complexity in the Heart of Software*. Addison-Wesley, 2003. ISBN 978-0321125217. **V** (catalogue: 2008 printing). Supports: `ddd-tactical.md`.
11. Vernon, V. *Implementing Domain-Driven Design*. Addison-Wesley, 2013. ISBN 978-0321834577. **V** (catalogue: 2012). Supports: aggregate design rules, events.
12. Vernon, V. *Domain-Driven Design Distilled*. Addison-Wesley, 2016. ISBN 978-0134434421. **V**. Supports: short tactical summary.
13. Feathers, M. *Working Effectively with Legacy Code*. Prentice Hall, 2004. ISBN 978-0131177055. **V**. Supports: seams, characterization tests.
14. Kerievsky, J. *Refactoring to Patterns*. Addison-Wesley, 2004. ISBN 978-0321213358. **V** (catalogue: 2007 printing). Supports: arriving at patterns by refactoring (`playbooks.md` 3).
15. Martin, R. C. *Agile Software Development, Principles, Patterns, and Practices*. Prentice Hall, 2002. ISBN 978-0135974445. **V**. Supports: SOLID.
16. Khononov, V. *Learning Domain-Driven Design*. O'Reilly, 2021. ISBN 978-1098100131. **V**. Supports: tactical patterns in a modern frame.
17. Wlaschin, S. *Domain Modeling Made Functional*. Pragmatic Bookshelf, 2018. ISBN 978-1680502541. **V**. Supports: unions, illegal states unrepresentable.
18. Khorikov, V. *Unit Testing Principles, Practices, and Patterns*. Manning, 2020. ISBN 978-1617296277. **V**. Supports: classical vs mockist view, test value.
19. Percival, H., Gregory, B. *Architecture Patterns with Python*. O'Reilly, 2020. ISBN 978-1492052203. **V**. Supports: repository and unit of work in practice.
20. Beck, K. *Tidy First?* O'Reilly, 2023. ISBN 978-1098151249. **V**. Supports: small tidyings, when to tidy.

## Web pages
21. Fowler, M. "Test Double" (bliki, 17 Jan 2006). https://martinfowler.com/bliki/TestDouble.html . **P** 18/11/2026: page opened; summarizes Meszaros's vocabulary.
22. Fowler, M. "Mocks Aren't Stubs". https://martinfowler.com/articles/mocksArentStubs.html . **P** 18/11/2026: page opened (sections on classical and mockist testing).
23. Fowler, M. "Anemic Domain Model" (25 Nov 2003). https://martinfowler.com/bliki/AnemicDomainModel.html . **P** 18/11/2026.
24. Fowler, M. "Value Object" (14 Nov 2016). https://martinfowler.com/bliki/ValueObject.html . **P** 18/11/2026.
25. Fowler, M. "Beck Design Rules" (2 Mar 2015). https://martinfowler.com/bliki/BeckDesignRules.html . **P** 18/11/2026.
26. "It's probably time to stop recommending Clean Code" (qntm). https://qntm.org/clean . **P** 18/11/2026: page opened, critique of the book's examples read in part. Opinion, not study.
27. Muratori, C. "Clean Code, Horrible Performance". https://www.computerenhance.com/p/clean-code-horrible-performance . **S**: page loads, title and text not extracted this pass (needs browser pass). Opinion plus a benchmark of one program.
28. Ousterhout, J., Martin, R. C. "A Philosophy of Software Design vs Clean Code" (discussion). https://github.com/johnousterhout/aposd-vs-clean-code . **P** 18/11/2026: repository landing page matches title; discussion body not read in full.

## Papers (Crossref record matched)
29. Rafique, Y., Mišić, V. "The Effects of Test-Driven Development on External Quality and Productivity: A Meta-Analysis". *IEEE TSE*, 2013. DOI 10.1109/TSE.2012.28. **P** (Crossref).
30. Fucci, D., Erdogmus, H., Turhan, B., Oivo, M., Juristo, N. "A Dissection of the Test-Driven Development Process: Does It Really Matter to Test-First or to Test-Last?". *IEEE TSE*, 2017. DOI 10.1109/TSE.2016.2616877. **P** (Crossref).
31. Munir, H., Moayyed, M., Petersen, K. "Considering rigor and relevance when evaluating test driven development: A systematic review". *Information and Software Technology*, 2014. DOI 10.1016/j.infsof.2014.01.002. **P** (Crossref).
32. Nagappan, N., Maximilien, E. M., Bhat, T., Williams, L. "Realizing quality improvement through test driven development: results and experiences of four industrial teams". *Empirical Software Engineering*, 2008. DOI 10.1007/s10664-008-9062-z. **P** (Crossref).
33. Erdogmus, H., Morisio, M., Torchiano, M. "On the effectiveness of the test-first approach to programming". *IEEE TSE*, 2005. DOI 10.1109/TSE.2005.37. **P** (Crossref).
34. Khomh, F., Di Penta, M., Guéhéneuc, Y.-G., Antoniol, G. "An exploratory study of the impact of antipatterns on class change- and fault-proneness". *Empirical Software Engineering*, 2012 (Crossref lists online year 2011). DOI 10.1007/s10664-011-9171-y. **P** (Crossref).
35. Sjøberg, D. I. K., Yamashita, A., Anda, B. C. D., Mockus, A., Dybå, T. "Quantifying the Effect of Code Smells on Maintenance Effort". *IEEE TSE*, 2013. DOI 10.1109/TSE.2012.89. **P** (Crossref).
36. Palomba, F., Bavota, G., Di Penta, M., Fasano, F., Oliveto, R., De Lucia, A. "On the diffuseness and the impact on maintainability of code smells: a large scale empirical investigation". *Empirical Software Engineering*, 2018 (Crossref: 2017 online). DOI 10.1007/s10664-017-9535-z. **P** (Crossref).

Totals: 36 entries. Verified identity (V or P): 35 = 97%. Seen but text unread (S): 1 (item 27). Unverified (U): 0 as entries; sub-claims marked U: the findings attributed to papers 29-36 in the reference files are summaries from memory of the abstracts, not re-read this pass (the Crossref records confirm only identity). Not located: Karac and Turhan 2018 (IEEE Software, "What do we (really) know about TDD?") returned no Crossref record, so it is not cited.

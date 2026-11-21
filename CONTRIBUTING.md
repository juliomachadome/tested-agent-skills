# Contributing

Thanks for helping improve Tested Agent Skills. Contributions are welcome when they make a skill more accurate, safer, clearer, more portable, or easier to verify.

## Contribution does not grant repository access

For external contributors, the normal path is: fork the repository, create a branch in the fork, and open a pull request (PR). A PR proposes a change; it does **not** grant write access, merge rights, release rights, access to secrets, access to private evaluation material, or permission to change repository settings.

Only maintainers with the appropriate GitHub role can merge a PR, manage branches, create releases, change workflows, alter security settings, or add collaborators. See [maintainer publication checklist](docs/maintainer-publication-checklist.md) for the intended `main`-branch protections.

## Before opening an issue or PR

- Search existing issues and PRs first.
- Do not include secrets, API keys, access tokens, personal data, local paths, customer material, private prompts, raw session logs, private holdouts, or unlicensed third-party text.
- For a security concern, follow [SECURITY.md](SECURITY.md); do not publish an exploit or sensitive detail in an issue.
- Keep one PR focused on one outcome. A small correction, a source update and a new skill should normally be separate PRs.

## Types of contribution

### Fix a skill or reference

Explain the concrete problem, the evidence for the correction, and the affected skill/reference. Prefer primary or authoritative sources for changeable facts. Do not copy books, paywalled articles, or long third-party passages into the repository: write an original synthesis and cite the source.

### Propose a new skill

Start with an issue describing the user problem, audience, trigger boundary, existing overlap, sources, expected output, and how the proposal could be evaluated. A maintainer may ask for the scope to be narrowed or decide that an existing skill should be improved instead.

New public-facing material must be in clear English. It must distinguish verified facts, uncertainty, and practitioner guidance; must name its source boundaries; and must not claim universal model or harness performance.

### Improve evaluation or compatibility evidence

Use synthetic, non-sensitive fixtures for anything intended to be public. Record the exact harness, model, skill revision, tools, isolation settings, date, evaluation rule, and outcome. Do not add raw private answers or private holdouts. A result is specific to its model/harness pair unless independently measured elsewhere.

For a skill change that claims better output, compare the same synthetic tasks with and without the proposed skill on the same model and harness, using a rubric or assertions defined before inspecting the outputs. Repeat where practical, report all runs and ties, losses and inconclusive results, and describe how the outputs were judged. A single pair is exploratory evidence, not proof of a general improvement. For a trigger change, include prompts that should load the skill and near-miss prompts that should not.

### Test another harness or model

Cross-harness reports are especially valuable. A useful report answers a narrow question, such as “does this skill load in this harness?”, “does its trigger avoid this near-miss?”, or “does a public fixture improve the declared output contract on this exact model?”

Start with the **Harness evaluation** issue template. Use only synthetic fixtures or inputs you are allowed to share. Include the harness/version, exact model, skill commit, discovery method, enabled tools, isolation settings, fixture IDs and SHA-256 fingerprints, evaluation rule, redacted outcome and date. A report without that context is feedback, not benchmark evidence.

Maintainers label third-party reports as external evidence. They become a repository compatibility or quality claim only after the methodology, safety boundary and artifact are reviewed. A negative, tied or inconclusive result is still useful and will not be hidden.

### Improve a model- or harness-specific loss

A skill can beat the baseline in one model and lose in another. That is a useful compatibility finding, not a reason to erase the losing result. Open an evaluation report with the exact pair, then classify the failure: the skill was not discovered, the model ignored it, the skill added no decision-relevant structure, the output contract broke, or the skill introduced a regression. Propose the smallest targeted change, rerun the same with/without fixture plus a near-miss/regression case, and keep the result labelled for that model/harness. Do not tune the skill to one model while silently degrading another.

### Add a source or bibliography item

Do not add a source merely because it says something generally true that a capable model already knows. A source earns a place when it changes an actionable decision: a diagnosis branch, safety boundary, measurable rule, implementation detail, exception, current official policy, or an evidence-backed counterexample.

For a bibliography proposal, explain:

1. The exact claim or decision it improves.
2. What gap, ambiguity or outdated rule exists in the current skill.
3. Why the source is authoritative enough for that claim.
4. The original synthesis you propose—never a copied passage.
5. How the change could be tested against a no-skill or prior-skill baseline when practical.

Prefer primary research, official standards/documentation, maintained specifications and serious systematic reviews. Secondary sources can provide context but should not be the sole basis for a high-impact claim. Books, articles and websites remain their authors' property; link and synthesize rather than reproduce them.

### Improve a skill beyond the model baseline

The point of a skill is not to repeat generic advice. A strong contribution adds reusable structure a model is unlikely to apply reliably without context: decision boundaries, failure modes, domain-specific calculations, operational checklists, current constraints, source hierarchy, examples of near misses, or a testable output contract.

State the **incrementality hypothesis** in the issue or PR: what concrete behavior should improve when the skill is used, compared with no skill or the prior version? If the proposal cannot name an observable difference, it likely belongs in ordinary model context rather than a new skill.

## Local checks

Run the checks relevant to your change before opening a PR:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/check-public-safety.py .
python3 scripts/build-agent-profiles.py
```

The public checkout does not include the historical catalog and evaluation-summary generators or their private inputs. Propose corrections to those published summaries in a PR; a maintainer will verify and regenerate them in the private working repository. The agent-profile generator is available publicly: if an agent definition changes, include its regenerated profile in the same PR.

## Pull request checklist

- [ ] The PR has one clear purpose and a descriptive title.
- [ ] I have the right to submit every line and have not included third-party text beyond fair quotation/citation.
- [ ] I have not added sensitive data, local configuration, raw sessions, private holdouts, or credentials.
- [ ] I ran the relevant checks, or clearly stated why I could not.
- [ ] If I claim a quality improvement, I ran a same-prompt with/without comparison; if I changed triggering, I tested positive and near-miss cases.
- [ ] Claims are scoped to the evidence; no new universal compatibility or quality claim is implied.
- [ ] A new source adds a decision-relevant rule or current evidence, not generic restatement.
- [ ] A new skill or substantial change states its incrementality hypothesis and a safe evaluation path.
- [ ] Sources, license scope and attribution remain accurate.
- [ ] I updated generated output only when its source changed.

## Review and merge

Maintainers may request changes, split a PR, close a proposal that does not fit the project, or rewrite a contribution for clarity and safety. A PR is merged only after the required checks pass and the maintainer accepts the scope, evidence, licensing and security boundary.

For a skill or evaluation change, the maintainer should test the PR branch before merging and compare it with the current `main` baseline. A contributor's local result is evidence to review, not approval. If the change is merged, rerun the relevant public smoke checks on the new commit and update the aggregate evidence only when the exact model/harness result and limitations are recorded.

By submitting a contribution, you confirm that you have the right to submit it and agree that your original contribution is shared under this repository's [CC BY-SA 4.0 license](LICENSE).

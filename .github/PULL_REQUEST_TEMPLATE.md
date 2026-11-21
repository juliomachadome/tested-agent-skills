## What changed?

Describe one concrete outcome and why it is needed.

## Evidence and scope

- Relevant source, test, issue or reproduction:
- Model/harness claim (if any):
- Incrementality hypothesis (if a skill changes):
- What is intentionally out of scope:

## Safety and licensing

- [ ] No secrets, personal data, local paths, raw sessions, private holdouts or customer material.
- [ ] I have the right to submit this content; sources and attribution are accurate.
- [ ] I did not copy unlicensed third-party text.
- [ ] A new bibliography item changes a decision, rule, constraint or testable behavior; it is not generic restatement.

## Checks

- [ ] `python3 -m unittest discover -s tests -v`
- [ ] `python3 scripts/check-public-safety.py .`
- [ ] Relevant generator(s), if an input changed.
- [ ] If skill behavior changed, I included a paired baseline/comparison or explained why a smoke/trigger-only test is the appropriate scope.

## Maintainer checklist

- [ ] Claim is evidence-scoped.
- [ ] Scope, sources, license and public-release boundary are acceptable.
- [ ] Required checks passed; no workflow or permission expansion is hidden in the diff.

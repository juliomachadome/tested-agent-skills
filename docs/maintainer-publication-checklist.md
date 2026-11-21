# Maintainer checklist for the future public repository

This checklist is for the owner/admin when the filtered export becomes its own public repository. It is not a permission grant to contributors.

## Before making it public

- [ ] Generate a fresh export with `scripts/export-public-release.py`.
- [ ] Review the export and run `python3 scripts/check-public-safety.py <export-directory>`.
- [ ] Confirm no `.git` history, raw answers, holdouts, local paths or historical PT-BR catalog source files entered the export.
- [ ] Create a new repository from the inspected export; do not change the working repository's visibility.
- [ ] Set the description, topics, license and social-preview image in the repository's About settings.

## Security and quality settings

For a public GitHub repository, enable the free repository protections shown under **Settings → Security and quality → Advanced Security**:

- [ ] Dependency graph (this repository currently has no runtime package manifest, so it may report no dependencies).
- [ ] Dependabot alerts.
- [ ] Secret scanning and push protection.
- [ ] Code scanning/CodeQL for the Python scripts, after reviewing the generated workflow.
- [ ] Do not enable paid trials, Copilot Autofix, AI Scan or other metered AI features unless you intentionally choose a billing plan.

GitHub makes these core protections available to public repositories at no charge; the repository owner should still read the current billing label shown by GitHub before enabling any feature that says `Try free`, `AI`, `Autofix` or `credits`.

## Protect `main`

Create a GitHub ruleset (preferred) or branch-protection rule targeting `main`:

- [ ] Require a pull request before merge.
- [ ] Require the `Verify contribution / verification` status check.
- [ ] Require conversation resolution before merge.
- [ ] While there is only one maintainer, do **not** require a reviewer or Code Owner approval: it would prevent the owner from merging their own PRs.
- [ ] After adding a second trusted maintainer, require one approving review and Code Owner review; `.github/CODEOWNERS` identifies sensitive paths.
- [ ] Dismiss stale approvals when new commits arrive.
- [ ] Block force pushes and branch deletion.
- [ ] Do not allow bypassing the ruleset, including for administrators, unless an exceptional recovery is needed.
- [ ] Keep releases, repository rules, security settings, Actions configuration and collaborator access limited to the owner/admin.

## Fork workflow safety

- [ ] In Actions settings, require approval before workflows from outside collaborators run.
- [ ] Keep the default `GITHUB_TOKEN` read-only for PR checks.
- [ ] Do not expose secrets to fork-triggered workflows; avoid `pull_request_target` unless there is a reviewed, unavoidable design.

## Ongoing maintenance

- [ ] Review dependency/action updates before accepting them.
- [ ] Tag a version and update `CHANGELOG.md` for each public release.
- [ ] Re-run the safety check before every release.
- [ ] Review proposed skill sources, licensing, attribution and model/harness claims before merge.

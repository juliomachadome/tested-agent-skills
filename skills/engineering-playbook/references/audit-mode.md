# Audit mode

Open only when the user explicitly invokes `/engineering-playbook audit` or asks for a full playbook audit; never start it on your own.

Goal: map every point to this codebase once and persist the result so later sessions need not re-read everything.

1. **Map the project:** README, project files, folder structure, bootstrap/DI, data layer and migrations, auth, CI, infra. Identify stack and versions, architecture style, entry points, hot paths, external dependencies.
2. **Go through every file in `references/`** (except `BIBLIOGRAPHY.md`, `diagnosis-playbook.md`, `playbooks.md` and this file; the two playbooks are routines, not rule lists). Classify each point as `OK` (cite `file:line`), `GAP` (cite `file:line`, severity, concrete fix), `N/A` (one-line reason) or `UNKNOWN` (say what would confirm it). A valid alternative convention is `OK (convention)`, not `GAP`; `GAP` means real risk. For large repos, use one subagent per reference file and consolidate.
3. **Never guess evidence:** every `OK`/`GAP` points to code you opened.
4. **Write `docs/engineering-audit.md`:** top 10 gaps by severity (file:line, why, fix, effort S/M/L), one table per area, date and commit hash.
5. **Propose a `## Project engineering profile` block (40 lines max) for `CLAUDE.md`:** stack, architecture, conventions in use, hot paths, key areas, N/A areas, pointer to the audit. Show it and ask before editing.
6. **Do not change application code during the audit.** Fixes come later, one gap per change.


## Sources

- This is the skill's own procedure; the rules it checks cite their sources in each reference file.

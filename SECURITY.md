# Security and privacy

The repository is intended to be safe to inspect and install. It is not a security product, and no automated check can prove that a release contains no sensitive material. Review each version as code and documentation before use.

## Release boundary

Public releases contain skills, portable documentation, synthetic fixtures and aggregate evaluation results. They do not intentionally include personal configuration, local paths, connectors, raw sessions, private holdouts, full model responses, internal notes or personal cost records.

Before releasing a public export, run:

```bash
python3 scripts/check-public-safety.py <release-directory>
```

The check looks for a narrow set of common private-path, personal-email and credential markers. It prints only a rule and a relative file path, never the matching content. It is a guardrail, not a replacement for human review, repository secret scanning or a fresh-history check.

Use `scripts/export-public-release.py <new-empty-directory>` to make that reviewable fresh export. It omits `.git`, raw evaluation directories, internal planning material and the historical detailed PT-BR catalog/source files; the generated English catalog remains. Initialize or publish a Git repository only from the inspected export, never by changing this working repository's visibility.

## Install boundary

`scripts/install.sh` links selected skills into a local discovery folder. By default it does not execute a downloaded skill, transmit data, create a network service or remove unrelated files. If a target name already exists, the installer moves that item to a dated backup before creating its link. Review the script and use `--dry-run` first when this matters to your environment.

Skills are instructions, not a permission boundary. A harness, its configured tools, and the model provider determine what a session can read, write or send. Do not give an agent private data or powerful tools merely because it loaded a skill from this repository.

## Evaluation boundary

The historical evaluation artifacts are from Claude-based runs. Public evaluation materials use synthetic prompts and do not include answer keys in fixture directories. A real model run can send its prompt to the selected provider and can incur provider charges.

The Codex adapter is designed to run with an isolated, read-only session:

```bash
--ephemeral --ignore-user-config --sandbox read-only
```

Those options prevent loading normal user configuration and make the local workspace read-only; they do not make a model call free, nor do they protect data that a user chooses to place in a fixture. Use only synthetic, non-sensitive test inputs.

## Reporting a vulnerability

Do not put a secret, exploit payload or private data in a public issue. Use GitHub's private vulnerability reporting for this repository when it is enabled. If it is unavailable, open a minimal public issue requesting a private reporting channel, without including sensitive details.

For a public release, the maintainer checklist recommends GitHub's free protections: dependency graph, Dependabot alerts, secret scanning/push protection and code scanning. These GitHub-side controls do not replace the local release check. Avoid paid or metered AI security features unless billing is intentionally approved.

## Trust model

- The source is public and intended for inspection.
- The release checker and unit tests reduce common publication mistakes; they do not guarantee absence of every secret or unsafe instruction.
- References are bibliographic pointers. They are not bundled third-party books, credentials or external access grants.
- Compatibility claims name the exact harness and model when measured. Plain Markdown portability does not mean identical behavior or automatic tool access everywhere.

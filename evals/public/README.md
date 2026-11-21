# Public evaluation fixtures

This directory is reserved for synthetic, non-sensitive test fixtures. A fixture may include a task, expected output shape and deterministic assertions. It must not include customer data, credentials, local paths, full private model answers, hidden holdouts or connector configuration.

## Separate from historical evaluation

These are **public smoke/reproduction fixtures**. They are not the historical blind holdout and do not count toward the repository's historical win/tie totals. Historical evaluation material lives under individual skill `evals/` directories in the private working repository and is deliberately excluded from a public release.

Use this command before reporting a result to identify the exact fixture contents you ran:

```bash
python3 scripts/fingerprint-public-fixtures.py
```

Include the fixture `id` and SHA-256 value in an external evaluation report. If the fingerprint matches, the contributor ran the same public case; if it differs, it is a different or modified case. Both are useful, but they are reported separately.

## Safe fixture contract

```json
{
  "id": "short-stable-name",
  "skill": "skill-name",
  "prompt": "Synthetic task only",
  "expected_output": "Public output contract",
  "assertions": ["Deterministic property to check"]
}
```

Keep the answer key out of the same directory when the task is intended to test an agent's behavior. Smoke fixtures may instead assert an observable non-secret property, such as whether the requested skill was read or whether output is valid JSON.

## Reporting a run

Save only redacted metadata and outcome: harness/version, model, skill commit, fixture ID, isolation flags, tools, date and result. Full answers belong in a private evaluation workspace unless they are intentionally authored as public examples.

Read [the evaluation methodology](../../docs/evaluation-methodology.md) before treating a public smoke test as a benchmark.

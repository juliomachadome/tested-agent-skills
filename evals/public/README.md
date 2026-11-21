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

## Run a paired development check

The paired runner is separate from the smoke adapter. It defaults to a dry run. Supply a model ID available to the account being used.

```bash
python3 scripts/codex-skill-compare.py \
  --fixture evals/public/qa-stale-release.json --model <model-id>
```

Add `--live` to run both conditions in separate sessions. This calls the provider and may incur charges. For independent repetitions, use --runs 3 (three sessions per condition, six total for a pair). Use `--condition with` or `--condition without` to run one arm. The default `--discovery explicit` supplies the main skill text in the with arm and tests what those instructions add. `natural` installs a project skill without directing the model to read it. `forced` also directs the model to read the local file. A matching file-read event is evidence of a read; an absent event is inconclusive. The runner requests that plugins and host skill discovery be skipped. Use a clean test environment and check what the harness actually exposed before treating the without arm as isolated.

The JSON report contains fixture and skill fingerprints, session completion, available token usage, duration and deterministic field checks. For these public development cases, `expected_fields` gives the machine-checked JSON fields and is never added to the model prompt. The `assertions` list can also contain reviewer checks, such as whether a release verdict avoids a false green. A passing field check is narrower than a quality pass.

For blind review, create a private directory outside any Git checkout and opt in with `--answers-dir`. The runner saves only final answers in a fresh subdirectory, under the letters A and B. Repeated pairs add the pair number to the private filenames. Consult run_index and pair_index in the redacted report. Give the evaluator those files and the rubric, then consult the report's label mapping after scoring. The runner does not save raw traces or explanations of errors. Use synthetic data only and do not commit the answer directory.

These fixtures cover release evidence, customer support disposition, and a defensive workspace access policy. They are development checks, not a held-out evaluation or new evidence of skill quality.

## Probe routing between overlapping skills

Use the offers-versus-copywriting fixture with natural discovery. The alternate skill is present in both arms and the target is added only in the with arm.

    python3 scripts/codex-skill-compare.py --fixture evals/public/copywriting-offers-routing.json --model <model-id> --discovery natural --runs 3

Add --live only to execute. The redacted report lists observed reads for the target and alternatives separately. No observed read is inconclusive. reference_paths_in_successful_commands reports only validated project file path mentions from successful commands, and does not prove their content was read. Track false routing independently of answer quality.

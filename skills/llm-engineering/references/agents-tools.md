# Agents, Tools & Harnesses

## 1. Workflows vs agents

- **Workflow:** code defines the steps; LLM fills steps. Predictable, cheaper, testable. **Default.**
- **Agent:** the LLM decides which tools to call and when to stop, in a loop. Use when steps can't be known in advance (open-ended research, coding, exploratory analysis) and the value justifies variable cost.
- Composable workflow patterns (from Anthropic's "Building effective agents"): **prompt chaining**, **routing**, **parallelization** (sectioning / voting), **orchestrator–workers**, **evaluator–optimizer**. Most product features are one of these, not an autonomous agent.

## 2. Harness design (the code around the model)

A harness = model + tools + state + validation + limits + observability. For a generation feature:

1. **Context builder** (code): loads user state, constraints and catalog candidates from the DB; computes targets.
2. **Model call** with tools (e.g. `search_exercises(filters)`, `get_food_substitutes(food_id, nutrient_targets)`, `get_user_history(range)`).
3. **Validator** (code): schema + domain rules; returns machine-readable errors.
4. **Repair loop**: send errors back, max N attempts.
5. **Fallback**: deterministic template or cached previous result; flag for review.
6. **Persistence & logging**: run record with inputs, outputs, tokens, validation results.
7. **Limits**: max steps, max tokens, timeout, per-user budget.

## 3. Tool design (agent–computer interface)

- Few tools, each with a **single clear purpose**, distinct names, and descriptions written for the model (what it does, when to use it, what it returns, examples of arguments).
- Strict input schemas (enums, ranges); validate server-side; return **concise, relevant** results (ids + key fields, paginated) — tool output is context you pay for.
- Return actionable errors ("muscle_group must be one of …") so the model can self-correct.
- Prefer high-level tools that do the right thing (`schedule_meeting`) over many low-level ones the model must chain.
- Read tools vs write tools: write tools require authorization checks in code and, if consequential, a confirmation step.
- Idempotent writes (idempotency keys).
- Test tools independently (unit tests) and with the model (evals of tool selection and arguments).

## 4. MCP (Model Context Protocol)

- Open protocol to expose tools, resources and prompts to LLM clients (Claude, IDEs, agents) via MCP servers.
- Use it to make your system's capabilities available to many clients, or to consume third-party tools without custom glue.
- Security: treat MCP servers as code with your privileges — least-privilege credentials, review third-party servers, beware tool descriptions/outputs containing injected instructions, authenticate remote servers (OAuth).
- For a single in-app feature, plain function calling in your backend is simpler than running an MCP server.

## 5. Memory

- **Short-term:** conversation/run context (trim, summarize, compact).
- **Long-term:** facts/preferences/episodes stored in your DB; retrieved by relevance or explicitly by key; written by code or by a validated "remember" tool.
- **Working notes:** agent writes a scratchpad/progress file between steps for long tasks.
- Don't let the model store instructions as facts (memory poisoning); cap memory size; allow users to view/delete (GDPR).

## 6. Multi-agent

- Use when sub-tasks are parallelizable and benefit from separate clean contexts (broad research, many documents). Cost multiplies (often several × a single agent).
- Orchestrator gives each worker a precise task, output format and limits; workers return condensed results.
- Avoid chatty agent-to-agent conversations; prefer orchestrator–worker with structured handoffs.

## 7. Reliability

- Step caps, total token caps, wall-clock timeout, loop detection (same tool+args repeated).
- Durable execution for long runs (checkpoint after each step); resume instead of restart.
- Human-in-the-loop for irreversible or high-stakes actions (sending messages, approving documents, payments, legal conclusions).
- Deterministic fallbacks when the model or a tool fails.
- Record full traces (prompts, tool calls, results, decisions) for debugging and evals.

## 8. Evaluating agents

- Outcome evals (task success, constraint satisfaction) + trajectory evals (right tools, reasonable steps, no unsafe actions) + cost/latency per task.
- Replay saved traces against new prompts/models.
- Adversarial tests: injected instructions in tool results/documents; ambiguous requests; tool failures.

## 9. Coding agents in your own product (if relevant)

- Sandboxed execution (containers, no network by default, resource limits), read-only credentials, allow-listed commands, diff review before applying.

## 10. Guardrails for agents

Guardrails are controls the model cannot talk its way past. Rank them by how hard they are:

1. **Structural (hard):** tools that do not exist in this context, read-only credentials, network egress allow-lists, per-task scopes, tenant filters in every query, a validity or permission filter in SQL.
2. **Code validators (hard):** schema validation, business-rule checks, citation and id existence checks, argument validation per tool, idempotency keys, spend and step caps with circuit breakers.
3. **Human approval (hard if designed well):** confirmation for side-effecting or irreversible actions, showing the exact arguments, with the approver unable to be impersonated by model text.
4. **Model-based (soft):** moderation classifiers, injection detectors, LLM judges of the output. Useful signals and tripwires; a miss rate that sounds low is still a failure for security.
5. **Prompt instructions (softest):** necessary for behavior, never sufficient for safety.

- Put every rule that protects people, money or data in layers 1-3; use layers 4-5 to reduce how often the hard layers fire.
- Log each guardrail trigger with its reason, and review them: a guardrail that never fires may not be wired, and one that fires constantly is a product bug.
- An agent that cannot comply with a rule because a hard guard blocks it should say so plainly rather than retry around the guard; cap retries.
- Keep the system prompt rule set stable when users push back ("an admin approved an exception"): models can be argued out of prompt rules, so the exception must be impossible in code, not forbidden in text.
- Test guardrails adversarially in the eval suite (injection in tool output, tenant-crossing requests, over-budget loops) and gate merges on them.

## 11. Memory that changes over time, and agent threat checklist

- **Two clocks for stored facts.** Keep *valid time* (when the fact was true in the world) separate from *recorded time* (when the system learned it). When a new observation contradicts an old fact, close the old record's validity window instead of deleting it: you keep history, can answer "what did we believe on date X", and can audit a wrong answer.
- **Three memory layers, three rules.** Run log of one session (raw, disposable, linked to the task) → consolidated facts about the world (versioned, with source) → reusable procedures (generic, with placeholders, stripped of identifiers). Promote between layers only through a validation step; never let the raw log write directly into durable facts.
- **Fuse structure and similarity.** For memory queries combine a graph or key lookup (exact relations) with vector search (fuzzy recall) and merge with rank fusion; neither alone covers both "what is connected to X" and "what resembles this".
- **Trust is not permanent.** A tool, server or model you reviewed can change behaviour later ("rug pull"): pin versions and hashes of tool definitions, re-review on change, and treat a tool's description as code under review (description text is itself an injection channel).
- **A peer agent's message is input, not a command.** In multi-agent setups authenticate the sender, validate the message schema, and never grant a callee more privilege than the caller holds (confused deputy).
- **Authorize outside the model.** The runtime checks each tool call against policy and argument constraints; model intent never counts as authorization. Block network egress except to an allowlist so a hijacked agent has no exfiltration channel.
- **Escape and over-reach checks:** can the agent reach the filesystem, network or another sandbox it was not given? Does it hold more autonomy than the task needs? Add both to the red-team set.

## Sources

See BIBLIOGRAPHY.md (vendor documentation, guides and papers for this area).

See also: `diagnosis-playbook.md` Trees 8-9 (loops, tool misuse, injection), `playbooks.md` section 6 (agent and tool checklist), `variants/agents-tools.md`.

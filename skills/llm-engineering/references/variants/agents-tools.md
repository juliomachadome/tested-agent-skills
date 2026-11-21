# Variant: agents and tool use

Use for: features where the model chooses actions (search, query, write, send, run code) in a loop, or calls functions with arguments.

## Architecture choice
Climb only as far as the eval forces: deterministic code, single call with a tool, fixed workflow (prompt chain or router), agent loop, multi-agent. Most features are a workflow with one or two model-chosen steps. An autonomous loop needs a step cap, a cost cap, a timeout and loop detection from day one. Multi-agent only when contexts must be isolated or work is genuinely parallel. Detail: `../agents-tools.md`; project patterns of the current repository win.

## Prompt pattern
Describe the goal, constraints and stopping rule in the system prompt; give each tool a precise description that also says when not to use it; closed enums and strict schemas for arguments (Anthropic strict tool use, Gemini function schemas, OpenAI strict mode); actionable tool error messages ("not found: try search with the order id"). Do not script chain of thought for reasoning models; set thinking effort per step. Untrusted tool output is fenced and labelled as data.

## Eval metrics
- Task success on checkable end states (database row, file, ticket status), not on the model's own claim.
- Tool-call accuracy: right tool, valid arguments, no forbidden call.
- Steps, tokens and cost per task; p95 latency; loop and timeout rate.
- Safety: injection set pass rate; zero unapproved side effects; refusal correctness.
- Report n and Wilson intervals; run each task several times, since runs differ.

## Failure modes
Repeated identical calls; wrong tool from overlapping descriptions; invented arguments; context bloat from long tool results; injected instructions in tool output; excessive agency (more permissions than the task needs); silent partial failure. See `../diagnosis-playbook.md` Trees 8 and 9 and `../security-safety.md` (OWASP LLM06 and the lethal trifecta: private data plus untrusted content plus an outbound channel; remove one).

## Cost notes
Each loop turn re-sends the growing context, so cost grows faster than the number of steps; cache the stable prefix, trim tool results, summarise old turns, cap steps, route simple steps to a smaller model. Tool definitions add input tokens on every request (the Anthropic tool-use page lists a fixed system-prompt overhead per model). Budget per task, alarm per day.

## Checklist
- [ ] Workflow tried first; autonomy justified by an eval.
- [ ] Least privilege per tool and per user; read tools apart from write tools.
- [ ] Human confirmation before irreversible or external effects; dry-run mode.
- [ ] Step, token, cost and time caps; loop detection; kill switch.
- [ ] Arguments validated in code before execution.
- [ ] Traces with every call, argument, result size, approval.
- [ ] Injection test set; end-state eval suite; both run on every change.

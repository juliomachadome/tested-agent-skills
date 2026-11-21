# llm-engineering

A skill for building, reviewing and optimizing features that use LLMs: prompts and context, structured outputs, RAG, graphs, agents, evals, cost and latency, model choice, security, and recipes per use case. It sits next to `engineering-playbook`, which covers general engineering; both can be installed together.

```
llm-engineering/
├── SKILL.md                    principles, checklist, routing table, workflow, gaps
├── references/
│   ├── diagnosis-playbook.md   Step 0, ten symptom trees, worked cost, Wilson and sample-size numbers
│   ├── playbooks.md            ship a feature, eval set and judge, RAG loop, prompt change, incident response
│   ├── variants/               choose by feature type (rag-qa, agents-tools, classification-extraction, ...)
│   ├── prompting-context.md    context engineering, structured output, anchored citations, fencing,
│   │                           caching, versioning, Claude vs Gemini, extended thinking trade-offs
│   ├── cost-latency.md         unit economics, caching, routing, batching, budgets
│   ├── rag.md                  parsing, chunking, hybrid search, RRF, pgvector filtering, rerank, rewriting
│   ├── graphs-knowledge.md     knowledge graphs, GraphRAG, workflow graphs
│   ├── agents-tools.md         workflow vs agent, harness, tool design, MCP, memory
│   ├── evals-observability.md  per-stage metrics, Wilson intervals, paired tests, sealed sets,
│   │                           abstention, judge calibration, A/B exit criteria, OTel tracing
│   ├── security-safety.md      OWASP LLM Top 10 2025, lethal trifecta, untrusted content, ingestion
│   ├── models-providers.md     model choice, local models, fine-tuning, gateways
│   ├── speech-asr.md           Whisper, proper names, diarization, WER/DER, GPU cost
│   ├── use-cases.md            recipes per kind of feature
│   ├── red-flags-audit.md      smells to scan for and the audit procedure
│   └── BIBLIOGRAPHY.md         sources behind every rule
└── evals/                      evals.json (task prompts) and trigger_eval.json (trigger tests)
```

## Use

- **Automatic:** loads when you touch code that calls an LLM or embedding API, or ask to make an AI feature cheaper, faster or more accurate.
- **Manual:** `/llm-engineering <request>`.
- **Audit:** `/llm-engineering audit` inventories every call site with model, tokens and cost, classifies each reference point as OK, GAP, N/A or UNKNOWN with file and line, and writes `docs/llm-audit.md` with a ranked optimization plan. It changes no code.

## Limits

Prices and model names change monthly; the skill tells you to check current provider docs and keep prices as configuration. Optimizing without an eval set is guessing, so build one first.

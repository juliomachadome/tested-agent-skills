# Variant: RAG question answering with citations

Use for: policies, manuals, regulations, knowledge bases, support answers, where the answer must come from your documents and show where.

## Architecture choice
- Start with the simplest rung that passes the eval: lexical plus vector retrieval, rank fusion, a reranker, one generation call. Add a query rewriter, parent-child chunks or a graph only when a named failure class justifies it (`../graphs-knowledge.md` for questions that span many documents, where a graph can help; test on your data).
- Hard filters (validity dates, tenant, permission, language) live in the query, never in the prompt.
- No relevant retrieval, no model call: code returns a plain "not found in the sources" answer.
- Detail: `../rag.md`.

## Prompt pattern
Static prefix first (role, rules with reasons, output schema), then the fenced chunks with ids, then the question last. Ask for the supporting quote before the answer. Give explicit permission and duty to say the sources do not answer. Cite by provided ids only; a code validator checks the id exists and the quote appears in the chunk. Retrieved text is data, not instruction (`../prompting-context.md`, `../security-safety.md`).

## Eval metrics (measure each stage alone)
- Retrieval: recall@k on valid documents, full-recall rate on multi-source questions.
- Generation given perfect context: faithfulness (every claim supported).
- Citation: precision (cited source supports the claim) and recall (claims that have a citation).
- Abstention: wrongful answer rate on unanswerable questions and wrongful abstention rate on answerable ones, reported separately.
- Cost and p95 latency next to quality. Wilson intervals, paired comparisons, a sealed set (`../evals-observability.md`).

## Failure modes
Chunk cut through the answer; right chunk ranked low; filters dropping valid documents or returning fewer than k rows; answer chunk buried mid-context; fabricated citation ids; stale index; confident answer where the corpus is silent; injected instructions inside a document. Each has a row in `../diagnosis-playbook.md` Trees 1-3 and 9.

## Cost notes
Cost is mostly input tokens: k chunks times chunk size per request. Cache the stable prefix; rerank to a small k before generation; use a small model for rewriting and a mid-size one for answering unless the eval says otherwise; batch the contextual-header indexing step (paid once per document). Worked per-request and per-month numbers are in `../diagnosis-playbook.md`.

## Checklist
- [ ] Eval set with unanswerable and adversarial questions, sealed part frozen.
- [ ] Recall measured before touching the prompt.
- [ ] Filters in the query; abstention gate in code.
- [ ] Citation validator in code; quote check.
- [ ] Chunk metadata: document id, version, page, validity, tenant.
- [ ] Embedding model and dimension recorded per row.
- [ ] Injection test set for documents and user uploads.
- [ ] Freshness plan: re-index on change, version stamp shown.

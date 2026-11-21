# Graphs: Knowledge Graphs, GraphRAG and Workflow Graphs

Contents: 1 When a graph helps · 2 Two ways to get a graph · 3 GraphRAG family · 4 Storage and querying · 5 Graph + LLM patterns · 6 Workflow graphs · 7 When graph beats vector (decision) · 8 Indexing cost · 9 Graphs from code and documents (extraction, communities, god nodes, query/path/explain) · 10 Evaluating a graph approach

"Graph" means two different things in LLM engineering. Identify which one the task needs.

- **A. Knowledge graphs** — data modeled as entities and relationships, used for retrieval and reasoning (GraphRAG, domain graphs).
- **B. Workflow graphs** — the control flow of an LLM application as nodes and edges / state machine (LangGraph-style, durable workflows). See section 6.

## 1. When a knowledge graph helps

| Question type | Vector RAG | Graph |
|---|---|---|
| "What does article 5 say?" (local fact) | good | unnecessary |
| Multi-hop: "Which contracts with supplier X were signed by people who also approved Y?" | weak | strong |
| Global/thematic: "What are the main topics discussed in sessions this year?" | weak | strong (community summaries) |
| Relationships, dependencies, lineage, references between documents (law A amends law B) | weak | strong |
| User state that is relational (goals ↔ plans ↔ adherence ↔ history) | n/a | strong as a domain model |

Rule: start with vector/hybrid RAG + metadata; add a graph when evals show failures on relational/multi-hop/global questions, or when your **domain is inherently a graph** you already have as data.

## 2. Two ways to get a graph

1. **Explicit domain graph (preferred when you own the data):** model entities and relations in your DB (relational tables with foreign keys, or a graph DB). E.g. `Customer → Order → Product → Category`, `Course → Module → Lesson → Skill`, `Policy → Section → Clause`, `Document amends Document`, `Meeting → Agenda item → Decision`, `Contract → Supplier → Invoice`. Deterministic, cheap, correct. The LLM queries it through tools.
2. **LLM-extracted graph (GraphRAG family):** an LLM reads documents and extracts entities, relations and claims; then you cluster and summarize. Useful for unstructured corpora; **indexing is expensive** (many LLM calls per chunk) and extraction errors propagate.

## 3. GraphRAG family (LLM-extracted)

- **Microsoft GraphRAG:** extract entities/relations per chunk → build graph → community detection (Leiden) → LLM summaries per community at several levels. Query modes: **local** (entity-centered neighborhood + text), **global** (map-reduce over community summaries for corpus-wide questions), **DRIFT** (hybrid). Strong for global questions; highest indexing cost; re-indexing on updates is heavy.
- **LightRAG:** graph + vector dual-level retrieval (low-level entities, high-level themes), cheaper indexing and **incremental updates**. Good default to try when you need graph benefits with a changing corpus.
- **HippoRAG / HippoRAG 2:** knowledge graph + Personalized PageRank for multi-hop associative retrieval; HippoRAG reports gains of up to 20% on multi-hop QA and single-step retrieval matching iterative retrieval at 10-30x lower cost; HippoRAG 2 targets the weakness of graph methods on plain factual memory, reporting gains across factual, sense-making and associative tasks (all vendor-reported, see section 7).
- **Fast/nano GraphRAG variants:** lighter variants; check maintenance status.
- Cost control: use a cheap model for extraction, batch APIs, cache prompts, extract only from relevant document types, and benchmark indexing cost per 1k pages before committing.
- Evaluate against plain hybrid RAG on your questions — graph approaches don't win on local factual lookups.

## 4. Graph storage & querying

- Options: relational tables + recursive CTEs (often enough), Postgres + Apache AGE, Neo4j / Memgraph (Cypher), Neptune, Kùzu (embedded).
- **Text-to-Cypher/SQL by LLM** is fragile and risky: prefer predefined parameterized query tools (`get_neighbors(entity_id, relation, depth)`), read-only credentials, query timeouts and result limits.
- Entity resolution (dedupe "Acme Corporation" vs "ACME Corp.") is the hardest part of extracted graphs — normalize ids, use canonical lists, human review for key entities.

## 5. Graph + LLM patterns

- **Graph-as-context:** retrieve the subgraph around the user/entity (k-hop, filtered by relation types and time) and serialize it compactly (triples or a small JSON) into the prompt.
- **Graph-guided retrieval:** find related entities in the graph, then fetch their text chunks.
- **Graph for constraints:** the graph encodes rules (exercise contraindicated for injury X; food substitutes by nutrient profile; norm hierarchy) that code applies before/after the LLM.
- **Metric on the graph:** define the objective in data (e.g. distance from current state to goal) and let code compute progress; the LLM proposes actions, code scores them.

## 6. Workflow graphs (control flow)

- **What:** model the application as a state machine/graph: nodes = steps (LLM call, tool, validation, human approval), edges = transitions with conditions, shared typed state, checkpoints.
- **Why over a free agent loop:** predictable cost and latency, testable nodes, explicit retries/branches, resumability, easier debugging and evals per node.
- **Patterns:**
  - Generate → validate → (pass → save) / (fail → repair with errors, max N) / (still fail → fallback/human).
  - Router node → specialized sub-graphs per intent.
  - Parallel fan-out (per day/section) → merge → global validation.
  - Human-in-the-loop interrupt node (approve minutes, approve high-risk analysis) with persisted state.
  - Evaluator–optimizer loop with a stop condition (score threshold or max iterations).
- **Tools:** LangGraph (Python/JS), Mastra/Vercel AI SDK workflows (TS), Inngest/Trigger.dev/Temporal/Azure Durable Functions for durable execution, or a plain hand-written state machine with a jobs table — often enough and easiest to own.
- Persist state per run (id, step, inputs, outputs, tokens, errors) for observability and resume after crashes.
- Make each node idempotent; checkpoint after expensive LLM steps so retries don't re-pay them.

## 7. When graph beats vector: decision rules

- **Graph wins** on (a) *global sensemaking* questions about a whole corpus ("main themes", "what changed across the year"), which are query-focused summarization rather than retrieval (Edge et al.); (b) *multi-hop* questions whose answer needs facts from several documents linked by entities (HippoRAG); (c) domains where the relations are the data (amendments, dependencies, ownership, lineage), and you can store them explicitly.
- **Vector/hybrid wins or ties** on local factual lookups, exact identifiers, and small corpora. Graph-augmented methods have been reported to do *worse* than standard RAG on basic factual memory (the motivation for HippoRAG 2), so never replace the vector leg; add the graph as an extra leg and fuse.
- Order of attempts: hybrid RAG with metadata and reranking, then explicit domain graph or link table (cheap, deterministic), then hierarchical summaries (RAPTOR-style), then LLM-extracted graph with communities. Move down only when an eval on your question mix shows the failure and names its class.
- Claims in the papers are on specific datasets (for example corpora around 1 million tokens, judged by LLMs on comprehensiveness and diversity), with abstracts giving no absolute metrics; treat them as hypotheses to test on your data.

## 8. Indexing cost and operations

| Approach | Index-time cost | Update behavior | Query behavior |
|---|---|---|---|
| Hybrid RAG | embeddings only | incremental by content hash | one retrieval, one generation |
| Explicit domain graph | no LLM, ETL only | transactional | parameterized tool calls |
| GraphRAG (entities + communities) | many LLM calls per chunk plus a summary call per community and level | community structure can change with new data, so partial or full re-summarization | local mode: neighborhood plus text; global mode: one partial answer per community then a reduce step (many calls per query) |
| LightRAG-style | extraction per chunk, but no community-report hierarchy; authors claim an incremental update algorithm instead of rebuilding | incremental merge of new entities/edges | dual-level: low-level entity retrieval and high-level theme retrieval, with vectors |
| HippoRAG-style | extraction per passage (open information extraction) plus a graph index | add passages and edges | Personalized PageRank from query entities, single step |

- Estimate before building: pages x chunks per page x tokens per chunk x extraction price, plus summaries; run on 1k pages first and extrapolate. Use a small model for extraction, batch APIs for offline runs, prompt caching for the shared instruction prefix, and cache by content hash so re-runs skip unchanged files.
- Extraction quality caps everything: measure entity/relation precision and recall on a hand-labelled sample, and run entity resolution (aliases, abbreviations) with canonical ids and a review queue for important entities.
- Treat the graph as a derived artifact: keep provenance (source file, span, extraction version, confidence) on every node and edge, and never let an inferred edge look like an extracted one.
- Guard against shrinking: if a rebuild produces a much smaller graph than the previous one, refuse to overwrite and surface the difference.

## 9. Graphs from code and documents: extraction, communities, god nodes, queries

A well-engineered pipeline for turning a folder (code, docs, papers, images, transcripts) into a navigable graph looks like this:

1. **Detect and classify files**; transcribe audio/video to text first. Respect ignore files and size limits.
2. **Structural extraction for code** with a parser (AST): modules, classes, functions, imports, calls, inheritance. It is deterministic, free and exact, so code files do not go to an LLM for entities.
3. **Semantic extraction for prose** with an LLM in parallel chunks: concepts, entities, claims, and relations between them, each edge tagged by how it was obtained (extracted from text, inferred, ambiguous) and with a confidence. Cache per file hash; make runs incremental.
4. **Merge** structural and semantic nodes, deduplicate by stable ids, keep the source path relative to the scan root so the graph is portable.
5. **Cluster with community detection** (Leiden or Louvain on the edge weights) to find groups of densely connected nodes; label communities with a short human-readable name and summarize them. These communities are the units for global questions.
6. **Analyze:** *god nodes* are the highest-degree hubs everything routes through (surface them: they are the core abstractions, and also the riskiest to change); *surprising connections* are edges that cross communities; isolated nodes and weakly connected components point to gaps or dead code.
7. **Health-check before publishing:** no empty extraction overwriting a good graph, dangling edges, duplicate ids.
8. **Query tools over the graph**, not free-form graph query language written by the model:
   - *query*: expand the question to candidate start nodes with a constrained, auditable matcher, traverse breadth-first (broad context) or depth-first (a specific chain) under a token budget, and return the ranked subgraph with sources;
   - *path*: shortest or most informative path between two concepts, with edge types and provenance;
   - *explain*: one node with its neighbors, community, and the evidence for each edge.
- Return answers with evidence pointers (file and span) so a person can verify; an answer from a graph without provenance is a hallucination risk like any other.

## 10. Evaluating a graph approach

1. Build a question set stratified by type: local factual, multi-hop, global/thematic, relational ("what depends on X"), and unanswerable. Have domain experts mark the expected entities, documents and answer points.
2. Compare against the hybrid-RAG baseline **per type**, not on the average: graph methods can lose on local questions while winning on global ones.
3. Metrics by type: multi-hop and local questions: answer correctness and retrieval recall of all supporting passages (R, see evals-observability.md); global questions: pairwise LLM-judged *comprehensiveness*, *diversity* and *directness* (head-to-head judging protocol and the directness criterion come from the paper body; not re-verified), calibrated against human labels on a sample and swapped in order to cancel position bias; relational questions: exact set match against the explicit graph.
4. Report cost with quality: index cost per 1k pages, update cost, query cost and p95 latency (global mode fans out into many calls).
5. Paired comparison and intervals as for any eval; keep a sealed set; read failures by class (extraction miss, entity merge error, community too coarse, retrieval of wrong subgraph).
6. Add a regression case for each fixed failure; re-run when the extraction prompt or model changes (a new extractor changes the whole graph).

## Sources (read 2026-11-15 unless noted)

- Edge et al., From Local to Global: A Graph RAG Approach to Query-Focused Summarization (2024): https://arxiv.org/abs/2404.16130 (abstract verified 2026-11-15)
- Guo et al., LightRAG: Simple and Fast Retrieval-Augmented Generation (2024): https://arxiv.org/abs/2410.05779 (abstract verified 2026-11-15)
- Gutierrez et al., HippoRAG: Neurobiologically Inspired Long-Term Memory for Large Language Models (NeurIPS 2024): https://arxiv.org/abs/2405.14831 (abstract verified 2026-11-15)
- Gutierrez et al., From RAG to Memory: Non-Parametric Continual Learning for LLMs (HippoRAG 2, ICML 2025): https://arxiv.org/abs/2502.14802 (abstract verified 2026-11-15)
- Sarthi et al., RAPTOR (hierarchical summaries): https://arxiv.org/abs/2401.18059 (not re-verified)
- Traag, Waltman, van Eck, From Louvain to Leiden (2019): https://arxiv.org/abs/1810.08473 (not re-verified)
- Design ideas for code/document graph extraction, god nodes and query/path/explain tools come from an installed graph-building skill (read as data, 2026-11-15); no primary standard.

# Retrieval-Augmented Generation (RAG)

## 1. When to use what

| Situation | Approach |
|---|---|
| Small, stable knowledge (< a few hundred pages) used in most calls | put it in the prompt + prompt caching (long context) — simpler than RAG |
| Large or changing corpus, questions touch a small part | RAG |
| Structured data (tables, records) | query the DB (SQL/API) as a tool, not embeddings |
| Exact identifiers (law numbers, article §, product codes, names) | keyword/BM25 + metadata filters (hybrid) |
| Questions about relationships across many documents / "global" questions (themes, summaries across corpus) | GraphRAG / hierarchical summaries (see graphs-knowledge.md) |
| Model needs to decide what to look up, iteratively | agentic RAG (retrieval as a tool) |

## 2. Pipeline

```
ingest → parse → clean → chunk → enrich (metadata, context) → embed + index (vector + keyword)
query → rewrite/expand → filter (tenant, permissions, validity date, type) → hybrid retrieve (top 50–100)
      → rerank (top 5–15) → assemble context (dedupe, order, ids) → generate with citations → verify citations → answer / abstain
```

## 3. Parsing

- Quality of parsing caps the quality of everything after it.
- PDFs: use layout-aware parsers (tables, headings, columns); OCR for scans; keep page numbers. Tables → Markdown/HTML or row-wise text with headers repeated.
- Keep **document structure** (title, section, article, paragraph, page) as metadata.
- Remove boilerplate (headers/footers/page numbers) before chunking.
- Store the original document and the extracted text with a content hash (re-index only on change).

## 4. Chunking

| Strategy | Use |
|---|---|
| **Structure-aware** (by heading/section/article/clause) | default for structured docs (laws, contracts, manuals) |
| Recursive character/token split with overlap (~200–800 tokens, 10–20% overlap) | unstructured prose |
| Semantic chunking (split where embedding similarity drops) | long unstructured text; costlier |
| **Parent–child / small-to-big** | retrieve small precise chunks, send the larger parent section to the LLM |
| **Contextual chunking / contextual retrieval** | prepend to each chunk a short LLM-generated (or template) context: document title, section path, what the chunk is about — markedly improves retrieval for chunks that lose meaning in isolation; cost is paid once at indexing (use prompt caching/batch) |
| Late chunking | embed the whole document with a long-context embedding model, then pool per chunk — keeps document context in chunk vectors |
| Propositions | split into atomic facts; precise but expensive |

- Never split mid-sentence, mid-table row, or between an article and its paragraphs if they must be read together.
- Each chunk carries: `doc_id`, `chunk_id`, section path, page, dates (published, valid from/to), tenant, permissions, language, source URL.

## 5. Embeddings

- Choose by evaluation on **your** queries (domain text in other languages behaves differently from English benchmarks). MTEB/MMTEB leaderboards are a starting point only.
- Multilingual models for non-English content; same model for documents and queries (or the paired query/document modes some models require).
- Normalize vectors if using cosine/dot product consistently.
- Store model name + version + dimension; re-embed all on model change (never mix spaces).
- Dimension truncation (Matryoshka) to cut storage/latency — evaluate.

## 6. Indexes & stores

- **Default: Postgres + pgvector** (HNSW index) when you already use Postgres — transactions, metadata filters, joins, RLS for tenants, one system to operate. Add full-text (`tsvector`, or BM25 via extensions) for hybrid.
- Dedicated vector DBs (Qdrant, Weaviate, Milvus, Pinecone) or search engines (OpenSearch/Elasticsearch, Azure AI Search, Vespa) when scale, hybrid ranking features or filtering performance demand it.
- ANN (HNSW/IVF) trades recall for speed: tune `ef_search`/probes and measure recall against exact search on a sample.
- Filtered vector search can lose recall when filters are very selective — check the store's filtering strategy; pre-filter by partition (tenant/jurisdiction) where possible.

## 7. Retrieval

- **Hybrid search:** BM25/keyword + vector, fused with **Reciprocal Rank Fusion** (RRF) or weighted scores. Catches exact terms (numbers, names, acronyms) that embeddings miss.
- **Metadata filters** first: tenant, permissions, document type, jurisdiction, **validity date** (for laws: the version in force at the date of the question).
- **Query transformation:** rewrite conversational follow-ups into standalone queries; multi-query (several paraphrases); decomposition for multi-part questions; HyDE (embed a hypothetical answer) for vocabulary mismatch; step-back queries for general principles. Each adds a call — measure.
- **Reranking:** cross-encoder or LLM reranker on top 50–100 → keep top 5–15. Usually one of the biggest quality gains per cost.
- **Diversity:** MMR to avoid near-duplicate chunks.
- Retrieve more, send less: recall at retrieval, precision at rerank.

## 8. Context assembly & generation

- Order chunks by relevance (or by document order within the same doc); models attend better to the beginning and end of long contexts ("lost in the middle").
- Label each chunk with an id and source: `<source id="act-123-art5-p2" title="Act 123/2020, art. 5, par. 2" valid_from="2021-01-01">…</source>`.
- Instruct: answer only from sources; cite ids per claim; if sources are insufficient, say so (abstain) and state what is missing.
- **Verify citations in code:** cited ids must exist in the provided set; optionally check the quoted span appears in the source; strip or flag uncited claims.
- Separate "answer" from "sources" in structured output.

## 9. Freshness, versions, permissions

- Incremental indexing by content hash; deletions propagate to the index (GDPR erasure too).
- Temporal validity: keep versions of norms/policies; filter by "in force at date X"; show "in force" vs "repealed" status in citations.
- Permission-aware retrieval: filter by ACL/tenant **in the query**, never post-hoc by the LLM.
- Cache retrieval results per normalized query + filters + corpus version for a short TTL if traffic repeats; a cache key that omits anything influencing the ranking changes answers silently.

## 10. Advanced patterns

- **Agentic RAG:** the model calls `search(query, filters)` as a tool, iterates, and stops when it has enough — better for complex questions, more cost/latency; cap steps.
- **Corrective RAG (CRAG):** grade retrieved docs; if poor, rewrite query or use another source.
- **Self-RAG style reflection:** model decides when to retrieve and critiques its use of evidence.
- **RAPTOR / hierarchical summaries:** tree of summaries for questions at different levels of abstraction.
- **Late-interaction retrieval (ColBERT-style):** token-level matching, strong quality, heavier index.
- **Long-context + cache vs RAG:** with large context windows and caching, sending a whole manual can beat a fragile RAG pipeline for small corpora — evaluate both.

## 11. Evaluating RAG (separately per stage)

- **Retrieval:** recall@k / hit rate (is the needed chunk in top k?), MRR, nDCG, context precision. Build a set of (question → relevant chunk ids).
- **Generation:** faithfulness/groundedness (claims supported by context), answer relevance, citation accuracy, abstention correctness (abstains when it should, answers when it can).
- Tools: Ragas, DeepEval, TruLens, Phoenix, or custom graders. See evals-observability.md.
- Track failure buckets: not retrieved / retrieved but not used / used but misinterpreted / hallucinated beyond sources.

## 12. Hard filters in SQL, never boosts

A property that makes a passage **unusable** (repealed, expired, not permitted for this user, wrong tenant, below a parse-quality floor) is a filter in the query, not a ranking feature.

- A boost can be outvoted by a high similarity score; a filter cannot. Wrong-version or unauthorized content that reaches the context can be quoted.
- Put the filter in the SQL `WHERE` of both the keyword and the vector leg, and apply it again when assembling context (defense in depth). Never rely on the prompt ("ignore repealed texts").
- Test it as a hard invariant in the eval: zero retrieved passages that violate the filter, across every query.
- Soft signals (recency, source authority) can be boosts; unusable states cannot.

## 13. Rank fusion

- Keyword scores (BM25, `ts_rank`) and cosine similarities have different scales and distributions; adding them is arbitrary. Fuse by **rank**.
- **Reciprocal Rank Fusion:** `score(d) = sum over lists of 1/(k + rank_i(d))`, with `k` commonly 60. The k=60 default comes from the original paper (Cormack, Clarke, Buttcher, SIGIR 2009); do not assume it is optimal: sweep k in {10, 30, 60} on a tune set, it is cheap and offline.
- pgvector's documentation points to RRF or a cross-encoder as the ways to combine vector search with Postgres full-text search.
- Postgres full-text notes: `ts_rank`/`ts_rank_cd` use no global corpus statistics, so they are not BM25 and scores are not comparable across queries; treat any minimum-score threshold as a heuristic recalibrated whenever the corpus changes. `websearch_to_tsquery` tolerates raw user text; `plainto_tsquery` ANDs all terms and loses recall on sloppy queries. Add the `unaccent` dictionary to the text-search configuration so unaccented queries match accented text.
- Keep the original query as one leg when rewriting or expanding, and let fusion merge candidates from all legs.

## 14. pgvector: HNSW, filtering and iterative scans

- An approximate index returns the nearest `ef_search` candidates (default 40) and the `WHERE` filter is applied **after** the index scan. With a filter matching 10% of rows, a default scan returns about 4 rows on average, so a `LIMIT 10` query comes back short.
- Remedies, in order: a **partial index** when the filter has few distinct values (for example `WHERE in_force`); **partitioning** when it has many (per tenant); an **exact scan** when the filter is highly selective; **iterative index scans** (pgvector 0.8.0 and later): `SET hnsw.iterative_scan = strict_order` keeps exact distance order, `relaxed_order` gains recall with slightly out-of-order results; scanning stops at `hnsw.max_scan_tuples` (default 20,000).
- Use `SET LOCAL` inside the transaction so settings do not leak through a transaction pooler.
- To use the index the query needs `ORDER BY <distance operator> ASC LIMIT n` with the raw operator; an extra tiebreak column in `ORDER BY` can force an exact scan. An exact scan is slower but has 100% recall, so a switch to the index is a precision decision: compare recall@k to the exact result (`SET LOCAL enable_indexscan = off`) on recorded queries before and after any change to index type, `m`, `ef_construction`, `ef_search`, or `halfvec`.
- Embedding task types: if the provider has them, index documents with the document type and embed queries with the query type; dimension truncation (Matryoshka) needs manual re-normalization when the provider only normalizes the full size. Changing embedding model or dimension means re-embedding the whole corpus and an A/B on the same cases.

## 15. Contextual chunk headers

- Chunks lose meaning alone ("the company's revenue grew 3%"). **Contextual Retrieval** (Anthropic) prepends a short, chunk-specific context (50-100 tokens, generated by an LLM from the whole document) before embedding and before building the keyword index.
- Reported results (top-20 retrieval failure rate): -35% with contextual embeddings, -49% adding contextual BM25, -67% adding reranking. Cost is paid once at indexing; with prompt caching the document is processed once, about US$1.02 per million document tokens at the prices quoted then. Gains vary by embedding model and corpus: test on your own set.
- For structured documents a **template header** (document title, section path, ancestors) often gets most of the gain without an LLM call.
- If chunk text is later **quoted or cited**, keep the original text in its own field and put the header only in the embedded/indexed text, so a citation never contains words the source did not.

## 16. Cross-encoder reranking

- A cross-encoder reads query and passage together and scores the pair; apply it to the top 50-100 candidates from hybrid retrieval and keep 5-15. It is the most robust single quality gain in retrieval benchmarks, at higher compute cost.
- Managed rerankers (for example Cohere, Voyage) work on results from any first stage without reindexing; check context limits, multilingual support and whether the score is calibrated. A calibrated 0-1 score allows cutting by threshold instead of by count (and supports abstention), but still calibrate on a tune set and confirm on a sealed one.
- Related-but-non-answering passages hurt generation more than random ones in some experiments ("Power of the Noise"), and models read the middle of long contexts poorly. Put the best passages first (and the next best last), and measure C as a function of context size and of the position of the needed passage before adding more candidates.

## 17. Query rewriting for sloppy questions

- Resolve what code can resolve first: typo repair, acronym expansion, pronouns from history, lay-term to domain-term glossary. It is auditable and free.
- LLM expansion: multi-query, decomposition, step-back, **HyDE** (embed a hypothetical answer; the dense encoder filters invented details) and query2doc (append a generated pseudo-document; reported +3% to +15% BM25 gains on MS-MARCO/TREC DL). Risk: the generated text may contain false facts.
- Mitigation by structure: the hypothetical text only **generates candidates**; the candidates still pass the hard filters and only passages that exist in the index reach the prompt or citations. Log the rewritten query next to the original and show the user how the question was understood when it matters.
- Abstaining on a vaguely worded question that has an answer is an error; resolve interpretation first, ask a clarifying question only when the ambiguity changes the answer.

## 18. Measure R before blaming the model

1. Define **R** as "every passage needed for the answer is in the context delivered to the model", computed offline with no LLM, from (question, expected passages) pairs.
2. If R is low, fix retrieval (filters, chunking, embeddings, fusion, rerank, rewriting) and **do not touch the prompt**; the prompt can only affect the generation factor.
3. When R is high and answers are still wrong, the problem is generation: prompt, model, context size/order, citation validation.
4. Keep a tune set (for iteration) and a sealed set (for the decision); a gain that appears only on the tune set is suspect (see evals-observability.md).
5. Retrieval benchmarks across collections show that BM25 stays competitive where queries carry lexical cues, and that rankings swap between collections; report per class and keep both legs.

## 18b. Index choice and filtering pitfalls (extra checks)

- Exact (flat) search is the correct baseline: measure approximate-index recall against it before tuning anything, and re-measure after data growth or an embedding change.
- Cost ladder: flat (simple, linear, fine for small corpora) → inverted-file/scalar-quantized (needs a training step) → product-quantized (compressed, lossy) → graph index (fastest, memory-heavy). Move up only when latency or memory forces it.
- Training-based indexes drift: if the data distribution shifts, retrain or rebuild; keep the build reproducible.
- Pure vector search blurs exact technical terms, codes and identifiers; always keep a keyword or metadata path next to it.
- Never mix vectors from different embedding models or versions in one index; a model change is a full re-embed plus a recall comparison before cut-over (build the new index beside the old one, then switch).
- Push the filter into the index query when the store supports it; a filter applied after a top-k scan silently returns fewer than k rows.
- Watch memory during index builds and keep a delete/update plan (tombstones, periodic rebuild) for corpora that change.

## Sources (read 2026-11-15 unless noted)

- pgvector README (filtering, iterative scans, ef_search, max_scan_tuples, hybrid search): https://raw.githubusercontent.com/pgvector/pgvector/master/README.md (read 2026-11-15)
- Anthropic, Introducing Contextual Retrieval: https://www.anthropic.com/news/contextual-retrieval (figures from study notes, read 2026-11-13; not re-verified)
- Cormack, Clarke, Buttcher, Reciprocal Rank Fusion, SIGIR 2009 (original paper not opened; k=60 as documented in practice; not re-verified)
- PostgreSQL docs, text search controls: https://www.postgresql.org/docs/current/textsearch-controls.html and unaccent: https://www.postgresql.org/docs/current/unaccent.html (study notes, 2026-11-13; not re-verified)
- Thakur et al., BEIR: https://arxiv.org/abs/2104.08663; Nogueira and Cho, passage re-ranking with BERT: https://arxiv.org/abs/1901.04085 (not re-verified)
- Cuconasu et al., The Power of Noise: https://arxiv.org/abs/2401.14887; Liu et al., Lost in the Middle: https://arxiv.org/abs/2307.03172 (abstracts, not re-verified)
- HyDE: https://arxiv.org/abs/2212.10496; Query2doc: https://arxiv.org/abs/2303.07678; Rewrite-Retrieve-Read: https://arxiv.org/abs/2305.14283 (abstracts, not re-verified)
- Chen et al., Dense X Retrieval (granularity): https://arxiv.org/abs/2312.06648 (abstract, not re-verified)
- Cohere and Voyage rerank documentation (study notes, 2026-11-13; not re-verified)

See also: `diagnosis-playbook.md` Trees 1-3 (ungrounded answers, wrong chunks, citation mismatch), `playbooks.md` section 3 (build and tuning loop), `variants/rag-qa.md`.

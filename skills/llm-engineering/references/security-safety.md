# LLM Security & Safety

Contents: 1 OWASP LLM Top 10 · 2 Lethal trifecta · 3 Engineering controls · 4 Privacy · 5 Domain safety · 6 Abuse · 7 OWASP 2025 applied · 8 Agents and untrusted content · 9 Ingested documents as evidence · 10 MITRE ATLAS · 11 Gap-pass additions

## 1. OWASP Top 10 for LLM Applications (2025 edition)

| Id | Risk | Main controls |
|---|---|---|
| LLM01 | **Prompt injection** (direct from users; indirect via documents, web pages, emails, tool results, images) | treat all model input from outside as data; separate/delimit untrusted content; least-privilege tools; authorization in code; human confirmation for consequential actions; output validation; don't put secrets in prompts; monitor |
| LLM02 | **Sensitive information disclosure** | minimize data sent; tenant/permission filtering before retrieval; redact PII in logs; provider data-use terms; no secrets in context |
| LLM03 | **Supply chain** (models, datasets, plugins, packages) | trusted sources, pinned versions, model provenance, review third-party tools/MCP servers |
| LLM04 | **Data and model poisoning** | control sources of fine-tuning/RAG data; validate ingested documents; provenance metadata; protect memory writes |
| LLM05 | **Improper output handling** | encode output for its context (HTML/Markdown), never `eval`; parameterized/allow-listed execution for SQL/commands; schema validation |
| LLM06 | **Excessive agency** | minimal tools and permissions; read-only by default; scoped credentials; approval steps; rate limits |
| LLM07 | **System prompt leakage** | assume the system prompt can be extracted — no secrets, keys or sensitive logic only enforced by the prompt |
| LLM08 | **Vector and embedding weaknesses** | permission-aware retrieval, tenant isolation in vector stores, poisoning checks, embedding inversion awareness for sensitive data |
| LLM09 | **Misinformation** (hallucination, overreliance) | grounding, citations, abstention, verification, UI that shows sources and uncertainty, human review for high stakes |
| LLM10 | **Unbounded consumption** (denial of service / denial of wallet, model extraction) | input size limits, output caps, rate limits and quotas per user/tenant, step caps, spend alerts |

OWASP also maintains guidance for **agentic applications** (tool misuse, memory poisoning, privilege compromise, cascading failures across agents) — apply the same principles to agent loops.

## 2. The "lethal trifecta" for agents

(Term coined by Simon Willison, 2025-06-16; see section 8.)

If one agent/session has **(1) access to private data + (2) exposure to untrusted content + (3) a way to communicate externally** (send email, HTTP requests, render images from URLs, write to shared places), a prompt injection can exfiltrate data. Remove at least one leg for that flow: no external communication tools, sanitize/strip URLs and images from outputs, or split into separate sessions with no shared privileged context.

## 3. Engineering controls

- Instructions vs data: wrap untrusted content in clear tags and state it is data; still assume it can override instructions — security must not depend on the prompt.
- Authorization is enforced **in tools**, using the authenticated user's identity — never the model's claims.
- Output rendering: Markdown → sanitize HTML; block or proxy external images/links in model output; no auto-following links.
- Structured outputs + validation reduce the injection blast radius (the model can only fill allowed fields).
- Input filters/classifiers (prompt-injection detectors, moderation) help as one layer, not the only one.
- Logs and alerts for unusual tool use, large outputs, repeated failures.
- Red-team tests in the eval suite: injected instructions in documents/tool outputs, attempts to reveal other tenants' data, jailbreaks relevant to your domain.

## 4. Privacy & compliance

- Data minimization: send only fields the task needs; pseudonymize ids.
- Check provider terms: data retention, use for training (API usually opt-out by default for paid tiers — verify), region/residency, zero-data-retention options, DPA.
- Health and wellness data and legal/government data are sensitive: explicit consent, purpose limitation, DPIA where required (GDPR in the EU and equivalent laws elsewhere).
- EU AI Act transparency: tell users when they interact with AI; label AI-generated content where required; human oversight for consequential decisions.
- Let users see and delete stored memory/profile data.

## 5. Domain safety

- **Health & fitness:** screen for injuries, medical conditions, pregnancy, extreme goals, signs of disordered eating; route to safe defaults and professional advice; cap intensity/volume and calorie deficits via code rules, not prompt wishes; disclaimers where appropriate.
- **Legal/government:** always cite the norm and its validity; distinguish analysis from decision; humans approve and sign; abstain without sources; never allege wrongdoing without evidence grade.
- **Finance:** no personalized investment advice unless licensed; numbers from code; audit trails.

## 6. Abuse & cost attacks

- Authentication before AI endpoints; per-user and per-IP rate limits; CAPTCHA/attestation on anonymous flows; maximum input length; reject huge files; quota per plan.

## 7. OWASP LLM Top 10 (2025) applied: what to test

| Id | Concrete check in a code review or eval |
|---|---|
| LLM01 Prompt injection | Eval cases with instructions hidden in documents, tool output, filenames, image text; assert no tool call, no data in output, no policy change. Output format validated by code. |
| LLM02 Sensitive information disclosure | Cross-tenant questions return nothing; logs and traces carry ids, not message content; pseudonymize personal names before the call; remember that "do not reveal X" in a prompt can be bypassed. |
| LLM03 Supply chain | Pinned model snapshots and package versions; review of third-party tools, MCP servers and model files (prefer safe serialization formats). |
| LLM04 Data and model poisoning | Provenance for every ingested document; review queue for corpus changes; memory writes validated. |
| LLM05 Improper output handling | Model text is encoded for HTML, never evaluated, never concatenated into SQL or shell; parameterized, allow-listed, read-only execution. |
| LLM06 Excessive agency | Inventory of tools with permission, side effect and approval status; remove the unused ones. |
| LLM07 System prompt leakage | Nothing in the prompt whose exposure would hurt: no keys, no authorization logic. |
| LLM08 Vector and embedding weaknesses | ACL/tenant filter inside the vector query; poisoning review of indexed text; access control on the vector store itself. |
| LLM09 Misinformation | Citations verified in code, abstention path, labels on generated content, human sign-off for consequential output. |
| LLM10 Unbounded consumption | Input size and output caps, per-tenant quotas, step and spend limits, timeouts, alerts on spend spikes. |

## 8. Agent security with untrusted content: the lethal trifecta

- **Origin:** Simon Willison (16 June 2025) named three capabilities that together make an agent exploitable: (1) access to private data, (2) exposure to untrusted content, (3) the ability to communicate externally in a way that can leak data. His conclusion is to avoid the combination entirely; guardrail filters are not dependable, because even a 95% detection rate is a failing grade for security.
- OWASP's Agentic Security Initiative publishes a threat-model-based guide, "Agentic AI - Threats and Mitigations" (v1.0, February 2025), covering risks that appear once models act: tool misuse, memory poisoning, privilege compromise, cascading failures (categories from general knowledge of the guide; not re-verified).
- **Design review question for every agent flow:** which of the three legs does it have? Remove one: no outbound channel (including image/URL rendering and link previews), no private data in this session, or no untrusted input.
- **Authorization of tool calls is enforced outside the model.** The tool server checks the authenticated user's identity and scopes on every call; the model's claim ("the admin approved this") is not evidence. Tool arguments are validated like any untrusted API input.
- **Human approval** for side-effecting tools (send, pay, delete, publish, write to shared stores): show the exact action and arguments to the person, who confirms in a separate channel the model cannot click through.
- **Least privilege and separation:** per-task credentials, read-only by default, separate sessions or agents for reading untrusted content and for acting, passing only validated structured data between them (never raw text).
- **Tool outputs, web pages, emails, tickets, and MCP server responses are untrusted data**, including their tool descriptions and metadata. Pin and review MCP servers, treat tool-description changes as a supply-chain event, and do not let one server's output select calls to another with higher privilege.
- **Memory is an attack surface:** validate what is written to long-term memory; do not store instructions as facts.
- Log every tool call with identity, arguments and result size; alert on unusual sequences (read private data then external call).
- Test with red-team cases per leg and keep them in the regression suite.
- Deterministic input screens catch only a fraction of injection attempts (a measured screen caught a minority of prompt-exfiltration attempts in one internal test), so use them as a tripwire and a signal, never as the control; the controls are structure, privilege and validation.
- Multi-tenant vector stores: partition by tenant with a mandatory filter in every query, never put one tenant's text in a shared cache key, and delete embeddings together with the source data on erasure (embeddings can leak the text they encode).

## 9. Ingested documents are evidence, never instructions

- Treat uploaded or crawled documents as hostile data: cite them, summarize them, extract fields from them, but never obey them. An imperative sentence inside a PDF ("ignore previous rules") is a finding to report.
- **Separate privileges for ingestion.** The parsing/OCR/extraction stage runs with no access to tenant secrets, no outbound network beyond what it needs, and no tools; its output is validated structured data plus provenance (source, hash, parse quality).
- Scan on ingestion for instruction-like text addressed to an AI and quarantine for review rather than silently indexing.
- At answer time fence the passages (see prompting-context.md section 12), keep policy in the system turn, and validate the output format and citations in code.
- Content from outside is **evidence with a source and a grade**, not a premise: store where it came from and when, and show it to the user as such.
- A status gate in code (for example the document is repealed, unverified or poorly parsed) decides whether a passage can be cited, regardless of what the passage says about itself.
- Never allow ingested text to modify system prompts, memory or retrieval filters.

## 10. MITRE ATLAS pointer

MITRE ATLAS is a knowledge base of adversary tactics and techniques against AI-enabled systems, modeled on ATT&CK. Use it to enumerate attack paths when threat-modeling an AI feature and to name findings consistently: https://atlas.mitre.org/ (page content not retrievable on 2026-11-15; description from general knowledge, not re-verified).

## 11. Gap-pass additions: model artifacts, AI incidents, voice (15/11)

Ideas cross-checked against an external knowledge base (AGPL), rewritten. Source tags are listed in the Sources section below (S11-1 to S11-4).

1. **Model weights are code until proven otherwise.** Prefer `safetensors` or another data-only format; never load a pickle-based checkpoint (`.pt`, `.bin`, `.pkl`) from a source you do not control, because unpickling can run arbitrary code. Import scanners help but are not foolproof. Take weights from publishers you trust, with signed commits. · S11-1
2. **Pin a model artifact by immutable revision (commit hash or digest), and enable `trust_remote_code`-style options only for a reviewed, pinned revision.** A moving tag lets an upstream change reach production unreviewed. · S11-1, OWASP LLM03
3. **Keep an inventory entry per model, dataset and fine-tune:** source, revision, hash, licence, owner, last evaluation date, where it runs. You cannot deactivate or audit what you have not listed. · S11-2 (GOVERN 1.6)
4. **Write the AI incident plan before launch:** what counts as an AI incident (cross-tenant leak, harmful output reaching users, successful injection, runaway spend), who decides, how to tell affected people, and an after-action review that updates the plan. · S11-2 (GV-1.5-002, MANAGE 4.3)
5. **Have a tested off switch per feature, tool and model** (flag or config, no deploy needed) and a decommissioning checklist: data retention, dependencies, leftover embeddings and caches. · S11-2 (GV-1.7-001, GV-1.7-002, MANAGE 2.4)
6. **Re-run the security and safety regression after every model, prompt, tool or retriever change,** and report over-refusal next to injection resistance; a defense that blocks half of valid requests is not a pass. · S11-2 (MEASURE 2.7; MS-2.7-001), engineering judgment
7. **A voice match never authorizes anything.** NIST's digital identity guidance does not accept voice comparison for authentication and treats biometrics as valid only alongside a physical authenticator; confirm sensitive voice-initiated actions through a second, non-voice step. · S11-3
8. **A transcript is untrusted input, equal to typed text.** Audio can carry instructions (played in the room, embedded in an uploaded recording); URLs, commands and entities extracted from speech go through the same allowlists and validation as any user input, and the tool layer still authorizes. · OWASP LLM01
9. **Bound audio resources per user and per tenant:** maximum duration and size, concurrent streams, timeouts on ASR and TTS calls, and a spend alert; long audio on a GPU is a denial-of-wallet path. · OWASP LLM10
10. **Synthetic speech and voice cloning need the speaker's recorded consent for a stated use, a visible AI label on the output, and generation logs.** EU AI Act transparency duties for synthetic audio (art. 50) apply; confirm the current text and dates with counsel. · AI Act pointer (art. 50 not re-opened for this pass)

## Sources (read 2026-11-15 unless noted)

- OWASP Top 10 for LLM Applications 2025 (ids and titles verified): https://genai.owasp.org/llm-top-10/
- OWASP LLM01 Prompt Injection: https://genai.owasp.org/llmrisk/llm01-prompt-injection/; LLM02: https://genai.owasp.org/llmrisk/llm022025-sensitive-information-disclosure/; LLM09: https://genai.owasp.org/llmrisk/llm092025-misinformation/ (2026-11-13; not re-verified)
- OWASP Agentic AI Threats and Mitigations v1.0 (Feb 2025): https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/ (title and date verified; categories not)
- Simon Willison, The lethal trifecta for AI agents (2025-06-16): https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/ (verified)
- Anthropic, Mitigate jailbreaks and prompt injections: https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks (2026-11-13; not re-verified)
- Beurer-Kellner et al., Design Patterns for Securing LLM Agents against Prompt Injections: https://arxiv.org/abs/2506.08837 (abstract, 2026-11-13; not re-verified)
- MITRE ATLAS: https://atlas.mitre.org/
- S11-1 Hugging Face Hub docs, Pickle Scanning (read 2026-11-15): https://huggingface.co/docs/hub/security-pickle
- S11-2 NIST AI 600-1, AI RMF Generative AI Profile (July 2024; GOVERN 1.5, 1.6, 1.7, MEASURE 2.7, MANAGE 2.4, 4.3 read in the PDF 2026-11-15): https://doi.org/10.6028/NIST.AI.600-1
- S11-3 NIST SP 800-63B-4 section 3.2.3 (read 2026-11-15): https://pages.nist.gov/800-63-4/sp800-63b.html

See also: `diagnosis-playbook.md` Tree 9 (injection triage), `playbooks.md` sections 6-7 (agent checklist, incident response).

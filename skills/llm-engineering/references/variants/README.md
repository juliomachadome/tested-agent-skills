# Variants: choose by feature type

Pick the row that matches the feature, open that one file, then follow its links into the deep references. If the feature mixes types (a chat assistant that does RAG and calls tools), start with the dominant risk and read the second file for its failure modes only.

| The feature mainly... | Variant | Dominant risk | Main metric |
|---|---|---|---|
| answers questions from your documents, with sources | `rag-qa.md` | ungrounded or wrongly cited answer | retrieval recall, faithfulness, citation precision, abstention both ways |
| takes actions through tools, runs loops, touches other systems | `agents-tools.md` | side effects, injection, runaway cost | task success on checkable end states, injection pass rate |
| labels, scores, routes or extracts fields into a schema | `classification-extraction.md` | silent wrong label, schema drift | per-class precision and recall, field accuracy, Wilson interval |
| holds a multi-turn conversation with memory and persona | `chat-assistant.md` | drift, leakage between users, unbounded context | conversation-level success, escalation rate, cost per conversation |
| writes, rewrites, summarises or translates text | `summarisation-generation.md` | unfaithful content, tone and brand errors | faithfulness to source, rubric score, human acceptance |
| measures and watches any of the above | `evals-and-monitoring.md` | an unmeasured change, a drifting judge | n with interval, paired wins and losses, drift alarms |

Not covered here, routed to the existing references: speech-to-text (`../speech-asr.md`), knowledge graphs (`../graphs-knowledge.md`), model choice and fine-tuning (`../models-providers.md`), text-to-SQL and voice agents (`../use-cases.md`).

Always, for every variant: read `../diagnosis-playbook.md` Step 0 when something is wrong, use `../playbooks.md` to ship it, and check prices and limits on the vendor page the day you decide (`../BIBLIOGRAPHY.md`, entries 1-14).

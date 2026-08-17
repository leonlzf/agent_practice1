# Model and System Change Policy

Changes to the model, prompt, embedding model, chunking, reranker, index, tools, permissions, or
workflow graph require impact assessment and risk-based regression testing.

At minimum, every evaluated run must record:

- code commit;
- model version;
- prompt version;
- index version;
- evaluation-set version;
- metric implementation version.


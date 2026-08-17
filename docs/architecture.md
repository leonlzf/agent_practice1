# Architecture

```text
FastAPI request
    ↓
Scope and risk classification
    ↓
Controlled workflow safeguards
    ↓
Deterministic routing
    ↓
Validated tool registry
    ├── Policy retrieval
    └── Deterministic calculator
    ↓
Evidence sufficiency and citation verification
    ↓
Answer / abstain / escalate / refuse
    ↓
Versioned, redacted audit events
```

The current scaffold implements schemas, safe defaults, tool boundaries, baseline metrics, and
audit event models. Retrieval and model-backed workflow nodes remain intentionally unimplemented.

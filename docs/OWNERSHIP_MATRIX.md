# Ownership Matrix

Status: Sprint 01 output

## Principle

Imprint owns the transformation from evidence to expression profile. It does not own every system
that produces evidence or every system that consumes the resulting profile.

| Capability | Owner | Upstream Dependencies | Downstream Consumers | Rationale |
| --- | --- | --- | --- | --- |
| Ingestion | Imprint for normalization; source systems for raw records | local files, exports, configured private sources | artifact registry, classifier | Imprint needs normalized artifacts, but source systems remain the raw-data owners. |
| Storage | Imprint for local artifact/profile registry; external systems for original data | normalized artifacts, classifications, signals | compiler, audit, diff | Imprint stores only what it needs to compile and audit profiles, not a general memory store. |
| Embeddings | Optional Imprint component or provider adapter | normalized artifacts, configured embedding provider | search, clustering, optional extraction | Embeddings can help, but must not become required for the local MVP. |
| Classification | Imprint | artifacts, source metadata, speaker hints | extractor, compiler, audit reports | Authorship, speaker confidence, AI assistance, and quote risk are core safety gates. |
| Signal extraction | Imprint | classified artifacts, source policy, optional LLM provider | profile compiler, first-run report | Extracted observations are the core product material. |
| Profile compilation | Imprint | signals, classifications, source weights, exclusions | exporters, downstream consumers | The compiled profile is Imprint's central contract. |
| Drift | Imprint | profile versions, time windows, extractor/model versions | first-run updates, downstream refresh decisions | Drift belongs with profile versioning, not with each consumer. |
| Evaluation | Shared: Imprint validates profile quality; downstream validates generated output | profiles, synthetic eval corpus, downstream outputs | maintainers, consumers | Imprint can evaluate profile correctness and privacy, but consumers evaluate task success. |
| Export generation | Imprint | canonical profile, export mode, target contract | Mosvera, publishing systems, agents, reports | Exporters are projections of the canonical profile, not separate source-of-truth profiles. |
| Publishing | Downstream publishing systems | Imprint profile or publishing export | readers, content workflows | Publishing systems generate and manage drafts; Imprint only provides expression guidance. |
| Persona generation | Downstream agent/persona systems | Imprint profile, user consent, consumer policy | agents, simulations, assistants | Persona behavior is broader and riskier than expression profiling. Imprint should not claim to be a person. |

## Boundary Notes

### Ingestion

Imprint can ship local public adapters and generic connector interfaces. Private connectors must be
configured externally and tested with synthetic fixtures.

### Storage

SQLite as default local storage is reasonable. Postgres support can exist later, but database
choice must not encode private deployment assumptions.

### Embeddings

Embeddings are optional infrastructure. They should not be required for first-run value or schema
validity.

### Classification

Classification is the main safety layer. It must happen before extraction and compilation.

### Signal Extraction

Signals must stay bounded to observable expression patterns. Extraction should not infer mental
health, intent, personality type, or hidden motives.

### Profile Compilation

Compilation should be deterministic where possible and auditable always. Profiles should expose
source counts, confidence, version metadata, and sample policy.

### Evaluation

Imprint should evaluate:

- schema validity
- privacy safety
- evidence coverage
- contamination handling
- regression stability

Downstream systems should evaluate:

- draft quality
- audience fit
- task success
- brand compliance

### Exports

Canonical Imprint JSON/YAML should remain the source of truth. Consumer-specific exports should be
thin projections.

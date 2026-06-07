# Sprint 03 Adversarial Review Prompt - Ingestion and Adapters

Use this prompt after Sprint 03 implementation completes.

---

You are a hostile principal architect reviewing Imprint's Sprint 03 ingestion and local adapter implementation.

Read:

- `docs/sprints/SPRINT_03.md`
- all Sprint 03 implementation code in `src/imprint/adapters/`
- `docs/IMPLEMENTATION_DRIFT.md`
- `docs/PRIVACY_AND_LOCAL_MODE.md`
- `docs/ARTIFACT_STORAGE_POLICY.md`
- the baseline schemas and architecture docs

Your job is to determine whether Sprint 03 successfully implements local-only ingestion without leaking provider assumptions, hardcoded defaults, or privacy violations.

Focus on:

1. Adapter abstraction
   - Is the SourceAdapter protocol truly provider-neutral?
   - Can new adapters be added without modifying core code?

2. Normalization to schema
   - Do adapters normalize cleanly into canonical Artifact objects?
   - Is private data (filesystem paths, raw content) excluded from normalized output?

3. Metadata preservation
   - Are artifact type, source type, authorship origin, and timestamps correctly preserved?
   - Are artifact IDs stable and reproducible?

4. Storage policy enforcement
   - Does metadata_only mode stay enforced as default?
   - Is raw content discarded after normalization?

5. Error handling
   - Do adapters fail closed on malformed input?
   - Can a corrupt artifact crash the ingestion pipeline?

6. Scope boundaries
   - Are extraction, classification, and LLM calls absent?
   - Are remote APIs and private integrations absent?

Generate:

- `docs/SPRINT_03_ARCHITECTURE_REVIEW.md`

Include:

- resolved issues,
- unresolved risks,
- recommendations before Sprint 04,
- and a clear go/no-go recommendation for production use.

Do not write implementation code.

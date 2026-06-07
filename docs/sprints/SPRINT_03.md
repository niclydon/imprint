# Sprint 03 - Artifact Registry and Local Adapters
Primary Model: GPT 5.4
Adversarial Reviewer: Claude

Status:
Implemented

Objective:
Implement local_text, local_markdown, local_jsonl and local_transcript_json ingestion.

Primary Prompt:
Build adapter registry, source interfaces and artifact registry. No network access, credentials or private integrations.

Reviewer Prompt:
Compare implementation to PROJECT_STRATEGY, ARCHITECTURE and SECURITY_PRIVACY. Generate IMPLEMENTATION_DRIFT.md and identify architectural drift.

Implemented behavior:

- Added a source adapter interface and adapter registry for local-only ingestion.
- Implemented `local_text`, `local_markdown`, `local_jsonl`, and `local_transcript_json`.
- Normalized adapter output into canonical schema objects: `ArtifactReference`, `ArtifactClassification`, `ArtifactStoragePolicy`, and `Artifact`.
- Kept storage defaulted to `metadata_only` and did not introduce raw-text persistence.
- Added synthetic fixtures and adapter tests.
- Added a minimal `imprint ingest` CLI command that reports normalized artifact counts.

Explicit non-goals preserved:

- no Gmail, iMessage, Plaud, Looki, SQL, or Nexus DB access
- no remote APIs or model-provider calls
- no embeddings, extraction prompts, or LLM classification
- no provider-specific code or private path assumptions

## Sprint 02.5 Carry-Forward: Model Provider Policy

Sprint 03 ingestion must preserve BYOM/BYOP boundaries:

- do not choose or hard-code a default model provider,
- keep remote inference optional and visible,
- record profile-affecting model invocations in build manifests,
- keep experience-only generation out of durable profiles unless explicitly promoted through evidence and validation,
- avoid API keys, private base URLs, and provider-specific SDK assumptions in canonical schemas.

# Sprint 03 - Artifact Registry and Local Adapters
Primary Model: GPT 5.4
Adversarial Reviewer: Claude

Objective:
Implement local_text, local_markdown, local_jsonl and local_transcript_json ingestion.

Primary Prompt:
Build adapter registry, source interfaces and artifact registry. No network access, credentials or private integrations.

Reviewer Prompt:
Compare implementation to PROJECT_STRATEGY, ARCHITECTURE and SECURITY_PRIVACY. Generate IMPLEMENTATION_DRIFT.md and identify architectural drift.

## Sprint 02.5 Carry-Forward: Model Provider Policy

Sprint 03 ingestion must preserve BYOM/BYOP boundaries:

- do not choose or hard-code a default model provider,
- keep remote inference optional and visible,
- record profile-affecting model invocations in build manifests,
- keep experience-only generation out of durable profiles unless explicitly promoted through evidence and validation,
- avoid API keys, private base URLs, and provider-specific SDK assumptions in canonical schemas.

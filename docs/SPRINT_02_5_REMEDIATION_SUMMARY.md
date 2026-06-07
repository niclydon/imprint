# Sprint 02.5 Remediation Summary

Status: Sprint 02.5 complete

## What Changed

Sprint 02.5 added a provider-neutral model policy layer without implementing runtime inference.

Created:

- `docs/MODEL_PROVIDER_POLICY.md`
- `docs/MODEL_ROLE_TAXONOMY.md`
- `docs/MODEL_CAPABILITY_CONTRACTS.md`
- `docs/MODEL_PRIVACY_BOUNDARIES.md`

Updated:

- `docs/EXTRACTOR_VERSIONING.md`
- `docs/PRIVACY_AND_LOCAL_MODE.md`
- `docs/EVIDENCE_AND_CONFIDENCE.md`
- `docs/SCHEMA.md`
- `docs/sprints/SPRINT_03.md`

Patched schema contracts:

- model role taxonomy
- provider kind taxonomy
- model capability flags
- model execution environment
- provider retention/training policy fields
- profile-affecting model invocation records in `BuildManifest`

## Decisions Encoded

1. Imprint is BYOM/BYOP.
2. Canonical schemas remain provider-neutral.
3. Profile-affecting inference is recorded in the build manifest.
4. Experience-only generation cannot mutate durable profiles without explicit promotion through evidence and validation.
5. Remote provider use is visible and privacy-sensitive.
6. Local-first operation remains possible.

## Non-Goals Preserved

Sprint 02.5 did not add model clients, provider SDKs, API keys, embeddings, LLM extraction, private integrations, or homelab-specific assumptions.

## Sprint 03 Readiness

Sprint 03 can implement ingestion without choosing a default model provider. Ingestion must preserve model role metadata and keep remote inference optional.

# Sprint 02.5 Prompt - Model Provider and Inference Policy

Use this prompt with GPT 5.5 from the repository root.

---

You are the Model Policy Architect for Imprint.

Sprint 02 schema work is already underway or complete. Your task is Sprint 02.5: Model Provider and Inference Policy.

Do not restart Sprint 02.
Do not rewrite the whole schema layer unless absolutely necessary.
Do not add actual model clients.
Do not add provider-specific implementation.
Do not add private or homelab-specific assumptions.

Read:

- `docs/sprints/SPRINT_02_5.md`
- `docs/EXTRACTOR_VERSIONING.md`
- `docs/PRIVACY_AND_LOCAL_MODE.md`
- `docs/EVIDENCE_AND_CONFIDENCE.md`
- `docs/ARTIFACT_STORAGE_POLICY.md`
- `docs/EXPORT_BOUNDARIES.md`
- `docs/SCHEMA.md`
- all Sprint 02 outputs and schemas if present

Create:

- `docs/MODEL_PROVIDER_POLICY.md`
- `docs/MODEL_ROLE_TAXONOMY.md`
- `docs/MODEL_CAPABILITY_CONTRACTS.md`
- `docs/MODEL_PRIVACY_BOUNDARIES.md`
- `docs/SPRINT_02_5_REMEDIATION_SUMMARY.md`

Update as needed:

- `docs/EXTRACTOR_VERSIONING.md`
- `docs/PRIVACY_AND_LOCAL_MODE.md`
- `docs/EVIDENCE_AND_CONFIDENCE.md`
- `docs/SCHEMA.md`
- `docs/sprints/SPRINT_03.md`

Core decisions to encode:

1. Imprint is BYOM/BYOP: bring your own model and provider.
2. Canonical schemas must be provider-neutral.
3. Profile-affecting inference must be recorded in the build manifest.
4. Experience-only generation must not mutate the durable profile unless explicitly promoted through validated evidence.
5. Model roles must be explicit.
6. Model capabilities must be declared.
7. Remote provider use must be visible and privacy-sensitive.
8. Local-first operation must remain possible.

If Sprint 02 introduced schema assumptions that conflict with this policy, patch the docs and propose minimal schema changes.

If code changes are necessary, keep them limited to schema contracts and tests. Do not implement runtime inference.

# Implementation Drift

Status: Sprint 03 review

## Alignment

- Local-only adapters preserve the local-first default described in `PRIVACY_AND_LOCAL_MODE.md`.
- Adapter output normalizes into existing schema contracts without adding provider-specific fields.
- The implementation keeps `metadata_only` as the default artifact storage mode.
- The CLI is limited to normalization and reporting; it does not introduce extraction or downstream generation concerns.

## Intentional Constraints

- Raw text is read only in-process for normalization and hashing, then discarded.
- Transcript and JSONL parsing fail closed on malformed input rather than guessing missing semantics.
- No connector, SQL, or Nexus-specific code is included in Sprint 03.

## Deferred Work

- Real local artifact-store persistence remains future work.
- Nexus DB ingestion is deferred to a dedicated adapter sprint.
- Classification, evidence extraction, and profile compilation remain out of scope for this implementation.

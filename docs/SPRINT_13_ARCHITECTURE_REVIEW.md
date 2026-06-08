# Sprint 13 Architecture Review: Private Adapter Strategy

**Review Date:** 2026-06-08
**Reviewer Role:** Hostile Privacy/Security Architect
**Status:** GO FOR PRIVATE ADAPTER IMPLEMENTATION PLANNING
**Go/No-Go:** **GO** for source-specific private adapter implementation planning; **NO-GO** for building real adapters without the documented gates

---

## Executive Summary

Sprint 13 correctly stays in strategy and threat-model territory. It does not add Gmail, iMessage,
Plaud, Looki, database, OAuth, live API, cloud, service-mode, raw corpus storage, or UI review-flow
implementations. Instead, it creates the missing source-specific threat models and cross-cutting
standards required before private adapters can safely exist.

The public/private boundary remains intact: public core still contains only generic local connector
framework behavior and synthetic examples. The new docs explicitly block implementation until each
source has threat modeling, credential handling, consent boundaries, replay/audit policy, and
synthetic fixture tests.

## Reviewed Artifacts

- `docs/GMAIL_CONNECTOR_THREAT_MODEL.md`
- `docs/IMESSAGE_CONNECTOR_THREAT_MODEL.md`
- `docs/TRANSCRIPT_CONNECTOR_THREAT_MODEL.md`
- `docs/DATABASE_CONNECTOR_THREAT_MODEL.md`
- `docs/CREDENTIAL_STORAGE_POLICY.md`
- `docs/CONSENT_AND_MULTI_PERSON_POLICY.md`
- `docs/CONNECTOR_IMPLEMENTATION_STANDARD.md`
- `docs/CONNECTOR_SYNTHETIC_FIXTURE_STANDARD.md`
- `docs/CONNECTOR_FRAMEWORK.md`
- `docs/PRIVATE_CONNECTOR_POLICY.md`
- `docs/CONFIGURATION.md`
- `docs/ROADMAP.md`
- `src/imprint/connectors/`
- `tests/test_connectors.py`

## Findings

### 1. Consent Failures

**Decision:** Addressed for planning.

The consent policy states that source possession is not enough and that only subject-authored content
is eligible by default. Gmail, chat, transcript, and database threat models all identify third-party,
unknown, quoted, forwarded, generated, system, and group-context contamination. Ambiguous authorship
falls to quarantine rather than inclusion.

**Residual risk:** Future implementations must prove these rules in tests. The docs are sufficient to
start implementation planning, not to waive implementation review.

### 2. Credential Storage Mistakes

**Decision:** Addressed for planning.

The credential policy forbids inline secrets in config, docs, fixtures, exports, logs, and build
metadata. It allows env var references and requires fail-closed behavior, redaction, scope
minimization, rotation, and revocation planning. Source threat models add specific constraints for
OAuth, local databases/backups, transcript vendor credentials, and database DSNs.

**Residual risk:** A future credential provider must be reviewed as private infrastructure and must
not become a public-core dependency by accident.

### 3. Multi-Person Data Contamination

**Decision:** Addressed for planning.

Each source-family threat model explicitly separates subject-authored material from other speakers,
participants, recipients, database subjects, generated summaries, and system messages. The connector
standard preserves the existing architecture: connector hints are advisory and classification remains
responsible for authorship and inclusion decisions.

**Residual risk:** Group chat and transcript diarization are high-risk implementation areas and should
be test-first if implemented.

### 4. Replay and Audit Gaps

**Decision:** Addressed for planning.

Each threat model defines replay metadata and local audit summary requirements. The implementation
standard requires connector/parser versions, source policy versions, storage mode, counts,
credential-reference names, skipped source classes, and replay limitations.

**Residual risk:** Replay from live mutable sources remains weaker than replay from pinned synthetic
or ignored local snapshots. Future connectors must disclose that limitation in build manifests or
local audit output.

### 5. Public/Private Repo Leakage

**Decision:** Addressed.

The private connector policy and fixture standard forbid real credentials, real source paths, real
account IDs, real corpora, real provider responses, private schemas, local databases, exports, and
credential-shaped placeholders in public docs and fixtures. Public-core admission is limited to
generic, synthetic-testable code that runs without private infrastructure.

**Residual risk:** Future docs for source-specific setup can accidentally expose private provider or
machine details. Those docs require the same public-release scan discipline as code.

### 6. Adapter Authority Creep

**Decision:** Addressed.

The connector implementation standard says connectors ingest only. They may discover, normalize,
attach advisory hints, report counts, and fail closed. They must not classify, extract signals,
compile profiles, export profiles, assemble prompts, call LLMs, publish content, expose raw corpus
search, or bypass validation.

**Residual risk:** Private connector packages outside public core can still drift. They should depend
on public Imprint interfaces and run the same validation suite before exporting profiles.

### 7. Source-Specific Privacy Holes

**Decision:** Addressed for planning.

The four source threat models cover the major privacy holes:

- Gmail: OAuth scope, sent-vs-received separation, quoted threads, attachments, provider metadata.
- iMessage/chat: local database access, participant consent, group contamination, sender attribution,
  attachments, device boundaries.
- Transcript/recorder: speaker consent, diarization uncertainty, third-party voices, audio/text
  separation, generated summaries.
- Database/cloud: query allowlists, DSN redaction, least privilege, row-level privacy, replay limits,
  private schema leakage.

## Blockers

None for private adapter implementation planning.

Real private adapter implementation remains blocked until the source-specific implementation has
synthetic fixtures, redaction tests, consent-boundary tests, replay/audit tests, and credential tests.

## Recommendations

1. Treat Gmail quoted-thread parsing, group chat participant separation, transcript diarization, and
   database row-level filtering as test-first implementation units.
2. Keep private connector packages out of public core unless they can run in public CI without
   credentials or private infrastructure.
3. Require a public-safety scan before committing any source-specific docs or fixtures.
4. Add fixture mutation tests for Sprint 12.5 privacy gates when the first private connector is
   implemented.
5. Keep service/API mode blocked until private connector replay/audit behavior is proven.

## Final Decision

**GO** for source-specific private adapter implementation planning.

**NO-GO** for building real private adapters directly from the generic connector framework without
satisfying the Sprint 13 threat models, credential policy, consent policy, implementation standard,
and synthetic fixture standard.

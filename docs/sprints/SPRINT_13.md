# Sprint 13 - Private Adapter Strategy and Threat Models

Primary Model: GPT 5.5 for design, GPT 5.4 for implementation planning
Adversarial Reviewer: GPT 5.5 or Gemini Antigravity
Status: Complete as Sprint 13 strategy and threat-model gate

## Mission

Define the safe implementation strategy for real private source adapters without adding private assumptions, credentials, corpora, or source-specific coupling to public core.

Sprint 13 is a strategy and threat-model sprint. It does not build real Gmail, iMessage, Plaud, Looki, database, or cloud adapters.

## Required Reading

- `docs/ROADMAP.md`
- `docs/SPRINT_09_ARCHITECTURE_REVIEW.md`
- `docs/CONNECTOR_FRAMEWORK.md`
- `docs/PRIVATE_CONNECTOR_POLICY.md`
- `docs/CONFIGURATION.md`
- `docs/SECURITY_PRIVACY.md`
- `docs/ARTIFACT_STORAGE_POLICY.md`
- `docs/PRIVACY_AND_LOCAL_MODE.md`
- `src/imprint/connectors/`
- `tests/test_connectors.py`

## Core Rule

No private adapter implementation starts without a source-specific threat model, synthetic fixtures, credential rules, consent boundaries, and replay/audit policy.

## Required Deliverables

Create:

- `docs/GMAIL_CONNECTOR_THREAT_MODEL.md`
- `docs/IMESSAGE_CONNECTOR_THREAT_MODEL.md`
- `docs/TRANSCRIPT_CONNECTOR_THREAT_MODEL.md`
- `docs/DATABASE_CONNECTOR_THREAT_MODEL.md`
- `docs/CREDENTIAL_STORAGE_POLICY.md`
- `docs/CONSENT_AND_MULTI_PERSON_POLICY.md`
- `docs/CONNECTOR_IMPLEMENTATION_STANDARD.md`
- `docs/CONNECTOR_SYNTHETIC_FIXTURE_STANDARD.md`

Update:

- `docs/PRIVATE_CONNECTOR_POLICY.md`
- `docs/CONNECTOR_FRAMEWORK.md`
- `docs/CONFIGURATION.md`
- `docs/ROADMAP.md`

## Threat Model Requirements

Each source-specific threat model must cover:

- source ownership and consent
- multi-person data risk
- credential handling
- local storage and retention
- replay/rebuild behavior
- audit and revocation
- source-specific privacy leaks
- adapter hint trust boundaries
- synthetic fixture requirements
- public repo safety constraints

## Source Families

### Gmail / Sent Mail

Focus on OAuth scope minimization, sent-vs-received separation, quoted thread contamination, multi-party consent, attachments, and provider retention.

### iMessage / Chat Export

Focus on local database access, participant consent, group chat contamination, sender attribution, quoted/forwarded content, and device-specific privacy boundaries.

### Transcript Sources

Focus on speaker attribution, recorder consent, diarization uncertainty, third-party voices, audio/transcript separation, and source provenance.

### Database / Cloud Sources

Focus on query allowlisting, DSN redaction, least privilege, row-level privacy, replay, and controlled synthetic fixtures.

## Non-Goals

Do not implement:

- Gmail connector
- iMessage connector
- Plaud/Looki connector
- database connector
- OAuth flows
- live APIs
- service mode
- raw corpus storage
- UI review flows

## Exit Criteria

Sprint 13 is complete when:

- each future adapter class has a threat model
- credential storage policy is explicit
- consent and multi-person data boundaries are explicit
- synthetic fixture standards exist
- implementation standards prevent adapter authority creep
- public/private repo boundaries remain intact
- all tests pass

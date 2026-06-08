# Sprint 13.5 Architecture Review: Private Adapter Enforcement Foundation

**Review Date:** 2026-06-08
**Reviewer Role:** Hostile Privacy/Security Architect with focused subagent fan-out
**Status:** GO FOR PRIVATE ADAPTER IMPLEMENTATION PLANNING
**Go/No-Go:** **GO** for implementation planning; **NO-GO** for real adapters that skip these contracts

---

## Executive Summary

Sprint 13.5 closes the Sprint 13 enforcement gaps without implementing real Gmail, iMessage,
transcript, database, cloud, OAuth, live API, service, UI, or raw corpus storage behavior.

The sprint adds concrete contracts and tests for consent boundaries, credential redaction, replay
manifests, audit logs, fixture leakage scanning, and connector authority boundaries. Focused
adversarial subagents initially returned NO-GO findings across consent, redaction/leakage, and
replay/audit/authority. Those findings were addressed before this final review.

## Review Method

Three focused adversarial reviews were run against the current worktree:

- consent bypass and third-party content contamination
- credential redaction and public/private repository leakage
- replay/version ambiguity, audit log leakage, and connector authority creep

The reviewers found actionable P1 issues. The final review includes only issues after remediation.

## Findings

### 1. Consent Bypasses

**Decision:** Fixed.

Sprint 13.5 adds `ConsentClass`, `ConsentAction`, `ConsentBoundary`, and `ConsentBoundaryResult` in
`src/imprint/connectors/consent.py`. Classification evaluates consent hints and records consent class,
action, and reason codes in `source_hints_considered`.

Resolved adversarial issues:

- private-family aliases such as `sent_mail`, `chat`, and `transcript` now fail closed when consent
  hints are absent
- explicit received mail is excluded
- group chat participant content is quarantined
- third-party transcript speakers are excluded
- transcript segments require explicit `speaker_role` before durable subject-authored inclusion

Remaining boundary: future real connectors must add source-specific fixtures and tests before they
can rely on these generic consent contracts.

### 2. Third-Party Content Contamination

**Decision:** Fixed for the Sprint 13.5 foundation.

The classifier applies consent actions after authorship/contamination scoring, so `exclude` overrides
potential inclusion and `quarantine` prevents durable support unless future policy explicitly allows
it. The compiler already ignores non-included classifications, so consent downgrades block durable
profile support.

### 3. Credential Redaction Failures

**Decision:** Fixed.

Connector redaction now covers:

- OAuth-style refresh/access tokens
- JWTs
- database DSNs with embedded credentials
- API keys in URL query parameters
- AWS access keys
- Azure-style connection strings
- bearer/basic authorization values
- local home paths

Resolved adversarial issue: nested `env` mappings no longer leak secret values or secret-like nested
keys; only safe env var name strings such as `IMPRINT_SYNTHETIC_TOKEN` remain visible.

### 4. Replay and Version Ambiguity

**Decision:** Fixed for the foundation.

`ConnectorReplayManifest` records connector, adapter, parser, source policy, storage mode, config
hash, synthetic/private fixture state, manifest version, and replay limitations. Compatibility checks
include manifest version and all drift-sensitive fields.

Resolved adversarial issue: config hashes are computed over redacted config shape instead of raw
caller-supplied secrets, paths, or private values.

### 5. Audit Log Leakage

**Decision:** Fixed.

`ConnectorAuditLog.to_public_safe_dict()` now returns an allowlisted public-safe payload. It preserves
counts, connector identifiers, storage mode, source policy version, replay manifest reference, and
safe metadata keys. It replaces warning/error content with numbered placeholders and excludes
arbitrary metadata keys that could contain raw artifact text.

### 6. Public/Private Repository Leakage

**Decision:** Fixed for the identified leak class and foundation scanner.

Sprint 13.5 adds `scan_fixture_path` and `scan_fixture_tree` for fixture leakage detection. The
scanner catches unsafe fixture names, real-looking emails, phone numbers, private URLs, local home
paths, account IDs, DSNs, plaintext credential/token shapes, and base64/base64url-encoded credentials
or local paths.

A narrative doc that contained private file-share handoff details was sanitized, and a regression test
now rejects those private handoff terms in public narratives.

### 7. Connector Authority Creep

**Decision:** Fixed for public-core connector modules.

Connector tests recursively scan connector modules to reject imports or calls into classifier, signal
extractor, compiler, exporter, LLM/provider, and network/API authority. This preserves the connector
contract: connectors ingest only.

## Blockers

None remaining for private adapter implementation planning.

Real private adapter implementation remains blocked unless the source-specific connector adds its own
threat-model mapping, synthetic fixtures, consent tests, redaction tests, replay/audit tests, and
public-safe export validation.

## Recommendations

1. Keep the first real private connector test-first, starting with consent and leakage fixtures.
2. Add replay manifest fields into profile build metadata before connector-driven profiles are
   compared as expression drift.
3. Keep source-specific connectors outside public core unless they are synthetic-testable and pass the
   recursive authority scan.
4. Treat audit logs as protected local records unless a public-safe projection is explicitly needed.

## Final Decision

**GO** for private adapter implementation planning.

**NO-GO** for real private adapters that bypass Sprint 13.5 consent, replay, audit, redaction,
fixture leakage, and authority-boundary contracts.

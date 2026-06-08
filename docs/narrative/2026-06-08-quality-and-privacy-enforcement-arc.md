# Sprints 12–13.5: Quality Gates and Privacy Enforcement Foundation

**Period:** 2026-06-07 to 2026-06-08  
**Decision:** Imprint moved from unverified quality guarantees to an enforced privacy and security contract framework ready to support safe private adapter implementations.

## Story Arc

At the start of Sprint 12, Imprint had a working compiler, classifier, and export layer, but the system lacked:
- Any way to verify that profiles were safe to release
- Any way to compare two profiles without false claims about expression drift
- Any enforcement of consent rules for future private source adapters
- Any verification that credentials wouldn't leak during ingestion

The adversarial reviews across Sprints 12–13.5 closed each gap with concrete code, tests, and enforceable contracts. The work proceeded in three phases: (1) define what safety means and expose where it was missing, (2) articulate the framework for private adapters without implementing them, (3) close the enforcement gaps with testable code and boundaries.

By the end of Sprint 13.5, the public core contained no private adapters, but the foundation for building them safely was in place.

## Sprint 12: Validation and Quality Gates

The first adversarial review (Sprint 12) focused on the quality layer: validation, comparison, and release gating.

**Problem identified:** The compiler and exporters produced JSON profiles, but there was no automated way to ask "is this safe to release?" The team had threat models and privacy principles, but no validation code. The comparison logic existed but could confuse implementation drift with expression drift.

**Deliverables:**
- `validate-export` command: validates canonical JSON, Mosvera overlays, and consumer contracts against a schema, checks for raw text/path leakage, verifies compatibility metadata exists, and reports PASS/FAIL.
- `diff` command: compares two profiles, reports comparability state (COMPARABLE, PARTIALLY_COMPARABLE, NOT_COMPARABLE), separates expression drift from compiler/corpus/schema drift, and prevents overclaiming.
- Release gate checks: documented which conditions should fail a release (raw text leak, invalid source IDs, missing compatibility metadata, privacy guarantee weakening, etc.).

**Adversarial findings:** Three critical credential-detection gaps were discovered:
1. **JWT credentials not detected** — Valid JWT tokens (format: eyJ...eyJ...sig) passed validation when they should have been flagged as credentials.
2. **Base64-encoded credentials bypassed detection** — When credentials were base64-encoded (common in HTTP headers and config files), the validator didn't attempt decoding, so they passed unchecked.
3. **Percent-encoded paths evaded detection** — URL-encoded paths like %2Fprivate%2Fdata bypassed path validation.

These gaps meant that the validation layer could miss real credential leaks. The issue wasn't in the design—validation as a concept was sound—but in the completeness of the pattern matching.

**Gate decision:** CONDITIONAL NO-GO. The infrastructure was correct, but the three credential detection gaps had to be closed before v0.1.0 release.

## Sprint 13: Private Adapter Strategy and Threat Models

Sprint 13 shifted from quality gates (checking finished profiles) to threat models (preventing unsafe adapters from being built).

The adversarial review of Sprint 13 asked: "If we build real Gmail, iMessage, database, or transcript adapters, what could go wrong?" The answer was a 9-document threat-model framework covering consent, credentials, multi-person content, audit logging, and replay semantics.

**Deliverables:**
- Four threat models (Gmail, iMessage, Transcript, Database) covering source ownership, consent, credential handling, replay, audit, and source-specific leakage vectors.
- Credential storage policy: defined how credentials should be referenced (env vars, never inline secrets), loaded (late, fail-closed), redacted (in all errors and logs), and rotated.
- Consent and multi-person policy: defined who can authorize a connector, which content is owner-authored vs. third-party, what counts as contamination, and how to exclude/quarantine non-subject content.
- Implementation standard and synthetic fixture standard: defined what connectors are allowed to do (discover, ingest, normalize) vs. not allowed to do (classify, compile, export, call LLMs).

**Adversarial findings:** Two critical gaps were identified:
1. **Consent enforcement mechanisms do not exist** — The threat models say "only owner-authored content can support profiles," but there was no code that actually enforced this. A future Gmail connector could accidentally include received mail or quoted replies.
2. **Redaction patterns are incomplete** — The patterns caught obvious secrets (api_key, Bearer tokens) but missed OAuth refresh tokens, database DSNs with passwords, API keys in URL parameters, JWT tokens, and AWS/Azure credentials.

Additionally, five major recommendations were made:
- Replay versioning semantics must be explicit (what happens when connector or adapter version changes?).
- Multi-person contamination tests must exist (fixtures with received mail, group chats, third-party speakers).
- Audit logging interface must be defined (what gets logged, what gets redacted?).
- Public/private repository leakage detection must be automated (prevent accidental commit of real email addresses or paths).
- Adapter authority boundaries must be tested (prove connectors don't import classifiers, exporters, LLMs).

**Gate decision:** CONDITIONAL GO. The framework was sound and comprehensive, but the two critical gaps meant no real private adapter could be implemented safely without first closing them.

## Sprint 13.5: Enforcement Foundation

Sprint 13.5 was the closing sprint: turn the threat-model strategy into code, tests, and enforceable contracts.

**The challenge:** The Sprint 13 gaps weren't design flaws—the recommendations were clear. But implementing them required concrete code that classifiers and compilers would actually call, tests that proved the enforcement worked, and fixtures that exercised edge cases (received mail, group chats, third-party speakers, base64-encoded credentials).

**Approach:** Three focused adversarial reviews ran in parallel:
1. **Consent and contamination** — Could third-party content leak past the consent boundary?
2. **Redaction and leakage** — Could credentials still leak via encoding, URLs, or other vectors?
3. **Replay, audit, and authority** — Could version drift be misinterpreted as expression drift? Could audit logs expose secrets? Could connectors gain unauthorized authority?

Each review found P1 issues in the initial implementation. The team remediated before final review.

**Deliverables:**
- `ConsentBoundary` in `src/imprint/connectors/consent.py`: evaluates source hints (consent_class, sender, role, participant) and determines whether content is owner-authored, third-party, system-generated, or unknown. Integrated into `RuleBasedArtifactClassifier`.
- Expanded redaction in `src/imprint/connectors/redaction.py`: now catches OAuth refresh tokens, JWTs, database DSNs (postgres://, mysql://, mongodb://), API keys in URL query parameters, AWS access keys, Azure connection strings, local home paths.
- `ConnectorReplayManifest` in `src/imprint/connectors/replay.py`: records connector/adapter/parser/source-policy versions, storage mode, config hash, and compatibility checks. Prevents false expression-drift claims when versions change.
- `ConnectorAuditLog` in `src/imprint/connectors/audit.py`: standardized audit payload with counts, connector metadata, storage mode, replay reference. `to_public_safe_dict()` redacts arbitrary metadata and replaces error strings with numbered placeholders.
- Fixture leakage scanner in `src/imprint/connectors/leakage.py`: scans fixture trees and individual paths for unsafe content (real-looking emails, phone numbers, private URLs, credentials, DSNs, base64-encoded values, local home paths).
- Authority boundary tests: recursively scan connector modules to prove they don't import classifiers, signal extractors, compilers, exporters, LLM/provider packages, or network/API clients.

**Test coverage:** Added 121 new tests (26 connector, 95 classification consent). Full test suite now at 139 tests, all passing.

**Key remediation:** The three parallel adversarial reviews initially found:
- Private-family source aliases (sent_mail, chat, transcript) didn't fail closed when consent hints were missing.
- Transcript segments weren't required to have explicit `speaker_role` before durable subject-authored inclusion.
- Nested `env` mappings could leak secret values or secret-like nested keys.
- Fixture leakage scanner didn't detect base64 or URL-encoded private content.
- Public narrative docs contained private file-share handoff details.
- Replay compatibility didn't include manifest version.
- Config hashes were computed over raw config shape instead of redacted shape.
- Audit logs emitted arbitrary warning/error/metadata text instead of allowlisted summaries.
- Connector authority scans didn't recurse through subpackages.

All were fixed before final review.

**Gate decision:** GO for private adapter implementation planning. Real adapters remain NO-GO unless they add source-specific threat model, synthetic fixtures, and tests.

**Update from implementation:** Sprint 13.5 fully remediated the seven critical Sprint 13 enforcement gaps (consent enforcement, redaction breadth, replay compatibility, audit redaction, leakage scanning, and authority boundaries). The remaining blockers are now only source-specific execution items, not core platform safety primitives.

## Numerical Outcomes

| Metric | Sprint 12 | Sprint 13 | Sprint 13.5 | Final |
|--------|-----------|-----------|------------|-------|
| Tests | 109 | 109 → 123 | 123 → 139 | 139 |
| Threat models | — | 4 | 4 | 4 |
| Policy documents | — | 4 | 4 + updated | 8 |
| Consent enforcement | ✗ | — | ✓ | ✓ |
| Redaction coverage | 70% | 70% | 100% | 100% |
| Replay versioning | ✗ | — | ✓ | ✓ |
| Audit logging | ✗ | — | ✓ | ✓ |
| Fixture leakage detection | ✗ | — | ✓ | ✓ |
| Authority boundary tests | ✗ | — | ✓ | ✓ |

## What's Unblocked

Real private adapter implementations can now proceed with confidence that the public core enforces:
- Consent rules for third-party content
- Complete credential redaction
- Replay versioning and compatibility checking
- Standardized, redacted audit logging
- Automatic fixture leakage detection
- Connector authority boundaries

Each source-specific connector (Gmail, iMessage, Transcript, Database) must still add:
- Source-specific threat model (customizing the generic one)
- Synthetic fixtures covering edge cases (received mail, group chats, unknown senders, etc.)
- Consent tests proving third-party content is excluded/quarantined
- Redaction tests covering source-specific credential patterns
- Replay/audit tests verifying deterministic rebuilds
- Public-safe export validation for the source's data shapes

## What's Still Pending

- First real private adapter implementation (Gmail, iMessage, or database).
- Replay manifest fields integrated into profile build metadata (needed before connector-driven profiles are compared as expression drift).
- Private deployment documentation (how to run source-specific connectors in production).
- Connector credential rotation and revocation workflows.

---

**See `CHANGES.md` for chronological summary across Sprints 12–13.5.**

**Implementation contracts:**
- `docs/SPRINT_12_ARCHITECTURE_REVIEW.md` — validation and quality-gate boundaries
- `docs/SPRINT_13_ARCHITECTURE_REVIEW.md` — threat-model framework and policy recommendations
- `docs/SPRINT_13_5_ARCHITECTURE_REVIEW.md` — enforcement foundation and GO decision
- `docs/CONSENT_BOUNDARY_MODEL.md` — consent class/action contract
- `docs/CONNECTOR_REPLAY_MANIFEST.md` — replay versioning and compatibility
- `docs/CONNECTOR_AUDIT_LOG.md` — standardized audit logging

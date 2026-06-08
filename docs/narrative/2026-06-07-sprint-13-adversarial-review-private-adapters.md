# Sprint 13 Adversarial Review — Private Adapter Strategy and Threat Models

**Decision:** Hostile privacy/security architect review identified framework is sound; 2 critical gaps and 5 major recommendations must be addressed before implementation sprints begin.

**What was delivered in Sprint 13:**

Nine strategy documents defining threat models and policies for future private adapters:
- `GMAIL_CONNECTOR_THREAT_MODEL.md` — OAuth scope minimization, sent vs. received separation, quoted thread contamination, multi-party consent
- `IMESSAGE_CONNECTOR_THREAT_MODEL.md` — Local database access, participant consent, group chat contamination, sender attribution
- `TRANSCRIPT_CONNECTOR_THREAT_MODEL.md` — Speaker attribution, recorder consent, diarization uncertainty, third-party voices
- `DATABASE_CONNECTOR_THREAT_MODEL.md` — Query allowlisting, DSN redaction, least privilege, row-level privacy
- `CREDENTIAL_STORAGE_POLICY.md` — Env var references, no inline secrets, fail-closed on missing credentials, scope minimization
- `CONSENT_AND_MULTI_PERSON_POLICY.md` — Owner-authored vs. third-party distinction, quarantine on uncertainty, audit-only content
- `CONNECTOR_IMPLEMENTATION_STANDARD.md` — Authority boundaries, configuration standard, replay/audit requirements
- `CONNECTOR_SYNTHETIC_FIXTURE_STANDARD.md` — No real data, covers edge cases, multi-person scenarios, source-specific minimums
- Updated `CONNECTOR_FRAMEWORK.md` and related docs

All 14 existing connector tests pass; framework is generic and synthetic-testable.

## Critical Gaps Identified via Adversarial Analysis

### Gap 1: Consent Enforcement Does Not Exist in Code

Threat models specify that only owner-authored content can support profiles, third-party content must be excluded or quarantined. However:
- No code validates consent
- No tests prove third-party content is excluded
- Classification layer unaware of source-specific consent rules
- Compiler applies no source-specific authorship policies

**Risk:** Gmail connector could include received mail; iMessage connector could include group participants' messages; legal/ethical boundary violation.

**Fix:** Define `ConsentBoundary` protocol that classifiers and compilers consult before including content. Map each threat model to concrete boundary instance. Add tests proving enforcement.

**Timeline:** Before implementation.

---

### Gap 2: Redaction Patterns Incomplete

Current patterns catch obvious secret keys (token, password, api_key) and Bearer tokens, but miss real-world formats:
- OAuth refresh tokens
- Database DSNs with passwords (`postgres://user:password@host:5432/db`)
- API keys in URL parameters (`?api_key=abc`, `&token=xyz`)
- JWT tokens (`eyJ...eyJ...sig`)
- AWS access keys, Azure connection strings
- Refresh token patterns in various formats

**Risk:** Error messages and audit logs from future credentialed connectors could leak passwords, tokens, or connection strings.

**Fix:** Expand `SECRET_VALUE_PATTERN` to detect database DSNs, URL parameter credentials, JWT tokens, and AWS/Azure credentials. Add tests.

**Timeline:** Before any credentialed connector (Gmail OAuth, database connector, transcript API).

---

## Major Recommendations

1. **Replay Versioning Semantics** (HIGH) — Define explicit versioning contract for rebuilds; what happens when connector/adapter/parser version changes?
2. **Multi-Person Contamination Tests** (HIGH) — Add comprehensive fixtures and tests for received mail, group chats, third-party participants before implementation
3. **Audit Logging Interface** (HIGH) — Define `ConnectorAuditLog` contract before implementation; audit requirements are specified but not instrumentized
4. **Public/Private Repository Detection** (MEDIUM) — Add pre-commit hook preventing accidental commit of real email addresses, phone numbers, private domains in fixtures
5. **Adapter Authority Boundary Tests** (MEDIUM) — Add tests proving connectors don't import classifier, LLM packages, or call export generation

---

## Verification Evidence

**Framework soundness:**
- All 9 threat models reviewed for comprehensive coverage
- Credential storage policy and consent policy aligned and non-contradictory
- Implementation standard and synthetic fixture standard cover requirements

**Redaction analysis:**
- Current patterns tested against common secret formats
- Missing patterns identified and documented
- Tests proposed for each missing pattern type

**Connector code:**
- No implementation of real private adapters (as intended for strategy sprint)
- Generic connectors remain public-safe
- 14 connector tests passing

**Threat model coverage:**
- 4 source families covered (Gmail, iMessage, Transcript, Database)
- Consent classes defined
- Multi-person risks acknowledged
- Replay/audit requirements specified

---

## Gate Decision

**Status:** CONDITIONAL GO

**Framework is ready for planning and review.** Proceed to implementation planning in Sprint 14+ **only if**:

- Consent enforcement interface is designed
- Redaction patterns are expanded
- Multi-person contamination tests are added to fixture standards
- Replay versioning contract is defined
- Audit logging interface is defined
- Public/private repository detection is automated
- Adapter authority boundary tests are added

The strategy is sound. Gaps are about enforcement and completeness, not fundamental design flaws.

---

**Document:** `docs/SPRINT_13_ARCHITECTURE_REVIEW.md`

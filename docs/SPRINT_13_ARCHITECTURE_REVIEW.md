# Sprint 13 Architecture Review: Private Adapter Strategy and Threat Models

**Review Date:** 2026-06-07  
**Reviewer Role:** Hostile Privacy/Security Architect  
**Status:** IDENTIFIED GAPS & RECOMMENDATIONS  
**Go/No-Go:** **CONDITIONAL GO** — Proceed with implementations only after addressing critical gaps

---

## Executive Summary

Sprint 13 successfully established a comprehensive threat-model framework for future private adapters without implementing any real connectors. Nine strategy documents cover credential storage, consent, implementation standards, and synthetic fixtures.

Adversarial analysis identified **2 critical gaps** and **5 major recommendations** that must be addressed before real private adapter implementations (Gmail, iMessage, database, transcript):

- Consent enforcement mechanisms are specified in policy but not enforced in code or tests
- Redaction patterns miss several credential formats common in real deployments (refresh tokens, database DSNs, API keys in URLs, JWT tokens)
- Replay/rebuild semantics lack explicit versioning contracts
- Multi-person content contamination risks are identified but boundaries are not tested
- Public/private repository leakage lacks automated detection
- Audit requirements are defined but logging interfaces don't exist
- Adapter authority boundaries are described but not validated by tests

These gaps are acceptable for a strategy sprint but must be closed before implementation. The framework is sound; gaps are about enforcement.

---

## Part 1: Critical Gaps

### Gap 1: Consent Enforcement Mechanisms Do Not Exist

**Severity:** CRITICAL — Privacy boundary failure vector

**Evidence:** Threat models specify consent classes (owner-authored vs. third-party) and exclude rules, but:
- No code validates consent before including content
- No tests prove third-party content is actually excluded
- Classification layer is not connected to threat-model consent rules
- Compiler does not enforce source-specific authorship policies

**Impact:** A Gmail connector could inadvertently include received mail or quoted replies. An iMessage connector could include group-chat participants' messages. Consent is a legal and ethical boundary; accidental inclusion violates user trust.

**Fix Priority:** Define before implementation. Required:

1. Define abstract `ConsentBoundary` contract that classifiers and compilers consult
2. Map each threat model to a concrete `ConsentBoundary` instance
3. Add tests proving enforcement (e.g., `test_gmail_excludes_received_mail`)

**Timeline:** Before any private connector implementation.

---

### Gap 2: Redaction Patterns Are Incomplete

**Severity:** CRITICAL — Credential leakage vector

**Evidence:** Redaction catches basic secret keys and Bearer tokens, but misses:
- OAuth refresh tokens
- Database DSNs with embedded passwords (postgres://user:password@host:5432/db)
- API keys in URL parameters (?api_key=abc123)
- JWT tokens (format: eyJ...eyJ...sig)
- AWS access keys, Azure connection strings, refresh tokens in various formats

**Impact:** Error messages, dry-run summaries, and audit logs could expose credentials from future database/API connectors. A postgres connection string would pass unredacted.

**Fix Priority:** Expand `SECRET_VALUE_PATTERN` before any credentialed connector. Include:
- Database DSN patterns (postgres://, mysql://, mongodb://, etc.)
- URL parameter credential patterns (?api_key=, ?token=, &auth=)
- JWT token format (eyJ...eyJ...sig)
- AWS access key format (AKIA...)
- Refresh token patterns

Add tests verifying redaction of real-world credentials.

**Timeline:** Before any credentialed connector (Gmail, database, transcript API).

---

## Part 2: Major Recommendations

### Recommendation 1: Replay Versioning Semantics Unclear

**Severity:** HIGH — Reproducibility risk

**Evidence:** Threat models say "deterministic for same connector version" but don't define what happens when versions change or how to detect version mismatches in comparisons.

**Recommendation:** Define `ProfileReplayManifest` capturing connector version, adapter version, parser version, source policy version, storage mode, and source-specific config. Store in profile build metadata so comparisons can verify compatibility before claiming expression drift.

**Timeline:** Before Sprint 14 implementation.

---

### Recommendation 2: Multi-Person Contamination Tests Missing

**Severity:** HIGH — Boundary enforcement risk

**Evidence:** Consent policy defines multi-person exclusion but zero tests prove it works. No fixtures with received mail, group chats, or third-party participants.

**Recommendation:** Add comprehensive fixtures and tests before implementation (e.g., `test_gmail_excludes_received_mail`, `test_imessage_excludes_group_participants`).

**Timeline:** Before implementation sprints.

---

### Recommendation 3: Audit Logging Interface Not Defined

**Severity:** HIGH — Observability gap

**Evidence:** Threat models require audit logging (what was read, included, excluded, quarantined, etc.) but no interface exists for connectors to produce standardized, redacted audit logs.

**Recommendation:** Define `ConnectorAuditLog` contract with events, counts, warnings, and redaction method.

**Timeline:** Before implementation.

---

### Recommendation 4: Public/Private Repository Boundary Lacks Detection

**Severity:** MEDIUM — Unintentional leakage risk

**Evidence:** Policy says no private data in public repo but no automated scanner prevents accidental commit of real email addresses or chat exports.

**Recommendation:** Add pre-commit hook validating fixtures contain no real email domains, phone numbers, private URLs. Require fixture names contain `synthetic`, `example`, `fixture`, or `test`.

**Timeline:** Before first private connector PR.

---

### Recommendation 5: Adapter Authority Boundaries Not Tested

**Severity:** MEDIUM — Scope creep risk

**Evidence:** Implementation standard lists things connectors must NOT do (classify, extract signals, call LLMs, bypass export validation) but zero tests enforce these boundaries.

**Recommendation:** Add tests proving connectors don't import classifier, LLM packages, or call export generation.

**Timeline:** Before implementation.

---

## Part 3: Go/No-Go Decision

### Current Status: CONDITIONAL GO

**Blockers:**
1. ✗ Consent enforcement mechanisms do not exist (CRITICAL)
2. ✗ Redaction patterns incomplete (CRITICAL)

**Must-Have Recommendations:**
1. ⚠ Replay versioning semantics (HIGH)
2. ⚠ Multi-person contamination tests (HIGH)
3. ⚠ Audit logging interface (HIGH)
4. ⚠ Public/private repository detection (MEDIUM)
5. ⚠ Adapter authority boundary tests (MEDIUM)

### Release Criteria

Framework is ready for **planning and review** if all gaps are acknowledged. Proceed to **implementation planning** in Sprint 14+ only after:

- Consent enforcement interface is designed and consent boundaries are testable
- Redaction patterns are expanded and tested against real credential formats
- Replay versioning contract is defined
- Multi-person contamination tests are added to fixture standards
- Audit logging interface is defined
- Repository detection is automated
- Adapter authority boundary tests are added
- All 14 existing connector tests still pass

---

## Conclusion

Sprint 13 established a sound threat-model framework. Gaps are about turning strategy into code and tests, not fundamental design flaws. With gaps addressed, the framework can support safe private adapter implementation without compromising privacy or security.

---

**Document Version:** sprint13-adversarial-review-v1  
**Last Updated:** 2026-06-07  
**Status:** FRAMEWORK SOUND; IMPLEMENTATION-READY WITH GAP FIXES

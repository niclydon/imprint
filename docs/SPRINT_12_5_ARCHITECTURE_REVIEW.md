# Sprint 12.5 Architecture Review: Quality Gate Hardening

**Review Date:** 2026-06-07  
**Reviewer Role:** Hostile Security Architect  
**Status:** GO  
**Go/No-Go:** **GO** for Sprint 13 and `v0.1.0` planning after full test-suite verification

---

## Executive Summary

Sprint 12.5 closes the Sprint 12 privacy-gate blockers. The implementation moves credential, JWT,
encoded credential, path, encoded path, and underscore-private-metadata checks into the shared export
safety surface. Quality validation now calls the same string validator, reducing drift between export
safety and release gates.

The comparison gate also no longer treats mixed classifier-version outputs as fully comparable.
Mixed-version state is explicit in machine-readable metadata and forces release review.

## Re-Review Findings

### JWT credential bypass

**Decision:** Fixed.

JWT-shaped values with base64url JSON header and payload segments are rejected by public-safe payload
validation and quality-gate privacy checks.

### Base64/base64url credential bypass

**Decision:** Fixed.

The validator scans plain strings, safely decodes plausible bounded base64/base64url strings once,
and re-scans decoded text for credential and JWT patterns. The implementation is intentionally
non-recursive and length-bounded.

### Encoded path bypass

**Decision:** Fixed.

The validator rejects `%2F`, `%2f`, `%5C`, and `%5c`, and URL-decodes candidate values before
re-scanning for path-like shapes.

### Underscore-prefixed metadata escape hatches

**Decision:** Fixed.

Underscore-prefixed dictionary keys are rejected at root and nested levels. This conservative default
blocks `_metadata`, `_internals`, `_debug`, `_private`, and future private-looking fields unless a
future public schema explicitly introduces an allowlisted exception.

### Mixed classifier-version comparability gaps

**Decision:** Fixed.

Mixed classifier versions produce `PARTIALLY_COMPARABLE`, expose `comparability.version_metadata`,
and return `release_gate.status: WARN` with `mixed_classifier_versions` in structured reason codes.

### Inconsistent validation surfaces

**Decision:** Fixed.

Export safety and quality validation now share `validate_public_safe_string`. Quality still layers
raw/private content-field rejection on top, but credential and path semantics are shared.

### False PASS release states

**Decision:** Fixed for Sprint 12.5 scope.

Validation failures produce `release_gate.status: FAIL`. Comparison ambiguity produces
`release_gate.status: WARN` with `required_reviews` and `reason_codes` instead of relying on prose.

## Remaining Recommendations

- Preserve provider/model manifest metadata in Sprint 13+ private-adapter work.
- Treat any future underscore-prefixed public schema field as an explicit security exception requiring tests and documentation.
- Keep encoded-value scanning bounded and one-level unless a concrete corpus demonstrates a need for deeper decoding.

## GO Conditions

Sprint 13 and `v0.1.0` planning may proceed if the full repository verification remains green:

- `pytest -q`
- `python3 -m compileall -q src`
- synthetic export generation and validation smoke tests
- comparison smoke test with identical synthetic exports

## Final Decision

**GO** for Sprint 13 and `v0.1.0` planning, contingent on the current full verification run passing
before merge/push/deploy.


# Sprint 12.5 Remediation Summary: Quality Gate Hardening

**Date:** 2026-06-07  
**Status:** Implemented  
**Scope:** Sprint 12 adversarial blockers and release-gate hardening

## Summary

Sprint 12.5 hardens public-safe validation and profile-comparison release gates before Sprint 13 or
`v0.1.0` planning. The remediation centralizes unsafe string detection in export safety code so
canonical export validation and quality gates use the same credential, path, encoded-value, and
private-metadata checks.

## Blockers Fixed

### JWT credential detection

- Added JWT-shaped credential detection for three-segment base64url token shapes.
- Validates that JWT header and payload segments decode to JSON-shaped objects before rejection.
- Applies through `assert_public_safe_payload`, `validate_opaque_source_id`, and quality-gate privacy walking.

### Base64/base64url credential detection

- Scans plain strings first, then safely attempts bounded one-level base64/base64url decoding.
- Re-scans decoded text for credential patterns and JWT-shaped credentials.
- Limits candidate length and decoded byte size to avoid recursive or excessive decoding.

### Percent-encoded path detection

- Rejects encoded path separators `%2F`, `%2f`, `%5C`, and `%5c`.
- URL-decodes candidate strings and re-scans decoded values for Unix, Windows, and relative path shapes.
- Applies consistently to payload strings, context filters, and source IDs.

### Underscore metadata rejection

- Rejects underscore-prefixed metadata keys at root and nested levels.
- Blocks `_metadata`, `_internals`, `_debug`, `_private`, and any future private-looking `_field` escape hatch by default.
- Orders private-metadata rejection before forbidden-key scanning so nested underscore metadata cannot hide generation-control fields.

### Mixed classifier-version comparison coverage

- Adds `mixed_classifier_versions` comparability reason.
- Marks mixed classifier-version comparisons as `PARTIALLY_COMPARABLE` rather than fully comparable.
- Exposes version lists and mixed-version booleans in `comparability.version_metadata`.
- Sets comparison `release_gate.status` to `WARN` with structured `reason_codes` and `required_reviews` for partial, not-comparable, and mixed-version cases.

## Machine-Readable Gate Output

Validation release gates now include:

- `blocking_failures`
- `required_reviews`
- `reason_codes`

Comparison release gates now include:

- `blocking_failures`
- `required_reviews`
- `reason_codes`

These fields are intended for CI and release automation. Human-readable summaries remain present but are not the authoritative automation contract.

## Explicit Deferrals

Provider/model metadata future-proofing remains a Sprint 13+ compatibility requirement. Sprint 12.5 preserves the existing optional provider/model fields and documents that future private-adapter or provider work must extend, not erase, those manifest fields.

Sprint 12.5 does not implement private adapters, service/API mode, LLM judges, subjective voice scoring, broad schema redesign, or a web UI.

## Verification

Implemented regression coverage proves:

- JWT tokens fail export safety validation.
- JWT tokens fail quality-gate privacy validation.
- Base64-encoded credentials fail validation.
- Base64url-encoded credentials fail validation.
- Percent-encoded Unix paths fail validation.
- Percent-encoded Windows paths fail validation.
- Root-level underscore metadata fails validation.
- Nested underscore metadata cannot bypass forbidden-key validation.
- Mixed classifier versions produce `PARTIALLY_COMPARABLE`, expose structured version metadata, and require release review.
- Existing Sprint 12 quality and export tests remain passing.


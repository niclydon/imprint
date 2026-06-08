# Sprint 12 Adversarial Review — Evaluation and Quality Gates

**Decision:** Hostile security architect review identified 3 critical credential-detection gaps requiring fixes before v0.1.0 release. Conditional no-go; proceed to Sprint 13 only after blockers are fixed.

**What was implemented in Sprint 12:**
- `imprint validate-export <file>` emits machine-readable PASS/FAIL reports for canonical JSON, Mosvera overlays, and Sprint 08/consumer contracts.
- `imprint diff profile-a.json profile-b.json` validates both manifests and reports `COMPARABLE`, `PARTIALLY_COMPARABLE`, or `NOT_COMPARABLE`.
- Comparison explicitly separates expression drift from compiler/corpus/schema drift; does not overclaim implementation changes as expression drift.
- Privacy validation rejects raw/private content fields, path-like strings, credential-like tokens, and invalid opaque source IDs in public outputs.
- Release-gate checks for compatibility metadata, schema/version consistency, and required consumer warnings.

## Critical Blockers Identified via Adversarial Testing

### Blocker 1: JWT Credentials Not Detected (CRITICAL)

JWT tokens (format: `eyJ[...].eyJ[...].[-_A-Za-z0-9]{20,}`) are valid authentication credentials but pass validation. Current `CREDENTIAL_PATTERN` in `quality.py:29` lacks JWT regex.

**Fix:** Add JWT pattern to `CREDENTIAL_PATTERN`.

### Blocker 2: Base64-Encoded Credentials Bypass Validation (CRITICAL)

Credentials encoded as base64 (common in HTTP headers, config files) evade detection because `_walk_privacy()` checks plain-text patterns only without attempting decoding first.

**Fix:** Implement base64 decoding in `_walk_privacy()` before re-scanning for credential patterns.

### Blocker 3: Percent-Encoded Paths Evade Detection (HIGH)

URL-encoded paths like `%2Fprivate%2Fdata` (common in REST APIs, config URLs) evade detection because `PATH_PATTERN` checks for literal slashes/backslashes but not `%2F` or `%5C`.

**Fix:** Add percent-encoding detection to `PATH_PATTERN`.

## Verification Evidence

- Custom adversarial test suite exposed all 3 credential-detection gaps
- Full regression suite: `pytest -q` passed (109 tests)
- `pytest -q tests/test_quality_gates.py` passed (9 tests)
- `python3 -m compileall -q src` passed
- Smoke checks: `imprint example`, `imprint validate-export`, `imprint diff` executed without error

## Recommendations (Non-Blocking)

1. Underscore-prefixed fields should be rejected at root level (HIGH priority for v0.1.0)
2. Provider metadata should be added to `BuildManifest` for future drift detection (MEDIUM priority for Sprint 13+)
3. Regression corpus should expand to cover mixed classifier versions (MEDIUM priority for v0.1.0)
4. Release gate output should be machine-readable for CI/CD integration (LOW priority for v0.2.0)

## Gate Decision

**Status:** CONDITIONAL NO-GO

Release criteria: Fix all 3 blockers, add unit tests, expand regression corpus, ensure all 109 existing tests still pass.

**Full story:** [`docs/SPRINT_12_ARCHITECTURE_REVIEW.md`](../SPRINT_12_ARCHITECTURE_REVIEW.md)

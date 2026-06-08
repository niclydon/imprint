# Quality Gates

Status: Sprint 12.5 hardened baseline

Sprint 12.5 hardens release gates for public-safe exports and profile comparisons.

## Required Gates

Before release:

```bash
pytest -q
python -m compileall -q src
imprint example
imprint validate-export exports/synthetic-demo/profile.imprint.json
imprint validate-export exports/synthetic-demo/mosvera.expression.json
imprint validate-export exports/synthetic-demo/human-cli.consumer.json
imprint diff exports/synthetic-demo/profile.imprint.json exports/synthetic-demo/profile.imprint.json
```

## Failing Conditions

A release candidate fails when:

- raw text fields appear in public-safe JSON
- filesystem paths or private locators appear
- percent-encoded Unix or Windows path separators appear
- credential-like strings, keys, tokens, private keys, or DSNs appear
- JWT-shaped credentials appear
- base64/base64url values decode to credential-like strings
- underscore-prefixed metadata fields appear at root or nested levels
- source IDs are not opaque `source-*` values
- compatibility metadata is missing
- consumer compatibility warnings disappear
- public-safe payloads contain prompt/provider/generation-control fields
- prohibited or quarantined claims appear in export patterns
- schema or export versions are invalid
- profile comparisons present implementation drift as expression drift

## Report Handling

`validate-export` returns `status: PASS` or `status: FAIL`. The nested `release_gate` includes
`blocking_failures`, `required_reviews`, and stable `reason_codes` for automation.

`diff` returns `status: PASS`, a comparability state, drift categories, and release-gate summary.
`PARTIALLY_COMPARABLE` and `NOT_COMPARABLE` comparisons are not invalid, but they return
`release_gate.status: WARN` and require release review before anyone treats changes as expression
drift. Mixed classifier-version metadata is also review-required even when the compared exports are
otherwise schema-compatible.

## CI Coverage

The Sprint 12.5 regression tests exercise passing exports, raw text leakage, path/source-ID
leakage, JWTs, base64/base64url credentials, percent-encoded paths, underscore metadata, missing
compatibility metadata, consumer contract validation, comparable exports, compiler drift, corpus
drift, and mixed classifier-version comparisons.

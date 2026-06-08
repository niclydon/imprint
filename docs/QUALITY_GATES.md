# Quality Gates

Status: Sprint 12 baseline

Sprint 12 adds release gates for public-safe exports and profile comparisons.

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
- credential-like strings, keys, tokens, private keys, or DSNs appear
- source IDs are not opaque `source-*` values
- compatibility metadata is missing
- consumer compatibility warnings disappear
- public-safe payloads contain prompt/provider/generation-control fields
- prohibited or quarantined claims appear in export patterns
- schema or export versions are invalid
- profile comparisons present implementation drift as expression drift

## Report Handling

`validate-export` returns `status: PASS` or `status: FAIL`.

`diff` returns `status: PASS`, a comparability state, drift categories, and release-gate summary.
`NOT_COMPARABLE` comparisons are not invalid, but they require release review before anyone treats
changes as expression drift.

## CI Coverage

The Sprint 12 regression tests exercise passing exports, raw text leakage, path/source-ID leakage,
missing compatibility metadata, consumer contract validation, comparable exports, compiler drift, and
corpus drift.

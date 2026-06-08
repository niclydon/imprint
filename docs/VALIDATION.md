# Validation

Status: Sprint 12.5 hardened baseline

`imprint validate-export` validates public-safe Imprint exports and consumer contracts before release
or downstream use.

## Command

```bash
imprint validate-export exports/synthetic-demo/profile.imprint.json
```

The command prints a machine-readable JSON report and exits non-zero on failure.

## Report Shape

```json
{
  "report_version": "sprint12-validation-report-v1",
  "file": "profile.imprint.json",
  "status": "PASS",
  "checks": [],
  "warnings": [],
  "release_gate": {
    "status": "PASS",
    "blocking_failures": [],
    "required_reviews": [],
    "reason_codes": []
  }
}
```

## Checks

Validation covers:

- JSON object shape
- canonical export schema fields
- build manifest metadata
- artifact storage metadata
- source policy metadata
- export schema version
- compatibility metadata
- opaque source IDs
- no prohibited or quarantined claims
- no raw/private content fields
- no filesystem path-like strings
- no percent-encoded Unix or Windows path separators (`%2F`, `%2f`, `%5C`, `%5c`)
- no credential-like strings or DSNs
- no JWT-shaped credentials
- no bounded base64/base64url-encoded credentials that decode to credential-like values
- no generation-control fields
- no underscore-prefixed private metadata fields, at root or nested levels
- consumer contract evidence policy
- mandatory consumer compatibility warnings

## Supported Payloads

The Sprint 12 validator supports:

- canonical JSON profile exports
- Mosvera expression overlays
- Mosvera, Broadside, agent, and human CLI consumer contracts

Markdown and first-run text outputs are user-facing summaries. Their safety remains covered by export
unit tests and source exporter validation, not by the JSON validator.

## Release Gate Semantics

`status: FAIL` means the output is not releaseable or safe for downstream consumption.

Failures include raw text leakage, path leakage, encoded path leakage, credential-like leakage,
encoded credential leakage, invalid source IDs, underscore-prefixed metadata, missing compatibility
metadata, schema/version mismatch, prohibited claims, and prompt/provider control fields.

`release_gate.reason_codes` is the stable machine-readable field for automation. It mirrors the
failed check categories, while `blocking_failures` remains a human-readable list of failed checks.

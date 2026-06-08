# Validation

Status: Sprint 12 baseline

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
    "blocking_failures": []
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
- no credential-like strings or DSNs
- no generation-control fields
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

Failures include raw text leakage, path leakage, credential-like leakage, invalid source IDs, missing
compatibility metadata, schema/version mismatch, prohibited claims, and prompt/provider control
fields.

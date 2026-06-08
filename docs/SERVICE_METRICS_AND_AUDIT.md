# Service Metrics and Audit

Status: Sprint 14 metrics and audit model

## Metrics Model

Allowed metrics:

- service health
- package version
- export schema version
- latest export filename
- latest export modification timestamp
- validation status
- warning count
- profile signal count
- included support count
- generated export presence
- dry-run job result

Forbidden metrics:

- raw artifact text
- private filesystem paths
- credentials
- source snippets
- private account identifiers
- provider/model configuration
- prompt contents
- downstream publishing state

## Audit Model

Service audit events should be local/private and public-safe by construction. A safe service audit
event may include:

- event type
- endpoint name
- timestamp
- result code
- validation status
- warning count
- read-only/job mode

It must not include request authorization values, environment variables, raw source data, connector
configuration, local paths, stack traces with private values, or response payloads containing exports.

## Validation Status

Validation status comes from the existing quality gate for `profile.imprint.json`. The service should
surface validation failure as status metadata and must not return invalid canonical JSON as a latest
profile.

## Warning Semantics

Warnings are compatibility and limitation signals that downstream consumers must surface. Warning
counts are safe to expose. Warning text must pass the public-safe payload validator before return.


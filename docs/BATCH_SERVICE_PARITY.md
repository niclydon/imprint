# Batch/Service Parity

Status: Sprint 14 parity contract

## Principle

The batch CLI remains the producer of public-safe profile exports. Service mode is a delivery and
status facade. A service-delivered profile is not a separate profile class and must not diverge from
the CLI-generated canonical export.

## Required Parity Checks

For the same config, source inputs, code version, and export directory, compare:

- canonical JSON export
- build manifest
- export schema version
- compatibility warnings
- validation report status

The service must either return the same canonical JSON payload or fail closed with a parity/validation
error.

## Markdown Parity

`GET /exports/latest.md` serves the generated `profile.md` file. It does not regenerate Markdown from
a different code path in service mode.

## Job Parity

Sprint 14 dry-run jobs do not rebuild. Future rebuild jobs must prove that service-generated outputs
match CLI-generated outputs or disclose a structured reason why they are not comparable.

## Non-Parity Conditions

Service output must not be treated as comparable when:

- export schema versions differ
- build manifests differ unexpectedly
- validation fails
- compatibility metadata is missing
- canonical JSON differs after deterministic normalization
- private paths, raw text, credentials, prompts, or provider settings appear


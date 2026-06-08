# Service Mode Design

Status: Sprint 14 local/private service design

## Scope

Service mode is a disabled-by-default local/private facade over public-safe exports. It does not
compile profiles unless a future authenticated rebuild endpoint is explicitly added and reviewed.
The Sprint 14 scaffold reads a configured export directory, validates the canonical JSON export, and
returns only public-safe status, warning, JSON, and Markdown surfaces.

## Non-Goals

Service mode must not become:

- a SaaS product
- a public API
- a dashboard
- a raw-corpus browser
- a connector configuration UI
- a credential manager
- a prompt or model-router surface
- a publishing workflow
- a Mosvera or Broadside runtime adapter
- a background data lake

## Runtime Boundary

Allowed runtime inputs:

- explicit local export directory
- generated `profile.imprint.json`
- generated `profile.md`
- generated compatibility warnings inside public-safe exports
- static configuration for bind host, read-only mode, and job authentication

Forbidden runtime inputs:

- raw artifact directories
- connector config containing private source paths or credentials
- `.env` values beyond service auth references
- provider/model config
- downstream publishing config
- prompts or prompt fragments

## Path Boundary

The service may only read fixed filenames inside the configured export directory. It must not accept
caller-supplied file paths. It must never return the configured export directory path or resolved
filesystem paths in responses.

## Export Boundary

The canonical JSON response is loaded through the existing validation gate before it is returned.
The Markdown response is limited to the generated `profile.md` file and is scanned for credential or
path-like content before return. Both responses are treated as service delivery of batch outputs, not
as service-generated profile classes.

## Operational Boundary

The service may report:

- service health
- package version
- export schema version
- consumer contract schema version
- latest export filename
- latest export modification timestamp
- validation status
- compatibility warnings
- read-only/job capability flags

The service must not report:

- raw source names
- source filesystem paths
- private connector config
- credentials or env values
- raw artifact text
- private account identifiers
- prompt/model/provider settings

## Job Boundary

Sprint 14 only allows an authenticated dry-run job. Dry-run validates current generated exports and
returns the same public-safe status payload as `GET /status`, plus an explicit `would_rebuild: false`
marker. It must not ingest, rebuild, call providers, run connectors, or publish.

## Failure Model

Service failures are fail-closed:

- missing export file returns unavailable status
- invalid export returns validation failure status
- missing job auth rejects write/job requests
- unknown export path requests are impossible because filenames are fixed
- validation failures prevent canonical JSON delivery


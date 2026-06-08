# Connector Framework

Status: Sprint 13 strategy baseline

## Purpose

Sprint 09 adds a generic private connector framework for owner-operated Imprint deployments. The
framework makes private ingestion configurable without adding real private-service connectors or
committing private data to the public repository.

Connectors ingest source artifacts. They do not classify, extract signals, compile profiles, export
profiles, assemble prompts, publish content, call LLMs, or call remote providers.

## Architecture

The connector layer sits before the existing adapter layer:

```text
connector config -> connector discovery/ingest -> existing source adapter -> ArtifactEnvelope -> Artifact
```

Connectors use adapters; they do not replace adapters. Adapter normalization remains responsible for
opaque source IDs, metadata-only artifact defaults, and advisory source hints.

Current public-core implementation:

```text
src/imprint/connectors/
  config.py          # config schema, manifest schema, runtime validation
  protocol.py        # connector capability/discovery contracts
  registry.py        # connector registry and default connector set
  local_directory.py # generic local file/directory connector over existing adapters
  manifest.py        # synthetic manifest connector over existing adapters
  redaction.py       # secret/path redaction utilities
```

## Built-In Connector Types

### `local_directory`

Uses one allowlisted adapter over a configured local file or directory.

Required config:

- `name`
- `type: local_directory`
- `enabled`
- `adapter`
- `path`

### `manifest`

Reads a synthetic manifest containing multiple adapter/path entries. Manifest paths are resolved
relative to the manifest file when they are not absolute.

Required config:

- `name`
- `type: manifest`
- `enabled`
- `manifest_path`

## Deferred Private Connector Families

Sprint 13 keeps real private adapters deferred. Future Gmail, iMessage/chat, transcript/recorder,
database/cloud, and live API connectors must satisfy these documents before implementation:

- `docs/GMAIL_CONNECTOR_THREAT_MODEL.md`
- `docs/IMESSAGE_CONNECTOR_THREAT_MODEL.md`
- `docs/TRANSCRIPT_CONNECTOR_THREAT_MODEL.md`
- `docs/DATABASE_CONNECTOR_THREAT_MODEL.md`
- `docs/CREDENTIAL_STORAGE_POLICY.md`
- `docs/CONSENT_AND_MULTI_PERSON_POLICY.md`
- `docs/CONNECTOR_IMPLEMENTATION_STANDARD.md`
- `docs/CONNECTOR_SYNTHETIC_FIXTURE_STANDARD.md`

No source-specific connector may enter public core solely because the generic framework exists.
Threat model, consent policy, credential handling, replay/audit behavior, and synthetic fixture tests
are preconditions.

## Config Shape

Connector declarations support:

- connector name
- connector type
- enabled/disabled flag
- adapter mapping
- local path or manifest path
- storage mode
- source policy version
- optional tags and labels
- local-only/private flags
- required or optional credential env var references

Credentials must be declared as env var references, not inline secrets.

```yaml
connectors:
  - name: synthetic_markdown
    type: local_directory
    enabled: true
    adapter: local_markdown
    path: ./examples/synthetic_corpus/markdown
    storage_mode: metadata_only
    source_policy_version: sprint09-source-policy-v1
    tags: [synthetic]

  - name: optional_private_export
    type: local_directory
    enabled: false
    adapter: local_jsonl
    path: ./private/example-export.jsonl
    credentials:
      source_token:
        env: IMPRINT_PRIVATE_SOURCE_TOKEN
        required: false
```

## Dry Run

`connectors-dry-run` discovers configured connector artifacts without ingesting normalized artifacts
or persisting output:

```bash
imprint connectors-dry-run --config imprint.config.example.yaml
```

Dry-run output reports connector name, type, enabled state, adapter types, artifact count, storage
mode, and warnings. It does not print raw artifact text or configured paths.

## Runtime Validation

Connector config fails closed when:

- required connector fields are missing
- connector names are duplicated
- a connector type has the wrong shape
- a Sprint 09 connector is not `local_only`
- an enabled connector path does not exist
- an enabled manifest path does not exist
- a required credential env var is unset
- label metadata contains inline secret-like values

Disabled connectors are inert. They can reference a private path that does not exist on the public
development machine without being run.

## Capability Metadata

Connectors expose capability metadata:

- connector type
- supported adapter types
- dry-run support
- artifact persistence behavior
- network requirement state
- model invocation state

Sprint 09 built-ins report no artifact persistence, no network requirement, and no model invocation.

## Boundary Rules

Connectors must preserve these boundaries:

- Connector hints are advisory. Classification re-assesses authorship and inclusion.
- Source IDs remain opaque after adapter normalization.
- Raw artifact text does not enter public-safe exports.
- Public examples stay synthetic.
- Private paths, credentials, service names, account identifiers, and corpora stay outside tracked
  public files.
- Consumer contracts remain projections of canonical JSON and do not become connector integrations.

## Implementation Gate

A future connector is implementation-ready only when it has:

- a source-specific threat model
- a credential-storage decision
- consent and multi-person-data handling
- synthetic fixtures for source-specific edge cases
- redaction tests for credentials, paths, provider locators, and private IDs
- replay/audit policy
- tests proving dry-run output contains counts and warnings only
- tests proving generated public-safe exports pass validation

Connectors continue to ingest only. They do not classify, infer, score, summarize, publish, or expose
raw corpus search.

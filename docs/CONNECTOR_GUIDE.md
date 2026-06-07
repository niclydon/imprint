# Connector Guide

Status: Sprint 09 baseline

## Connector Purpose

Connectors turn configured source locations into normalized Imprint artifacts through existing
adapters. They should not compile expression, decide final weights, call models, or embed private
assumptions.

## Connector Contract

A Sprint 09 connector:

- validates its configuration
- reports capability metadata
- supports dry-run discovery
- optionally ingests artifacts through an allowlisted adapter
- returns normalized `Artifact` records through the existing adapter registry

Adapters continue to own `ArtifactEnvelope` normalization. Connector metadata is advisory source
context only.

## Built-In Public Connectors

- `local_directory`: one configured file or directory plus one adapter
- `manifest`: a synthetic manifest listing one or more adapter/path entries

Built-in adapters available to those connectors:

- `local_text`
- `local_markdown`
- `local_jsonl`
- `local_transcript_json`

## Example Local Directory Connector

```yaml
connectors:
  - name: synthetic_markdown
    type: local_directory
    enabled: true
    adapter: local_markdown
    path: ./examples/synthetic_corpus/markdown
    storage_mode: metadata_only
    tags: [synthetic]
```

## Example Manifest Connector

```yaml
connectors:
  - name: synthetic_manifest
    type: manifest
    enabled: true
    manifest_path: ./examples/synthetic_corpus/connector-manifest.yaml
    storage_mode: metadata_only
```

Manifest file:

```yaml
version: sprint09-manifest-v1
entries:
  - name: markdown_examples
    adapter: local_markdown
    path: ./markdown
  - name: chat_export
    adapter: local_jsonl
    path: ./chat.jsonl
```

Relative manifest entry paths resolve relative to the manifest file.

## Dry Run

```bash
imprint connectors-dry-run --config imprint.config.example.yaml
```

Dry-run mode discovers artifact counts and adapter types. It does not emit normalized artifacts,
persist artifacts, print raw text, or print configured paths.

## Public Connector Rules

- Do not hard-code private paths.
- Do not hard-code private table names.
- Do not hard-code emails, names, phone numbers, account IDs, or service hostnames.
- Do not require private services for tests.
- Provide synthetic fixtures.
- Use env var references for credentials.
- Keep raw local corpus paths in ignored config only.
- Keep source IDs opaque after normalization.

## Private Connector Examples

Private deployments may eventually configure connectors such as:

- sent email connector
- chat export connector
- transcript connector
- AI conversation export connector
- SQL connector
- API connector

These remain future private connector work. They are not implemented in Sprint 09 public core.

## AI Conversation Exports

AI conversation connectors must separate:

- user messages
- assistant messages
- system/developer messages
- quoted content
- tool outputs

Default policy:

- user messages can contribute lexical/tone signal.
- assistant messages must not contribute voice signal.
- assistant messages may contribute topic context only if explicitly allowed by a later policy.
- tool outputs must not contribute voice signal.

## Connector Review Checklist

- [ ] No private names or paths in code.
- [ ] Credentials loaded only from env or ignored local config.
- [ ] Tests use synthetic data.
- [ ] Speaker attribution is explicit and advisory.
- [ ] Quoted/forwarded content is handled by adapters/classification.
- [ ] Connector can be disabled.
- [ ] Disabled connectors are inert.
- [ ] Dry-run avoids persistence.
- [ ] Failure does not leak secrets or paths in logs.
- [ ] No remote/provider/LLM calls are introduced.

# Connector Guide

Status: planning

## Connector purpose

Connectors turn external source records into normalized Imprint artifacts. They should not compile voice, decide final weights, or embed private assumptions.

## Connector contract

A connector emits `NormalizedArtifact` records.

Required fields:

- `artifact_id`
- `source_id`
- `source_type`
- `artifact_type`
- `text`
- `occurred_at`
- `speaker_id` or `speaker_label`
- `speaker_confidence`
- `metadata`

## Public connector rules

- Do not hard-code private paths.
- Do not hard-code private table names.
- Do not hard-code emails, names, or phone numbers.
- Do not require private services for tests.
- Provide synthetic fixtures.
- Use env vars for credentials.
- Use query files for SQL rather than inline private queries.

## Built-in public connectors

- `local_text`
- `local_markdown`
- `local_jsonl`
- `local_transcript_json`

## Private connector examples

Private deployments may configure connectors such as:

- sent email connector
- chat export connector
- transcript connector
- AI conversation export connector
- SQL connector
- API connector

These should be documented generically.

## AI conversation exports

AI conversation connectors must separate:

- user messages
- assistant messages
- system/developer messages
- quoted content
- tool outputs

Default policy:

- user messages can contribute lexical/tone signal.
- assistant messages must not contribute voice signal.
- assistant messages may contribute topic context only if explicitly allowed.
- tool outputs must not contribute voice signal.

## Connector review checklist

- [ ] No private names or paths in code.
- [ ] Credentials loaded only from env or local config.
- [ ] Tests use synthetic data.
- [ ] Speaker attribution is explicit.
- [ ] Quoted/forwarded content is handled.
- [ ] Connector can be disabled.
- [ ] Failure does not leak secrets in logs.

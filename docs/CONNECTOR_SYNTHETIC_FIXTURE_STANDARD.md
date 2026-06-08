# Connector Synthetic Fixture Standard

Status: Sprint 13 strategy gate

## Purpose

Private connectors cannot be implemented safely without synthetic fixtures that exercise source shape,
privacy boundaries, redaction, replay, and consent behavior. This standard defines fixture
requirements before private adapter work begins.

## Core Requirements

Synthetic fixtures must be:

- fictional
- small enough for public CI
- deterministic
- free of real credentials, real source paths, real account IDs, real people, and real message bodies
- representative of source-specific edge cases
- paired with tests that prove public-safe outputs remain raw-free and path-free

## Prohibited Fixture Content

Do not commit:

- real mailbox exports
- real chat exports
- real transcripts or audio
- real database dumps or SQL from private deployments
- real provider API responses
- real contact names, emails, handles, phone numbers, account IDs, tenant IDs, or source IDs
- real local paths or private hostnames
- credential-shaped placeholders

Use fictional names, reserved example domains, synthetic IDs, and generated content only.

## Required Fixture Categories

Each connector class must include fixtures for:

- happy-path subject-authored content
- third-party-authored contamination
- unknown authorship
- generated/system/template content
- quoted, forwarded, replied-to, summarized, or attachment-present content when the source supports it
- missing or invalid credential references without secret values
- local path or private locator redaction
- storage mode behavior
- replay metadata behavior
- source schema drift or malformed records

## Source-Specific Minimums

### Gmail

Fixtures must cover sent mail, received mail, quoted replies, forwards, attachments-present metadata,
signatures, notifications/templates, group recipients, and missing credential config.

### iMessage / Chat

Fixtures must cover subject messages, other participant messages, group chats, unknown sender,
quoted/replied-to content, edits/deletes/system messages, attachment-only messages, and participant
identifier redaction.

### Transcript / Recorder

Fixtures must cover subject speech, other speakers, unknown speakers, low-confidence diarization,
generated summaries, manual corrections, audio-present metadata without audio bytes, and vendor/device
identifier redaction.

### Database / Cloud

Fixtures must cover allowlisted subject rows, other-person rows, generated/system rows, schema drift,
query denylist failures, row limit behavior, DSN redaction, and replay from a synthetic snapshot.

## Fixture Naming and Location

Public fixtures should live under `tests/fixtures/` or `examples/synthetic_corpus/` using names that
make synthetic status obvious. Do not use names copied from private systems.

Recommended naming patterns:

- `synthetic-sent-mail.jsonl`
- `synthetic-group-chat.json`
- `synthetic-diarized-transcript.json`
- `synthetic-allowlisted-rows.jsonl`

## Expected Test Assertions

Each fixture set must support assertions that:

- connector dry-run reports counts without paths or raw text
- ingestion produces opaque `source-*` IDs
- non-subject content is excluded or quarantined
- generated/template content is excluded or quarantined
- public-safe exports contain no raw fixture text
- validation catches intentional credential, encoded credential, path, encoded path, and private metadata mutations
- replay/audit metadata is present without private locators

## Review Gate

A private connector is not implementation-ready until fixture standards are met and tests can run in
public CI without credentials or private infrastructure.

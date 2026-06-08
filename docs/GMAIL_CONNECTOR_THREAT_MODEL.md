# Gmail Connector Threat Model

Status: Sprint 13 strategy gate

## Scope

This document defines the conditions required before any Gmail or sent-mail connector can be
implemented. Sprint 13 does not implement Gmail OAuth, Gmail API calls, mailbox scraping, attachment
handling, or live account access.

A future Gmail connector may ingest owner-authorized mail artifacts only after satisfying this threat
model, the connector implementation standard, the credential storage policy, the consent policy, and
the synthetic fixture standard.

## Source Ownership and Consent

Gmail data is multi-person communication. The account owner can authorize access to their own mailbox,
but the account also contains messages written by other people. The connector must distinguish:

- mail authored by the profile subject
- quoted or forwarded material authored by others
- received mail authored by others
- system notifications, templates, calendar messages, and machine-generated content
- attachments and embedded documents with independent authorship

Default policy: compile only subject-authored sent content unless a source-specific policy explicitly
allows another category. Received mail, quoted threads, and attachments are contamination risks and
must default to excluded or quarantined.

## Credential Handling

Gmail credentials are high-risk OAuth credentials. A future connector must:

- request the narrowest feasible read scope for the chosen source class
- store tokens only through the approved credential storage policy
- never write refresh tokens into YAML, JSON, logs, public docs, fixtures, or exported artifacts
- redact account identifiers and token metadata from errors
- support explicit credential revocation and reauthorization
- fail closed when credentials are absent, expired, over-scoped, or stored in an unapproved location

Public examples may use only synthetic env var names. No real OAuth client IDs, secrets, scopes tied
to a real project, tenant IDs, email addresses, or mailbox paths belong in the public repository.

## Local Storage and Retention

The connector must support `metadata_only` by default. If local artifact storage is enabled, the local
store becomes protected data and must stay under ignored operator-controlled paths.

Retention policy must record:

- whether raw message bodies were retained
- whether headers were retained
- whether attachment metadata was retained
- whether attachments were skipped, summarized, or stored
- whether quoted thread sections were stripped, quarantined, or retained for audit only

## Replay and Rebuild Behavior

Rebuilds must be deterministic for the same authorized mailbox window and connector version. The
connector must record enough non-secret metadata to explain replay limits, including:

- selected mailbox category, such as sent-only
- time window or cursor class without exposing provider cursor secrets
- connector version
- parser version
- redaction and storage mode
- known skipped classes, such as attachments or quoted replies

Provider message IDs and thread IDs are private locators. They must not appear in public-safe exports.
If retained for local replay, they must stay in protected local state.

## Audit and Revocation

The connector must produce a local audit summary that answers:

- which mailbox class was read
- how many records were discovered, included, excluded, and quarantined
- how many records contained quoted text, attachments, or uncertain authorship
- which OAuth scopes were requested
- when credentials were last used and revoked, without printing token values

Revocation must invalidate future reads and mark cached private replay state as stale unless the
operator explicitly preserves it for local audit.

## Source-Specific Privacy Leaks

Gmail-specific leak vectors include:

- email addresses and display names
- message IDs, thread IDs, labels, folder names, and provider cursors
- quoted reply chains and forwarded content
- signature blocks with phone numbers or addresses
- attachments containing unrelated people or organizations
- calendar and notification emails that look authored by the user but are templates
- provider headers revealing account, device, client, or routing metadata

Public-safe outputs must expose only opaque source IDs and aggregate support metadata.

## Adapter Hint Trust Boundaries

Gmail headers and folders may provide hints, but they are not durable truth. The connector may hint at
sent-vs-received state, sender, recipients, quote boundaries, attachment presence, and timestamp
bucket. Classification must still decide authorship, inclusion, quarantine, and AI/template risk.

The connector must not infer personality, voice, topic preferences, intent, or truth about the subject.
It may only normalize source records and preserve advisory metadata.

## Synthetic Fixture Requirements

Before implementation, synthetic Gmail fixtures must cover:

- subject-authored sent mail
- received mail from another person
- quoted reply contamination
- forwarded thread contamination
- signature block redaction
- attachment-present metadata with no attachment body
- template or notification email
- multi-recipient and group-thread cases
- expired or missing credential configuration errors using fake env var names only

Fixtures must use fictional names, domains reserved for examples, fake IDs, and synthetic message
bodies. No real mailbox exports or provider responses may be committed.

## Public Repository Safety Constraints

The public repository may contain the threat model, connector interface expectations, and synthetic
fixtures. It must not contain Gmail API client setup, live OAuth flows, real mailbox schemas copied
from a private account, private account examples, or real provider responses.

A Gmail connector remains blocked until this threat model has implementation tests, redaction tests,
credential-storage tests, replay/audit tests, and consent-boundary tests.

# iMessage Connector Threat Model

Status: Sprint 13 strategy gate

## Scope

This document defines the conditions required before any iMessage, Messages database, chat export, or
similar local chat connector can be implemented. Sprint 13 does not implement local database access,
chat export parsing beyond existing synthetic transcript/local adapters, device inspection, or live
message ingestion.

## Source Ownership and Consent

Chat logs are inherently multi-person records. The device owner may control a local database or
export, but they do not own every message in it. A future connector must distinguish:

- messages authored by the profile subject
- messages authored by other participants
- group chat records
- quoted, forwarded, reacted-to, or attachment-only messages
- system messages, tapbacks, delivery events, and edits
- unknown or ambiguous sender records

Default policy: only subject-authored messages can support profile signals. Other participants'
messages must be excluded or quarantined unless explicitly needed for local audit counts.

## Credential and Access Handling

iMessage-style sources may not use OAuth credentials, but local database and backup access can expose
entire private communication histories. A future connector must:

- require explicit operator confirmation for database or export selection
- never auto-scan default device databases from public examples
- never bypass operating-system permissions or encryption
- avoid printing local database paths in errors or dry-run output
- treat device IDs, phone numbers, account handles, chat IDs, and backup identifiers as private locators

If an implementation needs a helper tool or export process, that process must be documented as a
private local prerequisite and excluded from public CI.

## Local Storage and Retention

Default storage must be `metadata_only`. If raw chat text is retained in a local artifact store, it is
protected data and must remain under ignored local paths.

Retention metadata must record:

- whether raw message bodies were stored
- whether non-subject messages were skipped, counted, or quarantined
- whether attachments were skipped
- whether edits, reactions, and deleted-message markers were retained as metadata
- whether participant identifiers were hashed, redacted, or retained locally

## Replay and Rebuild Behavior

Replay must be based on an explicit export or local snapshot selected by the operator. The connector
must not silently re-read an evolving device database without recording the snapshot policy.

Replay metadata should include:

- source snapshot identifier or content hash
- parser version
- participant mapping policy
- time window
- storage mode
- excluded message classes

Raw chat IDs and participant handles must remain outside public-safe exports.

## Audit and Revocation

A future connector must produce a local audit summary with:

- total chats and messages discovered
- subject-authored messages included
- other-participant messages excluded or quarantined
- group chat counts
- attachment, edit, reaction, and unknown-speaker counts
- local source snapshot and parser version without path disclosure

Revocation means removing the configured source path or snapshot permission and marking derived local
state stale. Public-safe exports generated before revocation remain raw-free but should be traceable
to a build manifest that records replay limitations.

## Source-Specific Privacy Leaks

Chat-specific leak vectors include:

- phone numbers, emails, handles, contact names, and group names
- device database paths and backup paths
- chat IDs and participant IDs
- message timestamps precise enough to identify events
- other participants' messages and quoted replies
- attachment filenames, previews, stickers, location shares, and media metadata
- deleted-message and edit history metadata

Public-safe outputs may contain only opaque source IDs, coarse support metadata, and non-raw profile
patterns.

## Adapter Hint Trust Boundaries

Local chat metadata may hint at sender, chat type, timestamp, reply relationship, and attachment
presence. These hints are advisory. Classification and compiler policy must still determine
subject-authored status, exclusion, quarantine, and support eligibility.

The connector must not infer relationship strength, sentiment, identity truth, or profile traits from
participant metadata.

## Synthetic Fixture Requirements

Before implementation, synthetic chat fixtures must cover:

- one-on-one subject-authored messages
- one-on-one other-participant messages
- group chat contamination
- unknown sender records
- quoted or replied-to messages
- attachment-only and media-placeholder messages
- edited/deleted/system messages
- timestamp and participant redaction behavior
- missing local source configuration errors

Fixtures must be fictional and generated for the test suite. No real chat exports, device database
schemas copied from a private machine, contact names, handles, or message bodies may be committed.

## Public Repository Safety Constraints

The public repository may contain generic parser expectations and synthetic fixtures only. Real device
paths, backup instructions that reveal private machine layouts, local database files, chat exports,
and participant maps must stay outside public core.

An iMessage/chat connector remains blocked until source consent, participant separation, local access,
redaction, replay, and audit tests exist.

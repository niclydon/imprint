# Consent and Multi-Person Data Policy

Status: Sprint 13 strategy gate

## Purpose

Imprint profiles are owner-controlled expression profiles. Private source connectors often read
communications that include other people. This policy defines consent, authorship, contamination, and
multi-person boundaries before real private adapters can be implemented.

## Core Principle

Possession of a data source is not enough. A connector may be authorized to read a source, but the
compiler may use only evidence that is appropriate for the profile subject and consent context.

Default behavior must be conservative:

- subject-authored content may be eligible
- other people's content is excluded or quarantined
- unknown authorship is quarantined
- quoted, forwarded, generated, or template content is excluded or quarantined
- group contexts require explicit handling before support can become durable

## Consent Classes

A source-specific threat model must classify each source into one of these classes:

- **Owner-authored:** authored by the profile subject and controlled by the operator.
- **Owner-held multi-person:** held by the operator but includes other people.
- **Third-party-authored:** written or spoken by someone else.
- **Generated/system:** produced by software, templates, assistants, or automated systems.
- **Unknown:** attribution is missing or unreliable.

Only owner-authored content may support profile signals by default.

## Multi-Person Risks

Private connectors must handle:

- email reply chains and forwarded messages
- received mail and attachments
- direct chats with another person
- group chats
- transcript segments from multiple speakers
- database rows about multiple people
- generated summaries of meetings or threads
- mixed authorship documents

A future connector must not launder other people’s words into the subject’s profile through metadata
hints, summaries, or aggregate counts.

## Authorship Evidence

Connectors may provide advisory hints such as sender, speaker, participant ID, thread role, source
folder, or row owner. These hints are not final truth.

Classification and compiler policy must decide:

- whether the subject authored the artifact
- whether authorship is confident enough for durable support
- whether content should be included, excluded, quarantined, or downweighted
- whether AI-generated or template content is contamination

When authorship evidence is weak, the safe result is quarantine.

## Consent Requirements Before Implementation

Each private connector must document:

- who can authorize the connector
- whose data may appear in the source
- which records can support the subject profile
- which records are audit-only
- how other people’s content is excluded or quarantined
- how group contexts are represented
- how consent revocation affects future reads and retained local state

## Output Rules

Public-safe exports must never expose:

- raw text from the subject or third parties
- participant names, emails, phone numbers, handles, account IDs, or source locators
- evidence that reveals private relationships or group membership
- quoted content or generated summaries as examples

Aggregate support metadata may be used only when it cannot identify private people or sources.

## Review and Override Policy

Any connector that wants to include ambiguous, mixed, or group-authored content needs an explicit
source-specific policy and tests. Operator convenience is not sufficient justification.

Manual overrides, if added later, must be local-only, audited, and excluded from public-safe exports.
They must not silently convert third-party content into durable subject evidence.

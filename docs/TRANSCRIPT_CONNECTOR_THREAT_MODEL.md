# Transcript Connector Threat Model

Status: Sprint 13 strategy gate

## Scope

This document defines the conditions required before private transcript, recorder, meeting-note,
Plaud-like, Looki-like, or audio-derived transcript connectors can be implemented. Sprint 13 does not
implement live device connectors, recorder APIs, audio ingestion, diarization, or real transcript
imports beyond existing synthetic local transcript fixtures.

## Source Ownership and Consent

Transcripts often contain multiple speakers and sometimes people who did not know they were recorded.
A future connector must distinguish:

- words spoken by the profile subject
- words spoken by other participants
- unknown or low-confidence speakers
- diarization segments with uncertain attribution
- AI-generated summaries or action items
- recorder metadata and device/operator notes
- transcript corrections and human edits

Default policy: only high-confidence subject-authored transcript segments may support profile signals.
Third-party voices, unknown speakers, and generated summaries must be excluded or quarantined.

## Credential and Device Handling

Transcript sources may come from local files, device exports, or vendor APIs. A future connector must:

- use local export files by default before any live API work
- require a source-specific threat model extension before vendor API access
- store API credentials only through the credential storage policy
- keep device IDs, recording IDs, workspace IDs, and share URLs out of public-safe outputs
- redact local paths and vendor identifiers in errors
- fail closed on missing diarization or speaker-attribution metadata unless the operator chooses an audit-only mode

## Local Storage and Retention

Default storage must be `metadata_only`. Raw transcripts and audio files are protected data. Audio is
higher risk than transcript text and must not be stored by a connector unless explicitly enabled in a
future local-only policy.

Retention metadata must record:

- whether raw transcript text was retained
- whether audio was present and skipped
- whether diarization labels were retained
- speaker confidence thresholds
- generated-summary handling
- manual correction provenance

## Replay and Rebuild Behavior

Replay must distinguish raw audio, transcript text, diarization metadata, and generated summaries.
The connector must record:

- source export hash or opaque local snapshot ID
- transcript parser version
- diarization source and confidence policy
- manual correction policy
- skipped audio policy
- storage mode and replay limitations

A rebuild from transcript text is not equivalent to a rebuild from raw audio. The build manifest or
local audit summary must disclose that limitation without exposing raw content.

## Audit and Revocation

A future connector must produce a local audit summary with:

- recordings or transcript files discovered
- segments by speaker-confidence bucket
- subject-authored segments included
- third-party, unknown, and generated-summary segments excluded or quarantined
- audio-present counts and audio-retention status
- parser, diarization, and correction policy versions

Revocation removes connector access to transcript exports or vendor credentials and marks derived
local replay state stale unless explicitly preserved under protected local storage.

## Source-Specific Privacy Leaks

Transcript-specific leak vectors include:

- third-party voices
- speaker names and labels
- meeting titles, calendar metadata, and organization names
- recorder IDs, recording URLs, workspace IDs, and device IDs
- precise timestamps tied to meetings or locations
- raw audio, audio filenames, and generated summaries
- diarization errors that assign another person's words to the subject

Public-safe exports must not contain raw transcript text, audio locators, meeting identifiers, or
speaker names from private sources.

## Adapter Hint Trust Boundaries

Transcript metadata may hint at speaker, confidence, source device, timestamp, and generated-summary
status. These hints are advisory. Classification and compiler policy must re-assess authorship and
support eligibility.

The connector must not use transcript summaries as evidence of the subject's expression unless the
summary itself is explicitly treated as generated or third-party-authored content.

## Synthetic Fixture Requirements

Before implementation, synthetic transcript fixtures must cover:

- high-confidence subject speech
- third-party speech
- unknown speaker segments
- low-confidence diarization
- overlapping or interrupted speech
- generated summaries and action items
- manual transcript corrections
- audio-present metadata without audio bytes
- vendor/device identifier redaction

Fixtures must be synthetic and must not include real meeting transcripts, real participant names,
real audio filenames, or vendor export payloads from private accounts.

## Public Repository Safety Constraints

The public repository may contain generic transcript schemas, synthetic transcript fixtures, and
policy tests. It must not contain audio, private transcripts, recorder exports, vendor API clients, or
real meeting metadata.

A private transcript connector remains blocked until speaker consent, diarization uncertainty,
audio/text separation, replay, audit, and redaction tests exist.

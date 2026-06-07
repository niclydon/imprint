# Evidence and Confidence

Status: Sprint 01.5 remediation decision

## Decision

Evidence is the support trail for a claim. Confidence is a bounded estimate about the strength of
that claim, not truth about the person.

Authorship-origin classification is evidence-based metadata classification. It is not reliable AI
detection and must not pretend to be.

## Evidence Requirements

Every signal should answer:

- What artifacts supported this?
- What source types contributed?
- What time window was observed?
- What classification made the artifacts usable?
- What extraction method produced the signal?
- What evidence was excluded or quarantined?
- Is raw text available locally for audit?

Public-safe evidence must use references and aggregate support, not raw excerpts.

## Evidence Reference Fields

Sprint 02 should consider:

- artifact ID
- source ID
- artifact type
- source type
- classification ID
- extraction run ID
- content hash or fingerprint
- artifact timestamp or coarse time bucket
- inclusion status
- support count
- quarantine count
- source diversity

## Confidence Components

Confidence should be decomposable.

Recommended components:

- attribution confidence
- authorship-origin confidence
- extraction confidence
- evidence strength
- source diversity
- policy fit
- model agreement, if applicable

A single display confidence may exist, but it should be derived from named components.

## Authorship-Origin Policy

Authorship origin means the best-supported classification from available evidence.

Allowed evidence:

- source metadata
- connector role fields
- explicit speaker labels
- message author fields
- known assistant/tool roles in AI exports
- user-provided source policy
- template or notification markers
- quote/forward parsing

Disallowed claim:

- "This is AI-generated" solely because a detector guessed it.

AI detectors may contribute weak evidence, but their output should never be treated as ground
truth.

## Unknown Handling

Unknown remains unknown.

Unknown or weakly supported authorship should:

- reduce confidence
- prevent high-stakes profile claims
- default to lower weights
- be quarantined when speaker or authorship risk is material
- remain visible in source summaries

## Claim Levels

Signals should declare:

- `observation`: directly supported pattern
- `bounded_interpretation`: cautiously inferred expression guidance
- `prohibited`: diagnosis, intent attribution, personality typing, or unsupported identity claim

Prohibited claims should fail validation or be quarantined before profile compilation.

## Sprint 02 Implications

Sprint 02 must define:

- evidence model
- confidence model
- authorship-origin taxonomy
- unknown and suspected AI-assisted weighting
- claim-level validation
- public-safe evidence references

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

Sprint 04 artifact classification uses a versioned deterministic confidence model. The baseline
components are attribution, authorship-origin confidence, evidence strength, source reliability,
policy fit, contamination penalty, and a derived display score. If these formulas change, the
classifier should version the model rather than silently redefining old results.

Sprint 05 artifact-level signal extraction derives signal confidence from classification confidence
plus deterministic rule reliability and evidence strength. Quarantined or excluded artifacts must
not silently become durable signal support.

Sprint 06 profile compilation derives profile confidence from durable observation signals only.
The `sprint06-confidence-v1` summary averages candidate confidence components, includes source
diversity, applies a bounded support-count factor, and records classifier/signal model versions in
support metadata. Display confidence remains a support-strength summary, not truth about a person.

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

Adapter-provided metadata is upstream source evidence, not final classification truth. Hints such
as `authorship_origin`, `authorship_confidence`, `classification_label`, and record-level
`artifact_type` must be re-assessed by classification logic before they influence durable profile
claims or validation outcomes.

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

## Sprint 02.5 Model Evidence Boundary

Model output can support evidence only according to its role.

Profile-affecting model roles such as classification, signal extraction, claim validation, evidence interpretation, confidence assessment, and drift comparison must be recorded in the build manifest. Their output is compiler evidence, not ground truth about the subject.

Experience-only model roles such as report writing or first-run artifact generation do not support durable profile claims unless their output is explicitly reintroduced as an artifact and passes classification, authorship-origin, confidence, evidence, and claim validation requirements.

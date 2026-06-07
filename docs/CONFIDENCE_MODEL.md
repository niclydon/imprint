# Confidence Model

Status: Sprint 02 schema contract

## Definition

Confidence is a bounded, heuristic estimate of support for an expression claim in the compiled corpus. It is not a probability that a person has a trait and not a truth score about identity.

## Components

Every confidence object decomposes into:

- `attribution`: evidence that artifacts belong to the intended subject.
- `authorship_origin`: evidence that the material is human-origin, human-directed AI-assisted, quoted, assistant output, or otherwise classified.
- `extraction`: reliability of the extraction method for the signal family.
- `evidence_strength`: quantity, quality, and directness of support.
- `source_diversity`: breadth across source types or declared narrowness of a context.
- `policy_fit`: alignment with source and authorship policies.
- `model_agreement`: optional agreement across extractors or models.
- `display`: derived summary for UI consumption.

## Combination Policy

Display confidence must be derived from named components and must not hide a low-confidence safety component. Implementations may use weighted heuristics, but the schema preserves component scores so future compilers can migrate formulas.

Unknown or weak authorship lowers confidence. AI detector output may affect metadata and weak evidence only; it cannot establish authorship ground truth.

## Minimum Guidance

- `observation` claims require support and nonzero evidence strength.
- `bounded_interpretation` claims require stronger evidence and explicit rationale.
- `quarantined` claims are retained for review, not emitted as public-safe claims.
- `prohibited` claims fail canonical and public-safe export validation.

## What Confidence Is Not

Confidence is not statistical certainty unless a specific extractor declares a statistically valid method. It is not model self-confidence. It does not authorize diagnostic, personality-typing, hidden-intent, or unsupported identity claims.

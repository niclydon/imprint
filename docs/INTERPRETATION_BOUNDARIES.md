# Interpretation Boundaries

## Purpose

Define the line between observation and interpretation.

## Observation

Observation is preferred.

Examples:

- uses short paragraphs
- frequently cites evidence
- often explains through examples
- uses humor in casual communication

These are evidence-backed observations.

## Interpretation

Interpretation is risky.

Examples:

- analytical
- skeptical
- optimistic
- sarcastic

These may be allowed if clearly labeled as interpretations and confidence-scored.

Machine-readable schemas should prefer `bounded_interpretation` for these claims and include
evidence support. They should avoid schema fields such as `identity.stance`,
`identity.recurring_lens`, or personality-like labels.

## Diagnosis

Diagnosis is prohibited.

Examples:

- depression
- anxiety disorder
- bipolar disorder
- narcissistic personality disorder
- autism spectrum disorder

Imprint is not a diagnostic system.

Diagnostic, personality-typing, and hidden-intent claims should be represented as prohibited and
must not enter compiled profiles.

## Intent Attribution

Imprint must not claim intent.

Bad examples:

- wanted to persuade
- was angry
- was manipulative

The system may only discuss observable artifacts.

## Profile Safety Rule

When uncertain:

Prefer a weaker observation over a stronger interpretation.

Observation > Interpretation > Diagnosis

Sprint 05 baseline signal extraction should overwhelmingly emit `observation` claims. If an
artifact is not cleanly eligible for durable support, prefer a quarantined candidate signal over a
stronger interpretation.

## Claim Levels

Sprint 02 schemas should represent claim levels explicitly:

- `observation`: directly supported expression pattern
- `bounded_interpretation`: cautious interpretation with evidence and confidence
- `prohibited`: diagnosis, personality typing, intent attribution, or unsupported identity claim

Prohibited claims should fail validation or be quarantined before profile compilation.

# First-Run Output

Status: Sprint 07 baseline

## Purpose

The first-run output is the first meaningful user-facing explanation of what Imprint learned. It is
not raw JSON, a writing prompt, a generated article, a personality report, or a diagnosis.

## Source of Truth

The first-run output is generated from compiled `ExpressionProfile` data only.

It may use:

- profile ID and build metadata
- compiled expression pattern claims
- support counts
- confidence summaries
- source-type summaries
- limitations and compatibility warnings

It must not use:

- raw artifact text
- source snippets
- filesystem paths
- private local locators
- provider prompts
- downstream writing instructions
- generated demos or article text

## Required Sections

The Sprint 07 baseline emits:

- `Profile Overview`
- `Strongest Observed Patterns`
- `Limits and Cautions`
- `What Imprint Cannot Say`

## Language Rules

Use:

- “Observed pattern”
- “Supported by N included artifacts”
- “Confidence summarizes support strength”
- “Limited by metadata-only storage”

Avoid:

- “The subject is...”
- “This proves...”
- “Personality...”
- diagnostic, psychological, emotional-state, hidden-intent, or identity-trait language

## Experience Boundary

The first-run output is experience-only. It does not mutate the durable profile and does not become
evidence unless a future workflow explicitly promotes it as a new artifact and sends it through
normal ingestion, classification, evidence, confidence, and claim validation.

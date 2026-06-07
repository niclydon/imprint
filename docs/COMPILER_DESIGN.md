# Compiler Design

Status: Sprint 06 baseline

## Purpose

The profile compiler aggregates artifact-level signal candidates into reusable expression profiles.
It is deterministic, local-only, and conservative: it summarizes supported expression patterns
without adding person-level psychological, diagnostic, or intent claims.

## Pipeline

1. Ingest normalized artifacts.
2. Classify artifacts for inclusion, exclusion, quarantine, and authorship-origin risk.
3. Extract artifact-level signal candidates.
4. Compile only eligible durable observation signals into profile-level `Signal` and `Claim`
   objects.

## Aggregation

Signals are grouped by profile signal family, candidate name, observed feature, and extraction
rule. Artifact-level families are projected into profile-level families:

- `structure` and `formatting` compile to `structure`
- `lexical` compiles to `lexical`
- `tone_marker` compiles to `tone`
- `rhetorical_pattern` and `reasoning` compile to `reasoning`
- `narrative` compiles to `narrative`
- `anti_pattern` compiles to `anti_pattern`

The compiler emits one profile signal per deterministic pattern group.

## Version Boundaries

Compiler output records:

- compiler version: `sprint06-rule-v1`
- compiler confidence model: `sprint06-confidence-v1`
- classifier confidence model versions in support metadata
- signal extraction model versions in support metadata and build manifest

Durable signals from multiple signal model versions are rejected rather than silently merged.
Mixed classifier versions are recorded in support metadata and the build manifest so downstream
review can treat the profile as compatibility-sensitive instead of assuming a clean expression-only
change.

## Validation Gates

Before aggregation, the compiler checks that each candidate has a matching artifact, source ID,
classification ID, included classification label, durable status, allowed claim level, and opaque
source ID. Prohibited candidates fail compilation. Quarantined, excluded, non-durable, and default
bounded-interpretation candidates do not enter durable support.

## Non-Goals

Sprint 06 does not generate reports, downstream writing instructions, publishing prompts, remote
API calls, embeddings, vector search, or private connector behavior.

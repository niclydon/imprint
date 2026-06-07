# Sprint 06 - Profile Compiler
Primary Model: GPT 5.5
Reviewer: Gemini

Compile signals into expression profiles, confidence metrics and drift reports.

Reviewer Prompt: Challenge weighting, stability, drift and versioning. Generate COMPILER_RISKS.md.

Implementation Plan: `SPRINT_06_IMPLEMENTATION_PLAN.md`

## Implemented Baseline

- Deterministic `ProfileCompiler` aggregates durable artifact-level observation signals into
  evidence-backed profile signals.
- Quarantined, non-durable, prohibited, and default bounded-interpretation candidates cannot enter
  durable profile support.
- Support metadata preserves contributing signal IDs, artifact references, opaque source IDs,
  classification model versions, signal model versions, and rule IDs.
- Mixed durable signal model versions are rejected rather than silently merged.
- CLI command `imprint compile` runs local ingest, classify, extract, and compile without LLM calls
  or provider dependencies.

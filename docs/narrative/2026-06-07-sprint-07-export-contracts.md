# Sprint 07 Narrative: Export Contracts and First-Run Experience

## Status

Implemented and ready for adversarial review.

## Context

Sprint 06 made compiled expression profiles possible. Sprint 07 made those profiles consumable. The
core challenge was not serialization itself; it was preserving every upstream safety boundary while
creating outputs that are useful to humans, machines, and future downstream systems.

## Shipped Behavior

- Added `src/imprint/exports/` with shared safety validation and four export surfaces:
  - canonical JSON
  - human-readable Markdown
  - first-run “What Imprint Learned” output
  - Mosvera expression overlay skeleton
- Added `imprint export-profile` for local compile-and-export smoke paths.
- Added deterministic public-safe payload construction from compiled profile data only.
- Added safety validation for prohibited claims, ungated bounded interpretations, non-durable
  support, mixed signal model versions, path-like source IDs, and generation-control keys.

## Safety Boundaries

Sprint 07 exports do not include raw artifact text, filesystem paths, private local locators,
provider prompts, generation settings, downstream writing instructions, Broadside integration,
Mosvera runtime behavior, or LLM calls.

The first-run output remains experience-only. It explains compiled profile patterns and limitations
without becoming profile evidence or implying that Imprint has diagnosed, simulated, or become the
subject.

## Test Coverage

`tests/test_exports.py` verifies:

- deterministic JSON export
- deterministic Markdown export
- no raw text or path leakage
- prohibited claims cannot export
- bounded interpretations remain policy-gated
- source IDs remain opaque
- mixed signal model versions cannot export as comparable
- first-run output uses compiled profile data only
- Mosvera overlay contains expression summaries only
- CLI export smoke paths work for all formats

Final validation: `pytest -q` passed.

## Handoff to Sprint 08

Sprint 08 can build publishing/downstream projections from the canonical export contract. It should
not move prompt assembly, model tuning, generation settings, or workflow ownership into core Imprint.

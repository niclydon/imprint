# 2026-06-07: Schema and Model Contract Foundation

## Context

The latest session moved Imprint from “architecture intent” into enforceable contracts. We finalized Sprint 02 and Sprint 02.5 documentation into code-level schema artifacts so future implementation work can target stable interfaces instead of assumptions.

## Narrative

- **Schema layer landed first.** A new Pydantic contract module was added under `src/imprint/schemas/` with a focused vocabulary for artifact handling, evidence claims, signal families, profile versions, confidence and validation, and model invocation metadata.
- **Policy and safety semantics were encoded.** Provider policy and model capability boundaries were codified in docs and represented in schema fields to keep remote inference behavior explicit, auditable, and portable.
- **Model neutrality became technical.** Contracts were written as provider-agnostic abstractions so local and remote providers can plug into the same profile workflow later without redesign.
- **Synthetic validation coverage arrived with it.** The commit added schema tests that assert both stable contract shape and Sprint gating behavior for the key objects this layer protects.
- **Documentation and public story were updated together.** Sprint and model-policy docs were expanded, and project assets were added for README presentation, so narrative and implementation move in sync.

## Outcome

Imprint now has a stronger boundary between product strategy and execution:

- downstream code can treat schema as shared language,
- reviewers can evaluate privacy and drift implications from concrete fields,
- and Sprint 03 planning can continue without re-opening core definitions.

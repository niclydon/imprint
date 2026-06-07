# Mosvera Integration

Status: Sprint 08 consumer contract

## Boundary

Imprint compiles expression. Mosvera compiles aesthetic intent.

Sprint 08 defines a public-safe expression overlay contract Mosvera can consume later. It does not
implement Mosvera runtime behavior, provider behavior, aesthetic compilation, visual prompt assembly,
or image generation instructions.

## Overlay Contents

The Mosvera consumer contract is generated from canonical Imprint JSON by
`mosvera_consumer_contract(profile)`. The legacy `mosvera_expression_overlay(profile)` remains a
Sprint 07-compatible overlay and now also surfaces compatibility warnings.

The contract may include:

- contract name and contract schema version
- source profile ID and canonical export reference
- compiler, classifier, signal, and export version metadata
- mandatory compatibility warnings
- no-raw-text evidence policy
- expression summaries
- avoid-pattern summaries
- opaque source IDs
- boundary statement

Expression summaries include:

- family
- name
- observed expression pattern
- confidence
- support artifact count
- source types
- opaque source IDs

## Explicit Non-Goals

The overlay must not contain:

- provider-specific prompts
- image generation instructions
- model settings
- raw Imprint evidence or raw artifact text
- private source locators
- aesthetic-intent compilation
- Mosvera runtime behavior

## Review Rule

If a field tells Mosvera how to call or tune a model, it does not belong in the Imprint contract. If
a field summarizes what Imprint observed about expression, it may belong when it remains public-safe,
evidence-scoped, and warning-preserving.

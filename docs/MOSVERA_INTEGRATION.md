# Mosvera Integration

Status: Sprint 07 export contract skeleton

## Boundary

Imprint compiles expression. Mosvera compiles aesthetic intent.

Sprint 07 defines a public-safe expression overlay contract that Mosvera can consume later. It does
not implement Mosvera runtime behavior and does not merge the systems.

## Overlay Contents

The overlay contains:

- contract name and overlay version
- source profile ID
- compiler and signal model version metadata
- no-raw-text evidence policy
- expression summaries
- anti-pattern summaries
- boundary statement

Expression summaries include:

- family
- name
- observed expression pattern
- confidence
- support artifact count
- source types

## Explicit Non-Goals

The overlay must not contain:

- provider-specific prompts
- image generation instructions
- model settings
- raw Imprint evidence
- private source locators
- aesthetic-intent compilation
- Mosvera workflow/runtime behavior

## Review Rule

If a field tells Mosvera how to call or tune a model, it does not belong in the Sprint 07 overlay.
If a field summarizes what Imprint observed about expression, it may belong if it remains
public-safe and evidence-scoped.

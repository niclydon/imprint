# Derived Profile Model

Status: Sprint 01.5 remediation decision

## Decision

Avoid hidden inheritance.

A master profile and derived profiles are explicit compiled views over evidence. Derived profiles
reference a baseline profile but do not implicitly inherit unspecified fields at runtime.

## Master Profile

A master profile is the broadest compiled expression profile for a subject under a declared corpus
window, source policy, authorship policy, and build manifest.

It is not a personality model or complete identity model.

## Derived Profile

A derived profile is a compiled context view.

Examples:

- casual
- technical
- published
- email
- podcast
- executive

Each derived profile must declare:

- baseline profile ID and version
- context label
- source filters
- artifact type filters
- time window, if different
- source policy overrides, if any
- authored-origin policy overrides, if any
- included/quarantined/excluded counts
- divergences from baseline

## Inheritance Policy

Derived profiles may reference baseline profiles for comparison, but should compile their own
signals from filtered evidence.

Allowed:

- baseline reference
- explicit copied fields with provenance
- explicit divergences
- explicit context constraints

Not allowed:

- hidden runtime fallback to master profile fields
- downstream consumers guessing merge semantics
- silently overriding baseline signals without recording divergence

## Divergences

A divergence is a structured statement that a context profile differs from its baseline.

Examples:

- casual artifacts have shorter paragraph-like units than published artifacts
- technical artifacts include more operational evidence references
- podcast transcripts include more unfinished clauses than essays

Divergences need evidence support and confidence. Weak divergences should be omitted or marked low
confidence.

Planned shape:

```json
{
  "divergence": {
    "signal_family": "structure",
    "pattern": "shorter_paragraph_units",
    "baseline_value": {
      "summary": "Published artifacts commonly use multi-paragraph setup before conclusion.",
      "confidence": 0.72
    },
    "context_value": {
      "summary": "Casual artifacts usually move directly from observation to action.",
      "confidence": 0.81
    },
    "direction": "context_is_more_direct",
    "claim_level": "observation",
    "support": {
      "baseline_artifact_count": 34,
      "context_artifact_count": 210,
      "source_types": ["article", "chat_message"]
    }
  }
}
```

## Collision Handling

When profiles disagree, Imprint should preserve the conflict rather than flatten it.

Example:

- baseline: high use of concrete operational evidence
- casual: lower use of explicit evidence markers
- technical: higher use of evidence markers

The export should show context-specific values and source support, not compute a vague average.

Collision labels:

- `context_specific`: both values are valid in their contexts
- `baseline_weak`: baseline lacks enough evidence to override context
- `context_weak`: context lacks enough evidence to override baseline
- `policy_conflict`: source weighting or authorship policy changed the result
- `not_comparable`: context and baseline were compiled under incompatible manifests

## Compilation Strategy

MVP context profiles should recompile signals from filtered evidence rather than merge master
signals. This is more expensive but avoids hidden inheritance and makes divergences auditable.

Allowed reuse:

- normalized artifacts
- classifications
- source policy definitions
- extractor run metadata

Not allowed:

- deriving context signals by averaging or rewriting master profile prose
- silently filling missing context fields from the master profile

Cost tradeoff: context compilation is roughly proportional to the number of requested contexts.
The MVP should keep the number of context profiles small and explicit.

## Rejected Alternatives

### Implicit Inheritance

Rejected because downstream consumers would not know whether a value came from context evidence or
fallback behavior.

### Fully Separate Profiles Only

Rejected because users need to compare context profiles against a baseline.

### Blended Profiles by Default

Rejected because blends hide context conflicts and invite consumer-specific behavior into core.

## Sprint 02 Implications

Sprint 02 schemas must include:

- baseline profile references
- context filters
- source policy overrides
- divergence objects
- collision labels
- no hidden inheritance semantics
- context compilation strategy metadata

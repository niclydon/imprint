# Profile Compilation Rules

Status: Sprint 06 baseline

## Eligibility

Compiled profile support may include only signal candidates that are all of the following:

- `durable=true`
- `claim_level=observation`
- backed by an `included` artifact classification
- public-safe, with opaque source IDs
- produced by a compatible signal model version

The compiler skips quarantined and non-durable candidates. It rejects prohibited candidates. It
excludes bounded interpretations by default unless an explicit future policy allows them.

## Evidence Policy

Every compiled profile signal keeps support metadata without raw text:

- contributing signal IDs
- evidence references with artifact IDs and opaque source IDs
- source types
- classification IDs
- classification model versions
- signal model versions
- extraction rule IDs
- support counts
- public-safe audit limitations

Profile claims use aggregate wording such as “Across included artifacts...” and do not include
source snippets or local paths.

## Confidence Policy

Profile confidence summarizes support strength, not truth about a person. The deterministic
`sprint06-confidence-v1` calculation averages candidate confidence components and applies a bounded
support-count factor. It records decomposed confidence fields so downstream consumers can audit the
result without treating display confidence as ground truth.

The baseline formula is:

```text
display = clamp(
  (
    0.20 * avg(attribution)
    + 0.20 * avg(authorship_origin)
    + 0.20 * avg(extraction)
    + 0.20 * avg(evidence_strength)
    + 0.10 * source_diversity
    + 0.10 * avg(policy_fit)
  )
  * min(1.0, 0.55 + 0.15 * included_support_count),
  low=0.05,
  high=0.95
)
```

The formula version is a compatibility boundary. Changing weights, support-count handling, or
component semantics requires a new compiler confidence model version.

## Build Manifest Policy

Compiled profiles record schema, compiler, classifier, extractor, source-policy,
authorship-policy, export-schema, artifact-store, and config-hash metadata in `BuildManifest`.
The local rule baseline records no model provider, model name, model version, or
profile-affecting model invocations.

## Context Profile Policy

Sprint 06 may emit minimal context-profile scaffolding derived from safe source-type metadata.
These context profiles record explicit filters and counts only. They do not contain hidden
inheritance, divergences, prompt instructions, or private source locators.

## Safety Rules

The compiler must not compile diagnostic, personality-typing, hidden-intent, or unsupported
identity claims. When evidence is weak or contaminated, prefer no compiled claim over a stronger
interpretation.

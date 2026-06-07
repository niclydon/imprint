# Sprint 01.5 Remediation Summary

Status: Sprint 01.5 output

## Verdict

Sprint 02 can proceed after Sprint 01.5.

The adversarial review identified real blockers. They are resolved as architectural decisions,
schema constraints, and explicit Sprint 02 gates, not implementation code.

## Resolved Blockers

### Artifact Storage and Auditability

Decision: Imprint may store raw artifact text locally in an explicit user-controlled Artifact Store
for compilation, audit, and regeneration.

Guardrail: the Artifact Store is not a memory system and must not expose arbitrary recall.

Primary doc: `docs/ARTIFACT_STORAGE_POLICY.md`

### Extractor Versioning and Determinism

Decision: every profile build must include a build manifest. Drift must distinguish expression
drift, compiler drift, and corpus drift.

Primary doc: `docs/EXTRACTOR_VERSIONING.md`

### Export Boundaries

Decision: core exports are profile contracts and projections. Prompt assembly and ghostwriting
workflow belong to downstream systems.

Primary doc: `docs/EXPORT_BOUNDARIES.md`

### Derived Profile Model

Decision: derived profiles are explicit compiled views with baseline references, filters,
divergences, and collision handling. There is no hidden inheritance.

Primary doc: `docs/DERIVED_PROFILE_MODEL.md`

### Terminology and Interpretation Safety

Decision: schema-level contracts should use safer terms such as `expression_profile`,
`expression_posture`, `rhetorical_patterns`, and `context_profiles`. Broad identity language is
not a machine-readable schema claim.

Updated docs:

- `docs/SCHEMA.md`
- `docs/PROFILE_THEORY.md`
- `docs/INTERPRETATION_BOUNDARIES.md`

### Authorship-Origin and AI Assistance

Decision: authorship origin is evidence-based metadata classification, not reliable AI detection.
Unknown remains unknown and should reduce weight or trigger quarantine where risk is material.

Primary doc: `docs/EVIDENCE_AND_CONFIDENCE.md`

## Rejected Alternatives

- never storing raw text
- always storing raw text
- treating artifact storage as memory
- treating all profile differences as expression drift
- making core exports generation-ready prompts
- hidden inheritance for derived profiles
- using schema-level `identity` fields for stance or recurring lens claims
- treating AI detector output as ground truth

## Sprint 02 Constraints

Sprint 02 must define:

- artifact storage mode
- build manifest
- evidence reference model
- confidence component model
- claim levels
- authorship-origin taxonomy
- context profile model
- export projection metadata
- public-safe export validation

Mandatory gates before Sprint 02 implementation:

- claim validation must be enforced in schema/compiler design
- artifact storage default is `metadata_only`
- cross-model semantic extraction is `not_comparable` unless an explicit migration/equivalence
  method is designed
- divergence objects and collision labels must be serialized explicitly
- context profiles should recompile from filtered evidence in the MVP rather than use hidden merge
  inheritance

## Remaining Non-Blockers

- exact database encryption mechanism
- exact drift distance metrics
- final implementation of local storage
- private connector prioritization
- downstream prompt adapter design

These are implementation or later architecture details. They do not block schema design if Sprint
02 encodes the constraints above.

## Go Decision

Sprint 02 is a conditional go. It is safe to begin schema work only if the Sprint 02 schema
documents encode the gates above before Pydantic implementation begins.

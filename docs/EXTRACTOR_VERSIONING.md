# Extractor Versioning

Status: Sprint 01.5 remediation decision

## Decision

Every profile build must record a build manifest. Drift must distinguish expression drift from
compiler drift.

Imprint must not present profile changes as changes in the subject's expression unless the relevant
schema, extractor, prompt, model, source policy, and corpus window are comparable.

## Build Manifest

Every profile version should stamp:

- schema version
- profile compiler version
- classifier version
- extractor version
- extractor prompt version, when applicable
- model provider and model identifier, when applicable
- model settings relevant to reproducibility
- source policy version
- authorship policy version
- redaction/export mode
- corpus window
- artifact counts by inclusion status
- artifact store mode
- config hash
- run timestamp

The manifest is part of the profile contract, not a debug log.

## Drift Types

### Expression Drift

Expression drift means comparable evidence suggests the subject's expression changed.

Requirements:

- comparable schema version or documented migration
- comparable extractor family
- comparable source policy
- comparable corpus type mix
- stable enough evidence count

### Compiler Drift

Compiler drift means output changed because Imprint changed.

Examples:

- new extractor prompt
- different LLM model
- changed classifier logic
- changed signal taxonomy
- changed source weighting policy
- changed schema migration behavior

### Corpus Drift

Corpus drift means the underlying evidence changed.

Examples:

- new source added
- source removed
- time window changed
- new artifact type included
- higher quarantine rate

## Comparison Policy

Profile comparisons should be labeled:

- `comparable`
- `partially_comparable`
- `not_comparable`

Do not compute or display expression drift as a single clean claim when compiler or corpus drift is
dominant.

Operational comparability:

| Label | Required Conditions | Allowed Claim |
| --- | --- | --- |
| `comparable` | same schema compatibility family, same extractor family and major version, same source policy version, comparable corpus window and source mix | expression drift may be reported |
| `partially_comparable` | compatible schema but changed extractor minor version, model settings, source mix, or corpus window | report changed profile output with caveats; do not overstate expression drift |
| `not_comparable` | different extractor family, different LLM model family for model-derived semantic signals, incompatible schema, or materially different corpus | report compiler/corpus change only; expression drift is unsupported |

Cross-model recompilation is not comparable for model-derived semantic signals by default. A
profile can stay in the same subject lineage, but its semantic drift claims are unsupported unless
Sprint 02 defines an explicit migration or equivalence method.

## Determinism Policy

Imprint should be deterministic where practical, but semantic extraction is not guaranteed to be
fully deterministic.

Required controls:

- record all extractor and model versions
- prefer rule-based or statistical baselines where possible
- pin prompt versions for LLM-backed extraction
- expose model-backed signals as model-derived evidence
- avoid pretending a rebuild across models is the same experiment

## Rejected Alternatives

### One Profile Version Number Only

Rejected because schema, compiler, extractor, model, and export versions change independently.

### Treat All Profile Differences as User Drift

Rejected because it would make model upgrades look like personal expression change.

### Ban LLM Extraction

Rejected because some useful expression observations require semantic extraction. The correct
control is versioning, evidence labeling, and comparability rules.

## Sprint 02 Implications

Sprint 02 schemas must include:

- build manifest
- extractor run metadata
- profile comparability metadata
- drift type labels
- signal provenance indicating rule-based, model-derived, or human-reviewed origin
- clear `not_comparable` handling for cross-model semantic extraction

## Sprint 02.5 Model Invocation Metadata

Imprint is BYOM/BYOP. Build manifests must record profile-affecting model invocations without assuming a provider.

For each profile-affecting invocation, the manifest should record:

- model role
- provider kind and provider name
- base URL kind without secrets
- model name and model version, if known
- extractor family and version fields, when the invocation participates in extraction
- prompt version or policy version
- schema version
- decoding policy needed for reproducibility
- seed, if supported
- capability flags
- local versus remote execution
- retention and training policy, if known

Experience-only generation is outside the durable profile unless explicitly promoted through artifact classification, evidence support, confidence scoring, and claim validation.

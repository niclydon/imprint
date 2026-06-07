# Model Capability Contracts

Status: Sprint 02.5 model policy contract

## Principle

Model selection is role-based. A model is acceptable for a role only if its declared capabilities satisfy that role's contract.

Capability declarations are metadata, not runtime clients. They support configuration review, privacy disclosure, and drift analysis.

## Capability Flags

Canonical model invocation metadata may declare:

- `structured_output`
- `json_schema_output`
- `low_temperature_operation`
- `long_context`
- `stable_embedding_dimension`
- `deterministic_seed_support`
- `artifact_id_citation_support`
- `local_only_support`
- `no_retention_policy`
- `no_training_policy`
- `batch_inference`
- `streaming_output`

## Role Requirements

- `classifier_llm`: structured output, artifact ID citation support, low-temperature operation.
- `signal_extractor_llm`: structured output, JSON schema output where possible, artifact ID citation support, low-temperature operation.
- `claim_validator_llm`: structured output, taxonomy/rule rationale support, artifact ID citation support.
- `evidence_interpreter_llm`: artifact ID citation support, long context when operating over broad evidence windows.
- `confidence_assessor_llm`: structured output and component-score support.
- `drift_comparator_llm`: structured output and manifest-aware reasoning.
- `embedding_model`: stable embedding dimension and versioned model name.
- `reranker_model`: stable ranking contract and versioned model name.
- `profile_summarizer_llm`, `first_run_artifact_llm`, `report_writer_llm`: no durable mutation authority by default.

## Decoding Policy

Profile-affecting inference should use a declared decoding policy. The schema may record temperature, seed, and determinism policy for reproducibility. These are build-manifest fields only; they are not core export prompt controls.

## Failure Mode

If a required capability is absent or unknown, the runtime should either reject the configuration for that role or downgrade output to a non-durable, review-required status. Sprint 02.5 defines the contract only; runtime enforcement belongs in later implementation.

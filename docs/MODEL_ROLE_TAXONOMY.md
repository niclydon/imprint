# Model Role Taxonomy

Status: Sprint 02.5 model policy contract

Model roles describe why inference is used. The same provider or model may serve multiple roles, but each role must be recorded separately when it affects the durable profile.

## Profile-Affecting Roles

### `classifier_llm`

Classifies artifacts, source type, inclusion status, authorship-origin evidence, or quarantine risk.

### `signal_extractor_llm`

Extracts expression signals from evidence. Changes to this role can change profile semantics and comparability.

### `claim_validator_llm`

Assists validation of observation, bounded interpretation, quarantined, and prohibited claims. Validator output is a validation input, not a bypass around policy.

### `evidence_interpreter_llm`

Interprets support relationships between artifacts, signals, claims, and confidence components.

### `confidence_assessor_llm`

Assists confidence scoring. Scores must remain decomposed into named components.

### `drift_comparator_llm`

Assists drift or comparability analysis. Expression drift still requires structured manifest comparability.

### `embedding_model`

Embeds artifacts or signal text for clustering, deduplication, retrieval, or similarity support. Stable embedding dimensions and version metadata are required.

### `reranker_model`

Ranks candidate evidence, artifacts, or support references before extraction or review.

## Experience-Only Roles

### `profile_summarizer_llm`

Writes explanatory prose from a canonical profile. It does not define profile claims.

### `first_run_artifact_llm`

Creates onboarding or delight artifacts. Generated output is not evidence unless explicitly re-ingested and validated.

### `report_writer_llm`

Produces report prose or formatting from canonical profile fields. It must not add unsupported claims.

## Promotion Rule

Experience-only output can affect durable profiles only through explicit promotion into the evidence pipeline: artifact creation, classification, authorship-origin labeling, evidence support, confidence scoring, and claim validation.

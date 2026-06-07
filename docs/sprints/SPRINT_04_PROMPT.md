# Sprint 04 Prompt - Classification Engine

Use this prompt with GPT 5.5 from the repository root.

---

You are implementing Sprint 04 for Imprint.

Sprint 04 builds the classification layer. This is the first layer that starts assigning meaning to artifacts, so it must be conservative, explainable, and privacy-safe.

## Required Reading

Read before making changes:

- `docs/sprints/SPRINT_04.md`
- `docs/SPRINT_03_5_REMEDIATION_SUMMARY.md`
- `docs/SPRINT_03_5_ARCHITECTURE_REVIEW.md`
- `docs/ARTIFACT_STORAGE_POLICY.md`
- `docs/PRIVACY_AND_LOCAL_MODE.md`
- `docs/EVIDENCE_AND_CONFIDENCE.md`
- `docs/INTERPRETATION_BOUNDARIES.md`
- `docs/SCHEMA.md`
- `docs/SCHEMA_RISKS.md`
- `docs/MODEL_PROVIDER_POLICY.md`
- `src/imprint/adapters/`
- `src/imprint/schemas/`
- `tests/test_adapters.py`
- `tests/test_schemas.py`

## Mission

Implement deterministic, local-first classification logic for normalized artifacts.

The classifier should produce explainable classification outputs for:

- authorship origin
- authorship confidence
- artifact type
- inclusion/exclusion/quarantine status
- quote/forward/template/notification likelihood
- contamination risk
- evidence summary

## Core Rule

Adapter output is ingestion evidence, not ground truth.

Classification must re-assess:

- adapter-provided authorship hints
- adapter-provided confidence hints
- adapter-provided inclusion/exclusion hints
- adapter-provided artifact-type hints
- JSONL record-level metadata

Adapters may provide useful source hints. They do not decide durable classification.

## Required Implementation Scope

Allowed:

- classifier interfaces
- deterministic/rule-based baseline classifier
- classification result models if existing schemas require extension
- evidence objects for classification decisions
- local-only classification over normalized artifacts
- quarantine/exclusion reasoning
- tests using synthetic fixtures
- minimal CLI integration if clean and scoped

Forbidden:

- signal extraction
- profile compilation
- remote APIs
- LLM calls
- provider-specific code
- prompt generation
- Gmail/iMessage/Plaud/Looki/SQL/private connectors
- psychological or diagnostic interpretation
- raw corpus persistence beyond existing artifact storage policy

## Classification Requirements

### 1. Authorship Origin

Classification must distinguish at least:

- `human_origin`
- `human_directed_ai_assisted`
- `assistant_output`
- `quoted_or_forwarded`
- `template_or_notification`
- `mixed_authorship`
- `unknown_speaker`
- `missing_metadata`
- `parser_uncertain`
- `suspected_ai_assisted`

If the existing schema uses different enum names, follow the schema but preserve these concepts.

AI detector output, if any, is weak evidence only. Do not implement AI detection in Sprint 04.

### 2. Inclusion State

Classification must support:

- included
- excluded
- quarantined

Quarantine when uncertain.

Examples that should quarantine or exclude:

- quoted reply chains
- forwarded content
- assistant-generated output
- template notifications
- unclear speaker
- missing or contradictory metadata
- parser uncertainty

### 3. Artifact Type

Classification must re-assess adapter artifact type hints.

Adapter-obvious hints such as `transcript_segment` may be accepted when supported by source shape, but still need evidence.

### 4. Evidence and Explainability

Every classification result must include support metadata explaining why the decision was made.

At minimum, include:

- input artifact ID
- source type
- source hint values considered
- rule IDs or reason codes applied
- confidence level or score
- final classification
- limitations or uncertainty notes

### 5. Privacy

Do not expose or reconstruct local filesystem paths from opaque `source_id` values.

Do not include raw artifact text in public-safe classification output.

Metadata-only remains the default.

### 6. Validation Boundaries

Classification is not claim validation and is not signal extraction.

Do not produce durable profile claims like:

- “the subject is analytical”
- “the subject is introverted”
- “the subject is anxious”
- “the subject prefers written communication”

Sprint 04 classifies artifacts. It does not interpret the subject.

## Test Requirements

Add tests proving:

- adapter hints do not automatically become final classification truth
- JSONL-supplied authorship/classification metadata is treated as advisory
- unclear authorship reduces confidence or triggers quarantine
- assistant output is excluded or quarantined according to policy
- quoted/forwarded/template-like artifacts are excluded or quarantined
- opaque source IDs remain opaque in classification outputs
- no local filesystem paths leak
- classification results include reason/evidence metadata
- no LLM/provider calls are required

## Documentation Requirements

Create or update:

- `docs/CLASSIFICATION_DESIGN.md`
- `docs/CLASSIFICATION_RULES.md`
- `docs/CLASSIFICATION_RISKS.md` only if doing self-review, otherwise leave adversarial review to Gemini

Update as needed:

- `docs/sprints/SPRINT_04.md`
- `docs/EVIDENCE_AND_CONFIDENCE.md`
- `docs/PRIVACY_AND_LOCAL_MODE.md`

## Exit Criteria

Sprint 04 is complete only if:

- classification logic exists
- classification is deterministic and local-first
- adapter hints are advisory only
- classification outputs are explainable
- uncertain artifacts quarantine rather than silently include
- no provider assumptions are introduced
- no raw filesystem paths leak
- all tests pass

At the end, summarize:

- files changed
- tests run
- classification behaviors implemented
- explicit non-goals preserved
- remaining blockers for Sprint 05

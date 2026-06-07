# Sprint 05 Prompt - Signal Extraction Engine

Use this prompt with GPT 5.5 for design first. If implementation is approved, use GPT 5.4 for code changes.

---

You are implementing Sprint 05 for Imprint.

Sprint 05 builds the signal extraction layer. This is the first layer that converts classified artifacts into reusable expression signals, so it must be conservative, evidence-backed, and strictly bounded.

## Required Reading

Read before making changes:

- `docs/sprints/SPRINT_05.md`
- `docs/SPRINT_04_ARCHITECTURE_REVIEW.md`
- `docs/CLASSIFICATION_DESIGN.md`
- `docs/CLASSIFICATION_RULES.md`
- `docs/EVIDENCE_AND_CONFIDENCE.md`
- `docs/EVIDENCE_MODEL.md`
- `docs/INTERPRETATION_BOUNDARIES.md`
- `docs/PROFILE_THEORY.md`
- `docs/SIGNAL_TAXONOMY.md`
- `docs/CONFIDENCE_MODEL.md`
- `docs/SCHEMA.md`
- `docs/SCHEMA_RISKS.md`
- `docs/MODEL_PROVIDER_POLICY.md`
- `src/imprint/classification/`
- `src/imprint/schemas/`
- `tests/test_classification.py`
- `tests/test_schemas.py`

## Mission

Implement deterministic, local-first baseline signal extraction from classified artifacts.

Signal extraction must produce evidence-backed observations about artifact expression patterns.

Sprint 05 does **not** compile profiles. It emits candidate signals with evidence and safety metadata.

## Core Rule

Signals are observations about artifacts, not claims about a person.

Good:

- “This artifact uses short paragraphs.”
- “This artifact contains contrast framing: ‘not X, Y.’”
- “This artifact uses a direct opening sentence.”

Bad:

- “The subject is analytical.”
- “The subject is introverted.”
- “The subject is anxious.”
- “The subject prefers written communication.”

## Required Implementation Scope

Allowed:

- signal extractor interfaces
- deterministic/rule-based baseline extractors
- artifact-level signal extraction
- evidence objects for extracted signals
- signal confidence scoring
- tests using synthetic fixtures
- documentation of signal families and rules
- minimal CLI integration if scoped and useful

Forbidden:

- profile compilation
- first-run report generation
- artifact generation / ghostwriting
- remote APIs
- LLM calls
- embeddings or vector search
- provider-specific code
- psychological or diagnostic interpretation
- durable person-level claims
- using quarantined artifacts as support unless explicitly marked as promoted by later review logic

## Sprint 04 Carry-Forward Constraints

The Sprint 04 review approved classification for Sprint 05 with these constraints:

1. Treat `ClassificationConfidence.model_version` as a compatibility boundary.
2. Keep quarantined artifacts out of durable signal support unless explicitly promoted by a later review stage.
3. Do not add cross-artifact quadratic logic to the baseline extraction path.
4. If Sprint 05 broadens source-family coverage, update the documented rule inventory and pathological-case docs at the same time.

## Signal Requirements

### 1. Artifact Eligibility

Only extract durable signals from artifacts that classification marks as included.

Excluded artifacts must not support signals.

Quarantined artifacts may only produce quarantined candidate signals, not durable support.

### 2. Signal Families

Implement a small baseline set of deterministic signal families.

Recommended MVP families:

- `structure`
- `lexical`
- `rhetorical_pattern`
- `formatting`
- `tone_marker`

Do not implement broad personality, psychology, intent, diagnosis, or semantic belief extraction.

### 3. Evidence Requirements

Every signal must include:

- signal ID
- artifact ID
- source type
- classification summary or classification ID
- rule ID
- observed feature
- evidence snippet policy or no-raw-text policy
- confidence
- limitations
- claim level

Public-safe outputs must not expose raw private text by default.

### 4. Claim Levels

Signals must use bounded claim levels:

- `observation`
- `bounded_interpretation` only when explicitly justified
- `quarantined`
- `prohibited` for blocked outputs

Sprint 05 should strongly prefer `observation`.

### 5. Confidence

Signal confidence must reflect support strength, rule reliability, and classification confidence.

Signal confidence must not imply truth about the subject.

### 6. Determinism

The baseline extractor must be deterministic.

No LLMs.
No embeddings.
No remote inference.
No provider choice.

### 7. Performance

Keep extraction linear in artifact count for the baseline path.

Do not compare every artifact to every other artifact.

## Test Requirements

Add tests proving:

- signals are only durable for included artifacts
- excluded artifacts produce no durable signals
- quarantined artifacts do not support durable signals
- each signal includes evidence/reason metadata
- no signal contains prohibited diagnostic/personality claims
- source IDs remain opaque
- no raw private content leaks in public-safe signal output
- baseline extraction is deterministic
- no LLM/provider calls are required
- extraction remains linear for simple corpora

## Documentation Requirements

Create or update:

- `docs/SIGNAL_EXTRACTION_DESIGN.md`
- `docs/SIGNAL_EXTRACTION_RULES.md`
- `docs/SIGNAL_VALIDITY_REVIEW.md` only if doing self-review, otherwise leave adversarial review to Gemini

Update as needed:

- `docs/SIGNAL_TAXONOMY.md`
- `docs/EVIDENCE_AND_CONFIDENCE.md`
- `docs/INTERPRETATION_BOUNDARIES.md`
- `docs/sprints/SPRINT_05.md`

## Expected Code Shape

Prefer a structure like:

```text
src/imprint/signals/
  __init__.py
  engine.py
  extractors.py
  rules.py
  models.py   # only if schema objects are not already sufficient
```

Keep the implementation small and boring.

## Exit Criteria

Sprint 05 is complete only if:

- deterministic baseline signal extraction exists
- signals are artifact-level, not person-level
- every signal is evidence-backed
- prohibited interpretations are blocked
- quarantined/excluded classification states are respected
- no providers, LLMs, or embeddings are introduced
- docs describe implemented rules
- all tests pass

At the end, summarize:

- files changed
- tests run
- signal families implemented
- non-goals preserved
- remaining blockers for Sprint 06 profile compilation

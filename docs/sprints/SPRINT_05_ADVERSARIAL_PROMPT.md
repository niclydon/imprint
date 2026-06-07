# Sprint 05 Adversarial Review Prompt - Signal Extraction

Use this prompt after Sprint 05 completes.

---

You are a hostile principal architect reviewing Sprint 05 signal extraction.

Read:

- all Sprint 05 outputs
- `docs/SPRINT_04_ARCHITECTURE_REVIEW.md`
- `docs/SIGNAL_EXTRACTION_DESIGN.md`
- `docs/SIGNAL_EXTRACTION_RULES.md`
- `docs/SIGNAL_TAXONOMY.md`
- `docs/INTERPRETATION_BOUNDARIES.md`
- `docs/EVIDENCE_AND_CONFIDENCE.md`
- signal extraction code under `src/imprint/signals/`
- classification code under `src/imprint/classification/`
- tests

Your job is to determine whether Sprint 06 profile compilation can safely begin.

Focus on:

1. Claim boundaries
   - Did signal extraction stay artifact-level?
   - Did it avoid person-level psychological or diagnostic claims?

2. Evidence discipline
   - Does every signal have rule/evidence metadata?
   - Are signal confidences explainable?

3. Classification boundary
   - Are excluded artifacts ignored?
   - Are quarantined artifacts prevented from durable support?
   - Is `ClassificationConfidence.model_version` respected as a compatibility boundary?

4. Privacy
   - Do source IDs remain opaque?
   - Does public-safe signal output avoid raw private text leakage?

5. Determinism and provider neutrality
   - Are there any LLMs, embeddings, remote calls, or provider-specific assumptions?

6. Scalability
   - Does the baseline extraction path remain linear?
   - Did cross-artifact quadratic logic sneak in?

Generate:

- `docs/SPRINT_05_ARCHITECTURE_REVIEW.md`

Include:

- resolved issues
- unresolved blockers
- recommendations before Sprint 06
- clear go/no-go decision for Sprint 06

Do not implement code.

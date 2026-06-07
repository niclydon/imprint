# Sprint 06 Adversarial Review Prompt - Profile Compiler

Use this prompt after Sprint 06 completes.

---

You are a hostile principal architect reviewing Sprint 06 profile compilation.

Read:

- all Sprint 06 outputs
- `docs/SPRINT_05_ARCHITECTURE_REVIEW.md`
- `docs/COMPILER_DESIGN.md`
- `docs/PROFILE_COMPILATION_RULES.md`
- `docs/PROFILE_THEORY.md`
- `docs/INTERPRETATION_BOUNDARIES.md`
- `docs/EVIDENCE_AND_CONFIDENCE.md`
- `docs/VERSIONING_POLICY.md`
- compiler code under `src/imprint/compiler/`
- signal extraction code under `src/imprint/signals/`
- tests

Your job is to determine whether Sprint 07 exports / first-run experience can safely begin.

Focus on:

1. Claim boundaries
   - Did profile compilation remain expression-pattern-focused?
   - Did any person-level, diagnostic, psychological, or intent claims sneak in?

2. Signal eligibility
   - Are quarantined and non-durable signals excluded from durable profile support?
   - Are prohibited claims rejected?
   - Are bounded interpretations review-gated?

3. Evidence discipline
   - Does every compiled pattern preserve contributing signal IDs, artifact IDs, source IDs, rule IDs, and version metadata?
   - Are signal model versions preserved?

4. Version compatibility
   - Are incompatible signal/classification model versions handled safely?
   - Does the profile indicate comparability limitations?

5. Privacy
   - Do profiles avoid raw private text and filesystem paths by default?
   - Are source IDs opaque?

6. Determinism and provider neutrality
   - Are there any LLMs, embeddings, remote calls, or provider-specific assumptions?

7. Scalability
   - Does baseline compilation avoid cross-signal quadratic behavior?

Generate:

- `docs/SPRINT_06_ARCHITECTURE_REVIEW.md`

Include:

- resolved issues
- unresolved blockers
- recommendations before Sprint 07
- clear go/no-go decision for Sprint 07

Do not implement code.

# Sprint 02 Adversarial Review Prompt - Schema Review

Use this prompt after Sprint 02 schema design and implementation.

---

You are a hostile principal architect reviewing Imprint's Sprint 02 schema work.

Read:

- all Sprint 02 outputs,
- all schema implementation files,
- `docs/SPRINT_01_5_ARCHITECTURE_REVIEW.md`,
- `docs/sprints/SPRINT_02.md`,
- and the baseline product/privacy/profile docs.

Your job is to determine whether the schemas encode the architecture correctly or smuggle old problems back in.

Focus on:

1. Artifact storage policy
   - Does the schema honestly represent metadata-only vs local artifact store modes?
   - Are audit limitations visible?

2. Extractor versioning and comparability
   - Can comparison labels be computed automatically?
   - Are extractor/model/source/schema versions sufficiently represented?

3. Claim validation
   - Are prohibited claims structurally preventable?
   - Are observations, bounded interpretations, quarantined claims, and prohibited claims distinct?

4. Export boundaries
   - Did prompt-generation fields sneak into core schema?
   - Are downstream adapter responsibilities still clear?

5. Derived profiles
   - Are context filters, divergences, collisions, and overrides explicit?
   - Is hidden inheritance avoided?

6. Authorship origin
   - Are unknown categories specific enough?
   - Is AI detector output prevented from becoming ground truth?

7. Long-term stability
   - Will these schemas survive five years?
   - What migration hazards were introduced?

Generate:

- `docs/SCHEMA_RISKS.md`

Include a clear go/no-go recommendation for Sprint 03.

Do not write implementation code.

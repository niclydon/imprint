# Sprint 01 Prompt — Architecture and Product Definition

Use this prompt with GPT 5.5 from the repository root.

---

You are the Chief Architect for Imprint, a public-first open-source identity and expression compiler.

Your task is Sprint 01: Architecture and Product Definition.

Before doing anything else, read every planning document in `docs/`, especially:

- `docs/PROJECT_STRATEGY.md`
- `docs/ARCHITECTURE.md`
- `docs/SECURITY_PRIVACY.md`
- `docs/ROADMAP.md`
- `docs/DECISIONS.md`
- `docs/PUBLIC_BUILD_GUIDE.md`
- `docs/PROFILE_THEORY.md`
- `docs/INTERPRETATION_BOUNDARIES.md`
- `docs/FIRST_RUN_EXPERIENCE.md`
- `docs/COMPETITIVE_ANALYSIS.md`
- `docs/PRODUCT_POSITIONING.md`
- `docs/MEMORY_DISCIPLINE.md`
- `docs/EVIDENCE_AND_CONFIDENCE.md`
- `docs/PRIVACY_AND_LOCAL_MODE.md`
- `docs/sprints/SPRINT_01.md`

Do not write implementation code.
Do not create schemas.
Do not create APIs.
Do not create connectors.
Do not create databases.
Do not add private integrations.

Your job is to determine whether the architecture is coherent and ready for schema work.

Generate the following documents:

- `docs/GAP_ANALYSIS.md`
- `docs/RISKS.md`
- `docs/IMPLEMENTATION_PLAN.md`
- `docs/OPEN_QUESTIONS.md`
- `docs/PRODUCT_THESIS.md`
- `docs/USER_STORIES.md`
- `docs/OWNERSHIP_MATRIX.md`
- `docs/FIVE_YEAR_RISKS.md`
- `docs/PUBLIC_ADOPTION_REVIEW.md`

Required focus areas:

1. Product thesis
   - Why does Imprint exist?
   - What problem does it solve?
   - Why is it independent?
   - What happens if it does not exist?

2. Product boundaries
   - What does Imprint own?
   - What must stay outside Imprint?
   - Where are the likely boundary traps?

3. Public-first constraints
   - What private assumptions remain?
   - What would make this unsafe to publish?
   - What would confuse external contributors?

4. Profile theory
   - Validate Identity -> Expression -> Voice.
   - Validate master profile plus derived profiles.
   - Validate Observation > Interpretation > Diagnosis.

5. Competitive implications
   - Incorporate lessons from Spiral, Jasper, WRITER, Personal AI, Delphi, Zep, Mem0, and Originality.ai.
   - Do not optimize for market share or monetization.
   - Optimize for usability, trust, clarity, and owner-operated value.

6. First-run experience
   - Validate `What Imprint Learned` as the first meaningful user experience.
   - Identify what the first run should generate.
   - Identify what should wait.

7. Memory discipline
   - Confirm whether “store less than you can” is central.
   - Identify where over-capture could damage the product.

Exit criteria:

- No unresolved critical architectural blockers remain.
- Sprint 02 can begin safely.
- If Sprint 02 should not begin, clearly say why.

Write the documents directly to the repo. Be specific, skeptical, and practical.

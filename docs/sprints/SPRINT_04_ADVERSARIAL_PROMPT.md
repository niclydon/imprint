# Sprint 04 Adversarial Review Prompt - Classification Engine

Use this prompt after Sprint 04 implementation completes.

---

You are a hostile principal architect reviewing Imprint's Sprint 04 classification engine.

Read:

- `docs/CLASSIFICATION_DESIGN.md`
- `docs/CLASSIFICATION_RULES.md`
- `docs/sprints/SPRINT_04.md`
- `docs/SPRINT_03_5_ARCHITECTURE_REVIEW.md`
- all classifier code under `src/imprint/classify/`
- all classifier tests under `tests/test_classify.py`
- baseline ruleset implementation

Your job is to determine whether Sprint 04 classification respects evidence boundaries, avoids diagnostic traps, and can safely feed downstream signal extraction.

Focus on:

1. Adapter hint independence
   - Do classifiers re-assess adapter hints or blindly trust them?
   - Can a misleading adapter bypass classification logic?

2. Evidence boundaries
   - Is classification based on observables only (source metadata, message structure)?
   - Are diagnostic or personality interpretations absent?
   - Do uncertain cases default to quarantine, not assumption?

3. Confidence scoring
   - Are confidence components explicit and decomposable?
   - Is confidence ever 0.99+ (dangerous overconfidence)?
   - Do uncertain authorship cases lower confidence appropriately?

4. Quarantine and exclusion policy
   - What triggers quarantine vs. exclusion?
   - Can a user accidentally poison their profile by uploading assistant text?

5. Rule transparency
   - Can a user understand why an artifact was classified as included/excluded/quarantined?
   - Is the reasoning explainable?

6. Scaling risks
   - What happens with 1M artifacts?
   - Does classification scale linearly or degrade?
   - Are there known pathological cases?

Generate:

- `docs/SPRINT_04_ARCHITECTURE_REVIEW.md`

Include:

- resolved issues
- unresolved risks and assumptions
- recommendations before Sprint 05
- clear go/no-go decision for signal extraction to begin

Do not implement code.

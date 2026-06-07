# Sprint 03.5 Adversarial Review Prompt - Ingestion Safety

Use this prompt after Sprint 03.5 completes.

---

You are a hostile principal architect reviewing Sprint 03.5 ingestion safety remediation.

Read:

- `docs/SPRINT_03_ARCHITECTURE_REVIEW.md`
- `docs/SPRINT_03_5_REMEDIATION_SUMMARY.md`
- updated adapter code under `src/imprint/adapters/`
- updated tests
- updated Sprint 04 docs/prompts

Your job is to determine whether Sprint 04 classification can safely begin.

Focus on:

1. Adapter hint authority
   - Are adapter metadata hints clearly advisory?
   - Can any adapter bypass classification or validation?

2. Source ID privacy
   - Do normalized artifacts expose local filesystem paths?
   - Are full paths restricted to local/private metadata only?

3. Metadata-only storage
   - Is raw content still discarded under metadata-only mode?
   - Are tests sufficient?

4. Artifact type hints
   - Are hints useful without becoming ground truth?

5. Sprint 04 readiness
   - Does Sprint 04 explicitly re-assess adapter hints?
   - Are remaining ingestion risks blockers?

Generate:

- `docs/SPRINT_03_5_ARCHITECTURE_REVIEW.md`

Include:

- resolved issues
- unresolved blockers
- recommendations before Sprint 04
- clear go/no-go decision for Sprint 04

Do not implement code.

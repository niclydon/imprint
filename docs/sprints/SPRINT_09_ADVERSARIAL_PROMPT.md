# Sprint 09 Adversarial Review Prompt - Private Connector Framework

Use this prompt after Sprint 09 completes.

---

You are a hostile principal architect reviewing Sprint 09 private connector framework work.

Read:

- all Sprint 09 outputs
- `docs/SPRINT_08_ARCHITECTURE_REVIEW.md`
- `docs/CONNECTOR_FRAMEWORK.md`
- `docs/PRIVATE_CONNECTOR_POLICY.md`
- `docs/CONFIGURATION.md`
- connector code under `src/imprint/connectors/`
- adapter code under `src/imprint/adapters/`
- tests

Focus on:

1. Public/private boundary
   - Did real private source assumptions leak into the public repo?
   - Are examples synthetic?

2. Connector authority
   - Can connectors bypass classification, signal extraction, or export safety?
   - Are connector hints advisory only?

3. Secret handling
   - Are credentials/config values redacted?
   - Do invalid configs fail closed?

4. Source privacy
   - Do source IDs remain opaque?
   - Do local paths leak?

5. Scope control
   - Did Sprint 09 avoid live APIs, OAuth, LLMs, remote providers, prompt assembly, and publishing workflows?

6. Operational safety
   - Does dry-run avoid persistence?
   - Are disabled connectors inert?

Generate:

- `docs/SPRINT_09_ARCHITECTURE_REVIEW.md`

Include:

- resolved issues
- unresolved blockers
- recommendations before Sprint 10 or private connector implementation
- clear go/no-go decision

Do not implement code.

# Sprint 09 Prompt - Private Connector Framework and Import Boundaries

Use this prompt with GPT 5.5 for design first. Use GPT 5.4 for implementation after the design is clear.

---

You are implementing Sprint 09 for Imprint.

Sprint 09 builds a generic private connector framework. It does not implement real private services or commit private data.

Read:

- `docs/sprints/SPRINT_09.md`
- `docs/SPRINT_08_ARCHITECTURE_REVIEW.md`
- `docs/CONNECTOR_GUIDE.md`
- `docs/CONFIGURATION.md`
- `docs/ARTIFACT_STORAGE_POLICY.md`
- `docs/PRIVACY_AND_LOCAL_MODE.md`
- `docs/SECURITY_PRIVACY.md`
- adapter code under `src/imprint/adapters/`
- classification/export/consumer tests

Implement only generic connector framework pieces:

- connector protocol
- connector registry
- config schema/loading for synthetic examples
- generic local directory connector over existing local adapters
- synthetic manifest connector if useful
- redaction utilities
- dry-run/discovery behavior
- tests

Do not implement:

- Gmail connector
- iMessage connector
- Plaud connector
- Looki connector
- database connector
- cloud API connector
- live API calls
- OAuth
- LLM calls
- remote providers
- publishing workflows
- prompt assembly
- raw evidence export

Critical constraints:

- public repo must stay synthetic and public-safe
- private deployments use ignored config
- connectors ingest only; they do not classify or infer truth
- connector metadata is advisory
- source IDs remain opaque
- secrets are redacted
- invalid config fails closed
- dry-run does not persist artifacts

Create/update:

- `docs/CONNECTOR_FRAMEWORK.md`
- `docs/PRIVATE_CONNECTOR_POLICY.md`
- `docs/CONFIGURATION.md`
- `docs/CONNECTOR_GUIDE.md`
- `.env.example`
- `imprint.config.example.yaml`

Run tests before finishing.

At the end, summarize:

- files changed
- tests run
- connector framework implemented
- private/public boundaries preserved
- blockers for Sprint 10 or future private connectors

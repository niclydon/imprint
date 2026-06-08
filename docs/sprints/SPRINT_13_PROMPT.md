# Sprint 13 Prompt - Private Adapter Strategy and Threat Models

Use this prompt with GPT 5.5 for design. Use GPT 5.4 only for doc implementation after the plan is clear.

You are implementing Sprint 13 for Imprint.

Do not build real private adapters. Create the threat models and implementation standards required before private adapters can be safely implemented.

Read:

- `docs/sprints/SPRINT_13.md`
- `docs/SPRINT_09_ARCHITECTURE_REVIEW.md`
- `docs/CONNECTOR_FRAMEWORK.md`
- `docs/PRIVATE_CONNECTOR_POLICY.md`
- `docs/CONFIGURATION.md`
- connector code and tests

Create the required threat model and policy docs.

Critical constraints:

- no real credentials
- no real source paths
- no private corpora
- no live APIs
- no OAuth
- no adapter implementation
- synthetic examples only
- connectors ingest only and never classify or infer truth

Run tests before finishing.

Summarize files changed, tests run, and remaining blockers before real private adapter work.

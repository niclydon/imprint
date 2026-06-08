# Sprint 14 Prompt - Service and Automation Planning

Use this prompt with GPT 5.5 for design. Use GPT 5.4 only after the service boundaries are clear.

You are implementing Sprint 14 for Imprint.

Design local/private service mode and automation around public-safe exports. Do not build a SaaS platform and do not expose raw corpora.

Read:

- `docs/sprints/SPRINT_14.md`
- `docs/EXPORT_FORMATS.md`
- `docs/CONSUMER_CONTRACTS.md`
- `docs/SECURITY_PRIVACY.md`
- export, consumer, connector, and CLI code

Create the service/API design docs listed in Sprint 14. Implement code only if the design is clear and scope remains small.

Critical constraints:

- no raw corpus exposure
- no private path exposure
- no credential exposure
- no prompt assembly
- no publishing workflows
- no LLM/provider calls
- no Mosvera/Broadside runtime adapters inside core
- batch and service outputs must be equivalent

Run tests before finishing.

Summarize files changed, tests run, service boundaries, and blockers before implementation or release.

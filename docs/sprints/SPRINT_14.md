# Sprint 14 - Service and Automation Planning

Primary Model: GPT 5.5 for design, GPT 5.4 for implementation planning
Adversarial Reviewer: GPT 5.5 or Gemini Antigravity
Status: Future phase after Sprint 13 private adapter strategy

## Mission

Define a local/private service and automation model for Imprint without turning the project into a SaaS platform or weakening raw-corpus boundaries.

Sprint 14 is primarily a design sprint. It may add small validation scaffolding, but it should not rush into service implementation before the API, auth, scheduling, and batch/service parity rules are clear.

## Required Reading

- `docs/ROADMAP.md`
- `docs/SPRINT_11_ARCHITECTURE_REVIEW.md`
- `docs/SPRINT_09_ARCHITECTURE_REVIEW.md`
- `docs/EXPORT_FORMATS.md`
- `docs/CONSUMER_CONTRACTS.md`
- `docs/SECURITY_PRIVACY.md`
- `docs/EXPORT_BOUNDARIES.md`
- `src/imprint/exports/`
- `src/imprint/consumers/`
- `src/imprint/connectors/`
- `src/imprint/cli.py`

## Core Rule

Service mode may expose public-safe contracts. It must not expose raw corpora, credentials, private connector state, local filesystem paths, or unvalidated profile outputs.

## Required Deliverables

Create:

- `docs/SERVICE_MODE_DESIGN.md`
- `docs/API_CONTRACT.md`
- `docs/SERVICE_AUTH_POLICY.md`
- `docs/SERVICE_AUTOMATION_PLAN.md`
- `docs/SERVICE_METRICS_AND_AUDIT.md`
- `docs/BATCH_SERVICE_PARITY.md`

Update:

- `docs/SECURITY_PRIVACY.md`
- `docs/EXPORT_BOUNDARIES.md`
- `docs/CONSUMER_CONTRACTS.md`
- `docs/ROADMAP.md`

## Allowed Scope

- local/private HTTP service design
- health endpoint design
- version/status endpoint design
- public-safe latest-profile endpoint design
- public-safe export delivery design
- file-drop export delivery design
- scheduled connector dry-run/rebuild design
- metrics and audit event design
- authentication and authorization policy
- batch/service parity requirements

## Forbidden Scope

- multi-tenant SaaS
- hosted public service
- raw corpus browsing
- credential management UI
- publishing workflow automation
- prompt assembly
- LLM/provider runtime calls
- Mosvera or Broadside runtime adapters inside core
- service access to private paths outside configured local runtime

## API Boundary

Potential endpoints should be public-safe by default:

- `GET /health`
- `GET /version`
- `GET /profiles/latest`
- `GET /exports/latest.json`
- `GET /exports/latest.md`
- `POST /jobs/rebuild` only if authenticated and explicitly scoped

No endpoint may return raw artifacts, private paths, credentials, or unredacted connector config.

## Automation Requirements

Scheduled jobs must:

- run locally/private only
- record build manifests
- preserve batch/service parity
- log audit events without raw text
- fail closed on connector/config errors
- emit compatibility warnings

## Exit Criteria

Sprint 14 is complete when:

- service/API design is documented
- auth policy is documented
- automation plan is documented
- public-safe endpoint boundaries are explicit
- batch/service parity rules exist
- service mode does not weaken privacy or export safety
- all tests pass

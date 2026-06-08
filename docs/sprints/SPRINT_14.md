# Sprint 14 - Service and Automation Planning

Primary Model: GPT 5.5 for design, GPT 5.4 for scoped implementation
Adversarial Reviewer: GPT 5.5 or Gemini Antigravity
Status: Future phase after Sprint 13.5 private adapter enforcement foundation

## Mission

Design and, only if still small and safe, scaffold a local/private service mode for Imprint.

Sprint 14 must not turn Imprint into a SaaS, dashboard, raw-corpus browser, model router, publishing engine, or background data lake. It should make the existing CLI/export pipeline operable as a private local service for trusted downstream consumers.

## Product Goal

A private operator should eventually be able to run Imprint locally and expose only public-safe profile contracts to local tools, automations, or downstream systems.

The service should answer:

- Is Imprint healthy?
- What version/configuration is running?
- What is the latest public-safe profile?
- What exports are available?
- When was the last rebuild?
- Did the latest run fail, warn, or produce compatibility limitations?

It must not answer:

- What raw artifacts were read?
- What private paths are configured?
- What credentials exist?
- What private source data was excluded?
- What prompt should a model run?

## Required Reading

- `docs/ROADMAP.md`
- `docs/SPRINT_11_ARCHITECTURE_REVIEW.md`
- `docs/SPRINT_12_5_ARCHITECTURE_REVIEW.md` if present
- `docs/SPRINT_13_5_ARCHITECTURE_REVIEW.md` if present
- `docs/EXPORT_FORMATS.md`
- `docs/CONSUMER_CONTRACTS.md`
- `docs/EXPORT_BOUNDARIES.md`
- `docs/SECURITY_PRIVACY.md`
- `docs/PRIVATE_CONNECTOR_POLICY.md`
- `docs/CONNECTOR_AUDIT_LOG.md` if present
- `docs/CONNECTOR_REPLAY_MANIFEST.md` if present
- `src/imprint/cli.py`
- `src/imprint/exports/`
- `src/imprint/consumers/`
- `src/imprint/connectors/`
- `tests/`

## Core Rule

Service mode may expose public-safe contracts. It must not expose raw corpora, credentials, private connector state, local filesystem paths, unvalidated profile outputs, prompt assembly, model/provider configuration, or downstream runtime behavior.

## Implementation Posture

Sprint 14 is design-first. Code is allowed only after the service boundary is documented.

Preferred sequence:

1. Write service design docs.
2. Define API contracts.
3. Define auth policy.
4. Define audit/metrics model.
5. Define batch/service parity requirements.
6. Add tests for contract assumptions.
7. Add minimal local service scaffold only if all boundaries remain clear.

## Required Design Deliverables

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

## Allowed Implementation Scope

Allowed only after docs exist:

- local-only service scaffold
- health endpoint
- version/status endpoint
- latest public-safe profile/export endpoint
- static file/export delivery from an explicit configured export directory
- dry-run-only job endpoint if authenticated and clearly scoped
- tests proving endpoints do not expose private data

## Forbidden Scope

Do not implement:

- multi-tenant SaaS
- hosted public service
- raw corpus browsing
- credential management UI
- private connector configuration UI
- publishing workflow automation
- prompt assembly
- LLM/provider runtime calls
- Mosvera runtime adapters inside core
- Broadside runtime adapters inside core
- service access to paths outside configured local runtime
- background ingestion without explicit operator configuration

## API Contract Requirements

Potential endpoints must be public-safe by default:

- `GET /health`
- `GET /version`
- `GET /status`
- `GET /profiles/latest`
- `GET /exports/latest.json`
- `GET /exports/latest.md`
- `GET /warnings/latest`
- `POST /jobs/dry-run` only if authenticated
- `POST /jobs/rebuild` only if authenticated and explicitly enabled

No endpoint may return:

- raw artifacts
- raw source content
- private local paths
- credentials
- unredacted connector config
- private connector state
- prompts
- model/provider settings
- platform publishing settings

## Authentication Policy Requirements

Document at least three modes and select one default:

1. disabled service mode / CLI only
2. localhost-only unauthenticated read-only mode
3. bearer-token protected private mode
4. reverse-proxy protected mode, such as Cloudflare Access or Tailscale-only access

Baseline recommendation:

- default: service disabled
- if enabled: bind localhost only
- write/job endpoints require explicit auth
- no credential values logged

## Automation Requirements

Scheduled jobs must:

- be opt-in
- run locally/private only
- record build manifests
- preserve batch/service parity
- log audit events without raw text
- fail closed on connector/config errors
- emit compatibility warnings
- never silently publish or call downstream consumers

## Metrics and Audit Requirements

Metrics may include:

- last successful build timestamp
- last failed build timestamp
- artifact counts
- included/excluded/quarantined counts
- export generation status
- warning count
- validation status

Metrics and audit logs must not include:

- raw artifact text
- private paths
- credentials
- source snippets
- personal account identifiers

## Batch/Service Parity Requirements

For the same config, source inputs, and code versions, service-generated outputs must match CLI-generated outputs or explain why they differ.

Tests should compare:

- build manifest
- canonical JSON export
- validation report
- compatibility warnings

A service output must never be treated as a different profile class than CLI output.

## Test Requirements

If code is implemented, add tests proving:

- health/version endpoints work
- latest export endpoint returns public-safe output only
- private fields are not exposed
- raw text/path/credential strings are rejected or absent
- unauthenticated write/job endpoints fail
- service and batch outputs are equivalent
- service mode uses no LLM/provider calls

## Exit Criteria

Sprint 14 is complete only if:

- service/API design is documented
- auth policy is documented
- automation plan is documented
- metrics/audit model is documented
- public-safe endpoint boundaries are explicit
- batch/service parity rules exist
- any implemented service code is local/private, tested, and bounded
- all tests pass
- adversarial review gives GO or explicitly defers implementation until blockers are fixed

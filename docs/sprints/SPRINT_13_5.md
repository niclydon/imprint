# Sprint 13.5 - Private Adapter Enforcement Foundation

Primary Model: GPT 5.5 for design, GPT 5.4 for implementation
Adversarial Reviewer: GPT 5.5 or Gemini Antigravity
Status: Complete as private adapter enforcement foundation

## Mission

Turn Sprint 13 private-adapter strategy into enforceable contracts, tests, and runtime boundaries.

Sprint 13 established the threat-model framework. Sprint 13.5 closes the enforcement gaps identified by the adversarial review before Gmail, iMessage, Plaud, Looki, database, cloud, or transcript adapters are implemented.

## Required Reading

- `docs/SPRINT_13_ARCHITECTURE_REVIEW.md`
- `docs/sprints/SPRINT_13.md`
- `docs/PRIVATE_CONNECTOR_POLICY.md`
- `docs/CONNECTOR_FRAMEWORK.md`
- `docs/CONFIGURATION.md`
- `docs/SECURITY_PRIVACY.md`
- `docs/CREDENTIAL_STORAGE_POLICY.md` if present
- `docs/CONSENT_AND_MULTI_PERSON_POLICY.md` if present
- `src/imprint/connectors/`
- `src/imprint/adapters/`
- `src/imprint/classification/`
- `tests/test_connectors.py`

## Blocking Issues to Resolve

### 1. Consent enforcement contract

Define an enforceable consent boundary layer for private-source ingestion.

Required behavior:

- model consent classes such as owner-authored, third-party-authored, mixed, unknown, and system-generated
- map source-specific threat models to concrete consent rules
- ensure classifiers/compilers can consume consent boundary results or source policy outputs
- ensure third-party content cannot become durable profile support without explicit policy approval

Deliverables:

- consent boundary model or protocol
- source-policy mapping docs
- synthetic tests for received mail, group chat participants, and third-party transcript speakers

### 2. Stronger redaction patterns

Expand connector redaction to cover real-world credential formats before any credentialed connector exists.

Required detection/redaction coverage:

- OAuth refresh tokens
- JWT tokens
- database DSNs with embedded credentials
- API keys in URL query parameters
- AWS access keys
- Azure-style connection strings
- bearer/basic auth values

This should align with Sprint 12.5 quality-gate hardening where possible.

### 3. Replay and rebuild versioning

Define a replay manifest for connector-driven profile rebuilds.

Required metadata:

- connector name/type/version
- adapter version
- parser version
- source policy version
- storage mode
- config hash
- synthetic/private fixture indicator

Do not claim expression drift when connector, parser, source policy, or storage behavior changed.

### 4. Multi-person contamination fixture standard

Add or document fixture requirements for private-source adapters.

Must include synthetic examples for:

- received email vs sent mail
- quoted email replies
- group chat participant messages
- unknown sender messages
- third-party transcript speakers
- mixed-speaker transcripts

### 5. Connector audit log contract

Define a standardized, redacted connector audit log.

Audit records should include:

- connector run ID
- connector type/name
- source policy version
- counts discovered/included/excluded/quarantined
- warnings and redacted errors
- storage mode
- replay manifest reference

Audit logs must never include raw text, credentials, private local paths, or unredacted connector config.

### 6. Public/private repository leakage detection

Add a scanner or tests that reduce accidental private fixture leakage.

Required checks:

- fixture filenames should indicate synthetic/example/test status
- no real-looking emails, phone numbers, private URLs, tokens, DSNs, local home paths, or account IDs
- generated private outputs remain ignored

### 7. Adapter authority boundary tests

Add tests proving connectors do not import or call:

- classifiers
- signal extractors
- compilers
- exporters
- LLM/provider packages
- network/API clients unless explicitly allowed by a future source-specific implementation

## Documentation Requirements

Create or update:

- `docs/SPRINT_13_5_REMEDIATION_SUMMARY.md`
- `docs/CONSENT_BOUNDARY_MODEL.md`
- `docs/CONNECTOR_AUDIT_LOG.md`
- `docs/CONNECTOR_REPLAY_MANIFEST.md`
- `docs/CONNECTOR_SYNTHETIC_FIXTURE_STANDARD.md`
- `docs/PRIVATE_CONNECTOR_POLICY.md`
- `docs/CONNECTOR_IMPLEMENTATION_STANDARD.md`

## Non-Goals

Do not implement:

- real Gmail connector
- real iMessage connector
- real Plaud or Looki connector
- database/cloud connector
- OAuth flows
- live API calls
- service/API mode
- UI review flows
- raw corpus storage changes

## Exit Criteria

Sprint 13.5 is complete only if:

- consent enforcement is modeled and testable
- redaction patterns cover real-world credential formats
- replay manifest contract exists
- multi-person synthetic fixture standards exist
- connector audit log contract exists
- public/private leakage detection exists
- adapter authority boundary tests exist
- all tests pass
- adversarial review gives GO for private adapter implementation planning

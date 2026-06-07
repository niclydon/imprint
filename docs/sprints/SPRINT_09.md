# Sprint 09 - Private Connector Framework and Import Boundaries

Primary Model: GPT 5.5 for design, GPT 5.4 for implementation
Boilerplate Model: Codex Spark only for repetitive adapter scaffolding after contracts exist
Adversarial Reviewer: GPT 5.5 or Gemini Antigravity
Status: Ready after Sprint 08 consumer contract review

## Mission

Build the private connector framework that lets owner-operated Imprint deployments ingest real private sources through configuration while preserving the public-first repository boundary.

Sprint 09 is the first sprint that touches private-source architecture. It must remain generic, configurable, and public-safe.

This sprint should make private connectors possible without hard-coding Nic-specific systems, paths, credentials, services, or corpora.

## Required Reading

Read before making changes:

- `docs/SPRINT_08_ARCHITECTURE_REVIEW.md`
- `docs/CONSUMER_CONTRACTS.md`
- `docs/EXPORT_BOUNDARIES.md`
- `docs/ARTIFACT_STORAGE_POLICY.md`
- `docs/PRIVACY_AND_LOCAL_MODE.md`
- `docs/CONNECTOR_GUIDE.md`
- `docs/CONFIGURATION.md`
- `docs/SECURITY_PRIVACY.md`
- `docs/MODEL_PROVIDER_POLICY.md`
- `src/imprint/adapters/`
- `src/imprint/classification/`
- `src/imprint/exports/`
- `src/imprint/consumers/`
- `tests/test_adapters.py`
- `tests/test_classification.py`
- `tests/test_exports.py`
- `tests/test_consumers.py`

## Sprint 08 Carry-Forward Constraints

Sprint 09 must preserve these findings:

1. Consumer payloads remain projections of canonical JSON.
2. Prompt assembly stays outside core Imprint.
3. Publishing workflows stay outside core Imprint.
4. Runtime adapters for Mosvera and Broadside stay outside core Imprint.
5. No raw-text public export boundary remains intact.
6. Opaque source IDs remain opaque.
7. Compatibility warnings remain visible in consumer-facing projections.
8. Consumer contracts must not become private connector integrations.

## Core Boundary

Connectors ingest artifacts. They do not classify, extract signals, compile profiles, generate outputs, publish content, or call LLMs.

Connector responsibilities:

- discover source artifacts
- normalize into existing adapter/envelope flow
- preserve source metadata as advisory hints
- enforce configuration and privacy policies
- fail closed on missing credentials, invalid paths, or unsupported source shapes

Connector non-responsibilities:

- authorship truth
- inclusion truth
- signal extraction
- profile compilation
- prompt generation
- downstream publishing
- provider inference

## Required Connector Framework

Implement or define:

- connector interface/protocol
- connector registry
- configuration schema for connector declarations
- allowlisted local/file connector examples
- secret/config loading rules
- connector capability metadata
- source policy mapping
- dry-run/discovery mode
- validation and redaction utilities
- synthetic-only tests

## Private Adapter Policy

Public repo may contain generic connector framework and synthetic adapters only.

Do not commit:

- real Gmail/iMessage/Plaud/Looki connector credentials
- real source paths
- real source IDs
- real corpora
- private service hostnames
- personal account identifiers
- database DSNs
- OAuth tokens
- API keys

Private deployments may configure real connectors through ignored config.

## Initial Connector Types

Allowed in Sprint 09:

- generic local directory connector using existing local adapters
- generic file manifest connector using synthetic manifest fixtures
- optional generic command/output connector only if sandboxed and documented as dangerous/deferred

Deferred:

- Gmail API connector
- iMessage connector
- Plaud connector
- Looki connector
- database connector
- cloud storage connector
- live API connectors

These should be documented as future private deployment adapters, not implemented in public core during Sprint 09 unless fully generic and synthetic.

## Security Requirements

Connectors must:

- fail closed on invalid config
- distinguish required vs optional credentials
- redact secrets in errors/logs
- avoid printing raw artifact text
- avoid exporting local filesystem paths
- generate opaque source IDs
- respect artifact storage policy
- support dry-run/source discovery without ingestion where possible
- never send data to remote providers
- never invoke LLMs

## Configuration Requirements

Connector config should support:

- connector name
- connector type
- enabled/disabled flag
- source path or source descriptor
- adapter mapping
- storage mode
- source policy version
- optional tags/labels
- private/local-only metadata

Use `.env.example` and example config files only with fake/synthetic values.

## Test Requirements

Add tests proving:

- connector configs validate
- invalid configs fail closed
- disabled connectors do not run
- dry-run does not persist artifacts
- connector output flows through existing adapter normalization
- connector metadata remains advisory
- source IDs remain opaque
- local paths do not leak into public-facing artifacts
- secrets are redacted in errors
- no remote/provider/LLM calls are introduced
- synthetic fixtures only

## Documentation Requirements

Create or update:

- `docs/CONNECTOR_FRAMEWORK.md`
- `docs/PRIVATE_CONNECTOR_POLICY.md`
- `docs/CONFIGURATION.md`
- `docs/CONNECTOR_GUIDE.md`
- `.env.example`
- `imprint.config.example.yaml`

## Expected Code Shape

Prefer a small framework such as:

```text
src/imprint/connectors/
  __init__.py
  config.py
  protocol.py
  registry.py
  local_directory.py
  manifest.py
  redaction.py
```

Do not replace the adapter layer. Connectors should feed adapters or reuse adapter normalization.

## Exit Criteria

Sprint 09 is complete only if:

- connector framework exists
- connector config is documented and tested
- public repo contains only synthetic/generic connector examples
- private connector boundaries are explicit
- secrets and private paths are not committed
- connector outputs preserve adapter/classification/export boundaries
- tests pass

At the end, summarize:

- files changed
- tests run
- connector framework behavior
- security/privacy boundaries preserved
- remaining blockers for Sprint 10 public web presence or future private connector implementations

# Private Connector Policy

Status: Sprint 13 strategy baseline

## Public Repository Policy

The public Imprint repository may contain:

- generic connector framework code
- generic local-file connector types
- synthetic manifests
- synthetic examples
- fake env var names
- public-safe documentation
- tests using synthetic fixtures only

The public repository must not contain:

- real Gmail, iMessage, Plaud, Looki, database, or cloud connector credentials
- OAuth tokens, API keys, refresh tokens, cookies, bearer tokens, or DSNs
- real source paths
- real source IDs
- real private corpora
- private service hostnames
- personal account identifiers
- private table names or private query files

## Private Deployment Policy

Private deployments may configure real connectors through ignored local files:

- `.env`
- `imprint.config.yaml`
- `*.local.yaml`
- `*.local.json`
- files under `private/`, `data/`, `exports/`, or other ignored local paths

Private connector implementations should live outside public core unless they are generic,
synthetic-testable, and do not encode private source assumptions.

No real private connector may be implemented until its source family has:

- a source-specific threat model
- credential storage and revocation rules
- consent and multi-person data handling
- synthetic fixtures and redaction tests
- replay/rebuild and audit policy
- public/private repository boundary review

## Connector Authority

Connectors may:

- discover source records
- read configured local files
- normalize source records through existing adapters
- preserve source metadata as advisory hints
- report discovery counts
- fail closed on unsafe config

Connectors must not:

- decide final authorship truth
- decide final inclusion truth
- extract profile signals
- compile profiles
- export public profiles
- assemble prompts
- call LLMs
- call live APIs in public core
- publish content
- expose raw corpus search to downstream consumers

## Secret Handling

Secrets must be referenced through env vars. Config examples may show fake env var names, but must
not include real secret values.

Errors and CLI output must redact:

- secret-like keys
- token-like values
- credential-like values
- DSNs with embedded credentials
- local filesystem paths

Required credentials fail closed when missing. Optional credentials may be absent, but the connector
must either remain disabled or degrade explicitly according to the private deployment's policy.

Detailed credential rules live in `docs/CREDENTIAL_STORAGE_POLICY.md`. Source-specific threat models
may add stricter requirements, but they may not weaken this policy.

## Source Privacy

Adapters may briefly read raw local text to normalize artifacts. Public-safe normalized artifacts and
exports must not expose source paths or raw text.

Source IDs in exported or normalized public-safe surfaces must be opaque `source-*` identifiers.
Original private locators must remain outside canonical/public artifacts.

Multi-person data must follow `docs/CONSENT_AND_MULTI_PERSON_POLICY.md`. Connector possession or
operator access does not make other people's words eligible profile evidence.

## Deferred Connectors

Deferred until a future private implementation sprint:

- Gmail API connector
- iMessage connector
- Plaud connector
- Looki connector
- database connector
- cloud storage connector
- live API connectors
- command/output connector

These require the Sprint 13 threat models and standards before inclusion. Transcript-oriented
connectors, including Plaud-like and Looki-like sources, must satisfy
`docs/TRANSCRIPT_CONNECTOR_THREAT_MODEL.md` unless a future source-specific review defines a stricter
model.

## Public-Core Admission Rule

Private connector code may enter public core only if it is generic, synthetic-testable, credential-free
by default, and safe to run in CI without private infrastructure. Otherwise it belongs in a private
deployment package that depends on public Imprint interfaces.

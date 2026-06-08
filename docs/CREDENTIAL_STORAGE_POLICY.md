# Credential Storage Policy

Status: Sprint 13 strategy gate

## Purpose

This policy defines how Imprint private connectors may reference, load, store, redact, rotate, and
revoke credentials. It is a prerequisite for future Gmail, chat, transcript, database, cloud, or live
API connectors.

Sprint 13 does not add credential storage implementation. It defines the required contract before any
private connector is allowed to use credentials.

## Core Rules

- Credentials must never be committed.
- Credentials must never appear inline in YAML, JSON, TOML, Markdown examples, test fixtures, logs,
  CLI output, public-safe exports, or architecture reviews.
- Public examples may name fake env vars only.
- Runtime config must reference credential sources, not credential values.
- Missing required credentials fail closed before discovery or ingestion.
- Optional credentials must degrade explicitly and safely.
- Credential-derived provider/account identifiers are private metadata unless explicitly documented as
  public-safe synthetic examples.

## Approved Credential References

Public and local config may reference credentials by env var name:

```yaml
credentials:
  source_access:
    env: IMPRINT_EXAMPLE_SOURCE_ACCESS
    required: false
```

The env var name is not secret. The env var value is secret and must be loaded only at runtime.

Future private deployments may add a local credential provider, but it must satisfy the same redaction,
revocation, and audit rules. Any credential provider integration must be local/private by default and
must not become a public-core dependency.

## Prohibited Storage Locations

Credentials must not be stored in:

- `.env.example`
- `imprint.config.example.yaml`
- committed docs or fixtures
- generated exports
- canonical profiles
- consumer contracts
- build manifests
- logs intended for public issues or CI artifacts
- local artifact stores unless explicitly encrypted and documented in a future private deployment plan

Ignored local files such as `.env` or `imprint.config.yaml` may reference or contain operator secrets,
but they remain protected local state and must never be copied into public artifacts.

## Runtime Loading

A connector may read a credential only when all are true:

1. The connector is enabled.
2. The credential is declared by name in local config.
3. The credential source is approved for that connector type.
4. The connector has passed source-specific threat-model requirements.
5. The connector is about to perform an operation that requires the credential.

Dry-run commands should validate presence and scope shape where possible without printing or storing
secret values.

## Redaction Requirements

All errors, dry-run summaries, audit summaries, and validation reports must redact:

- secret-like keys
- token-like values
- OAuth codes and refresh material
- DSNs and embedded passwords
- private hostnames and tenant/account IDs when source-specific policy treats them as private
- local paths and provider locators that could identify a private source

Redaction must happen before exceptions cross connector boundaries. Tests must prove both direct
errors and nested context objects are redacted.

## Rotation and Revocation

Every credentialed connector must define:

- how credentials are rotated
- how credentials are revoked
- how stale cached replay state is identified
- how audit logs record credential use without secret values
- what happens when a credential loses required scope

Revocation must stop new reads. Existing local artifact stores remain protected data and require a
separate retention decision.

## Scope Minimization

Credentialed connectors must request only the minimum authority needed for the configured source
class. Scope must be documented in the source-specific threat model and visible in local audit output
without printing credential values.

Examples:

- sent-mail ingestion must not request broad mailbox mutation authority
- database ingestion must use read-only least-privilege access
- transcript API ingestion must not request audio download authority unless audio retention is
  explicitly part of a future approved local-only mode

## Audit Requirements

Credentialed connectors must record local audit metadata:

- credential reference name
- credential env var name
- required/optional status
- scope class requested
- last successful use timestamp bucket
- revocation status
- connector version

Audit metadata must not include credential values, refresh material, raw provider account IDs, or
private tenant identifiers.

## Public Repository Boundary

Public docs and tests may use fictional env var names and synthetic credential-missing cases. They
must not include real provider setup, live OAuth flows, cloud IAM instructions tied to an account, or
credential-shaped placeholder values that trigger secret scanners.

# Privacy and Local Mode

Status: Sprint 01.5 remediation decision

## Local-First Default

Imprint should run in local mode without credentials, cloud providers, private connectors, or
network calls.

Default local mode should use:

- synthetic examples for public demos
- ignored local storage for user data
- strict redaction
- public-safe exports
- raw examples disabled

## Export Modes

### Public-Safe

No raw private text. No personal identifiers. Safe for examples and demos.

### Private-Local

May include richer metadata and redacted excerpts. Not for commit.

### Full-Local

May include raw excerpts only when explicitly enabled. Not for commit or CI.

## Local Data Rules

- local artifact stores are protected data
- local databases and exports must be ignored
- public fixtures must be synthetic
- public-safe mode must fail closed on raw examples
- cloud providers are optional, never required for default local behavior
- exported source identifiers must be opaque and must not reveal local filesystem paths
- adapter metadata hints are not ground truth and must be re-classified before profile compilation

## Sprint 02.5 Model Provider Boundaries

Imprint remains local-first and BYOM/BYOP. Remote model providers are optional and must be visible when used.

Profile-affecting remote inference must disclose the model role, provider kind, provider name, model name, local versus remote execution, and known retention/training policy. Canonical schemas must not store API keys, bearer tokens, private base URLs, tenant IDs, or homelab-specific hostnames.

Experience-only generation may improve onboarding or reporting, but it must not mutate durable profiles unless the generated output is explicitly promoted through the normal evidence and validation pipeline.

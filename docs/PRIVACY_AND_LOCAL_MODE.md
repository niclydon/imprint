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

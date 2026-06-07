# Model Privacy Boundaries

Status: Sprint 02.5 model policy contract

## Principle

Remote inference is a privacy boundary crossing. It must be explicit to users and recorded for profile-affecting inference.

## Required Disclosure

When a model invocation can send artifact text or derived evidence outside the local process, users should be able to see:

- what artifact text or metadata may be sent
- provider kind and provider name
- model role
- model name and version, if known
- whether execution is local or remote
- base URL kind without secrets
- whether provider retention or training terms are known
- whether a local alternative exists

## Local Execution

Local execution includes local rules, local model processes, and local HTTP endpoints controlled by the user. Local endpoints still must not leak private hostnames, secrets, or account identifiers into canonical profiles.

## Remote Execution

Remote execution includes hosted model APIs, remote OpenAI-compatible endpoints, hosted provider APIs, or any non-local inference service. Remote use is optional and never required for public demos or default local mode.

## Data Minimization

Profile-affecting model calls should send the minimum artifact text required for the role. Public-safe exports must not include raw text. Metadata-only artifact storage remains the default even when a remote provider is used during compilation.

## Experience-Only Output

Experience-only generation may use remote providers only when disclosed. Its output must not become durable profile evidence unless explicitly promoted and validated.

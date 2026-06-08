# Sprint 14 Architecture Review: Service and Automation

Review date: 2026-06-08
Reviewer role: hostile service/security architect with focused subagent fan-out
Status: GO after Sprint 14.5 hardening

## Executive Summary

Sprint 14 correctly keeps service mode local/private, disabled by default in configuration, and
focused on public-safe export delivery instead of raw-corpus browsing, connector execution, prompt
assembly, provider calls, or downstream publishing automation.

The design docs are aligned with the previous export, consumer, connector, and privacy boundaries.
The initial scaffold is intentionally small and tests batch/service parity for canonical JSON.

The initial adversarial review found two blocking issues and two hardening recommendations:

- disabled service mode can still expose exports if an app is constructed with the default disabled
  config
- Markdown delivery validates strings for path/credential shapes but does not prove the file is the
  generated Imprint Markdown export
- FastAPI error handling should return bounded service errors instead of framework/default exception
  behavior
- reverse-proxy deployment policy is documented but the config model currently rejects all
  non-localhost binds without an explicit protected-mode flag

Sprint 14.5 resolved those findings with disabled-mode guards, generated Markdown shape validation,
bounded FastAPI service errors, and an explicit protected-bind config flag.

**Gate decision: GO for Sprint 15 planning after full-suite verification, merge, push, and deploy.**

## Review Method

Focused adversarial passes were run against:

1. service justification and SaaS creep
2. raw-corpus, path, and credential exposure
3. auth and disabled-mode bypasses
4. scheduling and job authority creep
5. batch/service parity
6. downstream runtime, prompt, and provider coupling
7. install/quickstart masking risk

Reviewed artifacts:

- `docs/SERVICE_DECISION_RECORD.md`
- `docs/SERVICE_MODE_DESIGN.md`
- `docs/API_CONTRACT.md`
- `docs/SERVICE_AUTH_POLICY.md`
- `docs/SERVICE_AUTOMATION_PLAN.md`
- `docs/SERVICE_METRICS_AND_AUDIT.md`
- `docs/BATCH_SERVICE_PARITY.md`
- `docs/SECURITY_PRIVACY.md`
- `docs/EXPORT_BOUNDARIES.md`
- `docs/CONSUMER_CONTRACTS.md`
- `docs/ROADMAP.md`
- `src/imprint/service.py`
- `tests/test_service.py`
- full focused and repository test output

## Findings

### B1: Disabled service mode is not enforced by the app/data endpoints

Severity: blocker
Status: fixed in Sprint 14.5

`ServiceConfig.enabled` defaults to `False`, and `/health` reports disabled, but the service data
helpers and `create_app()` still allow latest export delivery if a caller constructs the app with a
disabled config. That weakens the central Sprint 14 claim that service mode is disabled by default.

Required fix:

- fail closed for all data/job endpoints when `enabled=False`
- either make `create_app()` reject disabled config or make every non-health endpoint enforce enabled
  state
- add tests proving disabled config cannot return latest profile, export, warnings, or dry-run data

Resolution:

- data/job helpers now fail closed when `enabled=False`
- health may report disabled without exposing exports
- regression tests cover disabled latest profile, JSON, Markdown, warnings, status, version, and
  dry-run calls

### B2: Markdown delivery does not prove generated-export shape

Severity: blocker
Status: fixed in Sprint 14.5

`latest_markdown_export()` checks path/credential safety over the Markdown string, but a raw corpus
document without path-like or credential-like strings could pass. Because Markdown is not schema
validated like canonical JSON, the service needs a stronger generated-export shape check before
serving it.

Required fix:

- require the generated profile Markdown heading/sections expected from `markdown_profile_export()`
- reject obvious raw/private field markers such as raw content keys
- add tests where `profile.md` is replaced by plausible raw prose and service delivery fails

Resolution:

- Markdown delivery now requires generated Imprint profile headings and sections
- raw/private field markers are rejected
- regression tests cover substituted prose and explicit raw-text markers

### H1: Service errors should be bounded in FastAPI responses

Severity: hardening
Status: fixed in Sprint 14.5

The pure helpers raise bounded service exceptions, but `create_app()` does not install explicit
exception handlers. Framework defaults may be safe in production, but the service contract should own
its error shape and avoid stack/detail leakage.

Recommended fix:

- add handlers for `ServiceError` and `QualityGateError`
- return short public-safe error codes/messages
- add at least one route-level test when FastAPI is installed or keep the helper-level error tests if
  optional dependencies are unavailable

Resolution:

- `create_app()` installs handlers for service and quality-gate errors
- error payloads are public-safe and bounded
- route-level FastAPI test runs when optional dependencies are installed

### H2: Protected reverse-proxy mode lacks a config representation

Severity: hardening
Status: fixed in Sprint 14.5

Docs allow reverse-proxy protected private mode, but `ServiceConfig` rejects non-localhost bind hosts
unconditionally. That is safer than overexposure, but it creates drift between policy and config.

Recommended fix:

- add an explicit `external_protection=True` flag before allowing non-localhost binds, or adjust docs
  to say the current scaffold only supports localhost binds
- keep localhost as the default
- keep job endpoints authenticated in every mode

Resolution:

- `ServiceConfig.external_protection` explicitly gates non-localhost binds
- non-localhost binds require an auth token
- tests cover rejected unprotected bind and accepted protected bind

## Passed Areas

### Service justification

The decision record adequately justifies a small service facade for trusted local consumers without
making service mode a required v0.1.0 release dependency.

### Raw-corpus and credential boundaries

Canonical JSON delivery reuses the existing validation gate and public-safe payload validator. Tests
cover raw text, path, and credential absence for generated exports.

### Job authority

Sprint 14 implements only authenticated dry-run status. It does not add rebuild, connector execution,
scheduling mutation, provider calls, or publishing.

### Batch/service parity

The service returns the existing CLI-generated canonical JSON file and includes a parity helper/test
for exact canonical JSON and build-manifest equality.

### Downstream runtime coupling

No Mosvera, Broadside, provider, model, prompt, or publishing runtime adapter was added to core.

### Install/quickstart masking

The documented prerequisite gates were run before implementation:

- `python3 -m compileall -q src`
- `python3 -m pytest -q`
- `python3 -m imprint.cli example --output-dir /tmp/imprint-sprint14-smoke`
- `python3 -m imprint.cli validate-export /tmp/imprint-sprint14-smoke/profile.imprint.json`
- `python3 -m imprint.cli diff /tmp/imprint-sprint14-smoke/profile.imprint.json /tmp/imprint-sprint14-smoke/profile.imprint.json`

## Gate Decision

**GO.**

Sprint 14 and Sprint 14.5 satisfy the service/API design and bounded implementation requirements.
Completion remains contingent on the release loop evidence: full tests, merge, push, and deployment
smoke verification.

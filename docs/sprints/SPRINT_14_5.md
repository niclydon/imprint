# Sprint 14.5 - Service Boundary Hardening Plan

Status: completed

## Mission

Resolve the Sprint 14 adversarial review findings before declaring service/API mode complete.

Sprint 14.5 does not expand service scope. It hardens the disabled-mode, Markdown-delivery, error,
and protected-bind boundaries identified in `docs/SPRINT_14_ARCHITECTURE_REVIEW.md`.

## Required Reading

- `docs/SPRINT_14_ARCHITECTURE_REVIEW.md`
- `docs/SERVICE_DECISION_RECORD.md`
- `docs/SERVICE_MODE_DESIGN.md`
- `docs/API_CONTRACT.md`
- `docs/SERVICE_AUTH_POLICY.md`
- `docs/BATCH_SERVICE_PARITY.md`
- `src/imprint/service.py`
- `tests/test_service.py`

## Implementation Plan

### U1: Enforce disabled-mode fail-closed semantics

Goal: service data/job helpers must not deliver exports or warnings when service mode is disabled.

Required changes:

- add a shared enabled-state guard
- allow `health_payload()` to report disabled
- require enabled state for version/status/latest profile/latest JSON/latest Markdown/latest warnings
  and dry-run jobs
- add tests proving disabled mode blocks latest profile, latest JSON, latest Markdown, warnings, and
  dry-run

Verification:

- disabled service config cannot expose public-safe exports
- enabled service config preserves existing read behavior

### U2: Validate generated Markdown export shape

Goal: `profile.md` delivery must prove the file is the generated Imprint Markdown export, not merely
path/credential-safe prose.

Required changes:

- add a Markdown export shape validator
- require the generated profile summary heading and expected privacy/compatibility sections
- reject raw/private content field markers
- add tests replacing `profile.md` with raw-looking prose that otherwise has no obvious path or
  credential

Verification:

- generated `profile.md` is still served
- substituted raw prose is rejected

### U3: Bound service error responses

Goal: optional FastAPI service responses must not leak stack traces, paths, auth details, or
implementation exception text beyond short service-owned reason codes.

Required changes:

- add FastAPI exception handlers for `ServiceError` and `QualityGateError`
- return public-safe error payloads
- keep helper-level exception messages bounded

Verification:

- compile and tests pass
- route-level tests are added if FastAPI is available; otherwise helper-level tests remain the base
  dependency gate

### U4: Align protected bind policy and config

Goal: docs and config must agree on reverse-proxy/private-network mode.

Required changes:

- add `external_protection` to `ServiceConfig`
- continue rejecting non-localhost binds unless `external_protection=True`
- require job auth token when external protection is enabled
- document the explicit flag in `docs/SERVICE_AUTH_POLICY.md`

Verification:

- localhost config remains default
- `0.0.0.0` without external protection fails
- `0.0.0.0` with external protection and job auth succeeds

## Exit Criteria

Sprint 14.5 is complete only if:

- ✅ B1 disabled-mode blocker is fixed and tested
- ✅ B2 Markdown-delivery blocker is fixed and tested
- ✅ H1 bounded service errors are implemented with optional FastAPI route coverage
- ✅ H2 protected bind policy/config drift is resolved
- ✅ focused service tests pass: `python3 -m pytest -q tests/test_service.py`
- ✅ full repository tests pass: `python3 -m pytest -q`
- ✅ Sprint 14 adversarial review is updated to GO

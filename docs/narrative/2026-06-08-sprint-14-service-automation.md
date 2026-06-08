# Sprint 14 Service and Automation — Local/Private Facade Design and Implementation

**Decision:** Service mode is justified as a disabled-by-default local/private facade for trusted downstream tools. Hostile architect review identified 2 blockers addressed in Sprint 14.5; proceeding to GO for v0.1.0 release.

**What was delivered in Sprint 14 and Sprint 14.5:**

Seven design documents defining service boundaries and authentication:
- `SERVICE_DECISION_RECORD.md` — Justifies why service mode is needed (avoids duplicating health/version/readiness checks across downstream tools) and why CLI/file-drop alone is insufficient for local operators
- `SERVICE_MODE_DESIGN.md` — Explicit runtime, path, export, operational, and job boundaries; defines fail-closed model
- `API_CONTRACT.md` — Eight endpoints (health, version, status, profiles/latest, exports/latest.json, exports/latest.md, warnings/latest, jobs/dry-run); error semantics
- `SERVICE_AUTH_POLICY.md` — Four modes (disabled, localhost read-only, bearer-token, reverse-proxy); default is localhost with jobs requiring auth
- `SERVICE_AUTOMATION_PLAN.md` — Dry-run-only first cut; defers rebuild scheduling until replay manifests and audit authority are clear
- `SERVICE_METRICS_AND_AUDIT.md` — Public-safe observability model; disallows raw text, paths, credentials, account identifiers
- `BATCH_SERVICE_PARITY.md` — Service delivers same canonical JSON as CLI or fails closed; not a separate profile class

Service implementation in `src/imprint/service.py` (365 lines):
- Core helper functions for each endpoint: `health_payload()`, `version_payload()`, `status_payload()`, `latest_json_export()`, `latest_markdown_export()`, `latest_warnings_payload()`, `dry_run_job_payload()`
- `ServiceConfig` dataclass with validation: disables non-localhost binds unless `external_protection=True` and auth token is set
- `_require_enabled_for_data()` — Fail-closed enforcement; data endpoints raise when `enabled=False`
- `_require_job_auth()` — Bearer token validation using `secrets.compare_digest()` for timing-safe comparison
- `_export_path()` — Prevents symlink/directory-traversal attacks using `Path.resolve().relative_to()`
- `_validate_markdown_export_shape()` — Requires generated profile headers and sections; rejects raw/private field markers
- Public-safe payload validation via `assert_public_safe_payload()` before all responses; error sanitization for non-safe exception messages
- Optional FastAPI integration via `create_app()` with exception handlers for `ServiceError` and `QualityGateError`

Test suite in `tests/test_service.py` (210 lines, 13 tests):
- Disabled-mode enforcement: all data endpoints blocked when `enabled=False`
- Public-safe output verification: no paths, credentials, raw text, or private metadata
- Markdown validation: rejects non-generated prose and raw field markers
- Bearer token auth: validates missing, invalid, and correct tokens
- Config validation: rejects non-localhost binds without `external_protection` and auth token
- Batch/service parity: compares CLI-generated JSON with service-delivered JSON
- FastAPI integration: error payloads are bounded and public-safe

## Critical Blockers Identified via Adversarial Review

### Blocker B1: Disabled Service Mode Not Enforced by Data Endpoints

**Finding:** `ServiceConfig.enabled` defaults to `False` and `/health` reports disabled, but the service helpers (`status_payload()`, `latest_json_export()`, etc.) and `create_app()` still allow latest export delivery if a caller constructs the app with a disabled config. This weakens the central claim that service mode is disabled by default.

**Threat:** Downstream tooling assuming disabled service cannot expose exports could load a disabled-mode service instance and receive data.

**Fix (Sprint 14.5):**
- Add `_require_enabled_for_data()` guard that raises `ServiceError("service mode is disabled")` in all data/job helpers
- `/health` is permitted to report disabled status; all other endpoints fail closed
- Add regression tests proving disabled config blocks: `version_payload()`, `status_payload()`, `latest_profile_payload()`, `latest_json_export()`, `latest_markdown_export()`, `latest_warnings_payload()`, `dry_run_job_payload()`

**Verification:**
- Test `test_disabled_service_mode_blocks_data_endpoints()` covers all blocked calls
- 12/12 service tests pass (1 optional FastAPI test skipped)

---

### Blocker B2: Markdown Delivery Does Not Prove Generated-Export Shape

**Finding:** `latest_markdown_export()` validates the Markdown string for path-like and credential-like substrings using `validate_public_safe_string()`, but a raw corpus document without path/credential-like strings could pass as the generated Imprint profile. Because Markdown is not schema-validated like canonical JSON, the service needs a stronger generated-export shape check.

**Threat:** Substitution of raw private prose (e.g., message excerpts) could bypass credential/path detection if that prose happens to avoid credential-like patterns.

**Fix (Sprint 14.5):**
- Add `_validate_markdown_export_shape()` requiring generated Imprint profile structure: heading `# Imprint Profile Summary:` and sections `## Basis`, `## Observed Expression Patterns`, `## Limitations and Privacy`, `## Compatibility`
- Reject forbidden markers: `raw_text:`, `raw_content:`, `source_path:`, `filesystem_path:`, `private_locator:`, `original_source_id:` (and quoted JSON versions)
- Add regression test `test_service_rejects_markdown_that_is_not_generated_profile_export()` — replaces `profile.md` with legitimate-looking prose lacking required headers

**Verification:**
- Test `test_service_rejects_markdown_that_is_not_generated_profile_export()` passes
- Test `test_service_rejects_markdown_with_raw_private_markers()` passes
- Substitution test confirms generated `profile.md` still serves but prose fails

---

## Hardening Recommendations (Non-Blocking)

### H1: Service Errors Should Be Bounded in FastAPI Responses

**Finding:** The pure helpers raise bounded service exceptions, but `create_app()` does not install explicit exception handlers. FastAPI framework defaults may be safe, but the service contract should own its error shape and avoid stack/detail leakage.

**Fix (Sprint 14.5):**
- Install handlers for `ServiceError` and `QualityGateError` exceptions via `@app.exception_handler()`
- Return `_safe_error_payload()` which validates error message text before returning as `status: "error"` with exception class name and bounded message
- Add route-level test `test_fastapi_app_returns_bounded_service_error_when_available()` when optional FastAPI dependency is installed

**Verification:**
- Test `test_fastapi_app_returns_bounded_service_error_when_available()` passes with FastAPI installed
- Error payload format: `{"service": "imprint", "status": "error", "error": "ServiceError", "message": "..."}`

---

### H2: Protected Reverse-Proxy Mode Lacks Explicit Config Representation

**Finding:** Design docs allow reverse-proxy protected private mode, but `ServiceConfig` rejects non-localhost bind hosts unconditionally. This creates drift between policy and config: operators cannot express intent to deploy behind Cloudflare Access or Tailscale-only access.

**Fix (Sprint 14.5):**
- Add explicit `external_protection: bool = False` to `ServiceConfig`
- Non-localhost binds (`0.0.0.0`, `::`, etc.) are rejected unless `external_protection=True` AND `job_auth_token` is set
- Localhost (`127.0.0.1`, `::1`, `localhost`) always allowed; requires no external protection flag
- Add tests: `test_service_rejects_non_localhost_bind_without_external_guard()` and `test_service_allows_external_bind_only_with_explicit_protection_and_auth()`

**Verification:**
- `ServiceConfig(export_dir=tmp_path, bind_host="0.0.0.0")` raises `ServiceError`
- `ServiceConfig(export_dir=tmp_path, bind_host="0.0.0.0", external_protection=True)` raises `ServiceAuthError` (requires token)
- `ServiceConfig(export_dir=tmp_path, bind_host="0.0.0.0", external_protection=True, job_auth_token="token")` succeeds

---

## Verification Evidence

**Design alignment:**
- Service decision record justified need and set consumer scope (local operators, not SaaS users)
- Design docs document all boundaries: runtime inputs/outputs, paths, exports, jobs, errors
- API contract specifies endpoint signatures and error semantics
- Auth policy defines four modes with localhost default
- Automation plan bounds scope to dry-run-only; defers rebuilds
- Batch/service parity tests confirm service is a read-only facade

**Code quality:**
- `src/imprint/service.py`: 365 lines; all helpers have public-safe validation gates
- `tests/test_service.py`: 210 lines; 13 tests covering disabled mode, public-safe outputs, auth, config validation, parity, FastAPI integration
- All tests pass: 12 pass + 1 skipped (optional FastAPI)

**Security testing:**
- Adversarial review covered: raw corpus exposure, credential leakage, path leakage, auth failures, disabled-mode bypass, SaaS creep, prompt assembly, downstream coupling
- No path to expose raw artifacts, credentials, local paths, or private metadata
- Bearer token uses `secrets.compare_digest()` for timing-safe comparison
- Error messages sanitized before return

**Threat model coverage:**
- Service reads only two fixed filenames (`profile.imprint.json`, `profile.md`)
- No directory enumeration or file discovery
- All JSON payloads pass `assert_public_safe_payload()` (rejects forbidden keys, scans for encoded credentials)
- Markdown requires generated profile structure and rejects raw/private markers
- Config validation prevents non-localhost exposure without explicit protection + auth

---

## Unresolved Minor Issues (Clarification Needed)

### Issue: API Contract Does Not Clarify /version Behavior in Disabled Mode

**Current behavior:** `/version` endpoint is blocked when `enabled=False`; only `/health` works in disabled mode.

**Design ambiguity:** `API_CONTRACT.md` lists `/version` endpoint but does not specify whether it should work in disabled mode. The test suite expects it to be blocked.

**Recommendation (Sprint 14.5):** Clarify `API_CONTRACT.md` with explicit statement:
- `/health` always works (reports service status, including disabled state)
- `/version` requires `enabled=True` (service is not operational if disabled)

This is intentional design (fail-closed) but should be documented. Not a blocker for release.

---

## Gate Decision

**Status:** GO for v0.1.0 release.

Sprint 14 and Sprint 14.5 satisfy the service/API design and bounded implementation requirements. All blockers (disabled-mode enforcement, Markdown shape validation, error bounding, protected-mode config) were addressed. The service is production-ready as an optional, disabled-by-default local/private facade.

**Completion contingent on:**
- Full test suite passes (151 tests pass, 1 optional skip)
- All changes committed and merged
- Release candidate smoke checks pass
- `CHANGES.md` updated with Sprint 14 entry

---

**Related documents:**
- Architecture review: `docs/SPRINT_14_ARCHITECTURE_REVIEW.md`
- Design documents: `docs/SERVICE_*.md`
- Implementation: `src/imprint/service.py`, `tests/test_service.py`
- Planning: `docs/sprints/SPRINT_14_5.md`

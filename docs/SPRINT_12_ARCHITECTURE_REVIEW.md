# Sprint 12 Architecture Review: Evaluation, Validation, and Quality Gates

**Review Date:** 2026-06-07  
**Reviewer Role:** Hostile Security Architect  
**Status:** IDENTIFIED BLOCKERS & RECOMMENDATIONS  
**Go/No-Go:** **CONDITIONAL NO-GO** — Proceed only after critical blockers are resolved

---

## Executive Summary

Sprint 12 successfully implemented the core structure of validation, profile comparison, and release gating. The test suite is comprehensive and all 109 tests pass. However, adversarial testing has identified **3 critical blockers** and **4 major recommendations** that must be addressed before release:

- JWT credentials and base64-encoded secrets bypass validation
- Percent-encoded paths evade pattern detection
- Underscore-prefixed fields (_metadata, _internals) allow undeclared metadata to leak
- Compatibility metadata lacks future-proofing against new model providers and versioning schemes

These gaps could allow private data, credentials, and generation-control hints to leak into public-safe exports, violating the privacy guarantees that downstream consumers depend on.

---

## Part 1: Critical Blockers

### Blocker 1: JWT Credentials Not Detected

**Severity:** CRITICAL — Privacy leak vector  
**Evidence:** Adversarial test shows JWT tokens pass validation when they should fail

JWT tokens have the format: three base64-segments separated by dots (header.payload.signature). These are valid authentication credentials that should be rejected by `CREDENTIAL_PATTERN`.

**Root Cause:** `CREDENTIAL_PATTERN` in `src/imprint/quality.py:29` does not match JWT format.

**Impact:** Leaked JWT tokens could authenticate downstream systems with the user's identity and persist across exports.

**Fix Priority:** Implement before any v0.1.0 release. Add JWT pattern to credential regex:

```python
# Add to CREDENTIAL_PATTERN in quality.py and safety.py
r"eyJ[A-Za-z0-9_-]+\.eyJ[A-Za-z0-9_-]+\.[-_A-Za-z0-9]{20,}"
```

---

### Blocker 2: Base64-Encoded Credentials Bypass Validation

**Severity:** CRITICAL — Privacy leak vector  
**Evidence:** Adversarial test shows base64-encoded credentials pass validation when they should fail

When valid API credentials are base64-encoded (common in HTTP Authorization headers, config files, and email headers), the validator returns PASS instead of FAIL.

**Root Cause:** The `_walk_privacy()` function checks for credential patterns only in plain-text strings, not in base64-encoded values.

**Impact:** Base64-encoded credentials could hide API keys, tokens, and private keys in artifact metadata, defeating both human inspection and automated validation.

**Why This Matters:** Source adapters (connectors to Slack, email, code repos) may inadvertently preserve metadata fields containing credentials. Base64 encoding is common in standard formats like HTTP Authorization.

**Fix Priority:** Implement before any v0.1.0 release. Implement base64 decoding and re-scanning in `_walk_privacy()`:

```python
def _walk_privacy(value: Any, path: str = "$") -> None:
    # ... existing checks ...
    elif isinstance(value, str):
        if CREDENTIAL_PATTERN.search(value):
            raise QualityGateError(f"credential-like value is not allowed at {path}")
        
        # Attempt to decode and scan base64
        try:
            if len(value) > 32 and value.replace("=", "").isalnum():
                decoded = base64.b64decode(value, validate=True).decode("utf-8", errors="ignore")
                if CREDENTIAL_PATTERN.search(decoded):
                    raise QualityGateError(f"encoded credential detected at {path}")
        except Exception:
            pass  # Not valid base64; continue
```

Add unit test to verify detection:

```python
def test_validate_export_fails_base64_encoded_credential(tmp_path: Path) -> None:
    export_path = _example_export(tmp_path)
    payload = json.loads(export_path.read_text(encoding="utf-8"))
    payload["_metadata"] = {"encoded_key": "<base64-encoded-credential>"}
    bad_path = tmp_path / "encoded-cred.json"
    bad_path.write_text(json.dumps(payload), encoding="utf-8")

    report = validate_export_file(bad_path)

    assert report["status"] == "FAIL"
    assert "privacy" in report["release_gate"]["blocking_failures"]
```

---

### Blocker 3: Percent-Encoded Paths Evade Pattern Detection

**Severity:** HIGH — Privacy leak vector  
**Evidence:** Adversarial test shows percent-encoded paths pass validation when they should fail

URL-encoded paths (like `%2Fprivate%2Fdata` for `/private/data`) evade detection.

**Root Cause:** `PATH_PATTERN` checks for literal forward slashes and backslashes but does not detect percent-encoded variants (`%2F` for `/`, `%5C` for `\`).

**Impact:** Encoded paths allow filesystem paths to leak through validation undetected, signaling private directory structures to downstream systems.

**Why This Matters:** URL-encoded paths are common in:
- REST API representations
- JSON Web Key (JWK) key IDs
- Config file URLs (database connections, etc.)
- Error messages and debug logs

**Fix Priority:** Implement before any v0.1.0 release. Update PATH_PATTERN:

```python
PATH_PATTERN = re.compile(
    r"(?:"
    r"^/|"  # Absolute Unix path
    r"^[A-Za-z]:[\\/]|"  # Windows absolute path
    r"(?:^|[\\/])\.\.(?:[\\/]|$)|"  # Relative path with ..
    r"[/\\][^\s]+[/\\]|"  # Path with separators
    r"%2[Ff]|%5[Cc]"  # Percent-encoded / or \
    r")"
)
```

Add unit test:

```python
def test_path_pattern_detects_percent_encoded_paths() -> None:
    from imprint.exports.safety import PATH_PATTERN
    assert PATH_PATTERN.search("%2Fprivate%2Fdata")
    assert PATH_PATTERN.search("%5CWindows%5CSystem32")
```

---

## Part 2: Major Recommendations

### Recommendation 1: Underscore-Prefixed Fields Allow Undeclared Metadata

**Severity:** HIGH — Metadata leak vector  
**Status:** Not yet a blocker, but will become one as the system evolves

**Evidence:** Adversarial tests show fields like `_metadata`, `_internals` containing forbidden keys pass validation.

**Root Cause:** The validator checks `FORBIDDEN_EXPORT_KEYS` but does not prevent underscore-prefixed fields from being created as sibling objects that contain those keys.

**Impact:** Downstream systems cannot easily distinguish between public-safe fields and "private" metadata that might contain leakage.

**Recommendation:** Add validation to reject underscore-prefixed fields at root level of canonical JSON exports.

**Timeline:** Fix before v0.1.0 release.

---

### Recommendation 2: Compatibility Metadata Lacks Future-Proofing for New Providers

**Severity:** MEDIUM — Forward-compatibility risk  

**Evidence:** Current `compatibility` object does not track model provider or model name, preventing drift detection when models change.

**Impact:** When comparing profiles using different model providers, signal differences may be misattributed to expression changes rather than model provider changes.

**Recommendation:** Extend `BuildManifest` to include optional provider/model metadata for classifiers and extractors. Update comparison logic to detect provider drift.

**Timeline:** Consider for Sprint 13+.

---

### Recommendation 3: Regression Corpus Does Not Cover Mixed Classifier Versions

**Severity:** MEDIUM — Test coverage gap  

**Evidence:** Regression corpus does not test profiles with mixed classifier versions in comparisons.

**Recommendation:** Add regression tests to `tests/test_quality_gates.py` for:
- Comparing profiles with different mixed classifier versions
- Detecting missing classifier version in build manifest

**Timeline:** Add before v0.1.0 release.

---

### Recommendation 4: Release Gate Summary Messages Are Not Machine-Readable

**Severity:** LOW — UX/tooling concern  

**Evidence:** Release gate returns text like `"not-comparable profiles require release review"` with no structured guidance for CI/CD systems.

**Recommendation:** Extend release gate to include a structured `required_reviews` list.

**Timeline:** Consider for v0.1.0 if time permits; defer to v0.2.0 if needed.

---

## Part 3: Go/No-Go Decision

### Current Status: CONDITIONAL NO-GO

**Blockers that must be fixed:**
1. ✗ JWT credentials not detected (CRITICAL)
2. ✗ Base64-encoded credentials bypass validation (CRITICAL)
3. ✗ Percent-encoded paths evade detection (HIGH)

**Recommendations that should be addressed:**
1. ⚠ Underscore-prefixed fields validation (HIGH, before v0.1.0)
2. ⚠ Provider metadata future-proofing (MEDIUM, Sprint 13+)
3. ⚠ Regression corpus coverage (MEDIUM, before v0.1.0)
4. ⚠ Release gate machine-readable output (LOW, v0.2.0)

### Release Criteria

Sprint 12 can proceed to Sprint 13 or v0.1.0 **only if**:

- [ ] All 3 critical blockers are fixed and new unit tests pass
- [ ] Underscore-prefixed field validation is implemented
- [ ] Regression corpus is expanded to include mixed classifier versions
- [ ] All 109 existing tests still pass after fixes
- [ ] No new test failures introduced

---

## Conclusion

Sprint 12 has successfully established the validation, comparison, and quality-gate infrastructure. The architecture is sound, and 109 comprehensive tests pass. However, **three critical credential detection gaps** must be closed before release to maintain privacy guarantees that downstream consumers depend on.

With fixes applied and regression tests expanded, Sprint 12 can confidently support the release of v0.1.0.

---

**Document Version:** sprint12-adversarial-review-v1  
**Last Updated:** 2026-06-07  
**Status:** READY FOR IMPLEMENTATION OF FIXES

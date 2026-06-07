# Classification Performance

Status: Sprint 04 baseline targets

## Targets

- classify 1,000,000 artifacts in under 1 hour on a single modern workstation
- keep steady-state classification memory under 2GB for in-process rule evaluation
- keep per-artifact explainability output under 1KB in canonical/public-safe surfaces
- preserve linear scaling with artifact count; no cross-artifact quadratic loops in baseline

## Scaling Assumptions

- Sprint 04 classification is artifact-local. It does not compare artifacts to each other.
- Rule evaluation is bounded by simple string scans over normalized content-derived hints and safe
  metadata, so runtime is expected to be `O(n)` in artifact count plus per-artifact content length.
- The baseline classifier stores only result objects and does not maintain a global corpus index.
- Cross-artifact deduplication, clustering, or thread reconstruction is deferred beyond Sprint 04.

## Verification Strategy

- maintain batch classification smoke coverage in tests to guard against hidden shared state
- keep rule lists finite and curated; do not add user-defined runtime rules in core
- if a future sprint introduces corpus-wide state, add dedicated benchmarking before enabling it by
  default

## Pathological Cases

- oversized artifacts (>10MB) are quarantined for review rather than deeply processed
- malformed or contradictory metadata lowers confidence and tends toward quarantine
- unsupported source families should preserve the artifact boundary and avoid fallback to remote or
  model-based classification

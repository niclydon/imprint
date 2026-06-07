# Imprint Changes Log

Chronological per-phase record of significant work. See `docs/narrative/` for detailed documentary accounts.

---

## 2026-06-07

### Phase: Sprint 07 Adversarial Review — Export Layer and First-Run Experience Readiness

**Verdict:** GO for Sprint 08

Conducted comprehensive adversarial review of Sprint 07 exports and first-run experience against 6 architectural focus areas:

1. **Export safety** — All formats validated; no raw text, paths, or private metadata leak. Shared safety layer rejects prohibited claims, quarantined support, non-durable evidence, mixed signal model versions, path-like source IDs, and generation-control fields.
2. **Claim boundaries** — Expression-pattern-only scope preserved. All exports use "observed pattern" language; first-run explicitly states what Imprint cannot say.
3. **Version compatibility** — Compiler, classifier, and signal model versions preserved in all machine-readable exports. Mixed classifier versions warn; mixed signal model versions reject.
4. **First-run experience** — Useful, clear, non-overstated. Sorted by confidence, warns about low-confidence patterns and metadata-only storage limits.
5. **Mosvera boundary** — Contract/fragment only. Expression summaries and anti-patterns; no provider prompts, aesthetic-intent compilation, or runtime behavior.
6. **Determinism and provider neutrality** — All exports deterministic (byte-for-byte reproducible). No LLMs, embeddings, remote calls, or provider assumptions.

**Evidence:**
- `docs/SPRINT_07_ARCHITECTURE_REVIEW.md` — Detailed findings (147 lines)
- `tests/test_exports.py` — 10 comprehensive tests, all passing
- Full test suite: 71/71 passing
- All 10 Sprint 06 carry-forward constraints remain enforced

**Handoff to Sprint 08:**
- Canonical JSON is the source of truth for downstream projections.
- Downstream prompt assembly and publishing workflow are Sprint 08 scope, not Imprint.
- No architectural blockers remain.

Full story: `docs/narrative/2026-06-07-sprint-07-adversarial-review-exports-ready.md`

---

## Earlier Phases

See `docs/narrative/2026-06-07-sprint-06-compiler-verification-and-gates.md` for Sprint 06 adversarial review and earlier narrative docs in `docs/narrative/` by date.

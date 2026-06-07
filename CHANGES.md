# Imprint Changelog

## Sprint 10: Forge OG image — 2026-06-07

**Decision:** Use a pure OpenAI `gpt-image-2` text-to-image OG card for social previews.

**What changed:**

- `web/og.png` — 1200×630 image via Forge `openai:gpt-image-2` (txt2img, no hero reference).
- `web/og-gen.json` — generation metadata.

## Sprint 10: ai-glass-futuristic overlay — 2026-06-07

**Decision:** Apply `ai-glass-futuristic` structural DNA (glassmorphism, atmosphere, cinematic depth, motion) to the Imprint landing page while keeping the existing Imprint palette frozen. Register the result as Mosvera aesthetic `imprint`.

**What changed:**

- `web/styles.css` and `web/index.html`: glass surfaces, cerulean/amber atmosphere mesh, grain, spotlit hero, lift/sheen hovers, staggered reveal.
- Mosvera registry: `~/.config/mosvera/registry/template.imprint-base.json` and `composition.imprint.json`.

## Sprint 10: Public Web Presence — 2026-06-07

**Decision:** Ship a single-page static landing site at `imprint.niclydon.dev` for project communication and social sharing — not an application UI.

**What changed:**

- Added `web/` static site: `index.html`, `styles.css`, brand assets (favicon, OG image, hero), social metadata, and `DEPLOYMENT.md`.
- Updated `README.md` with website link and refreshed pre-release status.

**Deploy:** Vercel project with root directory `web/`, Cloudflare CNAME `imprint` → `cname.vercel-dns.com`.

## Phase 0: Public-First Foundation Setup — 2026-06-07

**Decision:** Establish minimal but complete scaffolding for a public repository—developer guidance, build configuration, and editor consistency rules.

**What changed:**

- **CLAUDE.md** (26 → 170 lines): Added setup commands (`pip install -e ".[test]"`, `pytest`, `ruff check/format`), architecture overview with planned module structure, development workflow (schemas → CLI → logic → tests), and expanded design principles. Developers can now clone and contribute without consulting six separate docs.

- **.gitignore** (32 → 47 lines): Added exclusions for Claude Code workspace (`.claude/`, `.cursor/`, `.remember/`), Python build artifacts (`build/`, `dist/`, `*.egg-info/`), IDE caches (`.mypy_cache/`, `.coverage/`), editor backups (`.swp`, `*~`), logs, and OS metadata.

- **.editorconfig** (new, 28 lines): Enforces 100-char Python line length (matching Ruff config), 2-space indents for YAML/JSON, UTF-8 encoding, and final newlines. Recognized natively by VS Code, JetBrains, and Vim (with plugin).

- **.dockerignore** (new, 56 lines): Prepared for future containerization. Excludes `.git`, `__pycache__`, IDE files, OS metadata, dev scratch, and optional tests/docs. Ready to use as soon as service mode is implemented.

**What was deferred:**

- `MANIFEST.in` — Distribution packaging deferred until PyPI workflow is planned.

**What's unblocked:**

- Contributors can now run tests, lint, and format code from the command line without guessing tool names.
- Code structure is documented; someone adding signal extraction logic knows it goes in `src/imprint/extract/`, not elsewhere.
- Editor tooling is consistent across the team (no accidental line-length violations from different IDE defaults).
- Future Dockerization has a ready template.

**Full story:** `docs/narrative/2026-06-07-public-foundation-setup.md`

## Phase 1: Schema and Model Policy Contracts — 2026-06-07

**Decision:** Lock first-class schema contracts before runtime work by defining testable model and profile boundaries.

**What changed:**

- Added `src/imprint/schemas/models.py` with 654 lines of canonical `pydantic` models for artifacts, evidence, claims, signals, profiles, and provider-facing metadata.
- Exported all schema symbols through `src/imprint/schemas/__init__.py` and added `pythonpath` in `pyproject.toml` so tests and tools import schemas consistently.
- Added `tests/test_schemas.py` with synthetic coverage for Sprint 01.5 gates plus new profile-affecting model invocation contracts.
- Added and expanded contract docs: `docs/SCHEMA_PHILOSOPHY.md`, `docs/SCHEMA_THREAT_MODEL.md`, `docs/SIGNAL_TAXONOMY.md`, `docs/CONFIDENCE_MODEL.md`, `docs/EXTRACTOR_VERSIONING.md`, `docs/MIGRATION_STRATEGY.md`, `docs/MODEL_CAPABILITY_CONTRACTS.md`, `docs/MODEL_PROVIDER_POLICY.md`, `docs/MODEL_ROLE_TAXONOMY.md`, `docs/MODEL_PRIVACY_BOUNDARIES.md`, and related Sprint 02/02.5 artifacts.

**What was deferred:**

- Runtime inference clients, prompt execution, and provider credentials remain out of scope until contracts are stable.
- No local connector implementations were introduced in this session.

**What’s unblocked:**

- The architecture now has a source-of-truth contract layer for downstream components.
- Sprint 03 can proceed with ingestion and export work while remaining provider-neutral.
- Docs and tests now match the same contract language, reducing design/runtime drift risk.

**What changed in docs only:**

- Updated `README.md` with the Imprint hero visual for the main project narrative.
- Added `docs/assets/imprint-brand-board.png` and `docs/assets/imprint-hero.png` for publish-ready documentation context.

**Full story:** `docs/narrative/2026-06-07-schema-model-contract-foundation.md`

## Phase 2: Sprint 05 Adversarial Review and Post-Review Hardening — 2026-06-07

**Decision:** Conduct adversarial review of Signal 05 extraction engine; implement identified minor hardening items rather than deferring to Sprint 06.

**What changed:**

- **Adversarial review completed** (`docs/SPRINT_05_ARCHITECTURE_REVIEW.md`): Engine passed all six architectural gates (claim boundaries, evidence discipline, classification boundary, privacy, determinism, scalability). Verdict: GO for Sprint 06.

- **Signal model version tracking** (schema + engine): Added `signal_model_version` field to `ArtifactSignalEvidence`. Engine populates from `SIGNAL_CONFIDENCE_MODEL_VERSION = "sprint05-rule-v1"`. Future extraction rule changes are now auditable.

- **Source ID validation** (engine): Added `validate_source_id()` function that rejects filesystem paths, path traversal, and file extensions. Runs during signal creation; catches adapter leaks early.

- **Confidence formula documented** (engine): Added 30-line docstring to `_signal_confidence()` explaining weight rationale (0.25×attribution, 0.2×authorship_origin, 0.25×extraction, 0.2×evidence_strength, 0.1×policy_fit). Future tuning discussions now have explicit starting point.

- **Sprint 06 claim-level validation requirement documented** (architecture review): Profile compiler must reject `ClaimLevel.PROHIBITED` signals and validate `BOUNDED_INTERPRETATION` claims. Explicit requirement for Sprint 06 design.

- **Implementation expansion documented**: Discovered and verified that baseline of 8 rules expanded to 17 rules across 8 families. Reasoning (3), Narrative (3), Anti-Pattern (3) now implemented. All additions remain deterministic and artifact-local. Updated architecture review with expansion rationale.

- **Tests added**: `test_signal_model_version_is_tracked()`, `test_source_id_validation_rejects_paths()`. All 44 project tests passing.

**What's unblocked:**

- Evidence export chain is fully versioned (classification model version + signal model version).
- Privacy boundary actively enforced at signal creation time.
- Confidence formula is auditable and documented.
- Sprint 06 profile compiler has explicit claim-level validation requirements.
- Implementation expansion (17 rules) is documented with rationale.

**Full story:** `docs/narrative/2026-06-07-sprint-05-adversarial-review-and-hardening.md`

## Phase 3: Sprint 06 Profile Compilation Implementation — 2026-06-07

**Decision:** Implement deterministic profile compiler that aggregates artifact-level signals into expression profiles while enforcing strict signal eligibility, evidence preservation, and claim boundaries.

**What changed:**

- **Profile compiler engine** (`src/imprint/compiler/engine.py`, 464 lines): Deterministic rule-based compiler that:
  - Groups signals by pattern (family, name, observed feature, rule ID)
  - Projects artifact-level families into profile-level families (structure+formatting→structure, lexical→lexical, tone_marker→tone, rhetorical+reasoning→reasoning, narrative→narrative, anti_pattern→anti_pattern)
  - Enforces signal eligibility: only durable OBSERVATION claims from INCLUDED artifacts support durable profiles
  - Rejects PROHIBITED claims and incompatible signal model versions
  - Preserves full evidence chain: signal IDs, artifact IDs, source IDs (opaque), classification IDs, rule IDs, version metadata
  - Compiles claim text as "Across included artifacts, {observed_feature} appears in N artifacts"
  - Computes profile-level confidence from aggregated artifact-level components with support-count factor

- **Design and policy docs** (4 docs, 12.1 KB):
  - `COMPILER_DESIGN.md`: Aggregation pipeline, family projection, version boundaries, validation gates
  - `PROFILE_COMPILATION_RULES.md`: Eligibility criteria, evidence policy, confidence policy, build manifest policy, safety rules
  - `PROFILE_THEORY.md`: Expression-analysis core principle, subject→expression→voice model, allowed vs. forbidden claims, compilation boundary
  - `VERSIONING_POLICY.md`: Versioned surfaces, semantic roles, drift categories, comparability rules

- **Tests** (17 tests, 326 lines): Complete coverage of eligibility paths (durable, quarantined, excluded, non-durable, prohibited, bounded_interpretation), evidence preservation, version handling (mixed classifier versions, incompatible signal versions), privacy (no raw text, no paths), determinism, and error paths

- **CLI command** (`src/imprint/cli.py`): Added `compile` command that ingests artifacts, classifies, extracts signals, compiles profile, and reports summary

- **Adversarial review** (`SPRINT_06_ARCHITECTURE_REVIEW.md`): Post-implementation gate review across 7 dimensions (claim boundaries, signal eligibility, evidence discipline, version compatibility, privacy, determinism, scalability). Verdict: GO for Sprint 07.

**What's unblocked:**

- Expression profiles are now computable from ingested and classified artifacts and extracted signals.
- Profile evidence chains are fully versioned and traceable back to source artifacts and extraction rules.
- Claim-level validation is enforced: PROHIBITED claims rejected, BOUNDED_INTERPRETATION policy-gated, OBSERVATION-only for durable support.
- Incompatible extraction rule changes are detected and rejected (signal model version mismatch causes compilation error).
- Profile privacy is enforced: no raw text, opaque source IDs, validated against path leakage.
- Sprint 07 can proceed with export formats, report generation, and first-run experience design.

**Deferred to Sprint 07 and beyond:**

- Report generation and export formats (Markdown, JSON schemas for downstream systems)
- Publishing contracts and downstream prompts (how profiles are consumed by applications)
- Context profile enrichment (multi-voice separation, divergence tracking, inheritance policies)
- Bounded interpretation review workflow UI/tooling
- Confidence model tuning against labeled ground truth
- Advanced multi-voice profile support (casual vs. technical vs. published)

**Full story:** `docs/narrative/2026-06-07-sprint-06-compiler-verification-and-gates.md`

---

## Phase 3.5: Sprint 06 Adversarial Review — 2026-06-07

**Decision:** Conduct hostile principal architect review of Sprint 06 profile compilation against seven architectural gates.

**Review verdict:** GO for Sprint 07. No blockers.

**Key findings:**

- ✅ Claim boundaries enforced by design (expression patterns only, no diagnostic or personality claims)
- ✅ Signal eligibility strict (durable OBSERVATION only, PROHIBITED rejected, BOUNDED_INTERPRETATION gated)
- ✅ Evidence discipline excellent (full support chain preserved, opaque source IDs, version metadata throughout)
- ✅ Version compatibility enforced (incompatible signal versions rejected, classifier versions recorded)
- ✅ Privacy by design (no raw text, no paths, opaque source IDs validated)
- ✅ Determinism guaranteed (byte-for-byte reproducible, no LLMs/embeddings/providers)
- ✅ Scalability O(n log n) (no cross-signal quadratic logic)

**Test coverage:** 17 tests, all passing. Coverage includes happy path, all eligibility boundaries, version handling (mixed classifiers, incompatible signals), privacy verification, determinism, and error paths.

**Recommended carry-forward:**
1. Do not weaken claim-level validation
2. Do not merge incompatible signal versions without migration layer
3. Keep source IDs opaque in exports
4. Maintain no-raw-text policy
5. Preserve explicit filter/divergence model in context profiles

**Full story:** `docs/SPRINT_06_ARCHITECTURE_REVIEW.md`

## Phase 4: Sprint 07 Export Contracts and First-Run Experience — 2026-06-07

**Decision:** Implement the public-safe export layer for compiled profiles and create the first user-facing “What Imprint Learned” output without weakening compiler safety boundaries.

**What changed:**

- **Export package** (`src/imprint/exports/`): Added deterministic exporters for canonical JSON, human-readable Markdown, first-run summary, and Mosvera expression overlay.
- **Shared export safety**: Added validation that rejects prohibited claims, ungated bounded interpretations, non-durable support exported as durable evidence, mixed signal model versions, non-opaque source IDs, path-like data, and generation-control keys.
- **CLI command** (`imprint export-profile`): Added local compile-and-export flow for `json`, `markdown`, `first-run`, and `mosvera` formats.
- **Tests** (`tests/test_exports.py`): Added coverage for determinism, privacy, claim gates, bounded-interpretation policy gates, source opacity, signal-version compatibility, first-run source discipline, Mosvera boundary, and CLI smoke paths.
- **Documentation**: Added `docs/EXPORT_FORMATS.md`, `docs/FIRST_RUN_OUTPUT.md`, `docs/MOSVERA_INTEGRATION.md`, Sprint 07 narrative, and `docs/SPRINT_07_ARCHITECTURE_REVIEW.md`; updated export, first-run, derived-profile, README, and Sprint 07 docs.
- **Public narrative** (`web/index.html`): Added a landing-page export-contract section for canonical JSON, Markdown, first-run output, and Mosvera overlay boundaries.

**What remains out of scope:**

- LLM calls, remote APIs, prompt generation, publishing workflows, Broadside integration, Mosvera runtime behavior, application UI, demo article generation, and raw evidence export.

**Validation:** `pytest -q` passes with 71 tests. Direct CLI smoke was run for all four export formats with `PYTHONPATH=src python3 -m imprint.cli export-profile ...`.

**Review verdict:** GO for Sprint 08. No blockers.

**Full story:** `docs/narrative/2026-06-07-sprint-07-export-contracts.md`

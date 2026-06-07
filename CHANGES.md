# Imprint Changelog

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

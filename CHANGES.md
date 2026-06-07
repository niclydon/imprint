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

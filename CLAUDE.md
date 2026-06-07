# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Imprint at a glance

Imprint is a public-first identity and expression profile compiler. It analyzes human-authored artifacts (writing, messages, transcripts, documents) and produces structured expression profiles for downstream systems.

**Core pipeline:** configured sources → harvest → classify → extract signals → compile profile → export contracts

**Python 3.12+ project** with Typer CLI, Pydantic schemas, and SQLite storage (planned).

## Non-negotiable rules — public-first repository

- Do not commit real personal data, private corpus text, transcripts, emails, messages, screenshots, database dumps, or generated private profiles.
- Do not hard-code private hostnames, database names, local paths, API keys, emails, person names, or deployment-specific identifiers.
- All private integrations must be configured through `.env`, ignored local config, or external query files.
- Use synthetic fixtures and examples only.
- Keep source adapters and downstream integrations generic unless they are public examples.

**Config files to exclude:** `.env`, `imprint.config.yaml`, `*.local.yaml`, `*.db`, `*.sqlite*`.

## Setup and common commands

```bash
# Install for development (with test dependencies)
pip install -e ".[test]"

# Run the CLI
imprint version

# Run tests
pytest

# Run tests with coverage
pytest --cov=src/imprint tests/

# Run linting (Ruff)
ruff check src/ tests/

# Format code
ruff format src/ tests/

# Type checking (if mypy is added)
mypy src/imprint
```

**Local configuration:** Copy `.env.example` to `.env` and `imprint.config.example.yaml` to `imprint.config.yaml` for local development. Never commit these files.

## Architecture overview

### Conceptual layers

```
Artifact sources (files, APIs, custom)
  ↓
Harvester (source adapters convert to normalized artifacts)
  ↓
Artifact registry (metadata store, SQLite default)
  ↓
Classifier (speaker, type, audience, provenance, AI-risk)
  ↓
Signal extractor (lexical, tone, structure, reasoning, rhetoric, patterns)
  ↓
Profile compiler (aggregate signals, version, compute confidence, drift)
  ↓
Exporters (JSON, YAML, aesthetic pack, publishing contract, Markdown)
  ↓
Downstream consumers (agents, drafting tools, publishing, brand systems)
```

### Module structure (planned)

```
src/imprint/
  cli.py                 # Typer CLI entry point
  config.py              # Config loading (env, YAML, CLI)
  schemas/               # Pydantic models for artifacts, profiles, signals, exports
  sources/               # Source adapters (local_text, local_markdown, etc.)
  classify/              # Classification logic
  extract/               # Signal extraction (rule-based and LLM-backed)
  compile/               # Profile compilation and versioning
  export/                # Export formatters (JSON, YAML, markdown, etc.)
  privacy/               # Redaction and privacy enforcement
  storage/               # Database layer (SQLite default)
  api/                   # Optional FastAPI service (defer for MVP)
```

### Current status

- **Implemented:** CLI skeleton, basic config structure, example configs.
- **Next:** Storage layer (SQLite schema), artifact schemas, source adapters, classifier.

## Key design principles

1. **Public first:** All code, examples, tests, and docs are safe for public repository. Private details stay in `.env` and ignored config.
2. **Evidence-based:** Every signal is traceable to source metadata (type, time, confidence, speaker, AI-risk).
3. **Multi-dimensional voice:** Different artifacts (chat, essays, emails) contribute different signal types. Preserve these distinctions.
4. **Profiles, not samples:** Output is compiled profiles, not raw writing samples. Downstream systems don't need to read private messages.
5. **Versioned profiles:** Profiles track source windows, model versions, extractor versions, and drift over time.
6. **Configuration-driven:** All private integrations are external configuration, not hardcoded.

## Development workflow

### Adding a new feature or module

1. **Create schemas first** in `src/imprint/schemas/` with Pydantic models. Keep them public-safe (no person names, IDs, private labels).
2. **Add CLI command** in `src/imprint/cli.py` (use Typer groups for subcommands).
3. **Implement core logic** in the appropriate module (`extract/`, `compile/`, etc.).
4. **Write tests** in `tests/` with the same module structure. Use synthetic data only.
5. **Update docs** if the feature affects public API or configuration.

### Working with configuration

- **Defaults:** Checked into `imprint.config.example.yaml` and `.env.example`.
- **Local overrides:** Create `imprint.config.yaml` and `.env` (both ignored).
- **Priority order:** CLI args > env vars > local config > example config > code defaults.

### Testing

- **Use pytest.** Put tests in `tests/` mirroring `src/imprint/` structure.
- **Synthetic data only.** Never use real artifacts, transcripts, or personal data in tests.
- **Mock external services** (LLMs, databases, APIs) unless testing integration paths.
- **Cover privacy paths.** Test redaction, signal filtering, and private data exclusion.

## Product boundary

**Imprint owns:** Harvesting policy, artifact classification, signal extraction, profile compilation, export contracts, privacy enforcement.

**Imprint does not own:** Raw data lake, model router, publishing system, aesthetic-pack resolver, downstream application logic.

## Start here for context

- `docs/PROJECT_STRATEGY.md` — positioning, jobs, design principles
- `docs/ARCHITECTURE.md` — system design, recommended components, open questions
- `docs/SECURITY_PRIVACY.md` — privacy stance, redaction modes, data minimization
- `docs/ROADMAP.md` — planned milestones and phases

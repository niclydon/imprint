# Imprint Architecture

Status: planning

## System boundary

Imprint sits between raw evidence systems and downstream expression consumers.

```text
Raw data systems
  mail / chat exports / transcript stores / docs / articles / local files / custom APIs
        |
        v
Imprint
  harvest -> classify -> extract -> compile -> export
        |
        v
Downstream consumers
  aesthetic packs / publishing systems / agent frameworks / writing tools / creative pipelines
```

Imprint must not own the full data lake. It reads from configured sources, stores normalized artifact metadata, compiles profiles, and exports structured artifacts.

## Recommended components

### CLI

Primary user entrypoint.

```bash
imprint init
imprint sources list
imprint harvest --source local_markdown
imprint classify --profile default
imprint extract --profile default
imprint compile --profile default
imprint export --profile default --format mosvera
imprint diff --from v1 --to v2
imprint audit
```

### API service

Optional FastAPI service for local or private deployments.

```text
GET  /health
GET  /v1/profiles
GET  /v1/profiles/{id}
POST /v1/harvest
POST /v1/classify
POST /v1/extract
POST /v1/compile
GET  /v1/exports/{profile_id}/{format}
```

The API is optional for the MVP. The CLI and library should work without a service.

### Source adapters

Source adapters convert external records into normalized artifacts.

Public-safe built-ins:

- `local_text`
- `local_markdown`
- `local_jsonl`
- `local_transcript_json`

Private deployment adapters:

- sent mail
- chat exports
- transcripts
- AI conversation exports
- personal knowledge graphs
- custom SQL queries
- custom API sources

Private adapters should be generic and configured through environment variables or local config. No personal table names, hostnames, source names, emails, or paths should be hard-coded.

### Artifact registry

Stores normalized artifact metadata and optional content. SQLite should be the default. Postgres can be supported for larger deployments.

Core tables:

- `artifacts`
- `artifact_sources`
- `artifact_classifications`
- `signals`
- `profiles`
- `profile_versions`
- `exports`
- `audit_events`

### Classifier

Classifies artifacts before signal extraction.

Output dimensions:

- speaker attribution
- source type
- artifact type
- audience class
- authorship origin
- AI-assistance risk
- quote/forward/template risk
- time window
- privacy sensitivity
- usable signal dimensions

### Signal extractor

Extracts structured observations from classified artifacts.

Signal families:

- lexical
- tone
- humor
- structure
- reasoning
- narrative
- rhetorical moves
- metaphor patterns
- technical explanation style
- emotional register
- platform fit
- anti-patterns

Signal extraction should support multiple backends:

- local rule-based extractors
- local LLM through OpenAI-compatible endpoint
- cloud LLM through provider adapter
- no-LLM mode for basic statistics

### Profile compiler

Aggregates signals into versioned expression profiles.

Responsibilities:

- apply source weights
- handle exclusions and quarantines
- separate signal types
- compute confidence
- generate profile summaries
- generate downstream pack sections
- preserve evidence counts without leaking raw content
- compute drift against baselines

### Exporters

Initial exporters:

- canonical Imprint JSON
- canonical Imprint YAML
- aesthetic pack fragment
- publishing prompt contract fragment
- Markdown human-readable report

Future exporters:

- agent persona card
- character expression profile
- TTS style guidance
- eval prompt bundle

## Configuration model

Imprint should use layered config:

1. checked-in defaults
2. checked-in examples
3. local ignored config file
4. environment variables
5. CLI overrides

Recommended files:

```text
imprint.config.example.yaml   # committed
imprint.config.yaml           # ignored
.env.example                  # committed
.env                          # ignored
```

## Environment variables

```bash
IMPRINT_DB_URL=sqlite:///./data/imprint.db
IMPRINT_LLM_PROVIDER=openai_compatible
IMPRINT_LLM_BASE_URL=http://localhost:8000/v1
IMPRINT_LLM_API_KEY=change-me
IMPRINT_EMBEDDINGS_PROVIDER=openai_compatible
IMPRINT_EMBEDDINGS_BASE_URL=http://localhost:8000/v1
IMPRINT_REDACTION_MODE=strict
IMPRINT_PROFILE_OUTPUT_DIR=./exports
```

Connector-specific settings must use generic names:

```bash
IMPRINT_SOURCE_GMAIL_ENABLED=false
IMPRINT_SOURCE_GMAIL_CREDENTIALS_FILE=/path/to/local/credentials.json
IMPRINT_SOURCE_SQL_ENABLED=false
IMPRINT_SOURCE_SQL_DSN=postgresql://user:pass@host/db
IMPRINT_SOURCE_SQL_QUERY_FILE=/path/to/local/query.sql
```

## Public repository structure

```text
imprint/
  README.md
  LICENSE
  SECURITY.md
  CONTRIBUTING.md
  CODE_OF_CONDUCT.md
  pyproject.toml
  .env.example
  imprint.config.example.yaml
  src/imprint/
    cli.py
    config.py
    schemas/
    sources/
    classify/
    extract/
    compile/
    export/
    privacy/
    storage/
    api/
  docs/
  examples/
    synthetic_corpus/
    profiles/
    configs/
  tests/
```

## Dependency stance

Keep the core lightweight:

- Python 3.12+
- Pydantic for schemas
- Typer or Click for CLI
- SQLAlchemy or SQLModel for storage
- FastAPI only if service mode is included
- Rich for CLI output
- pytest for tests

LLM providers should be optional extras.

## Naming conventions

Use public-neutral names in code and docs:

- `subject_id`, not a person's real name
- `profile_id`, not private project name
- `source_id`, not private source label
- `local_sql`, not the name of a private database
- `openai_compatible`, not a private router name

## Open questions

- Should raw artifact text be persisted by default, or should the default store metadata and derived signals only?
- Should embeddings be part of Imprint or delegated to external stores?
- Should the MVP include API service mode or defer it until the CLI is stable?
- How should Imprint represent multi-person conversations without accidentally compiling other people's voices?
- What is the minimum viable drift metric that is useful without overclaiming?

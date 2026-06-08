# Security and Privacy Plan

Status: mandatory planning document

## Security thesis

Imprint is designed to analyze sensitive personal and professional communication artifacts. Privacy, provenance, and public-repo hygiene are product requirements.

The public repository must contain no private corpus data, no personal identifiers, no credentials, no local infrastructure details, and no hard-coded private assumptions.

## Protected data classes

Imprint may process the following data classes in private deployments:

- personal messages
- sent email
- private writing drafts
- transcripts
- meeting notes
- AI conversation exports
- personal knowledge graph records
- speaker-attributed audio/video transcript segments
- professional communications
- metadata such as timestamps, recipients, source names, and locations

These must never be committed to the public repository.

When local raw artifact storage is enabled, the Artifact Store is protected data. It is allowed
only under ignored local paths and exists for profile compilation, auditability, and regeneration.
It must not be exposed as a general memory or corpus search product surface.

## Public repository rules

### Never commit

- `.env`
- local config files
- database dumps
- local artifact stores
- private sample corpora
- screenshots from private systems
- exported personal profiles
- source credentials
- OAuth tokens
- API keys
- local hostnames
- private IPs
- private table names if unique to one deployment
- real email addresses in examples
- real message bodies
- real transcript excerpts
- real person names unless deliberately public and necessary

### Allowed in repo

- `.env.example`
- `imprint.config.example.yaml`
- synthetic corpora
- generated profiles from synthetic corpora
- generic connector interfaces
- redacted test fixtures
- schema examples using fictional people and organizations

## Secret handling

- All secrets must be loaded from environment variables or ignored config files.
- Example values must be obviously fake.
- Tests must not require real secrets.
- CI must run without private credentials.
- Provider integrations must skip gracefully when credentials are absent.

## Git hygiene

Recommended ignored paths:

```gitignore
.env
.env.*
!.env.example
imprint.config.yaml
*.local.yaml
*.local.json
/data/
/exports/
/private/
/corpus/
/tmp/
*.db
*.sqlite
*.sqlite3
*.dump
*.parquet
```

Do not ignore all `.json` or `.yaml` files globally because public schema examples are useful. Use directory-level rules.

## Pre-commit controls

Recommended checks:

- secret scanner
- high-entropy token detector
- private hostname detector
- email detector for fixtures
- corpus file size detector
- sample text detector for known private phrases
- denylist for local deployment names

Suggested tooling:

- gitleaks
- detect-secrets
- ripgrep-based custom checks
- pre-commit framework

## Redaction policy

Imprint should provide strict, balanced, and off modes.

### Strict

Default for public artifacts.

- redact emails
- redact phone numbers
- redact physical addresses
- redact URLs with private hostnames
- redact access tokens
- redact names not explicitly allowed
- redact exact timestamps unless needed
- redact source-specific IDs

### Balanced

For private profile reports.

- preserve coarse dates
- preserve source type
- preserve signal summaries
- redact direct content excerpts by default

### Off

Local-only. Must never be used in public CI or committed artifacts.

## Speaker attribution risk

The system must avoid compiling the wrong person's voice.

Controls:

- source adapters must indicate speaker confidence
- transcripts must require diarization or explicit speaker labels
- conversations must separate author text, quoted text, and assistant text
- forwarded email and quoted reply chains must be treated as high-risk unless parsed
- group chats must not assume every message belongs to the subject

## AI contamination risk

Recommended authorship-origin values:

- `human_origin`
- `human_directed_ai_assisted`
- `ai_origin_human_edited`
- `ai_origin_lightly_edited`
- `assistant_output`
- `quoted_or_forwarded`
- `template_or_notification`
- `unknown`

Profiles must be able to assign different weights by origin and signal dimension.

```yaml
source_policy:
  human_origin:
    lexical: 1.0
    structure: 1.0
    reasoning: 1.0
  human_directed_ai_assisted:
    lexical: 0.4
    structure: 0.5
    reasoning: 0.7
  assistant_output:
    lexical: 0.0
    structure: 0.0
    reasoning: 0.2
```

## Privacy-preserving outputs

Compiled profiles should favor abstracted patterns over raw excerpts.

Good:

```json
{
  "pattern": "uses concrete operational evidence before generalizing",
  "confidence": 0.86,
  "support": {
    "artifact_count": 42,
    "source_types": ["article", "technical_note"],
    "date_range": "2024-01 to 2026-02"
  }
}
```

Avoid by default:

```json
{
  "example": "exact private sentence from a message"
}
```

Profiles should record artifact storage mode and raw-content availability without exposing the raw
content in public-safe exports.

## Service-mode privacy boundary

Sprint 14 service mode is disabled by default and may expose only public-safe exports and
public-safe operational metadata from an explicit export directory. Service responses must not
include raw artifact text, source filesystem paths, credentials, private connector config, prompt
assembly, provider/model settings, or downstream publishing state.

Allowed service metadata is limited to health, version, validation status, warning counts, generated
export filenames, and compatibility warnings that pass the public-safe payload validator. Job
endpoints require explicit authentication and fail closed when auth is missing or invalid.

## Threat model

### Accidental public data leak

Controls: strong `.gitignore`, pre-commit scanning, synthetic examples only, ignored export directories, docs warning against real fixtures.

### Overbroad connector

Controls: speaker confidence thresholds, allowlist subject identifiers in local config, quarantine unknown speakers, per-source review reports.

### AI output laundering

Controls: AI-assistance classifier, date-based policy rules, source-specific origin metadata, profile weighting by origin, drift tracking.

### Downstream misuse

Controls: license and acceptable-use statement, consent-oriented docs, watermark or metadata options, default outputs designed for owner-controlled use.

### Prompt injection from corpus

Controls: quote source text as data, isolate instructions from artifacts, validate structured JSON, and forbid extraction prompts from following artifact instructions.

## Public-build checklist

- [ ] Repo has no real corpus files.
- [ ] Repo has no `.env` or local config.
- [ ] Full secret scan passes.
- [ ] Example corpus is synthetic.
- [ ] Generated example profiles are synthetic.
- [ ] README explains privacy model.
- [ ] Connector docs use fake values.
- [ ] CI runs without private services.
- [ ] Default config uses local SQLite and synthetic examples.
- [ ] Exported profiles are ignored by default.

## Incident response

If private data is committed:

1. Stop pushing.
2. Rotate any exposed credentials.
3. Remove the data from the working tree.
4. Rewrite git history if the repo is public or shared.
5. Invalidate generated artifacts derived from leaked data.
6. Document the incident in a private note, not public issue text, if sensitive.

## Maintainer stance

Privacy is a release blocker. If a feature makes the public/private boundary ambiguous, it does not ship until the boundary is explicit.

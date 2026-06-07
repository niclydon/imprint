# Configuration

Status: Sprint 09 baseline

## Configuration Goals

- Keep public code generic.
- Keep private deployments externalized.
- Make source systems configurable.
- Keep connector examples synthetic.
- Make output paths configurable.
- Make model providers optional and replaceable.
- Make privacy defaults strict.

## Config Files

Committed:

```text
.env.example
imprint.config.example.yaml
```

Ignored:

```text
.env
imprint.config.yaml
*.local.yaml
*.local.json
```

Private data and generated outputs should stay under ignored paths such as `data/`, `exports/`,
`private/`, or deployment-specific ignored directories.

## Environment Variables

```bash
IMPRINT_CONFIG_FILE=./imprint.config.yaml
IMPRINT_OUTPUT_DIR=./exports
IMPRINT_REDACTION_MODE=strict
IMPRINT_LOG_LEVEL=INFO
```

Optional local model/provider variables remain local configuration. They are not required for default
synthetic runs or Sprint 09 connector tests.

Connector credentials must be referenced by env var name from config:

```yaml
credentials:
  source_token:
    env: IMPRINT_PRIVATE_SOURCE_TOKEN
    required: false
```

Do not put credential values directly in YAML.

## Connector Config

Sprint 09 connector declarations live under `connectors`:

```yaml
connectors:
  - name: synthetic_markdown
    type: local_directory
    enabled: true
    adapter: local_markdown
    path: ./examples/synthetic_corpus/markdown
    storage_mode: metadata_only
    source_policy_version: sprint09-source-policy-v1
    tags: [synthetic]
    local_only: true
    private: false

  - name: synthetic_manifest
    type: manifest
    enabled: true
    manifest_path: ./examples/synthetic_corpus/connector-manifest.yaml
    storage_mode: metadata_only
    tags: [synthetic]
```

Supported Sprint 09 connector types:

- `local_directory`
- `manifest`

Deferred connector types such as Gmail, iMessage, Plaud, Looki, databases, cloud storage, and live
APIs must stay out of public core until a future private connector sprint.

## Dry Run

Run connector discovery without artifact ingestion:

```bash
imprint connectors-dry-run --config imprint.config.example.yaml
```

The dry-run output reports counts and connector metadata. It must not print raw artifact text or local
paths.

## Source Policy Config

```yaml
source_policy:
  chat_message:
    lexical: 0.9
    tone: 0.8
    humor: 0.7
    reasoning: 0.3
    structure: 0.1
    longform: 0.0

  transcript_segment:
    lexical: 0.6
    tone: 0.8
    humor: 0.7
    reasoning: 0.4
    structure: 0.0
    spoken_style: 1.0
```

Connector-level `source_policy_version` records which source policy applies. It does not make
connector metadata durable truth; classification and compilation still re-assess artifact hints.

## Authorship Policy Config

```yaml
authorship_policy:
  human_origin:
    multiplier: 1.0
  human_directed_ai_assisted:
    multiplier: 0.55
    allowed_dimensions: [reasoning, structure, topic_context]
  assistant_output:
    multiplier: 0.0
    quarantine: true
  quoted_or_forwarded:
    multiplier: 0.0
    quarantine: true
  template_or_notification:
    multiplier: 0.0
    exclude: true
```

## Validation

Startup and connector loading fail closed when:

- connector shape is invalid
- enabled paths or manifests are missing
- required connector env vars are unset
- config includes inline secret-like labels
- redaction mode is unsafe or missing in future runtime config
- public-safe exports attempt to include raw examples
- source policy references unknown dimensions in future source-policy validation

## Recommended Default

Default mode should remain boring and safe:

- synthetic local sources
- strict redaction
- `metadata_only` artifact storage
- raw examples disabled in public-safe exports
- no network connectors
- no cloud providers
- exports written to ignored directories

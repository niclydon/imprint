# Configuration Plan

Status: planning

## Configuration goals

- Keep public code generic.
- Keep private deployments externalized.
- Make all source systems configurable.
- Make all output paths configurable.
- Make LLM providers optional and replaceable.
- Make privacy defaults strict.

## Config files

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

## Environment variables

```bash
IMPRINT_CONFIG_FILE=./imprint.config.yaml
IMPRINT_DB_URL=sqlite:///./data/imprint.db
IMPRINT_OUTPUT_DIR=./exports
IMPRINT_REDACTION_MODE=strict
IMPRINT_LOG_LEVEL=INFO
```

## Source policy config

```yaml
source_policy:
  chat_message:
    lexical: 0.9
    tone: 0.8
    humor: 0.7
    reasoning: 0.3
    structure: 0.1
    longform: 0.0

  sent_email:
    lexical: 0.7
    tone: 0.6
    reasoning: 0.5
    structure: 0.3
    longform: 0.2

  longform_article:
    lexical: 0.7
    tone: 0.7
    reasoning: 1.0
    structure: 1.0
    longform: 1.0

  transcript_segment:
    lexical: 0.6
    tone: 0.8
    humor: 0.7
    reasoning: 0.4
    structure: 0.0
    spoken_style: 1.0
```

## Authorship policy config

```yaml
authorship_policy:
  human_origin:
    multiplier: 1.0
  human_directed_ai_assisted:
    multiplier: 0.55
    allowed_dimensions: [reasoning, structure, topic_context]
  ai_origin_human_edited:
    multiplier: 0.35
    allowed_dimensions: [topic_context]
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

## Config validation

Startup should fail closed when:

- redaction mode is missing
- output path points inside tracked example directories
- private source is enabled without required env var
- public-safe export includes raw examples
- source policy references unknown dimensions
- connector config includes inline secrets instead of env var references

## Recommended default

Default mode should be boring and safe:

- SQLite local database
- synthetic local source
- strict redaction
- raw examples disabled
- no network connectors
- no cloud providers
- exports written to ignored directory

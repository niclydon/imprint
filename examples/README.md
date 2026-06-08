# Synthetic Examples

The example corpus is intentionally synthetic and public-safe.

## Inputs

- `synthetic_corpus/markdown/example_article.md` - synthetic Markdown article
- `synthetic_corpus/chat.jsonl` - synthetic chat-style JSONL record
- `synthetic_corpus/transcript/synthetic-demo.json` - synthetic transcript segments with speaker metadata

## Commands

Dry-run configured connectors:

```bash
imprint connectors-dry-run --config imprint.config.example.yaml
```

Generate example exports:

```bash
imprint example
```

The default output directory is `exports/synthetic-demo/`, which is ignored by git.

## Safety Rules

Examples must not include real names, private messages, private emails, transcripts, account IDs,
service hostnames, credentials, source paths, or raw private exports.

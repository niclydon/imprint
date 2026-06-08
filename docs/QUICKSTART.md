# Quickstart

Status: Sprint 11 developer-preview baseline

This walkthrough runs Imprint against committed synthetic data only. It does not require private
corpora, credentials, model providers, homelab services, OAuth, live APIs, or network connectors.

## 1. Clone and Install

```bash
git clone https://github.com/niclydon/imprint.git
cd imprint
python -m venv .venv
source .venv/bin/activate
pip install -e ".[test]"
```

## 2. Check the CLI

```bash
imprint --help
imprint version
```

Expected:

- `imprint --help` lists commands such as `connectors-dry-run`, `example`, and `export-profile`.
- `imprint version` prints `0.1.0`.

## 3. Dry-Run Synthetic Connectors

```bash
imprint connectors-dry-run --config imprint.config.example.yaml
```

Expected:

- `synthetic_markdown` is enabled and discovers at least one artifact.
- `synthetic_chat` is enabled and discovers at least one artifact.
- `synthetic_transcript` is enabled and discovers transcript segments.
- `disabled_private_example` remains disabled and inert.
- No raw artifact text, source file paths, credentials, or private locators are printed.

## 4. Generate Public-Safe Example Exports

```bash
imprint example
```

Expected output files:

```text
exports/synthetic-demo/profile.imprint.json
exports/synthetic-demo/profile.md
exports/synthetic-demo/what-imprint-learned.md
exports/synthetic-demo/mosvera.expression.json
exports/synthetic-demo/human-cli.consumer.json
```

Inspect the human-readable outputs:

```bash
sed -n '1,80p' exports/synthetic-demo/what-imprint-learned.md
sed -n '1,80p' exports/synthetic-demo/profile.md
```

The generated files are ignored by git. They are derived from compiled profile metadata and should not
contain raw synthetic article text, source paths, credentials, provider prompts, or private source IDs.

## 5. Produce a Specific Export Manually

```bash
imprint export-profile \
  --source-type local_transcript_json \
  --path examples/synthetic_corpus/transcript/synthetic-demo.json \
  --subject-id example_subject \
  --format json \
  > exports/synthetic-demo/manual-profile.imprint.json
```

Supported formats:

- `json`
- `markdown`
- `first-run`
- `mosvera`
- `mosvera-consumer`
- `broadside`
- `agent`
- `human-cli`

## 6. Run Tests

```bash
pytest -q
```

The test suite uses synthetic fixtures and local deterministic rules. It should pass without any
private configuration.

## What Is Safe to Configure Next

Safe public/developer-preview changes:

- copy `.env.example` to `.env` for local-only settings
- copy `imprint.config.example.yaml` to `imprint.config.yaml`
- add synthetic local files under `examples/`
- write generated outputs under `exports/`

Keep out of git:

- `.env`
- `imprint.config.yaml`
- private messages, emails, transcripts, notes, or source exports
- real connector tokens, API keys, cookies, DSNs, account IDs, or hostnames
- generated private profiles and exports

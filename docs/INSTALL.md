# Install

Status: Sprint 11 developer-preview baseline

Imprint is a Python package with a console script named `imprint`.

## Requirements

- Python 3.12 or newer
- `pip`
- Git

No private services, credentials, model providers, or network connectors are required for the
synthetic developer-preview path.

## Editable Install

```bash
git clone https://github.com/niclydon/imprint.git
cd imprint
python -m venv .venv
source .venv/bin/activate
pip install -e ".[test]"
```

Verify:

```bash
python -c "import imprint; print(imprint.__version__)"
imprint --help
pytest -q
```

## Runtime Smoke Check

```bash
imprint connectors-dry-run --config imprint.config.example.yaml
imprint example
sed -n '1,40p' exports/synthetic-demo/what-imprint-learned.md
```

The smoke check uses:

- `examples/synthetic_corpus/markdown/example_article.md`
- `examples/synthetic_corpus/chat.jsonl`
- `examples/synthetic_corpus/transcript/synthetic-demo.json`
- `imprint.config.example.yaml`

Generated outputs are written under ignored `exports/`.

## Package Metadata

Current developer-preview metadata:

- package name: `imprint`
- version: `0.1.0`
- Python: `>=3.12`
- license: MIT
- console script: `imprint = imprint.cli:app`
- test extra: `pip install -e ".[test]"`

## Troubleshooting

If `imprint` is not found, activate the virtual environment and reinstall:

```bash
source .venv/bin/activate
pip install -e ".[test]"
```

If connector dry-run fails on missing paths, make sure the command is run from the repository root.

If generated output paths are missing, create them through the CLI:

```bash
imprint example
```

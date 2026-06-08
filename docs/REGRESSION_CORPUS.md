# Regression Corpus

Status: Sprint 12 baseline

The public regression corpus is synthetic. It exists to verify classification, signal extraction,
compilation, export safety, consumer projections, connector dry-run behavior, validation, and profile
comparison.

## Corpus Sources

Committed synthetic sources:

- `examples/synthetic_corpus/markdown/example_article.md`
- `examples/synthetic_corpus/chat.jsonl`
- `examples/synthetic_corpus/transcript/synthetic-demo.json`
- `tests/fixtures/`
- `tests/fixtures/regression/sprint12/`

## Executable Path

The Sprint 12 executable regression path is:

```bash
imprint example
imprint validate-export exports/synthetic-demo/profile.imprint.json
imprint diff exports/synthetic-demo/profile.imprint.json exports/synthetic-demo/profile.imprint.json
pytest -q tests/test_quality_gates.py
```

## Regression Coverage

The tests verify:

- canonical JSON export validation
- consumer contract validation
- raw text leakage failure
- path/source-ID leakage failure
- missing compatibility metadata failure
- comparable profile comparison
- compiler/version drift categorization
- corpus drift categorization
- no expression-drift claim for not-comparable profiles

## Corpus Rules

Regression fixtures must not contain:

- real names or accounts
- private messages, emails, transcripts, or notes
- private source paths
- credentials, tokens, cookies, DSNs, or private keys
- generated private profiles or exports

Synthetic JSONL fixtures are allowed only when intentionally placed under `examples/` or `tests/`.

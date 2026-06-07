# Contributing to Imprint

Imprint is early, public-first, and intentionally privacy-sensitive.

## Current status

Imprint is in active planning and foundation development. Expect schemas, terminology, and module boundaries to change.

## Contribution priorities

Good early contributions include:

- documentation improvements,
- schema review,
- synthetic fixtures,
- privacy and safety review,
- test coverage,
- local-only source adapters,
- CLI ergonomics,
- and evidence/confidence model feedback.

Please avoid large feature PRs until the Sprint 01 and Sprint 02 architecture/schema work is complete.

## Privacy rules

Do not include real private corpora in issues, pull requests, tests, examples, screenshots, or docs.

Never commit:

- real emails,
- real messages,
- real transcripts,
- real profile exports,
- database dumps,
- credentials,
- private hostnames,
- or local config.

Use synthetic examples only.

## Development principles

- Imprint observes expression. It does not diagnose people.
- Evidence matters more than polish.
- Confidence is support strength, not truth.
- Store less than you can.
- Keep private integrations configurable and out of public code.

## Before opening a PR

- Run tests if available.
- Check that no private data is included.
- Keep examples synthetic.
- Update docs when behavior changes.

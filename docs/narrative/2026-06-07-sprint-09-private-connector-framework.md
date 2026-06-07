# Sprint 09 Private Connector Framework

Sprint 09 added a generic connector framework for private-source ingestion boundaries without adding
real private service integrations.

The implementation introduced `src/imprint/connectors/` with config validation, capability/discovery
contracts, a registry, local-directory and synthetic-manifest connectors, and secret/path redaction.
Connectors feed existing adapters and preserve the existing adapter -> classification -> signal ->
compiler -> export boundary.

Public examples remain synthetic. Real private connectors such as Gmail, iMessage, Plaud, Looki,
databases, cloud storage, and live APIs remain deferred to future private deployment work.

Validation:

- `pytest -q` passed with 96 tests.
- `python3 -m compileall -q src` passed.
- `PYTHONPATH=src python3 -m imprint.cli connectors-dry-run --config imprint.config.example.yaml` passed.
- Static scan found no remote/provider/LLM call surfaces in connector code.

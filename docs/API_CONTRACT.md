# API Contract

Status: Sprint 14 service/API contract

## Contract Principles

All endpoints are public-safe by default. Responses must be serializable, deterministic, and free of
raw text, private paths, credentials, unredacted connector config, prompts, provider/model settings,
and downstream runtime behavior.

## Endpoints

### `GET /health`

Returns service liveness only.

Allowed fields:

- `service`
- `status`
- `mode`
- `read_only`

### `GET /version`

Returns package and contract versions.

Allowed fields:

- `service`
- `version`
- `export_schema_version`
- `consumer_contract_schema_version`

### `GET /status`

Returns public-safe readiness for the configured export directory.

Allowed fields:

- `service`
- `status`
- `latest_export`
- `latest_markdown_export`
- `latest_export_mtime`
- `validation_status`
- `warning_count`
- `read_only`
- `jobs_enabled`

`latest_export` and `latest_markdown_export` are filenames only. They are not paths.

### `GET /profiles/latest`

Returns the same public-safe canonical JSON payload as `GET /exports/latest.json`.

### `GET /exports/latest.json`

Returns the validated canonical JSON export from `profile.imprint.json`.

### `GET /exports/latest.md`

Returns the generated public-safe Markdown export from `profile.md`.

### `GET /warnings/latest`

Returns compatibility warnings and limitations extracted from validated canonical JSON.

Allowed fields:

- `service`
- `status`
- `warnings`
- `limitations`
- `warning_count`

### `POST /jobs/dry-run`

Requires job authentication. Returns a public-safe dry-run result and must not rebuild.

Allowed fields:

- `service`
- `status`
- `job`
- `would_rebuild`
- `status_report`

## Deferred Endpoints

The following endpoints are explicitly out of scope until a later reviewed sprint:

- `POST /jobs/rebuild`
- connector run endpoints
- scheduler mutation endpoints
- credential endpoints
- private config endpoints
- prompt/model/provider endpoints
- downstream publish endpoints
- raw corpus endpoints

## Error Contract

Errors should return short reason codes or safe messages. They must not include local paths,
credentials, raw text, config values, environment values, stack traces, or connector state.

## Compatibility

Service JSON export delivery must preserve the same canonical export schema as CLI output. Consumers
must validate the canonical JSON export before applying any profile constraints.


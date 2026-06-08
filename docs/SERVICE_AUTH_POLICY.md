# Service Auth Policy

Status: Sprint 14 service authentication policy

## Default

Service mode is disabled by default. If enabled, the default bind host is localhost and read endpoints
are allowed only for local/private consumers.

## Supported Modes

### 1. Disabled CLI-Only Mode

Default mode. No HTTP surface runs. Operators use the existing CLI and generated exports.

### 2. Localhost Read-Only Mode

Read endpoints are available on localhost only. Job endpoints remain authenticated. This mode is
acceptable for trusted same-machine consumers that need health/status/export reads.

### 3. Bearer-Token Private Mode

Read endpoints may also require a bearer token if the operator exposes the service beyond same-machine
localhost. Job endpoints always require explicit bearer-token authentication.

### 4. Reverse-Proxy Protected Mode

Private deployment may put the service behind Cloudflare Access, Tailscale-only access, or an
equivalent operator-owned private proxy. The proxy does not relax Imprint's own no-raw-corpus and
no-private-path response rules.

The Sprint 14 scaffold represents this with an explicit `external_protection` flag. Non-localhost
bind hosts are rejected unless `external_protection=True` and an auth token is configured. This keeps
localhost as the safe default while making private reverse-proxy deployment an explicit operator
choice.

## Job Authentication

`POST /jobs/dry-run` requires a bearer token. Missing or invalid auth fails closed. Tokens must come
from ignored local configuration or environment variables and must never be logged or returned.

## Logging

Logs may include endpoint names, validation result codes, timestamps, and counts. Logs must not
include credentials, local paths, raw text, environment values, private config, or request auth
headers.

## Rebuild Authentication

`POST /jobs/rebuild` is deferred. If later implemented, it must require explicit operator enablement,
bearer-token authentication, scheduler/job audit logging, and separate parity tests.

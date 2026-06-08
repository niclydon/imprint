# Service Automation Plan

Status: Sprint 14 automation plan

## Automation Posture

Automation is opt-in and local/private only. Sprint 14 implements only authenticated dry-run status.
Rebuild scheduling is planned but deferred until it can be reviewed with connector-specific
authority, replay manifests, and audit behavior.

## Allowed First-Cut Automation

- validate the latest generated canonical export
- report public-safe warnings and limitations
- report whether required generated files exist
- report dry-run readiness without changing files

## Deferred Automation

- scheduled rebuilds
- connector execution
- private source harvest
- live API calls
- provider/model calls
- downstream webhook delivery
- automatic publishing

## Scheduled Rebuild Requirements

If scheduled rebuilds are added later, they must:

- be disabled by default
- require explicit local operator configuration
- run only within the configured local runtime boundary
- record build manifests
- emit public-safe audit events
- preserve batch/service parity
- fail closed on connector/config errors
- emit compatibility warnings
- never silently publish or call downstream consumers

## Dry-Run Behavior

The Sprint 14 dry-run job validates the current export directory and returns status. It explicitly
does not rebuild. This gives automations a safe readiness check without adding ingestion authority.

## Audit Inputs

Automation audit entries may include:

- job type
- success/failure status
- validation status
- warning count
- artifact/export counts
- generated export filenames

Audit entries must not include raw text, filesystem paths, credentials, source snippets, account
identifiers, private connector state, or provider/model settings.


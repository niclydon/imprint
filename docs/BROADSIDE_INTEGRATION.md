# Broadside Integration

Status: Sprint 08 consumer contract

## Boundary

Imprint supplies public-safe expression constraints. Broadside owns publication decisions.

Sprint 08 does not implement a Broadside API client, publishing adapter, editorial workflow, article
generator, scheduler, platform formatter, or model-configuration layer.

## Consumer Payload

The Broadside consumer contract is generated from canonical Imprint JSON by
`broadside_consumer_contract(profile)`.

It may include:

- source profile metadata
- canonical export reference
- observed expression patterns
- support counts
- source-type summaries
- opaque source IDs
- confidence summaries
- limitations
- mandatory compatibility warnings
- no-raw-text evidence policy

It must not include:

- article generation prompts
- system prompts
- editorial or approval process logic
- publishing schedules
- platform-specific formatting rules
- model parameters
- provider controls
- raw artifact text or excerpts
- private source locators

## Usage Rule

Broadside should treat the payload as input constraints only. If Broadside turns the constraints into
a prompt, draft, schedule, or platform-specific publication artifact, that transformation belongs in
Broadside or in a separate downstream adapter, not in core Imprint.

# Consumer Contracts

Status: Sprint 08 baseline

## Purpose

Sprint 08 defines how downstream systems consume Imprint exports without moving downstream behavior
into core Imprint. Consumer contracts are deterministic projections of the canonical public-safe JSON
export. They are not integrations, adapters, prompt builders, publishing systems, runtime clients, or
model-configuration layers.

Canonical JSON remains the source of truth. Consumer projections may narrow and relabel canonical
fields for a target consumer, but they must not introduce new evidence, raw text, generation controls,
or workflow behavior.

## Mandatory Policy

Every consumer-facing projection must include compatibility and safety metadata. This is mandatory,
not optional presentation polish.

Required compatibility fields:

- compiler version
- classifier versions
- signal model versions
- canonical export schema version
- consumer contract schema version
- warnings array

Required warnings when applicable:

- multiple classifier versions in support metadata
- multiple signal model versions across profile patterns
- metadata-only audit limitations
- bounded interpretation policy state
- confidence is support strength, not truth about a person
- non-comparable or partially comparable profile state when a comparison workflow supplies that state

## Shared Safety Contract

Consumer payloads may contain:

- profile IDs and canonical export IDs
- observed expression patterns
- confidence summaries
- limitation summaries
- no-raw-text evidence policy
- opaque `source-*` source IDs
- compatibility warnings

Consumer payloads must not contain:

- raw artifact text
- raw evidence excerpts
- source filenames, filesystem paths, or private locators
- provider-specific prompts
- system prompts or prompt fragments
- model controls such as `temperature`, `top_p`, `model_hint`, `provider`, or decoding settings
- image generation instructions
- publishing workflows
- runtime adapter behavior
- diagnosis, personality typing, hidden-intent, or identity-truth claims

## Mosvera Contract

Purpose: let Mosvera consume an Imprint expression overlay without learning from raw private corpora
or taking over profile inference.

Allowed fields:

- expression summaries
- avoid-pattern summaries
- source profile/version metadata
- no-raw-text evidence policy
- opaque source IDs
- compatibility warnings

Boundary:

> Imprint compiles expression. Mosvera compiles aesthetic intent.

Mosvera owns aesthetic compilation, runtime behavior, provider setup, and visual generation. Imprint
only supplies expression constraints.

## Broadside Contract

Purpose: let Broadside or similar publishing systems consume profile exports as input constraints,
not drafting logic.

Allowed fields:

- profile summary
- observed expression patterns
- support counts and source types
- confidence and limitations
- public-safe source references
- compatibility warnings

Boundary:

> Imprint tells Broadside what expression patterns are supported. Broadside decides how publication
> systems use them.

Broadside owns editorial decisions, schedules, platform formatting, model settings, approval flows,
and draft generation.

## Agent / Application Contract

Purpose: let future agents, applications, and tools read Imprint exports safely.

Allowed behavior:

- validate canonical JSON first
- check export and contract versions
- display profile metadata
- display evidence summaries and limitations
- perform safe pattern lookup by signal ID
- surface compatibility warnings before use

Forbidden behavior:

- treating confidence as truth
- treating bounded interpretations as facts
- using quarantined or non-durable support as durable evidence
- inferring personality, diagnosis, values, or intent from expression patterns
- silently ignoring warnings

## Human / CLI Contract

Purpose: define how a person should inspect export outputs from the CLI.

Allowed behavior:

- show summary sections
- show observed patterns
- show limitations
- show compatibility warnings
- validate outputs against public-safe contract checks

Forbidden behavior:

- dumping raw corpus text by default
- presenting profile claims as identity truth
- hiding audit limitations

## Implementation Surface

Sprint 08 adds small deterministic helpers under `src/imprint/consumers/`. These helpers consume the
canonical JSON export and emit scoped consumer projections for Mosvera, Broadside, agents/apps, and
human CLI display.

The helpers do not call remote APIs, assemble prompts, generate drafts, tune models, create images,
or implement runtime integrations.

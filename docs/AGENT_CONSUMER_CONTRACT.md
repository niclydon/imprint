# Agent Consumer Contract

Status: Sprint 08 baseline

## Purpose

Agents, applications, and tools may read Imprint exports for validation, display, and safe expression
pattern lookup. They must not turn profile metadata into claims about identity, personality, mental
state, diagnosis, or intent.

## Source of Truth

Agents must treat canonical public-safe JSON as the source of truth. Consumer projections are
convenience views derived from canonical JSON.

## Required Behavior

Agents must:

- validate canonical JSON before using a consumer projection
- verify export schema and consumer contract schema versions
- surface compatibility warnings before applying constraints
- display limitations when displaying confidence or patterns
- preserve opaque source IDs
- preserve the no-raw-text evidence policy

Agents must not:

- treat confidence as truth
- treat bounded interpretations as facts
- upgrade quarantined, excluded, or non-durable support into durable evidence
- infer personality, diagnosis, values, or hidden intent
- ignore classifier, signal, compiler, metadata-only, or comparability warnings
- request raw corpus text through a public-safe projection

## Safe Pattern Lookup

The Sprint 08 agent projection exposes a `safe_pattern_lookup` keyed by signal ID. Each entry contains
only observed expression pattern text, claim level, confidence display value, support counts, source
types, opaque source IDs, audit limitations, and limitations.

The lookup is for display and constraint retrieval. It is not a prompt, instruction hierarchy, or
runtime policy engine.

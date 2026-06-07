# Memory Discipline

Status: Sprint 01.5 remediation decision

## Principle

Store less than you can.

Imprint may retain artifacts when needed for compilation, audit, and regeneration. It must not
become a general memory system.

## Allowed Retention

Allowed:

- artifact metadata
- local raw artifact text when explicitly enabled
- classifications
- signals
- profile versions
- build manifests
- evidence references
- audit events

## Disallowed Retention and Behavior

Disallowed:

- arbitrary fact recall
- assistant memory retrieval
- relationship graph construction
- open-ended corpus search as a product surface
- downstream access to raw artifacts by default
- storing private artifacts in public examples or docs

## Policy

Every retained field should have a profile-compilation reason.

If a field exists only because it might be useful someday, it should not be part of the MVP.

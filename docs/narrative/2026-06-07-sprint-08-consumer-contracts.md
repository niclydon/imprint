# Sprint 08 Consumer Contracts

Sprint 08 added deterministic consumer contract projections for Mosvera, Broadside, agents/apps, and
human CLI inspection.

The implementation keeps canonical JSON as the source of truth. Consumer contracts under
`src/imprint/consumers/` project canonical public-safe profile data into scoped payloads while
preserving compatibility warnings, no-raw-text policy, opaque source IDs, confidence caveats, and
limitations.

No downstream integration was added. Prompt assembly, provider settings, publication decisions,
Mosvera runtime behavior, image generation instructions, remote APIs, and LLM calls remain outside
core Imprint.

Validation:

- `pytest -q` passed with 82 tests.
- `python3 -m compileall -q src` passed.
- Static scan found no remote/provider/runtime calls in the consumer/export code path.

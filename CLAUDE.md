# Claude Code Instructions

Read `AGENTS.md` first. It is the canonical agent handoff for this repository.

Then read `REPO_MAP.md` and the active sprint prompt under `docs/sprints/` before changing files.

Do not use private data, credentials, private paths, provider calls, prompt assembly, or downstream runtime integrations unless the active sprint explicitly allows them.

Run:

```bash
python3 -m pytest -q
```

before reporting completion.

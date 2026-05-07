# Dev Context Refresh Instructions

This file is read by `make claude-dev`. The invocation is:

```bash
claude --dangerously-skip-permissions --print -p "Read .claude/CLAUDE-DEV.md and follow the instructions"
```

Your job is to (re)generate `.claude/dev-context.md` — a single file that gives a future Claude session enough context to be productive in this repo without reading the whole codebase.

## Scope

- **You may write** to `.claude/dev-context.md`.
- **You may NOT** modify any other file. Read everything you need, write only the context file.
- **You may NOT** commit or push.

## What dev-context.md should contain

Keep it under ~400 lines. Aim for *signal*, not coverage.

1. **Purpose** — one paragraph. What is Phloem; what problem does it solve.
2. **Status snapshot** — which interfaces are implemented vs. stubbed (read the source; do not trust prior notes).
3. **Module map** — one bullet per top-level module under `src/phloem/`, with a one-line role summary.
4. **Extension seams** — where the keystone abstractions are (`LLMAdapter`, `KBSource`, `BusClient`) and how to add to them.
5. **Conventions** — anything non-obvious about how this repo is laid out: `uv` for deps, `make check` for quality, ruff/mypy config, `.claude/` workflow files, test conventions.
6. **Things that surprised the previous Claude** — list any subtle gotchas surfaced by recent commits or open issues.
7. **Out-of-scope** — what NOT to refactor or "improve" without asking.

## Procedure

1. Read `README.md`, `pyproject.toml`, `Makefile`, `mkdocs.yml`.
2. Walk `src/phloem/` and skim every public symbol.
3. Skim the last 20 commits via `git log --oneline -20` for direction.
4. Write `.claude/dev-context.md`. Overwrite any prior version.
5. Print a one-paragraph summary of what changed since the previous version (or "first generation" if none existed).

## Style

Same as user-facing docs: short, direct, no fluff, no emojis. This file is for Claude — write what you'd want to read on day one.

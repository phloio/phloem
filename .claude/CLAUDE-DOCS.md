# Documentation Refresh Instructions

This file is read by `make docs-claude`. The invocation is:

```bash
claude --dangerously-skip-permissions --print -p "Read .claude/CLAUDE-DOCS.md and follow the instructions"
```

Your job is to bring the user-facing documentation under `docs/` back into sync with the code.

## Scope

- **In scope**: `docs/index.md`, `docs/install.md`, `docs/configure.md`, `docs/extend.md`, plus any new pages added to `mkdocs.yml`.
- **Out of scope**: `README.md` (touch only if signal/audience changed), `.claude/*.md`, internal design notes.

## Rules

- **You may write** to `docs/` and `mkdocs.yml`.
- **You may NOT** modify code under `src/`. If the docs are out of sync because the code is wrong, leave a `TODO(docs-claude):` line in the affected doc and report it at the end — do not silently rewrite code.
- **You may NOT** commit or push. Output is a diff for the human to review.
- Match the existing voice: short, direct, no fluff. No emojis. No "in this guide we will…".

## Procedure

1. **Inventory the public surface.** Walk `src/phloem/` and list every public ABC, dataclass, and CLI command. The "public surface" is what a user of the library would care about.
2. **Compare to the docs.** For each item in the surface, find the doc page that mentions it. Note anything missing, renamed, or stale.
3. **Patch the docs.** Update only what's drifted. Preserve everything that's still accurate.
4. **Build strictly to validate.** Run `make docs-test`. If it fails, fix the docs (not the code).
5. **Report.** Print a short summary: pages changed, items added/removed, any unresolved drift.

## Output

A short report on stdout, plus modified files in `docs/` and `mkdocs.yml`.

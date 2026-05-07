# Phloem — Claude Code session brief

This file is auto-loaded by Claude Code whenever a session opens in this
repository. It tells you (the Claude session) where to find what you
need.

## What Phloem is

A coordination substrate for operator-supervised LLM agent fleets.
Bus = NATS, runtime = Python daemons, LLM = pluggable adapter, role
catalog = `roles.yaml`. Public OSS, MIT-licensed.

The architecture, the rationale for each keystone choice, and the
phasing plan are documented — read them once at the start of a session
rather than rediscovering from scratch.

## Read before doing anything substantive

| Order | File | Purpose |
|---|---|---|
| 1 | `.claude/agent-context.md` | What the previous session was working on, what's blocked, what's the next concrete step |
| 2 | `docs/design/architecture.md` | The full system shape |
| 3 | `docs/design/decisions/index.md` | One-page index of architecture decisions; read individual ADRs as needed |
| 4 | `README.md` | The user-facing summary |

If `.claude/agent-context.local.md` exists, also read it — that's the
operator's personal scratchpad for things they don't want public.

## Conventions

- **Dependency management:** `uv` (not pip-tools or poetry). Use
  `[dependency-groups]` in `pyproject.toml`, not
  `[project.optional-dependencies]` for dev/docs deps.
- **Quality:** `make check` runs ruff + mypy + lock check. Run before
  every commit. CI runs the same.
- **Tests:** `make test`. Pytest with coverage and JUnit XML output.
- **Docs:** mkdocs-material. `make docs` to serve locally; `make docs-test`
  to validate strictly. `make docs-claude` runs a one-shot Claude that
  refreshes user-facing docs from code (output is a diff for review).
- **Make targets:** all targets are documented in
  `docs/getting-started.md` — read it once.
- **No shell scripts** in the project. Admin tooling lives as Click
  subcommands under `phloem admin`. See
  [ADR-0006](docs/design/decisions/0006-python-everywhere.md).
- **No emojis** in code or documentation unless the user explicitly
  asks. Write plainly.
- **Comments** are for the *why*, not the *what*. Default to writing
  none unless the comment captures a non-obvious constraint.

## Saving and loading session context

| Mechanism | When |
|---|---|
| `/save-context` slash command | Before stepping away — captures what we discussed and the current state into `.claude/agent-context.md` |
| Auto-load via this file | Every new session reads `.claude/agent-context.md` automatically |
| `/load-context` slash command | Manual re-read mid-session, rarely needed |

**Critical rule for `agent-context.md`:** the file is committed to a
**public** repository. Never write secrets, credentials, customer data,
internal hostnames, IP addresses, or anything that would embarrass
either the project or the operator. If unsure, omit. Use
`.claude/agent-context.local.md` (gitignored) for anything that
shouldn't be public.

## Status (v0.0)

Implemented:

- Package layout, type-checked ABCs (`LLMAdapter`, `KBSource`),
  pydantic-typed `roles.yaml` loader.
- CLI shell: `phloem version`, `phloem validate <file>`,
  `phloem admin <subcommand>` (stubs), `phloem ops <subcommand>`
  (stubs).
- Makefile, pre-commit, mkdocs, GitHub Actions CI, Testspace
  integration, GitHub Pages deployment, smoke tests.

Not yet implemented:

- `BusClient.{connect,publish,subscribe}` — NATS wiring.
- `ClaudeAdapter.run` — Anthropic SDK wiring.
- `FilesystemKBSource.{search,read}` — markdown search.
- `AgentDaemon.run` — the event loop.
- `phloem admin setup-relay` — VM provisioning.
- `phloem ops *` — bus interaction.

The contract / planned shape of every stub is documented in its
docstring. Don't reinvent the design when implementing.

## What you may NOT do without asking

- Push to remote.
- Force-push, amend, or rewrite published history.
- Delete branches you don't own.
- Create PRs.
- Run destructive operations (rm -rf, dropping DB tables, etc.).
- Bypass git hooks (`--no-verify`, `--no-gpg-sign`, etc.).

What you may freely do: edit files, run tests, run lint, build docs,
commit locally (and only if the user explicitly asks).

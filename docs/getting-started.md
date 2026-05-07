# Getting started

This page walks you from a fresh clone to a working development setup,
then catalogues every `make` target you'll use day-to-day.

## Prerequisites

- **Python 3.12+**
- **`uv`** — install from <https://docs.astral.sh/uv/>. Phloem uses `uv`
  for dependency management; trying to substitute `pip` will work but
  isn't supported in CI.
- **A NATS server**, eventually. Not required to run tests, lint, or
  build docs.
  - For local development: the single static binary from
    <https://nats.io>.
  - For shared/production use: see [Relay setup](relay-setup.md).
- **Provider credentials**, eventually. An Anthropic API key for
  Claude (`ANTHROPIC_API_KEY`), OpenAI key for OpenAI (`OPENAI_API_KEY`),
  etc. Not required to run tests, lint, or build docs.

## Install

```bash
git clone https://github.com/phloio/phloem.git
cd phloem
make install
source .venv/bin/activate
```

`make install` runs `uv sync --all-groups` (which creates `.venv/`,
installs the package in editable mode, and pulls every dev + docs
dependency) and then installs the pre-commit hooks. After activating
the venv you can use `phloem`, `pytest`, `ruff`, `mypy` and `mkdocs`
directly without prefixing each command with `uv run`.

Verify:

```bash
phloem version
```

## Run NATS for local development

The simplest local setup, no JetStream, no auth:

```bash
nats-server -p 4222
```

For anything beyond playing around, enable JetStream and bind it to a
data directory so messages survive restarts:

```bash
nats-server -js -sd ./nats-data -p 4222
```

For production setup with auth and TLS, see [Relay setup](relay-setup.md).

## Smoke test

```bash
phloem validate examples/roles.example.yaml
```

Expected:

```
ok: 2 role(s) defined
  - architect (claude/claude-opus-4-7)
  - ask-helper (claude/claude-sonnet-4-6)
```

If validation passes, your install is good. The runtime itself is not
yet implemented in v0.0 — the agent daemons, bus client, and admin
commands all exist as stubs that document their planned interface.

## Make targets

The `Makefile` is the development entry point. Every common task is
behind a target so you don't have to remember commands. `make help`
prints the list with descriptions; this section explains *when* to use
each.

### Day-to-day development

| Target | What it does | When to use |
|---|---|---|
| `make install` | Set up `.venv/` via `uv sync --all-groups` and install pre-commit hooks. | First time after clone, and again whenever `pyproject.toml` changes meaningfully. |
| `make check` | Lock-file check, pre-commit (ruff lint + format + baseline checks), mypy, dependency consistency. | Before every commit. CI runs the same. |
| `make test` | Pytest with coverage and JUnit XML output (`junit-test.xml`, `coverage.xml`). | Before every commit; whenever you've changed code. |
| `make clean` | Remove caches, build artefacts, JUnit XML, coverage XML, and the built docs site. | When something feels stale, or before profiling. |

### Documentation

| Target | What it does | When to use |
|---|---|---|
| `make docs` | Run `mkdocs serve` — live-reloading docs site at <http://127.0.0.1:8000>. | While you're editing docs locally. |
| `make docs-test` | Run `mkdocs build -s` — strict build (warnings = errors). | Before pushing docs changes. CI runs the same. |
| `make docs-claude` | One-shot Claude that reads `.claude/CLAUDE-DOCS.md` and refreshes user-facing docs from code. | When code has drifted from documentation and you want a Claude pass to bring them back in sync. The output is a diff for you to review — Claude does not commit. |

### Working with Claude Code

| Target | What it does | When to use |
|---|---|---|
| `make claude` | Start an interactive Claude Code session in this directory. Resumes the most recent prior session if one exists; otherwise starts fresh. Always passes `--dangerously-skip-permissions`. | Every time you sit down to work on Phloem. |

The `claude` target relies on a few project-level conventions to give
each session enough context:

- **`CLAUDE.md`** at the repo root. Auto-loaded by Claude Code on every
  session. Points at the design docs and the session-context files.
- **`.claude/agent-context.md`** (committed). The "what we were
  working on" file. Auto-loaded via `CLAUDE.md`. Updated by
  `/save-context` (a slash command — see below).
- **`.claude/agent-context.local.md`** (gitignored). Personal scratch
  for things you don't want public.

Slash commands inside a Claude session:

| Command | What it does |
|---|---|
| `/save-context` | Refresh `.claude/agent-context.md` to capture the current state of work. Run before stepping away. |
| `/load-context` | Manually re-read `.claude/agent-context.md` mid-session (rarely needed since CLAUDE.md auto-loads it on startup). |

### Help

| Target | What it does |
|---|---|
| `make help` | Print all targets with their one-line descriptions. The default goal — running just `make` does this. |

## Next steps

- Read the [Architecture](design/architecture.md) document for the why.
- Skim the [decisions](design/decisions/index.md) for the rationale
  behind the keystone choices.
- [Configure](configure.md) a `roles.yaml` for your project.
- [Extend](extend.md) — add a new LLM adapter or KB source.

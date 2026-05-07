# Agent session context

> **PUBLIC FILE — NO SECRETS.** This file is committed to a public
> repository. Do NOT record API keys, tokens, credentials, customer
> data, internal hostnames, IP addresses, or anything else that would
> be unsafe to share. If unsure, omit. Personal scratchpad lives at
> `.claude/agent-context.local.md` (gitignored).

**Last updated**: 2026-05-07
**Last session focus**: Repo bootstrap — scaffold, conventions, CI, docs publishing, design docs. Last act was writing this file as a manual test of the `/save-context` flow before stepping away.
**Branch**: `main` (working tree clean)
**Last commit**: `bb9447c` — Add design docs, ADRs, CLAUDE.md, and session-context system
**CI status**: Green on the last push (quality + tests + Testspace upload + GitHub Pages deploy all passing in ~46s)

## Where the project stands

v0.0 scaffold complete and CI is green. The full surface area exists,
the design is documented end-to-end, but most behaviour is stubbed.
Each stub has a docstring describing the contract it will fulfil — do
not reinvent the design when implementing. Read `CLAUDE.md`,
`docs/design/architecture.md`, and the ADRs under
`docs/design/decisions/` before touching code.

## What's done (cumulative, not just this session)

**Repo + license + tooling:**

- Public repo at <https://github.com/phloio/phloem>, MIT-licensed.
- Python 3.12+ package with `LLMAdapter`, `KBSource`, `BusClient`,
  `AgentDaemon` ABCs (typed, documented, stubbed).
- CLI: `phloem version`, `phloem validate <file>` (both work
  end-to-end). `phloem admin {setup-relay, configure, status,
  issue-creds, revoke-creds}` and `phloem ops {subscribe, inject, who,
  history}` are scaffolded and documented but raise NotImplementedError.
- `uv` for deps with PEP 735 dependency groups (`dev`, `docs`).
- Pre-commit: ruff (lint + format) pinned to v0.15.12 to match the dev
  dep, plus baseline checks.
- mypy strict-ish per phi-core conventions. Clean.
- Makefile: `install`, `check`, `test`, `docs`, `docs-test`,
  `docs-claude`, `claude`, `clean`, `help`. (`claude-new` and
  `claude-dev` were dropped this session as redundant.)

**CI + publishing:**

- GitHub Actions: quality + test (with Testspace upload of junit +
  coverage) + docs strict build + GitHub Pages deploy on push to main.
- Docs published at <https://phloio.github.io/phloem/>.
- README has CI / Testspace / Docs / License badges.
- Smoke tests (6, all passing) cover version, validate, and CLI
  subgroup registration.

**Design docs (committed this session):**

- `docs/design/architecture.md` — full canonical design, adapted from
  the original conversational draft at
  `phloio-agent/workspace/the-switchboard.md` (now superseded).
  Subjects normalised to `phloem.*`.
- `docs/design/decisions/` — six ADRs:
  - 0001 Use NATS as the message bus
  - 0002 Inversion of control — daemons own the event loop
  - 0003 Provider-neutral LLM adapter from day 1
  - 0004 Pluggable knowledge-base sources
  - 0005 Config-driven role catalog (`roles.yaml`)
  - 0006 Python everywhere — no shell scripts in admin tooling
- `CLAUDE.md` at root, auto-loaded by Claude Code on every session.
- `.claude/agent-context.md` (this file) committed; auto-loaded via
  CLAUDE.md.
- `.claude/agent-context.local.md` pattern documented and gitignored.
- `.claude/commands/save-context.md` and `load-context.md` slash
  commands.
- `docs/install.md` renamed to `docs/getting-started.md` with a
  thorough Make-target reference.

## What's next

The keystone work is implementing the **NATS `BusClient`**. Once it
runs, the daemon runtime, the Claude adapter, and the `phloem ops`
subcommands all unblock.

Concrete order, smallest viable steps:

1. **`BusClient.connect()` and `.publish()`** against a local NATS
   server. New file work in `src/phloem/bus/nats_client.py`. Add a
   `tests/integration/test_bus_basic.py` that actually starts a NATS
   server (via `pytest-nats` fixture or a docker fixture) and round-trips
   a `BusMessage`. This step requires NATS installed locally — see
   `docs/getting-started.md` for the one-line setup.
2. **`BusClient.subscribe()`** returning an async iterator of
   `BusMessage`s, with a JetStream durable consumer per subscriber name.
3. **Wire `phloem ops subscribe` and `phloem ops inject`** through the
   client. Now operators can use the bus from the terminal.
4. **`ClaudeAdapter.run()`** against the Anthropic SDK. Cover with a
   recorded-response test (e.g., `pytest-recording`).
5. **`AgentDaemon.run()`** — assemble bus + adapter + KB + role config.
   End-to-end smoke test: publish a message on `phloem.test.in`, assert
   a response on `phloem.test.out`.

Each step is independently testable and independently useful. Don't
skip ahead.

## Open questions to revisit when resuming

- **Conversation context store** (NATS KV vs SQLite per agent) — see
  the "What's still undecided" section of
  `docs/design/architecture.md`. Worth deciding before step 5.
- **Where SDK daemons run** (operator laptop vs shared dev server) —
  same source. Affects packaging and the eventual `phloem run` CLI
  shape.
- **Agent discovery / capability registry** — defer until there are
  more than 2 roles in a fleet.

## Tests passing locally as of this commit

- `make check` — ruff + mypy + lock check, clean
- `make test` — 6 smoke tests, all passing in <1s
- `make docs-test` — strict mkdocs build, clean

## Notes for future sessions

- The original architecture conversation lived in
  `phloio-agent/workspace/the-switchboard.md` (a different repo, on
  the `laurent/catalog-arch` branch). A "Superseded by" header was
  added there and committed locally; the commit was **not pushed** —
  push at your discretion when you next push that branch.
- The `phloio-agent` repo is the host project that will be Phloem's
  first consumer. Its current Slack-based agent system is what Phloem
  is eventually replacing.
- Running `make claude` in this repo gives you a session that
  auto-loads this file via `CLAUDE.md`. Start there. The Makefile uses
  `--continue` with a fallback to a fresh session, so it works whether
  there's a prior session in this cwd or not.
- `make claude-new` and `make claude-dev` no longer exist (dropped as
  redundant); don't be surprised if older notes mention them.

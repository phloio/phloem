# Agent session context

> **PUBLIC FILE — NO SECRETS.** This file is committed to a public
> repository. Do NOT record API keys, tokens, credentials, customer
> data, internal hostnames, IP addresses, or anything else that would
> be unsafe to share. If unsure, omit. Personal scratchpad lives at
> `.claude/agent-context.local.md` (gitignored).

**Last updated**: 2026-05-07
**Last session focus**: Repo bootstrap — scaffold, conventions, CI, docs publishing, design docs

## Where the project stands

v0.0 scaffold complete and CI is green. The full surface area exists
but most behaviour is stubbed and documented to spec rather than
implemented. See `README.md` for the public framing and
`docs/design/architecture.md` for the why.

## What's done

- Public repo at <https://github.com/phloio/phloem>, MIT-licensed.
- Package layout with `LLMAdapter`, `KBSource`, `BusClient`,
  `AgentDaemon` ABCs and stubs.
- CLI: `phloem version`, `phloem validate <file>`, plus `admin` and
  `ops` subgroups (all stubs).
- Tooling: Makefile, pre-commit, mkdocs, ruff, mypy, pytest, uv.
- CI: GitHub Actions runs quality + test (with Testspace upload) +
  docs build + GitHub Pages deploy on push to main.
- Docs published at <https://phloio.github.io/phloem/>.
- Design captured: `docs/design/architecture.md` plus six ADRs covering
  the keystone choices (NATS bus, inversion of control, LLM adapter,
  pluggable KBs, config-driven roles, Python-everywhere).
- `CLAUDE.md` at root telling new sessions where to look first.
- `.claude/agent-context.md` (this file) and the `/save-context` /
  `/load-context` slash commands wired in.

## What's next

The natural next step is implementing the **NATS `BusClient`** — it's
the keystone. Once it works, the daemon runtime, the Claude adapter,
and the `phloem ops` subcommands all unblock in sequence.

A reasonable order:

1. `BusClient.connect()` and `.publish()` against a local NATS server,
   covered by an integration test.
2. `BusClient.subscribe()` returning an async iterator of `BusMessage`s,
   with a JetStream durable consumer.
3. `phloem ops subscribe` and `phloem ops inject` wired through the
   client.
4. `ClaudeAdapter.run()` against the Anthropic SDK, covered by a
   minimal recorded-response test.
5. `AgentDaemon.run()` — wire it together, end-to-end smoke test that
   sends a message in and asserts a response out.

Each step is independently testable and independently useful. Don't
skip ahead.

## Open questions to revisit when resuming

- **Conversation context store** (NATS KV vs SQLite per agent) — see
  the "What's still undecided" section of
  `docs/design/architecture.md`. Worth picking before step 5.
- **Where SDK daemons run** (operator laptop vs shared dev server) —
  same. Affects packaging and the `phloem run` CLI shape.
- **Agent discovery / capability registry** — defer until there are
  more than 2 roles in a fleet.

## Tests passing locally

- `make check` — ruff + mypy + lock check, clean
- `make test` — 6 smoke tests, all passing in <1s
- `make docs-test` — strict mkdocs build, clean

## Notes for future sessions

- The original architecture conversation lived in
  `phloio-agent/workspace/the-switchboard.md` (a different repo).
  That document was the seed for `docs/design/architecture.md` here
  and is now superseded.
- The `phloio-agent` repo is the host project that will be the first
  consumer of Phloem. Its agent system is what we're eventually
  replacing.
- Running `make claude` in this repo gives you a session that
  auto-loads this file via `CLAUDE.md`. Start there.

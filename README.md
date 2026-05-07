# Phloem

[![CI](https://github.com/phloio/phloem/actions/workflows/ci.yml/badge.svg)](https://github.com/phloio/phloem/actions/workflows/ci.yml)
[![Tests](https://phloio.testspace.com/spaces/phloem/badge?token=tests)](https://phloio.testspace.com/spaces/phloem)
[![Docs](https://img.shields.io/badge/docs-phloio.github.io%2Fphloem-blue)](https://phloio.github.io/phloem/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> A coordination substrate for operator-supervised agent fleets.

Phloem lets a small team of human operators run a fleet of LLM-powered
agents that collaborate over a shared message bus. Operators observe and
inject; agents subscribe and respond. The bus is NATS, the agents can use
any LLM provider, and the role catalog is configuration — not code.

**Named after** the plant tissue that transports nutrients between organs.
Phloem moves information between organs in a system the same way its
namesake moves sugars in a tree.

## Status

**v0.0 — scaffold.** Nothing works yet. The package layout, interfaces,
and configuration shape are in place; adapters and the runtime are stubs.
This is the public starting point, not a usable release.

## What it is

- A **bus**: NATS subjects shaped around roles (`phloem.<role>.in/out/events`)
- A **daemon runtime**: one process per role, owns the event loop, invokes
  the LLM per message
- An **LLM adapter layer**: one interface, multiple providers (Claude first,
  OpenAI planned)
- A **knowledge-base abstraction**: pluggable sources (filesystem first,
  more later)
- An **operator MCP server**: lets a human in Claude Code (or any MCP host)
  observe the bus, inject messages, and supervise agents
- A **role catalog**: defined per project in `roles.yaml`

## What it is not

- An agent framework. Phloem orchestrates *between* agents; what an agent
  does internally is up to the LLM and its tools.
- A workflow engine. There is no DAG, no retries, no scheduler. Just a
  bus and a runtime.
- Hosted infrastructure. You bring your own NATS server.

## Documentation

- [Install](docs/install.md)
- [Configure](docs/configure.md)
- [Extend](docs/extend.md) — write a new adapter or KB source

## License

MIT — see [LICENSE](LICENSE).

# Install

## Prerequisites

- **Python 3.12+**
- **A NATS server.** For local development, the easiest path is the
  single static binary from <https://nats.io>. For production, run it
  on a small VM with JetStream enabled and TLS termination.
- **Provider credentials.** An Anthropic API key for Claude, an OpenAI
  key for OpenAI, etc. Set them via the conventional env vars
  (`ANTHROPIC_API_KEY`, `OPENAI_API_KEY`) or in your `roles.yaml`.

## Install Phloem

From source (until v0.1 is published to PyPI):

```bash
git clone https://github.com/phloio/phloem.git
cd phloem
pip install -e ".[claude]"      # or ".[all]" for every provider
```

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

For production, see [docs/configure.md](configure.md) — auth and TLS are
covered there.

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
yet implemented in v0.0 — see the project roadmap on GitHub.

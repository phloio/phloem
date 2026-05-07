# Phloem

> A coordination substrate for operator-supervised agent fleets.

## What you get

- **Bus**: NATS subjects shaped around agent roles.
- **Runtime**: one daemon per role, owning its own event loop. The LLM
  is invoked per message — it has no monitoring loop to forget.
- **Adapter layer**: Claude today, OpenAI next. Bring your own provider
  by implementing `LLMAdapter`.
- **Knowledge base abstraction**: filesystem today, anything queryable
  later.
- **Operator MCP server**: lets a human in Claude Code (or any MCP host)
  observe the bus and inject messages.
- **Config-driven role catalog**: `roles.yaml` per project; the runtime
  is project-agnostic.

## When to use it

- You have **multiple LLM agents** that need to coordinate.
- You have **one or more humans** who need to observe and occasionally
  steer those agents.
- You want the agents to **survive restarts**, **scale across machines**,
  and **not depend on a specific LLM provider**.

## When not to use it

- Single agent, single user → just call the LLM directly.
- Pure batch processing with no human in the loop → use a workflow engine.
- You need a UI shipped → Phloem is plumbing, not chrome.

## Next

- [Install](install.md)
- [Configure](configure.md) — anatomy of `roles.yaml`
- [Extend](extend.md) — write a new adapter or KB source

# 0002 — Inversion of control: daemons own the event loop

**Status**: Accepted
**Date**: 2026-05-06
**Decider**: Founding design conversation

## Context

In the predecessor system, each agent was a long-lived interactive Claude
Code session running an `/ask_monitor`-style loop:

```
LOOP:
  1. poll for new messages
  2. for each message: research, answer, persist
  3. sleep 30s
  4. GOTO 1
```

This worked technically but was *fundamentally fragile*. The LLM was
responsible for remembering to keep looping. Any time the operator told
the agent to do something else mid-loop, the loop died and the agent
went silent. We had to repeatedly remind it to monitor.

The root problem is that **LLMs do not own event loops**. They act when
invoked and then stop. Asking an LLM to *also* be a polling daemon is
fighting the grain of the tool.

## Decision

Phloem inverts control: a small, ordinary Python process (the
**daemon runtime**) owns the event loop. The LLM is invoked once per
incoming message as a stateless function, produces a response, and exits.

```
DAEMON LOOP (pure Python, never forgets):
  1. await message on phloem.<myrole>.in
  2. call llm_adapter.run(messages=[...], tools=[...]) -> response
  3. publish response to phloem.<myrole>.out
  4. persist updated context
  5. heartbeat to phloem.<myrole>.events
  6. GOTO 1
```

The daemon is a real program: it doesn't get distracted, doesn't forget,
doesn't need reminding, and survives restarts via JetStream durable
consumers.

## Consequences

**Positive**:

- The forgetfulness failure mode is structurally impossible.
- Crash recovery is JetStream's problem, not the LLM's.
- The LLM invocation is short-lived → low per-step token cost, easy to
  cap budgets per message.
- Each invocation is independently testable: feed it a message, check the
  response. No need to set up a long-running session to test agent
  behaviour.
- Multiple operators can interject without breaking anything — the daemon
  is publishing/subscribing, not holding a conversation.
- Different LLM providers can be swapped per role without changing the
  daemon (see [ADR-0003](0003-llm-provider-abstraction.md)).

**Negative**:

- Conversation context across messages must be reconstructed for each
  invocation. We store it in NATS KV or local SQLite per session and
  pass it back in. Slightly more boilerplate than "the LLM remembers."
- Loses the affordance of an interactive shell *for the agent itself*.
  Operators still get an interactive shell; agents become services.
- A single "what was I in the middle of saying?" turn requires the
  daemon to fetch context, which adds a few ms of latency vs. an
  in-process conversation.

**Neutral**:

- The agent role definitions (`roles.yaml`) become the thing that
  evolves; agent code (the daemon binary) is mostly identical across
  roles.

## Alternatives considered

### Keep the long-lived session model, fix the loop

Try harder to make the LLM remember to loop. Maybe more robust system
prompts, periodic self-check tools, or hooks. Rejected because the
failure mode kept resurfacing across many model and prompt variations —
we were fighting the architecture, not the prompt.

### Run the LLM session as a child of a supervisor that nudges it

A cron-like process that pokes the agent every N seconds with "still
monitoring?" Rejected because (a) it doesn't actually solve
forgetfulness, just papers over it, and (b) it makes the system
non-deterministic and noisy.

### External work queue, agents pull jobs

Equivalent in spirit to what we landed on — the daemon *is* the worker
pulling from the queue (NATS subject). The substantive choice is "make
the LLM stateless per message," which is the same answer.

## Notes

- The daemon implementation is mostly boring; expect a small core file
  per role rather than a framework.
- Heartbeats to `phloem.<role>.events` are how operators discover live
  agents — see [Architecture](../architecture.md) section 3.
- "Stateless per invocation" is a property of the *adapter call*, not of
  the role: the daemon retains durable state between calls (open
  questions, conversation history, journals).

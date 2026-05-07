# 0001 — Use NATS as the message bus

**Status**: Accepted
**Date**: 2026-05-06
**Decider**: Founding design conversation

## Context

Phloem needs a substrate that lets agent daemons, operators, and the
user-facing helper exchange messages. The substrate has to handle:

- Multiple subscribers to the same logical channel (operators all watching
  one role's traffic)
- Durable queueing so a crashed agent doesn't lose work
- Wildcard subscriptions (an operator wants `phloem.>` or `phloem.*.events`)
- Per-identity authn/authz scoped to subjects
- Cross-machine: agents on operator laptops, user-facing agent in the cloud,
  operators anywhere
- Replay from history when an agent restarts mid-conversation

It also has to be **boring infrastructure**: easy to deploy, easy to
diagnose, no business logic embedded in the bus itself.

## Decision

Use **NATS** (with JetStream enabled) as the message bus.

- Subjects shaped as `phloem.<role>.{in,out,events}`
  (configurable prefix per deployment).
- JetStream provides durable consumers and message replay.
- nkeys / JWT credentials per identity, scoped to subjects.
- TLS for cross-network connections.

A single small VM is enough for the foreseeable scale; clustering is a
config-only change later.

## Consequences

**Positive**:

- Multiple subscribers, wildcards, durable consumers, and replay are all
  built-in primitives, not things we have to build.
- Single static binary; deploys in minutes; trivial to operate.
- The subject hierarchy is the data model — no SQL, no schema migrations.
- Cross-machine and cross-network work out of the box.
- Strong auth model that maps naturally onto the role-based separation
  Phloem already needs.

**Negative**:

- Operators have to run a NATS server somewhere (Phloem ships
  `phloem admin setup-relay` to make this one command).
- NATS is less commonly known than HTTP or AMQP; documentation has a small
  learning curve.
- JetStream is a more recent NATS subsystem; production stability is good
  but less battle-tested than the core protocol.

## Alternatives considered

### Slack/Discord/chat-as-bus

What the predecessor system used. Rejected because:

- `conversations.history` is rate-limited and eventually consistent;
  polling either hammers the API or misses messages.
- Webhooks require a public receiver, which defeats "just use Slack."
- Multiple operators on one channel can step on each other.
- No durability or replay semantics; "what did I miss while offline?" is
  unsolved.

We retain the option of a one-way bridge (NATS → chat) for passive human
visibility — see [Architecture](../architecture.md), section 5.

### Append-only JSONL on a shared filesystem

Tail a file, append to write. Boring, debuggable with `cat`, no infra.
Rejected because:

- Doesn't work cross-machine without a network filesystem.
- No durable-consumer semantics; tracking "where am I in this stream"
  is each subscriber's problem.
- No subject hierarchy or wildcards.
- File rotation, locking, and concurrent-writer correctness are all
  manual.

Acceptable for a single-host, single-operator prototype; doesn't survive
contact with the requirements.

### Redis Streams

Real, designed-for-this option. Rejected because:

- Adds a Redis deployment with no other use in the system; NATS does the
  same job with less surface area.
- Per-subject auth is more awkward than NATS's nkeys/subject model.
- No native cluster/leafnode model that maps cleanly to "operators on
  laptops + agents on a server."

Reasonable second choice if NATS proves too unfamiliar.

### SQLite with WAL

Single writer, multiple readers. Durable, queryable, no infra. Rejected
because:

- Single-host only.
- No subscribe primitive; subscribers have to poll.
- No native auth model; you'd build it.

Useful as a *secondary* per-agent state store inside the daemon (which
Phloem may use), but not as the bus.

### A custom TCP/HTTP protocol

Considered for completeness. Rejected immediately — building a message
bus from scratch is the hardest possible answer to a solved problem.

## Notes

The schema for messages on the bus is intentionally minimal:

```json
{
  "id": "uuid",
  "ts": "2026-05-06T12:00:00Z",
  "sender": "architect",
  "subject": "phloem.architect.out",
  "type": "message",
  "payload": { "...": "role-specific" },
  "correlation_id": "optional-original-message-id"
}
```

If schema needs evolve, we version the envelope rather than negotiate
per-subject schemas.

# Architecture

> The full system shape Phloem implements.

**Status**: Accepted — this is the design Phloem implements. Individual
keystone choices are captured as ADRs under [decisions/](decisions/index.md).
**Last revised**: 2026-05-07

## Why this exists

Phloem grew out of three concrete problems with operator-supervised LLM agent
systems:

1. **Chat-as-bus is flaky.** Slack/Discord/etc. work for a single agent and a
   single operator, but polling, rate limits, and missed messages compound
   linearly with each new agent or operator.
2. **LLM agents have no event loop.** Any "monitor in a loop" pattern is
   fundamentally fragile because the LLM has to *remember* to keep looping.
   The first time the agent is told to do something else, the loop dies.
3. **Operators can't easily share the wire.** "One human watching one channel"
   doesn't compose across multiple operators or shifts.

There is also a latent fourth want: a **user-facing helper agent** ("Ask
Jeeves" — answers questions about a platform from inside the platform). With
the chat-as-bus model there is no place to plug it in.

Phloem addresses all four with one substrate.

## Three requirements

1. Connect agents together via **inversion of control** — the LLM is invoked
   per message, never owns the loop.
2. Provide a way to build a **user-facing "Ask Jeeves"-style helper** on the
   same substrate.
3. Allow **multiple operators** to observe and inject without contention.

## Layered view

```
┌───────────────────────────────────────────────────────────────────┐
│  OPERATORS (1..N)                                                 │
│  Claude Code (or any MCP host) + a "phloem-bus" MCP server        │
│  → subscribe, observe, inject on any subject                      │
└──────────────────┬────────────────────────────────────────────────┘
                   │
┌──────────────────▼────────────────────────────────────────────────┐
│  NATS (single VM is fine to start; JetStream + nkeys auth + TLS)  │
│  Subjects:                                                        │
│    phloem.<role>.in        — work coming in to a role             │
│    phloem.<role>.out       — work going out of a role             │
│    phloem.<role>.events    — lifecycle, status, heartbeats        │
│    phloem.user-help.<sid>  — per-session user-facing chats        │
│    phloem.ops.<topic>      — operator-only chatter                │
└─────┬──────────────────────────┬──────────────────────────────────┘
      │                          │
┌─────▼─────────────────┐  ┌─────▼──────────────────────┐
│  INTERNAL AGENT       │  │  USER-FACING AGENT         │
│  DAEMONS              │  │  (cloud, scoped tools)     │
│  one per role         │  │                            │
│  full local tool set  │  │  HTTP ←→ daemon ←→ NATS    │
│  Claude Agent SDK     │  │  Claude Agent SDK          │
└───────────────────────┘  └────────────────────────────┘

       (optional one-way bridge)
NATS ────────────► Slack / Discord / etc.  for passive human observability
```

## Components

### 1. NATS substrate

- **Where**: A single small VM is plenty to start (~€4/mo class). Single
  static binary + systemd unit + TLS via Caddy or NATS-native.
- **Auth**: nkeys per agent, per operator, per user-facing instance. Subjects
  are the permission boundary.
- **JetStream**: Enabled for `phloem.>` so messages survive agent restarts
  and can be replayed.
- **Schema**: Every message is JSON: `{id, ts, sender, subject, type, payload, correlation_id}`.

See [ADR-0001 — Use NATS as the message bus](decisions/0001-message-bus.md).

### 2. Internal agent daemons (Requirement #1 — inversion of control)

One process per role, defined in `roles.yaml`. Each daemon:

- Subscribes to `phloem.<myrole>.in` (durable consumer, so messages queue if
  the daemon is down)
- On message: invokes the LLM via the configured adapter as a function call,
  passing the message + relevant context
- The adapter exposes the same tools the agent role has been granted (Read,
  Edit, Bash, MCP servers, KB sources)
- Publishes the response to `phloem.<myrole>.out`
- Heartbeats to `phloem.<myrole>.events` every N seconds so operators can see
  who's alive

The daemon owns the event loop. The LLM is stateless per-invocation. State
(conversation history, journals, pending work) lives in NATS KV or a local
SQLite per agent.

**Key reframe**: agents stop being *"chat sessions that have to remember to
poll"* and become *"small services that invoke an LLM per event."* The
forgetfulness problem disappears because the LLM is no longer responsible for
the loop.

See [ADR-0002 — Inversion of control](decisions/0002-inversion-of-control.md).

### 3. Operator consoles (Requirement #3 — multiple operators)

Each operator runs an MCP host (Claude Code, the Anthropic desktop app, or
anything else that speaks MCP) with a `phloem-bus` MCP server that exposes
the bus as tools:

- `bus_subscribe(subject_pattern)` — start tailing
- `bus_inject(subject, message)` — publish as the operator
- `bus_history(subject, limit)` — pull from JetStream
- `bus_who()` — list live agents from `phloem.*.events`
- `bus_takeover(role)` — temporarily route a role's `.in` to this console
  (debugging)

NATS supports multiple subscribers natively — operators don't compete, they
all see everything they're authorized for. Per-operator auth scopes prevent
accidental footguns (e.g., trainees can observe but not inject on production
roles).

### 4. User-facing agent (Requirement #2)

Separate deployment (cloud container or process). Connects to NATS as a
publisher on `phloem.user-help.<sid>`:

- Web endpoint the host application calls: `POST /ask {session_id, user_id, message}`
- Daemon translates that to a NATS message on `phloem.user-help.<session_id>`,
  awaits response on a reply subject
- LLM invocation is **scoped**: tools = (platform docs reader, API read-only,
  knowledge-base search). No filesystem, no shell.
- Per-session conversation history in NATS KV keyed by `session_id`
- Token budget enforced per session
- Can publish "interesting" questions to `phloem.user-help.escalations` →
  an internal agent or operator picks them up

**Why this matters**: real user questions can flow into the existing internal
agent system. The user-facing agent isn't a separate product — it's a new
entry point on the same bus.

### 5. Optional chat bridge

A single process subscribes to `phloem.>` and posts a digest stream to
Slack/Discord/etc. for passive human visibility. One-way, one publisher → no
rate limits, no polling. Drop it entirely once operator consoles are good
enough.

## What this gets you

- **No more forgetful monitoring loops.** Daemons own the loop; the LLM is a
  function.
- **Operators become first-class.** Multiple humans can observe and inject
  without contention.
- **Internal agents keep their power.** Same tools, same code access, same
  MCP servers — just a different harness.
- **The user-facing helper shares the bus**, so user questions can flow into
  the internal agent system when needed.
- **Chat platforms become optional.** Keep them for passive observability,
  drop them when you don't need them.

## What this does *not* address

- The host project's knowledge base / curator workflow — orthogonal.
- Auth/billing/quotas for the public user-facing surface — needs its own
  design pass.
- Cross-org or multi-tenant deployment — single-tenant assumed for v1.

## What's still undecided

- **Conversation context store** — NATS KV vs SQLite per agent. Either works;
  KV centralizes, SQLite is more queryable.
- **Agent discovery / capability registry** — do agents publish what they can
  do to a `phloem.registry` subject so others can route work? Or is routing
  purely operator-driven?
- **User-facing-agent auth** — does it inherit the host platform's user auth,
  or does it need its own?
- **Where the SDK daemons run** — operator laptop (so they have local code),
  a shared dev server, or both (operator picks)?

## Phasing

Smallest viable steps, each independently useful:

1. **Stand up NATS** on a small VM — `phloem admin setup-relay` will
   automate this.
2. **Migrate one low-stakes agent** to the daemon model — prove the inversion
   of control works in production before touching the rest.
3. **Build operator console MCP server**, prove single-operator works.
4. **Add a second operator**, prove multi-op works.
5. **Migrate the rest of the internal agents** one at a time.
6. **Build the user-facing agent** on the proven substrate.
7. **Sunset the chat-as-bus mode** in the host project, keep one-way mirror
   only if useful.

---

*Phloem began as a conversation between Laurent Brack and Claude on
2026-05-06 about how to scale the Phloio internal agent system. The original
working draft lived at `phloio-agent/workspace/the-switchboard.md`; this
document is its canonical, polished version inside the Phloem repo.*

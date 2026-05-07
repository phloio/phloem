# Architecture decisions

Short architecture decision records (ADRs) capturing the *why* behind each
keystone choice in Phloem. Each ADR follows the standard
**Context / Decision / Consequences / Alternatives considered** shape.

| #    | Title | Status |
|------|-------|--------|
| 0001 | [Use NATS as the message bus](0001-message-bus.md) | Accepted |
| 0002 | [Inversion of control — daemons own the event loop](0002-inversion-of-control.md) | Accepted |
| 0003 | [Provider-neutral LLM adapter from day 1](0003-llm-provider-abstraction.md) | Accepted |
| 0004 | [Pluggable knowledge-base sources](0004-pluggable-knowledge-bases.md) | Accepted |
| 0005 | [Config-driven role catalog (`roles.yaml`)](0005-config-driven-roles.md) | Accepted |
| 0006 | [Python everywhere — no shell scripts in admin tooling](0006-python-everywhere.md) | Accepted |

## How to add an ADR

1. Pick the next number.
2. Copy an existing ADR as a template.
3. Fill in **Context**, **Decision**, **Consequences**, and **Alternatives
   considered**.
4. Set **Status** to `Proposed` while it's under discussion;
   `Accepted` once adopted; `Superseded by ADR-NNNN` if later overturned.
5. Add a row to the table above.
6. Open a PR. Discussion happens on the PR.

ADRs are not deleted once accepted — if a decision is reversed, write a new
ADR that supersedes the old one and update the old one's status to point at
the new one. The history is the value.

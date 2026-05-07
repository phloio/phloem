"""Per-role agent daemon — STUB.

Each role configured in `roles.yaml` becomes one running AgentDaemon
process. The daemon is a small, boring loop:

    1. Subscribe to my inbound subjects on the bus.
    2. For each incoming message:
         a. Load conversation context (from KB / state store).
         b. Call the LLM adapter with the message + context + tools.
         c. Process any tool calls the model emits.
         d. Publish the response to my outbound subjects.
         e. Persist updated context.
    3. Heartbeat to my events subject every N seconds.
    4. Survive restarts via JetStream durable consumers.

Crucially, the daemon — not the LLM — owns the event loop. The LLM is
invoked once per message and forgets nothing because there is nothing
for it to remember between calls.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from phloem.adapters.base import LLMAdapter
from phloem.bus.nats_client import BusClient
from phloem.kb.base import KBSource


@dataclass
class RoleConfig:
    """Resolved configuration for a single role."""

    name: str
    adapter: LLMAdapter
    bus: BusClient
    subjects_in: list[str]
    subjects_out: list[str]
    system_prompt: str
    tools: list[str]
    kb_sources: list[KBSource]
    heartbeat_interval_s: int = 30


class AgentDaemon:
    """Runs one role. Subscribes, invokes, responds, heartbeats.

    Not yet implemented. Planned interface:

        config = load_role_config("roles.yaml", role="architect")
        daemon = AgentDaemon(config)
        await daemon.run()  # blocks until cancelled
    """

    def __init__(self, config: RoleConfig) -> None:
        self.config = config

    async def run(self) -> None:
        raise NotImplementedError("AgentDaemon.run is not implemented in v0.0")

    async def shutdown(self) -> None:
        raise NotImplementedError("AgentDaemon.shutdown is not implemented in v0.0")

    async def _handle_message(self, raw: dict[str, Any]) -> None:
        raise NotImplementedError

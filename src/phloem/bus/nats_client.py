"""NATS client wrapper — STUB.

A thin layer on top of `nats-py` that:
- enforces Phloem's message envelope
- exposes subscribe/publish/request primitives
- handles JetStream consumer setup for durable subscriptions
- speaks nkeys/JWT auth

Subject conventions (Phloem-default; projects can override the prefix):

    phloem.<role>.in        work coming in to a role
    phloem.<role>.out       work going out of a role
    phloem.<role>.events    lifecycle, status, heartbeats
    phloem.user-help.<sid>  per-session user-facing conversations
    phloem.ops.<topic>      operator-only chatter
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass
class BusMessage:
    """Envelope for every message that crosses the bus.

    Adapters serialize this to JSON before publishing; subscribers
    deserialize back into this shape.
    """

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    ts: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
    sender: str = ""
    subject: str = ""
    type: str = "message"  # message | event | command | response
    payload: dict[str, Any] = field(default_factory=dict)
    correlation_id: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "ts": self.ts,
            "sender": self.sender,
            "subject": self.subject,
            "type": self.type,
            "payload": self.payload,
            "correlation_id": self.correlation_id,
        }


class BusClient:
    """Minimal NATS client wrapper — STUB.

    Planned interface:

        client = BusClient(servers=["nats://..."], creds_file="agent.creds")
        await client.connect()
        await client.publish("phloem.architect.in", BusMessage(...))
        async for msg in client.subscribe("phloem.architect.out"):
            ...
    """

    def __init__(
        self,
        servers: list[str] | None = None,
        creds_file: str | None = None,
        name: str | None = None,
    ) -> None:
        self.servers = servers or ["nats://localhost:4222"]
        self.creds_file = creds_file
        self.name = name

    async def connect(self) -> None:
        raise NotImplementedError("BusClient.connect is not implemented in v0.0")

    async def publish(self, subject: str, message: BusMessage) -> None:
        raise NotImplementedError("BusClient.publish is not implemented in v0.0")

    async def subscribe(self, subject_pattern: str, durable: str | None = None) -> Any:
        raise NotImplementedError("BusClient.subscribe is not implemented in v0.0")

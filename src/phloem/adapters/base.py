"""LLM adapter interface — the seam that lets Phloem support multiple providers.

Every agent invocation flows through an LLMAdapter. Concrete adapters
(claude, openai, ...) translate the provider-neutral types below into
provider-native API calls and back.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Literal


Role = Literal["system", "user", "assistant", "tool"]


@dataclass
class Message:
    """A single turn in a conversation, provider-neutral."""

    role: Role
    content: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ToolDefinition:
    """A tool the LLM may decide to call.

    `input_schema` is JSON Schema. Adapters translate to provider-native
    formats (Anthropic tool use, OpenAI function calling, etc.).
    """

    name: str
    description: str
    input_schema: dict[str, Any]


@dataclass
class ToolCall:
    """A model-emitted request to invoke a tool."""

    id: str
    name: str
    arguments: dict[str, Any]


@dataclass
class AdapterResponse:
    """The result of one LLM invocation."""

    content: str
    tool_calls: list[ToolCall] = field(default_factory=list)
    stop_reason: str | None = None
    usage: dict[str, int] = field(default_factory=dict)
    raw: Any = None  # provider-native response, kept for debugging


class LLMAdapter(ABC):
    """Provider-neutral interface for invoking an LLM.

    Implementations should be stateless — conversation history is passed
    in via `messages` on each call. Daemon code owns the loop.
    """

    name: str

    @abstractmethod
    async def run(
        self,
        messages: list[Message],
        tools: list[ToolDefinition] | None = None,
        system_prompt: str | None = None,
        max_tokens: int = 4096,
        **provider_kwargs: Any,
    ) -> AdapterResponse:
        """Invoke the model once and return its response.

        Args:
            messages: Conversation history, oldest first.
            tools: Tools the model is allowed to call.
            system_prompt: System-level instructions.
            max_tokens: Cap on response tokens.
            provider_kwargs: Adapter-specific knobs (e.g., temperature).
        """
        raise NotImplementedError

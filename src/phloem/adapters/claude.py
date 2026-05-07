"""Anthropic Claude adapter — STUB.

Will wrap the `anthropic` Python SDK. Not yet implemented.
"""

from __future__ import annotations

from typing import Any

from phloem.adapters.base import (
    AdapterResponse,
    LLMAdapter,
    Message,
    ToolDefinition,
)


class ClaudeAdapter(LLMAdapter):
    """LLMAdapter backed by the Anthropic Python SDK.

    Not yet implemented. Planned shape:

    - Accept `model`, `api_key` (or rely on env), and optional `base_url` for proxies.
    - Translate Phloem `Message`s to Anthropic message blocks.
    - Translate Phloem `ToolDefinition`s to Anthropic tool definitions.
    - Translate Anthropic `tool_use` blocks back to Phloem `ToolCall`s.
    """

    name = "claude"

    def __init__(
        self,
        model: str = "claude-opus-4-7",
        api_key: str | None = None,
        base_url: str | None = None,
    ) -> None:
        self.model = model
        self.api_key = api_key
        self.base_url = base_url

    async def run(
        self,
        messages: list[Message],
        tools: list[ToolDefinition] | None = None,
        system_prompt: str | None = None,
        max_tokens: int = 4096,
        **provider_kwargs: Any,
    ) -> AdapterResponse:
        raise NotImplementedError("ClaudeAdapter.run is not implemented in v0.0")

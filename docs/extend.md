# Extend

Phloem has two extension seams: **LLM adapters** and **KB sources**.
Both are plain Python ABCs; implement the interface, register your
class, reference it from `roles.yaml`.

## Add an LLM adapter

Implement `phloem.adapters.base.LLMAdapter`:

```python
from phloem.adapters.base import (
    AdapterResponse,
    LLMAdapter,
    Message,
    ToolDefinition,
)


class MyProviderAdapter(LLMAdapter):
    name = "my-provider"

    def __init__(self, model: str, api_key: str | None = None) -> None:
        self.model = model
        self.api_key = api_key

    async def run(
        self,
        messages: list[Message],
        tools: list[ToolDefinition] | None = None,
        system_prompt: str | None = None,
        max_tokens: int = 4096,
        **provider_kwargs,
    ) -> AdapterResponse:
        # Translate Phloem types -> your SDK's types
        # Call your SDK
        # Translate the response back -> AdapterResponse
        ...
```

Register it (mechanism is TBD pre-v0.1; likely an entry-point group
`phloem.adapters` or an explicit `register_adapter()` call). Then in
`roles.yaml`:

```yaml
adapter:
  type: my-provider
  model: my-model-id
  options:
    api_key: ...
```

### What "translate" means in practice

The interface intentionally avoids leaking provider-specific concepts.
Where providers differ:

- **Tool calling format.** Anthropic uses `tool_use` blocks; OpenAI uses
  `tool_calls` on the message. Your adapter should translate both
  directions so callers see Phloem `ToolCall` regardless.
- **System prompt placement.** Anthropic takes it as a top-level field;
  OpenAI puts it as the first message with `role: "system"`. Your
  adapter handles this.
- **Streaming vs. non-streaming.** v0.1 will be non-streaming only. A
  streaming variant of `run()` will be added later as a separate method.

## Add a KB source

Implement `phloem.kb.base.KBSource`:

```python
from phloem.kb.base import KBDocument, KBSource


class MyKBSource(KBSource):
    name = "my-kb"

    def __init__(self, **options) -> None:
        ...

    async def search(self, query: str, limit: int = 10) -> list[KBDocument]:
        ...

    async def read(self, uri: str) -> KBDocument:
        ...
```

Reference from `roles.yaml`:

```yaml
kb_sources:
  - type: my-kb
    options:
      ...
```

## What the runtime expects from your code

- **Stateless** between calls. The daemon owns the loop and passes
  history in.
- **Async**. All I/O is `async def`. Wrap sync SDKs with `asyncio.to_thread`
  if you must.
- **Honest exceptions**. Raise. The runtime logs and surfaces failures
  on `phloem.<role>.events`.
- **No silent retries**. If you want retries, do them explicitly with a
  budget you can configure.

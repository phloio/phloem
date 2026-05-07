# 0003 — Provider-neutral LLM adapter from day 1

**Status**: Accepted
**Date**: 2026-05-06
**Decider**: Founding design conversation

## Context

Different agent roles in a fleet have different needs:

- A heavyweight reasoning agent (architect) might want a frontier Claude
  model.
- A high-volume user-facing helper might want a cheaper, faster model
  from the same or a different provider.
- An on-prem deployment might require a self-hosted open model.
- Provider availability and pricing change over time.

If the daemon runtime is hard-coded to one provider's SDK, every change
above becomes a rewrite. The provider boundary is a natural seam for an
abstraction.

## Decision

Define an `LLMAdapter` ABC at the very centre of the daemon runtime.
Every LLM invocation flows through it. Concrete adapters wrap each
provider's SDK and translate to/from a small set of provider-neutral
types: `Message`, `ToolDefinition`, `ToolCall`, `AdapterResponse`.

```python
class LLMAdapter(ABC):
    name: str

    @abstractmethod
    async def run(
        self,
        messages: list[Message],
        tools: list[ToolDefinition] | None = None,
        system_prompt: str | None = None,
        max_tokens: int = 4096,
        **provider_kwargs: Any,
    ) -> AdapterResponse: ...
```

The role config in `roles.yaml` declares which adapter and model:

```yaml
adapter:
  type: claude
  model: claude-opus-4-7
  options:
    max_tokens: 8192
```

Day-1 ship: Claude adapter (wraps `anthropic` SDK). Planned next:
OpenAI. Anything else is pluggable.

## Consequences

**Positive**:

- Switching a role's provider is a config change, not a code change.
- Different roles can use different providers in the same fleet.
- The daemon runtime stays small and provider-agnostic.
- Self-hosted / open models are accommodated by writing one adapter.
- Forces the team to design tool/message handling at the right level of
  abstraction (not coupled to one vendor's quirks).

**Negative**:

- Tool-calling formats differ across providers (Anthropic `tool_use`
  blocks vs. OpenAI `tool_calls` on the message). Adapters absorb the
  translation; we accept that translation cost.
- System-prompt placement varies (top-level field vs. first message).
  Adapter responsibility.
- Streaming semantics vary. v0.1 is non-streaming only across the
  board; streaming will be added later as a separate adapter method.
- Some provider-specific features (Anthropic's prompt caching,
  OpenAI's reasoning-effort knob) leak through `provider_kwargs`. We
  accept this rather than design a lowest-common-denominator interface
  that hides useful capability.

## Alternatives considered

### Hard-code Claude

Simpler short-term. Rejected because retrofitting genericity later is
much more painful than designing it from day 1, and we already have a
concrete second-provider use case in the host project.

### Use a third-party "any LLM" wrapper (LiteLLM, etc.)

Considered. Rejected because the dependency surface is large for what
we need (chat + tools + streaming-later), the abstraction is heavier
than what fits the daemon runtime, and it complicates the message →
adapter → response flow with another translation layer.

### Per-role custom client code

Each role writes its own LLM client. Rejected — there's no per-role
variation worth that level of duplication, and it makes the runtime
much harder to reason about.

## Notes

- Adapters are async. Sync provider SDKs should be wrapped with
  `asyncio.to_thread`.
- Adapters are stateless — conversation history is passed in via
  `messages` on each call, consistent with
  [ADR-0002](0002-inversion-of-control.md).
- Prompt caching, where supported, is enabled inside the adapter
  (transparent to the daemon).

# 0004 — Pluggable knowledge-base sources

**Status**: Accepted
**Date**: 2026-05-06
**Decider**: Founding design conversation

## Context

Agent roles need access to bodies of knowledge:

- An internal-developer agent searches a markdown documentation tree.
- A user-facing helper searches public product docs.
- A code-aware agent searches a git repository.
- A future agent might query a vector store, Notion, or Confluence.

Hard-coding knowledge access into the daemon runtime forces every new
knowledge type to be a code change. Different roles in the same fleet
also commonly need access to *different* knowledge sources.

## Decision

Define a `KBSource` ABC. Each source implements two methods:

```python
class KBSource(ABC):
    name: str

    @abstractmethod
    async def search(self, query: str, limit: int = 10) -> list[KBDocument]: ...

    @abstractmethod
    async def read(self, uri: str) -> KBDocument: ...
```

Sources are configured per-role in `roles.yaml`:

```yaml
kb_sources:
  - type: filesystem
    options:
      root: ./public-docs
      glob: "**/*.md"
```

Day-1 ship: filesystem source (markdown directory). Planned: git, http,
vector-store wrappers. Anything else is pluggable.

## Consequences

**Positive**:

- A new knowledge source is one new module that implements two methods.
- Roles compose multiple sources cleanly — `kb_sources` is a list.
- Vector-search adapters can wrap any other `KBSource`, layering
  semantics without coupling.
- The runtime doesn't have to know whether a source hits a local file,
  a remote API, or an embedding index.

**Negative**:

- The interface is intentionally minimal (search + read). Some sources
  expose richer capabilities (graph navigation, structured query) that
  this interface flattens. Accepted: roles that need such richness can
  use a custom tool rather than going through `KBSource`.
- Source-specific URIs leak into `read(uri)` calls. Accepted as a
  pragmatic seam: the URI is opaque to the runtime, meaningful to the
  source.

## Alternatives considered

### Embed retrieval in each role

Each role role implements its own retrieval logic in its system prompt
and tools. Rejected because (a) duplication across roles, (b) the
retrieval pattern is the same shape across most use cases, (c) it
prevents cross-role reuse of curated knowledge.

### Standardise on one provider (e.g., a vector store)

Force every project to vectorise its knowledge into a specific store.
Rejected because (a) most projects start with markdown on disk and
graduate to vectors only when scale demands it, (b) it introduces a
hard dependency that v0.0 doesn't need, (c) it fails the "reusable
across projects" test.

### Tools-only, no KB abstraction

Treat KB access as just another tool the LLM can call. Rejected
because (a) it loses the per-role config-driven model, (b) it forces
each role to redeclare KB access in its tool list, (c) it makes
multi-source composition awkward.

## Notes

- The runtime exposes `KBSource` instances to the LLM as searchable
  read-only tools — the LLM does not see the source class directly.
- `KBDocument.metadata` is intentionally a free-form dict; sources can
  attach whatever they want (file path, modified time, score, etc.).

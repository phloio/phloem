"""Knowledge-base source interface — the seam for plugging in any KB.

A KBSource gives an agent role read access to a body of knowledge. The
canonical implementation is filesystem (markdown directory), but the
same interface accommodates git repos, HTTP, vector stores, Notion,
Confluence, etc.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class KBDocument:
    """One retrieved document from a KB source."""

    uri: str  # source-specific identifier (path, URL, doc id)
    title: str | None = None
    content: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


class KBSource(ABC):
    """A source of knowledge an agent can search and read.

    Implementations are responsible for translating their native query
    semantics into the search/read shape below. They do NOT need to
    implement embedding or vector search themselves — that can be
    composed in a separate adapter that wraps another KBSource.
    """

    name: str

    @abstractmethod
    async def search(self, query: str, limit: int = 10) -> list[KBDocument]:
        """Return documents matching the query, ranked best-first."""
        raise NotImplementedError

    @abstractmethod
    async def read(self, uri: str) -> KBDocument:
        """Read a single document by its URI."""
        raise NotImplementedError

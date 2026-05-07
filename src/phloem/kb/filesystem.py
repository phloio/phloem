"""Filesystem KB source — STUB.

Treats a directory of markdown files as a knowledge base. Search is
substring/regex over file contents to start; a vector-search wrapper
can be layered on later without changing this interface.
"""

from __future__ import annotations

from pathlib import Path

from phloem.kb.base import KBDocument, KBSource


class FilesystemKBSource(KBSource):
    """Markdown-on-disk knowledge base.

    Args:
        root: Directory to scan.
        glob: File pattern to include (default: ``**/*.md``).
    """

    name = "filesystem"

    def __init__(self, root: str | Path, glob: str = "**/*.md") -> None:
        self.root = Path(root).resolve()
        self.glob = glob

    async def search(self, query: str, limit: int = 10) -> list[KBDocument]:
        raise NotImplementedError("FilesystemKBSource.search is not implemented in v0.0")

    async def read(self, uri: str) -> KBDocument:
        raise NotImplementedError("FilesystemKBSource.read is not implemented in v0.0")

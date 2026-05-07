"""Knowledge-base sources. Each source is a pluggable adapter."""

from phloem.kb.base import KBDocument, KBSource
from phloem.kb.filesystem import FilesystemKBSource

__all__ = ["FilesystemKBSource", "KBDocument", "KBSource"]

"""Daemon runtime — owns the event loop, invokes the LLM per message."""

from phloem.daemon.runtime import AgentDaemon

__all__ = ["AgentDaemon"]

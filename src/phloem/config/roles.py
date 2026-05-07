"""Role configuration loader.

Reads `roles.yaml` (or any path) and produces typed RoleSpec instances
that the daemon runtime can resolve into AgentDaemons.

Roles are the unit of configuration in Phloem. Every project ships its
own `roles.yaml`; the runtime is otherwise project-agnostic.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field


class AdapterSpec(BaseModel):
    """Which LLM provider this role uses, and how."""

    type: str  # "claude" | "openai" | ...
    model: str
    options: dict[str, Any] = Field(default_factory=dict)


class KBSourceSpec(BaseModel):
    """Pointer to one knowledge-base source available to this role."""

    type: str  # "filesystem" | "git" | "http" | ...
    options: dict[str, Any] = Field(default_factory=dict)


class RoleSpec(BaseModel):
    """One row in roles.yaml."""

    name: str
    description: str | None = None
    adapter: AdapterSpec
    subjects_in: list[str]
    subjects_out: list[str] = Field(default_factory=list)
    system_prompt: str  # path or inline
    tools: list[str] = Field(default_factory=list)
    kb_sources: list[KBSourceSpec] = Field(default_factory=list)
    heartbeat_interval_s: int = 30


class RolesFile(BaseModel):
    """The whole roles.yaml document."""

    version: int = 1
    bus: dict[str, Any] = Field(default_factory=dict)  # connection / auth defaults
    roles: list[RoleSpec]


def load_roles(path: str | Path) -> RolesFile:
    """Parse roles.yaml from disk into typed objects."""
    text = Path(path).read_text(encoding="utf-8")
    raw = yaml.safe_load(text)
    return RolesFile.model_validate(raw)

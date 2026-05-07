"""``phloem ops`` — day-to-day bus operations from the terminal.

These commands let an operator observe and inject on the bus without
launching a full Claude Code + MCP setup. Useful for debugging, quick
tests, and scripting.

Planned subcommands:

    phloem ops subscribe <subject_pattern>   Tail subjects (wildcards allowed).
    phloem ops inject <subject> <message>    Publish a one-off message.
    phloem ops who                           List live agents from heartbeats.
    phloem ops history <subject> [--limit N] Pull recent messages from JetStream.
"""

from __future__ import annotations

import click


@click.group()
def ops() -> None:
    """Day-to-day bus operations."""


@ops.command()
@click.argument("subject_pattern")
@click.option(
    "--creds",
    type=click.Path(exists=True, dir_okay=False),
    default=None,
    help="NATS credentials file (defaults to bus.creds_file from roles.yaml).",
)
def subscribe(subject_pattern: str, creds: str | None) -> None:
    """Tail one or more subjects on the bus (wildcards allowed).

    Not implemented in v0.0.
    """
    raise click.ClickException("phloem ops subscribe is not implemented in v0.0")


@ops.command()
@click.argument("subject")
@click.argument("message")
@click.option(
    "--creds",
    type=click.Path(exists=True, dir_okay=False),
    default=None,
    help="NATS credentials file.",
)
def inject(subject: str, message: str, creds: str | None) -> None:
    """Publish a one-off message to a subject (not implemented in v0.0)."""
    raise click.ClickException("phloem ops inject is not implemented in v0.0")


@ops.command()
@click.option(
    "--creds",
    type=click.Path(exists=True, dir_okay=False),
    default=None,
    help="NATS credentials file.",
)
def who(creds: str | None) -> None:
    """List live agents based on recent heartbeats (not implemented in v0.0)."""
    raise click.ClickException("phloem ops who is not implemented in v0.0")


@ops.command()
@click.argument("subject")
@click.option("--limit", default=20, show_default=True, type=int, help="Number of messages.")
@click.option(
    "--creds",
    type=click.Path(exists=True, dir_okay=False),
    default=None,
    help="NATS credentials file.",
)
def history(subject: str, limit: int, creds: str | None) -> None:
    """Pull recent messages from JetStream for a subject (not implemented in v0.0)."""
    raise click.ClickException("phloem ops history is not implemented in v0.0")

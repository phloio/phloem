"""Phloem command-line interface.

Top-level groups:

    phloem version              Print version info.
    phloem validate <file>      Validate a roles.yaml.
    phloem run <file> <role>    Run one role's daemon (planned).
    phloem admin ...            Operator/administrator subcommands (relay, keys, config).
    phloem ops ...              Day-to-day bus operations (subscribe, inject).
"""

from __future__ import annotations

import sys

import click

from phloem import __version__
from phloem.cli.admin import admin
from phloem.cli.ops import ops


@click.group()
@click.version_option(__version__, prog_name="phloem")
def main() -> None:
    """Phloem — operator-and-agent-fleet coordination over NATS."""


@main.command()
def version() -> None:
    """Print version info."""
    click.echo(f"phloem {__version__}")


@main.command()
@click.argument("roles_path", type=click.Path(exists=True, dir_okay=False))
def validate(roles_path: str) -> None:
    """Validate a roles.yaml file."""
    from phloem.config import load_roles

    try:
        roles = load_roles(roles_path)
    except Exception as e:
        click.echo(f"invalid: {e}", err=True)
        sys.exit(1)

    click.echo(f"ok: {len(roles.roles)} role(s) defined")
    for role in roles.roles:
        click.echo(f"  - {role.name} ({role.adapter.type}/{role.adapter.model})")


@main.command()
@click.argument("roles_path", type=click.Path(exists=True, dir_okay=False))
@click.argument("role_name")
def run(roles_path: str, role_name: str) -> None:
    """Start one role's daemon (not implemented in v0.0)."""
    raise click.ClickException("phloem run is not implemented in v0.0")


main.add_command(admin)
main.add_command(ops)


if __name__ == "__main__":
    main()

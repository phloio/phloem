"""``phloem admin`` — relay setup, identity provisioning, configuration.

These commands are run by the human who owns the bus infrastructure
(usually the same person who provisioned the VM). They are NOT meant to
be called from agent daemons or from operator consoles in normal use.

Planned subcommands:

    phloem admin setup-relay <host>      One-shot: install + configure NATS on a fresh VM.
    phloem admin configure <host>        Re-apply config without reinstalling.
    phloem admin status <host>           Show running NATS server status.
    phloem admin issue-creds <name>      Generate nkeys/JWT credentials for a new identity.
    phloem admin revoke-creds <name>     Revoke previously issued credentials.

All subcommands operate over SSH; the caller is responsible for having
key-based access and `sudo` (NOPASSWD) on the target host.
"""

from __future__ import annotations

import click


@click.group()
def admin() -> None:
    """Administrative commands for the relay server and identities."""


@admin.command("setup-relay")
@click.argument("host")
@click.option("--user", default="root", show_default=True, help="SSH user on the target host.")
@click.option("--port", default=22, type=int, show_default=True, help="SSH port.")
@click.option(
    "--jetstream/--no-jetstream",
    default=True,
    show_default=True,
    help="Enable JetStream (recommended).",
)
@click.option(
    "--tls/--no-tls",
    default=True,
    show_default=True,
    help="Provision TLS via Caddy (recommended).",
)
@click.option(
    "--data-dir",
    default="/var/lib/nats",
    show_default=True,
    help="Where JetStream stores data on the target host.",
)
def setup_relay(  # noqa: PLR0913
    host: str,
    user: str,
    port: int,
    jetstream: bool,
    tls: bool,
    data_dir: str,
) -> None:
    """One-shot install + configure of NATS on a fresh VM.

    Prerequisites on the target host:

    - SSH key-based access for ``--user``.
    - ``sudo`` configured with NOPASSWD for ``--user`` (or ``--user`` is root).
    - A reachable hostname or IP at ``HOST``.

    What it will do (when implemented):

    1. Verify SSH connectivity and sudo privileges.
    2. Install NATS server (latest stable) via the official tarball.
    3. Write a systemd unit for ``nats-server`` with JetStream + TLS as configured.
    4. Generate an operator + system account + initial agent/operator nkeys.
    5. Open the firewall on the NATS port (4222) and the leafnode port if requested.
    6. Start and enable the service; verify ``nats-server --signal status``.
    7. Write the credential files locally so they can be referenced from ``roles.yaml``.

    The operation is idempotent — re-running it on a configured host repairs
    drift rather than starting over.
    """
    raise click.ClickException("phloem admin setup-relay is not implemented in v0.0")


@admin.command("configure")
@click.argument("host")
@click.option("--user", default="root", show_default=True, help="SSH user on the target host.")
def configure(host: str, user: str) -> None:
    """Re-apply NATS configuration to a previously set-up host (not implemented in v0.0)."""
    raise click.ClickException("phloem admin configure is not implemented in v0.0")


@admin.command("status")
@click.argument("host")
@click.option("--user", default="root", show_default=True, help="SSH user on the target host.")
def status(host: str, user: str) -> None:
    """Show NATS server status on the relay host (not implemented in v0.0)."""
    raise click.ClickException("phloem admin status is not implemented in v0.0")


@admin.command("issue-creds")
@click.argument("name")
@click.option(
    "--scope",
    type=click.Choice(["agent", "operator", "trainee"]),
    default="agent",
    show_default=True,
    help="Permission scope to grant.",
)
@click.option(
    "--out",
    type=click.Path(dir_okay=False),
    default=None,
    help="Where to write the credentials file (defaults to ./<name>.creds).",
)
def issue_creds(name: str, scope: str, out: str | None) -> None:
    """Generate nkeys/JWT credentials for a new identity (not implemented in v0.0)."""
    raise click.ClickException("phloem admin issue-creds is not implemented in v0.0")


@admin.command("revoke-creds")
@click.argument("name")
def revoke_creds(name: str) -> None:
    """Revoke previously issued credentials (not implemented in v0.0)."""
    raise click.ClickException("phloem admin revoke-creds is not implemented in v0.0")

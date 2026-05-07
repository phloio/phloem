"""Smoke tests — exercise the bits that already work in v0.0."""

from __future__ import annotations

from pathlib import Path

from click.testing import CliRunner

from phloem import __version__
from phloem.cli import main
from phloem.config import load_roles

EXAMPLE_ROLES = Path(__file__).resolve().parent.parent / "examples" / "roles.example.yaml"


def test_version_string() -> None:
    assert __version__
    assert __version__.count(".") >= 2


def test_cli_version_command() -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["version"])
    assert result.exit_code == 0
    assert __version__ in result.output


def test_cli_validate_example() -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["validate", str(EXAMPLE_ROLES)])
    assert result.exit_code == 0
    assert "ok:" in result.output


def test_load_roles_example() -> None:
    roles = load_roles(EXAMPLE_ROLES)
    assert roles.version == 1
    assert len(roles.roles) >= 1
    names = [r.name for r in roles.roles]
    assert "architect" in names


def test_cli_admin_subcommand_registered() -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["admin", "--help"])
    assert result.exit_code == 0
    assert "setup-relay" in result.output


def test_cli_ops_subcommand_registered() -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["ops", "--help"])
    assert result.exit_code == 0
    assert "subscribe" in result.output

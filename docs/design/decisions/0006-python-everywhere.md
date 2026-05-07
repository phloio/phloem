# 0006 — Python everywhere; no shell scripts in admin tooling

**Status**: Accepted
**Date**: 2026-05-06
**Decider**: Founding design conversation

## Context

Phloem ships an admin layer (`phloem admin setup-relay`, `configure`,
`status`, `issue-creds`, `revoke-creds`) that operates on remote VMs
over SSH. The natural temptation is to write this as a `setup-relay.sh`
shell script — that's the path of least resistance for "install some
stuff on a Linux box."

The same temptation applies to operator-facing tooling (`phloem ops`)
and to anything that wraps `nats` CLI commands.

## Decision

All admin and ops tooling is implemented as **Click subcommands inside
the `phloem` CLI**. No shell scripts in the project, beyond what
GitHub Actions runners require.

```
phloem admin setup-relay <host>
phloem admin configure <host>
phloem admin status <host>
phloem admin issue-creds <name> --scope agent
phloem ops subscribe <subject>
phloem ops inject <subject> <message>
```

Remote-host operations use `paramiko` or `asyncssh` from inside the
Python process. No `subprocess.run(["ssh", ...])` shell-out unless
genuinely necessary.

## Consequences

**Positive**:

- Operators get the admin tooling for free with `pip install phloem`.
  No second repo to keep in sync.
- Subcommands are testable (Click's `CliRunner`) and have typed
  arguments, validation, and `--help`.
- Composability: admin commands can call each other, share helper
  functions, share credentials handling. Shell scripts can't share
  state without files.
- Idempotency is easier to express in Python than in Bash.
- Cross-platform if it ever matters (Bash isn't on Windows out of the
  box; Click is).
- Errors raise typed exceptions instead of failing silently with
  unchecked exit codes.
- One language to read when something breaks.

**Negative**:

- Some "obvious" Bash recipes (`curl ... | tar xz`, `systemctl enable`)
  become slightly more verbose in Python.
- A new operator who is fluent in Bash but not Python has a small
  learning curve. Mitigated by `--help` output and clear error
  messages.
- Adding a new admin operation requires adding a Click subcommand and
  registering it, vs. dropping a `.sh` file in a directory. We accept
  the tradeoff.

## Alternatives considered

### Hybrid: Python CLI orchestrates shell scripts

The CLI wraps `setup-relay.sh`. Rejected because it gives the worst of
both: you still maintain shell scripts AND a Python wrapper, and the
script-vs-CLI boundary becomes a place where errors are silently lost.

### Pure shell scripts in `scripts/`, no admin CLI

Simpler short-term. Rejected because (a) it forks the project surface
into "the package" and "the scripts," (b) operators have to install
both, (c) we can't unit-test shell scripts the way we unit-test Click
commands.

### Use Ansible / Pulumi / Terraform for relay setup

Considered. Rejected for v0.1 because (a) it adds a heavyweight
dependency, (b) it pushes a tool choice onto users who may already use
something else, (c) the surface area we need (one VM, install NATS,
write a systemd unit) is small enough that direct SSH is simpler. Easy
to layer Ansible-callable wrappers on top later if there's demand.

## Notes

- Bash one-liners in `Makefile` recipes are fine — they invoke `make`
  targets which invoke Python. The principle is "no business logic in
  Bash," not "no Bash anywhere."
- GitHub Actions step `run:` blocks are Bash — that's a constraint of
  the runner, not a violation of this ADR.

# Relay setup

The relay is the NATS server every agent and operator connects to.
Phloem ships a `phloem admin setup-relay` command that takes a fresh
VM and brings it to a working, secured state in one step.

> **Status (v0.0):** the command is wired up but the implementation is
> a stub. The interface and prerequisites below are the contract it
> will fulfil. Track progress at <https://github.com/phloio/phloem/issues>.

## Prerequisites on the target VM

You provision the VM (Hetzner, DigitalOcean, Fly, your own metal —
Phloem does not care). Before running `setup-relay`, the VM must have:

- A public IP or hostname you can reach over SSH.
- Your SSH public key installed for some user (`root` or any user with
  `sudo`).
- That user configured with `NOPASSWD` `sudo` (or be `root` directly).
- Inbound TCP 4222 (NATS client port) reachable from your agents and
  operators. If you use TLS via Caddy, also TCP 443.

That's it. Phloem handles everything inside the VM.

## Run it

```bash
phloem admin setup-relay nats.example.com \
    --user phloem \
    --jetstream \
    --tls \
    --data-dir /var/lib/nats
```

What this will do:

1. Verify SSH connectivity and `sudo` privileges.
2. Install NATS server (latest stable) from the official release.
3. Write a systemd unit with JetStream + TLS as configured.
4. Generate an operator + system account + initial agent/operator
   nkeys.
5. Open the firewall on the NATS port.
6. Start and enable `nats-server`; verify it's healthy.
7. Write the credential files locally so you can reference them from
   `roles.yaml`.

The command is **idempotent** — re-running it on a configured host
repairs drift rather than starting over.

## Day-2: re-applying configuration

If you change config (e.g., add an account, rotate keys) and want to
re-apply without reinstalling:

```bash
phloem admin configure nats.example.com --user phloem
```

## Day-2: checking status

```bash
phloem admin status nats.example.com --user phloem
```

Reports NATS server health, JetStream stream sizes, and currently
connected clients.

## Issuing credentials for a new identity

When you onboard a new agent role or operator:

```bash
phloem admin issue-creds backend-developer --scope agent --out ./secrets/backend.creds
phloem admin issue-creds priya             --scope operator --out ./secrets/priya.creds
phloem admin issue-creds new-hire          --scope trainee  --out ./secrets/new-hire.creds
```

Scopes:

| Scope    | Can publish on                      | Can subscribe to    |
|----------|--------------------------------------|---------------------|
| agent    | `phloem.<own-role>.out` and `.events`| `phloem.<own-role>.in` and any allowlisted KB subjects |
| operator | `phloem.>` (anything)               | `phloem.>` (anything) |
| trainee  | `phloem.ops.>` only                 | `phloem.>` (read-only otherwise) |

Reference the resulting `.creds` file from `roles.yaml` (`bus.creds_file`)
or the operator console config.

## Why a Python command instead of a shell script?

Same reason the rest of Phloem is Python: testable, composable, no
Bash-isms, and operators only need `pip install phloem` to get the
admin tooling — no separate script repo to keep in sync.

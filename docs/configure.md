# Configure

Phloem's configuration model is one YAML file per project: `roles.yaml`.
The runtime reads it, resolves each role into a daemon, and runs them
all against the same bus.

## Anatomy of `roles.yaml`

```yaml
version: 1

bus:
  servers:
    - nats://nats.example.com:4222
  creds_file: ./secrets/agent.creds
  subject_prefix: phloem

roles:
  - name: architect
    description: System design and technical direction.
    adapter:
      type: claude
      model: claude-opus-4-7
      options:
        max_tokens: 8192
    subjects_in:
      - phloem.architect.in
    subjects_out:
      - phloem.architect.out
    system_prompt: ./prompts/architect.md
    tools:
      - read
      - grep
      - bash
    kb_sources:
      - type: filesystem
        options:
          root: ../knowledge-base
```

### Top-level fields

| Field     | Purpose |
|-----------|---------|
| `version` | Config schema version. Currently `1`. |
| `bus`     | Connection defaults shared by all roles. |
| `roles`   | List of role definitions. One daemon per role. |

### `bus`

| Field            | Purpose |
|------------------|---------|
| `servers`        | NATS server URLs. Multiple for clustering. |
| `creds_file`     | Path to nkeys/JWT credentials. Optional but recommended. |
| `subject_prefix` | Override the default `phloem` subject prefix. Use this if multiple Phloem fleets share a NATS cluster. |

### `roles[]`

| Field                  | Purpose |
|------------------------|---------|
| `name`                 | Role identity. Appears in subjects, logs, heartbeats. |
| `description`          | Human-readable. Surfaces in operator tools. |
| `adapter`              | Which LLM provider, model, and options. See [Adapters](#adapters). |
| `subjects_in`          | Subjects this role subscribes to. Wildcards (`>` and `*`) allowed. |
| `subjects_out`         | Subjects this role publishes responses to. |
| `system_prompt`        | Either an inline string or a path to a markdown file. |
| `tools`                | Tools the model is allowed to call. |
| `kb_sources`           | Knowledge bases this role can read. See [KB sources](#kb-sources). |
| `heartbeat_interval_s` | How often to publish to `phloem.<role>.events`. Default `30`. |

## Adapters

Each adapter declares a `type` and a `model`. Per-provider `options`
flow through to the underlying SDK.

| Type     | Status     | Required env / options |
|----------|------------|-------------------------|
| `claude` | scaffolded | `ANTHROPIC_API_KEY` (or `options.api_key`) |
| `openai` | planned    | `OPENAI_API_KEY` (or `options.api_key`)    |

Want a provider that isn't listed? See [Extend](extend.md).

## KB sources

A role can have any number of KB sources. The runtime exposes them to
the model as searchable read-only tools.

| Type         | Status     | Options |
|--------------|------------|---------|
| `filesystem` | scaffolded | `root` (required), `glob` (default `**/*.md`) |
| `git`        | planned    | `url`, `branch`, `path` |
| `http`       | planned    | `base_url`, `auth` |

## Authentication

Phloem inherits NATS's auth model. Recommended setup:

1. Generate per-identity nkeys/JWT credentials with `nsc`.
2. Issue one credential per agent role and one per operator.
3. Scope each credential to the subjects that identity is allowed to
   publish/subscribe.
4. Reference the credential file from `bus.creds_file`.

Operators get broader scopes than agents (e.g., the ability to publish
on `phloem.<any-role>.in`); trainee operators can be observe-only.

For development, you can run NATS without auth on `localhost`. Do not
do this in production.

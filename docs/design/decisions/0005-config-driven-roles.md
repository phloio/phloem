# 0005 — Config-driven role catalog (`roles.yaml`)

**Status**: Accepted
**Date**: 2026-05-06
**Decider**: Founding design conversation

## Context

A core goal of Phloem is that the runtime is **project-agnostic**. The
host project decides what its agents are called, what they do, what they
have access to, and how many of them exist. The same Phloem code should
run a fleet of internal-developer agents in one project and a fleet of
customer-support agents in another, with no Phloem changes.

The "what is in the fleet" information is not code — it's data. The
question is where that data lives.

## Decision

Every project ships a single YAML file describing its agent fleet:

```yaml
version: 1
bus:
  servers: [nats://...]
  creds_file: ./secrets/agent.creds
  subject_prefix: phloem
roles:
  - name: architect
    adapter: { type: claude, model: claude-opus-4-7 }
    subjects_in: [phloem.architect.in]
    subjects_out: [phloem.architect.out]
    system_prompt: ./prompts/architect.md
    tools: [read, grep, bash]
    kb_sources:
      - type: filesystem
        options: { root: ../knowledge-base }
```

The Phloem runtime reads this file, validates it (Pydantic), resolves
each entry into an `AgentDaemon`, and runs them all against the same
bus. The runtime contains no Phloio-specific (or any other project's)
strings.

## Consequences

**Positive**:

- A new project bootstraps by writing one YAML file.
- Adding/removing/renaming a role is a config change, not a code
  change.
- The same role definition format documents what the fleet *is*, which
  is useful for operators reading along.
- Validation surfaces errors at load time, before any daemon starts.
- Tooling (a `phloem validate <file>` command, today; richer linting
  later) can statically analyze a fleet.

**Negative**:

- YAML has known foot-guns (whitespace sensitivity, surprising type
  coercion). Mitigated by Pydantic validation + a strict schema.
- Some project-specific behaviour will need *some* code (a custom
  KBSource adapter, a custom tool). The seam between config-driven
  composition and code-required extension is the adapter ABCs.
- Secret material (creds files, API keys) shouldn't live in
  `roles.yaml` directly. We keep secrets out by referencing files /
  env vars from the YAML.

## Alternatives considered

### Code-driven role definitions

Each role is a Python class. The fleet is assembled in code (e.g., an
`agents/__init__.py`). Rejected because:

- Reusability across projects becomes a packaging problem.
- Operators can't read the fleet definition without reading code.
- Validation requires running Python.
- Ergonomics of "edit one line and restart" suffer.

### TOML or JSON instead of YAML

Considered. YAML wins because (a) multi-line strings (system prompts
inline) are far more readable, (b) comments are first-class, (c)
existing Python ecosystem familiarity. JSON has no comments; TOML's
nested-list syntax is awkward for `roles[].kb_sources[]`.

### One file per role

Considered. Rejected for v0.1 because the "list of roles in one place"
view is a high-value affordance for operators reading the system, and
the single file is short enough to fit on one screen for typical
fleets. We can split if a project's `roles.yaml` grows past a few
hundred lines.

## Notes

- `subject_prefix` defaults to `phloem` and is overridable per
  deployment so multiple Phloem fleets can share a NATS cluster.
- Future schema versions will be opt-in via `version:` — the loader
  rejects unknown versions rather than silently coerce.

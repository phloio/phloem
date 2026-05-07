---
description: Re-read .claude/agent-context.md and any local context, then summarise
---

Re-read the session-context files and produce a short oriented summary
so we can resume work cleanly.

## Procedure

1. Read `.claude/agent-context.md`.
2. If `.claude/agent-context.local.md` exists, read it as well.
3. Print a tight summary covering:
   - **What we were last working on** (one or two sentences)
   - **What's the next concrete step** (one sentence)
   - **Anything blocked or undecided** (one sentence each, only if
     there's something actually blocked)
4. Do not modify the files. Do not run shell commands beyond reading.

This command is normally not needed — `CLAUDE.md` already auto-loads
`agent-context.md` at session start. Use it when:

- You're mid-session and want to re-anchor after a long divergence.
- The user explicitly asks you to "reload the context" or similar.
- The agent-context file has been edited externally and you want to
  pick up the change.

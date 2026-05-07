---
description: Refresh .claude/agent-context.md with the current state of work
---

You're being asked to update `.claude/agent-context.md` so the next
Claude Code session in this repo can pick up where this one left off.

## Procedure

1. **Read the current `.claude/agent-context.md`** so you know what's
   already captured.
2. **Survey the actual state** — `git status`, `git log -10 --oneline`,
   the diff between main and the current branch (if any), uncommitted
   changes.
3. **Reconstruct what we've been working on** from this conversation:
   - Decisions made (and the why)
   - Files created or substantially changed
   - In-flight work that isn't done yet
   - Open questions left unresolved
   - Anything we explicitly deferred
4. **Rewrite `.claude/agent-context.md`** in full, preserving the
   public-no-secrets header. Aim for ~80–200 lines. Sections:
   - **Last updated** (today's date)
   - **Last session focus** (one line)
   - **Where the project stands** (one paragraph)
   - **What's done** (bullets, since last context save)
   - **What's next** (concrete next steps, ordered)
   - **Open questions to revisit when resuming**
   - **Notes for future sessions** (anything subtle that would surprise
     a stranger reading the repo)
5. **If `.claude/agent-context.local.md` exists**, leave it alone — that
   is the operator's personal scratch.

## Critical rule: no secrets

The file is committed to a **public** repository. Before writing
anything, scan your draft for:

- API keys, tokens, passwords, credentials of any kind
- Internal hostnames, IP addresses, domain names not already public
- Customer names, company names not already public
- Anything from `.env`, `secrets/`, or files starting with a dot that
  aren't otherwise public
- Personal information about people on the project beyond their public
  GitHub handles

If you spot anything in any of those categories, **omit it**. If you
think the user wanted it there, ask before writing — don't quietly
include.

## Output

After writing the file, print a one-paragraph summary of what changed
versus the prior version (or "first save" if the file was empty).
Don't commit or push — that's for the human to do.

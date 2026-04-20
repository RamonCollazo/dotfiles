---
name: vault-inbox
description: Write a handoff note to the Obsidian vault inbox when a gotcha, lesson learned, non-trivial decision, or useful discovery is encountered during work. Use when something unexpected happens, a workaround is needed, a debugging session reveals something non-obvious, or an architectural decision is made.
---

# Vault Inbox Handoff

When you encounter something worth documenting — a gotcha, lesson, decision, workaround, or non-obvious discovery — write a handoff file to the vault inbox.

## When to Write

- A non-trivial bug or misconfiguration is debugged
- A gotcha, limitation, or undocumented behavior is discovered
- A significant architectural or technical decision is made
- A workaround is needed for a tool or service
- External docs were wrong or misleading

Do NOT write handoffs for routine tasks, simple config changes, or things already documented in the vault.

## Where

`~/Repos/forgejo/personal/claude-obsidian/inbox/<YYYY-MM-DD>-<short-slug>.md`

## Template

```markdown
# Inbox: <short descriptive title>

## Project
<project name — e.g., homelab, devops-best-practices, vesperp4>

## What Was Done
<clear description of what was built, configured, or solved. Include the "why".>

## Tools Used
<comma-separated list of tools/services involved>

## Key Decisions Made
<options considered, what was chosen, why. Write "None." if no decisions.>

## Gotchas / Surprises
<anything unexpected — error messages, misconfigs, wrong docs. Be specific. Write "None." if nothing surprising.>

## References Used
<external URLs consulted, one per line. Write "None." if no external refs.>

## Existing Vault Notes Referenced
<vault notes read during this work, e.g., [[tools/cnpg/patterns]]. Write "None." if none.>

## Raw Notes
<logs, error outputs, config snippets, observations, follow-ups.>
```

## Quality Rules

- Be specific, not generic — include error messages, exact config, versions
- Capture the why, not just the what
- Don't filter gotchas — if it took time to figure out, document it
- Include real URLs, not "AWS docs"
- One handoff per logical unit of work

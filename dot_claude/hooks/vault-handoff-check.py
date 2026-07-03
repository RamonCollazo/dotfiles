#!/usr/bin/env python3
"""Stop hook: enforce 'documentation is part of done'.

If the session made meaningful changes (file edits or git commits) in a project
workspace but never wrote a vault inbox handoff, block the stop once with a
reminder. stop_hook_active guards against loops: the nudge fires at most once
per stop, and the second stop always passes.

Python is provided by mise in devpods (no system python in the images) and by
the OS on the host. Portable across host and devpods: paths are home-relative,
devpod workspaces (/workspaces/<repo>) are watched, and the hook stays silent
when the vault is not present. Fails open on any error.
"""
import json
import os
import sys

HOME = os.path.expanduser("~")
VAULT_INBOX = os.path.join(HOME, "Projects", "claude-obsidian", "inbox")
VAULT_INBOX_MARKER = "claude-obsidian/inbox"
WATCHED = [os.path.join(HOME, "Projects"), os.path.join(HOME, "Claude"), "/workspaces"]
EXCLUDED_DIR_PARTS = ("claude-obsidian", "vault-obsidian")
EDIT_TOOLS = {"Edit", "Write", "MultiEdit", "NotebookEdit"}
MIN_EDITS = 2


def in_watched(cwd: str) -> bool:
    real = os.path.realpath(cwd)
    for prefix in WATCHED:
        for p in (prefix, os.path.realpath(prefix)):
            if real == p or real.startswith(p + os.sep) or cwd.startswith(p + os.sep):
                return True
    return False


def main() -> None:
    data = json.load(sys.stdin)
    if data.get("stop_hook_active"):
        return

    if not os.path.isdir(VAULT_INBOX):
        return

    cwd = data.get("cwd", "")
    if not cwd or not in_watched(cwd):
        return
    if any(part in cwd for part in EXCLUDED_DIR_PARTS):
        return

    transcript_path = data.get("transcript_path", "")
    if not transcript_path or not os.path.exists(transcript_path):
        return

    edits = 0
    committed = False
    handoff_written = False
    with open(transcript_path, "r", errors="replace") as fh:
        for line in fh:
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue
            message = entry.get("message") or {}
            content = message.get("content")
            if not isinstance(content, list):
                continue
            for block in content:
                if not isinstance(block, dict) or block.get("type") != "tool_use":
                    continue
                name = block.get("name", "")
                tool_input = block.get("input") or {}
                file_path = str(tool_input.get("file_path", ""))
                if VAULT_INBOX_MARKER in file_path:
                    handoff_written = True
                elif name in EDIT_TOOLS and file_path:
                    edits += 1
                elif name == "Bash":
                    command = str(tool_input.get("command", ""))
                    if VAULT_INBOX_MARKER in command:
                        handoff_written = True
                    elif "git commit" in command:
                        committed = True

    meaningful = committed or edits >= MIN_EDITS
    if meaningful and not handoff_written:
        print(json.dumps({
            "decision": "block",
            "reason": (
                "This session made changes but no vault inbox handoff was written. "
                "Per the Project Agent protocol, write a handoff to "
                "~/Projects/claude-obsidian/inbox/<YYYY-MM-DD>-<slug>.md using the "
                "template in the project CLAUDE.md (What Was Done, Key Decisions, "
                "Gotchas, References), then commit and push the vault if working in "
                "a devpod. If the changes were genuinely trivial (typo-level, no "
                "knowledge worth keeping), state that in one line and stop."
            ),
        }))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)

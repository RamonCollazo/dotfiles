#!/usr/bin/env python3
"""Stop hook: enforce 'documentation is part of done'.

Design rule (Bitter Lesson): the hook supplies environmental facts and a single
nudge; the model judges whether a handoff is warranted. No transcript tool
parsing and no tool-name allowlists; those rot silently as the harness evolves.

Signals, all environmental:
- session start: timestamp of the first transcript line (the only harness-schema
  dependence; if unreadable, degrade to nudging, never to silence)
- handoff written: any vault inbox file modified since session start
- meaningful work (git repos only): dirty working tree or a commit since start

In a watched non-git directory, or when session start is unknown, the nudge
fires unconditionally once; a session with nothing to document says so in one
line and stops. stop_hook_active guarantees at most one nudge per stop. Fails
open on error. Python comes from mise in devpods and from the OS on the host.
"""
import json
import os
import subprocess
import sys
from datetime import datetime

HOME = os.path.expanduser("~")
VAULT_INBOX = os.path.join(HOME, "Projects", "claude-obsidian", "inbox")
WATCHED = [os.path.join(HOME, "Projects"), os.path.join(HOME, "Claude"), "/workspaces"]
EXCLUDED_DIR_PARTS = ("claude-obsidian", "vault-obsidian")
CLOCK_SLACK = 120


def in_watched(cwd: str) -> bool:
    real = os.path.realpath(cwd)
    for prefix in WATCHED:
        for p in (prefix, os.path.realpath(prefix)):
            if real == p or real.startswith(p + os.sep) or cwd.startswith(p + os.sep):
                return True
    return False


def session_start_epoch(transcript_path: str):
    if not transcript_path or not os.path.exists(transcript_path):
        return None
    try:
        with open(transcript_path, "r", errors="replace") as fh:
            for line in fh:
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue
                ts = entry.get("timestamp")
                if isinstance(ts, str) and ts:
                    return datetime.fromisoformat(ts.replace("Z", "+00:00")).timestamp()
    except (OSError, ValueError):
        pass
    return None


def handoff_written_since(start: float) -> bool:
    try:
        for name in os.listdir(VAULT_INBOX):
            path = os.path.join(VAULT_INBOX, name)
            if os.path.isfile(path) and os.path.getmtime(path) >= start - CLOCK_SLACK:
                return True
    except OSError:
        pass
    return False


def git(args, cwd):
    return subprocess.run(
        ["git", *args], cwd=cwd, capture_output=True, text=True, timeout=10
    )


def git_activity(cwd: str, start: float):
    """True/False when cwd is a git repo, None when it is not (or git is absent)."""
    try:
        inside = git(["rev-parse", "--is-inside-work-tree"], cwd)
    except (OSError, subprocess.SubprocessError):
        return None
    if inside.returncode != 0 or inside.stdout.strip() != "true":
        return None
    try:
        status = git(["status", "--porcelain"], cwd)
        if status.returncode == 0 and status.stdout.strip():
            return True
        head_time = git(["log", "-1", "--format=%ct"], cwd)
        if head_time.returncode == 0 and head_time.stdout.strip().isdigit():
            return int(head_time.stdout.strip()) >= start - CLOCK_SLACK
    except (OSError, subprocess.SubprocessError):
        return None
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

    start = session_start_epoch(data.get("transcript_path", ""))
    if start is not None:
        if handoff_written_since(start):
            return
        if git_activity(cwd, start) is False:
            return

    print(json.dumps({
        "decision": "block",
        "reason": (
            "Before stopping, apply the Project Agent protocol: if this session "
            "did meaningful work (built, configured, fixed, decided, or learned "
            "something) and no vault inbox handoff covers it yet, write one to "
            "~/Projects/claude-obsidian/inbox/<YYYY-MM-DD>-<slug>.md, then commit "
            "and push the vault if working in a devpod. If nothing worth "
            "documenting happened, say so in one line and stop."
        ),
    }))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)

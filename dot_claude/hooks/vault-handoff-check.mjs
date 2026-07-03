#!/usr/bin/env node
// Stop hook: enforce 'documentation is part of done'.
//
// If the session made meaningful changes (file edits or git commits) in a
// project workspace but never wrote a vault inbox handoff, block the stop once
// with a reminder. stop_hook_active guards against loops: the nudge fires at
// most once per stop, and the second stop always passes.
//
// Node (not python): devpod images have no system python, but mise ships node
// in every pod and on the host. Portable across host and devpods: paths are
// home-relative, devpod workspaces (/workspaces/<repo>) are watched, and the
// hook stays silent when the vault is not present. Fails open on any error.

import fs from "node:fs";
import os from "node:os";
import path from "node:path";

const HOME = os.homedir();
const VAULT_INBOX = path.join(HOME, "Projects", "claude-obsidian", "inbox");
const VAULT_INBOX_MARKER = "claude-obsidian/inbox";
const WATCHED = [path.join(HOME, "Projects"), path.join(HOME, "Claude"), "/workspaces"];
const EXCLUDED_DIR_PARTS = ["claude-obsidian", "vault-obsidian"];
const EDIT_TOOLS = new Set(["Edit", "Write", "MultiEdit", "NotebookEdit"]);
const MIN_EDITS = 2;

function realpathSafe(p) {
  try {
    return fs.realpathSync(p);
  } catch {
    return p;
  }
}

function inWatched(cwd) {
  const real = realpathSafe(cwd);
  for (const prefix of WATCHED) {
    for (const p of [prefix, realpathSafe(prefix)]) {
      if (real === p || real.startsWith(p + path.sep) || cwd.startsWith(p + path.sep)) {
        return true;
      }
    }
  }
  return false;
}

function main() {
  const data = JSON.parse(fs.readFileSync(0, "utf8"));
  if (data.stop_hook_active) return;
  if (!fs.existsSync(VAULT_INBOX)) return;

  const cwd = data.cwd || "";
  if (!cwd || !inWatched(cwd)) return;
  if (EXCLUDED_DIR_PARTS.some((part) => cwd.includes(part))) return;

  const transcriptPath = data.transcript_path || "";
  if (!transcriptPath || !fs.existsSync(transcriptPath)) return;

  let edits = 0;
  let committed = false;
  let handoffWritten = false;
  for (const line of fs.readFileSync(transcriptPath, "utf8").split("\n")) {
    let entry;
    try {
      entry = JSON.parse(line);
    } catch {
      continue;
    }
    const content = entry?.message?.content;
    if (!Array.isArray(content)) continue;
    for (const block of content) {
      if (!block || block.type !== "tool_use") continue;
      const name = block.name || "";
      const input = block.input || {};
      const filePath = String(input.file_path || "");
      if (filePath.includes(VAULT_INBOX_MARKER)) {
        handoffWritten = true;
      } else if (EDIT_TOOLS.has(name) && filePath) {
        edits += 1;
      } else if (name === "Bash") {
        const command = String(input.command || "");
        if (command.includes(VAULT_INBOX_MARKER)) {
          handoffWritten = true;
        } else if (command.includes("git commit")) {
          committed = true;
        }
      }
    }
  }

  const meaningful = committed || edits >= MIN_EDITS;
  if (meaningful && !handoffWritten) {
    process.stdout.write(JSON.stringify({
      decision: "block",
      reason:
        "This session made changes but no vault inbox handoff was written. " +
        "Per the Project Agent protocol, write a handoff to " +
        "~/Projects/claude-obsidian/inbox/<YYYY-MM-DD>-<slug>.md using the " +
        "template in the project CLAUDE.md (What Was Done, Key Decisions, " +
        "Gotchas, References), then commit and push the vault if working in " +
        "a devpod. If the changes were genuinely trivial (typo-level, no " +
        "knowledge worth keeping), state that in one line and stop.",
    }));
  }
}

try {
  main();
} catch {
  // fail open
}
process.exit(0);

# Global Instructions (Ramon)

## Knowledge system: vault is the source of truth

The Obsidian vault at `~/Projects/claude-obsidian/` is the single source of truth for
durable knowledge: gotchas, decisions, lessons, tool notes, project state.

- **Documentation is part of done.** When meaningful work completes, write an inbox
  handoff to `~/Projects/claude-obsidian/inbox/` per the Project Agent protocol
  (see the project CLAUDE.md symlink). Do this unprompted; do not wait to be asked.
- Built-in Claude memory is for **behavioral preferences and ephemeral state only**
  (how to act in a repo, what to skip). Never store lessons, gotchas, architecture,
  or project status in memory; that content goes to the vault inbox instead.
- Before starting work on a known tool or project, check the vault
  (`tools/`, `projects/`, `lessons/`, `patterns/`) before re-researching.
- **In a devpod**, the vault is a fresh clone: after writing an inbox handoff,
  `git add`/`commit`/`push` the vault (auth is automatic via `FORGEJO_TOKEN`), or the
  handoff dies with the container.

## Harness design rule (Bitter Lesson)

- When changing the harness itself (CLAUDE.md files, hooks, agents, skills, settings):
  prefer context over instruction, verification over prescription; never encode what
  the model can infer. Scaffolding must name the model weakness it compensates for.
- Every harness constraint is tracked in the scaffold ledger at
  `~/Projects/claude-obsidian/meta/scaffold-ledger.md`. New scaffolds get an entry
  (weakness + removal test). When the default model changes, review the ledger and
  delete what the new model no longer needs; deletion is the default trajectory.

## Workspaces

- Project work happens in devpods (repo mounted at `/workspaces/<repo>`); on the host,
  repos live flat under `~/Projects/`. Never write project code into `~/Claude/*`
  session directories; those are session scratch only.

## Writing style

- No em dashes (—) or en dashes (–) in any writing: prose, commit messages, replies.
  Use a period, semicolon, colon, comma, or parentheses instead. (En dash allowed
  only for numeric ranges.)

## Git

- Never add a `Co-Authored-By: Claude` trailer or any Claude/Anthropic authorship
  trailer to commits. Authorship stays with the user.

## Code and config style

- Default to zero comments in YAML/JSON manifests and config files. Only keep a
  comment that encodes a genuine non-obvious constraint; put rationale in the
  commit message or vault handoff, not the file.

## Collaboration

- Drive actions directly (edit, apply, restart) rather than narrating steps for the
  user to run, except for destructive or shared-state changes.

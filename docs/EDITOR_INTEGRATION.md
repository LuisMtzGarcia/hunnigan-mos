# Editor & agent integration (Claude Code / VS Code)

This guide wires HUNNIGAN into an AI coding assistant so that **every session, in
every project, automatically knows about your task store** — without you re-explaining
it or passing paths by hand.

It is written for [Claude Code](https://claude.com/claude-code), including its
**VS Code extension**, but the same approach applies to any assistant that can run a
shell command and read files, and that loads a user-level instruction file.

> There is no plugin to install. The assistant already has the shell and file-reading
> tools it needs to drive `mos.py`. "Integration" just means giving every session a
> **stable store location** and **awareness that the store exists**.

## The problem this solves

Two things break the naive setup:

1. **A per-shell `export MOS_ROOT=...` does not persist.** A new terminal or a fresh
   agent session starts with `MOS_ROOT` unset, so `mos.py` falls back to its own
   folder (see `mos.py`) and reads an unrelated, usually empty, store.
2. **A fresh session does not know the store exists.** Asked "what am I working on?",
   the assistant answers from its own conversation memory — finds nothing — and
   reports nothing, even though tasks are safely on disk.

Both are fixed by putting configuration in the assistant's **global tier** so it loads
regardless of which project folder is open.

## Prerequisites

- Claude Code (CLI, or the VS Code / JetBrains extension).
- Python 3.10+ (`mos.py` has no third-party dependencies).
- A local clone of this repository. Note its absolute path to `mos.py`; below it is
  written as `/path/to/hunnigan-mos/mos.py`.

## Step 1 — Choose and initialize a store location

Keep your **data** separate from this **tool** repository. A dedicated home in your
user directory is recommended so the store survives tool updates, re-clones, and moves,
and so private task data never risks being committed to a shared repo.

```sh
# Pick a home for your tasks. $HOME/hunnigan is a good default.
MOS_ROOT="$HOME/hunnigan" python3 /path/to/hunnigan-mos/mos.py init
```

You may instead point `MOS_ROOT` at any project (a per-project store) or omit it to use
the repo's built-in default `.mos/`. A single central store is simplest for tracking
work that spans multiple projects.

## Step 2 — Set `MOS_ROOT` globally

Add an `env` block to your **user-level** settings so every session points at the same
store. For Claude Code this is `~/.claude/settings.json`:

```json
{
  "env": {
    "MOS_ROOT": "/absolute/path/to/your/hunnigan"
  }
}
```

User-level settings load in every workspace, so this replaces the fragile per-shell
`export`.

## Step 3 — Make every session aware of the store

Create a **user-level instruction file** that loads in every project. For Claude Code
this is `~/.claude/CLAUDE.md`. It tells the assistant that the store exists, how to call
it, and when. A minimal version:

```markdown
# Personal task store (HUNNIGAN MOS)

A durable, cross-session task store is the source of truth for what I am working on
across ALL projects — do not rely on chat history for that.

- Command: `python3 /path/to/hunnigan-mos/mos.py <subcommand>`
- Store: `$MOS_ROOT` (set globally). Never pass a different root unless I ask.

When I ask what I'm working on / my status → run `mos.py list` (or `mos.py show <id>`)
and answer from that output, not from memory.
When I narrate real work → record it with `add` / `update` / `complete` / `event`.
For a period summary → `mos.py context day|week|month|year`.

Follow the full contract in /path/to/hunnigan-mos/AGENTS.md.
```

This is the piece that stops a fresh session from answering "nothing tracked" without
ever checking the store. See [`AGENTS.md`](../AGENTS.md) for the complete behavioral
contract to reference or inline.

## Step 4 — Allowlist the command (optional but recommended)

So routine `mos.py` calls do not prompt for permission every time, add the command to
`permissions.allow` in `~/.claude/settings.json`:

```json
{
  "permissions": {
    "allow": [
      "Bash(python3 /path/to/hunnigan-mos/mos.py:*)"
    ]
  }
}
```

## Step 5 — Reload

Global config is read when a session starts. In the VS Code extension, run
**Command Palette → "Developer: Reload Window"** (or restart the editor). Already-open
sessions will not pick up the new files until reloaded.

## Verify

1. **Config loaded** — in the assistant, run `/memory` and confirm your user-level
   `CLAUDE.md` is listed.
2. **Awareness** — ask *"What am I working on?"*. The assistant should run
   `mos.py list` on its own and report your tasks (or that there are none yet).
3. **Capture** — narrate a task ("I'm investigating X, next step is Y"); confirm with
   *"show me that task"*.
4. **Cross-project reload** — open the extension in a **different** project and ask for
   the task's status. It should resolve from the same central store. This is the core
   value: continuity across sessions and projects.
5. **Ground truth** — from any terminal, `python3 /path/to/hunnigan-mos/mos.py list`
   works with no `export`, because `MOS_ROOT` is now global.

## A caveat worth knowing

The user-level `CLAUDE.md` makes the assistant *aware and instructed*, but choosing to
run the command is still its judgment. If a session ever answers from memory instead of
querying the store, the guidance did not fire. For a **hard** trigger, add a Claude Code
hook that runs `mos.py list` at session start and feeds the result into context — a
heavier but deterministic option.

## Scope: global vs. per-project

- **User-level** (`~/.claude/`) applies to every project — best for a personal operator
  that spans repositories.
- **Project-level** (`<project>/.claude/settings.json`, `<project>/CLAUDE.md`) applies
  only to that project — use it to scope a store to one repository, or to override the
  global `MOS_ROOT`.

## Uninstall

Remove the `env` and `permissions` additions from `~/.claude/settings.json`, delete the
task lines from `~/.claude/CLAUDE.md`, and optionally remove the store directory. None
of this touches the repository.

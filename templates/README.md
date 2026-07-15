# Portable Personal Assistant Starter Kit

This directory contains blank, personal-data-free files for starting the same asynchronous task and activity-tracking workflow in another workspace.

## Included files

- `PERSONAL_ASSISTANT.md` — agent mission, invariants, update workflow, reporting rules, and recovery contract.
- `PROFILE.md` — private identity, timezone, work context, and preferences.
- `TASK_INDEX.md` — compact locator for current and archived tasks.
- `TASKS.md` — open/recent task tracker.
- `ACTIVITY_LOG.md` — monthly activity-shard manifest.
- `REFERENCE_MODEL.md` — platform-neutral schema for every external/work location.
- `ROUTINE_MODEL.md` — schema for scheduled, event-driven, and hybrid recurring work.
- `PRIORITIZATION_MODEL.md` — customer-impact assessment, reassessment, and pending-work ordering.
- `STORAGE_MODEL.md` — selective reads, sharding, archives, retention, and reopening.
- `AGENT_HANDOFF_PROMPT.md` — full-context handoff prompt for a new task or recovery.
- `AGENT_ACTIVITY_UPDATE_PROMPT.md` — delta-only prompt for subsequent task updates.
- `gitignore.example` — ignore rules for private runtime files; rename it to `.gitignore` in a standalone copy.
- `activity/ACTIVITY_SHARD_TEMPLATE.md` — template for new monthly event shards.
- `archive/tasks/TASK_ARCHIVE_TEMPLATE.md` — template for yearly completed-task archives.

## Setup

1. Copy the starter files into a new directory while preserving the nested `activity/` and `archive/tasks/` paths.
2. Fill in the bracketed values in `PROFILE.md`.
3. If this is a standalone Git repository, copy `gitignore.example` to `.gitignore` before adding runtime data.
4. Give the assistant this bootstrap instruction:

> Read `PERSONAL_ASSISTANT.md`, `REFERENCE_MODEL.md`, `ROUTINE_MODEL.md`, `PRIORITIZATION_MODEL.md`, and `STORAGE_MODEL.md` completely. Then inspect `PROFILE.md`, `TASK_INDEX.md`, `TASKS.md`, and `ACTIVITY_LOG.md`; validate registered shards and archives without loading unrelated history. Confirm that material updates will keep the task snapshot, index, and matching monthly shard consistent. Do not invent missing task, reference, routine, run, impact, or archive data.

5. Add the first task by providing its goal, current status, known facts, TODOs, dependencies, and every relevant work location. Use `AGENT_HANDOFF_PROMPT.md` when the task already has an AI-agent conversation.

## Daily operation

- Give the assistant task updates in ordinary language or through the delta prompt.
- Ask “What are my current tasks?” for the snapshot.
- Ask “What should I work on next?” for Now/Next/Later ordering based on current customer impact and urgency.
- Ask “What is today's summary?” for outcomes, changes, owned TODOs, dependencies, and stakeholder follow-ups.
- Ask for weekly, monthly, or annual summaries; the assistant must use activity occurrence dates, not file-edit dates.
- Completed one-time tasks remain current for the configured grace period and then move into yearly archives while remaining discoverable through `TASK_INDEX.md`.

## Portability

Back up the directory using an approved private repository or storage system. Restoring the files into another agent workspace is sufficient to continue; chat history is useful but not required.

Do not place credentials, tokens, private customer payloads, or unnecessary personal data in these files.

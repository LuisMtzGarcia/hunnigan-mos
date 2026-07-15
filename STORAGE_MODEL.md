---
schema: personal-assistant-storage-model
schema_version: 1
---

# Storage, Sharding, and Archive Model

This model keeps everyday agent context small without deleting task history or activity evidence.

## Layout

```text
TASKS.md                         # Current active/waiting tasks and recent completions
TASK_INDEX.md                    # Compact locator for every known task
ACTIVITY_LOG.md                  # Activity-shard manifest, not the event store
activity/
  YYYY/
    YYYY-MM.md                   # Immutable monthly event shards
archive/
  tasks/
    YYYY.md                      # Completed task snapshots grouped by completion year
```

Private runtime files and directories remain excluded from a shared repository. Corresponding public starter files live under `templates/`.

## Task snapshot lifecycle

`TASKS.md` contains:

- every Active, Investigating, Changes requested, Ready for review, Waiting, or Blocked task;
- completed tasks still inside the configured grace period;
- recurring parent tasks that remain active after individual runs close.

The default completed-task grace period is 30 calendar days. `PROFILE.md` may override `completed_task_grace_days`.

When a one-time task is completed:

1. Verify that no required work remains.
2. Record the final status, completion date, customer-impact assessment, evidence, completed TODOs, and final references.
3. Move the task to `TASKS.md` → Completed.
4. Append the completion event to the current monthly activity shard.
5. Update `TASK_INDEX.md` with `state: completed`, `completed_on`, and `current_location: TASKS.md`.
6. Keep it in `TASKS.md` through the grace period so recent summaries and corrections remain cheap.

During a weekly/monthly summary, restoration audit, or explicit maintenance request, archive every completion older than the grace period:

1. Copy the complete final task block into `archive/tasks/<completion-year>.md` with a unique `archive_record_id`.
2. Remove the task block from `TASKS.md` only after the archive record exists and validates.
3. Update the index `current_location` to the archive path and add the path to `archive_locations`.
4. Append a system `reference_change` or `system` event only when the archival operation itself is useful to audit; ordinary mechanical archival need not appear in work summaries.

Archiving never means deletion or cancellation.

## Task index

`TASK_INDEX.md` is the first lookup for a task that is not visible in `TASKS.md`. Each entry stores only:

- immutable Task ID and current title;
- current state;
- current impact level;
- completion date when applicable;
- current canonical location;
- prior archive locations when a task has completed more than once;
- last updated date.

The index is a locator, not restart context. The canonical task block remains authoritative.

## Reopening archived work

If new evidence, regression, or required follow-up reopens a completed task:

1. Use `TASK_INDEX.md` to find its most recent completed snapshot.
2. Restore that context as the current task block in the appropriate `TASKS.md` section using the same Task ID.
3. Keep the archived completion snapshot as historical evidence; do not delete or rewrite it.
4. Update the index to `current_location: TASKS.md`, preserve `archive_locations`, clear the current `completed_on`, and set the new state.
5. Append a `status_change` event describing why the task reopened.

Only one location is canonical for current state even when historical archive snapshots exist.

## Activity sharding

`ACTIVITY_LOG.md` is a manifest listing available monthly shards and the current writable shard. Events live in `activity/YYYY/YYYY-MM.md`.

Rules:

1. Select a shard from the event's `occurred_at` month, not its `recorded_at` month.
2. Create a new shard when the first event for a month is recorded.
3. Append events in occurrence order when possible. Late historical events may be appended to an older shard with their true `occurred_at` value.
4. Never rewrite, move, or deduplicate an existing event merely because a newer shard exists. Corrections remain new events with `supersedes`.
5. Update the manifest whenever a shard is created; do not load every shard during ordinary operation.
6. Event IDs remain workspace-unique across all shards.

## Selective reading

- Current tasks or pending work: read `TASKS.md`; consult `TASK_INDEX.md` only for lookup.
- Today/this week: read only shards intersecting the requested dates, then read `TASKS.md` for current TODOs.
- Month: read that month's shard.
- Year/performance review: read the year's shards plus relevant archived/current task snapshots. A generated summary may accelerate review but never replaces source events.
- Task history: resolve the task through the index, then search only the listed task locations and relevant event shards.

Do not load all archives by default.

## Integrity contract

A maintenance or restoration validation must confirm:

- every index Task ID resolves to its `current_location`;
- every live task appears exactly once in `TASK_INDEX.md`;
- archived records have unique `archive_record_id` values;
- every activity shard listed in the manifest exists;
- every event ID is unique across shards;
- event Task IDs resolve through the index;
- event Reference IDs resolve in the current task block or an archived snapshot;
- no completed task is removed from `TASKS.md` before its archive snapshot validates.

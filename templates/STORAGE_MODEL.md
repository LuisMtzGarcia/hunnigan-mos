---
schema: personal-assistant-storage-model
schema_version: 1
---

# Storage, Sharding, and Archive Model

```text
TASKS.md                         # Open work and recent completions
TASK_INDEX.md                    # Compact locator for every task
ACTIVITY_LOG.md                  # Monthly-shard manifest
activity/YYYY/YYYY-MM.md         # Immutable monthly events
archive/tasks/YYYY.md            # Completed task snapshots
```

## Completion and archival

Keep completed one-time tasks in `TASKS.md` for `PROFILE.md`'s `completed_task_grace_days` (default 30 calendar days). Then copy the complete final block into the completion-year archive, validate it, remove it from `TASKS.md`, and update `TASK_INDEX.md`. Archiving is not deletion.

Recurring parent tasks remain current when a run completes; only the run outcome moves to activity history.

## Index

Every Task ID has one entry with title, state, impact level, completion date, canonical current location, historical archive locations, and last update. The index locates context but never replaces the canonical task block.

## Reopening

Restore the latest archived snapshot into `TASKS.md` with the same Task ID, preserve the archive record, point the index back to `TASKS.md`, clear the current completion date, and append a reopening `status_change` event.

## Activity shards

Store an event in the shard matching its `occurred_at` month. `ACTIVITY_LOG.md` lists all shards and identifies the current one. Event IDs remain unique across shards; old events remain immutable; late events may be appended to an older shard.

Read only shards intersecting the requested reporting period. Use yearly shards and relevant task snapshots for annual reviews; generated summaries do not replace source events.

## Integrity

Validate index locations, unique task/archive/event IDs, manifest paths, event Task IDs, event Reference IDs, and archive existence before removing completed work from `TASKS.md`.

---
schema: personal-assistant-task-archive
schema_version: 1
year: YYYY
profile: PROFILE.md
storage_model: STORAGE_MODEL.md
last_updated: null
---

# Completed Task Archive — YYYY

For each eligible completion, append its entire final task block after this metadata:

```yaml
archive_record:
  archive_record_id: task-id-completed-YYYYMMDD-NNN
  task_id: task-id
  completed_on: YYYY-MM-DD
  archived_on: YYYY-MM-DD
  source_location: TASKS.md
```

Keep historical snapshots if a task later reopens.

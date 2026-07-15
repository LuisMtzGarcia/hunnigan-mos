---
schema: personal-assistant-task-index
schema_version: 1
profile: PROFILE.md
storage_model: STORAGE_MODEL.md
last_updated: null
---

# Task Index

Compact task locator. Canonical restart context remains in `TASKS.md` or the path listed by `current_location`.

```yaml
tasks: []
```

Each task entry uses:

```yaml
task_id: stable-lowercase-kebab-id
title: Exact current title
state: active | investigating | changes_requested | ready_for_review | waiting | blocked | completed | cancelled | superseded
impact_level: critical | high | medium | low | none | unknown
completed_on: null
current_location: TASKS.md
archive_locations: []
last_updated: YYYY-MM-DD
```

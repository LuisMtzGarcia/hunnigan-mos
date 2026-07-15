---
schema: personal-assistant-routine-model
schema_version: 1
---

# Recurring Routine Model

Represent repeated operational work as one persistent task plus dated runs. Keep only the current run in `TASKS.md`; append completed run outcomes to the monthly shard registered by `ACTIVITY_LOG.md`.

```yaml
routine:
  routine_id: recurring-operation
  mode: scheduled | event_driven | hybrid
  timezone: PROFILE.md
  schedule:
    expected_days: []
    expected_time: null
    overdue_after: null
  trigger: "[What starts a run]"
  allow_unscheduled_runs: true
  run_id_format: recurring-operation-run-YYYYMMDD-NNN
  item_id_field: external_id
  required_input_fields: [name, external_id, operation]
  allowed_operations: []
  workflow_stages: [intake, execute, verify, report, close]
  completion_rule: Every item is terminal and required reporting is sent
  current_run: null
```

When work arrives, populate `current_run` with a unique Run ID, source Reference IDs, state, stage, item records, per-item blockers/next actions, and reporting status. Recommended run states are `pending`, `active`, `waiting`, `completed`, and `cancelled`.

Expected schedule days mean “check for work,” not “invent a run.” Hybrid routines may also start from surprise intake.

For delayed follow-up work, define a grouped derived task:

```yaml
derived_task:
  group_by: due_on
  one_task_per_group: true
  task_id_format: recurring-operation-followup-YYYYMMDD
  due_rule: Next configured workday after the source event
  required_item_fields: [item_id, name, source_date, due_on, state]
```

Use `PROFILE.md` workdays, create no empty task, and append every item with the same grouping value to one existing task.

Routine activity events add:

```yaml
routine:
  routine_id: recurring-operation
  run_id: recurring-operation-run-20260713-001
  stage: report
  item_ids: []
  counts:
    total: 0
    completed: 0
    blocked: 0
    waiting: 0
```

Use `routine: null` for non-routine events. A run is not complete until every item is terminal and required reporting is sent. Append completed history before clearing `current_run`.

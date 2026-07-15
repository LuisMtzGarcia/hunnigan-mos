---
schema: personal-assistant-routine-model
schema_version: 1
---

# Recurring Routine Model

Use a routine when the same operational workflow repeats over time but individual runs may occur on a schedule, in response to incoming work, or both.

A routine is represented by one persistent task in `TASKS.md`. Do not create a new top-level task for every occurrence. Instead, create a dated Run ID, keep only the current run in the task snapshot, and append completed run outcomes to the monthly activity shard registered by `ACTIVITY_LOG.md`.

## Routine definition

```yaml
routine:
  routine_id: recurring-operation
  mode: hybrid
  timezone: PROFILE.md
  schedule:
    expected_days: [Monday, Tuesday]
    expected_time: null
    overdue_after: null
  trigger: New batch received from the intake reference
  allow_unscheduled_runs: true
  run_id_format: recurring-operation-run-YYYYMMDD-NNN
  item_id_field: external_id
  required_input_fields: [name, external_id, operation]
  allowed_operations: [onboard, cancel]
  workflow_stages: [intake, execute, verify, report, close]
  completion_rule: Every item is terminal and required reporting is sent
  current_run: null
```

### Modes

- `scheduled` — runs are expected at defined times.
- `event_driven` — runs begin only when intake arrives.
- `hybrid` — proactive schedule checks plus unscheduled intake.

An expected day is a check expectation, not proof that work exists. Do not mark a routine overdue merely because no batch arrived unless `overdue_after` explicitly defines that behavior.

## Current run

When work arrives, replace `current_run: null` with:

```yaml
current_run:
  run_id: recurring-operation-run-20260713-001
  triggered_at: 2026-07-13
  source_reference_ids: [recurring-operation-ref-001]
  state: active
  stage: intake
  items:
    - item_id: "12345"
      name: Example item
      operation: onboard
      state: pending
      blocker_category: null
      blocker_notes: null
      next_action: Execute onboarding
      audit:
        required: true
        state: pending
        checked_at: null
        evidence: null
  reporting:
    destination_reference_ids: [recurring-operation-ref-001]
    state: pending
    sent_at: null
```

Recommended run states are `pending`, `active`, `waiting`, `completed`, and `cancelled`. Item states are workflow-specific but should distinguish at least `pending`, `completed`, and `blocked`.

## Run lifecycle

1. **Intake:** Validate every required field and assign a Run ID.
2. **Execute:** Perform the requested operation for each item.
3. **Verify:** Perform any delayed or asynchronous audit required by the operation.
4. **Report:** Send results through the appropriate typed reference.
5. **Close:** Mark the run completed only when all items are terminal and required reporting is sent.

If a run must wait for an asynchronous job or another person, keep it in `current_run`, set its state to `waiting`, record the exact dependency, and move the parent task to `Waiting` only when the owner has no other actionable step.

After completion, append an activity event containing the run summary and set `current_run: null`. Historical item details live in the activity log; the routine definition remains reusable.

## Derived grouped tasks

Some routine items create delayed follow-up work, such as an audit on the next workday. Define a derived-task rule instead of creating one task per item:

```yaml
derived_task:
  group_by: due_on
  one_task_per_group: true
  task_id_format: recurring-operation-followup-YYYYMMDD
  title_format: "Recurring operation follow-ups — YYYY-MM-DD"
  due_rule: Next configured workday after the source event
  required_item_fields: [item_id, name, source_date, due_on, state]
```

All items with the same grouping value must be appended to the same task. Calculate workdays from `PROFILE.md`; do not assume Monday–Friday. If no holiday calendar is configured, apply only the configured weekday rule and accept explicit user corrections for holidays.

Do not create an empty derived task. Create or update it only after a qualifying source item is confirmed. Preserve the source date so reports can distinguish when work happened from when verification occurred.

## Activity integration

Routine events use the standard event schema plus:

```yaml
routine:
  routine_id: recurring-operation
  run_id: recurring-operation-run-20260713-001
  stage: report
  item_ids: ["12345", "67890"]
  counts:
    total: 2
    completed: 1
    blocked: 1
    waiting: 0
```

Use `routine: null` for non-routine events. Period summaries should count completed operational work from run events, not from the persistent task's existence.

## Agent rules

1. Never invent a run because a scheduled check day arrived; confirm whether intake exists.
2. Preserve supplied item identifiers exactly and do not merge items based only on similar names.
3. Derive operation-specific stages only when the routine definition requires them.
4. Record blockers per item with a category, notes, owner, and communication destination when known.
5. Keep stakeholder reporting separate from execution; a technically completed batch is not closed until required reporting is sent.
6. Do not overwrite completed run history. Append its event, then clear the current snapshot.
7. When a routine creates derived work, group items according to the declared rule and never create duplicate tasks for the same grouping key.

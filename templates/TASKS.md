---
schema: personal-assistant-task-snapshot
schema_version: 3
profile: PROFILE.md
task_index: TASK_INDEX.md
storage_model: STORAGE_MODEL.md
last_updated: null
---

# Task Tracker

Purpose: Current open/recent state and restart context. `TASK_INDEX.md` locates all tasks; monthly history is registered by `ACTIVITY_LOG.md`; eligible completions move to `archive/tasks/`. Task IDs and Reference IDs are immutable.

## Active

<!-- Copy this block for an active task, then remove this comment.

### [Task title]

- **Task ID:** `[stable-lowercase-kebab-id]`
- **References:**

  ```yaml
  - reference_id: stable-lowercase-kebab-id-ref-001
    system: "[Exact product, service, tool, or medium]"
    kind: "[Platform-neutral object kind]"
    roles: ["[Why this reference matters]"]
    external_id: null
    title: "[Exact title/name or null]"
    url: null
    access: unknown
    state: active
    locator: "[Fallback location or null]"
    notes: "[Operational context or null]"
  ```
- **Status:** [Accurate current status]
- **People:** [People and roles]
- **Goal:** [Desired outcome and why]
- **Customer impact:**

  ```yaml
  customer_impact:
    level: "[critical / high / medium / low / none / unknown]"
    type: "[direct / indirect / potential / internal-only / none-confirmed / unknown]"
    affected_count: null
    affected_unit: "[users / customers / properties / accounts / jobs / events / other / unknown]"
    denominator: null
    percentage: null
    time_window: "[Measured period or unknown]"
    ongoing: null
    evidence: "[Measurement source, calculation, or why impact is internal-only]"
    confidence: "[confirmed / estimated / inferred / unknown]"
    diagnostic_sql: null
    interpretation: "[How to interpret the measurement/query result or null]"
    last_assessed_on: null
  ```
- **Urgency / priority constraints:** [Deadline, active incident, customer commitment, obligation, work unblocked, or None]
- **Confirmed context:** [Facts required to resume]
- **Decisions:** [Current decisions and rationale]
- **TODO — [short label]:** [Owner and immediate action]
- **Waiting on:** [External dependency or None]
- **Optional follow-up:** [Non-blocking work or None]
- **Resume references:** [Local files, branches, commands, or context not represented by typed references]
- **Stakeholder summary:** [One or two non-technical sentences]
- **Last update:** [YYYY-MM-DD — concise delta]

For recurring work, add a **Routine** YAML block following `ROUTINE_MODEL.md`. Keep only the active `current_run` in this snapshot and preserve completed runs in the monthly shard registered by `ACTIVITY_LOG.md`.

-->

No active tasks yet.

## Waiting

No tasks currently waiting.

## Completed

Keep completed one-time tasks here for `PROFILE.md`'s `completed_task_grace_days`, then archive their validated final blocks through `STORAGE_MODEL.md`.

No completed tasks yet.

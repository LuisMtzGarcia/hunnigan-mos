---
schema: personal-assistant-activity-shard
schema_version: 2
legacy_event_schema_default: 1
profile: PROFILE.md
created_on: null
mode: append-only
period: YYYY-MM
---

# Activity Log — YYYY-MM

Append immutable events whose `occurred_at` falls in this month. Register this file in `ACTIVITY_LOG.md`.

## Event schema

```yaml
event_schema_version: 2
event_id: evt-YYYYMMDD-NNN
task_ids: [stable-task-id]
reference_ids: []
occurred_at: YYYY-MM-DD
recorded_at: YYYY-MM-DD
time_precision: date | minute | second
event_type: task_created | progress | outcome | decision | impact_reassessment | status_change | todo_change | reference_change | communication | review | blocker | correction | system
significance: routine | notable | major
summary: One factual sentence describing the delta.
details: []
status_before: null
status_after: null
todo_added: []
todo_completed: []
waiting_on_after: []
people: []
artifacts: []
communication: null
routine: null
impact:
  category: reliability | customer_support | delivery | quality | productivity | team_enablement | process | other
  scope: individual | team | customer | multi_customer | organization
  evidence: []
source:
  kind: user_update | agent_handoff | assistant_observation | imported_history
  reference: null
confidence: confirmed | inferred
supersedes: null
reporting:
  daily: true
  weekly: true
  monthly: true
  annual: false
```

## Events

<!-- Add date headings and events. Never rewrite prior events; corrections supersede them. -->

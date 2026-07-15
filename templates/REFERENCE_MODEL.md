---
schema: personal-assistant-reference-model
schema_version: 2
---

# Platform-Neutral Reference Model

Represent every external work location as a typed reference rather than a vendor-specific field. This supports support portals, ticket trackers, chat tools, email, source control, documents, dashboards, AI work sessions, and systems that do not provide stable URLs.

## Schema

```yaml
reference_id: example-task-ref-001
system: Freshdesk
kind: support_ticket
roles: [intake, stakeholder_updates]
external_id: "12345"
title: Customer-reported delivery issue
url: https://support.example.com/tickets/12345
access: restricted
state: active
locator: null
notes: Primary destination for customer-facing updates
```

Use `{task-id}-ref-{NNN}` for immutable, workspace-unique `reference_id` values. Unknown values are `null`, never guessed. A URL is optional when the system plus `external_id` or `locator` can recover the object.

Recommended `kind` values include `agent_conversation`, `conversation`, `email_thread`, `support_ticket`, `issue`, `incident`, `pull_request`, `merge_request`, `document`, `specification`, `dashboard`, `dataset`, `repository`, `meeting`, and `other`.

Recommended `roles` include `intake`, `work_session`, `work_tracking`, `discussion`, `stakeholder_updates`, `approval`, `implementation`, `review`, `evidence`, `documentation`, `monitoring`, and `other`. Roles may be combined and extended.

`access` is one of `public`, `organization`, `restricted`, `private`, `local`, or `unknown`. It documents visibility but does not grant authorization. Never store credentials or tokens.

`state` is one of `active`, `closed`, `superseded`, or `unknown`. Retain closed and superseded references for history and describe a successor in `notes` when applicable.

## Activity integration

Version 2 events use stable references:

```yaml
event_schema_version: 2
event_type: communication
task_ids: [example-task]
reference_ids: [example-task-ref-001]
communication:
  direction: outbound
  purpose: status_update
  participants: [Customer contact]
  follow_up_required: true
  follow_up_owner: Workspace owner
```

For non-communication events, set `communication: null`.

Legacy events with untyped `artifacts` remain valid and immutable. New events must use `event_schema_version: 2` and cite `reference_ids` whenever a matching task reference exists.

## Agent rules

1. Preserve supplied values exactly.
2. Assign the next unused reference ID for the task.
3. Infer type, roles, access, and state only when unambiguous; otherwise use `other` or `unknown` and describe the uncertainty.
4. Deduplicate by canonical URL or system plus external ID within each task.
5. Never rename a reference ID.
6. Update mutable reference metadata in `TASKS.md` and append a `reference_change` event.
7. Use `stakeholder_updates`, `approval`, and `review` references when producing follow-up reminders.

If one external object applies to multiple tasks, assign a separate task-prefixed reference to each task so each remains independently resumable.

---
schema: personal-assistant-reference-model
schema_version: 2
---

# Platform-Neutral Reference Model

Tasks often span several systems: a support case creates an engineering issue, implementation produces a pull request, review happens in a chat, and the resolution is posted back to the requester. The Personal Assistant represents all of these as typed references instead of using vendor-specific task fields.

## Reference object

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

### Required fields

- `reference_id` — immutable and unique across the workspace. Use `{task-id}-ref-{NNN}`.
- `system` — product, service, repository host, local tool, or communication medium. It is free text and must not be restricted to a vendor list.
- `kind` — what the referenced object is.
- `roles` — why the reference matters to this task. One reference may serve multiple roles.
- `external_id` — native identifier when one exists; otherwise `null`.
- `title` — short factual label; otherwise `null`.
- `url` — canonical URL when available; otherwise `null`.
- `access` — expected visibility/access boundary.
- `state` — whether the referenced object is currently active, closed, superseded, or unknown.
- `locator` — fallback instructions for finding the object when a stable URL is unavailable; otherwise `null`.
- `notes` — concise operational context; otherwise `null`.

Unknown values must be `null`, never guessed. A reference is valid without a URL when its system plus external ID or locator is sufficient to recover it.

## Recommended kinds

Use these when they fit; add a clear lowercase snake-case kind when they do not:

- `agent_conversation`
- `conversation`
- `email_thread`
- `support_ticket`
- `issue`
- `incident`
- `pull_request`
- `merge_request`
- `change_request`
- `document`
- `specification`
- `dashboard`
- `dataset`
- `repository`
- `meeting`
- `other`

Kinds describe the object, not the vendor. For example, Jira and Linear both commonly use `issue`; GitHub commonly uses `pull_request`; GitLab commonly uses `merge_request`.

## Recommended roles

Roles are extensible and may be combined:

- `intake` — where the request originated.
- `work_session` — AI or human workspace used to perform/resume the work.
- `work_tracking` — canonical ticket or work item.
- `discussion` — ongoing technical or stakeholder conversation.
- `stakeholder_updates` — destination for progress or resolution messages.
- `approval` — location or artifact holding required approval.
- `implementation` — code change or delivery artifact.
- `review` — location where feedback/review occurs.
- `evidence` — artifact supporting a finding or outcome.
- `documentation` — durable background or handoff.
- `monitoring` — operational status, alerts, or dashboards.
- `other` — purpose does not fit the recommended vocabulary; clarify in `notes`.

## Access values

- `public` — accessible without organization-specific authorization.
- `organization` — generally accessible to members of an organization/workspace.
- `restricted` — limited to a subset of users, a customer portal, or a permissioned group.
- `private` — direct message, private correspondence, or personally scoped resource.
- `local` — available only in the current device, editor, or assistant workspace.
- `unknown` — access boundary has not been confirmed.

Access metadata is descriptive, not an authorization mechanism. Never store credentials or access tokens.

## State values

- `active` — currently relevant for work, updates, approval, or resumption.
- `closed` — completed or closed externally but retained as evidence/history.
- `superseded` — replaced by another reference; explain the successor in `notes`.
- `unknown` — external state has not been confirmed.

## Multi-system example

```yaml
references:
  - reference_id: delivery-retry-ref-001
    system: Freshdesk
    kind: support_ticket
    roles: [intake, stakeholder_updates]
    external_id: "12345"
    title: Partner delivery failures
    url: https://support.example.com/tickets/12345
    access: restricted
    state: active
    locator: null
    notes: Post customer-safe updates here

  - reference_id: delivery-retry-ref-002
    system: Jira
    kind: issue
    roles: [work_tracking]
    external_id: ENG-123
    title: Retry partner delivery failures
    url: https://issues.example.com/browse/ENG-123
    access: organization
    state: active
    locator: null
    notes: Canonical engineering work item

  - reference_id: delivery-retry-ref-003
    system: GitHub
    kind: pull_request
    roles: [implementation, review]
    external_id: "#456"
    title: Retry non-successful delivery responses
    url: https://github.example.com/org/repo/pull/456
    access: organization
    state: active
    locator: null
    notes: null

  - reference_id: delivery-retry-ref-004
    system: Microsoft Teams
    kind: conversation
    roles: [discussion, approval]
    external_id: null
    title: Delivery retry review
    url: null
    access: private
    state: active
    locator: Engineering team > Integrations channel > July 13 review thread
    notes: Stable URL unavailable; use the locator
```

## Activity-log integration

Version 2 activity events link back to task references through `reference_ids`. Communication events add structured metadata:

```yaml
event_schema_version: 2
event_type: communication
task_ids: [delivery-retry]
reference_ids: [delivery-retry-ref-001]
communication:
  direction: outbound
  purpose: status_update
  participants: [Customer contact]
  follow_up_required: true
  follow_up_owner: Workspace owner
```

Recommended communication directions are `inbound`, `outbound`, and `internal`. Recommended purposes include `intake`, `status_update`, `review_request`, `review_feedback`, `approval_request`, `approval_response`, `resolution`, and `other`.

For non-communication events, set `communication: null`.

## Agent behavior

When ingesting a reference:

1. Preserve the exact supplied system, external ID, title, URL, and locator.
2. Assign the next unused reference ID for the task.
3. Infer `kind`, `roles`, `access`, and `state` only when the supplied context makes them unambiguous; otherwise use `other` or `unknown` and state the uncertainty in `notes`.
4. Within one task, reuse an existing reference instead of creating a duplicate when system, external ID, or canonical URL matches.
5. Never change a `reference_id`. Update mutable metadata in the task snapshot and append a `reference_change` activity event.
6. Use references with `stakeholder_updates`, `approval`, or `review` roles to generate actionable follow-up reminders.

When the same external object applies to multiple tasks, give each task its own task-prefixed reference. This keeps every task independently resumable and lets cross-task activity events cite all applicable Reference IDs.

## Backward compatibility

Activity events created before schema version 2 may contain only untyped `artifacts`. They remain immutable and valid as legacy events. Readers should use their raw artifacts plus the task's current typed references. New events must use `event_schema_version: 2` and `reference_ids` whenever a matching typed reference exists.

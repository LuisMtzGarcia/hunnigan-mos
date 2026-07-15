# Agent Task Handoff Prompt

```text
Create a concise, restart-safe handoff for my personal task tracker.

Use this structure:

**Task:** [Short name]
**Existing task ID:** [Stable ID or “New task — assistant must assign.”]

**References:**
[Repeat for the AI work session, request source, support case, tracker item, discussion, approval, delivery/review artifact, documentation, or evidence.]

- **Reference ID:** [Existing ID or “New reference — assistant must assign.”]
  **System:** [Exact tool/service]
  **Kind:** [Object type]
  **Roles:** [Operational purpose]
  **External ID:** [Native ID or “None”]
  **Title:** [Exact title or “Unknown”]
  **URL:** [Exact URL or “None”]
  **Access:** [public / organization / restricted / private / local / unknown]
  **State:** [active / closed / superseded / unknown]
  **Locator:** [Fallback location or “None”]
  **Notes:** [Why it matters or “None”]

**Goal:** [Desired outcome and why]
**People involved:** [Requester, owner, reviewers, approvers, dependencies]
**Relevant examples or identifiers:** [Useful non-reference identifiers]
**Current status:** [Accurate state]
**Customer impact:**
- **Impact level:** [critical / high / medium / low / none / unknown]
- **Impact type:** [direct / indirect / potential / internal-only / none-confirmed / unknown]
- **Affected scale:** [Approximate count plus unit and denominator/percentage when useful, or “Unknown — measurement required.”]
- **Time window:** [Measured period or “Unknown”]
- **Ongoing:** [yes / no / unknown]
- **Evidence / confidence:** [Source plus confirmed/estimated/inferred confidence; show estimate calculation]
- **Impact diagnostic:** [“Not needed” or safe read-only aggregate SQL plus a one-sentence interpretation]
**Urgency / priority constraints:** [Deadline, incident, commitment, obligation, work unblocked, or “None known”; do not assign global priority without the complete task list]
**Recurring routine:** [“None” or mode, schedule, trigger, item schema, operations, stages, grouped derived-task rules, completion rule, reporting references, and current run following ROUTINE_MODEL.md]
**Changes since the previous summary:** [Dated material deltas]
**What we know:** [Confirmed restart-critical facts]
**Work completed:** [Verified work]
**Decisions made:** [Decision and rationale]
**TODOs / next steps:** [Action and owner]
**Waiting on / blockers:** [Dependency and owner or “None”]
**Where to resume:** [Only local context not covered by references]
**Stakeholder summary:** [One or two non-technical sentences]
**Last updated:** [Exact date/timezone when known]

Rules:
- Prefer fewer than 500 words excluding diagnostic SQL.
- Include all references needed to find intake, resume work, review delivery, or send updates.
- References may use an ID or locator instead of a URL.
- Do not invent a recurring run merely because a scheduled check day arrived.
- Distinguish facts from inference and progress from completion.
- Customer impact is separate from priority/severity. Use the most meaningful unit (users, customers, properties, accounts, jobs, events, etc.) and label internal-only or potential impact accurately.
- Follow `PRIORITIZATION_MODEL.md` for impact levels and reassessment when available.
- Include the impact time window, evidence, confidence, and denominator/percentage when useful. Never invent an impact metric.
- If impact is unknown and measurable from data, inspect the available schema and include safe, read-only aggregate SQL with explicit time bounds, no row-level PII, and an interpretation. Prefer numerator, denominator, and percentage.
- Never invent tables or columns. If schema is unavailable, include an executable metadata-discovery query and identify the mappings still required for the final aggregate query.
- Never invent IDs, names, URLs, locators, people, dates, metrics, access, or status.
- Do not include secrets, credentials, tokens, or private payloads.
- Return only the completed handoff.
```

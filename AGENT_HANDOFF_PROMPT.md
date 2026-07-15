# Agent Task Handoff Prompt

Copy this prompt into the AI work session handling the task:

```text
Create a concise handoff summary for my personal task tracker.

Include enough context for a new agent to resume if this conversation disappears. Avoid lengthy logs and implementation details that are not required for restart.

Use this exact structure:

**Task:** [Short task name]

**Existing task ID:**
[Stable task ID if supplied; otherwise “New task — assistant must assign.”]

**References:**
[Repeat the following group for every relevant location or artifact: the current AI conversation, request source, support case, work-tracking item, discussion, approval, implementation/review artifact, document, dashboard, or other restart reference.]

- **Reference ID:** [Existing stable ID or “New reference — assistant must assign.”]
  **System:** [Exact product/service/tool name]
  **Kind:** [agent_conversation / conversation / email_thread / support_ticket / issue / incident / pull_request / merge_request / document / dashboard / other]
  **Roles:** [intake / work_session / work_tracking / discussion / stakeholder_updates / approval / implementation / review / evidence / documentation / monitoring / other]
  **External ID:** [Native ID or “None”]
  **Title:** [Exact title/name or “Unknown”]
  **URL:** [Exact canonical URL or “None”]
  **Access:** [public / organization / restricted / private / local / unknown]
  **State:** [active / closed / superseded / unknown]
  **Locator:** [Fallback search/location instructions when no stable URL exists, or “None”]
  **Notes:** [Why this reference matters, or “None”]

**Goal:**
[What we are trying to accomplish and why]

**People involved:**
[Who requested/reported it and anyone whose work, input, review, or approval is needed]

**Relevant examples or identifiers:**
[Customer, property, record, service, dataset, or other useful identifiers not already captured as references]

**Current status:**
[Active / Investigating / Changes requested / Waiting / Blocked / Ready for review / Completed]

**Customer impact:**
- **Impact level:** [critical / high / medium / low / none / unknown]
- **Impact type:** [direct / indirect / potential / internal-only / none-confirmed / unknown]
- **Affected scale:** [Approximate count and unit, such as users, customers, properties, accounts, jobs, or events; include denominator/percentage when useful, or “Unknown — measurement required.”]
- **Time window:** [Period covered by the estimate or “Unknown”]
- **Ongoing:** [yes / no / unknown]
- **Evidence / confidence:** [Observed source and confirmed/estimated/inferred confidence; show the calculation for an estimate]
- **Impact diagnostic:** [“Not needed” when impact is measured or demonstrably internal-only. Otherwise include a read-only aggregate SQL query and a one-sentence explanation of how to interpret its result.]

**Urgency / priority constraints:**
[Deadline, active incident, customer commitment, compliance/contractual obligation, work this task unblocks, or “None known.” Do not assign global priority without seeing the other tracked tasks.]

**Recurring routine:**
[Write “None” for one-time work. Otherwise provide the routine mode, expected check schedule, trigger, allowed unscheduled runs, required item fields, operations, stages, any grouped derived-task rule, completion rule, reporting destination Reference IDs, and current run. Follow ROUTINE_MODEL.md and never invent a run or empty derived task solely because a check day arrived.]

**Changes since the previous summary:**
- [Material outcome, decision, review, communication, blocker, or status change]
- [Include when each change occurred if known]

**What we know:**
- [Important confirmed fact]

**Work completed:**
- [What has already been investigated, changed, or verified]

**Decisions made:**
- [Decision and why it was made]

**TODOs / next steps:**
- [Immediate action and owner]

**Waiting on / blockers:**
[Person, approval, implementation, external system, or “None”]

**Where to resume:**
[Relevant local files, branches, commands, code areas, or other context not already represented by a typed reference]

**Stakeholder summary:**
[One or two non-technical sentences explaining the current situation]

**Last updated:**
[Exact date and timezone when known]

Rules:
- Keep the summary concise, preferably under 500 words excluding diagnostic SQL.
- Prioritize current state, conclusions, decisions, blockers, and next steps.
- Clearly distinguish confirmed facts from assumptions and progress from completion.
- Treat customer impact as a distinct task attribute, not as task priority or technical severity. Internal observability work may have `internal-only` or `potential` impact even when it improves incident diagnosis.
- Apply the impact levels and reassessment rules from `PRIORITIZATION_MODEL.md` when that file is available.
- Use the most meaningful affected unit available; do not force a “user” count when customers, properties, accounts, jobs, or events better represent the scope.
- If an impact number is available in the conversation or evidence, report it with its time window, denominator when useful, source, and confidence. Label approximations and show their calculation.
- If customer impact is unknown and data can answer it, inspect the available schema and provide a safe, read-only aggregate SQL query. Prefer a numerator, denominator, and percentage; use explicit time bounds; avoid row-level PII; state the SQL dialect/data source when known; and explain what result would establish the scale.
- Never invent tables or columns. If the schema cannot be confirmed, provide an executable metadata-discovery query first and clearly identify the remaining table/column mappings needed for the final aggregate query.
- Include every reference needed to find the original request, resume work, review delivery, or send updates.
- For recurring work, distinguish the durable routine definition from the current dated run.
- A reference may have no URL; preserve its system, native ID, title, or locator instead.
- Never invent task/reference IDs, system names, conversation names, URLs, locators, people, dates, metrics, or status.
- Label private or restricted references accurately.
- Do not include credentials, tokens, private payloads, or unnecessary sensitive data.
- Return only the completed summary, with no introduction or closing comments.
```

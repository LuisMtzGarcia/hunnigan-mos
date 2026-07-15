# Agent Activity Update Prompt

Use this prompt when a task is already tracked and only its changes need to be recorded:

```text
Create a concise delta update for my personal task tracker and append-only activity log.

Report only what changed since the previous handoff. The receiving assistant already has the task's full current snapshot.

Use this exact structure:

**Task:** [Exact tracked task title]

**Task ID:**
[Stable task ID supplied by the user. If unavailable, write “Unknown — assistant must resolve from exact references.”]

**Update period:**
[Start/end date and timezone when known; otherwise the most precise known date]

**Status before:**
[Previous status or “Unknown”]

**Status now:**
[Current status]

**Outcomes / changes:**
- [Concrete result, diagnosis, implementation, merge, deployment, verification, review, communication, or blocker]
- [State what changed and when; do not call progress “completed”]

**Evidence:**
- [Test result, production observation, measurement, or stable reference ID]

**Reference changes:**
[For each new or changed reference, repeat:]

- **Action:** [add / update / supersede / close]
  **Reference ID:** [Existing ID or “New reference — assistant must assign.”]
  **System:** [Exact product/service/tool name]
  **Kind:** [Object type]
  **Roles:** [Why it matters]
  **External ID:** [Native ID or “None”]
  **Title:** [Exact title/name or “Unknown”]
  **URL:** [Exact URL or “None”]
  **Access:** [public / organization / restricted / private / local / unknown]
  **State:** [active / closed / superseded / unknown]
  **Locator:** [Fallback locator or “None”]
  **Notes:** [Delta or operational context]

**Routine update:**
[Write “None” for non-routine work. Otherwise include Routine ID, Run ID, trigger date, current stage/state, affected item IDs, completed/blocked/waiting counts, per-item blockers or next actions, reporting state, and any grouped derived task ID/due date. Do not create a run without confirmed intake.]

**Decisions made:**
- [Decision and brief reason]

**TODOs completed:**
- [Previously open action now complete]

**TODOs added or still open:**
- [Next action and owner]

**Waiting on:**
- [Person/system, exact dependency, and whether follow-up is needed]

**Communication:**
- **Direction:** [inbound / outbound / internal]
  **Purpose:** [intake / status_update / review_request / review_feedback / approval_request / approval_response / resolution / other]
  **Reference ID:** [Destination/source reference ID or “New reference — assistant must assign.”]
  **Participants:** [People or groups]
  **Follow-up required:** [yes / no]
  **Follow-up owner:** [Person or “None”]

**Where to resume:**
[Only new or changed local references]

**Impact:**
- **Impact level:** [critical / high / medium / low / none / unknown]
- **Impact type:** [direct / indirect / potential / internal-only / none-confirmed / unknown]
- **Affected scale:** [Updated approximate count and unit, denominator/percentage when useful, or “Unknown — measurement required.”]
- **Time window:** [Period represented by the measurement]
- **Ongoing:** [yes / no / unknown]
- **Evidence / confidence:** [Source and confirmed/estimated/inferred confidence; show estimate calculation]
- **Impact diagnostic:** [“Not needed,” the existing query/reference, or safe read-only aggregate SQL plus interpretation when still unknown]

**Urgency / priority changes:**
[New or removed deadline, incident state, customer commitment, obligation, or unblocking effect; otherwise “None.”]

Rules:
- Keep the update under 350 words unless multiple distinct outcomes require more space.
- Report deltas, not the full task history.
- Use “None” for sections with no changes.
- A reference does not require a URL if its system plus external ID or locator can recover it.
- For recurring work, report the current Run ID and delta rather than repeating the entire routine definition.
- Never invent dates, IDs, system names, titles, URLs, locators, people, metrics, access, or status.
- Keep customer impact separate from task priority and technical severity. Use the most meaningful affected unit and label internal-only or potential impact accurately.
- When evidence changes the credible impact, state the previous and new classifications so the receiving assistant can append an `impact_reassessment` event and rerank the task using `PRIORITIZATION_MODEL.md`.
- When impact remains unknown, inspect known schema and provide safe, read-only aggregate SQL with explicit time bounds, no row-level PII, and an explanation of the result. Never invent tables/columns; use metadata discovery when schema is unavailable.
- Distinguish facts from inference and progress from completion.
- Return only the completed delta, with no introduction or closing comments.
```

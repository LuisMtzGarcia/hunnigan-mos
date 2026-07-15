# Agent Activity Update Prompt

```text
Create a concise delta update for my current task snapshot and append-only activity log. Report only what changed.

**Task:** [Exact title]
**Task ID:** [Stable ID or “Unknown — assistant must resolve from references.”]
**Update period:** [Most precise known date/timezone]
**Status before:** [Previous status or “Unknown”]
**Status now:** [Current status]
**Outcomes / changes:** [Dated concrete deltas]
**Evidence:** [Measurements, observations, or stable reference IDs]

**Reference changes:**
- **Action:** [add / update / supersede / close]
  **Reference ID:** [Existing ID or “New reference — assistant must assign.”]
  **System:** [Exact tool/service]
  **Kind:** [Object type]
  **Roles:** [Purpose]
  **External ID:** [Native ID or “None”]
  **Title:** [Exact title or “Unknown”]
  **URL:** [Exact URL or “None”]
  **Access:** [public / organization / restricted / private / local / unknown]
  **State:** [active / closed / superseded / unknown]
  **Locator:** [Fallback or “None”]
  **Notes:** [Delta or context]

**Routine update:** [“None” or Routine ID, Run ID, trigger, stage/state, item IDs, counts, blockers/next actions, reporting state, and grouped derived task ID/due date]

**Decisions made:** [Decision and reason]
**TODOs completed:** [Completed actions]
**TODOs added or still open:** [Action and owner]
**Waiting on:** [Dependency and follow-up]

**Communication:**
- **Direction:** [inbound / outbound / internal]
  **Purpose:** [status_update / review_request / review_feedback / approval / resolution / other]
  **Reference ID:** [Stable or new]
  **Participants:** [People/groups]
  **Follow-up required:** [yes/no]
  **Follow-up owner:** [Person or “None”]

**Where to resume:** [Only changed local context]
**Impact:**
- **Impact level:** [critical / high / medium / low / none / unknown]
- **Impact type:** [direct / indirect / potential / internal-only / none-confirmed / unknown]
- **Affected scale:** [Updated count/unit and denominator/percentage when useful, or “Unknown — measurement required.”]
- **Time window:** [Measured period]
- **Ongoing:** [yes / no / unknown]
- **Evidence / confidence:** [Source and confirmed/estimated/inferred confidence]
- **Impact diagnostic:** [“Not needed,” existing query/reference, or safe read-only aggregate SQL plus interpretation]
**Urgency / priority changes:** [Deadline, incident, commitment, obligation, unblocking change, or “None”]

Rules:
- Prefer fewer than 350 words.
- Use “None” for empty sections.
- A reference may use an ID/locator instead of a URL.
- Do not create a routine run without confirmed intake.
- Customer impact is separate from priority/severity. Use the most meaningful unit and label internal-only or potential impact accurately.
- When evidence changes impact, provide the before/after classification so the assistant can append an `impact_reassessment` event and rerank it through `PRIORITIZATION_MODEL.md`.
- If impact is unknown, inspect known schema and provide safe read-only aggregate SQL with explicit time bounds and no row-level PII. Never invent tables/columns; use metadata discovery if schema is unavailable.
- Never invent facts or claim progress as completion.
- Return only the completed delta.
```

# Impact-Based Prioritization Model

Use this model whenever the owner asks what they should work on, what is pending for them, or which task should come next. Customer impact is a living evidence-based assessment, not a permanent label inherited from intake.

## Principles

1. Rank only work the owner can act on now. Put dependencies owned by other people or systems in a separate **Waiting** section unless the owner has a concrete follow-up due.
2. Customer impact is the primary ordering signal among otherwise actionable work, but urgency, deadlines, incident containment, compliance commitments, and the ability to unblock others may override it.
3. Keep customer impact separate from technical severity, implementation difficulty, stakeholder anxiety, and task age.
4. Unknown impact is not low impact. If credible evidence suggests material exposure, prioritize measuring or containing it until evidence supports a lower classification.
5. Never preserve an alarming intake estimate after investigation disproves it. Update the current assessment and retain the transition in `ACTIVITY_LOG.md`.

## Current task assessment

Store this block in each task when impact information is available:

```yaml
customer_impact:
  level: critical | high | medium | low | none | unknown
  type: direct | indirect | potential | internal-only | none-confirmed | unknown
  affected_count: null
  affected_unit: users | customers | properties | accounts | jobs | events | other | unknown
  denominator: null
  percentage: null
  time_window: null
  ongoing: null
  evidence: null
  confidence: confirmed | estimated | inferred | unknown
  diagnostic_sql: null
  interpretation: null
  last_assessed_on: YYYY-MM-DD
```

Use the unit that best represents actual exposure. Do not translate properties, jobs, or events into “users” without evidence. A zero must identify exactly what was measured; for example, `0 of 164 reported properties overlapped the confirmed scan gap`.

## Impact levels

- **critical:** Broad or severe confirmed customer harm requiring immediate containment.
- **high:** Confirmed material harm to multiple customers/entities, or a serious ongoing failure with meaningful exposure.
- **medium:** Confirmed limited harm, degraded behavior, or a material potential impact with bounded exposure.
- **low:** Minor, narrow, historical, or non-urgent customer effect.
- **none:** Evidence confirms no customer-facing effect for the task's reported scope; work may still improve reporting, clarity, or internal correctness.
- **unknown:** Evidence is insufficient. Preserve the plausible risk and create a measurement action.

These are operational guidelines, not mathematical thresholds. Record the evidence and unit so the ranking remains explainable.

## Focus ordering

When presenting the owner's pending work, group it as follows:

1. **Now**
   - Actionable containment or remediation for confirmed critical/high ongoing customer impact.
   - Imminent commitments where delay would create material customer, compliance, or operational harm.
   - A concrete measurement step for unknown impact when a major outage remains plausible.
2. **Next**
   - Actionable medium customer impact.
   - High potential impact that is not currently confirmed or ongoing.
   - Time-sensitive review feedback, stakeholder commitments, or work that unblocks delivery.
3. **Later**
   - Low or no confirmed customer impact without an imminent deadline.
   - Internal-only diagnostics, observability, reporting corrections, documentation, and process improvements.
4. **Waiting**
   - No owner action is currently possible. Show the dependency and any follow-up date/action separately.

Within a group, order by: nearest meaningful deadline, ongoing versus historical impact, affected scale, evidence confidence, ability to unblock other work, and then oldest explicit commitment. Use effort only as a tie-breaker; do not let a quick low-impact task silently outrank active customer harm.

For every ranked item, state the next action and a one-sentence reason for its placement. Do not present a fabricated numeric score.

## Unknown-impact measurement

When impact is unknown and data can answer it:

1. Use the handoff's diagnostic SQL or inspect confirmed schemas.
2. Prefer read-only aggregate SQL that returns an affected numerator, relevant denominator, percentage, and explicit time window.
3. Avoid row-level PII and unbounded scans where practical.
4. Never invent tables or columns. If schema is unavailable, run or provide metadata discovery first and identify the missing mappings.
5. Keep the task's impact `unknown` until results are supplied; do not treat query generation as measurement completion.

## Reassessment workflow

Reassess impact whenever investigation, production verification, stakeholder clarification, a diagnostic query, deployment, or recurrence changes the credible scope.

1. Record the previous assessment and new evidence.
2. Update the task's `customer_impact` block to current truth, including `last_assessed_on`.
3. Add, complete, or remove the impact-measurement TODO as supported by evidence.
4. Append an `impact_reassessment` event to the monthly shard selected through `ACTIVITY_LOG.md`, with the before/after classification and measurement evidence. Do not rewrite the original intake event.
5. Recompute where the task belongs the next time pending work is ranked.

A downgrade does not cancel remaining work. It changes focus: for example, a report query can still need correction after evidence shows that the apparent outage did not affect the reported customers.

## Default response to “What should I work on?”

Return:

1. **Now** — highest-impact actionable work.
2. **Next** — important work to pick up afterward.
3. **Later** — lower-impact maintenance and internal improvements.
4. **Waiting** — external dependencies plus any owner follow-up.
5. **Impact unknown** — only when measurement actions need special visibility and are not already in Now/Next.

Mention missing impact evidence explicitly. Never imply that file order, task age, or an alarming original report determines current priority.

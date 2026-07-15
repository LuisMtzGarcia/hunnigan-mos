# Impact-Based Prioritization Model

Use this model when the owner asks what to work on or which pending task comes next. Customer impact is a current evidence-based assessment and may change after investigation.

## Task impact

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

Use the most meaningful unit and identify exactly what a zero or estimate measures. Do not convert properties, jobs, or events into users without evidence.

## Ordering

Rank only owner-actionable work:

1. **Now:** confirmed critical/high ongoing harm; imminent commitments whose delay creates material harm; or a concrete measurement/containment step while a major outage remains plausible.
2. **Next:** medium impact; high potential but unconfirmed/non-ongoing impact; time-sensitive reviews, commitments, or work that unblocks delivery.
3. **Later:** low/no confirmed impact and internal-only diagnostics, reporting fixes, documentation, or process work without an imminent deadline.
4. **Waiting:** another person/system owns the next action; show any owner follow-up separately.

Within a group, use deadline, ongoing scope, affected scale, confidence, ability to unblock work, then oldest commitment. Effort is only a tie-breaker. Give a one-sentence placement reason; do not fabricate a numeric score.

Unknown does not mean low. If credible material exposure remains, prioritize safe read-only aggregate SQL or containment. Require an affected numerator, useful denominator/percentage, explicit time bounds, no row-level PII, and confirmed table/column names. Use metadata discovery when schema is unavailable.

## Reassessment

When evidence changes:

1. Update the task's current impact block and `last_assessed_on`.
2. Update the measurement TODO.
3. Append an `impact_reassessment` event to the matching monthly activity shard with before/after classification and evidence; never rewrite intake history.
4. Recompute focus placement on the next priority request.

A downgrade changes focus but does not erase remaining work. A wrong report query can remain actionable even after the apparent customer outage is disproven.

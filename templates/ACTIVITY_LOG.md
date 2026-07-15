---
schema: personal-assistant-activity-manifest
schema_version: 1
profile: PROFILE.md
storage_model: STORAGE_MODEL.md
current_shard: null
last_updated: null
---

# Activity Log Manifest

This file lists immutable monthly event shards. Do not place events directly here.

```yaml
shards: []
```

On the first material event, create `activity/YYYY/YYYY-MM.md` from `activity/ACTIVITY_SHARD_TEMPLATE.md`, register it here, and set `current_shard`.

Follow `STORAGE_MODEL.md`: choose shards from `occurred_at`, keep Event IDs globally unique, update counts/bounds after writes, and never delete shards containing events.

# MOS Agent Bootstrap

Use `python3 mos.py`; do not edit generated `TASKS.md` or scan raw event history.

1. Run `python3 mos.py list` for current work.
2. Run `python3 mos.py show <task-id>` before updating one task.
3. Use `add`, `update`, `complete`, or `event`; each mutation records one compact delta and regenerates the human view.
4. Use `python3 mos.py context day|week|month|year` for period reports. Read only the returned packet.
5. Preserve exact names, IDs, URLs, dates, and supplied facts. Unknown values remain unknown.
6. Rank owner-actionable work by current impact and urgency. Keep work waiting on others separate.
7. Keep confirmations short. Do not record routine chatter or MOS bookkeeping as activity.

Canonical private state is under `.mos/`: `index.tsv`, one JSON file per task, and monthly JSONL events. `TASKS.md` is the generated human/offline view. Run `python3 mos.py verify` after repairs, not after every read.

#!/usr/bin/env python3
"""Portable, dependency-free storage engine for the MOS workspace."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(os.environ.get("MOS_ROOT", Path(__file__).resolve().parent)).resolve()
STORE = ROOT / ".mos"
TASK_DIR = STORE / "tasks"
EVENT_DIR = STORE / "events"
CONFIG_PATH = STORE / "config.json"
INDEX_PATH = STORE / "index.tsv"
TASK_VIEW_PATH = ROOT / "TASKS.md"
INDEX_HEADER = ["id", "state", "impact", "due", "owner", "updated", "path", "title"]
VALID_STATES = {"active", "waiting", "blocked", "completed", "cancelled"}
VALID_IMPACTS = {"critical", "high", "medium", "low", "none", "unknown"}


class MosError(RuntimeError):
    pass


def today_iso() -> str:
    return date.today().isoformat()


def atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", dir=path.parent, delete=False, newline=""
    ) as handle:
        handle.write(text)
        temp_path = Path(handle.name)
    temp_path.replace(path)


def write_json(path: Path, data: Any) -> None:
    atomic_write(path, json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise MosError(f"Missing file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise MosError(f"Invalid JSON in {path}: {exc}") from exc


def default_config() -> dict[str, Any]:
    return {
        "schema": 1,
        "timezone": "UTC",
        "week_starts_on": "Monday",
        "work_days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        "language": "en",
        "human_view": "TASKS.md",
    }


def ensure_store() -> None:
    TASK_DIR.mkdir(parents=True, exist_ok=True)
    EVENT_DIR.mkdir(parents=True, exist_ok=True)
    if not CONFIG_PATH.exists():
        write_json(CONFIG_PATH, default_config())
    if not INDEX_PATH.exists():
        atomic_write(INDEX_PATH, "\t".join(INDEX_HEADER) + "\n")


def slug(value: str) -> str:
    result = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    if not result:
        raise MosError("Task ID cannot be empty")
    return result


def dedupe(values: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        normalized = value.strip()
        if normalized and normalized not in seen:
            seen.add(normalized)
            result.append(normalized)
    return result


def load_tasks() -> list[dict[str, Any]]:
    ensure_store()
    return [read_json(path) for path in sorted(TASK_DIR.glob("*.json"))]


def task_path(task_id: str) -> Path:
    return TASK_DIR / f"{slug(task_id)}.json"


def load_task(task_id: str) -> dict[str, Any]:
    return read_json(task_path(task_id))


def compact_task(task: dict[str, Any]) -> dict[str, Any]:
    def compact(value: Any) -> Any:
        if isinstance(value, dict):
            return {key: compact(item) for key, item in value.items() if item not in (None, "", [], {})}
        if isinstance(value, list):
            return [compact(item) for item in value if item not in (None, "", [], {})]
        return value

    return compact(task)


def validate_task(task: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for field in ("schema", "id", "title", "state", "impact", "updated"):
        if field not in task:
            errors.append(f"missing {field}")
    if task.get("schema") != 1:
        errors.append("schema must be 1")
    if task.get("id") != slug(str(task.get("id", ""))):
        errors.append("id must be lowercase kebab-case")
    if task.get("state") not in VALID_STATES:
        errors.append(f"invalid state: {task.get('state')}")
    impact = task.get("impact", {})
    if not isinstance(impact, dict) or impact.get("level", "unknown") not in VALID_IMPACTS:
        errors.append("impact.level is invalid")
    return errors


def save_task(task: dict[str, Any], *, render: bool = True) -> None:
    task = compact_task(task)
    errors = validate_task(task)
    if errors:
        raise MosError(f"Invalid task {task.get('id', '<unknown>')}: {', '.join(errors)}")
    write_json(task_path(task["id"]), task)
    rebuild_index()
    if render:
        render_tasks()


def impact_rank(task: dict[str, Any]) -> int:
    return {"critical": 0, "high": 1, "medium": 2, "unknown": 3, "low": 4, "none": 5}.get(
        task.get("impact", {}).get("level", "unknown"), 3
    )


def state_rank(state: str) -> int:
    return {"active": 0, "blocked": 1, "waiting": 2, "completed": 3, "cancelled": 4}.get(state, 5)


def rebuild_index() -> None:
    tasks = sorted(load_tasks(), key=lambda task: (state_rank(task["state"]), impact_rank(task), task["title"].lower()))
    rows = [INDEX_HEADER]
    for task in tasks:
        rows.append(
            [
                task["id"],
                task["state"],
                task.get("impact", {}).get("level", "unknown"),
                task.get("due", ""),
                task.get("owner", ""),
                task.get("updated", ""),
                f".mos/tasks/{task['id']}.json",
                task["title"].replace("\t", " "),
            ]
        )
    atomic_write(INDEX_PATH, "\n".join("\t".join(str(value) for value in row) for row in rows) + "\n")


def render_items(lines: list[str], label: str, values: list[str]) -> None:
    if not values:
        return
    lines.append(f"- **{label}:**")
    for value in values:
        lines.append(f"  - {value}")


def render_tasks() -> None:
    tasks = sorted(load_tasks(), key=lambda task: (state_rank(task["state"]), impact_rank(task), task["title"].lower()))
    lines = [
        "<!-- Generated by mos.py. Do not edit directly. -->",
        "# Tasks",
        "",
        f"Last rendered: {datetime.now().astimezone().isoformat(timespec='minutes')}",
        "",
        "Canonical state lives under `.mos/`. This file is the human/offline view.",
        "",
    ]
    groups = [
        ("Active", {"active", "blocked"}),
        ("Waiting", {"waiting"}),
        ("Completed", {"completed", "cancelled"}),
    ]
    for heading, states in groups:
        matching = [task for task in tasks if task["state"] in states]
        lines.extend([f"## {heading}", ""])
        if not matching:
            lines.extend(["_None._", ""])
            continue
        for task in matching:
            impact = task.get("impact", {})
            lines.extend(
                [
                    f"### {task['title']}",
                    "",
                    f"- **ID:** `{task['id']}`",
                    f"- **State:** {task['state']}",
                    f"- **Impact:** {impact.get('level', 'unknown')}",
                ]
            )
            for field, label in (("status", "Status"), ("priority", "Priority"), ("goal", "Goal")):
                if task.get(field):
                    lines.append(f"- **{label}:** {task[field]}")
            if impact.get("scope"):
                lines.append(f"- **Impact scope:** {impact['scope']}")
            render_items(lines, "Next", task.get("next", []))
            render_items(lines, "Waiting on", task.get("wait", []))
            render_items(lines, "Current context", task.get("facts", []))
            render_items(lines, "Decisions", task.get("decisions", []))
            render_items(lines, "Completed work", task.get("done", []))
            if task.get("resume"):
                lines.append(f"- **Resume:** {task['resume']}")
            if task.get("summary"):
                lines.append(f"- **Summary:** {task['summary']}")
            refs = task.get("refs", [])
            if refs:
                lines.append("- **References:**")
                for ref in refs:
                    name = ref.get("title") or ref.get("external_id") or ref.get("id") or ref.get("system", "Reference")
                    locator = ref.get("url") or ref.get("locator") or ""
                    suffix = f" — {locator}" if locator else ""
                    lines.append(f"  - {name}{suffix}")
            lines.extend([f"- **Updated:** {task.get('updated', '')}", ""])
    atomic_write(TASK_VIEW_PATH, "\n".join(lines).rstrip() + "\n")


def next_event_id(at: str) -> str:
    month_path = EVENT_DIR / f"{at[:7]}.jsonl"
    prefix = f"e-{at.replace('-', '')}-"
    highest = 0
    if month_path.exists():
        for raw in month_path.read_text(encoding="utf-8").splitlines():
            if not raw.strip():
                continue
            event_id = json.loads(raw).get("id", "")
            match = re.fullmatch(re.escape(prefix) + r"(\d+)", event_id)
            if match:
                highest = max(highest, int(match.group(1)))
    return f"{prefix}{highest + 1:03d}"


def append_event(event: dict[str, Any]) -> dict[str, Any]:
    ensure_store()
    at = str(event.get("at") or today_iso())
    event["at"] = at
    event.setdefault("id", next_event_id(at))
    event.setdefault("recorded", today_iso())
    event.setdefault("sig", "routine")
    event = compact_task(event)
    month_path = EVENT_DIR / f"{at[:7]}.jsonl"
    existing = month_path.read_text(encoding="utf-8") if month_path.exists() else ""
    atomic_write(month_path, existing + json.dumps(event, ensure_ascii=False, separators=(",", ":")) + "\n")
    return event


def cmd_init(_: argparse.Namespace) -> None:
    ensure_store()
    rebuild_index()
    render_tasks()
    print(f"Initialized {STORE.relative_to(ROOT)}")


def cmd_list(args: argparse.Namespace) -> None:
    tasks = sorted(load_tasks(), key=lambda task: (state_rank(task["state"]), impact_rank(task), task["title"].lower()))
    if args.state:
        tasks = [task for task in tasks if task["state"] in args.state]
    if args.json:
        payload = [
            {
                "id": task["id"], "title": task["title"], "state": task["state"],
                "impact": task.get("impact", {}).get("level", "unknown"),
                "next": task.get("next", []), "wait": task.get("wait", []), "updated": task.get("updated")
            }
            for task in tasks
        ]
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return
    print("\t".join(["state", "impact", "id", "title", "next"]))
    for task in tasks:
        next_action = task.get("next", [""])[0] if task.get("next") else ""
        print("\t".join([task["state"], task.get("impact", {}).get("level", "unknown"), task["id"], task["title"], next_action]))


def cmd_show(args: argparse.Namespace) -> None:
    full_task = load_task(args.task_id)
    task = full_task
    if not args.full:
        keys = [
            "id", "title", "state", "status", "impact", "priority", "goal", "next", "wait",
            "facts", "decisions", "done", "resume", "summary", "updated"
        ]
        task = {key: task[key] for key in keys if key in task}
        if task_refs := full_task.get("refs", []):
            ref_keys = ["id", "system", "kind", "external_id", "title", "url", "locator"]
            task["refs"] = [
                {key: ref[key] for key in ref_keys if ref.get(key) not in (None, "", [], {})}
                for ref in task_refs
            ]
    print(json.dumps(task, ensure_ascii=False, indent=2))


def cmd_add(args: argparse.Namespace) -> None:
    path = task_path(args.id)
    if path.exists():
        raise MosError(f"Task already exists: {args.id}")
    task: dict[str, Any] = {
        "schema": 1,
        "id": slug(args.id),
        "title": args.title,
        "state": args.state,
        "impact": {"level": args.impact},
        "updated": args.date or today_iso(),
        "status": args.status,
        "goal": args.goal,
        "next": args.next,
        "wait": args.wait,
        "facts": args.fact,
    }
    save_task(task)
    append_event({"at": args.date or today_iso(), "task": [task["id"]], "kind": "task_created", "sig": args.sig, "note": args.note or f"Created task: {task['title']}"})
    print(task["id"])


def remove_exact(values: list[str], targets: list[str]) -> list[str]:
    remove = set(targets)
    return [value for value in values if value not in remove]


def cmd_update(args: argparse.Namespace) -> None:
    task = load_task(args.task_id)
    previous_state = task["state"]
    for field in ("title", "state", "status", "priority", "goal", "resume", "summary", "due", "owner"):
        value = getattr(args, field)
        if value is not None:
            task[field] = value
    if args.impact:
        task.setdefault("impact", {})["level"] = args.impact
    operations = [
        ("next", args.add_next, args.remove_next),
        ("wait", args.add_wait, args.remove_wait),
        ("facts", args.fact, []),
        ("decisions", args.decision, []),
        ("done", args.done, []),
    ]
    for field, additions, removals in operations:
        values = remove_exact(task.get(field, []), removals)
        task[field] = dedupe(values + additions)
    if args.clear_wait:
        task["wait"] = []
    task["updated"] = args.date or today_iso()
    save_task(task)
    note = args.note or f"Updated task: {task['title']}"
    event: dict[str, Any] = {
        "at": args.date or today_iso(), "task": [task["id"]], "kind": args.kind,
        "sig": args.sig, "note": note
    }
    if task["state"] != previous_state:
        event["from"] = previous_state
        event["set"] = {"state": task["state"]}
    append_event(event)
    print(task["id"])


def cmd_complete(args: argparse.Namespace) -> None:
    task = load_task(args.task_id)
    previous = task["state"]
    task["state"] = "completed"
    task["updated"] = args.date or today_iso()
    task["completed"] = args.date or today_iso()
    if args.done:
        task["done"] = dedupe(task.get("done", []) + args.done)
    save_task(task)
    append_event({
        "at": args.date or today_iso(), "task": [task["id"]], "kind": "outcome", "sig": args.sig,
        "note": args.note, "from": previous, "set": {"state": "completed"}
    })
    print(task["id"])


def cmd_event(args: argparse.Namespace) -> None:
    for task_id in args.task:
        load_task(task_id)
    event = append_event({
        "at": args.date or today_iso(), "task": args.task, "kind": args.kind,
        "sig": args.sig, "note": args.note, "detail": args.detail
    })
    print(event["id"])


def period_bounds(period: str, anchor: date) -> tuple[date, date]:
    if period == "day":
        return anchor, anchor
    if period == "week":
        return anchor - timedelta(days=anchor.weekday()), anchor
    if period == "month":
        return anchor.replace(day=1), anchor
    if period == "year":
        return anchor.replace(month=1, day=1), anchor
    raise MosError(f"Unknown period: {period}")


def months_between(start: date, end: date) -> list[str]:
    result: list[str] = []
    year, month = start.year, start.month
    while (year, month) <= (end.year, end.month):
        result.append(f"{year:04d}-{month:02d}")
        month += 1
        if month == 13:
            year, month = year + 1, 1
    return result


def cmd_context(args: argparse.Namespace) -> None:
    anchor = date.fromisoformat(args.date) if args.date else date.today()
    start, end = period_bounds(args.period, anchor)
    events: list[dict[str, Any]] = []
    for month in months_between(start, end):
        path = EVENT_DIR / f"{month}.jsonl"
        if not path.exists():
            continue
        for raw in path.read_text(encoding="utf-8").splitlines():
            if raw.strip():
                event = json.loads(raw)
                occurred = date.fromisoformat(event["at"][:10])
                if start <= occurred <= end:
                    events.append(event)
    pending = []
    for task in sorted(load_tasks(), key=lambda item: (state_rank(item["state"]), impact_rank(item))):
        if task["state"] in {"completed", "cancelled"}:
            continue
        pending.append({
            "id": task["id"], "title": task["title"], "state": task["state"],
            "impact": task.get("impact", {}).get("level", "unknown"),
            "next": task.get("next", []), "wait": task.get("wait", [])
        })
    print(json.dumps({"period": {"from": start.isoformat(), "to": end.isoformat()}, "events": events, "pending": pending}, ensure_ascii=False, indent=2))


def cmd_render(_: argparse.Namespace) -> None:
    rebuild_index()
    render_tasks()
    print(TASK_VIEW_PATH.name)


def cmd_stats(_: argparse.Namespace) -> None:
    tasks = sorted(TASK_DIR.glob("*.json"))
    task_sizes = sorted(path.stat().st_size for path in tasks)
    event_sizes = [path.stat().st_size for path in EVENT_DIR.glob("*.jsonl")]
    median_task = task_sizes[len(task_sizes) // 2] if task_sizes else 0
    event_lines = 0
    for path in EVENT_DIR.glob("*.jsonl"):
        event_lines += sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip())
    data = {
        "agent_bootstrap_bytes": (ROOT / "AGENTS.md").stat().st_size if (ROOT / "AGENTS.md").exists() else 0,
        "index_bytes": INDEX_PATH.stat().st_size if INDEX_PATH.exists() else 0,
        "task_count": len(tasks),
        "median_task_bytes": median_task,
        "largest_task_bytes": max(task_sizes, default=0),
        "event_count": event_lines,
        "event_bytes": sum(event_sizes),
        "average_event_bytes": round(sum(event_sizes) / event_lines, 1) if event_lines else 0,
        "human_view_bytes": TASK_VIEW_PATH.stat().st_size if TASK_VIEW_PATH.exists() else 0,
    }
    print(json.dumps(data, ensure_ascii=False, indent=2))


def cmd_verify(_: argparse.Namespace) -> None:
    errors: list[str] = []
    tasks = load_tasks()
    ids: set[str] = set()
    ref_ids: set[str] = set()
    for task in tasks:
        task_errors = validate_task(task)
        errors.extend(f"{task.get('id')}: {error}" for error in task_errors)
        if task.get("id") in ids:
            errors.append(f"duplicate task: {task.get('id')}")
        ids.add(task.get("id"))
        for ref in task.get("refs", []):
            ref_id = ref.get("id")
            if ref_id:
                if ref_id in ref_ids:
                    errors.append(f"duplicate reference: {ref_id}")
                ref_ids.add(ref_id)
    event_ids: set[str] = set()
    event_count = 0
    for path in sorted(EVENT_DIR.glob("*.jsonl")):
        for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if not raw.strip():
                continue
            event_count += 1
            try:
                event = json.loads(raw)
            except json.JSONDecodeError as exc:
                errors.append(f"{path}:{number}: invalid JSON: {exc}")
                continue
            if event.get("id") in event_ids:
                errors.append(f"duplicate event: {event.get('id')}")
            event_ids.add(event.get("id"))
            for task_id in event.get("task", []):
                if task_id not in ids:
                    errors.append(f"event {event.get('id')} references unknown task {task_id}")
    if errors:
        for error in errors:
            print(f"ERROR\t{error}")
        raise MosError(f"Verification failed with {len(errors)} error(s)")
    print(f"OK\t{len(tasks)} tasks\t{event_count} events\t{len(ref_ids)} references")


def add_common_event_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--date", help="Occurrence date, YYYY-MM-DD")
    parser.add_argument("--sig", choices=["routine", "notable", "major"], default="routine")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="HUNNIGAN Model Operating System")
    sub = parser.add_subparsers(dest="command", required=True)

    init_parser = sub.add_parser("init", help="Initialize an empty private store")
    init_parser.set_defaults(func=cmd_init)

    list_parser = sub.add_parser("list", help="List compact current task state")
    list_parser.add_argument("--state", action="append", choices=sorted(VALID_STATES))
    list_parser.add_argument("--json", action="store_true")
    list_parser.set_defaults(func=cmd_list)

    show_parser = sub.add_parser("show", help="Show one task restart capsule")
    show_parser.add_argument("task_id")
    show_parser.add_argument("--full", action="store_true", help="Include archival and extended fields")
    show_parser.set_defaults(func=cmd_show)

    add_parser = sub.add_parser("add", help="Add one task and its creation event")
    add_parser.add_argument("--id", required=True)
    add_parser.add_argument("--title", required=True)
    add_parser.add_argument("--state", choices=sorted(VALID_STATES), default="active")
    add_parser.add_argument("--impact", choices=sorted(VALID_IMPACTS), default="unknown")
    add_parser.add_argument("--status")
    add_parser.add_argument("--goal")
    add_parser.add_argument("--next", action="append", default=[])
    add_parser.add_argument("--wait", action="append", default=[])
    add_parser.add_argument("--fact", action="append", default=[])
    add_parser.add_argument("--note")
    add_common_event_args(add_parser)
    add_parser.set_defaults(func=cmd_add)

    update_parser = sub.add_parser("update", help="Update one task and append one delta event")
    update_parser.add_argument("task_id")
    for name in ("title", "status", "priority", "goal", "resume", "summary", "due", "owner"):
        update_parser.add_argument(f"--{name.replace('_', '-')}")
    update_parser.add_argument("--state", choices=sorted(VALID_STATES))
    update_parser.add_argument("--impact", choices=sorted(VALID_IMPACTS))
    update_parser.add_argument("--add-next", action="append", default=[])
    update_parser.add_argument("--remove-next", action="append", default=[])
    update_parser.add_argument("--add-wait", action="append", default=[])
    update_parser.add_argument("--remove-wait", action="append", default=[])
    update_parser.add_argument("--clear-wait", action="store_true")
    update_parser.add_argument("--fact", action="append", default=[])
    update_parser.add_argument("--decision", action="append", default=[])
    update_parser.add_argument("--done", action="append", default=[])
    update_parser.add_argument("--kind", default="progress")
    update_parser.add_argument("--note")
    add_common_event_args(update_parser)
    update_parser.set_defaults(func=cmd_update)

    complete_parser = sub.add_parser("complete", help="Complete one task")
    complete_parser.add_argument("task_id")
    complete_parser.add_argument("--note", required=True)
    complete_parser.add_argument("--done", action="append", default=[])
    add_common_event_args(complete_parser)
    complete_parser.set_defaults(func=cmd_complete)

    event_parser = sub.add_parser("event", help="Append a compact event without changing task state")
    event_parser.add_argument("--task", action="append", default=[])
    event_parser.add_argument("--kind", required=True)
    event_parser.add_argument("--note", required=True)
    event_parser.add_argument("--detail", action="append", default=[])
    add_common_event_args(event_parser)
    event_parser.set_defaults(func=cmd_event)

    context_parser = sub.add_parser("context", help="Produce filtered context for a period summary")
    context_parser.add_argument("period", choices=["day", "week", "month", "year"])
    context_parser.add_argument("--date", help="Anchor date, YYYY-MM-DD")
    context_parser.set_defaults(func=cmd_context)

    render_parser = sub.add_parser("render", help="Regenerate index and human task view")
    render_parser.set_defaults(func=cmd_render)

    stats_parser = sub.add_parser("stats", help="Measure V1 context and storage sizes")
    stats_parser.set_defaults(func=cmd_stats)

    verify_parser = sub.add_parser("verify", help="Validate canonical task and event integrity")
    verify_parser.set_defaults(func=cmd_verify)
    return parser


def main() -> int:
    try:
        args = build_parser().parse_args()
        args.func(args)
        return 0
    except MosError as exc:
        print(f"mos: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

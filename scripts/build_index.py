#!/usr/bin/env python3
"""Generate a human-facing INDEX.md from README.md and TASKS.md.

INDEX.md is a generated file: agents update TASKS.md, then run this script.
Humans should not maintain INDEX.md by hand.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys

ACTIVE_MARKERS = (
    "进行中", "进行", "待确认", "待验证", "待", "未完成", "活动",
    "active", "in progress", "pending", "open", "todo",
)
COMPLETED_MARKERS = (
    "完成", "历史", "归档", "封存", "done", "completed", "archived",
)

COMMON_ENTRIES = (
    "AGENTS.md",
    "README.md",
    "TASKS.md",
    "01_tasks/",
    "02_shared/",
    "03_inbox/",
    "04_archive/",
    "05_tmp/",
)


def read_text(path: pathlib.Path) -> str:
    try:
        return path.read_text(encoding="utf-8").replace("\r\n", "\n")
    except FileNotFoundError:
        return ""


def first_heading(text: str, fallback: str) -> str:
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def parse_rows(text: str) -> tuple[list[dict[str, str]], bool]:
    table_lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip().startswith("|") and line.strip().endswith("|")
    ]
    rows: list[dict[str, str]] = []
    headers: list[str] | None = None
    for line in table_lines:
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if not cells:
            continue
        if all(re.fullmatch(r"[\s:|-]+", cell) for cell in cells):
            continue
        joined = " ".join(cells).lower()
        if headers is None and ("任务" in joined or "task" in joined) and ("目录" in joined or "directory" in joined):
            headers = cells
            continue
        if headers is None:
            rows.append({
                "date": cells[0] if len(cells) > 0 else "",
                "name": cells[1] if len(cells) > 1 else "",
                "dir": cells[2] if len(cells) > 2 else "",
                "status": cells[3] if len(cells) > 3 else "",
            })
            continue

        def get(*names: str) -> str:
            for name in names:
                for index, header in enumerate(headers):
                    if name in header.lower():
                        return cells[index] if index < len(cells) else ""
            return ""

        rows.append({
            "date": get("日期", "时间", "date", "time"),
            "name": get("任务", "task", "name"),
            "dir": get("目录", "directory", "dir"),
            "status": get("状态", "status"),
        })
    header_text = " ".join(headers).lower() if headers else ""
    english = "date time" in header_text or "task name" in header_text
    return rows, english


def date_key(value: str) -> tuple[int, int, int, int, int]:
    match = re.search(r"(\d{4})-(\d{2})-(\d{2})(?:[ T](\d{1,2})[:.]?(\d{2}))?", value)
    if not match:
        return (0, 0, 0, 0, 0)
    return (
        int(match.group(1)),
        int(match.group(2)),
        int(match.group(3)),
        int(match.group(4) or 0),
        int(match.group(5) or 0),
    )


def is_active(status: str) -> bool:
    lowered = status.lower()
    if any(marker in lowered for marker in ACTIVE_MARKERS):
        return True
    return not any(marker in lowered for marker in COMPLETED_MARKERS)


def format_row(row: dict[str, str], english: bool) -> str:
    date = row.get("date", "").strip()
    name = row.get("name", "").strip()
    status = row.get("status", "").strip()
    directory = row.get("dir", "").strip()
    label = " / ".join(part for part in (date, name) if part)
    if english:
        status_part = f" ({status})" if status else ""
        return f"- {label}{status_part}: {directory}" if directory else f"- {label}{status_part}"
    status_part = f"（{status}）" if status else ""
    return f"- {label}{status_part}: {directory}" if directory else f"- {label}{status_part}"


def render_index(root: pathlib.Path) -> str:
    theme = first_heading(read_text(root / "README.md"), root.name)
    rows, english = parse_rows(read_text(root / "TASKS.md"))
    active = [row for row in rows if is_active(row.get("status", ""))]
    recent = sorted(rows, key=lambda row: date_key(row.get("date", "")), reverse=True)[:8]
    lines = ["# INDEX", ""]
    if english:
        lines += ["## Topic", "", theme, "", "## Active Tasks"]
    else:
        lines += ["## 主题", "", theme, "", "## 活动任务"]
    lines.append("")
    if active:
        lines += [format_row(row, english) for row in active]
    else:
        lines.append("- （无）" if not english else "- (none)")
    lines += ["", "## Recent Tasks" if english else "## 最近任务", ""]
    if recent:
        lines += [format_row(row, english) for row in recent]
    else:
        lines.append("- （无）" if not english else "- (none)")
    lines += ["", "## Common Entry Points" if english else "## 常用入口", ""]
    lines += [f"- `{entry}`" for entry in COMMON_ENTRIES]
    lines.append("")
    return "\n".join(lines)


def check_index(root: pathlib.Path) -> int:
    generated = render_index(root)
    path = root / "INDEX.md"
    if not path.exists():
        print("INDEX.md not present (optional). Run python scripts/build_index.py to create it.")
        return 0
    if path.read_text(encoding="utf-8").replace("\r\n", "\n") != generated:
        print("INDEX.md is stale. Run: python scripts/build_index.py")
        return 1
    print("INDEX.md is up to date.")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate or check INDEX.md.")
    parser.add_argument("--root", default=".", help="Workspace root (default: current directory)")
    parser.add_argument("--check", action="store_true", help="Check freshness without writing")
    args = parser.parse_args(argv)
    root = pathlib.Path(args.root).resolve()
    if args.check:
        return check_index(root)
    generated = render_index(root)
    path = root / "INDEX.md"
    path.write_text(generated, encoding="utf-8", newline="\n")
    print(f"INDEX.md written to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

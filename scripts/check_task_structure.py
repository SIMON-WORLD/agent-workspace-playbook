#!/usr/bin/env python3
"""Validate that 01_tasks/* follows the slim task skeleton.

Allowed entries at a task root:
- files: prompt.md, notes.md
- directories: 01_assets, 02_output, 03_logs, 04_tmp

Nested subfolders are allowed but must be created on demand.
"""

from __future__ import annotations

import sys
from pathlib import Path

ALLOWED_FILES = {"prompt.md", "notes.md"}
ALLOWED_DIRS = {"01_assets", "02_output", "03_logs", "04_tmp"}


def check_workspace(root: Path) -> list[str]:
    issues: list[str] = []
    task_root = root / "01_tasks"
    if not task_root.is_dir():
        return [f"missing 01_tasks under {root}"]
    for task in sorted(task_root.iterdir()):
        if not task.is_dir():
            issues.append(f"{task.name}: unexpected file in 01_tasks")
            continue
        for name in sorted(ALLOWED_FILES):
            if not (task / name).is_file():
                issues.append(f"{task.name}: missing {name}")
        for name in sorted(ALLOWED_DIRS):
            if not (task / name).is_dir():
                issues.append(f"{task.name}: missing {name}")
        for entry in task.iterdir():
            if entry.name in ALLOWED_FILES or entry.name in ALLOWED_DIRS:
                continue
            kind = "directory" if entry.is_dir() else "file"
            issues.append(f"{task.name}: unexpected top-level {kind} {entry.name}")
    return issues


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd().resolve()
    issues = check_workspace(root)
    if issues:
        for issue in issues:
            print(f"ISSUE: {issue}")
        return 1
    print("OK: all task directories follow the slim skeleton.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
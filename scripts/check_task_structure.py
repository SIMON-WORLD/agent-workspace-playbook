#!/usr/bin/env python3
"""Validate that 01_tasks/* follows the slim task skeleton.

Allowed entries at a task root:
- files: prompt.md, notes.md
- directories: 01_assets, 02_output, 03_logs, 04_tmp

Nested subfolders are allowed but must be created on demand.
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

ALLOWED_FILES = {"prompt.md", "notes.md"}
ALLOWED_DIRS = {"01_assets", "02_output", "03_logs", "04_tmp"}
TEMPLATE_DIR_NAMES = {"00_template"}
GIT_DIR_NAME = ".git"
SKIP_DIR_NAMES = {"node_modules", ".venv", "__pycache__", ".git"}
STANDARD_SUBDIRS = (
    "01_assets/01_input",
    "01_assets/02_reference",
    "01_assets/03_working",
    "02_output/01_final",
    "02_output/02_reports",
    "02_output/03_exports",
    "02_output/90_working",
    "03_logs/01_runs",
    "03_logs/90_tool-state",
)


def _is_effectively_empty(path: Path) -> bool:
    """Return True only when a folder contains no entries at all."""
    return not any(path.iterdir())




def _find_git_dirs(task: Path):
    """Yield .git directories while pruning heavy or internal directories."""
    for root, dirs, files in os.walk(task):
        pruned = []
        for name in sorted(dirs):
            path = Path(root) / name
            if name == GIT_DIR_NAME:
                yield path
                continue
            if name in SKIP_DIR_NAMES:
                continue
            pruned.append(name)
        dirs[:] = pruned


def _registered_task_names(root: Path) -> set[str]:
    tasks_md = root / "TASKS.md"
    if not tasks_md.is_file():
        return set()
    text = tasks_md.read_text(encoding="utf-8")
    return set(re.findall(r"01_tasks/([A-Za-z0-9._-]+)", text))
def check_workspace(root: Path) -> list[str]:
    issues: list[str] = []
    registered = _registered_task_names(root)
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
        if task.name not in TEMPLATE_DIR_NAMES and registered and task.name not in registered:
            issues.append(f"{task.name}: not registered in TASKS.md")
        if task.name in TEMPLATE_DIR_NAMES:
            continue
        for sub in STANDARD_SUBDIRS:
            sub_path = task / sub
            if sub_path.is_dir() and _is_effectively_empty(sub_path):
                issues.append(f"{task.name}: empty pre-created subfolder {sub}")
        for git_dir in _find_git_dirs(task):
            rel = git_dir.relative_to(task)
            if "04_tmp" in rel.parts:
                continue
            issues.append(f"{task.name}: unexpected .git directory {rel.as_posix()}")
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
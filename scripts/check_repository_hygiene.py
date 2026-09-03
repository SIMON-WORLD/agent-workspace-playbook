#!/usr/bin/env python3
"""Check for common secrets, local paths, required workflow files, and nested Git repositories."""

from __future__ import annotations

import argparse
import os
import pathlib
import re
import subprocess
import sys

REQUIRED_FILES = [
    "README.md",
    "README.zh-CN.md",
    "TASKS.md",
    ".github/ISSUE_TEMPLATE/agent-task.yml",
    ".github/pull_request_template.md",
    ".github/workflows/tests.yml",
    "scripts/build_index.py",
    "scripts/check_commit_emails.py",
    "scripts/check_repository_hygiene.py",
    "scripts/check_task_structure.py",
    "tests/test_build_index.py",
    "tests/test_commit_emails.py",
    "tests/test_repository_hygiene.py",
    "tests/test_check_task_structure.py",
]

# At least one agent rule file must exist; a single-agent workspace may keep only its own.
REQUIRED_ONE_OF = [
    ("AGENTS.md", "CLAUDE.md"),
]

SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"ghp_[A-Za-z0-9_]{20,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"-----BEGIN (?:RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----"),
    re.compile(r"(?i)\b(?:api[_-]?key|token|password|secret)\s*=\s*['\"]?[^'\"\s]{8,}"),
]

LOCAL_PATH_PATTERNS = [
    re.compile(r"\b[A-Za-z]:\\(?:Users|Desktop|Downloads|Documents|OneDrive|BaiduSyncdisk)\\"),
    re.compile(r"/Users/[^/\s]+/"),
    re.compile(r"/home/[^/\s]+/"),
]

ALLOWED_LOCAL_PATH_CONTEXTS = (
    "example",
    "placeholder",
    "do not write",
    "don't write",
    "do not commit",
    "do not scan",
    "do not modify",
    "for example",
)

ALLOWED_ROOT_NAMES = {
    ".agents",
    ".claude",
    ".codex",
    ".git",
    ".github",
    ".gitignore",
    ".reasonix",
    ".workbuddy",
    "01_tasks",
    "02_shared",
    "03_inbox",
    "04_archive",
    "05_tmp",
    "AGENTS.md",
    "CLAUDE.md",
    "INDEX.md",
    "LICENSE",
    "README.md",
    "README.zh-CN.md",
    "TASKS.md",
    "activity",
    "docs",
    "scripts",
    "tests",
}

SKIP_SUFFIXES = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
    ".pdf",
    ".pptx",
    ".docx",
    ".xlsx",
    ".zip",
    ".exe",
    ".pyc",
}


def tracked_files(root: pathlib.Path) -> list[pathlib.Path]:
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    return [root / line for line in result.stdout.splitlines() if line.strip()]


def read_text(path: pathlib.Path) -> str | None:
    if path.suffix.lower() in SKIP_SUFFIXES:
        return None
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return None


def is_allowed_local_path_line(line: str) -> bool:
    lowered = line.lower()
    return any(marker in lowered for marker in ALLOWED_LOCAL_PATH_CONTEXTS)


def check_required_files(root: pathlib.Path) -> list[str]:
    missing = []
    for file_name in REQUIRED_FILES:
        if not (root / file_name).is_file():
            missing.append(f"Missing required file: {file_name}")
    for group in REQUIRED_ONE_OF:
        if not any((root / file_name).is_file() for file_name in group):
            missing.append(f"Missing at least one required file: {', '.join(group)}")
    return missing


def check_content(root: pathlib.Path) -> list[str]:
    findings = []
    for path in tracked_files(root):
        text = read_text(path)
        if text is None:
            continue
        rel = path.relative_to(root).as_posix()
        for index, line in enumerate(text.splitlines(), start=1):
            for pattern in SECRET_PATTERNS:
                if pattern.search(line):
                    findings.append(f"{rel}:{index}: possible secret pattern")
            for pattern in LOCAL_PATH_PATTERNS:
                if rel == "scripts/check_repository_hygiene.py" and "re.compile" in line:
                    continue
                if pattern.search(line) and not is_allowed_local_path_line(line):
                    findings.append(f"{rel}:{index}: local absolute path")
    return findings




def check_root_layout(root: pathlib.Path) -> list[str]:
    """Flag root entries that are not part of the standard workspace layout."""
    issues = []
    for entry in sorted(root.iterdir()):
        if entry.name not in ALLOWED_ROOT_NAMES:
            kind = "directory" if entry.is_dir() else "file"
            issues.append(f"Unexpected root {kind}: {entry.name}")
    return issues


def find_nested_git_directories(root: pathlib.Path) -> list[pathlib.Path]:
    """Return any .git directory/file nested below the repository root.

    The repository root's own .git (a directory or a gitfile pointing at a
    worktree) represents the active repository and is always allowed. Any
    nested .git directory is a nested Git repository and is rejected.
    """
    nested = []
    for dirpath, dirnames, filenames in os.walk(root):
        current = pathlib.Path(dirpath)
        if current == root:
            # Root .git is the active repository; skip it and do not descend.
            dirnames[:] = [name for name in dirnames if name != ".git"]
            continue
        if ".git" in dirnames:
            nested.append(current / ".git")
        if ".git" in filenames:
            nested.append(current / ".git")
        # Never walk inside another repository's internals.
        dirnames[:] = [name for name in dirnames if name != ".git"]
    return nested


def check_nested_git(root: pathlib.Path) -> list[str]:
    """Flag any nested Git repository below the repository root."""
    findings = []
    for path in find_nested_git_directories(root):
        findings.append(f"Nested Git repository: {path.relative_to(root).as_posix()}")
    return findings


def run(root: pathlib.Path) -> int:
    findings = (
        check_required_files(root)
        + check_content(root)
        + check_root_layout(root)
        + check_nested_git(root)
    )
    if findings:
        print("Repository hygiene check failed:")
        for finding in findings:
            print(f"- {finding}")
        return 1
    print("Repository hygiene check passed.")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".", help="Repository root")
    args = parser.parse_args(argv)
    return run(pathlib.Path(args.root).resolve())


if __name__ == "__main__":
    sys.exit(main())

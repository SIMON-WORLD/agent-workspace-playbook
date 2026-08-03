#!/usr/bin/env python3
"""Check for common secrets, local paths, and required workflow files."""

from __future__ import annotations

import argparse
import pathlib
import re
import subprocess
import sys

REQUIRED_FILES = [
    "AGENTS.md",
    "CLAUDE.md",
    "README.md",
    "TASKS.md",
    ".github/ISSUE_TEMPLATE/agent-task.yml",
    ".github/pull_request_template.md",
    ".github/workflows/tests.yml",
    "scripts/check_commit_emails.py",
    "scripts/check_repository_hygiene.py",
    "scripts/check_task_structure.py",
    "tests/test_commit_emails.py",
    "tests/test_repository_hygiene.py",
    "tests/test_check_task_structure.py",
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


def run(root: pathlib.Path) -> int:
    findings = check_required_files(root) + check_content(root)
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

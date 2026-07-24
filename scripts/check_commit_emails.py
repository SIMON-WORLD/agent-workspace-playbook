#!/usr/bin/env python3
"""Block personal commit emails in the repository history."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys

ALLOWED_EXACT = {
    "project-test-bot@example.com",
    "noreply@github.com",
    "noreply@openai.com",
    "noreply@anthropic.com",
}

ALLOWED_PATTERNS = [
    re.compile(r"^\d+\+[^@]+@users\.noreply\.github\.com$"),
    re.compile(r"^[^@]+@users\.noreply\.github\.com$"),
]


def commit_emails(rev_range: str) -> set[str]:
    result = subprocess.run(
        ["git", "log", "--format=%ae%n%ce", rev_range],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    return {line.strip() for line in result.stdout.splitlines() if line.strip()}


def is_allowed(email: str) -> bool:
    lowered = email.lower()
    if lowered in ALLOWED_EXACT:
        return True
    return any(pattern.match(lowered) for pattern in ALLOWED_PATTERNS)


def run(rev_range: str) -> int:
    emails = sorted(commit_emails(rev_range))
    blocked = [email for email in emails if not is_allowed(email)]
    if blocked:
        print("Commit email check failed. Use GitHub noreply or an approved bot email:")
        for email in blocked:
            print(f"- {email}")
        return 1
    print("Commit email check passed.")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rev-range", default="HEAD", help="Git revision range to inspect")
    args = parser.parse_args(argv)
    return run(args.rev_range)


if __name__ == "__main__":
    sys.exit(main())

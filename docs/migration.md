# Migration Guide

Use this guide when moving an existing messy agent workspace into this structure.

## Recommended Steps

1. Audit first. Do not move files immediately.
2. Identify task-like folders, shared materials, inbox files, archive candidates, and temporary outputs.
3. Create a move list in this form:

```text
old/path -> new/path
```

4. Ask the user to confirm the move list.
5. Move files only after confirmation.
6. Update `TASKS.md`.
7. Record the migration in the relevant task's `notes.md`.

## Destination Rules

- One-off task work goes under `01_tasks/YYYY-MM-DD-HHMM-short-task-name/`.
- Reusable docs go under `02_shared/01_docs/`.
- Reusable scripts go under `02_shared/02_scripts/`.
- Reusable assets go under `02_shared/03_assets/`.
- Unclear files go under `03_inbox/`.
- Completed or deprecated task folders go under `04_archive/` only after user confirmation.
- Temporary scratch files go under `04_tmp/`.

## Safety

Do not move, delete, or rewrite files outside the current workspace unless the user explicitly confirms.


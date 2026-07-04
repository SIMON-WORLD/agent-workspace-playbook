# CLAUDE.md

This is a local agent workspace. Claude should keep all task files and outputs inside this project root by default.

## Workspace Boundary

- Only create, modify, move, or delete files inside the current project root unless the user explicitly confirms otherwise.
- Unless the user explicitly requests another language, write user-facing replies, documentation, task notes, and final reports in Chinese.
- Do not write generated files, logs, temporary files, scripts, skills, MCP config, or task outputs to global `.claude`, global `.codex`, global `.agents`, Desktop, Downloads, Documents, system folders, or any path outside this workspace.
- Do not run global install commands such as `npm install -g`, global `pip install`, PATH edits, system environment changes, or user-level agent configuration changes without explicit confirmation.
- If a path, permission, or target directory is unclear, stop and ask the user.

## Task Folder Rule

- Each new task should use: `01_tasks/YYYY-MM-DD-HHMM-short-task-name/`.
- Do not create a new timestamp folder just because the user continues the same conversation, restarts the agent, asks for verification, asks for fixes, or adds documentation.
- Long-running projects should use one main task folder or an epic index.
- Each task folder should contain:
  - `prompt.md`
  - `notes.md`
  - `01_assets/`
  - `02_output/`
  - `03_logs/`
  - `04_tmp/`

## Task Subfolders

- `prompt.md`: original request, constraints, expected output.
- `notes.md`: decisions, process notes, file changes, verification, follow-up.
- `01_assets/01_input/`: user-provided files and copied-in external inputs.
- `01_assets/02_reference/`: reference material and read-only context.
- `01_assets/03_working/`: intermediate working assets.
- `02_output/01_final/`: final deliverables.
- `02_output/02_reports/`: reports, audits, explanations.
- `02_output/03_exports/`: exported files.
- `02_output/90_working/`: draft or in-progress outputs.
- `03_logs/01_runs/`: command logs and verification logs.
- `03_logs/90_tool-state/`: tool state, caches, hidden state folders.
- `04_tmp/`: task-local temporary files.

## Shared Materials

- Put reusable documents in `02_shared/01_docs/`.
- Put reusable scripts in `02_shared/02_scripts/`.
- Put reusable assets, reference images, and test data in `02_shared/03_assets/`.
- Put unclear files in `03_inbox/` until they can be classified.

## Skills And MCP

- Project-level Claude skills, if needed, should be created under `.claude/skills/[skill-name]/SKILL.md`.
- Do not modify global `.claude`, `.codex`, or `.agents` directories unless the user explicitly confirms.
- Do not create or modify MCP configuration without first explaining the reason, content, commands, permissions, and risks.

## Scripts

- Maintainable first-party scripts should use: `NN_verb_object_context.ext`.
- Examples: `01_check_project_structure.ps1`, `02_build_task_index.py`.
- Put historical or risky scripts under `90_legacy/` and prefix them with `90_legacy_`.
- Do not rename third-party repositories, downloaded packages, or unpacked skill internals just for neatness.

## End-Of-Task Report

At the end of each task, report:

- Files created
- Files modified
- Files moved
- Files not handled
- External path risk
- Verification results


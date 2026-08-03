# CLAUDE.md

This is a local agent workspace. Claude should keep all task files and outputs inside this project root by default.

## Workspace Boundary

- Only create, modify, move, or delete files inside the current project root unless the user explicitly confirms otherwise.
- Unless the user explicitly requests another language, write user-facing replies, documentation, task notes, and final reports in Chinese.
- Do not write generated files, logs, temporary files, scripts, skills, MCP config, or task outputs to global `.claude`, global `.codex`, global `.agents`, Desktop, Downloads, Documents, system folders, or any path outside this workspace.
- Do not run global install commands such as `npm install -g`, global `pip install`, PATH edits, system environment changes, or user-level agent configuration changes without explicit confirmation.
- If a path, permission, or target directory is unclear, stop and ask the user.

## User-Provided External Input Files

- If the user explicitly uploads, drops, pastes, or provides the full path to a specific external file, the agent may read that single file as task input in read-only mode.
- After reading it, copy the file into the current task folder under `01_assets/01_input/` and continue working from the project-local copy.
- Do not modify, move, or delete the external source file. Do not scan the external parent directory or bulk-read sibling files unless the user explicitly confirms.
- Do not write outputs, logs, caches, or intermediate files back to the external path. All generated files still belong inside the current task folder.
- If the file may contain sensitive information, the path is unclear, permissions are uncertain, or the task requires reading multiple external files/directories, ask the user first.
- If the runtime cannot directly read the external file, explain why and ask the user to upload/drop it again or approve copying it into the current task folder.

## Task Folder Rule

- Each new task should use: `01_tasks/YYYY-MM-DD-HHMM-short-task-name/`.
- `YYYY-MM-DD-HHMM` must use the current local date and time. Do not use `0000`, `HHMM`, or other placeholders unless the task actually starts at midnight. If the current time is unclear, run a local time command first.
- `short-task-name` should be a short English slug with hyphens. Sidebar titles may use Chinese.
- Do not create a new timestamp folder just because the user continues the same conversation, restarts the agent, asks for verification, asks for fixes, or adds documentation.
- Long-running projects should use one main task folder or an epic index.
- Each task folder should contain:
  - `prompt.md`
  - `notes.md`
  - `01_assets/`
  - `02_output/`
  - `03_logs/`
  - `04_tmp/`

## Conversation Title Rule

- Keep the user's first message natural. Do not require a `会话标题：...` prefix just to satisfy naming.
- If the user does provide `会话标题：...` or `Conversation title: ...`, prefer that title.
- The agent may suggest a short title (for example `⭐⭐⭐short-task-name`) in its first reply and record it in `prompt.md` or `notes.md`.
- Use stars to express importance and task level:
  - `⭐`: quick check, lightweight experiment, one-off test.
  - `⭐⭐`: normal test task.
  - `⭐⭐⭐`: important project task, reusable capability development, formal workflow test.
  - `⭐⭐⭐⭐`: workspace rules, template work, system-level cleanup, migration.
  - `⭐⭐⭐⭐⭐`: long-running mainline, core production workflow, highest-priority project.
- If the current agent environment provides a thread rename tool and the current thread id is available, apply the suggested title automatically. Otherwise, do not require the user to rename frequently; they may rename manually when they want a tidy sidebar.
- Never write to global config just to rename a title.
- Sidebar titles are only for human recognition. Task folders must still use `01_tasks/YYYY-MM-DD-HHMM-short-task-name/`.
- Continued work under the same sidebar title should reuse the same task folder unless the user clearly starts a different task.

## Task Subfolders

- Each task starts with only 6 entries: `prompt.md`, `notes.md`, `01_assets/`, `02_output/`, `03_logs/`, `04_tmp/`.
- Create the following subfolders on demand only; do not pre-create empty folders:
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

## Task Structure Validation

- Task roots must contain only `prompt.md`, `notes.md`, `01_assets/`, `02_output/`, `03_logs/`, `04_tmp/`.
- Do not create legacy top-level folders such as `output/`, `90_archive/`, `.venv/`, `.superpowers/`, `.worktrees/`, or `$task`.
- After creating or reorganizing tasks, run `python scripts/check_task_structure.py`.
- A PowerShell workspace-local equivalent is `02_shared/02_scripts/01_active/01_check_task_structure.ps1`.

## Human Navigation (Optional)

- For long-lived workspaces, maintain a root `INDEX.md` for humans: topic, current task paths, status, and key entry points.
- `TASKS.md` remains the agent-facing task register. `INDEX.md` must not change the `01_tasks/` structure.

## Task vs Project Boundary

- A task folder records one agent work session: prompt, notes, test results, patches, reports, and decisions.
- Long-lived code/products live in their own repository. The task folder keeps entry points, verification results, and links, not a full project copy (no `.git`, dependency folders, or caches inside task outputs).

## Shared Materials

- Put reusable documents in `02_shared/01_docs/`.
- Put reusable scripts in `02_shared/02_scripts/`.
- Put reusable assets, reference images, and test data in `02_shared/03_assets/`.
- Put unclear files in `03_inbox/` until they can be classified.

## Skills And MCP

- Project-level Claude skills, if needed, should be created under `.claude/skills/[skill-name]/SKILL.md`.
- Do not modify global `.claude`, `.codex`, or `.agents` directories unless the user explicitly confirms.
- Do not create or modify MCP configuration without first explaining the reason, content, commands, permissions, and risks.

## GitHub Agent Workflow

- For repository changes intended to reach GitHub, use an auditable Issue -> branch -> PR -> CI -> review -> merge flow.
- Start from a GitHub Issue that states the agent, goal, allowed files/directories, constraints, and acceptance criteria.
- Create a task branch for agent work; do not commit directly to `main`.
- Keep PR changes within the issue-approved scope. If the scope changes, update the issue or ask the maintainer before editing more files.
- Run repository hygiene, commit email, task structure, and tests before asking for review:
  - `python scripts/check_repository_hygiene.py`
  - `python scripts/check_commit_emails.py`
  - `python scripts/check_task_structure.py`
  - `python -m unittest discover -s tests`
- Do not commit secrets, credentials, private data, personal email addresses, or local absolute paths.
- Do not claim Codex or Claude contributor attribution unless there are real agent-authored commits intended to enter the default branch.
- `Co-Authored-By` trailers must use maintainer-approved identities. Do not invent agent identities.
- Branch protection and required checks must be configured by a maintainer or only after explicit maintainer confirmation.

## Scripts

- Maintainable first-party scripts should use: `NN_verb_object_context.ext`.
- Examples: `01_check_project_structure.ps1`, `02_build_task_index.py`.
- Put historical or risky scripts under `90_legacy/` and prefix them with `90_legacy_`.
- Do not rename third-party repositories, downloaded packages, or unpacked skill internals just for neatness.

## End-Of-Task Report

At the end of each task, report:

- Directly openable deliverable links
- Files created
- Files modified
- Files moved
- Files not handled
- External path risk
- Verification results

## Deliverable Links

- At the end of each task, provide directly openable or copyable entry points for the user.
- If the task creates or updates a GitHub Issue, PR, Release, Actions run, repository page, deployment, or hosted page, include the URL.
- If the task creates or updates important local files, include clickable absolute path links. Do not provide only relative paths or bare filenames for key deliverables.
- If the task creates HTML pages, images, PDFs, slide decks, reports, scripts, exports, or generated assets, group the entry points by type and explain where to view or open them.
- If there are many outputs, list only the most important entry points and point to the full manifest in `notes.md`, `TASKS.md`, or a report file.
- If a local dev server was started, include the local URL. If it was stopped, say so.
- If visual artifacts were generated and can be displayed, show them in the final report or provide clickable absolute paths.

# Agent Workspace Template

这是一个面向 Codex、Claude 和其他本地 Agent 的轻量工作区模板。

目标很简单：让每一次 Agent 任务都留在本地项目内，目录清楚、过程可追踪、结果可迁移。

除非用户明确要求其他语言，本模板默认要求 Agent 使用中文回复、中文任务记录和中文说明文档。

## 这个模板提供什么

- Codex 项目规则文件：`AGENTS.md`
- Claude 项目规则文件：`CLAUDE.md`
- 每个任务一个独立目录：`01_tasks/`
- 任务内清晰编号：素材、产出、日志、临时文件各归其位
- 跨任务复用资料区：`02_shared/`
- 待归类、归档、临时文件区
- 无需 clone 也能让 Agent 创建结构的 `docs/bootstrap-prompt.md`

## 目录结构

```text
agent-workspace-template/
├─ AGENTS.md
├─ CLAUDE.md
├─ README.md
├─ TASKS.md
├─ .gitignore
├─ 01_tasks/
│  └─ 00_template/
│     ├─ prompt.md
│     ├─ notes.md
│     ├─ 01_assets/
│     ├─ 02_output/
│     ├─ 03_logs/
│     └─ 04_tmp/
├─ 02_shared/
│  ├─ 01_docs/
│  ├─ 02_scripts/
│  └─ 03_assets/
├─ 03_inbox/
├─ 04_archive/
├─ 05_tmp/
└─ docs/
   ├─ bootstrap-prompt.md
   ├─ codex-usage.md
   ├─ claude-usage.md
   └─ migration.md
```

## 使用方式

方式一：作为 GitHub Template Repository 使用。

方式二：直接 clone：

```powershell
git clone <repo-url> my-agent-workspace
```

方式三：把 `docs/bootstrap-prompt.md` 复制给 Codex 或 Claude，让它直接在当前目录创建同样结构。

## 新任务规则

每个新任务创建一个目录：

```text
01_tasks/YYYY-MM-DD-HHMM-short-task-name/
```

每个任务目录包含：

```text
prompt.md
notes.md
01_assets/
02_output/
03_logs/
04_tmp/
```

如果当前对话只是同一主题继续，就复用已有任务目录，不要创建新的时间戳目录。

## 安全规则

默认只允许 Agent 在当前工作区内部写入文件。不要写入全局 `.codex`、`.claude`、`.agents`、桌面、下载、文档、系统目录或任何项目外路径，除非用户明确确认。

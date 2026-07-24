# Agent Workspace Template

这是一个面向 Codex、Claude 和其他本地 Agent 的轻量工作区模板。

目标很简单：让每一次 Agent 任务都留在本地项目内，目录清楚、过程可追踪、结果可迁移。

除非用户明确要求其他语言，本模板默认要求 Agent 使用中文回复、中文任务记录和中文说明文档。

## 外部输入文件

如果用户在对话中明确上传、拖入、粘贴，或给出某个外部文件的完整路径，Agent 可以只读读取这个文件作为本次任务输入。正确流程是：只读取用户明确提供的那个文件，把它复制到当前任务目录的 `01_assets/01_input/`，后续处理基于项目内副本进行，所有产出仍写入当前任务目录。

Agent 不应修改、移动、删除外部原文件，也不应扫描外部父目录或批量读取同目录其他文件。若路径不清楚、权限不确定、文件可能敏感，或需要读取一整个外部目录，必须先向用户确认。

## 这个模板提供什么

- Codex 项目规则文件：`AGENTS.md`
- Claude 项目规则文件：`CLAUDE.md`
- 每个任务一个独立目录：`01_tasks/`
- 任务内清晰编号：素材、产出、日志、临时文件各归其位
- 跨任务复用资料区：`02_shared/`
- 待归类、归档、临时文件区
- 无需 clone 也能让 Agent 创建结构的 `docs/bootstrap-prompt.md`

## GitHub Agent 协作

本仓库支持 Codex、Claude 或其他 Agent 通过 GitHub 进行可审计协作。推荐流程：

```text
Issue -> branch -> PR -> CI -> review -> merge
```

新增 Agent 任务时，优先使用 `.github/ISSUE_TEMPLATE/agent-task.yml` 说明 agent、目标、允许修改范围、约束和验收标准。PR 应使用 `.github/pull_request_template.md` 记录关联 issue、验证结果、隐私检查和 contributor attribution 情况。

CI 会运行：

```powershell
python scripts/check_repository_hygiene.py
python scripts/check_commit_emails.py
python -m unittest discover -s tests
```

Codex 和 Claude 只有在各自产生真实提交并进入默认分支后，才可能成为 GitHub Contributors。不要伪造 Agent 身份或随意添加未确认的 `Co-Authored-By`。

## 交付物入口

每次任务结束时，Agent 不应只说“生成了哪些文件”，还应该告诉用户“从哪里直接打开”。关键产物必须给可点击入口。

常见入口包括：

- GitHub PR、Issue、Actions、Release、仓库或部署页面 URL。
- 本地报告、HTML、图片、PDF、PPTX、脚本和导出文件的绝对路径链接。
- 本地服务的 URL，例如 `http://127.0.0.1:3000`。
- 完整文件清单所在的 `notes.md`、`TASKS.md` 或审计报告。

如果产物很多，只列最重要的入口，避免把最终汇报变成文件瀑布。

## 目录结构

```text
agent-workspace-template/
├─ AGENTS.md
├─ CLAUDE.md
├─ README.md
├─ TASKS.md
├─ .gitignore
├─ .github/
│  ├─ ISSUE_TEMPLATE/
│  │  └─ agent-task.yml
│  ├─ pull_request_template.md
│  └─ workflows/
│     └─ tests.yml
├─ scripts/
│  ├─ check_commit_emails.py
│  └─ check_repository_hygiene.py
├─ tests/
│  ├─ test_commit_emails.py
│  └─ test_repository_hygiene.py
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

其中 `YYYY-MM-DD-HHMM` 必须使用当前本机日期时间，不要使用 `0000` 或 `HHMM` 这类占位符；除非任务确实在零点开始。`short-task-name` 建议使用简短英文 slug，左侧会话标题可以使用中文。

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

## 会话标题规则

Codex 左侧会话标题建议使用“星标 + 短任务名”，不要使用日期时间或很长的首句请求。日期时间只放在任务目录名里。

星标规则：

- `⭐`：临时验证、小实验、一次性轻量任务。
- `⭐⭐`：普通测试任务。
- `⭐⭐⭐`：重要项目任务、可复用能力开发、正式工作流测试。
- `⭐⭐⭐⭐`：工作区规则、模板、系统级整理或迁移。
- `⭐⭐⭐⭐⭐`：长期主线、核心生产流或高优先级项目。

推荐新会话首句：

```text
会话标题：⭐⭐⭐短任务名
任务名：short-task-name

目标：……
请按当前工作区规则创建或复用任务目录，默认中文输出。
```

如果 Codex 当前环境能定位会话并提供重命名工具，agent 应主动把左侧标题改为上述格式；如果工具不可用或无法定位当前会话，则由用户手动重命名。无论左侧标题是否成功修改，文件产出仍必须按 `01_tasks/YYYY-MM-DD-HHMM-short-task-name/` 规则保存。

## 安全规则

默认只允许 Agent 在当前工作区内部写入文件。不要写入全局 `.codex`、`.claude`、`.agents`、桌面、下载、文档、系统目录或任何项目外路径，除非用户明确确认。

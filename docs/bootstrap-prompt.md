# Bootstrap Prompt

当你不想 `git clone`，而是希望 Codex、Claude 或其他本地 Agent 直接在当前目录创建这套工作区时，复制下面这段 prompt。

```text
请把当前目录初始化为一个本地 Agent 工作区。

硬性边界：
- 只能在当前目录内部创建或修改文件。
- 不要写入全局 `.codex`、`.claude`、`.agents`、桌面、下载、文档、系统目录或当前目录外路径。
- 未经我明确确认，不要创建或修改 MCP 配置。
- 不要执行全局安装命令。
- 除非我明确要求其他语言，回复、说明文档、任务记录和最终报告默认使用中文。

请创建这个结构：

AGENTS.md
CLAUDE.md
README.md
TASKS.md
.gitignore
01_tasks/
  00_template/
    prompt.md
    notes.md
    01_assets/
      01_input/
      02_reference/
      03_working/
    02_output/
      01_final/
      02_reports/
      03_exports/
      90_working/
    03_logs/
      01_runs/
      90_tool-state/
    04_tmp/
02_shared/
  01_docs/
  02_scripts/
  03_assets/
03_inbox/
04_archive/
05_tmp/
docs/
  bootstrap-prompt.md
  codex-usage.md
  claude-usage.md
  migration.md

请写入 AGENTS.md 和 CLAUDE.md 的核心规则：
- 每个新任务使用 `01_tasks/YYYY-MM-DD-HHMM-short-task-name/`。
- 同一主题继续时复用同一个任务目录，不要重复创建时间戳目录。
- 每个任务目录包含 `prompt.md`、`notes.md`、`01_assets/`、`02_output/`、`03_logs/`、`04_tmp/`。
- 会话标题尽量使用“星标 + 短任务名”，例如 `⭐⭐⭐stata-skill`、`⭐⭐⭐⭐project-workflow`、`⭐officecli-smoke-test`。
- 星标含义：`⭐` 临时轻量任务；`⭐⭐` 普通任务；`⭐⭐⭐` 重要项目任务；`⭐⭐⭐⭐` 工作区或系统级任务；`⭐⭐⭐⭐⭐` 长期主线或核心生产流。
- 如果用户首条消息写明 `会话标题：...`，优先采用该标题；如果工具无法自动重命名左侧会话，则提示用户手动重命名，但继续按目录规则执行。
- 输入和参考资料放入 `01_assets/`。
- 最终产出、报告和导出文件放入 `02_output/`。
- 日志和工具状态放入 `03_logs/`。
- 临时文件放入任务内 `04_tmp/` 或根目录 `05_tmp/`。
- 可复用文档、脚本、素材分别放入 `02_shared/01_docs`、`02_shared/02_scripts`、`02_shared/03_assets`。
- 任务结束时必须汇报新增文件、修改文件、移动文件、未处理文件、外部路径风险和验证结果。

创建完成后，请输出最终目录树，并确认没有向当前目录之外写入任何文件。
```

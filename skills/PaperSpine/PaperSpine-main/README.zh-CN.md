# PaperSpine

[English](README.md) | 中文

PaperSpine 是一个以 motivation 为主线的论文/报告写作 skill suite，面向期刊论文、会议论文、课程报告、技术报告、综述、数学建模/竞赛论文等任务。

它不是一个“一键润色 prompt”。PaperSpine 的目标是让 AI 先调研目标场景、学习优秀样例、确认全文核心动机，再逐段设计写作逻辑，最后生成 LaTeX 成果并完成审计。

## 核心思想

PaperSpine 遵循一个原则：

> 先学习，再写作。

它希望帮助用户看到一篇文章为什么这样写：动机如何提出，证据如何支撑，章节如何展开，修改为什么有效。

## 主要能力

- 支持四类目标场景：`journal`、`conference`、`report/review`、`competition`。
- 支持两档研究深度：`flash` 和 `pro`。
- 支持两条主流程：改进已有初稿，或从素材文件夹从零构筑。
- 支持最终输出英文或中文。
- 在调研后强制确认核心 motivation。
- 强制生成 `writing_rationale_matrix.md`，逐段解释写作设计。
- 强制输出 LaTeX：`paper_rewriting_output/final_paper/main.tex`。
- 本机有 TeX 编译器时尝试生成 PDF。
- 可选生成 Word，并用 `word_guard.py` 检查。
- 英文产物生成后可选完整中文翻译包。
- 提供带欢迎页、方向键操作和自动预填字段的终端 UI。

## 仓库结构

PaperSpine 同时支持 Codex 和 Claude Code，但两者安装结构不同。

```text
codex/paper-spine/        Codex 单 skill 版本
skills/                   Claude Code 扁平 skill suite
commands/                 Claude Code slash command 辅助入口
.claude-plugin/           Claude Code 插件元数据
scripts/                  共享脚本
references/               共享流程参考
tests/                    本地硬化测试
```

仓库根目录刻意不放顶层 `SKILL.md`，避免被宿主重复识别成一个泛化 skill。

## Codex 安装

Codex 推荐安装单个官方风格 skill：

```text
codex/paper-spine
```

Windows PowerShell：

```powershell
git clone https://github.com/WUBING2023/PaperSpine.git "$HOME\PaperSpine"
New-Item -ItemType Directory -Force -Path "$HOME\.codex\skills"
Copy-Item -Recurse -Force "$HOME\PaperSpine\codex\paper-spine" "$HOME\.codex\skills\paper-spine"
```

macOS/Linux：

```bash
git clone https://github.com/WUBING2023/PaperSpine.git ~/PaperSpine
mkdir -p ~/.codex/skills
cp -R ~/PaperSpine/codex/paper-spine ~/.codex/skills/paper-spine
```

重启 Codex 后调用：

```text
$paper-spine
```

期望结构：

```text
~/.codex/skills/paper-spine/SKILL.md
~/.codex/skills/paper-spine/references/
~/.codex/skills/paper-spine/scripts/
```

Codex 版本是一个自包含 skill，避免多个子 skill 在 Codex 中重复发现或触发不稳定。

## Claude Code 安装

Claude Code 推荐使用插件结构或扁平 skill suite。不要把 `codex/paper-spine` 当作 Claude Code 插件安装。

### 插件安装

```text
/plugin marketplace add https://github.com/WUBING2023/PaperSpine
/plugin install paper-spine
/reload-plugins
```

插件会提供这些 suite skills：

```text
paper-spine
paper-spine-intake
paper-spine-research
paper-spine-rewrite
paper-spine-build
paper-spine-latex
paper-spine-audit
```

### 扁平 skill 兜底安装

如果不使用插件系统，可以把每个 skill 直接复制到 `~/.claude/skills/`：

```bash
git clone https://github.com/WUBING2023/PaperSpine.git ~/PaperSpine
mkdir -p ~/.claude/skills ~/.claude/commands
cp -R ~/PaperSpine/skills/* ~/.claude/skills/
cp ~/PaperSpine/commands/*.md ~/.claude/commands/
```

Windows PowerShell：

```powershell
git clone https://github.com/WUBING2023/PaperSpine.git "$HOME\PaperSpine"
New-Item -ItemType Directory -Force -Path "$HOME\.claude\skills", "$HOME\.claude\commands"
Copy-Item -Recurse -Force "$HOME\PaperSpine\skills\*" "$HOME\.claude\skills\"
Copy-Item -Force "$HOME\PaperSpine\commands\*.md" "$HOME\.claude\commands\"
```

期望结构：

```text
~/.claude/skills/paper-spine/SKILL.md
~/.claude/skills/paper-spine-intake/SKILL.md
~/.claude/skills/paper-spine-research/SKILL.md
~/.claude/commands/paperspine.md
```

重启 Claude Code 后推荐调用：

```text
/paperspine
```

`/paperspine` 会启动 PaperSpine，并在缺少配置时自动打开 intake UI。`/paperspine-ui` 只作为手动/兼容入口保留。

## Codex 与 Claude Code 的差异

| 宿主 | 推荐结构 | 主要调用方式 | 原因 |
|---|---|---|---|
| Codex | `codex/paper-spine` | `$paper-spine` | 单个自包含 skill 更稳定，避免重复发现。 |
| Claude Code | 插件根目录或 `skills/*` 扁平安装 | `/paperspine` 或 `paper-spine` skill | Claude Code 按扁平目录发现 skill，也可以使用 slash command 辅助入口。 |

## Intake UI

Claude Code 中 `/paperspine` 会在真实 PowerShell 窗口中打开终端 UI，避免隐藏工具执行环境卡在 `stdin`。

键盘操作：

- `↑/↓`：切换字段。
- `←/→`：切换选项。
- `Enter`：编辑或确认。
- `S`：保存。
- `Q`：退出。

UI 会尽量自动读取当前项目中的初稿路径、素材文件夹、URL 和常见特殊要求，用户再进行修改。

视觉预览：

```bash
python scripts/tui_preview_server.py --port 8765
```

然后打开 `http://127.0.0.1:8765` 和 `http://127.0.0.1:8765/config`。

## 工作流

### 改进已有初稿

适合已经有论文初稿的情况。PaperSpine 会生成：

- `original_logic_map.md`
- `research_dossier.md`
- `motivation_options_after_research.md`
- `confirmed_motivation.md`
- `section_blueprints.md`
- `writing_rationale_matrix.md`
- `rewrite_matrix.md`
- `logic_transfer_audit.md`
- `final_paper/main.tex`

### 从素材从零构筑

适合已有实验设置、结果图片、数据、技术说明、调研笔记、PDF、Word 或部分草稿，但还没有完整论文的情况。

PaperSpine 会生成：

- `source_inventory.md`
- `evidence_bank.md`
- `figure_asset_map.md`
- `claim_register.md`
- `research_dossier.md`
- `section_blueprints.md`
- `writing_rationale_matrix.md`
- `final_paper/main.tex`

## 研究深度

- `flash`：3 篇目标场景样例、3 篇同领域样例、官方要求。
- `pro`：6 篇目标场景样例、6 篇同领域样例、官方要求。

官方要求可以来自期刊作者指南、会议 CFP、学校/学院页面、课程 rubric、竞赛官网、规则书、模板和官方通知。

## 最终产物

PaperSpine 把 LaTeX 作为最终必须产物：

```text
paper_rewriting_output/
  final_paper/
    main.tex
    paper.pdf        # 本机有 TeX 编译器时
    paper.docx       # 可选
    figures/
  latex_report.md
  word_report.md     # 请求 Word 输出时
  final_artifact_manifest.md
```

如果没有 TeX 编译器，也必须输出 `main.tex`，并在 `latex_report.md` 说明跳过编译。

## 验证

运行测试：

```bash
python -m unittest discover -s tests
```

检查产物：

```bash
python scripts/artifact_check.py paper_rewriting_output --markdown --write
```

可选检查：

```bash
python scripts/latex_guard.py paper_rewriting_output/final_paper/main.tex --markdown
python scripts/word_guard.py paper_rewriting_output/final_paper/paper.docx --markdown
```

## 本地开发同步

维护者可以运行：

```powershell
python scripts\sync_local_installs.py --clean-legacy
```

该命令会导出 Codex/Claude Code 发布结构，并同步本机开发安装。

## 许可证

MIT License。见 [LICENSE](LICENSE)。

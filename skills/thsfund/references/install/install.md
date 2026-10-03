# install runbook

> 公共约定见 SKILL.md §2，全局禁止事项见 §3。
>
> 本文件是 thsfund skill 的「安装」+「更新/重装」双角色 runbook。
> - **首次安装场景**：用户的 Agent 按上游 URL runbook执行完步骤 1-2（下载 bundle + 拷贝 skill 到 `<skills 目录>/`）后，install.md 已在文件系统上。Agent 用 Read 工具直接读取本文件（**无需重启会话、无需等 Skill 工具加载**），继续执行 §2 SDK 安装。
> - **更新/重装场景**：已安装 thsfund skill 的用户输入「重装 / 更新 / 部署 / 升级爱基金 skill」，Agent 通过 SKILL.md §1 路由表命中 install 意图，读本文件并重新安装 SDK（升级到 bundle 版本）。

## §1 前置要求

- Python 3.7+
- skill 已被拷贝到 `<skills 目录>/thsfund/`：
  - 首次安装场景：由上游 URL runbook 步骤 2 完成（包含清理旧的 5 个分散版 fund-* skill），Agent 拷贝完直接进入本文件
  - 更新/重装场景：由用户保证（用户输入「重装 / 更新」时已假定 skill 在位）

> 注：旧的 5 个分散版 skill（`fund-holding-list`、`fund-purchase`、`fund-redeem`、`fund-trade-query`、`fund-trade-revoke`）由 URL runbook 步骤 2 一并清理；install.md 不重复清理逻辑。

## §2 步骤 A · 安装 aijijin-sdk

> 本节假定 `thsfund/` 已被拷贝到 `<skills 目录>/`。首次安装场景下，bundle 下载与 skill 拷贝见上游 URL runbook。

执行：

```bash
# Windows (Git Bash / PowerShell)
pip install "<skills_dir>\thsfund\vendor\aijijin_sdk-<version>-py3-none-any.whl"

# macOS / Linux
pip install "<skills_dir>/thsfund/vendor/aijijin_sdk-<version>-py3-none-any.whl"

aijijin --version
```

**常用 AI Client 的 Skills 路径如下：**

\- Claude Code: `~/.claude/skills/`

\- Cursor: `~/.cursor/skills/`

\- Windsurf: `~/.codeium/windsurf/skills/` 或项目下 `.windsurf/skills/`

\- Codex: `~/.codex/skills/` 或项目下 `.agents/skills/`

\- Google Antigravity: `~/.gemini/antigravity/skills/`

\- Gemini CLI: `~/.gemini/skills/`

\- QoderWork: `~/.qoderwork/skills/`

\- workbuddy: `~/.workbuddy/skills/`

**判定**：`aijijin --version` 成功打印版本号即安装成功。

- 若 `pip install` 失败（whl 损坏、Python 版本不兼容），停下向用户报告。
- 若 `aijijin` 命令找不到（不在 PATH），提示重新安装或将 Scripts 加入 PATH，**停下**等用户处理后再重试。

## §3 完成汇报

全部步骤成功后向用户汇报：

1. SDK 版本号（§2 `aijijin --version` 打印的值）
2. skill 安装路径（即 `<skills_dir>/thsfund/`，由上游 URL runbook 或本地拷贝完成）
3. 「首次安装场景：5 类业务意图（持仓/申购/赎回/查询/撤单）现在可用」

## §4 错误处理汇总

| 步骤 | 触发条件 | 动作 |
|---|---|---|
| §2 | pip install 失败 | 停下向用户报告错误 |
| §2 | `aijijin` 不在 PATH | 提示重新安装或加 PATH，停下等用户 |

## 附录 A · Windows PowerShell 替代命令

Git Bash 默认带 `pip` + `aijijin`。若用户坚持 PowerShell：

```powershell
pip install "<skills_dir>\thsfund\vendor\aijijin_sdk-<version>-py3-none-any.whl"
aijijin --version
```

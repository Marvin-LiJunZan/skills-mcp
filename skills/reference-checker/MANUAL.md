# Reference Checker (文献核验助手) 使用手册

本手册详细介绍了如何使用 `reference-checker` 工具进行论文引用一致性、格式合规性与真伪闭环排查。

---

## 1. 安装与环境要求

- **Python 版本**: Python 3.8+ (已全面兼容 Python 3.13)
- **依赖说明**: 本工具仅依赖 Python 标准库（`re`, `os`, `sys`, `json`, `argparse`），**无需安装任何额外第三方 pip 包**，在任何离线科研服务器或 Windows 本地均可直接运行。

---

## 2. 常见问题排查与修复流程

### 问题 1: 文中引用缺失对应文献 (Missing in Reference List)
- **现象**: 正文中出现了 `\cite{wang2023pinn}` 或 `[15]`，但在文末参考文献列表中并未找到对应条目。
- **原因**: 删改正文时误引入未定义键，或未将最新的 `.bib` 条目编译更新。
- **修复**: 在 `.bib` 文件或文末 `\bibitem` 中补齐该文献，或运行 `cite-verify` 检索补齐元数据。

### 问题 2: 孤儿文献 (Orphan References)
- **现象**: 参考文献列表中列出了某篇文献，但全文正文没有任何一处提及该文献。
- **影响**: 期刊排版初筛（Technical Screening）会直接据此打回（Desk Reject）。
- **修复**: 删除多余的参考文献条目，或在对应综述/讨论段落中补充引用。

### 问题 3: 引用序号非单调递增 (Non-Monotonic Citation Order)
- **现象**: 正文第一章先引用了 `[3]`，后续段落才首次出现 `[1]` 或 `[2]`。
- **修复**: 重新排序参考文献条目，保证正文首次出现的引文按 `1, 2, 3...` 顺序编号。

---

## 3. 命令行调用参考

```powershell
# 1. 基础语法核对
python scripts/reference_checker.py --tex "paper/main.tex"

# 2. 生成 JSON 格式核验报告
python scripts/reference_checker.py --tex "paper/main.tex" --json-output "audit_report.json"
```

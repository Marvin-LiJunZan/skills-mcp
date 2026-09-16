---
name: reference-checker
description: "Reference audit and integrity checker: verifies bijective cross-referencing between in-text citations and bibliography lists, checks citation style compliance (GB/T 7714, APA, IEEE, Elsevier), and detects broken reference chains."
metadata:
  short-description: "Bijective reference cross-check and citation formatting auditor"
---

# Reference Checker — 文献核验助手

Reference Checker 是专门用于学术论文参考文献规范化与真伪核查的轻量化自动化工具，解决论文写作中最常被审稿人诟病的“文中有引、文后无源”、“文后有源、文中未引”、“引文序号错位”、“格式混乱污染”等问题。

---

## 核心核验能力

1. **双向全射闭环核查 (Bijective Cross-Check)**:
   - 文中所有引用标签（如 `\cite{...}`, `(Author, Year)`, `[1]`）必须 100% 存在于参考文献列表中。
   - 参考文献列表中的每一条条目必须在正文中至少被引用过一次（清除孤立文献/冗余条目）。

2. **多期刊与国标规范合规检查**:
   - **Elsevier Numbered**: `Initials. Surname`, ISO-4 期刊缩写, 无 GB/T 标识符。
   - **GB/T 7714-2015**: 顺序编码制与著者-出版年制，文献类型标志 `[J]`, `[M]`, `[C]` 规范核验。
   - **IEEE**: 方括号数字编号 `[1]`，严格按照文中出现次序单调递增。
   - **APA 7th**: `(Surname, Year)` 著者年制，三位作者及以上首次即使用 `et al.`。

3. **序号单调性与防断行检查**:
   - 连续引用按出现顺序单调增加（防止正文中先出现 [5] 后出现 [4]）。
   - 检查正文 `~` 不换行空格绑定（防止行尾单独断行掉落孤儿引用标号）。

---

## 快速使用指令

```powershell
# 核查 LaTeX 手稿中的引用对应关系
python scripts/reference_checker.py --tex "manuscript.tex"

# 核查 Markdown 或文本格式论文
python scripts/reference_checker.py --md "paper.md"
```

完整使用与故障排查说明请参阅 [MANUAL.md](MANUAL.md)。

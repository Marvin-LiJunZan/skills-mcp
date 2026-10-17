---
name: scan-project-merger
description: Batch merge and rotate scanned engineering project documents (e.g., labor/equipment cost allocations, timesheets, RD reports), auto-orient landscape tables to upright, extract project metadata, and triage into scan originals, markdown summaries, and merged PDFs.
---

# Scan Project Merger Skill

本技能专用于工程科研课题、横向课题、高新申报中**多批次扫描件的自动化归类、正向纠偏、按项目合并与文档归档**。

## 典型应用场景
1. **财务与科研工时分摊表合并**：如《研发费用—职工薪酬分摊明细表》、《研发人员科研工时安排表/考勤表》。
2. **多批次扫描方向混乱**：原始扫描仪进纸方向不一（部分顺时针旋转90°，部分逆时针旋转270°），表格倒置或坚放，需要统一校准为正向横向（Landscape A4 841.7 × 595.2 pt）。
3. **按项目/课题自动归集**：从杂乱的 `scan_YYYYMMDDHHMMSS.pdf` 自动按课题合同编号、项目简称归并，并按年月时序严谨重组。
4. **规范的三分法归档**：
   - `scan原件/`：完整保存原始高保真扫描文件（不破坏原始记录与电子签名）。
   - `md件/`：生成结构化 Markdown 档案（包含项目全称、合同号、统计区间、人员名单、审计勾稽说明）。
   - `合并好的pdf/`：输出标准命名（`研发人员及设备、无形资产的分配+<项目简称>.pdf`）的正向终稿。

---

## 核心脚本与调用方式

技能内置通用处理脚本位于：
`C:\JunzanLi_project\skills_mcp\skills\scan-project-merger\scripts\merge_scans.py`

### 1. 基础快速调用（在目标目录直接执行）
```bash
python "C:\JunzanLi_project\skills_mcp\skills\scan-project-merger\scripts\merge_scans.py" --work-dir "C:\JunzanLi_project\课题申报横向\王汉东\按项目合并"
```

### 2. 参数说明
- `--work-dir`: 待处理的工作目录（默认为当前目录）。
- `--auto-orient`: 自动检测并校正文字/表格朝向（默认为 True）。
- `--organize-folders`: 自动归入 `scan原件/`、`md件/`、`合并好的pdf/`（默认为 True）。
- `--generate-md`: 同步生成科研档案与审计对账 Markdown 说明（默认为 True）。

---

## 质量核查与审计准则
1. **页面方向验证**：合并后的每页 PDF 打开后表头必须水平置顶，手写签字及财务印章必须正向可读。
2. **多部门独立核算**：同一课题若存在“公司本部科研组”与“现场总包部项目部”（如长距离轨行区本部 vs 十八和二十二号线总承包部），应保持独立子账目 PDF，不得盲目交叉混拼，确保审计穿透核查。
3. **空白页排查**：自动检测过滤因进纸感应异常生成的灰底/纯白废页（如容量小于 5KB 的异常单页扫描）。

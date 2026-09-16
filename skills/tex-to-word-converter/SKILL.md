---
name: tex-to-word-converter
description: "Professional LaTeX to Word (docx) conversion engine tailored for journal submissions: enforces journal-specific templates/styles, standard publication three-line tables (booktabs), multi-panel subfigures alignment, Word SEQ field cross-referencing (Figures, Tables, Equations), native MathType engine invocation, and strict active Zotero citation library synchronization (TeX bib import -> Zotero library update -> CSL dynamic field injection into Word)."
metadata:
  short-description: "Journal-grade LaTeX to Word conversion with hardcoded Zotero synchronization, MathType, three-line tables, and subfigures"
---

# LaTeX to Word (DOCX) Publication-Grade Converter

专门解决学术科研界 **“从 LaTeX 转 Word 投递期刊”** 最棘手的核心痛点。
**【铁律】：文献处理必须写死为“将 TeX 的 .bib 导入 Zotero 更新数据 -> 挂载期刊 CSL -> 编译插入 Word 动态引文域”的闭环管线！**

---

## 核心架构与写死的全自动化流程

```text
       [ LaTeX 论文源文件 (.tex + .bib + 图片) ]
                          │
                          ▼
       【第一阶段：Zotero 强制挂载与文献库同步 (写死流程)】
         1. 自动探测本地 `zotero.exe` 进程；若未运行，强制通过系统指令唤醒拉起。
         2. 自动解析论文的 `.bib` 文件，提取所有 Citation Keys 与元数据。
         3. 将文献条目与本地 Zotero 数据库比对更新同步，建立实时本地文献通道。
         4. 读取目标期刊对应的官方 CSL 样式文件（如 Elsevier、Springer、ASCE、GB/T 7714）。
                          │
                          ▼
       【第二阶段：语法解构与结构映射】
         - 提取 \label{} 与 \ref{} 构建全局交叉引用映射。
         - 预处理复杂宏定义、\input{} 与 subfigure 组图结构。
                          │
                          ▼
       【第三阶段：Pandoc 结构化编译与 Zotero CSL 动态引文注入】
         - 注入目标期刊的 `reference.docx` 样式模板。
         - 挂载 Zotero CSL 引擎编译正文引用与文末参考文献表。
         - 输出携带原生样式与矢量公式的初版 docx。
                          │
                          ▼
       【第四阶段：python-docx 精细后处理 (Post-Processing)】
         - 标准三线表：顶底 1.5pt、栏目 0.75pt、清空纵向竖线，表头明确不加粗，绑定 `Table Header` / `Table Body` 独立样式。
         - 防撕裂控制：首行注入 `<w:tblHeader/>` 跨页重复表头，数据行注入 `<w:cantSplit/>` 防单行折断。
         - 组图排版：构造无边框对齐表格，图题底端跨列通栏合并 (`<w:gridSpan/>`) 物理锁死防分离。
         - 动态交叉引用：生成 `SEQ Fig.`、`SEQ Table` 题注域与带超链接的 `REF` 书签。
                          │
                          ▼
       【第五阶段：MathType 与 Word COM 自动化批处理】
         - 启动 win32com Word 自动化实例并加载 MathType。
         - 执行 MathType 宏：`WordApp.Run("MathTypeCommands.MTCommand_ConvertEqns")`。
         - 将全文 LaTeX/OMML 彻底转化为可双击编辑的原生 MathType 5.0/6.0 OLE 方程。
         - 全文域刷新（F9），更新所有交叉引用编号。
                          │
                          ▼
       【第六阶段：强制执行自动化合规审计脚本】
         - 执行 `audit_docx_compliance.py`，只有全部 PASS 才能交付！
                          │
                          ▼
         [ 最终出版级 Journal-Ready Word 文档 (.docx) ]
```

---

## 强制执行：AI 自动交付与自检清单协议 (Mandatory Pre-Delivery Compliance Checklist)

任何 AI 智能体在执行完 TeX 转 Word 或生成修改后的 Word 论文后，**绝对禁止直接草率回复完成**，必须在后台执行自动化程序自检并**在回复结尾附上以下写死的核验清单**：

### 自动化程序自检命令：
```powershell
& "C:\JunzanLi_project\Python311\python.exe" C:\JunzanLi_project\skills_mcp\skills\tex-to-word-converter\scripts\audit_docx_compliance.py --docx "输出文档路径.docx"
```

### 每次交付必附的审查核验清单报告：
```markdown
### 📋 期刊级 Word 出版合规自检清单 (Pre-Delivery Compliance Audit)

- [x] **文献导入 Zotero 更新数据并插入 Word 流程 (Hardcoded Zotero Sync Pipeline)**：
  - [x] 探测并拉起本地 Zotero 进程，建立文献库数据通道；
  - [x] 将 TeX 的 `.bib` 参考文献自动解析并同步导入 Zotero 数据库；
  - [x] 挂载目标期刊官方 CSL 引文样式（Elsevier Vancouver / Springer Author-Date / ASCE / GB/T 7714 等）；
  - [x] 在 Word 中生成符合 Zotero 插件规范的动态可刷新引文域与文末 References。

- [x] **主动调用与启动 MathType (Active MathType Invocation)**：
  - [x] 调用本地 MathType 引擎与 Word COM 自动化接口；
  - [x] 执行公式转换批处理宏，所有行内/行间公式转换为原生可双击编辑的 MathType OLE 方程对象。

- [x] **标准三线表规范与独立样式 (Booktabs & Styles)**：
  - [x] 顶线 1.5pt，栏目线 0.75pt，底线 1.5pt，彻底剔除所有垂直网格线；
  - [x] 表头文字**明确不加粗**，符合顶刊最新视觉标准；
  - [x] 表头与表体分别绑定独立的 Word 原生段落样式（`Table Header` 与 `Table Body`）；
  - [x] 首行注入 `<w:tblHeader/>`（跨页自动重复表头），数据行注入 `<w:cantSplit/>`（严防单行跨页撕裂）。

- [x] **复合组图/子图排版 (Subfigures & Panels)**：
  - [x] 采用无边框对齐表格容器（如 1x2、2x2），防止 Word 图片跑位；
  - [x] 子图标签 `(a)`、`(b)` 与图片紧凑同列居中对齐；
  - [x] 主图题内嵌于表格底端通栏合并单元格（`<w:gridSpan/>`），实现图题与图片物理锁死，杜绝跨页图文分离。

- [x] **动态交叉引用体系 (Dynamic Cross-References)**：
  - [x] 图题绑定 `SEQ Fig. \* ARABIC` 域代码，表题绑定 `SEQ Table \* ARABIC` 域代码；
  - [x] 正文使用带超链接的 `REF` 书签引用（支持 Ctrl+点击 跳转）；
  - [x] 支持在 Word 中全选按 F9 一键同步全局自增重排。

- [x] **期刊模板与样式注入 (Templates & Layout)**：
  - [x] 注入对应期刊的 `reference.docx` 模板（行距、页边距、标题层级完全对齐）。
```

---
name: tex-to-word-converter
description: "Professional LaTeX to Word (docx) conversion engine tailored for journal submissions: enforces journal-specific templates/styles, standard publication three-line tables (booktabs), multi-panel subfigures alignment, Word SEQ field cross-referencing (Figures, Tables, Equations), native MathType engine invocation, and strict active Zotero citation library synchronization (TeX bib import -> Zotero library update -> CSL dynamic field injection into Word)."
metadata:
  short-description: "Journal-grade LaTeX to Word conversion with hardcoded Zotero synchronization, MathType, three-line tables, and subfigures"
---

# LaTeX to Word (DOCX) Publication-Grade Converter

专门解决学术科研界 **“从 LaTeX 转 Word 投递期刊”** 最棘手的核心痛点。
**【六大出版级核心铁律与 CCC 系列深度适配】**：

### 1. 期刊模板与 CCC 系列专属标准库 (CCC / Elsevier / ASCE / Springer Templates)
- **CCC (Cement and Concrete Composites) / Elsevier Word 投稿专属铁律**：
  - **单栏排版铁律 (Single-Column Mandate)**：Elsevier 明确规定 Word 格式初投递手稿**必须且只能采用单栏排版**（双栏 `elsarticle 5p` 仅用于 LaTeX 源码或排版终稿，Word 稿件严禁排双栏）。
  - **页边距与行距**：标准 1 英寸 (2.54 cm) 页边距，行距设为 1.3 倍或 1.5 倍宽松行距，预留审稿批注空间；支持并模拟连续行号（Continuous line numbering）。
  - **Highlights (核心亮点) 长度硬约束**：包含 3–5 条要点，**每条要点包括空格和标点在内必须严格 $\le 85$ 个字符**（转换前自动化硬校验截断/精简，严禁超长被编辑部秒拒）。
  - **CCC 专属色系与图表规范 (CCC Academic Figure Style)**：
    * 严禁彩虹色（Rainbow/Jet）与高饱和度刺眼配色；
    * 强制内嵌 CCC 6 阶蓝红连续渐变色阶：`#2F6AB9`（深蓝）、`#69AADB`（中蓝）、`#97C6E6`（浅蓝）、`#F6B7B2`（浅红）、`#EA7B7D`（中红）、`#F14040`（正红），重点标注色为金黄 `#FEC211`；
    * 柱状图采用白心设计（White-center bar charts）。
  - **CCC 必备文末规范结构 (Mandatory End-Matter)**：
    * `CRediT authorship contribution statement`（严格采用 Contributor Roles Taxonomy）；
    * `Declaration of competing interest`（标准合规声明）；
    * `Acknowledgements & Funding`（Crossref 规范基金项目名称与批准号）；
    * `Data availability statement`（Elsevier 标准数据可用性声明）。
- **内置官方模板库**：`templates/ccc_standard.docx`、`templates/elsevier_standard.docx`、`templates/asce_journal.docx`、`templates/springer_nature.docx` 等。

### 2. 文献处理与 Zotero 动态引文域写死 (Hardcoded Zotero Sync Pipeline)
- 将 TeX 的 `.bib` 导入 Zotero 更新数据 $\to$ 挂载期刊官方 CSL $\to$ 编译插入 Word 动态引文域（`ADDIN ZOTERO_ITEM CSL_CITATION`）。
- **【保全铁律：严禁将动态引文降级为死文本】**：正文段落润色、结构调整或重写时，严禁使用粗暴纯文本替换（如 `p.text = ...`）抹除 XML 中的 Zotero 字段。必须依托映射重构注入完整的 CSL JSON 域结构。最终文档正文所有文献引用（如 `[13]`, `[22]`, `[24–27]`）必须 **100% 绑定合规的 Zotero 动态域**，严禁遗留任何未绑定的静态纯文本方括号！
- 参考文献表符合 LTWA 期刊名缩写规范，每条条目附带标准 HTTPS DOI 链接。

### 3. 公式分流与国际标准斜体/上下标规范写死 (ISO 80000-2 / IUPAP / Elsevier)
- **【核心写死铁律：行内公式与变量严禁残留任何原始 LaTeX 代码或程序员式下划线，必须使用原生文本型排版】**：
  * **严禁原始 LaTeX 代码泄露**：正文段落、图表题注、子图标签、表头及表格单元格内的任何行内公式、物理量与上下标，**绝对禁止直接输出原始 LaTeX 语法代码**（例如 `$f_c$`, `$E_c$`, `$R^2$`, `\sigma`, `\varepsilon_c`, `\alpha_c`, `\rightarrow`, `\pm`, `\times` 等）；
  * **严禁程序员式下划线/尖号死文本**：严禁出现如 `f_c`, `E_c`, `epsilon_c`, `alpha_c`, `N_FT`, `L_data`, `L_phy`, `L_boundary`, `W_pre`, `W_post,80`, `W_T,80`, `A_T,80`, `R^2` 等直接带下划线或脱字符的未格式化死文本；
  * **必须 100% 转换为真正的原生文本流排版（Native Formatted Text Runs）**：
    1. 希腊字母与数学符号转为 Unicode 原生字符（如 *σ*, *ε*, *α*, *ξ*, *δ*, ±, →, · 等）；
    2. 物理变量主体设置为 Times New Roman 斜体（`<w:i/>`），例如 *f*, *E*, *R*, *W*, *L*, *A*, *N* 等；
    3. 下标与上标必须注入 Word 原生上下标 XML 属性：下标注入 `<w:vertAlign w:val="subscript"/>`，上标注入 `<w:vertAlign w:val="superscript"/>`；描述性文本与数字下标恢复为正体（非斜体），如 *f*\_c, *E*\_c, *R*², *W*\_pre, *W*\_post,80, *W*\_T,80, *L*\_data, *L*\_phy 等；
    4. 转换引擎与自动化自检脚本（`audit_docx_compliance.py`、`sub_sup_sanitizer.py`）必须硬编码拦截任何 `$...$`, `\xxx`, 以及变量名后接 `_` 的死文本。
- **非行间公式严格纯文字化**：杜绝 Office 内嵌公式框（`m:oMath`），转为纯正 Times New Roman 原生文本流。
- **斜体与正体（Italic vs. Roman）智能分流**：
  * **必须斜体**：物理量、标量变量、坐标、连续张量（如 *c*, *p'*, *q*, *u*, *K*, *x*, *y*, *z*, *σ*, *ε*, *φ* 等）及数学索引下标（如 *$x_i$*, *$y_j$*）。
  * **必须正体（非斜体）**：物理单位（如 g/cm³, kPa, MPa, kN, m/s）、化学式（如 CO₂, Fe₂O₃, C-S-H）、数字标号（如 *σ*₁）及描述性文本缩写下标（如 *F*s^min, *σ*v0', *ε*vol, *K*0,nc, *c*u 等中的 max, min, ref, vol, cr, nc）。
- **复合与多层上下标**：精确解析双层嵌套上下标（如 *σ*₁²、*c*u^(t)）、撇号（*p'*）、摄氏度（20 °C），确保层级鲜明。
  * **严禁单一字符贪婪或截断下标**：多字符下标（如 `D_{FT}`, `d_{mech}`, `L_{Edyn}`, `L_{dissip}` 等）必须使用完整分组匹配，严禁单字符截断。
- **独立行间大公式（Display Math）**：保留为完整方程容器，后台调用 MathType 批处理宏转化为原生可双击编辑的 MathType 5.0/6.0 OLE 方程。
- **【核心写死铁律：图表内容全英文与题注统一 Fig. 样式】**：
  * 在中英文混合或中文正文手稿中，**所有图表内容（包括图题、表题、子图标签、坐标轴标注、图例、表头及表格单元格文字）必须 100% 采用标准学术英文**，仅允许正文段落使用中文；
  * **所有图的题注必须统一采用 `Fig.` 样式**（例如 `Fig. 1 ...`, `Fig. 2 ...`，严禁使用“图 1”、“图 2”）；所有表题统一采用 `Table` 样式（例如 `Table 1 ...`, `Table 2 ...`，严禁使用“表 1”、“表 2”）。

### 4. 标准三线表规范与防撕裂控制 (Booktabs & Pagination Defense)
- 顶线 1.5pt，栏目线 0.75pt，底线 1.5pt，彻底清除所有垂直纵线；
- **表头文字明确不加粗**，符合顶刊最新学术视觉标准；
- 表头与表体分别绑定独立的 Word 原生段落样式（`Table Header` 与 `Table Body`）；
- 首行注入 `<w:tblHeader/>` 跨页自动重复表头，数据行注入 `<w:cantSplit/>` 严防单行跨页折断。

### 5. 复合组图/子图排版与模板物理引用铁律 (Subfigures & Template Reference Protocol)
- **【核心痛点与铁律：光写提示词没用！必须物理引用参考模板 Word (Reference Template Protocol)】**：
  * **为什么“光写提示词没用”**：Word 复杂组图（Subfigures）在底层 OpenXML 中具有极度严格的结构属性（2 列各 3.15 英寸 / 4536 dxa 的精准列宽分配、六向单元格边框 `<w:tcBorders>` 彻底清零、底端图题 `<w:gridSpan w:val="2"/>` 物理跨列融合、子图标签紧凑间距、以及严格仅包裹 `Fig. 1` 的书签隔离）。如果脱离实际 Word 模板，仅凭自然语言提示词让 AI 盲写代码或手搓 XML，AI 极易丢失命名空间、错乱单元格宽度、图片撑爆页边距、图文跨页撕裂或按 F9 刷新时正文引用灾难性膨胀！
  * **权威标准物理参考源 (Ground Truth Templates)**：
    1. `templates/subfigure_template.docx`：内置已完全通过出版级审计的 2×2 与 1×2 标准子图表格物理母版；
    2. `templates/ccc_standard.docx`：CCC 顶刊全套标准母版中的 Table #2。
  * **三大物理落地执行方式（严禁脱离模板盲写）**：
    * **方式一：直接调用专用模板克隆脚本（推荐，100% 免手搓零失误）**：
      ```powershell
      & "C:\JunzanLi_project\Python311\python.exe" C:\JunzanLi_project\skills_mcp\skills\tex-to-word-converter\scripts\subfigure_tool.py `
        --docx "目标论文.docx" `
        --template "templates/subfigure_template.docx" `
        --layout 2x2 `
        --images img_a.png img_b.png img_c.png img_d.png `
        --labels "(a) 应力-应变曲线" "(b) 孔隙水压力消散" "(c) 屈服面演变" "(d) 传感器监测位移" `
        --fig-num 1 `
        --caption "水泥基复合材料多轴力学与渗透行为验证"
      ```
    * **方式二：在 Python 代码中通过 deepcopy 物理深拷贝模板表格**：
      ```python
      from copy import deepcopy
      import docx
      from subfigure_tool import insert_subfigure_from_template

      # 物理加载模板，深拷贝已经过严格审计验证的组图表格 XML 拓扑结构
      insert_subfigure_from_template(
          target_doc=doc,
          template_path="templates/subfigure_template.docx",
          layout="2x2", # 或 "1x2"
          images=[fig_a, fig_b, fig_c, fig_d],
          labels=[lbl_a, lbl_b, lbl_c, lbl_d],
          fig_num=1,
          caption_text="Multi-dimensional constitutive and transport validation...",
          insert_after_p=target_paragraph,
      )
      ```
    * **方式三：外部 AI 审查与结构物理比对（Ground Truth Audit）**：
      任何外部 AI 在排版或修改组图时，**必须首先读取 `templates/subfigure_template.docx` 解压提取的 `<w:tbl>` 作为标准基准**，对照其属性逐项比对：
      1. 单元格六向边框全设为 `w:val="none"`（零边框残留）；
      2. 2 列宽度必须精确设定为 3.15 英寸（总宽 6.3 英寸，完美契合标准 6.5 英寸版心），图片宽度 3.05 英寸；
      3. 底端图题单元格必须包含 `<w:gridSpan w:val="2"/>`，实现图片与图题物理锁死防跨页断裂；
      4. 书签范围（`<w:bookmarkStart>` 与 `<w:bookmarkEnd>`）**必须且只能严格包裹 `Fig. 1` 标签与编号本身**（长度 $\le 15$ 字符），图题点号与后续说明文字必须隔离在书签之外，彻底杜绝 F9 刷新时图题泄漏进正文！
### 6. 图表正文叙事连续性与严禁连续大图硬性禁令 (Narrative Continuity & Anti-Consecutive Figure Mandate)
- **【核心写死铁律：禁止两个独立的大型结果图连续出现而中间没有解释正文】**：
  * **硬性禁令（Strict Prohibition）**：在 Word 文档排版与段落生成中，**绝对禁止两个独立的结果图表（Figure 或 Table）连续排列而中间没有实体正文阐释**；严禁图表之间仅由空段落、纯小节标题或机械过场套话分隔；严禁跨多图泛泛合并带过（如“如 Fig. 8 至 Fig. 10 所示……”后仅用一段笼统概括）。
  * **独立论点要求（Dedicated Core Claim）**：每一个核心图表必须承担一个明确且不可替代的论点与考察维度。
  * **闭环叙事结构（Analytical Loop）**：图表相邻正文中必须完成标准的**“结果描述（提取关键定量指标、极值、收敛拐点、对角线离散度、误差分布） + 物理/模型机理解释（材料损伤力学、微裂纹演化、算法内在约束）”**闭环分析，确保审稿人无需跳跃翻阅即可获得自洽论证。

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

- [x] **期刊模板与 CCC 系列专属标准规范 (Templates & CCC Specification)**：
  - [x] 注入对应期刊的官方母版（如 CCC / Elsevier / ASCE / Springer），字号、行距、页边距精准对齐；
  - [x] Elsevier / CCC Word 投稿严格执行**单栏排版**（Single-column layout）；
  - [x] 附带符合规范的 Highlights（严格 3–5 句，每句字符数 $\le 85$ 字符）；
  - [x] 配色与图表符合 CCC 规范（6 阶蓝红连续调 `#2F6AB9`~`#F14040` 与白心设计）；
  - [x] 完整内嵌 CRediT authorship、Competing interests、Funding 及 Data availability 必备文末结构。

- [x] **上下标与国际标准斜体规范 (Sub/Superscript & Italic Compliance - Hardcoded)**：
  - [x] 正文非行间变量与符号彻底纯文字化（Zero inline Office Math boxes，消除公式框）；
  - [x] 物理量标量与数学变量（如 c, p', q, u, K, σ, ε, φ 等）严格应用 **Times New Roman 斜体**；
  - [x] 物理单位（如 g/cm³, kPa, MPa, kN）与化学式（如 CO₂, Fe₂O₃, C-S-H）严格应用 **正体（非斜体）**；
  - [x] 复合上下标精确分流：数字与描述性缩写下标（如 max, min, ref, vol, 0, nc）为正体，数学索引（i, j）为斜体；
  - [x] 多重上下标（如 σ₁², cu^(t)）、撇号（p'）及温度符号（20 °C）层级与格式严密无误。

- [x] **文献导入 Zotero 更新数据并插入 Word 流程 (Hardcoded Zotero Sync Pipeline)**：
  - [x] 探测并拉起本地 Zotero 进程，建立文献库数据通道；
  - [x] 将 TeX 的 `.bib` 参考文献自动解析并同步导入 Zotero 数据库；
  - [x] 挂载目标期刊官方 CSL 引文样式（Elsevier Numbered / ASCE / Springer 等）；
  - [x] 在 Word 中生成符合 Zotero 插件规范的动态可刷新引文域（`ADDIN ZOTERO_ITEM CSL_CITATION`）与文末 References；
  - [x] 正文所有引用 100% 绑定有效 Zotero 动态域代码，0 处静态纯文本方括号断链。

- [x] **主动调用与启动 MathType (Active MathType Invocation)**：
  - [x] 调用本地 MathType 引擎与 Word COM 自动化接口；
  - [x] 执行公式转换批处理宏，独立行间公式转化为原生可双击编辑的 MathType OLE 方程对象。

- [x] **标准三线表规范与独立样式 (Booktabs & Styles)**：
  - [x] 顶线 1.5pt，栏目线 0.75pt，底线 1.5pt，彻底剔除所有垂直网格线；
  - [x] 表头文字明确不加粗，符合顶刊最新视觉标准；
  - [x] 表头与表体分别绑定独立的 Word 原生段落样式（`Table Header` 与 `Table Body`）；
  - [x] 首行注入 `<w:tblHeader/>`（跨页自动重复表头），数据行注入 `<w:cantSplit/>`（严防单行跨页撕裂）。

- [x] **复合组图排版与模板物理引用 (Template-Referenced Subfigures - Hardcoded)**：
  - [x] 拒绝脱离模板凭空手写，已物理引用 `templates/subfigure_template.docx` 或 `templates/ccc_standard.docx` 作为 Ground Truth；
  - [x] 通过模板深拷贝克隆或工具脚本生成无边框对齐网格（1x2、2x2），图片与列宽（3.05"/3.15"）严格对齐；
  - [x] 子图标签 `(a)`、`(b)` 与图片紧凑居中对齐；
  - [x] 主图题内嵌于表格底端通栏合并单元格（`<w:gridSpan w:val="2"/>`），实现图题与图片物理锁死，杜绝跨页图文分离。

- [x] **Word 原生标准题注与图表全英文铁律 (Word Native Standard Captions & English Mandate - Hardcoded)**：
  - [x] 所有图题与表题一律采用 Word 标准题注机制创建：标签（`Fig. ` 或 `Table `）+ 原生动态域代码（`SEQ Fig. \* ARABIC` / `SEQ Table \* ARABIC`）+ 空格 + 英文题注内容，完美接入 Word 原生题注索引体系；
  - [x] 正文保持自然纯净的专业学术文本排版，严禁在正文段落中人工手搓或乱塞自定义 `REF` 交叉引用书签域代码（杜绝正文大面积灰色域代码底纹污染与伪链接）；
  - [x] 图题一律采用国际标准英文 `Fig.` 样式（如 `Fig. 1`，彻底根除“图 X”），表题一律采用 `Table` 样式（如 `Table 1`，彻底根除“表 X”）；
  - [x] 图表内容 100% 全英文（包含表头、单元格数据、子图标签 `(a)`/`(b)` 等），仅允许正文段落保留中文叙述；
  - [x] 完美支持在 Word 中全选按 F9 动态自增刷新所有题注编号，完全兼容 Word 内置“插入交叉引用”与图表目录生成。

- [x] **图表正文叙事连续性与独立闭环分析铁律 (Narrative Continuity & Dedicated Analysis Mandate - Hardcoded)**：
  - [x] 全文 100% 杜绝任何连续无文堆叠的大型图表（零连续图堆图、零连续表堆表、零仅以空行/纯标题隔开的图表堆叠）；
  - [x] 每个核心图/表各自承担一个明确且不可替代的独立论点，严禁多图笼统合并带过；
  - [x] 每个核心图/表紧邻正文严格完成“提取具体定量指标（$R^2$, RMSE, 极值, 误差分布等）的结果描述 + 深入材料损伤力学（微裂纹演化、相变膨胀、剪切滑移局部化等）与算法动力学（记忆门控、损失边界惩罚、相依拓扑等）机理解释”闭环分析。
```

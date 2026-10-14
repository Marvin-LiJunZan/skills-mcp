---
name: ccc-journal-guides
description: Comprehensive Guide for Authors, submission specifications, automated manuscript adaptation rules, and engineering narrative standards for premier journals in Intelligent Construction, Civil & Structural Engineering, Building Materials, and Advanced Materials/Defect Inspection (Automation in Construction, CACAIE, ADVEI, ASCE JCCE, Engineering Structures, Structures, Thin-Walled Structures, ASCE JSE, Construction and Building Materials, Cement and Concrete Composites, Cement and Concrete Research, Journal of Building Engineering, Materials & Design, JMPT, EAAI, NDT & E International). Enforces the Three Core Engineering Narrative Principles (plain engineering language over pretentious jargon, formulas strictly serving physical problems, and civil/structural reviewer-friendly titles, headings, and captions).
---

# CCC Journal Guides & Automated Manuscript Adaptation Standards

This skill provides verified, publication-grade **Guides for Authors**, an **Automated Manuscript Adaptation Protocol**, and **Engineering-First Writing Standards** for premier academic journals in **Intelligent Construction**, **Civil & Structural Engineering**, **Building Materials & Concrete**, and **Advanced Materials & Manufacturing/Inspection**.

When authoring, revising, or re-targeting an academic paper (LaTeX or Markdown), this skill enables the agent to automatically reconfigure the manuscript to comply with the exact editorial philosophy, length budgets, citation style, front/back-matter declarations, and rigorous engineering narrative standards of the target journal.

---

## 1. Master Journal Specification Matrix

| Domain | Journal Name | Publisher | JCR / IF | Main Text Words | Abstract Limit | Highlights Rule | Citation Style |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Intelligent Construction** | *Automation in Construction* (AUTCON) | Elsevier | Q1 / 10.3 | 6,000–9,000 | 150–250 w | Mandatory (3–5, $\le 85$ c) | Numbered `[1]` |
| | *Computer-Aided Civil & Infra. Eng.* (CACAIE) | Wiley | Q1 / 10.0 | 7,000–10,000 | $\le 250$ w | Not required (use GA) | Author-Date (APA) |
| | *Advanced Engineering Informatics* (ADVEI) | Elsevier | Q1 / 8.8 | 6,500–9,500 | 150–250 w | Mandatory (3–5, $\le 85$ c) | Numbered `[1]` |
| | *ASCE J. of Computing in Civil Eng.* (JCCE) | ASCE | Q1/Q2 / 4.6 | $\le 10,000$ equiv | $\le 200$ w | None (Notation list) | Author-Date |
| **Civil & Structural** | *Engineering Structures* (ENGSTRUCT) | Elsevier | Q1 / 5.7 | 6,000–9,500 | 150–250 w | Mandatory (3–5, $\le 85$ c) | Numbered `[1]` |
| | *Structures* | Elsevier / IStructE | Q2 / 4.1 | 6,000–9,000 | 150–250 w | Mandatory (3–5, $\le 85$ c) | Numbered `[1]` |
| | *ASCE J. of Structural Engineering* (JSE) | ASCE | Q1/Q2 / 3.8 | $\le 10,000$ equiv | $\le 200$ w | None (Notation list) | Author-Date |
| | *Thin-Walled Structures* (TWST) | Elsevier | Q1 / 6.4 | 6,000–9,000 | 150–250 w | Mandatory (3–5, $\le 85$ c) | Numbered `[1]` |
| **Building Materials** | *Construction and Building Materials* (CBM) | Elsevier | Q1 / 7.4 | 7,000–8,500 | 150–250 w | Mandatory (3–5, $\le 85$ c) | Numbered `[1]` |
| | *Cement and Concrete Composites* (CCC) | Elsevier | Q1 / 10.8 | 7,000–9,000 | 150–250 w | Mandatory (3–5, $\le 85$ c) | Numbered `[1]` |
| | *Cement and Concrete Research* (CCR) | Elsevier | Q1 / 11.4 | 7,000–10,000 | 150–250 w | Mandatory (3–5, $\le 85$ c) | Numbered `[1]` |
| | *Journal of Building Engineering* (JOBE) | Elsevier | Q1 / 6.4 | 6,500–9,000 | 150–250 w | Mandatory (3–5, $\le 85$ c) | Numbered `[1]` |
| **Materials & Manufacturing** | *Materials & Design* (MATDES) | Elsevier | Q1 / 8.4 | 6,500–9,000 | 150–250 w | Mandatory (3–5, $\le 85$ c) | Numbered `[1]` |
| | *J. of Materials Processing Technology* (JMPT) | Elsevier | Q1 / 6.3 | 6,500–9,000 | 150–250 w | Mandatory (3–5, $\le 85$ c) | Numbered `[1]` |
| | *Eng. Applications of AI* (EAAI) | Elsevier | Q1 / 8.0 | 6,500–9,500 | 150–250 w | Mandatory (3–5, $\le 85$ c) | Numbered `[1]` |
| | *NDT & E International* (NDTEINT) | Elsevier | Q1 / 4.2 | 6,000–8,500 | 150–250 w | Mandatory (3–5, $\le 85$ c) | Numbered `[1]` |

---

## 2. Directory Structure of Official Author Guides

Full-text, detailed guides covering specific editorial red lines, reviewer expectations, and submission instructions are indexed in `guides/`:

- **Core Writing & Narrative Standards**:
  - `guides/engineering-narrative-standards.md` *(The Three Iron Rules: plain language, problem-serving formulas, reviewer-friendly navigation)*
- **Intelligent Construction**:
  - `guides/automation-in-construction.md`
  - `guides/computer-aided-civil-and-infrastructure-engineering.md`
  - `guides/advanced-engineering-informatics.md`
  - `guides/asce-journal-of-computing-in-civil-engineering.md`
- **Civil & Structural Engineering**:
  - `guides/engineering-structures.md`
  - `guides/structures.md`
  - `guides/asce-journal-of-structural-engineering.md`
  - `guides/thin-walled-structures.md`
- **Building Materials & Cement/Concrete**:
  - `guides/construction-and-building-materials.md`
  - `guides/cement-and-concrete-composites.md`
  - `guides/cement-and-concrete-research.md`
  - `guides/journal-of-building-engineering.md`
- **Materials, Manufacturing & Defect Metrology**:
  - `guides/materials-and-design.md`
  - `guides/journal-of-materials-processing-technology.md`
  - `guides/engineering-applications-of-artificial-intelligence.md`
  - `guides/ndt-and-e-international.md`

---

## 3. Seven-Stage Automated Manuscript Adaptation Protocol

When adapting a manuscript to a specified target journal, execute the following systematic procedure:

### Stage 1: Narrative Angle & Scope Realignment
- **If target is *Automation in Construction***: Emphasize the IT/computational/robotic contribution (FastWeld-YOLO algorithm, directional attention, real-time edge latency, ISO compliance engine). De-emphasize purely passive material testing.
- **If target is *Construction and Building Materials***: Highlight the physical material system (structural steel grades, weld bead microstructure, heat-affected zone ripples) and practical construction quality assurance.
- **If target is *Engineering Structures* or *Structures***: Emphasize the effect of detected weld defects on structural load-carrying capacity, joint fatigue performance, and design standards (Eurocode 3, AISC).
- **If target is *Materials & Design***: Frame the visual detection output as an input for design tolerance decisions and structural integrity evaluation.
- **If target is *NDT & E International***: Highlight calibrated physical metrology (mm/pixel accuracy, skeletonization length, hydraulic diameter) and non-destructive optical inspection physics.

### Stage 2: Document Class & Typography Reconfiguration
- **Elsevier Journals** (*AUTCON, CBM, ENGSTRUCT, EAAI, CCC, etc.*):
  ```latex
  \documentclass[review,12pt]{elsarticle} % Initial submission
  % or
  \documentclass[5p,times,twocolumn]{elsarticle} % Final layout
  ```
- **Wiley Journals** (*CACAIE*):
  - Single-column, double-spaced with continuous line numbers (`\linenumbers`).
- **ASCE Journals** (*JCCE, JSE*):
  ```latex
  \documentclass[Journal]{ascelike-new}
  ```
  - **Remove all section numbers** (ASCE strictly uses unnumbered section headings).

### Stage 3: Title, Abstract & Keywords Precision (摘要、关键词与数据一致性规范)
- **摘要本质与四要素**：
  - 摘要必须是一篇客观反映文章核心观点与创新观点的表意明确、实在的小短文，必须完整包含四大核心要素：**研究目的 (Purpose)**、**研究方法 (Methodology)**、**主要结果 (Main Results)** 和 **结论 (Conclusions)**。
  - **切忌写成背景交代或“中心思想”**：严禁大篇幅交代宏观背景，严禁空洞拔高或喊口号式的思想升华。
  - **篇幅规格**：中英文篇幅控制在 **300 字左右**（英文通常对应 200～250 词，ASCE 200 词内），必须为单一连续学术段落。
  - **严禁含有编号**：摘要全文严禁出现任何形式的编号（如 ①②③、(1)(2)(3)、1. 2. 3. 等）。
  - **严禁使用非公知公用的符号与术语**：公式符号、自定义代号、未定义的生僻缩写一律不得进入摘要。
- **关键词规范 (Keywords)**：
  - 数量严格控制在 **6～8 个**，准确反映文章主要内容。
  - **必须严格按照重要性顺序排列**：`[核心对象/材料] -> [核心方法/算法] -> [关键物理性能] -> [应用场景]`。
- **数据一致性与正文显式支撑铁律 (Data Consistency & Provenance)**：
  - 中英文摘要和结论中出现的所有数值、百分比、误差度量在正文相应位置必须有**明确表述并展开解释**；
  - **严禁让读者去图表中寻找未解释的数据**：不得在正文不交代的前提下直接在摘要/结论中抛出孤立数据。正文负责深度归因，图表负责证据呈现。

### Stage 4: Highlights Generation (The Strict 85-Character Law)
- For all Elsevier journals requiring Highlights, generate exactly 3 to 5 bullet points.
- **Every single bullet must be $\le 85$ characters (including spaces and punctuation)**.
- Store highlights in `highlights.txt` or `highlights.md` for one-click submission.

### Stage 5: Equations, Tables & Figures Standardization (图表深度理论分析与制图规范)
- **图表正文对应描述与深度理论分析（四步深度闭环）**：
  - 针对图和表在正文中**必须有明确对应的文字描述**，严禁贴图无文；
  - 正文描述必须完整包含四项内容：
    1. **图（表）是什么图（表）**（交代研究对象、工况或考察维度）；
    2. **根据图（表）能够得到什么样的结果或数据**（提取定量读数、具体数值与变化幅度）；
    3. **这一结果能够反映（意味）出什么问题**（揭示力学破坏、物理规律、退化趋势或缺陷现象）；
    4. **针对实验结果和反映出的问题进行深入充分的理论机理分析**（深入分析原因，在分析宏观性能时说明与微观结构的本质联系）。
  - 总之：正文必须对图表有充分的说明以及理论分析，严禁将数据孤立留给读者在图表中寻找！
- **坐标图标尺线与边框铁律**：
  - **标尺线严格朝内**：坐标图标尺线/刻度线**必须严格全部朝内（`direction='in'`）**；
  - **四边完全闭合**：四周矩形全围合边框必须保留（线宽 $0.8\sim 1.0\,\text{pt}$，颜色深灰或纯黑 `#222222`）；
  - **无数字的边框严禁标尺线**：无数字的边框（顶部 top 与右侧 right，若无第二坐标系）绝对不要有标尺线/刻度线（`plt.rcParams['xtick.top'] = False`, `plt.rcParams['ytick.right'] = False`）。
- **表格与排版规范**：
  - Tables must strictly follow the three-line `booktabs` format (`\toprule`, `\midrule`, `\bottomrule`) with zero vertical rules.
  - Figure dimensions: single-column ($90\text{ mm}$), $1.5$-column ($140\text{ mm}$), or double-column ($190\text{ mm}$).
  - Ensure vector graphics (TikZ/EPS/PDF) are used for architectures and plots; $\ge 300\text{ dpi}$ for photographic halftones.

### Stage 6: Citation & Reference Re-styling
- **Numbered Style** (*Elsevier journals*):
  - In-text: `[1]`, `[2,3]`, `[4--6]`.
  - LaTeX BibTeX: `\bibliographystyle{elsarticle-num}`.
- **Author-Date Style** (*ASCE, Wiley CACAIE*):
  - In-text: `(Li and Wang 2024)`.
  - LaTeX BibTeX: `\bibliographystyle{ascelike-new}` or `\bibliographystyle{apacite}`.

### Stage 7: Mandatory Back Matter & Declarations
Inject the mandatory declarations before references:
1. `\section*{CRediT Authorship Contribution Statement}` (standardized 14 CRediT roles).
2. `\section*{Declaration of Competing Interest}` (mandatory statement).
3. `\section*{Data Availability}` (explicit repository/access statement).
4. `\section*{Declaration of Generative AI and AI-Assisted Technologies}` (Elsevier standard AI disclosure).

---

## 4. Automated Compliance Inspection Tool

The skill includes a dedicated command-line verification script:
`skills/ccc-journal-guides/scripts/journal_compliance_checker.py`

### Usage Example:
```bash
# Audit a paper for Automation in Construction
python scripts/journal_compliance_checker.py path/to/main.tex --journal autcon

# Audit for Construction and Building Materials
python scripts/journal_compliance_checker.py path/to/main.tex --journal cbm

# Audit for Engineering Structures
python scripts/journal_compliance_checker.py path/to/main.tex --journal engstruct
```

The script automatically:
- Computes abstract word count and flags deviations.
- Verifies character lengths of each bullet in `highlights.txt` against the 85-character limit.
- Checks for presence of all mandatory declarations (CRediT, Data Availability, Competing Interests).
- Validates document class and citation style.
- Outputs the journal's core editorial red lines to prevent desk rejection.

---

## 5. Engineering-First Academic Narrative Standards (土木与工程顶刊写作三大铁律)

> [!IMPORTANT]
> **三条不可动摇的写作标准（所有 AI 自动化生成/润色/修改论文时必须无条件执行）：**
>
> 1. **概念能用普通话讲清就不造术语 (Plain Language over Pretentious Jargon)**：
>    - 严禁硬造浮夸复合词（如滥用 *gradient stiffness diagnosis*, *conflict-aware bounded allocation*, *spatiotemporal manifold harmonization* 等）。
>    - 正文主线与摘要必须用质朴、精准的工程语言直接讲透本质。
>    - **主线范例**：*“训练前先判断各损失项对参数更新的影响，再在限定范围内确定固定权重。”* (Prior to training, the impact of individual loss terms on parameter updates is evaluated to determine fixed weights within a bounded range.)
>    - 算法生造词仅可降级作为局部方法细节的小括号注释，绝不能作为文章主线、摘要与标题的主语。
>
> 2. **公式只服务于问题，不为了“显得高级”堆符号 (Formulas Serve Problems, Not Pretentious Symbol-Stacking)**：
>    - 每个数学公式必须严格对应具体的力学约束、物理定律或明确可执行的计算步骤。
>    - 坚决杜绝无推导增量、纯粹堆砌冗余下标、花体符号与多层套娃式的伪形式化表达。
>    - 每一个变量第一次出现时必须紧跟明确的物理单位与工程定义。
>
> 3. **章节标题、图题与摘要尽量让土木和工程审稿人一眼看懂 (Civil & Engineering Reviewer-Friendly Navigation)**：
>    - 论文是面向土木、结构与材料工程领域的审稿人。
>    - **主标题**：直奔“工程对象 + 解决什么物理问题 + 核心技术”，不堆砌黑话。
>    - **摘要**：直球交代“工程痛点 $\rightarrow$ 直观方法 $\rightarrow$ 物理机制 $\rightarrow$ 量化结论”。
>    - **章节名**：采用具象直白的工程与方法分类（如“2.3 损失权重边界确定方法”而非“2.3 基于梯度刚度诊断的时空约束优化架构”）。
>    - **图题/表题**：第一句话必须给出结论性或清晰直观的描述，让审稿人扫一眼即明了物理含义。

---

## 6. Absolute Writing Quality Rule (Strict Zero-Listicle Policy)

> [!CAUTION]
> **STRICT ACADEMIC PROSE RULE (严禁“AI味”机械列点)**
> - In all journals covered by this skill, the main body (Introduction, Methodology, Results, Discussion, Conclusion) must consist of **fluent, continuous academic paragraphs**.
> - **Never** overuse bullet points (`itemize`) or numbered lists (`enumerate`) to describe contributions, bottlenecks, or experimental observations. Such listicle patterns are perceived by editors as superficial AI-generated text and lead to immediate rejection.

---

## 7. Anti-Defensive Writing & Sepia De-AI Pipeline (去防御性写作与 Sepia 结构级去 AI 味双引擎)

> [!IMPORTANT]
> **专属触发词**：“**调用 ccc-skills 来去 AI 味**” 或 “**去防御性写作**”。
> 当用户发出此类指令时，必须且自动按照《Anti-Defensive Writing》与《Sepia (StoryScope)》双引擎彻底重构文稿：
> 1. **学术发布会原则**：论文不是工作进度汇报，更不是自我审查报告；永远只围绕本文最强、最无可替代的工程/力学优势组织核心主线。
> 2. **严禁递刀子**：彻底剔除“遗憾的是 (regrettably)”、“仅 (merely)”、“效果有限 (marginal)”、“仍明显落后”等被动自我削弱词汇。
> 3. **打不赢的维度不设为赛道**：不占优的指标不硬碰硬，通过工作环境差异、工程成本平衡（Trade-off）或物理约束进行合理解释，绝不在正文中替审稿人攻击自己。
> 4. **Sepia 结构级去 AI 手术**：破除均一机械句长与万能填充词（Moreover, Furthermore, In summary, 值得注意的是），支持 review（诊断）、refactor（原地精修）、recreate（彻底重构）。
> 5. **完整规范参考**：`anti-defensive-writing/SKILL.md` 与 `sepia/SKILL.md`。

---

## 8. Civil & Concrete Machine Learning Empirical Paradigm (土木与混凝土机器学习实证写作规范)

> [!IMPORTANT]
> **专属触发词**：“**土木机器学习写作范式**”、“**模型性能与可解释性分析**”或“**调用 ccc-skills 撰写/精修第四、五章**”。
> 本规范提炼自刘凯华副教授与李俊赞团队在 *Computers and Concrete* (2025)、*Discover Applied Sciences* (2025) 以及《硅酸盐通报》等发表的经典实证写作范式，专为解决土木材料/结构期刊中对 AI 模型“过拟合质疑”、“黑盒机理脱节”和“工程落地性差”的三大审稿痛点。

### 8.1 模型性能与过拟合防御写作铁律 (Model Evaluation & Overfitting Defense)
1. **多模型横向竞赛架构 (Tournament-Style Benchmark)**：
   - 必须涵盖梯队式算法对比：主力提升树（CatBoost、XGBoost、LightGBM / Deep Forest）vs 传统集成/神经网络（RF, ANN/MLP）vs 现行设计规范/经验公式（Code-based empirical equations）。
   - 评价指标统一采用四维/五维矩阵：$R^2$、RMSE、MAE、解释方差（EV）及容差百分比指标 $a20$-index。
2. **训练-测试收敛差值论证 (The Narrow Performance Discrepancy Defense)**：
   - 坚决杜绝孤立汇报高 $R^2$。必须在同张表格中并列汇报训练集（Train）与独立测试集（Test）指标。
   - **核心话术**：主动指出训练集与测试集的误差差值极小（*"The narrow performance gap between the training set and testing set demonstrates that the proposed model is well-regularized and free from overfitting"*），从而作为模型具备高泛化能力的直接证据。
3. **多维几何与误差分布检验**：
   - 标配 $1:1$ 实测-预测散点图，必须绘制 $\pm 10\%$ 或 $\pm 20\%$ 误差包络带。
   - 推荐配备**泰勒图（Taylor Diagram）**与**残差正态分布核密度图（Residual PDF）**，以中心均方根误差与无偏高斯分布证明模型未出现系统性漂移。

### 8.2 多尺度模型可解释性写作铁律 (Hierarchical Interpretability & Micro-mechanisms)
严禁单纯堆砌 SHAP 图表，必须严格执行“以材料水化/微观缺陷机理为纲，以 SHAP 数据为目”的三层递进叙事：
1. **全局特征贡献排位 (Global Hierarchy)**：
   - 条形图（Mean $|SHAP|$）定量主导因子排位；
   - Beeswarm 蜂群图阐释红/蓝点极性，区分各配比参数对目标力学/耐久性能的促进或抑制作用。
2. **特征依赖曲线与“工程临界拐点”物理映射 (Dependence Thresholds & Micro-mechanisms)**：
   - **三段式论述模板**：`[锁定依赖曲线突变拐点数值]` $\rightarrow$ `[映射至微观水化反应/孔隙结构/ITZ界面缺陷/堆积密实度机理]` $\rightarrow$ `[给出工程配合比设计优化范围]`。
   - 示例：指出再生骨料取代率、水胶比或矿物掺合料的最佳活性区间与饱和阈值（Saturation threshold）。
3. **高阶耦合与因果推断 (Interactions & Causal Inference)**：
   - 运用 SHAP 交互值图（Interaction plots）论证两两成分之间的非线性协同（Synergistic）或拮抗（Antagonistic）效应；
   - 视需要引入因果发现算法（如 LiNGAM）或不确定性量化（如共形预测 CV+），从统计关联跃迁到物理因果网络，封死顶刊审稿人对模型科学性的追问。

### 8.3 材料类顶刊章节标题极简风与反拔高实证准则 (Concise Headings & Anti-Overclaiming Standard)

> [!IMPORTANT]
> **专属触发词**：“**材料类论文标题精简**”、“**章节标题极简风**”或在自动化撰写/修改/精修论文各章节标题时自动无条件执行。
> 论文面向土木、建筑材料与复合结构顶刊（CCC, CBM, CCR, MATDES）审稿人。审稿人高度关注材料性能本身与工程实用性，极度反感计算机/AI领域的冗长黑话标题；同时，严禁脱离实际工作开展宏大叙事（如将碳排放估算拔高为 LCA），防止招致审稿人的毁灭性反噬。

#### 1. 三大命名核心铁律
1. **绝不堆砌方法名称与冗长修饰词（2–4 词极简律）**：
   - 彻底剔除虚浮的复合修饰语（如 *Task-specific predictive modeling framework*, *Prediction performance and literature-to-experiment adaptation* 等）。
   - 小节标题直截了当表明讨论的材料物理量或模型环节（如 **`Prediction models`**, **`Model evaluation`**, **`Model performance`**, **`Strength prediction`**, **`Flowability prediction`**）。
2. **严防“宏大叙事”引发审稿致命攻击（Strict Anti-Overclaiming & Defensive Invariance）**：
   - **典型红线（第 5 章及类似工程配合比优选/情景核算）**：如果文章正文仅开展基于配合比的情景碳排放与能耗核算、配合比优化，**绝对不能**将标题定为宏大的 *“Life-cycle assessment (LCA)”* 或 *“Environmental footprint and life-cycle carbon-energy assessment”*！
   - **审查机理**：一旦冠以 LCA，审稿人必以 ISO 14040/14044 严苛标准（全生命周期系统边界、开采、运输、施工、运营维护、拆解回收全清单）进行致命审查；而实事求是写成 **`Embodied carbon and energy`**（或 `Carbon and energy analysis`），不仅 100% 严丝合缝对齐正文数据，更让审稿人完全找不到挑剔边界的切入点。
   - 同理，常规配合比筛选直截了当命名为 **`Mixture optimization`**，不虚夸为 *“Performance-oriented mixture screening”*。
3. **方法章名称统一规范为 `3. Methods`**：
   - 避免虚浮冗长的 `3. Methodology`，统一采用 Nature / Elsevier 顶刊标准的 **`3. Methods`**（或 `2. Materials and methods`）。

#### 2. 经典章节标题极简映射基准表 (Canonical Heading Mapping Matrix)

| 原繁复/堆砌/虚浮标题 (Banned) | 极简规范标题 (Mandatory) | 精简理由与审稿防御机制 |
| :--- | :--- | :--- |
| `Task-specific predictive modeling framework` | **`Prediction models`** | 剔除虚浮的 "Task-specific" 与 "framework"，直截交代预测模型体系 |
| `Validation strategy for literature-assisted prediction` | **`Literature-assisted training and validation`** | 准确朴实表达文献数据驱动的训练与验证流程，避免空谈 "strategy" |
| `Prediction reliability and material-variable interpretation` | **`Uncertainty and interpretation`** | 凝练涵盖不确定性量化与机理可解释性两大模块 |
| `Evaluation metrics and cross-validation protocols` | **`Model evaluation`** | 2 个词概括所有评估指标与交叉验证协议 |
| `Prediction performance and literature-to-experiment adaptation` | **`Model performance`** | 拒绝多重介词套娃，直观汇报预测表现 |
| `Compressive strength prediction and literature adaptation` | **`Strength prediction`** | 聚焦材料力学核心指标（抗压强度），去掉多余方法修饰 |
| `Fresh flowability prediction and literature-data utilization` | **`Flowability prediction`** | 聚焦材料工作性能核心指标（流动度/工作性） |
| `Performance-oriented mixture screening` | **`Mixture optimization`** | 配合比优化通用标准学术术语，不生造概念 |
| `Environmental footprint and life-cycle carbon-energy assessment` | **`Embodied carbon and energy`** | **严重红线**：情景估算严禁叫 LCA，改称隐含碳与能耗，实事求是且封死攻击漏洞 |
| `Methodology` | **`Methods`** | 顶刊标准，精练自然，拒绝虚浮 |

#### 3. 执行约束与排版保护原则
- **保留原有标题样式与导航层级**：修改标题文字时，必须严格保留 Word 的标题样式（Heading 1, Heading 2, Heading 3）及 LaTeX 的层级结构，杜绝层级坍塌；
- **排版零越界原则**：精简标题不得破坏段落对齐，修改后务必确认正文总页数未发生意外跳页、文字未出现越界或孤行。




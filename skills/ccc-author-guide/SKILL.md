---
name: ccc-author-guide
description: Complete author guidelines, submission checklist, automated LaTeX/Word formatting rules, and technical screening compliance audit for Cement and Concrete Composites (Elsevier, ISSN 0958-9465). Use when formatting, auditing, checking compliance, or editing manuscripts for submission to CCC, including LaTeX elsarticle 5p/3p layout, continuous line numbers, Highlights (3-5 bullets, <=85 chars), figure/table citation monotonicity, bijective bibliography verification, Elsevier Numbered reference style (Initials. Surname, LTWA abbreviations, full HTTPS DOIs), CRediT authorship statement, Funding/Crossref declarations, and Data availability statements.
---

# Cement and Concrete Composites (CCC) Author Guide & Submission Audit Standard

This skill establishes the definitive formatting, technical screening, and automated compliance rules for manuscripts submitted to ***Cement and Concrete Composites*** (Elsevier, ISSN: 0958-9465, JCR Q1, Impact Factor 6.6).

---

## 1. Quick Technical Audit Script (一键自动化排查脚本)

A production-grade Python audit script is bundled with this skill at `scripts/audit_ccc_manuscript.py`. Whenever the user asks to "审核 CCC 论文格式" or "修改为 CCC 投稿要求", run this script first to generate an instant diagnostic report:

```powershell
python "C:\Users\12830\.gemini\config\skills\ccc-author-guide\scripts\audit_ccc_manuscript.py" <path_to_paper.tex> [path_to_Highlights.txt]
```

### Checks Performed by the Script:
1. **Line Numbers**: Verifies `\usepackage{lineno}` and `\linenumbers`.
2. **Highlights Count & Length**: Verifies 3–5 bullets and $\le 85$ characters per bullet.
3. **Table Coverage & Order**: Ensures 100% table citation and monotonic numbering.
4. **Figure Coverage & Order**: Ensures 100% figure citation and strictly monotonic appearance.
5. **Bijective Reference Mapping**: Every `\cite{...}` exists in `\bibitem{...}`, and every `\bibitem{...}` is cited in text.
6. **GB/T 7714 Cleanliness**: Detects illegal Chinese reference markers (`[R]`, `[M]`, etc.).
7. **Mandatory End-Matter**: Verifies CRediT, Competing Interests, Funding, and Data statements.

---

## 2. Manuscript Layout & Submission Format (排版版式与行号标准)

### A. Word vs. LaTeX Submission Policy (Elsevier CCC 官方明文规则)
* **Word Submissions**: Must be formatted in **single-column layout ONLY**.
* **LaTeX Submissions**: **Double-column formatting is explicitly permitted and standard**!
  > *"Format Word files in a single-column layout. Double-column formatting is only permitted for LaTeX submissions."* (CCC Guide for Authors)
* **Standard Class Definition**:
  ```latex
  \documentclass[5p,times,twocolumn]{elsarticle}  % Standard 2-column final layout
  % OR: \documentclass[3p,times]{elsarticle}      % Conservative 1-column layout
  ```

### B. Mandatory Line Numbers for Peer Review
All review copies must include continuous line numbers:
```latex
\usepackage{lineno}
% In preamble:
\begin{document}
\linenumbers  % Right after \begin{document}
```

### C. Non-Breaking Space Citation Rule (防断行视觉错觉)
Never place a naked space before `\cite{...}`. Always bind the author name or preceding noun with a non-breaking tilde `~`:
```latex
% WRONG (Citation can wrap to the start of the next line, appearing as an isolated number):
published by Hlobil and Kumpov\'{a} \cite{hlobil2023}.

% CORRECT:
published by Hlobil and Kumpov\'{a}~\cite{hlobil2023}.
```

---

## 3. Abstract, Keywords & Cross-Section Data Consistency Standard (摘要、关键词与数据一致性铁律)

### A. 摘要四要素结构与文风禁忌 (Abstract Core Standards)
* **本质定位**：应是一篇能客观反映文章核心观点和创新观点的表意明确、实在的小短文。
* **篇幅规格**：**300 字左右**（中文约 300 字；英文通常对应 200～250 词，简明扼要）。
* **四大必备要素（无缝纯学术连续单段落）**：
  1. **研究目的 (Objective/Purpose)**：直奔科学或工程问题本身，一句话交代针对的材料/计算瓶颈；
  2. **研究方法 (Methodology)**：用直白朴实的工程/数学语言交代核心试验方案、模型构架与求解机制；
  3. **主要结果 (Main Results)**：客观列出核心量化实测数据、精度指标与规律特征；
  4. **研究结论 (Conclusions)**：提炼出材料微观机理、宏观服役性能提升或通用性工程价值。
* **两大核心禁忌 (Red Lines)**：
  - **切忌写成背景交代或“中心思想”**：背景最多一句话点破痛点，严禁通篇铺陈宏观背景，严禁在末尾喊口号或空泛升华“中心思想”；
  - **不应含有编号**：摘要全文严禁出现任何编号形式（如 ①②③、(1)(2)(3)、1. 2. 3. 等）；
  - **不应含有非公知公用的符号和术语**：严禁出现数学公式、生造符号代号或未定义的冷门缩写。

### B. 关键词规范 (Keywords: 6–8 Items by Importance)
* **数量规格**：严格控制在 **6～8 个**；
* **内容质量**：应能准确反映文章的主要内容与技术核心；
* **排序铁律**：**必须严格按照重要性顺序排列**，遵循学术逻辑递进层次：
  `[核心研究对象/材料] -> [核心计算方法/算法/模型] -> [关键物理性能/力学损伤机制] -> [工程应用/服役场景]`。

### C. 数据一致性与正文显式支撑铁律 (Cross-Section Data Provenance & Consistency Law)
* **中英文摘要、正文与结论数据 100% 绝对一致**：在三处出现的所有数值、百分比、极值、误差指标必须完全咬合，严禁前后矛盾或口径不一；
* **正文显式说明原则（严禁让读者去图表中寻找未在正文解释过的数据）**：
  - **在摘要和结论中出现的所有关键数据与量化结论，必须在正文相应的小节文字中明确提到并展开说明过**；
  - 绝对禁止“正文文字中只字不提，直接在摘要/结论中抛出某个惊艳的数值，让读者去图或者表中找对应的数据”。图表负责证据呈现，正文文字负责交代具体的数字与深度理论机理！

---

## 4. Highlights Requirements (投稿亮点强制规范)

* **File Format**: A separate editable file named with "highlights" (e.g., `Highlights.txt` or `Highlights.docx`).
* **Bullet Count**: Strictly **3 to 5 bullet points**.
* **Character Limit**: **Maximum 85 characters per bullet point, including spaces**!
* **Formula / Rule**:
  $$\text{Length}(\text{Bullet}_i) \le 85 \quad (i = 1, \dots, N; \; 3 \le N \le 5)$$
* **Content Focus**: Convey novel empirical/computational findings, quantitative improvements (e.g. error percentages, compression factors), and new physical insights.

---

## 5. Figures & Subfigures Rules (图件排版、坐标图制图与正文理论分析规范)

### A. Resolution & Vectors
* **Color / Grayscale Photographs & XCT**: Minimum 300 DPI (TIFF or PNG).
* **Line Art, Charts & Flowcharts**: Preferred vector formats (PDF, EPS) or minimum 1000 DPI.

### B. 坐标图四边与标尺线铁律 (Universal Spine & Inward Tick Marks)
* **标尺线严格朝内**：坐标图标尺线/刻度线**必须严格全部朝内（`direction='in'`）**，严禁朝外草稿风格；
* **四边完全闭合**：四周矩形全围合边框必须保留（`top`, `bottom`, `left`, `right` 边框线宽 $0.8\sim 1.0\,\text{pt}$，颜色中性深灰或黑色 `#222222`）；
* **无数字边框严禁标尺线**：**无数字的边框（顶部 top 与右侧 right，非双坐标轴时）绝对不要有标尺线/刻度线**（`plt.rcParams['xtick.top'] = False`, `plt.rcParams['ytick.right'] = False`），保持图面干净利落。

### C. 100% Sequential Monotonic Citation
* Every figure (`\label{fig:...}`) must be cited in the text before the next numbered figure is mentioned.
* **Never cite Figure 9 before Figure 8**. If cross-referencing a later figure, refer to the section instead (e.g., *"detailed in Section 3.5"*).

### D. 图表正文对应描述与深度理论机理分析闭环 (Dedicated Textual Description & Theoretical Analysis)
* **Strict Anti-Consecutive Mandate (严禁连续大图无文堆叠)**:
  - 绝对禁止两个独立的大型图或表连续出现而中间没有解释正文（"图堆图"属于顶刊排版大忌，严禁两图之间仅以空行、纯小节标题或机械过场套话隔开）；
  - 严禁多图笼统合并带过（严禁出现如 *"As shown in Figs. 8 to 10..."* 这种跨多图混合、泛泛而谈的粗糙写法）。
* **图表在正文中的对应文字描述与理论机理分析（四步深度闭环）**：
  针对每个图和表，在正文相应位置必须有对应的文字描述，包含以下四项内容：
  1. **图（表）是什么图（表）**：明确引出图表并说明其研究对象、工况或考察维度；
  2. **根据图（表）能够得到什么样的结果（或数据）**：从图表中提取具体的定量指标、数值读数与变化幅度；
  3. **这一结果能够反映（意味）出什么问题**：揭示其反映出的力学破坏、物理规律、退化趋势或缺陷现象；
  4. **深入充分的理论机理分析**：针对实验结果和反映出的问题进行恰当、深入和充分的理论机理分析（如：深入分析出现这一结果的原因是什么；在分析宏观力学/耐久性能时，说明与前面的微观结构分析有何本质联系，等等）。
  总之：正文必须对图表有充分的说明以及深刻的理论机理分析，严禁将数据孤立留给读者在图表中寻找！

### E. Multi-Subfigure Rigid Symmetric Grid Standard
When constructing multi-row, multi-column subfigure matrices (e.g., 3D cube grids):
1. **Pad all raw subfigure canvases** to identical dimensions $(W \times H)$ with white margins to ensure equal aspect ratios and cube centers.
2. **Never rely on elastic `\hfill`** across rows with dividers, which causes vertical divider misalignment. Use rigid symmetric `\hspace`:
```latex
\begin{figure*}[htbp]
  \centering
  % Row 1
  \begin{subfigure}[t]{0.226\textwidth}
    \centering
    \includegraphics[width=\textwidth]{figures/panel_a.png}
    \caption{Description A}
  \end{subfigure}\hspace{0.024\textwidth}%
  \begin{subfigure}[t]{0.226\textwidth}
    \centering
    \includegraphics[width=\textwidth]{figures/panel_b.png}
    \caption{Description B}
  \end{subfigure}\hspace{0.020\textwidth}%
  {\color{gray!60}\vrule width 0.8pt}\hspace{0.020\textwidth}%
  \begin{subfigure}[t]{0.226\textwidth}
    \centering
    \includegraphics[width=\textwidth]{figures/panel_c.png}
    \caption{Description C}
  \end{subfigure}\hspace{0.024\textwidth}%
  \begin{subfigure}[t]{0.226\textwidth}
    \centering
    \includegraphics[width=\textwidth]{figures/panel_d.png}
    \caption{Description D}
  \end{subfigure}
  \caption{Overall caption...}
  \label{fig:composite_matrix}
\end{figure*}
```
3. Use `[t]` (top alignment) instead of `[b]` (bottom alignment) to prevent vertical jumping caused by differing caption heights.

---


### D. Double-Column Wide-Float Placement Rule (双栏跨栏图表与空白页控制)

In `elsarticle` 5p/two-column manuscripts, `figure*` and `table*` are double-column floats. Their placement is much more constrained than ordinary single-column floats, and a float-dense Results section can easily create either a "float wall" or large blank regions if controlled too aggressively.

1. **Do not trust `[h]` for `figure*` / `table*`.** In two-column mode, `h` is normally ineffective for double-column floats. Avoid using `[htbp]` as if it guaranteed local placement.

2. **Default placement for float-dense CCC Results:** prefer wide figures at the page top and wide tables at the page bottom:
   ```latex
   \usepackage{stfloats} % enables bottom placement of double-column floats

   \begin{figure*}[!t]
   ...
   \end{figure*}

   \begin{table*}[!b]
   ...
   \end{table*}
   ```
   This allows the two text columns to continue through the middle of the page and reduces accumulation of all wide floats at page tops. Always compile-test `stfloats` with the actual `elsarticle` version before adopting it.

3. **Do NOT place `\FloatBarrier` before every Results subsection.** This was explicitly found to create half-empty pages when a pending `figure*`/`table*` cannot fit before the barrier. In a float-dense Results section, the default is **no subsection-level barrier**.

4. **Use `\FloatBarrier` only as an exceptional repair tool.** Load `placeins` only when needed and add a barrier at a major section boundary (e.g. Results -> Discussion) *only if visual inspection proves that unrelated floats are crossing that boundary*. If the barrier creates large blank areas, remove it and solve the queue through float placement/order instead.

5. **Do not use `H`, routine `\clearpage`, or repeated forced page breaks as cosmetic fixes.** They often solve one placement problem by creating another. Forced breaks are acceptable only for a deliberate standalone figure/float page.

6. **Interleave prose and evidence.** Avoid declaring many wide figures/tables from several scientific questions before enough explanatory prose has been processed. Where practical, keep each Results subsection in the semantic pattern `result prose -> associated figure/table -> interpretation`, while accepting that the rendered float may move to the nearest legal top/bottom position.

7. **Distinguish a real whitespace defect from a legitimate full-page figure.** A page with a large full-width 3D reconstruction or multi-panel chloride figure may contain little extractable text yet still be visually well occupied. The defect to eliminate is a page with only a short paragraph or heading followed by a large unused white region.

8. **Mandatory page-level verification after compilation.** Inspect the PDF page by page. Reject layouts with (a) half-empty text pages caused by subsection barriers, (b) unrelated wide floats from several scientific questions stacked as a data wall when avoidable, or (c) floats drifting into the wrong major section. A zero-warning LaTeX log is not sufficient evidence of good float layout.

**CCC default policy learned from production manuscripts:** in `elsarticle` 5p/two-column mode, first try `stfloats` with `figure* [!t]` and `table* [!b]`, avoid subsection-level `\FloatBarrier`, and only add a major-boundary barrier after visual proof that it improves rather than worsens the compiled pages.

---

## 5. Tables Standards (表格规范)

1. **Booktabs Three-Line Tables**: Always use `\toprule`, `\midrule`, and `\bottomrule`. No vertical lines (`|`).
2. **Citation Completeness**: Every table (`\label{tab:...}`) must be explicitly cited in the text in monotonic order (`Table 1` $\rightarrow$ `Table 2` $\rightarrow$ `Table 3`).
3. **Column Padding**: Use `\setlength{\tabcolsep}{...}` or `\begin{tabular*}{\textwidth}{@{\extracolsep{\fill}}...}` to ensure wide tables span the exact text width cleanly.

---

## 6. References & Bibliography (Elsevier Numbered Style)

CCC enforces the **Elsevier Numbered Reference Style**:

### A. Key Format Rules
1. **Author Names**: `Initials. Surname` (e.g., `Z. Xu, G. Ye, E.J. Garboczi`). Never invert to Chinese GB/T style (`Xu Z, Ye G`).
2. **Article Title**: Sentence case or title case in roman font.
3. **Journal Names**: Must be abbreviated according to ISO 4 / **List of Title Word Abbreviations (LTWA)**.
   * *Cement and Concrete Research* $\rightarrow$ `Cem. Concr. Res.`
   * *Cement and Concrete Composites* $\rightarrow$ `Cem. Concr. Compos.`
   * *Construction and Building Materials* $\rightarrow$ `Constr. Build. Mater.`
   * *Computer Methods in Applied Mechanics and Engineering* $\rightarrow$ `Comput. Methods Appl. Mech. Eng.`
   * *Journal of the American Ceramic Society* $\rightarrow$ `J. Am. Ceram. Soc.`
   * *Materials and Structures* $\rightarrow$ `Mater. Struct.`
   * *Advanced Functional Materials* $\rightarrow$ `Adv. Funct. Mater.`
4. **Volume & Pages**: `Vol (Year) PageStart–PageEnd` or `Vol (Year) ArticleNumber`.
5. **DOI**: Full HTTPS URL: `https://doi.org/10.1016/j.cemconcomp.2024.105...`
6. **Zero GB/T 7714 Pollution**: Absolutely NO `[R]`, `[M]`, `[C]`, `[D]`, `[J]`, `[S]` document type markers.

### B. Reference Template Examples
```latex
% Journal article with pages:
\bibitem{ref1}
J. van der Geer, J.A.J. Hanraads, R.A. Lupton, The art of writing a scientific article, J. Sci. Commun. 163 (2020) 51--59. https://doi.org/10.1016/j.sc.2020.00372.

% Journal article with article number:
\bibitem{ref2}
M. Hlobil, I. Kumpov\'{a}, A collection of three-dimensional datasets of hydrating cement paste, Data Brief 46 (2023) 108903. https://doi.org/10.1016/j.dib.2023.108903.

% Book:
\bibitem{ref3}
W. Strunk Jr., E.B. White, The Elements of Style, 4th ed., Longman, New York, 2000.

% Dataset:
\bibitem{ref4}
M. Oguro, S. Imahiro, S. Saito, T. Nakashizuka, Mortality data for Japanese oak wilt disease and surrounding forest compositions [dataset], Mendeley Data, v1, 2015. https://doi.org/10.1234/abc12nb39r.1.
```

---

## 7. Mandatory End-Matter Declarations (必备声明与资助格式)

Before `\begin{thebibliography}`, the following 4 sections must appear in order:

```latex
\section*{CRediT authorship contribution statement}
\textbf{First Author}: Conceptualization, Methodology, Software, Formal analysis, Writing - original draft. \textbf{Second Author}: Investigation, Data curation, Visualization. \textbf{Corresponding Author}: Supervision, Project administration, Funding acquisition, Writing - review \& editing.

\section*{Declaration of competing interests}
The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.

\section*{Acknowledgements}
The authors gratefully acknowledge the financial support from ...

\section*{Data availability}
The public datasets analyzed during this study are available in [Repository Name] (\url{https://doi.org/...}). Source code and evaluation scripts are accessible at \url{https://github.com/...}.
```

### Funding Sources Crossref Syntax:
```latex
Funding: This work was supported by the National Natural Science Foundation of China [grant numbers 52108123, 52378245]; and the Guangdong Provincial Science and Technology Project [grant number 2023A1515010987].
```

---

## 8. Engineering Narrative Standards & Anti-Jargon Rules (土木与工程顶刊写作三大铁律)

When authoring, revising, or refining manuscripts for *Cement and Concrete Composites*, the following three rules are mandatory:

1. **概念能用普通话讲清就不造术语 (Plain Language over Pretentious Jargon)**：
   - 严禁硬造浮夸的 AI/ML 复合新词（如 *gradient stiffness diagnosis*, *conflict-aware bounded allocation*, *spatiotemporal manifold harmonization* 等）。
   - 正文主线与摘要必须用质朴、精准的工程语言直接讲透本质。
   - **主线基准范例**：*“训练前先判断各损失项对参数更新的影响，再在限定范围内确定固定权重。”* (Prior to training, the impact of individual loss terms on parameter updates is evaluated to determine fixed weights within a bounded range.)
   - 算法生造词仅可降级保留在具体实现细节或局部变量括号内，绝不能作为文章主线、摘要与标题的主语。

2. **公式只服务于问题，不为了“显得高级”堆符号 (Formulas Serve Problems, Not Pretentious Symbol-Stacking)**：
   - 每个数学公式必须严格对应具体的材料本构、力学约束、损伤定律或可执行算法。
   - 坚决杜绝无推导增量、纯粹堆砌冗余下标、花体符号与多层套娃式的伪数学表达。
   - 每一个变量第一次出现时必须紧跟明确的物理单位与工程定义。

3. **章节标题、图题与摘要尽量让土木和工程审稿人一眼看懂 (Civil & Engineering Reviewer-Friendly Navigation)**：
   - 论文是写给土木、结构与建材领域审稿人看的。
   - **主标题**：直奔“工程对象 + 解决什么物理问题 + 核心技术”，不堆砌黑话。
   - **摘要**：直球交代“工程痛点 $\rightarrow$ 直观方法 $\rightarrow$ 物理机制 $\rightarrow$ 量化结论”。
   - **章节名**：采用具象直白的工程与方法分类（如“2.3 损失权重边界确定方法”而非“2.3 基于梯度刚度诊断的时空约束优化架构”）。
   - **图题/表题**：第一句话必须给出结论性或清晰直观的描述，让审稿人扫一眼即明了物理含义。

---

## 9. AI-Assisted Manuscript Reformatter Workflow (智能排版执行工作流)

When invoked to format or audit a manuscript for CCC, execute the following steps in sequence:

1. **Step 1: Narrative, Jargon & Heading Audit**:
   - Verify the Three Core Narrative Principles: replace pretentious AI terms with plain engineering prose; ensure formulas serve concrete physics; verify civil-engineer-friendly titles and figure captions.
   - Enforce Section 10 Concise Headings & Anti-Overclaiming: normalize `Methodology` to `Methods`; condense stacked headings to 2–4 concise words; prohibit naming mixture-level scenario footprint estimations as "LCA" (mandate `Embodied carbon and energy`).
2. **Step 2: Technical Audit**: Run `audit_ccc_manuscript.py <paper.tex> <Highlights.txt>`.
3. **Step 3: Line Numbers**: Inject `\usepackage{lineno}` and `\linenumbers` if missing.
4. **Step 4: Citation Integrity**:
   - Check and cite any unreferenced tables (`\Cref{tab:...}`).
   - Check and cite any unreferenced figures (`\Cref{fig:...}`).
   - Sort citations to ensure strictly monotonic ordering.
5. **Step 5: Reference Clean-Up**:
   - Convert all `\bibitem` entries to `Initials. Surname` format.
   - Replace full journal names with ISO 4 / LTWA abbreviations.
   - Strip `[R]`, `[M]`, `[J]` document markers.
   - Convert bare DOIs to `https://doi.org/...`.
   - Ensure a 100% bijective mapping between `\cite` and `\bibitem`.
6. **Step 6: Highlights Audit**:
   - Verify 3–5 bullets.
   - Count characters for each bullet. If $> 85$, condense text without losing core numerical claims.
7. **Step 7: End-Matter Audit**:
   - Verify CRediT, Competing Interests, Funding, and Data availability sections.
8. **Step 8: Double-Column Float Audit**:
   - In `elsarticle` 5p/two-column mode, inspect all `figure*` and `table*` placements after compilation, not merely their source options.
   - For float-dense Results, default to `figure* [!t]` and `table* [!b]` with `stfloats` when compatible; do **not** add `\FloatBarrier` at every subsection.
   - Add a major-boundary `\FloatBarrier` only if floats actually cross into the wrong scientific section and only if the resulting pages remain well filled.
   - Reject half-empty text pages caused by over-constrained floats; do not misclassify an intentionally full-page multi-panel figure as a blank-page defect.
9. **Step 9: Verification**:
   - Compile twice with `pdflatex` (or the manuscript's required LaTeX engine) to guarantee zero undefined citations (`?`) and zero undefined references.
   - Run `audit_ccc_manuscript.py` to confirm `PASSED [OK]`.

---

## 10. Concise Headings & Anti-Overclaiming Standard (材料类章节标题极简风与反拔高实证准则)

> [!IMPORTANT]
> **专属触发词**：“**材料类论文标题精简**”、“**章节标题极简风**”或在自动化撰写/修改/精修论文各章节标题时自动无条件执行。
> 论文面向土木、建筑材料与复合结构顶刊（CCC, CBM, CCR, MATDES）审稿人。审稿人高度关注材料性能本身与工程实用性，极度反感计算机/AI领域的冗长黑话标题；同时，严禁脱离实际工作开展宏大叙事（如将碳排放估算拔高为 LCA），防止招致审稿人的毁灭性反噬。

### A. 三大命名核心铁律
1. **绝不堆砌方法名称与冗长修饰词（2–4 词极简律）**：
   - 彻底剔除虚浮的复合修饰语（如 *Task-specific predictive modeling framework*, *Prediction performance and literature-to-experiment adaptation* 等）。
   - 小节标题直截了当表明讨论的材料物理量或模型环节（如 **`Prediction models`**, **`Model evaluation`**, **`Model performance`**, **`Strength prediction`**, **`Flowability prediction`**）。
2. **严防“宏大叙事”引发审稿致命攻击（Strict Anti-Overclaiming & Defensive Invariance）**：
   - **典型红线（第 5 章及类似工程配合比优选/情景核算）**：如果文章正文仅开展基于配合比的情景碳排放与能耗核算、配合比优化，**绝对不能**将标题定为宏大的 *“Life-cycle assessment (LCA)”* 或 *“Environmental footprint and life-cycle carbon-energy assessment”*！
   - **审查机理**：一旦冠以 LCA，审稿人必以 ISO 14040/14044 严苛标准（全生命周期系统边界、开采、运输、施工、运营维护、拆解回收全清单）进行致命审查；而实事求是写成 **`Embodied carbon and energy`**（或 `Carbon and energy analysis`），不仅 100% 严丝合缝对齐正文数据，更让审稿人完全找不到挑剔边界的切入点。
   - 同理，常规配合比筛选直截了当命名为 **`Mixture optimization`**，不虚夸为 *“Performance-oriented mixture screening”*。
3. **方法章名称统一规范为 `3. Methods`**：
   - 避免虚浮冗长的 `3. Methodology`，统一采用 Nature / Elsevier 顶刊标准的 **`3. Methods`**（或 `2. Materials and methods`）。

### B. 经典章节标题极简映射基准表 (Canonical Heading Mapping Matrix)

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

### C. 执行约束与排版保护原则
- **保留原有标题样式与导航层级**：修改标题文字时，必须严格保留 Word 的标题样式（Heading 1, Heading 2, Heading 3）及 LaTeX 的层级结构，杜绝层级坍塌；
- **排版零越界原则**：精简标题不得破坏段落对齐，修改后务必确认正文总页数未发生意外跳页、文字未出现越界或孤行。



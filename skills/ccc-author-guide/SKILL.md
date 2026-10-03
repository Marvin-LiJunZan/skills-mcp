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

## 3. Highlights Requirements (投稿亮点强制规范)

* **File Format**: A separate editable file named with "highlights" (e.g., `Highlights.txt` or `Highlights.docx`).
* **Bullet Count**: Strictly **3 to 5 bullet points**.
* **Character Limit**: **Maximum 85 characters per bullet point, including spaces**!
* **Formula / Rule**:
  $$\text{Length}(\text{Bullet}_i) \le 85 \quad (i = 1, \dots, N; \; 3 \le N \le 5)$$
* **Content Focus**: Convey novel empirical/computational findings, quantitative improvements (e.g. error percentages, compression factors), and new physical insights.

---

## 4. Figures & Subfigures Rules (图件排版与对称网格规范)

### A. Resolution & Vectors
* **Color / Grayscale Photographs & XCT**: Minimum 300 DPI (TIFF or PNG).
* **Line Art, Charts & Flowcharts**: Preferred vector formats (PDF, EPS) or minimum 1000 DPI.

### B. 100% Sequential Monotonic Citation
* Every figure (`\label{fig:...}`) must be cited in the text before the next numbered figure is mentioned.
* **Never cite Figure 9 before Figure 8**. If cross-referencing a later figure, refer to the section instead (e.g., *"detailed in Section 3.5"*).

### B1. Anti-Consecutive Figures & Dedicated Analytical Loop (严禁连续无文图表堆叠与独立闭环分析)
* **Strict Anti-Consecutive Mandate (严禁连续大图无文堆叠)**:
  - Never place two large figures (`\begin{figure}` / Word Figure Tables) or tables sequentially back-to-back without analytical paragraphs between them ("图堆图"属于顶刊排版大忌，严禁两图之间仅以空行、纯小节标题或机械过场套话隔开)。
  - Never bunch multiple figures together with a generic summary sentence (严禁出现如 *"As shown in Figs. 8 to 10..."* 这种跨多图混合、泛泛而谈的粗糙写法)。
* **Dedicated Analytical Loop (一图一论点，闭环深度分析)**:
  - Every core figure/table must carry an **explicit, irreplaceable core claim** (每个核心图/表必须承担一个明确且不可替代的论点).
  - Every core figure/table must be accompanied in adjacent text by a **four-step analytical loop**:
    1. **Lead-in & Claim (明确论点)**: State the investigative dimension and hypothesis.
    2. **Quantitative Result Description (定量结果描述)**: Report concrete metrics ($R^2$, RMSE, coverage PICP, interval width MPIW, extrema, inflections, diagonal alignment, error distribution).
    3. **Physical / Mechanistic & Model Explanation (物理机理与模型解释)**: Deeply trace phenomena to material damage mechanics (e.g., $9\%$ ice-water phase-change expansion, pore hydrostatic/osmotic pressure, ITZ microcrack nucleation, shear band localization) or algorithmic dynamics (e.g., Copula dependence preservation, LSTM gated damage accumulation, loss boundary admissible constraints).
    4. **Logical Transition (逻辑过渡)**: Synthesize the conclusion to naturally motivate the next question or subsequent figure.

### C. Multi-Subfigure Rigid Symmetric Grid Standard
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

1. **Step 1: Narrative & Jargon Audit**:
   - Verify the Three Core Narrative Principles: replace pretentious AI terms with plain engineering prose; ensure formulas serve concrete physics; verify civil-engineer-friendly titles and figure captions.
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


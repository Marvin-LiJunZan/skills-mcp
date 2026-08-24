---
name: ccc-academic-figure-style
description: Publication-grade scientific figure, Origin-ready Excel source-data, and LaTeX manuscript layout rules for Nature/Elsevier/CCC journals. Use for figure styling, multi-panel composition, reproducible figure-data export, image assets, Elsevier 5p two-column figure/table sizing, float-page whitespace, equation overflow, captions, LaTeX Workshop recipes, and XeLaTeX build verification.
---

# Academic Figure Style & Layout Standards (CCC Persona)

This skill defines the mandatory design, layout, and narrative rules for creating scientific figures in top-tier journals (e.g., *Cement and Concrete Composites*, *Cement and Concrete Research*, *Nature* family).

## 0. Strict Anti-Falsification & Data Integrity Rule (学术诚信与禁止数据造假铁律)

> [!CAUTION]
> **STRICT ZERO-TOLERANCE POLICY FOR SYNTHETIC/DUMMY FALLBACK DATA (严禁伪造数据与数学公式充数)**

- **Forbidden Synthetic Fallback Curves (严禁使用拟合/衰减公式伪造缺失数据)**:
  - 严禁在任何数据处理、绘图脚本或分析代码中引入“备用降级逻辑”（例如：“若 CSV/数据文件不存在，则调用指数衰减/对数正态/高斯拟合公式生成平滑过渡曲线”）。
  - 这种使用数学公式或随机数生成假的替代数据填充缺失文件的行为，属于典型的**学术不端与数据造假 (Academic Misconduct & Data Fabrication)**，在所有科研项目中被**绝对禁止**！
- **Fail-Fast Exception Handling (数据缺失必须直接报错中断)**:
  - 当指定的数据文件（如 `.csv`, `.npy`, `.json`, `.dat`）不存在、文件路径失效或提取到的数据为空时，**代码必须立即抛出显式异常（如 `FileNotFoundError`, `ValueError`）并直接终止程序**。
  - 严禁使用 `try-except` 静默吞掉错误，严禁在捕获文件缺失后自动切换至伪造数据生成器。数据缺失时唯二正确的做法是：**定位真实数据源路径，或向用户要求提供真实实验数据文件**。

---

## 1. Page Layout & Compactness (版面紧凑度与间距)

- **No Page-Wasting Single Figures**: A single figure should never occupy an entire page unless it is a 9-panel complex diagnostic map. Use compact aspect ratios ($4:3$ or $16:9$).
- **Evidence Chain Structure**: Align figures sequentially along a 5-step evidence chain:
  `Microstructure -> Geometric Metrics -> Steady Transport -> Transient Ingress -> Service Life Impact`.
- **Subfigure Grid Optimization**: Group related panels into $1\times 3$, $2\times 2$, or $3\times 3$ subfigure grids using Matplotlib `subplots` or LaTeX `subfigure`. Set explicit `wspace` ($0.2\sim 0.3$) and `hspace` ($0.25\sim 0.35$).
- **Margin Compliance**: Ensure all figure labels, colorbars, and legend text fit strictly within standard journal margins ($2.0\text{--}2.5\,\text{cm}$).

---

## 2. Text-First & Interleaved Narrative Flow (图文相间，严格一图一段)

- **Forbidden Layout (排版大忌)**: 严禁将两个或多个大图连续堆叠放置在同一页或连续页面（"图堆图"）。一段文字绝不能同时概括多个大图。
- **One-Figure-One-Paragraph Rule (一图一段/图文交替律)**:
  - 每一个大图（`\begin{figure}`）后面，**必须紧跟专属的深度分析段落**，详细阐述：
    1. 该图展示的具体物理/传质现象；
    2. 关键数值变化趋势与对比数据；
    3. 背后的微观结构机制或工程影响。
- **LaTeX Float Control & Anti-Blank Space (浮动体控制与严禁滥用 FloatBarrier)**:
  - **严禁盲目滥用 `\FloatBarrier`**：切勿在 `\section{...}` 或段落间随意添加 `\FloatBarrier`。在 Elsevier / IEEE 双栏排版（`elsarticle` 5p）中，`\FloatBarrier` 会强行清空浮动队列，导致前页右栏大面积抛空（Blank Column）或产生单行文本后全页留白。
  - **双栏大图 (`figure*`) 源码位置优化**：`figure*` 跨栏大图只能置于页顶。若将其写在 `\subsection{...}` 段落中间，会导致小节标题与文本被切断并产生巨型空白洞。正确做法是将 `figure*` 源码直接调整至 `\section{...}` 头部或页面起点，交由 LaTeX 浮动引擎自然浮动至页顶。

---

## 3. Bar Chart Aesthetics (柱状图设计标准)

- **White Interior / Hollow Center (柱体留白/白底)**:
  - **Never** use heavy, dark solid block fills for bars.
  - Set `color='white'` (or very light pastel fill) with bold colored borders (`edgecolor=COLOR`, `linewidth=2.0`).
  - Optionally apply subtle academic hatch patterns (`hatch='//'`, `\\\\`, `..`).
- **Palette Coordination (同组配色一致)**:
  - Match bar border colors strictly to the line plots or scatter markers in adjacent panels within the same figure group.
- **Callout Annotations (结论高亮框)**:
  - Never force readers to manually calculate differences between bars.
  - Always place a high-contrast annotated text box (e.g., `bbox=dict(boxstyle="round,pad=0.3", fc="#FEF3C7", ec="#F59E0B")`) above critical bars to highlight delta metrics (e.g., `$-4.7$ yrs ($-19.5\%$ earlier arrival)`).

---

## 4. 3D Volumetric Rendering Consistency (三维渲染一致性)

- **3D Depth & Lighting**: Enhance 3D perspective depth by adding subtle bounding boxes and axis grids.
- **Color Uniformity Across Subfigures (彻底消除多图色差)**:
  - For multi-panel 3D renders (e.g. comparing 7 hydration ages), set explicit single hex colors for pore spaces (e.g. Electric Sapphire Cyan `#00A3FF`).
  - **Disable auto-shading** (`shade=False` in Matplotlib 3D surfaces/voxels) to prevent lighting direction from altering hex colors across subfigures.

---

## 5. Domain Narrative & Logical Evidence Chain (科研故事线与循证表达)

- **Connect Abstract Metrics to Application Impact (从抽象指标到应用价值)**: 不应停留在纯粹的抽象数学/算法基准指标（如 Loss、PSNR、准确率）。必须将方法论偏差或性能提升，进一步联系到具体的学科应用场景与下游工程/科学结果中。
- **Evidence Chain Structure (完整循证逻辑链)**: 论文图表必须围绕一条严密的逻辑链条依次推演展开：
  `输入/结构基准 -> 关键中间表示与几何分析 -> 核心性能/传输求解 -> 下游应用影响/耐久性评估`。

---

## 6. Project Image Asset Organization & Naming Rules (通用科研项目图片资产管理与命名规范)

*注：本规范适用于所有顶刊与学术科研项目（无论投稿 CCC、Elsevier、Nature 还是 IEEE/Springer）。*

### 1. Directory Structure & Subfigure Folders (目录存储规范)
- **Unified Figures Directory (图片目录统一)**：所有论文出图必须统一存放于 `paper/figures/` (或 `figures/`) 目录下，严禁在项目根目录散落临时图片。
- **Dedicated Subfigure Folders (独立子图文件夹)**：对于包含多个对比面板的复合大图（如 Figure 4, Figure 5），必须建立以图号命名的专属子图文件夹，例如 `paper/figures/figX_subfigures/` (如 `fig4_subfigures/`, `fig5_subfigures/`, `fig8_subfigures/`, `fig10_subfigures/`)。

### 2. Semantic File Naming (语义化命名规范)
- **No Meaningless Generic Names (严禁无意义命名)**：绝对禁止使用 `temp.png`、`image1.png`、`fig_a.png` 或 `plot.png` 等模糊文件名。
- **Standardized Naming Pattern (统一命名格式)**：必须采用 **`figX_panel_[panel_id]_[descriptive_feature].png`** 或 **`[panel_id]_[Model/Method]_[Feature].png`** 结构，看文件名即知内容：
  - *示例*：`fig5_panel_a_Dice_Score.png`（第 5 图 Panel a Dice 分数）
  - *示例*：`fig8_panel_b_Single_Throat_Flux_Redistribution.png`（第 8 图 Panel b 孔喉通量重分布）
  - *示例*：`fig10_panel_d_Data_Compression.png`（第 10 图 Panel d 数据压缩率）
  - *示例*：`a1_Raw_XCT_Voxel_GT_23h.png`（第 4 图 a1 面板 23h 原始数据）

### 3. Standalone Subfigure Export & LaTeX Subfigure Composition (独立子图导出与 LaTeX 动态组图)
- **Standalone Subfigure Export (子图独立导出)**：Python/R 绘图脚本在绘制多面板图表时，**必须将各个子图独立导出保存为单张高清 PNG/PDF/SVG 文件**到对应子图目录中，严禁仅拼接导出无法拆分的整体图片。
- **LaTeX `subfigure` Modular Assembly (LaTeX \subfigure 动态组图)**：在 LaTeX 主文档中，必须使用 `\begin{subfigure}[b]{...}` 环境将独立子图拼装成组合大图 (`\begin{figure}`)。通过 `\hfill` 或 `\hspace{...}` 精确调整间距，利用 `(a)`, `(b)`, `(c)`, `(d)` 独立 caption/label，提升排版灵活性与出版规范度。

### 4. 1-to-1 Script Mapping (脚本与图表映射规范)
- **Modular Script Folder (出图脚本归类)**：所有绘图脚本统一存放于 `code/figure_scripts/` (或 `scripts/figure_scripts/`)。
- **Explicit Script Naming (清晰脚本命名)**：每个主图或图组对应独立的 Python/R 脚本，脚本名直观对应图号或主题（如 `fig4_3d_renderings.py`、`fig5_metrics_bar.py`、`fig8_microstructure_analysis.py`）。

### 5. Mandatory Origin-Ready Excel Source Data

Treat the figure image, plotting script, and source-data workbook as one inseparable deliverable. A data-driven figure is incomplete until all three exist and agree.

- Export one `.xlsx` workbook for every figure group, or one indexed project workbook containing a clearly named sheet for every figure or panel.
- Use semantic sheet names such as `F17_Capacity`, `F17_DRE`, and `F18_Intervals`; stay within Excel's 31-character sheet-name limit.
- Make every sheet directly usable in Origin:
  - curve/scatter/bar data: one header row, one variable per column, one observation per row;
  - multi-series curves: provide both authoritative long format and an Origin-friendly wide sheet when practical;
  - asymmetric intervals: export explicit `YErr-` and `YErr+` columns rather than requiring manual recalculation;
  - contour/heatmap data: export a regular matrix with X coordinates in the first row, Y coordinates in the first column, and Z values in the body; also retain long XYZ data when it is the authoritative output;
  - categorical plots: export the category label as a normal text column, not as cell formatting.
- Put units in column headers, for example `capacity_kNm`, `damage_pct`, and `cycles`; never mix numbers and unit strings in the same data column.
- Add an index/metadata sheet recording figure number, panel, title, authoritative source file, processing steps, data status, units, and the recommended Origin plot type.
- Mark evidence class explicitly where relevant: measured, derived, model output, parameter scan, uncertainty sample, or extrapolation.
- Preserve the authoritative raw source. Put transformations, pivots, error-bar calculations, or unit conversions in separate processed sheets or explicit helper columns.
- Export the exact numerical array used to draw the figure. Do not round the workbook more aggressively than the plotting code, and do not reconstruct source data from rendered pixels.
- If only an image or an Origin project exists and no machine-readable worksheet can be accessed, mark the figure as `Missing source data` in the index and stop. Never digitize the image or create a synthetic replacement unless the user explicitly requests digitization and accepts its uncertainty.
- Validate the exported workbook by reopening or inspecting it, checking all expected sheets, row/column counts, numeric types, missing values, error-bar identities, and matrix dimensions.
- Keep the workbook filename tied to the figure asset, for example `Fig17_Data_for_Origin.xlsx`, or use an explicit indexed bundle such as `All_Figure_Data_for_Origin.xlsx`.
- When the user asks for "all figure data," audit every manuscript figure. Include image/schematic figures in the index as `Not applicable`, and list unresolved numeric figures as `Missing`; do not silently omit them.

Completion gate:

```text
figure image exists
+ plotting script exists
+ Origin-ready Excel source data exists
+ workbook validation passes
= figure task complete
```

---

## 7. Font & Typography Standards (英文 Times New Roman 字体强制规范)

- **Mandatory English Font Standard (英文 Times New Roman 铁律)**:
  - 所有用于期刊投稿的英文图表、图例、坐标轴标签（X/Y Axis Labels）、刻度文字（Tick Labels）、滴标文本（Annotations）、色卡图例（Colorbar Labels）、比例尺文本（Scale Bars）以及子图标题（Subfigure Titles），**必须统一采用 Times New Roman 字体**。
  - **Matplotlib 脚本标准配置**：在所有出图 Python 脚本开头，必须显式声明如下 `rcParams` 配置：
    ```python
    plt.rcParams['font.sans-serif'] = ['Times New Roman', 'DejaVu Sans', 'Arial']
    plt.rcParams['font.serif'] = ['Times New Roman']
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['mathtext.fontset'] = 'stix'  # 保证 MathTeX 数学公式与 Times New Roman 完美匹配
    ```
- **Math & Units Consistency (数学公式与单位一致性)**:
  - 图表中的所有物理量符号（如 $D_{\mathrm{eff}}$, $\Delta C$, $LCC$, $T_{\mathrm{crit}}$）必须采用 LaTeX MathTeX 格式包裹，并与论文正文中的符号与字体完全相符。
  - **Matplotlib / SHAP 特征名称下标铁律**：在 Python 绘图脚本中，所有带下标的物理量/特征标签（如 $\mu_e$, $\sigma_c$, $\varepsilon_c$）在传给 Matplotlib 或 SHAP `summary_plot` 的 `feature_names` 列表时，**必须显式声明为 Raw LaTeX Math 格式（如 `r"$\mu_e$"`）**。严禁使用普通 Unicode 文本（如 `"μe"`），否则 Matplotlib 会将下标字母当作同行字符绘制，导致下标格式丢失。

---

## 8. Elsevier LaTeX Layout and Build Workflow

For `elsarticle` conversion, two-column figure/table sizing, multi-panel assembly, float-page whitespace, English captions under `ctex`, long equations, asset checks, LaTeX Workshop configuration, and compile verification, read [references/latex-elsevier-layout.md](references/latex-elsevier-layout.md).

The reference contains the validated fix for the Fig. 11/Fig. 12 blank-space case. Its LaTeX float guidance takes precedence over generic float-control advice elsewhere in this skill: inspect the float class and queue first, tune double-column parameters for `figure*`/`table*`, and treat forced barriers or page breaks as last-resort layout decisions.

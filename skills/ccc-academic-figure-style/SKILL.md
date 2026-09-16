---
name: ccc-academic-figure-style
description: Publication-grade figure design rules for Nature/Elsevier/CCC journals, covering white-center bar charts, color coordination, 3D volumetric consistency, compact layout, and text-first narrative flow.
---

# Academic Figure Style & Layout Standards (CCC Persona)

This skill defines the mandatory design, layout, and narrative rules for creating scientific figures in top-tier journals (e.g., *Cement and Concrete Composites*, *Cement and Concrete Research*, *Nature* family).

---

## 0. Universal Mandatory Color Palette & Contrast Selection Rules (全图强制统一色系与对比度选取原则)

**核心法则（全图默认强制执行）**：
所有学术图表（包括散点图、折线图、柱状图、直方图、时序曲线、等高线、SHAP分析等）**必须且只能遵循以下统一的 6 阶蓝红渐变色阶系统**，辅以专属的高亮亮黄色：

### 1. 基础 6 阶蓝红标准色板 (6-Step Blue-to-Red Palette)
```python
BLUE_RED_6 = [
    "#2F6AB9",  # 阶1: 深海蓝 (Dark Sapphire Blue - 极低值/基线)
    "#69AADB",  # 阶2: 浅海蓝 (Light Sky Blue - 次低值)
    "#97C6E6",  # 阶3: 柔和冰蓝 (Soft Ice Blue - 中低值)
    "#F6B7B2",  # 阶4: 柔和浅红 (Soft Peach Red - 中高值)
    "#EA7B7D",  # 阶5: 珊瑚深粉 (Coral Rose - 次高值)
    "#F14040",  # 阶6: 绯红强色 (Crimson Vivid Red - 极高值/峰值)
]
HIGHLIGHT_YELLOW = "#FEC211"  # 专属特别高亮/趋势线/最优标注亮黄色
```

### 2. 颜色数量选取与最大对比度策略 (Color Selection & Maximum Contrast Strategy)
- **物理量含义映射**：
  - **蓝色系（`#2F6AB9` 系列）**：严格代表参数值低（Low Value）、物理量基线（Baseline）、训练集、未受损状态等；
  - **红色系（`#F14040` 系列）**：严格代表参数值高（High Value）、实测/目标对比值、测试集、高应力/高温/高损伤等；
- **2 种颜色需求（最常用）**：
  - **必须优先取首尾两端最大对比度色**：`#2F6AB9`（深海蓝）与 `#F14040`（绯红强色）。
- **3~5 种颜色需求（从两头向中间渐进扩展，确保对比度最大化）**：
  - **3 种颜色**：`#2F6AB9`（低值/首端）、`#97C6E6`（中间值）或 `#5D6D7E`（中性灰）、`#F14040`（高值/尾端）；
  - **4 种颜色**：`#2F6AB9`（阶1）、`#69AADB`（阶2）、`#EA7B7D`（阶5）、`#F14040`（阶6）；
  - **5 种颜色**：`#2F6AB9`（阶1）、`#69AADB`（阶2）、`#97C6E6`（阶3）、`#EA7B7D`（阶5）、`#F14040`（阶6）；
- **6 种颜色需求（连续/阶梯物理参数分布）**：
  - 严格按数值从低到高依次完整映射 6 个色阶：`["#2F6AB9", "#69AADB", "#97C6E6", "#F6B7B2", "#EA7B7D", "#F14040"]`；
- **特别突出/高亮指示需求**：
  - 当需要对某个关键数据点、最优模型 Callout、核平滑趋势线或核心结论进行特别强调时，**统一且唯一采用 `#FEC211` 亮黄色**（半透明无黑色描边或专属高亮外框）。

---

## 1. Page Layout & Compactness (版面紧凑度与间距)

- **No Page-Wasting Single Figures**: A single figure should never occupy an entire page unless it is a 9-panel complex diagnostic map. Use compact aspect ratios ($4:3$ or $16:9$).
- **Subfigure Grid Optimization**: Group related panels into $1\times 3$, $2\times 2$, or $3\times 3$ subfigure grids using Matplotlib `subplots` or LaTeX `subfigure`. Set explicit `wspace` ($0.2\sim 0.3$) and `hspace` ($0.25\sim 0.35$).
- **Margin Compliance**: Ensure all figure labels, colorbars, and legend text fit strictly within standard journal margins ($2.0\text{--}2.5\,\text{cm}$).

---

## 2. Text-First Narrative Flow & Anti-Blank Space (先文后图，排版节奏与严禁滥用 FloatBarrier)

- **Forbidden Rule (忌讳)**: Never place two large figures sequentially back-to-back without analytical paragraphs between them ("图堆图"属于论文排版大忌).
- **Text-First Principle**: Every figure float (`\begin{figure}`) and table float (`\begin{table}`) must be preceded by 1–2 paragraphs of quantitative analysis explaining:
  1. What evidence the figure/table presents;
  2. The key metrics or trend transitions;
  3. The physical mechanism or engineering implication.
- **Independent Narrative for Every Table and Figure (一表一文、一图一文，严禁图表合并笼统带过)**:
  - **一图一叙事原则（One Figure, One Story）**：每个表格（Table）与每个图表（Figure）**必须各自拥有独立的专属深度分析段落**。**严禁出现“如 Fig. 4 与 Fig. 6 所示……”这种跨多图混合、泛泛而谈的粗糙写法**。
  - 每张图在正文中必须遵循标准的**四步分析闭环**：
    1. **引导看图**：明确引出图表（如“基于 Multi-Otsu 分割得到的水泥浆体三相组成随水化时间演化如图 4 所示……”）；
    2. **定量读数**：从图表与各子图中提取具体数值、变化幅度、特征拐点（如“体积分数由 23 h 的 $23.13\%$ 显著降至 668 h 的 $13.01\%$”）；
    3. **机理解释**：结合材料科学或物理机制深入阐释现象背后的原因（如“熟料溶解、C-S-H 凝胶沉淀导致毛细孔道充填细化”）；
    4. **小结与过渡**：得出该图的核心结论，并自然引出下一阶段的分析或后续图表。
  - **表格分析段落**：重点聚焦多维度分层数据（Subsets）、横向基线模型衬托对比（突出当前模型在恶劣工况下的断层优势）；
  - **图表分析段落**：必须紧密结合各子图编号（如 (a), (b), (c), (d)）逐面板展开细致拆解，详细说明瞬态时序演化轨迹、单步变化量捕捉、1:1 散点对角线拟合精度以及分层误差柱状图分布。
- **Caption vs. Body Text Division of Labor (图题注自解释性与正文深度分析的严格职责分工)**:
  - **图题注（Caption - Self-contained & Reviewer-Intuitive 原则）**：图题注的职责是**“让土木与工程审稿人脱离正文单独看图也能一眼看懂图的物理内容与核心结论”**。包括：
    1. 简洁精炼的主标题（告诉读者图的主题），**严禁堆砌生僻算法黑话**（如严禁写 *conflict-aware gradient stiffness diagnosis manifold*，一律写成直观明了的表达如 *Loss weighting procedure: evaluating gradient influences prior to training to establish fixed bounds*）；
    2. 各子图面板的准确物理含义（如 `(a) 三相体积分数的堆叠面积演化; (b) 孔隙率与水化产物双轴曲线`）；
    3. 关键测试条件或控制参数（如材料配合比 $w/c=0.35$、边界条件）；
    4. **严禁在 Caption 中堆砌大段机理推导、长篇结论或重复正文叙述**。
  - **正文描述（Body Text - 深度剖析）**：承担全部的**定量对比、数据挖掘、物理机理解释与逻辑推进**。正文必须显式引用具体子图编号（如 `Fig. 4a`, `Fig. 4b`）。
- **Strict Anti-FloatBarrier Abuse (严禁滥用 FloatBarrier 导致双栏空洞)**:
  - 严禁在 `\section{...}` 之前或段落间盲目使用 `\FloatBarrier`。在双栏 LaTeX (如 `elsarticle`) 中，`\FloatBarrier` 会强制清空浮动队列，极易导致上一页右栏大面积抛空（Blank Column）或产生单行文本后全页留白。
- **Double-Column Figure (`figure*`) Placement Anchor**:
  - `figure*` 跨栏大图只能置于页顶。若将其写在 `\subsection{...}` 段落中间，会导致小节标题与文本被切断并产生巨型空白洞。正确做法是将 `figure*` 源码直接调整至 `\section{...}` 头部或页面起点，交由 LaTeX 浮动引擎自然浮动至页顶。
- **Matplotlib / SHAP MathTeX Subscript Rule**:
  - 在 Python 绘图脚本中，所有带下标的物理量/特征标签（如 $\mu_e$, $\sigma_c$, $\varepsilon_c$）在传给 Matplotlib 或 SHAP `summary_plot` 时，**必须显式声明为 Raw LaTeX Math 格式（如 `r"$\mu_e$"`）**，严禁使用普通 Unicode 文本（如 `"μe"`）。

---

## 3. Bar Chart Aesthetics & Typography (柱状图设计与字体排版标准)

### 3.1 No Decorative Callout Boxes (禁止装饰性圆角标签框)
- 结论标注默认采用简短、无边框的文本，直接靠近对应数据点、柱顶或趋势线。
- 禁止使用大面积圆角 `bbox`、彩色实心标签框或演示稿式气泡框；它们会遮挡数据并破坏论文图的视觉层级。
- 如确实需要突出核心结论，只允许使用 CCC 亮黄色 `#FEC211` 的短文本、细线或小型箭头，且不能形成大块背景。
- 默认不在图内添加额外结论 callout；关键结论应放在 caption 或正文中。只有用户明确要求时才加入短标签。

### 3.2 Compact 3D Panel Labels (三维结构图面板标签简洁化)
- 3D 结构对比图禁止在每个面板顶部堆叠长句式标题；结构本身必须是视觉主体。
- 每个面板只保留底部居中的短标签，例如 `(a) Source`, `(b) Role-only`, `(c) Role + mechanics`, `(d) Final optimum`。
- 网格、视角、尺度和色条在同一组面板中必须保持一致，避免标签和装饰元素分散读者注意力。

- **Universal Typography (全图强制采用 Times New Roman 字体)**:
  - 图中所有文本（包括轴标题、刻度标签、图例、数据标注、高亮 Callout、子图题注）**必须统一采用 Times New Roman 字体**（`plt.rcParams['font.family'] = 'Times New Roman'`, `plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif', 'serif']`，数学公式设置 `plt.rcParams['mathtext.fontset'] = 'stix'`）。
- **Subpanel Captions Mandatory at Bottom Centered (多子图/组图题注 (a)/(b)/(c) 必须置于各子图正下方居中)**:
  - **严禁顶部堆叠或偏离居中**：严禁将 `(a)`, `(b)`, `(c)` 题注、子图标题或顶角英文字母（如 `A`, `B`）放置在子图顶部。
  - **统一居中置底标准**：所有横向并排或网格排布的多子图（如 $1\times 2$, $2\times 2$, $2\times 3$, $2\times 4$），各子图题注必须统一置于该子图 x 轴下方居中位置：
    ```python
    ax.text(0.5, -0.26, "(a) Subplot Description", transform=ax.transAxes, 
            ha="center", va="top", fontsize=8.0, fontweight="bold", fontfamily="Times New Roman")
    ```
  - **留足底部间距**：生成图形时必须通过 `fig.tight_layout(rect=[0, 0.05, 1, 1])` 或 `subplots_adjust(bottom=0.20~0.25)` 预留充分的底部空间，杜绝文字被图片边界裁切。
- **White Interior / Hollow Center (柱体留白/白底)**:
  - **Never** use heavy, dark solid block fills for bars.
  - Set `color='white'` (or very light pastel fill) with bold colored borders (`edgecolor=COLOR`, `linewidth=1.8~2.0`).
  - Subtle academic hatch patterns (`hatch='//'`, `\\\\`, `..`); **all bar hatch/fill lines must be white** (`hatch.color='white'`) so the pattern remains clean and consistent across CCC figures.
- **Palette Coordination (同组配色一致)**:
  - Match bar border colors strictly to the line plots or scatter markers in adjacent panels within the same figure group.
- **Universal Inward Tick Marks & Clean Boxed Spines (全图强制刻度线朝内、上/右边框刻度关闭规范)**:
  - **刻度线朝内强制规则**：所有学术图表（包括折线、散点、柱状、雷达、SHAP、等高线等）的刻度线**必须严格全部朝内（`direction='in'`）**。Matplotlib 默认的朝外刻度（`out`）属于非专业草稿风格，必须全局覆写为朝内。
  - **上框线与右框线刻度关闭（No Top and Right Ticks）**：四周矩形全围合边框必须保留（`top`, `bottom`, `left`, `right` 边框线宽 $0.8\sim 1.0\,\text{pt}$，颜色中性深灰或黑色 `#222222`），**但顶部和右侧边框一律关闭刻度线**（除非包含显式 `ax.twinx()` 双坐标轴）：
    ```python
    plt.rcParams['xtick.direction'] = 'in'
    plt.rcParams['ytick.direction'] = 'in'
    plt.rcParams['xtick.top'] = False
    plt.rcParams['ytick.right'] = False
    plt.rcParams['xtick.minor.visible'] = False
    plt.rcParams['ytick.minor.visible'] = False
    ```
    在单个子图内设置时统一使用：`ax.tick_params(direction='in', top=False, right=False)`。确保刻度线仅在左轴与底轴精致内向展示，上/右边框保持干净利落。
- **Callout Annotations & Arrow Optimization (结论高亮框与指引箭头规范)**:
  - 核心增益指标直接在柱体上方或内部配置高对比度 Callout 框（`bbox=dict(boxstyle="round,pad=0.35", fc="#EFF6FF", ec=COLOR, lw=1.2)`）。
  - **指引箭头严禁交叉乱穿**：箭头必须采用清晰利落的垂直单向指引（如从高亮框垂直指向柱顶 `xytext=(x, y_high), xy=(x, y_bar)`）或规整弧线，严禁箭头横跨其他柱体、穿过数据数值或遮挡图例。对于超高柱体，可直接将 Callout 徽章内嵌于空心柱体内部居中展示。

---

## 4. 3D Volumetric Rendering Consistency (三维渲染一致性)

- **3D Depth & Lighting**: Enhance 3D perspective depth by adding subtle bounding boxes and axis grids.
- **Color Uniformity Across Subfigures (彻底消除多图色差)**:
  - For multi-panel 3D renders (e.g. comparing 7 hydration ages), set explicit single hex colors for pore spaces (e.g. Electric Sapphire Cyan `#00A3FF`).
  - **Disable auto-shading** (`shade=False` in Matplotlib 3D surfaces/voxels) to prevent lighting direction from altering hex colors across subfigures.

---

## 5. Durability & Physical Storytelling (材料与耐久性故事主线)

- **Focus on Engineering Outcomes**: In material/durability papers (CCC persona), do not stop at abstract coefficients ($D_e/D_0$). Always connect transport bias to concrete engineering consequences (e.g., chloride ingress depth $C(x,t)$, steel depassivation initiation time $T_{\text{crit}}$).
- **Evidence Chain Structure**: Align figures sequentially along a 5-step evidence chain:
  `Microstructure -> Geometric Metrics -> Steady Transport -> Transient Ingress -> Service Life Impact`.

---

## 6. Research Intake & Literature Search Protocol (科研前置文献检索规范)

- **Mandatory Pre-project Requirement (新项目启动前置流程)**:
  - 每次启动新的科研课题或项目之前，必须首先总结并输出该领域的核心关键词。
  - 使用关键词前往 Web of Science (WOS) / OpenAlex / EuropePMC 搜索并筛选相关高水平文献。
  - **下载带摘要的 BibTeX 条目 (`.bib` 文件)** 并保存至本地项目目录（如 `paper/references.bib` 或 `dataset/literature/`）。
  - 对本地带摘要的文献条目进行系统化提炼与分析，梳理出研究空白（Research Gap）、已有方法局限性及本研究的切入点后，方可开展具体的代码与实验设计。

---

## 7. Radar Chart Design & Metric Polarity Alignment Standards (学术雷达图设计与极性统一规范)

- **Monotonic Area-Performance Rule (面积单调性法则 / 外圈最优原则)**:
  - 在学术雷达图中，多边形所包围的几何面积必须严格单调反映模型的综合优越性（**面积越大 = 综合性能越强**）。
  - 雷达图的最外圈（归一化刻度 1.0）必须严格对应**最佳性能点**，中心点（刻度 0.0）必须严格对应**最劣/失效性能点**。
- **Metric Polarity Inversion (极性反转与正负指标归一化)**:
  - **正向指标（越大越好，如 $R^2 \uparrow$、准确率 $\mathrm{Acc} \uparrow$、相关系数 $r \uparrow$、鲁棒性指标）**：
    直接正向归一化至 $[0, 1]$：
    $$\text{Score} = \frac{\text{Value} - \text{Min}}{\text{Max} - \text{Min}}$$
  - **负向/误差指标（越小越好，如 $\mathrm{RMSE} \downarrow$、$\mathrm{MAE} \downarrow$、计算延迟 $\mathrm{Latency} \downarrow$、滞后步长误差）**：
    **必须执行反向映射（Inverted Scaling）**：
    $$\text{Score} = \frac{\text{Max} - \text{Value}}{\text{Max} - \text{Min}} \quad \text{或} \quad \text{Score} = 1 - \frac{\text{Value} - \text{Min}}{\text{Max} - \text{Min}}$$
    确保误差越小、耗时越低、偏离度越低的模型，其多边形顶点向最外圈 1.0 扩张，而严重误差被压缩在中心 0.0 区域。
- **Explicit Metric Direction Notation (各轴方向指示与物理量标注)**:
  - 每个雷达轴标签必须显式标注指标极性方向符号（如 `$\uparrow$` 或 `$\downarrow$`，或使用逆误差形式如 `$\mathrm{RMSE}^{-1} \uparrow$`），严禁使用无方向概念的抽象模糊英文。
- **Individual Axis Scaling & Callout (独立轴刻度与可解释性)**:
  - 避免让审稿人产生“无量纲失真”误解，各轴归一化基准区间必须在图表附注或正文中透明声明；对于关键瓶颈轴，需在轴端或顶点清晰标注真实物理量级（如标注最佳值与基线值）。
- **Subpanel Captions at Bottom (题注必须置于底部居中)**:
  - 雷达图子图编号 `(a) ...` 必须置于雷达图正下方居中（`ax.text(0.5, -0.25, '(a) ...', transform=ax.transAxes, ha='center', va='top')`），预留充足底部间距（`pad_inches=0.08`），严禁顶部堆叠或偏离居中。

---

## 8. SHAP Dependence & Feature Interaction Scatter Standards (SHAP 依赖与非线性特征交互图标准)

- **Unified 6-Step Blue-to-Red Colormap (标准 6 阶蓝红渐变色带)**:
  - 散点图的次级交互特征（Secondary Interaction Feature）颜色映射与侧边 Colorbar 必须严格采用 6 阶科学蓝红渐变：
    ```python
    from matplotlib.colors import LinearSegmentedColormap

    BLUE_RED_6 = ["#2F6AB9", "#69AADB", "#97C6E6", "#F6B7B2", "#EA7B7D", "#F14040"]
    blue_red_cmap = LinearSegmentedColormap.from_list("BlueRed6", BLUE_RED_6, N=256)
    ```
- **Colorbar Tick & Padding Optimization (色条微型紧凑化与短刻度规范)**:
  - 色条必须使用 `make_axes_locatable(ax)` 依附于子图右侧，宽度紧凑（`size="4.0%"`, `pad=0.05`）。
  - **色条刻度线长必须改短（Short Ticks）**：严禁用过长、粗糙的默认刻度，必须通过 `cbar.ax.tick_params(labelsize=6.0, length=1.8, width=0.5, pad=1)` 缩短刻度线长度至 $1.5\sim 2.0\,\text{pt}$，保证色带边缘精致利落。
- **Golden Trendline without Border (亮黄平滑拟合趋势线)**:
  - 在散点图上方叠加高斯加权核平滑趋势线（Gaussian Kernel Smoothing Trendline），颜色固定采用亮黄色 `#FEC211`。
  - **严禁使用黑色描边外框**，设置半透明度 `alpha=0.5`，线宽 `linewidth=2.0`，确保既清晰指明整体非线性响应走势，又不遮挡底层散点分布。
- **Subpanel Bottom-Centered Lowercase Captions (子图编号全部小写并居中置底)**:
  - 所有多子图编号必须严格采用小写 `(a), (b), (c), (d), (e), (f), (g), (h)`。
  - 标题必须置于子图底部居中：`ax.set_title(f"({letter}) {feat_title}", fontsize=8.5, fontweight="bold", loc="center", y=-0.35)`。
- **Standard Python Implementation Template (标准绘图代码范例)**:
  ```python
  import matplotlib.pyplot as plt
  from matplotlib.colors import LinearSegmentedColormap
  from mpl_toolkits.axes_grid1 import make_axes_locatable
  import numpy as np

  BLUE_RED_6 = ["#2F6AB9", "#69AADB", "#97C6E6", "#F6B7B2", "#EA7B7D", "#F14040"]
  blue_red_cmap = LinearSegmentedColormap.from_list("BlueRed6", BLUE_RED_6, N=256)

  fig, axes = plt.subplots(2, 4, figsize=(12.0, 4.2))
  axes_flat = axes.flatten()

  for idx, (x_vals, y_vals, c_vals, label_x, label_c, feat_name, letter) in enumerate(specs):
      ax = axes_flat[idx]
      # 1. 真实散点
      sc = ax.scatter(x_vals, y_vals, c=c_vals, cmap=blue_red_cmap, s=8, alpha=0.65, edgecolors="none", zorder=2)
      
      # 2. 高斯核平滑 #FEC211 趋势线 (无描边，alpha=0.5)
      sort_mask = np.argsort(x_vals)
      x_s, y_s = x_vals[sort_mask], y_vals[sort_mask]
      x_line = np.linspace(x_s.min(), x_s.max(), 120)
      h = max((x_s.max() - x_s.min()) / 12.0, 1.0)
      w = np.exp(-0.5 * ((x_line[:, None] - x_s[None, :]) / h) ** 2)
      y_line = np.sum(w * y_s[None, :], axis=1) / np.maximum(np.sum(w, axis=1), 1e-6)
      ax.plot(x_line, y_line, color="#FEC211", linewidth=2.0, alpha=0.5, zorder=4)

      # 3. 轴标签与底部居中小写题注
      ax.axhline(0, color="gray", linestyle="--", linewidth=0.7, zorder=1)
      ax.set_xlabel(label_x, fontsize=7.5, labelpad=2)
      ax.set_ylabel(f"SHAP Value for {feat_name}", fontsize=7.5, labelpad=2)
      ax.set_title(f"({letter}) {feat_name}", fontsize=8.5, fontweight="bold", loc="center", y=-0.35)
      ax.grid(True, linestyle=":", alpha=0.35)
      
      # 4. 紧凑色条与短刻度线 (length=1.8)
      divider = make_axes_locatable(ax)
      cax = divider.append_axes("right", size="4.0%", pad=0.05)
      cbar = fig.colorbar(sc, cax=cax)
      cbar.set_label(label_c, fontsize=6.8, labelpad=2)
      cbar.ax.tick_params(labelsize=6.0, length=1.8, width=0.5, pad=1)

  fig.tight_layout(pad=0.3, h_pad=0.4, w_pad=0.3)
  ```

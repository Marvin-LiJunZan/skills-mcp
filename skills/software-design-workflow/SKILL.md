---
name: software-design-workflow
description: "End-to-end software product design and aesthetic UI engineering workflow. Integrates hand-drawn conceptual wireframing (Rough.js), technical architecture diagrams (Mermaid), systematic accessible palettes (Radix Colors), modern typography (Fontsource), designer-grade component systems (shadcn/ui), dynamic KPI cards (README Stats), brand vectors (Simple Icons), status tags (Markdown Badges), and industrial desktop delivery standards (CCC-UI/Electron)."
metadata:
  short-description: "End-to-end software & aesthetic UI design full-lifecycle workflow"
---

# Software Design Workflow — 软件设计全流程技能

本技能是现代高质感软件产品从**概念原型**、**设计系统定义**、**高保真交互组件**到**工程级桌面软件交付**的全生命周期设计中枢。

它将 8 大高端审美工具体系与工程级桌面交互规范紧密结合，彻底终结传统 AI 生成界面时的“塑料感”、“过度圆角”、“花哨失控”与“工程脱节”。

---

## 1. 软件设计全生命周期与技能矩阵

```text
[阶段一: 需求与概念原型]
  │──> mermaid-charts   : 业务流程图、系统架构图、数据时序流
  └──> roughjs-design   : 充满人类手作质感的手绘线框草图，快速对齐产品共识
        │
[阶段二: 视觉与设计系统规范]
  │──> radix-colors     : 严谨 12 阶无障碍对比度色彩标尺（亮暗色对称映射）
  │──> fontsource       : 现代专业排版字体阶梯（Inter, Plus Jakarta Sans, JetBrains Mono）
  │──> simple-icons     : 官方单色/品牌矢量技术图标库
  └──> markdown-badges  : 状态徽章与技术栈指示标牌
        │
[阶段三: 高保真交互与看板]
  │──> shadcn-ui        : 现代企业级 UI 原语（克制投影、精细微交互、自适应布局）
  └──> readme-stats     : 矢量级实时遥测指标动态卡片、统计进度看板
        │
[阶段四: 工程级桌面软件交付]
  └──> ccc-ui           : 工业桌面端 Chrome 规范（原生顶级菜单栏、快捷键合同、
                          WebGL/WebGPU 3D与BIM几何底座、低延迟遥测、便携免安装打包）
```

---

## 2. 阶段执行规程与产出标准

### 阶段一：需求调研与低保真概念（Idea & Architecture）
- **触发场景**：刚开始构思新功能、定义软件架构或绘制低保真线框原型。
- **调度子技能**：
  - 调用 `skills/mermaid-charts` 输出系统架构图与数据时序流：
    ```markdown
    %%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#f8fafc', 'lineColor': '#64748b'}}}%%
    flowchart LR
        Client[桌面客户端] --> Gateway[API网关] --> Engine[计算分析内核]
    ```
  - 调用 `skills/roughjs-design` 生成具备自然手绘感的产品原型与线框图，避免一开始陷入像素级争论。

### 阶段二：建立工程级 Design System
- **触发场景**：确立产品调色盘、排版层级、图标体系与品牌标识。
- **调度子技能**：
  - **色彩定义** (`skills/radix-colors`)：严格遵循 12 阶明度阶梯。背景（Step 1-2）、组件（Step 3-5）、边框（Step 6-8）、强调高亮（Step 9-10）、文字（Step 11-12）。
  - **字体阶梯** (`skills/fontsource`)：UI 主文本统一 Inter，数字遥测与代码统一 JetBrains Mono（启用 `tabular-nums` 防抖动）。
  - **图标与徽章** (`skills/simple-icons`, `skills/markdown-badges`)：统一采用 24x24 矢量 viewBox，以 `currentColor` 保持界面色彩协调。

### 阶段三：高保真界面与数据看板（High-Fidelity UI）
- **触发场景**：编写网页端或客户端实际界面代码、仪表盘与统计卡片。
- **调度子技能**：
  - **组件库选用** (`skills/shadcn-ui`)：使用 Tailwind + Radix 原语，卡片圆角严格控制在 `rounded-lg` (8px)，按钮与标签使用 `rounded-md`，拒绝夸张大阴影。
  - **数据展示卡片** (`skills/readme-stats`)：实时监测数据、硬件利用率、计算收敛度采用矢量化 SVG 或高对比度统计卡片排列。

### 阶段四：工程级软件交付与硬件交互（Desktop Delivery）
- **触发场景**：打包为可执行桌面软件（Electron）、接入串口/传感器遥测或集成 3D/BIM 场景。
- **调度子技能**：
  - 继承 `skills/ccc-ui` 的工业软件 Chrome 标准：
    - 统一顶级菜单栏布局：`文件` $\rightarrow$ `编辑` $\rightarrow$ `视图` $\rightarrow$ `窗口` $\rightarrow$ `帮助`。
    - 严格绑定标准快捷键（`Ctrl+R` 刷新，`F11` 全屏，`Alt/F10` 激活菜单）。
    - 优先产出免安装便携版（Portable Build），保护用户生产环境。

---

## 3. 相对路径与跨平台通用性保证

本全流程体系内部所有工具、子技能调用及脚本，均采用**相对当前工作区或仓库根目录的相对路径**（例如 `scripts/xxx.py` 或 `./components/...`），严禁包含任何特定盘符或用户名硬编码。无论团队成员在 Windows、macOS 还是 Linux 上拉取仓库，均可开箱即用。

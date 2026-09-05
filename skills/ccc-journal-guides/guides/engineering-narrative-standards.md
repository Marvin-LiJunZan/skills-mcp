# 土木与工程 AI 论文写作三大铁律与学术叙事实战标准
# (Engineering-First Academic Narrative & Anti-Jargon Standards)

本规范专为 **土木工程、结构工程、建筑材料与智能建造领域** 的 AI/计算力学交叉学科论文制定。旨在彻底清除“纯计算机套话”、“硬造假大空术语”、“无意义符号堆砌”等导致工程审稿人反感的顽疾，产出真正成熟、地道、经得起顶刊同行评审推敲的学术论文。

---

## 核心指导思想 (Core Philosophy)

> 真正成熟的顶级工程学术论文，力量源于**物理机制的深刻透彻**与**工程问题的清晰解决**，而非辞藻的浮夸与术语的生造。
> 审稿人是土木、结构与材料领域的工程学者，论文的一切表达必须建立在**工程物理直觉与严密数学逻辑**之上。

---

## 铁律一：概念能用普通话讲清就不造术语 (Plain Language over Jargon)

### 1. 核心红线 (Red Lines)
- **严禁为了“显得高级”而硬造复合学术新词**（如滥用 *gradient stiffness diagnosis*, *conflict-aware bounded allocation*, *spatiotemporal manifold synergism*, *holistic cognitive fusion* 等）。
- **正文主线、摘要与主旨段落必须用最朴实、精准、直接的工程/数学大白话把核心机制讲透**。

### 2. 术语降级与主线表达规范 (Jargon Relegation)
- **主线表达必须简洁直接**：
  > **标准正文主线**：
  > *“训练前先判断各损失项对参数更新的影响，再在限定范围内确定固定权重。”*
  > *(English: Prior to training, the influence of individual loss terms on parameter updates is evaluated to determine fixed weights within a bounded range.)*
- **生造术语的处理原则**：
  - 像 “gradient stiffness diagnosis”、“conflict-aware bounded allocation” 这类词汇，**绝不能成为整篇文章的主题表达、标题主语或摘要中心词**。
  - 它们**仅可降级保留在方法细节的小节局部**（如作为某个具体子模块或变量命名的小括号注释），且必须在首次出现时紧跟一句话大白话解释其实际物理/计算含义。

### 3. 典型对比案例 (Before vs. After)

| 场景 | ❌ 浮夸生造/AI味表达 (Reject) | ✅ 成熟工程学术表述 (Accept) |
| :--- | :--- | :--- |
| **多目标损失平衡** | We develop a *conflict-aware gradient stiffness diagnosis and bounded allocation paradigm* to synergistically orchestrate loss landscapes. | *Prior to model training, the relative sensitivity of individual loss terms on gradient updates is evaluated to determine bounded, fixed weighting factors.* (训练前先评估各损失项对参数更新的影响，并在限定范围内确定固定权重。) |
| **物理约束嵌入** | A *physically-grounded continuous manifold projection mechanism* is innovatively introduced to harmonize kinematics. | *The governing differential equations and boundary constraints of beam deformation are incorporated directly into the loss function.* (将梁变形的控制微分方程与边界条件直接嵌入损失函数中。) |
| **特征融合** | A *deep multi-scale semantic aggregation network* is proposed to capture holistic hierarchical clues. | *High-resolution surface crack textures and macro-scale deformation contours are combined to detect localized damage.* (结合高分辨率表面裂缝纹理与宏观变形轮廓以识别局部损伤。) |

---

## 铁律二：公式只服务于问题，不为了“显得高级”堆符号 (Formulas Serve Problems, Not Pretentious Symbol-Stacking)

### 1. 核心红线 (Red Lines)
- **每一个数学公式必须严格对应具体的物理定律、力学约束、平衡方程或明确可执行的算法步骤**。
- **严禁无实际推导增量、无物理实质、纯粹为了“充门面”而堆砌冗余的多重下标、花体符号、嵌套映射**。

### 2. 数学表达与符号规范
1. **单变量物理清晰度**：
   - 每一个变量第一次出现时，必须在同一段落内用明确的**物理定义与国际标准单位**交代清楚。
   - 示例：*“where $E_c$ is the elastic modulus of concrete ($\text{GPa}$), and $\varepsilon_{\text{cr}}$ represents the tensile cracking strain.”*
2. **拒绝伪数学化（Pseudo-mathematization）**：
   - 如果一个简单的几何测量步骤（如计算裂缝最大宽度）用文字叙述和标准三维投影几何即可完全说清，不要生造一个占据半页的抽象测度空间定义 $\mathcal{M} = (\Omega, \mathcal{F}, \mu)$。
3. **公式推导链路闭合**：
   - 所有中间推导步骤必须逻辑自洽，严禁直接从一个高度抽象的未定义泛函跳跃到离散实现代码。

---

## 铁律三：章节标题、图题与摘要尽量让土木和工程审稿人一眼看懂 (Civil & Engineering Reviewer-Friendly Navigation)

### 1. 核心红线 (Red Lines)
- 审稿人时间极其宝贵，且绝大多数是土木、结构、防灾、建材领域的专家。
- **标题、摘要、图题、表题、章节名必须做到“零理解门槛”**：审稿人扫一眼目录和插图，就能完全搞懂本文的研究对象、核心方法、物理机理和工程结论。

### 2. 各模块落地规范

#### A. 论文主标题 (Title)
- **公式**：`[工程研究对象/痛点] + [核心直观方法] + [达到的物理/工程目标]`
- ❌ **错误范式**：*A Synergistic Multi-Modal Cognitive Manifold Network with Conflict-Aware Gradient Diagnosis for Concrete Defect Metrology*
- ✅ **正确范式**：*Vision-Based Concrete Defect Measurement Using Loss-Balanced Neural Networks with Physical Boundary Constraints*

#### B. 摘要 (Abstract)
- **四步直球叙事**：
  1. **工程痛点**：明确指出传统方法在具体工况下的物理/力学/工程局限；
  2. **核心方法（白话）**：一句话讲清方法本质（如“在训练前先诊断各损失分量对梯度的影响，并确定约束权重”）；
  3. **力学/机制增量**：交代该方法如何保证物理自洽性（如应力连续、裂缝闭合满足变形协调）；
  4. **量化工程结论**：给出明确的实测精度、提升百分比与计算耗时。

#### C. 章节标题 (Section Headings)
- 采用具象、直接的工程语言，杜绝计算机抽象堆叠。
- ❌ *Section 3.2: Conflict-Aware Gradient Stiffness Diagnostic Architecture*
- ✅ *Section 3.2: Evaluation of Loss Sensitivity and Determination of Fixed Weights*
- ❌ *Section 4.3: Empirical Verification on Spatiotemporal Manifold Invariance*
- ✅ *Section 4.3: Model Validation under Dynamic Loading and Variable Temperatures*

#### D. 插图与图题 (Figure Captions)
- **图题第一句话必须是结论性或直观描述**：
  - ❌ *Fig. 4. Schematic of the proposed multi-objective optimization paradigm.*
  - ✅ *Fig. 4. Flowchart of the loss weighting procedure: evaluating gradient influences prior to training to establish fixed bounds.*
- **坐标轴与图例**：必须带有明确的物理量名称与单位（如 $\text{Stress }\sigma\text{ (MPa)}$，严禁只写无量纲抽象代号 $y$ 或 $\hat{f}$）。

---

## 4. AI 协助写作与润色时的自动执行机制 (Auto-Execution Checklist)

当调用 CCC 系列技能进行论文生成、修改、润色或审稿时，AI 将自动执行以下自检：

- [ ] **术语清洗**：全文检索是否有硬造的生僻复合 AI 词汇？若有，主线降解为大白话，细节移入小括号。
- [ ] **主线精简**：核心方法是否能用一句话（如“训练前先判断...再在限定范围内...”）直接说清？
- [ ] **符号核查**：公式中每个符号是否有明确的力学/物理定义与单位？是否存在无意义的“假装高级”堆砌？
- [ ] **审稿人友好度**：土木/材料审稿人只看各级标题与图题能否顺畅理解全文 80% 的工作？
- [ ] **纯学术连续段落**：正文是否严格避免机械无序的“AI味列点（itemize/enumerate）”，保持流畅论述？

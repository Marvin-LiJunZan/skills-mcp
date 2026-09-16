---
name: integrated-research-reviewer
description: "Master unified academic research inspection & improvement suite. Triggers on phrases like '调用我们科研skills来检查一下', '科研skills审查', '用科研skills改一下'. Integrates: 1) End-to-End Autonomous Experimentation & Review (AI Scientist, ARIS, Karpathy Autoresearch), 2) Deep Literature Discovery & Anti-Hallucination Citation Verification (STORM, Cite-Verify, Reference-Checker), 3) Top-Tier Manuscript Architecture & De-AI Humanization (PaperSpine, Benchmark-Paper-Template, Nature-Skills, CCC-Author-Guide, Human-Writing), and 4) Publication-Grade Visual Diagnostics (Academic-Figure, Scipilot-Figure, Nature-Figure)."
metadata:
  short-description: "Unified master skill for end-to-end scientific research auditing, peer-review simulation, citation verification, manuscript de-AI, and figure diagnostics."
---

# Integrated Academic Research Reviewer & Improver (科研Skills联合审查总控)

本技能是整个自动化科研生态的**中央审查与改进调度总控**。
当用户说 **“调用我们科研skills来检查一下”**、**“用科研skills帮我过一遍”**、**“科研技能全面审查”** 或类似指令时，必须且自动执行本套全维度联合审查协议。

---

## 4大核心维度与审查标准

审查将按以下4个维度对论文/项目/代码进行全方位诊断并直接输出**可落地的改进改写方案**：

```text
                       [ 用户论文 / 项目代码 / 实验材料 ]
                                       │
        ┌──────────────────────────────┼──────────────────────────────┐
        ▼                              ▼                              ▼                              ▼
【维度 1: 实验闭环与论据】      【维度 2: 文献与防幻觉】       【维度 3: 顶刊骨架与去AI】      【维度 4: 出版级可视化】
 • AI Scientist 假设-代码闭环    • STORM 多视角多跳证据链       • PaperSpine 论证主脊梁         • Scipilot 数据偏误拦截
 • ARIS 跨模型对抗审视          • Cite-Verify DOI/跨库真伪    • Benchmark 5大支柱规范        • Nature/Elsevier 布局规范
 • Karpathy 5-min 极简指标      • 虚假引文/撤稿/错配清零       • Human-Writing 活人感去AI味    • 矢量级/误差棒/双Y轴拦截
```

---

### 维度 1：端到端自主科研与实验论据闭环 (Autonomous Experimentation & Evidence)
*底层驱动参考: `AI-Scientist`, `auto-research-in-sleep` (ARIS), `karpathy-autoresearch`*

1. **假设-实证单调性 (Hypothesis-to-Evidence Monotonicity)**：
   - 核心科学假设（Claim）是否真正被代码/实验结果支撑？是否存在“幻觉式声明”或推论过度？
2. **基线与公平对比 (Fair Baseline & Ablation)**：
   - 是否包含关键 Baseline 对比？消融实验（Ablation Studies）是否能够独立证明各模块贡献？
3. **极简与可复现性检查 (Simplicity & Reproducibility)**：
   - 按照 Karpathy 准则：排除为了论文复杂性而强行增加的无用超参或冗余代码；检查随机种子、依赖项和环境闭环。
4. **跨模型对抗审视 (Cross-Model Adversarial Audit)**：
   - 模拟恶毒审稿人（Reviewer #2）发起攻击：实验数据集是否存在泄漏？评估指标是否过于讨巧？

---

### 维度 2：多跳文献链与引文防幻觉检验 (Deep Literature & Citation Integrity)
*底层驱动参考: `stanford-storm`, `Deep-Research-skills`, `cite-verify`, `reference-checker`*

1. **真实性验证 (Ground-Truth DOI & API Verification)**：
   - 逐条提取 BibTeX / 文本引用，调用 CrossRef / arXiv / OpenAlex 进行真实性比对。
   - 严厉标记四类状态：`[VERIFIED]`, `[DOI_MISMATCH]`, `[HALLUCINATED]`, `[RETRACTED]`。
2. **多跳证据链与前沿定位 (Multi-hop Evidence & SOTA Positioning)**：
   - 论文是否漏掉了最近1-2年的关键SOTA文献？是否陷入“信息茧房”只引本学派文献？
3. **引文单调性与双射验证 (Bijective Monotonicity)**：
   - 正文引用的每一篇文献必须在参考文献表中严格存在，参考文献表中的每一篇文献必须在正文中有明确且有意义的引用（严禁充数挂名引用）。

---

### 维度 3：顶刊骨架解构与活人感去 AI 改造 (Manuscript Framing & De-AI Humanization)
*底层驱动参考: `PaperSpine`, `benchmark-paper-template`, `nature-skills`, `ccc-author-guide`, `human-writing`*

1. **PaperSpine 骨架贯穿 (The Spine Check)**：
   - Hook（问题痛点）-> Mechanism（机制创新）-> Empirical Validation（实证支撑）-> Boundary Conditions（适用边界）。
   - 每一段第一句话是否是清晰有力的论断句，而非含糊的背景铺垫。
2. **五支柱完整度 (Benchmark/Tech Paper Pillars)**：
   - 研究盲区（Research Gap）、构建管线（Pipeline）、评测框架（Evaluation Protocol）、核心实证洞见（Empirical Findings）、技术实现（Method）。
3. **彻底清除 AI 痕迹 (Human-Writing Protocol)**：
   - **高危词汇零容忍**：严禁出现 *“delve into”, "testament to", "pivotal role", "beacon", "tapestry", "in summary", "moreover"* 等套话。
   - **动态呼吸节奏**：破除 22-26 词机械均一长句。要求交替使用单刀直入的短句（8-10词定论）与严谨展开的长句（30+词阐述机理）。
   - **主动有力动词**：消除无意义被动语态（如 *"It was observed that..."* 改为 *"Increasing axial pressure accelerated..."*）。

---

### 维度 4：出版级科研可视化与数据图诊断 (Publication Figures & Diagnostics)
*底层驱动参考: `academic-figure-skill`, `scipilot-figure-skill`, `nature-figure`, `ccc-academic-figure-style`*

1. **经典画图错误拦截**：
   - 拦截小样本柱状图掩盖真实离散分布（必须改用箱线图/小提琴图或散点重叠）。
   - 拦截双 Y 轴误导趋势、彩虹色谱（Rainbow colormap，必须改用色盲友好色系如 Viridis/Set2）。
   - 拦截折线图用于离散分类变量。
2. **顶刊排版与视觉标准 (Nature / Elsevier / CCC Standards)**：
   - 单栏（85-90mm）/ 双栏（170-180mm）排版适配。
   - 字体层次严密（Arial / Helvetica / Times New Roman，轴标签 8-10 pt，刻度 6-8 pt）。
   - 必须提供可复现的 Python (Matplotlib/Seaborn) 或矢量图（SVG/PDF 600 DPI）改进脚本。

---

## 标准审查报告输出规范

当触发本审查时，必须输出结构化、严谨专业的【综合科研审查与改进报告】：

```markdown
# 🔬 综合科研技能全面审查与改进报告

## 📊 1. 总体综合评分与快速诊断
- 实验与论据闭环: [Score / 10]
- 文献与引文可信度: [Score / 10]
- 论文骨架与学术口吻 (去AI度): [Score / 10]
- 图表与数据可视化: [Score / 10]
- 综合审稿预判: [Strong Accept / Accept / Major Revision / Reject]

---

## ⚡ 2. 核心漏洞与红线拦截清单 (P0 级别问题)
- [列出致命缺陷，例如：存在疑似幻觉引文、关键消融实验缺失、柱状图误导、强烈的 ChatGPT 模板痕迹]

---

## 🛠️ 3. 四维深度诊断与具体改进方案

### 维度一：实验闭环与论证链 (AI Scientist / ARIS / Karpathy 视角)
- [诊断意见]
- [补充实验 / 论据加固建议]

### 维度二：引文与真实性验证 (Cite-Verify / STORM 视角)
- [引文检测结果表格：DOI / 状态 / 替换建议]

### 维度三：论文架构与去 AI 味润色 (PaperSpine / Human-Writing / Nature 视角)
- **原始段落 (Before)**:
  > ...
- **修改后段落 (After - 活人学术口吻)**:
  > ...
- **改动理由与节奏解析**:
  - 去除的套话词汇：...
  - 增强的事实密度与主动动词：...

### 维度四：数据图表与视觉重构 (Academic Figure / Scipilot 视角)
- [图表缺陷分析与改进建议]
- [配套可直接运行的 Python / Matplotlib 出版级画图修复代码]

---

## 🎯 4. 下一步行动清单 (Action Items)
1. ...
2. ...
```

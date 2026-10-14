---
name: quant-trading-skills
description: 'Comprehensive quantitative investment and algorithmic trading suite distilled from foundational works ("Factor Investing: Methods and Practice" by Ishikawa et al., "Quantitative Trading" by Ernest P. Chan, and "Quantitative Investment: Strategies and Technology" by Ding Peng). Use when developing, testing, auditing, or optimizing quant strategies, calculating factor IC/IR, running Fama-MacBeth HAC regressions, performing GRS tests, fixing look-ahead/p-hacking biases, building Barra risk models, trading cointegrated pairs via Kalman filter, sizing positions via Half-Kelly, or implementing VWAP execution algorithms.'
---

# Quant Trading Skills · 现代量化投资与算法交易专家系统

> 本技能库由三部量化经典典籍系统性蒸馏重构而成：
> 1. **石川、刘洋溢、连祥斌《因子投资：方法与实践》** —— 实证资产定价、因子方法论、多因子模型与严谨统计推断
> 2. **欧内斯特·陈 (Ernest P. Chan)《量化交易：如何建立自己的算法交易事业》** —— 算法交易架构、无偏回测验证、均值回归协整系统与凯利资金管理
> 3. **丁鹏《量化投资：策略与技术》** —— 量化策略全景、股指期货套利对冲与大单算法执行技术

---

## 🌟 核心心智模型 (Mental Models)

1. **统一资产定价视角**：超额收益来自于承担了不可分散的系统性风险（风险补偿），或捕捉了市场参与者的系统性非理性行为（行为异象）。没有经济学因果机制的纯统计规律必死。
2. **零偏差数据铁律**：回测系统必须具有绝对的时间单向因果性，彻底杜绝向前看偏差（严格对齐披露日而非报告期）、幸存者偏差（涵盖退市与 ST 标的）以及成交流动性幻想。
3. **统计防伪意识 (t > 3.0)**：在被数千名研究员反复挖掘的“因子动物园”中，传统经典统计学 $|t| > 2.0$ 彻底崩溃。任何新因子必须经受多重检验校正（FDR）与 $|t| > 3.0$ 的考验。
4. **半凯利黄金生存法则**：任何策略在实盘中都绝不能使用全凯利杠杆，必须强制使用半凯利（Half-Kelly: $0.5 f^*$），赋予系统足够的安全边际对抗参数估计误差与极端肥尾冲击。

---

## 🧭 模块导航与自动路由规范 (Router Index)

当用户提出具体的量化工程任务时，优先索引并调阅对应的专项模块：

| 模块章节 | 核心主题与解决的问题 | 匹配场景 / 触发关键词 |
| :--- | :--- | :--- |
| [**01-数据工程与预处理**](file:///c:/JunzanLi_project/skills_mcp/skills/quant-trading-skills/chapters/01-factor-foundations-and-data-processing.md) | MAD 去极值、截面标准化、OLS 行业与市值残差中性化、公告日时滞对齐。 | "去极值", "中性化", "MAD", "数据清洗", "对齐披露日", "财务数据预处理" |
| [**02-因子有效性检验**](file:///c:/JunzanLi_project/skills_mcp/skills/quant-trading-skills/chapters/02-factor-evaluation-methodology.md) | 投资组合分层排序法（单调性/多空收益）、Fama-MacBeth 截面两步回归、Newey-West HAC 调整、IC/Rank IC 与衰减半衰期。 | "分层回测", "多空单调性", "Fama-MacBeth", "Newey-West", "Rank IC", "IR" |
| [**03-主流风格因子库**](file:///c:/JunzanLi_project/skills_mcp/skills/quant-trading-skills/chapters/03-core-style-factors-and-anomalies.md) | 规模 (Size/SMB)、价值 (Value/HML)、动量反转、盈利能力 (ROE/ROA)、资产投资扩张惩罚、特质波动率 (IVOL) 异象。 | "风格因子", "小市值溢价", "价值陷阱", "特质波动", "IVOL", "A股异象" |
| [**04-多因子定价与GRS**](file:///c:/JunzanLi_project/skills_mcp/skills/quant-trading-skills/chapters/04-multifactor-pricing-models-and-grs.md) | CAPM、Fama-French 3/5 因子、Carhart 4 因子、q-Factor 模型以及 GRS 联合定价误差假设检验数学推导与 Python 实现。 | "GRS检验", "FF5", "多因子模型", "定价误差联合检验", "Carhart" |
| [**05-多重测试与防伪**](file:///c:/JunzanLi_project/skills_mcp/skills/quant-trading-skills/chapters/05-data-mining-multiple-testing-p-hacking.md) | 因子动物园危机、Harvey-Liu-Zhu $t > 3.0$ 新标准、Benjamini-Hochberg 错误发现率 (FDR) 控制、样本外隔离军规。 | "p-hacking", "数据挖掘", "多重假设检验", "FDR", "Harvey", "防止过拟合" |
| [**06-组合优化与Barra**](file:///c:/JunzanLi_project/skills_mcp/skills/quant-trading-skills/chapters/06-portfolio-optimization-and-barra-risk.md) | Barra 结构化风险模型协方差降维分解、CVXPY 二次规划组合优化 (QP)、行业/风格硬约束、Almgren-Chriss 市场冲击模型。 | "组合优化", "二次规划", "Barra", "协方差矩阵", "跟踪误差", "冲击成本" |
| [**07-算法交易系统架构**](file:///c:/JunzanLi_project/skills_mcp/skills/quant-trading-skills/chapters/07-algo-trading-system-architecture.md) | 欧内斯特·陈量化事业四大支柱、真实性检验标准、无偏回测系统四大陷阱、夏普与卡玛比率考核准入。 | "算法交易系统", "回测引擎", "幸存者偏差", "向前看偏差", "夏普比率" |
| [**08-均值回归与协整**](file:///c:/JunzanLi_project/skills_mcp/skills/quant-trading-skills/chapters/08-mean-reversion-cointegration-kalman.md) | ADF 平稳性检验、Engle-Granger 协整检验、Ornstein-Uhlenbeck 过程半衰期、卡尔曼滤波动态对冲比率与灾难止损。 | "配对交易", "协整", "ADF检验", "半衰期", "卡尔曼滤波", "均值回归" |
| [**09-资金管理与凯利公式**](file:///c:/JunzanLi_project/skills_mcp/skills/quant-trading-skills/chapters/09-capital-management-kelly-and-drawdown.md) | 离散与连续凯利公式推导、全凯利自杀陷阱、半凯利 (Half-Kelly) 铁律、动态回撤阶梯截断控制器、CVaR 肥尾风控。 | "资金管理", "凯利公式", "半凯利", "仓位管理", "最大回撤控制", "CVaR" |
| [**10-对冲套利与算法执行**](file:///c:/JunzanLi_project/skills_mcp/skills/quant-trading-skills/chapters/10-hedging-arbitrage-and-execution-algorithms.md) | 股指期货 Alpha 对冲与负基差贴水滚仓成本、期现套利无套利区间模型、TWAP / VWAP / POV / IS 算法执行技术。 | "股指期货对冲", "基差贴水", "期现套利", "VWAP", "TWAP", "大单拆单" |

---

## 📚 快速参考资料 (Reference Files)

* 📖 [**量化全景中英文术语表 (Glossary)**](file:///c:/JunzanLi_project/skills_mcp/skills/quant-trading-skills/reference/glossary.md)：涵盖 FMB、GRS、Barra、Half-life、Kelly 等核心概念的标准中英对照与严谨数学定义。
* ⚠️ [**致命反模式清单 (Anti-Patterns)**](file:///c:/JunzanLi_project/skills_mcp/skills/quant-trading-skills/reference/anti-patterns.md)：详述向前看偏差、全凯利自杀、微盘流动性幻觉、死扛破裂均值回归等经典惨痛教训。
* ⚡ [**核心决策树与公式速查 (Cheatsheet)**](file:///c:/JunzanLi_project/skills_mcp/skills/quant-trading-skills/reference/cheatsheet.md)：一站式速查因子筛选决策流、均值回归检验流与全套核心数学计算公式。

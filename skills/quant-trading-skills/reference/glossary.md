# 量化交易全景专业术语表 (Glossary)

| 术语 (中文) | 英文对照 | 数学定义 / 核心概念 | 对应模块 |
| :--- | :--- | :--- | :--- |
| **因子载荷 / 暴露** | Factor Loading / Exposure ($\beta$) | 资产收益率对特定系统性风险因子变动的敏感程度 $\beta_i = \frac{\text{Cov}(R_i, F)}{\text{Var}(F)}$。 | 01, 04 |
| **因子风险溢价** | Factor Risk Premium ($\lambda$) | 单位因子风险暴露在截面上所获得的预期超额补偿。 | 01, 02 |
| **绝对中位数差** | MAD (Median Absolute Deviation) | 稳健统计学去极值指标：$\text{Median}(\|X - \text{Median}(X)\|)$，正态下 $1.4826 \times \text{MAD} \approx \sigma$。 | 01 |
| **中性化** | Neutralization | 采用 OLS 残差法剥离因子对行业哑变量和对数市值的共线性暴露。 | 01, 06 |
| **投资组合排序法** | Portfolio Sorting | 将截面股票按因子打分单调分组（如5分位），检验多空对冲收益与单调性。 | 02 |
| **Fama-MacBeth 回归** | FMB Two-Stage Regression | 第一阶段时序回归估计 $\beta$，第二阶段逐期截面回归估计溢价 $\lambda_t$。 | 02 |
| **HAC 稳健标准误** | Newey-West Standard Error | 消除金融时序自相关（Autocorrelation）与异方差（Heteroscedasticity）对 t 检验统计量的虚假放大。 | 02 |
| **信息系数** | IC / Rank IC | 因子打分与次期实际收益的截面相关系数（Rank IC 采用 Spearman 秩相关）。 | 02 |
| **信息比率 (因子)** | Information Ratio (IR) | $\text{IR} = \frac{\text{Mean}(\text{Rank IC})}{\text{Std}(\text{Rank IC})}$，衡量因子预测能力的稳定性。 | 02 |
| **特质波动率异象** | IVOL (Idiosyncratic Volatility) | 多因子回归残差的标准差。实证中高特质波动股票未来收益显著为负（彩票偏好驱动）。 | 03 |
| **GRS 检验** | Gibbons, Ross, Shanken (1989) | 联合检验多因子资产定价模型对 $N$ 个测试资产的定价误差 $\alpha$ 是否联合为零的 F 统计量。 | 04 |
| **数据挖掘 / p-hacking** | Data Snooping / p-hacking | 通过反复微调回测区间、参数、分组方式人为制造出的“虚假显著性”。 | 05 |
| **错误发现率** | FDR (False Discovery Rate) | 在所有被拒绝的原假设（宣称有效发现）中，假阳性因子所占的期望比例（BH/BHY 算法）。 | 05 |
| **Barra 结构化模型** | Barra Risk Model | 将资产协方差矩阵降维分解为因子协方差与特质风险：$\Sigma = X F X^T + \Delta$。 | 06 |
| **跟踪误差** | Tracking Error (TE) | 投资组合主动收益相对于基准指数收益的标准差：$\text{TE} = \sqrt{\text{Var}(R_p - R_b)}$。 | 06 |
| **市场冲击** | Market Impact | 大资金订单吃掉盘口流动性引发的临时与永久价格逆向滑点（平方根定律）。 | 06, 10 |
| **向前看偏差** | Look-ahead Bias | 在历史回测的决策点使用了未来才会披露或确定的信息（如未公告财报、收盘价瞬间成交）。 | 07 |
| **幸存者偏差** | Survivorship Bias | 回测股票池剔除了历史已退市、破产或 ST 标的，导致回测年化收益严重虚高。 | 07 |
| **平稳性 (单位根)** | Stationarity / Unit Root ($I(0)$ vs $I(1)$) | 均值、方差不随时间改变的时序性质；ADF 检验用于排查单位根。 | 08 |
| **协整** | Cointegration | 两个具有单边趋势的非平稳序列通过线性组合 $\beta$ 形成平稳残差序列 $I(0)$。 | 08 |
| **半衰期** | Half-life | Ornstein-Uhlenbeck 过程中，偏离的价差中枢恢复到一半所需的时间：$-\frac{\ln 2}{\lambda}$。 | 08 |
| **卡尔曼滤波** | Kalman Filter | 递归贝叶斯在线状态估计器，用于实时自适应跟踪动态时变对冲比率 $\beta_t$。 | 08 |
| **凯利公式** | Kelly Criterion | 连续交易下最大化长期几何复合收益率的最优杠杆比例：$f^* = \frac{\mu - r}{\sigma^2}$。 | 09 |
| **半凯利** | Half-Kelly ($0.5 f^*$) | 工业界强制风控标准，保留 75% 复合收益，降低 50% 回撤，赋予足够的安全边际。 | 09 |
| **条件在险价值** | CVaR / Expected Shortfall | 当损失突破 VaR 门槛时，极端尾部损失的条件数学期望，有效衡量肥尾崩盘风险。 | 09 |
| **基差与贴水** | Basis / Discount | 基差 = 现货指数 - 期货价格；现货高于期货为贴水，导致做空套保产生负滚仓成本。 | 10 |
| **无套利区间** | No-Arbitrage Band | 考虑借贷息差、滑点和冲击成本后，期货实际价格无法触发无风险套利的理论安全带。 | 10 |
| **VWAP** | Volume-Weighted Average Price | 成交量加权平均价执行算法，按日内分时成交量 U 型分布动态拆单，降低冲击成本。 | 10 |
| **TWAP** | Time-Weighted Average Price | 时间加权平均价执行算法，在固定时间窗口内均匀切片申报大单。 | 10 |

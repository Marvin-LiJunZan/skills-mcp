# 02 - 因子有效性评价方法论与统计检验

> 本模块系统阐述学术界与工业界检验因子有效性的两大支柱方法：**投资组合排序法 (Portfolio Sorting)** 与 **Fama-MacBeth 截面回归法 (FMB)**，并包含 IC/Rank IC 衰减分析与 Newey-West 自相关调整。

---

## 1. 投资组合排序法 (Portfolio Sorting)

投资组合排序法是检验因子能否产生截面单调超额收益的最直观、非参数的方法，完全不依赖线性模型的函数形式假设。

### 1.1 单变量分组回测 (Single Sorting)
在每个调仓截面日 $t$：
1. **排序与分箱**：根据当期因子值从大到小（或从小到大）将全部候选股票均匀分成 $N$ 组（通常 $N=5$ 或 $N=10$）。第一组为 $G_1$（Top），最后一组为 $G_N$（Bottom）。
2. **权重构建**：组内可以采用**市值加权 (Value-Weighted, VW)** 或 **等权重 (Equal-Weighted, EW)**。
   > **实务铁律**：A 股市场必须优先观察市值加权（或剔除微盘股后的等权）。纯等权往往会被尾部流动性极差的壳股严重污染，导致回测虚高。
3. **多空组合 (Long-Short Hedge)**：构建对冲组合 $L/S = G_1 - G_N$，计算多空净收益率、夏普比率（Sharpe Ratio）、最大回撤（Max Drawdown）和胜率。
4. **单调性检验**：理想的有效因子，其各组年化收益率 $R(G_1) \sim R(G_N)$ 应当呈现严格的单调递增或递减阶梯。若中间组别混乱，因子往往欠缺稳健性。

---

### 1.2 双重排序法 (Double Sorting)：剥离共线性

当两个因子存在高度相关性（例如账面市值比 BM 与流通市值 Size 负相关）时，单变量排序无法证明新因子的超额收益不是由已知风格因子驱动的。此时必须使用双重排序法。

#### 两种双重排序机制对比
| 排序机制 | 执行流程 | 适用场景 |
| :--- | :--- | :--- |
| **独立双重排序 (Independent)** | 独立按因子 A 分成 3 组，同时独立按因子 B 分成 3 组，交叉形成 $3 \times 3 = 9$ 个组合。 | 因子 A 与 B 相关性较弱，保证交叉单元格内股票分布均匀。 |
| **依序/条件双重排序 (Sequential)** | 先按控制变量（如 Size）将股票分成 5 组；在每一个组内部，再按目标因子（如 Alpha 因子）细分成 5 组。 | 因子 A 与 B 存在强相关性（如非线性规模倾斜），确保控制变量被严格锁定。 |

在每个控制组内部计算目标因子多空对冲收益，最后在 5 个控制组上求平均多空收益。如果平均多空收益仍然显著大于 0（t 统计量 > 2.0），则证明目标因子具备**超越控制变量的净增量信息 (Marginal Contribution)**。

---

## 2. Fama-MacBeth 截面两阶段回归法 (FMB)

Fama-MacBeth (1973) 架构是实证资产定价的核心骨干，用于估计因子的风险溢价 $\lambda$ 并对其统计显著性进行严谨推断。

### 2.1 算法流程
1. **第一阶段：时间序列回归（估计各资产的因子暴露 $\beta$）**
   对每个资产 $i=1,\dots,N$，在滑动时间窗口内（例如 36 个月或 60 周）对因子收益进行多元时序回归：
   $$R_{i,t} - R_{f,t} = \alpha_i + \beta_{i,1} f_{1,t} + \cdots + \beta_{i,K} f_{K,t} + \epsilon_{i,t}$$
   得到各资产的估计载荷 $\hat{\beta}_{i,k}$。

2. **第二阶段：截面回归（逐期估计因子溢价 $\lambda_t$）**
   在每个时间点 $t=1,\dots,T$，以所有资产当期的超额收益为因变量，以第一阶段估计出的 $\hat{\beta}_i$ 为自变量，做截面 OLS 回归：
   $$R_{i,t} - R_{f,t} = \alpha_t + \lambda_{1,t} \hat{\beta}_{i,1} + \cdots + \lambda_{K,t} \hat{\beta}_{i,K} + e_{i,t}$$
   从而得到一系列时间序列因子溢价估计值 $\{\hat{\lambda}_{k,t}\}_{t=1}^T$。

3. **统计推断与溢价检验**
   计算因子溢价的时序均值：
   $$\bar{\lambda}_k = \frac{1}{T} \sum_{t=1}^T \hat{\lambda}_{k,t}$$
   并检验原假设 $H_0: \lambda_k = 0$。

---

### 2.2 Newey-West 异方差与自相关稳健标准误 (HAC)

金融资产收益率存在时间序列自相关和截面异方差，传统的 OLS 标准误会低估方差，导致虚假的统计显著性。必须采用 **Newey-West 调整**：

$$\sigma^2_{NW}(\bar{\lambda}) = \frac{1}{T} \left( \hat{\Gamma}_0 + 2 \sum_{l=1}^{L} \left(1 - \frac{l}{L+1}\right) \hat{\Gamma}_l \right)$$
其中 $\hat{\Gamma}_l = \frac{1}{T} \sum_{t=l+1}^T (\hat{\lambda}_t - \bar{\lambda})(\hat{\lambda}_{t-l} - \bar{\lambda})$，滞后阶数通常取 $L = \text{round}(4 \cdot (T/100)^{2/9})$。

```python
import numpy as np
import statsmodels.api as sm

def newey_west_t_stat(series: pd.Series, lags: int = None) -> tuple:
    """计算时序均值的 Newey-West 稳健 t 统计量"""
    clean_s = series.dropna()
    T = len(clean_s)
    if lags is None:
        lags = int(4 * (T / 100)**(2/9))
    
    # 对常数项回归以提取 HAC 协方差
    y = clean_s.values
    X = np.ones((T, 1))
    model = sm.OLS(y, X).fit(cov_type='HAC', cov_kwds={'maxlags': lags})
    
    mean_val = model.params[0]
    t_stat = model.tvalues[0]
    p_val = model.pvalues[0]
    return mean_val, t_stat, p_val
```

---

## 3. IC (Information Coefficient) 与 Rank IC 全维度评价

### 3.1 定义与度量
在每个调仓日 $t$，因子暴露值向量 $F_t$ 与下一期实际收益率向量 $R_{t+1}$ 之间的相关系数：
* **Normal IC (Pearson)**：
  $$\text{IC}_t = \text{Corr}(F_t, R_{t+1})$$
* **Rank IC (Spearman 秩相关)**：
  $$\text{Rank IC}_t = \text{Corr}(\text{Rank}(F_t), \text{Rank}(R_{t+1}))$$
  > **实战推荐**：Rank IC 对极值不敏感，且与组合排序选股能力直接挂钩，是工业界首选评估指标。

### 3.2 因子评价四大金标准
1. **IC 均值**：A 股月频有效因子通常要求 $|\text{Mean}(\text{Rank IC})| > 0.03$，优秀因子可达 $0.05 \sim 0.08$。
2. **IC 标准差**：衡量因子选股稳定度。
3. **信息比率 (IR)**：
   $$\text{IR} = \frac{\text{Mean}(\text{Rank IC})}{\text{Std}(\text{Rank IC})}$$
   - $\text{IR} > 0.5$：可用；
   - $\text{IR} > 0.8$：优秀；
   - $\text{IR} > 1.0$：极高 Alpha 质量（需严防过拟合）。
4. **IC 胜率 (IC Win Rate)**：$\text{Rank IC} > 0$ 的月份占比，通常要求 $> 60\%$。

### 3.3 IC 衰减与换手率平衡 (Decay & Turnover)
计算因子与未来 $T+1, T+2, \dots, T+N$ 期收益的相关性，绘制 **IC 衰减曲线**：
* 若第 1 天 IC 极高（0.12），但第 3 天衰减到 0.01：属于**高频量价因子**，需要日频或更高频调仓，换手率极高；
* 若 IC 在 20~60 天维持平缓（0.04 缓慢降至 0.02）：属于**低频基本面因子**，支持月度调仓，换手率和冲击成本极低。

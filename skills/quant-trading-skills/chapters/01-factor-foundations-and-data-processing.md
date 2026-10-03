# 01 - 因子投资基础与数据工程规范

> 本模块基于石川、刘洋溢、连祥斌《因子投资：方法与实践》第1章及经典实证资产定价工程标准，阐述因子投资的统一视角、数学底层与专业级数据预处理流水线。

---

## 1. 统一视角下的因子投资

### 1.1 从单因子到多因子定价模型
实证资产定价的核心目标是解释不同资产截面上的预期超额收益差异。

* **资本资产定价模型 (CAPM)**：
  $$E[R_i] - R_f = \beta_i (E[R_M] - R_f)$$
  其中 $\beta_i = \frac{\text{Cov}(R_i, R_M)}{\text{Var}(R_M)}$。CAPM 认为市场因子是驱动资产收益的唯一系统性风险。

* **套利定价理论 (APT) 与线性多因子模型**：
  $$E[R_i] = \beta_{i,1}\lambda_1 + \beta_{i,2}\lambda_2 + \cdots + \beta_{i,K}\lambda_K$$
  - $\beta_{i,k}$：资产 $i$ 对第 $k$ 个因子的暴露（Factor Exposure）或因子载荷（Factor Loading）。
  - $\lambda_k$：第 $k$ 个因子的预期溢价（Factor Risk Premium）。
  - 约定：在实证资产定价中，收益率均默认指代扣除无风险利率后的预期超额收益。

### 1.2 因子投资的三大视角
1. **学术界视角**：探索市场是否存在未被定价的异象，检验市场有效性，寻找可替代 CAPM 的更低定价误差模型（如 Fama-French 5 因子）。
2. **资产管理人视角**：剥离市场 Beta 暴露，通过主动因子配置（如倾斜价值、小市值、动量）获取长期持续的超额 Alpha。
3. **资产所有者视角 (Smart Beta)**：以透明、规则化、低费率的被动或半指数化方式获取特定系统性风险溢价。

---

## 2. 因子数据清洗与预处理三部曲

在因子进入任何截面回归或组合构建之前，必须经过严格的数据预处理三部曲：**去极值 -> 标准化 -> 中性化**。任何省略或顺序颠倒都会引入严重的偏差。

```
原始财报/行情数据
       │
       ▼
 [ 1. 去极值 ]  ──> 消除异动噪点 (MAD / 3-sigma / 分位数 Winsorization)
       │
       ▼
 [ 2. 标准化 ]  ──> 消除量纲影响 (Z-Score / 排序标准化)
       │
       ▼
 [ 3. 中性化 ]  ──> 剥离非目标暴露 (OLS 残差法: 剔除行业与市值干扰)
       │
       ▼
纯净风格因子 (进入回测与建模)
```

### 2.1 步骤一：去极值 (Outlier Handling)

金融市场数据存在严重的“厚尾”现象，传统均值和标准差极易受到个别异常值拉扯。优先使用稳健统计量 **MAD (Median Absolute Deviation)**。

#### 核心算法：MAD 绝对中位数差法
1. 计算因子序列的中位数 $M = \text{Median}(X)$；
2. 计算每个样本与中位数的绝对偏差的中位数：
   $$\text{MAD} = \text{Median}(|X_i - M|)$$
3. 设定上下截断门槛（通常取 3 倍或 5 倍 MAD，对于正态分布， $1.4826 \times \text{MAD} \approx \sigma$）：
   $$\text{Upper} = M + 3 \times 1.4826 \times \text{MAD}$$
   $$\text{Lower} = M - 3 \times 1.4826 \times \text{MAD}$$
4. **软处理 (Winsorization)**：超过门槛的值直接赋值为对应门槛值（不要直接删除样本，以防幸存者偏差）。

```python
import numpy as np
import pandas as pd

def winsorize_mad(series: pd.Series, n_dev: float = 3.0) -> pd.Series:
    """基于绝对中位数法(MAD)对截面因子进行去极值缩尾处理"""
    median = series.median()
    mad = (series - median).abs().median()
    if mad == 0:
        return series
    # 1.4826 修正系数使 MAD 在正态分布下等于标准差
    norm_mad = 1.4826 * mad
    upper = median + n_dev * norm_mad
    lower = median - n_dev * norm_mad
    return series.clip(lower=lower, upper=upper)
```

---

### 2.2 步骤二：标准化 (Standardization)

为了消除不同指标的量纲单位，并使得不同截面期的因子值具备横向与纵向的可比性：

$$Z_i = \frac{X_i - \mu_X}{\sigma_X}$$

若因子分布偏度极大，亦可先做秩变换（Rank 分位数标准化）：
$$P_i = \frac{\text{Rank}(X_i) - 1}{N - 1} \in [0, 1] \implies Z_i = \Phi^{-1}(P_i)$$

```python
def standardize_zscore(series: pd.Series) -> pd.Series:
    """截面 Z-Score 标准化"""
    std = series.std(ddof=1)
    if std == 0:
        return series - series.mean()
    return (series - series.mean()) / std
```

---

### 2.3 步骤三：中性化 (Neutralization)

许多原始因子天然附带明显的行业属性或市值规模偏好（例如，低 PE 股票天然集中在银行、钢铁等周期行业）。为了考察因子本身的真实选股能力，必须剥离行业和市值的共线性暴露。

#### 数学模型：OLS 截面残差提取法
在每个调仓日 $t$ 的股票截面上，建立多元线性回归：
$$X_{i,t} = \sum_{j=1}^{M} \beta_{ind, j} \cdot D_{i,j} + \beta_{size} \cdot \ln(\text{MarketCap}_{i,t}) + \epsilon_{i,t}$$
- $D_{i,j}$：第 $j$ 个行业的 Dummy 哑变量（属于该行业为 1，否则为 0）；
- $\ln(\text{MarketCap}_{i,t})$：对数流通市值；
- **残差 $\epsilon_{i,t}$ 即为行业与市值中性化后的纯净因子值**。

```python
import statsmodels.api as sm

def neutralize_factor(factor_series: pd.Series, 
                      industry_dummies: pd.DataFrame, 
                      log_market_cap: pd.Series) -> pd.Series:
    """
    行业与市值中性化：利用 OLS 回归残差提取纯净因子
    """
    # 拼接自变量矩阵 (行业哑变量 + 对数市值)
    X = pd.concat([industry_dummies, log_market_cap.rename('ln_mcap')], axis=1)
    # 剔除空值股票
    valid_idx = factor_series.dropna().index.intersection(X.dropna().index)
    
    y = factor_series.loc[valid_idx]
    X_mat = X.loc[valid_idx]
    
    # 求解 OLS 回归
    model = sm.OLS(y, X_mat).fit()
    # 提取回归残差作为中性化因子
    residual = model.resid
    return residual.reindex(factor_series.index)
```

---

## 3. 实盘数据工程的四大“致命暗坑”与避坑军规

1. **财务数据发布时滞与向前看偏差 (Look-ahead Bias)**：
   - 年报披露截止日期为次年 4 月 30 日，中报为 8 月 31 日，一季报为 4 月 30 日，三季报为 10 月 31 日。
   - **铁律**：在历史截面计算因子时，必须使用**实际公告披露日期（Announce Date）**，绝不能使用财报报告期（Report Period）！如果在 1 月 1 日使用了上一年度的年报数据，属于典型的向前看作弊。
2. **幸存者偏差 (Survivorship Bias)**：
   - 股票池必须覆盖历史所有交易过的标的（包括退市股、暂停上市股、ST/*ST 股）。若仅使用当前存续的上市股票回溯历史，会虚增策略年化收益 3%~8% 以上。
3. **除权除息与前复权陷阱**：
   - 回测计算历史收益率时可以使用后复权或动态复权净值；严禁使用“历史截止日当前一次性前复权数据”回测，这会导致历史股价随未来的分红送股发生变动，产生未来的价格信息泄漏。
4. **流动性与可交易性过滤 (Tradability Filter)**：
   - 剔除上市未满 60 个交易日的次新股（波动极度失真）；
   - 剔除截面停牌股票；
   - 剔除涨停不可买入、跌停不可卖出的不可成交股票。

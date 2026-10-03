# 10 - 对冲套利、股指期货基差与算法执行技术

> 本模块系统拆解丁鹏《量化投资：策略与技术》中的高级实操课题：**Alpha 现货与期货对冲**、**股指期货升贴水与无套利区间模型**，以及减少大单市场冲击的四大核心**算法执行技术 (TWAP / VWAP / POV / IS)**。

---

## 1. Alpha 组合与股指期货对冲工程

在市场单边大跌时，纯股票多头策略即使跑赢基准 15%，整体账户依然可能面临 10%~20% 的名义亏损。为了获得与市场大势脱钩的“绝对收益”，必须运用金融衍生品（股指期货 IF/IC/IM 或场外期权）进行 Beta 完全对冲。

### 1.1 对冲模型与组合总收益分解
* 设现货股票多头组合价值为 $V_S$，预期收益率为 $R_S$：
  $$R_S = \alpha + \beta R_M + \epsilon$$
* 卖空股指期货合约市值 $V_F$ 对冲系统性风险：
  $$V_F = \beta \cdot V_S$$
* 对冲组合总收益 $R_{\text{total}}$：
  $$R_{\text{total}} = R_S - \beta R_M = \alpha + \epsilon$$
  从而成功滤除全市场的系统性涨跌 $\beta R_M$，仅保留精选因子的纯 Alpha 收益。

### 1.2 A 股特有的“贴水对冲成本”与年化滚仓损耗
在海外成熟市场，期货往往呈现轻微升水（反映资金借贷无风险利率）；而在中国 A 股市场，由于缺乏融券做空券源，大量量化对冲基金（中性策略）集中涌入股指期货（尤其是中证500 IC、中证1000 IM）做空，导致**期货长期处于深度贴水（Discount）状态**。

* **基差定义**：$\text{Basis}_t = S_t - F_t$（现货指数 - 期货价格）。当 $S_t > F_t$ 时为贴水。
* **滚仓对冲成本 (Hedging Drag)**：到期日时期货价格必然与现货指数强制收敛。做空期货者必须在低价平仓即将到期的近月合约，转去开仓更低价格的远月合约，造成确定性的“负展期损耗”：
  $$\text{Cost}_{\text{annual}} = \frac{S_t - F_t}{S_t} \cdot \frac{365}{\text{Days to Expiry}}$$
* **实战应对铁律**：如果基差年化贴水高达 $12\%$，则现货股票多头必须产生 $>15\%$ 以上的纯 Alpha 才能跑出正收益。当贴水极端放大时，需评估改用场外雪球/期权合成对冲或调整对冲头寸比例。

---

## 2. 股指期货期现套利与无套利区间模型

期货价格是由持有成本模型（Cost of Carry）决定的理论均衡值：
$$F^*(t, T) = S_t \cdot e^{(r - d)(T - t)}$$
其中 $r$ 为资金借贷利率，$d$ 为现货指数成分股的连续年化分红率。

### 2.1 无套利区间 (No-Arbitrage Band)
在真实交易中，由于存在借贷息差、买卖滑点、交易佣金和冲击成本，期货实际价格并不严格等于 $F^*$，而是在一个**无套利区间**内波动：

```
期货价格 F(t)
     ▲
     │  ─────── 无套利区间上界 F_upper ── 正向套利区 (卖期货, 买现货ETF/成分股)
     │  ................................
     │       无套利理论均衡价 F*(t)       无套利安全区 (任何套利交易均亏损)
     │  ................................
     │  ─────── 无套利区间下界 F_lower ── 反向套利区 (买期货, 融券卖空现货)
     └──────────────────────────────────────────────────────────► 时间 t
```

* **无套利上界**：$F_{\text{upper}} = S_t \cdot [1 + (r_{\text{borrow}} - d)(T-t)] + 2 \times \text{TransactionCost}$；
* **无套利下界**：$F_{\text{lower}} = S_t \cdot [1 + (r_{\text{lend}} - d)(T-t)] - 2 \times \text{TransactionCost}$；
* **套利触发逻辑**：一旦市场非理性恐慌或狂热导致实际价格突破上界（或下界），程序化套利系统立即自动开仓锁定无风险价差；随着到期日基差强制收敛归零，平仓赚取绝对超额收益。

---

## 3. 生产级算法执行技术 (Execution Algorithms)

当机构资金一次性调仓几千万甚至几亿元时，直接向撮合系统挂市价单会瞬间将盘口买穿，产生 $2\% \sim 5\%$ 的严重永久滑点。算法执行（Execution Algo）的核心使命是：**在限定时间内，以最低的冲击成本和最低的时延风险完成目标头寸的清算**。

### 3.1 经典执行算法对比矩阵
| 算法类型 | 核心执行逻辑 | 适用场景 | 优缺点 |
| :--- | :--- | :--- | :--- |
| **TWAP (时间加权)** | 将目标交易量在指定时间段内（如 2 小时）均等切碎成若干小单匀速申报。 | 流动性平稳、成交量日内分布极其均匀的大盘股。 | 算法极简单；缺点是在市场成交清淡时容易暴露痕迹，被高频机构嗅探。 |
| **VWAP (成交量加权)** | 按照历史日内成交量的“U 型分布”概率权重动态分配各时间分片的下单数量。 | 日频主力调仓，以当天的全市场成交均价作为考核基准。 | 工业界最普及；能顺应流动性高峰（早盘/尾盘放量，中午缩量）。 |
| **POV (比例参与)** | 实时监控当前盘口每一笔成交量，按固定比例（如 $5\% \sim 10\%$）紧随市场跟单。 | 突发异动股票或行情剧烈放量的流动性追随。 | 隐蔽性极强，完全不干扰正常市场走势；缺点是若全天缩量，可能无法在收盘前完成预定头寸。 |
| **IS (实施差额)** | Almgren-Chriss 最优动态轨迹，平衡“延时持仓风险”与“快速交易冲击”。 | 高 Alpha 衰减因子（要求快速建仓锁定 Alpha，同时压制冲击）。 | 数学最优解；需要精确估计瞬时冲击与价格方差参数。 |

---

### 3.2 生产级 VWAP 分时调度算法 Python 实现

```python
import numpy as np
import pandas as pd

def generate_vwap_schedule(total_shares_to_buy: int,
                           historical_volume_profile: np.ndarray,
                           intervals: int = 48) -> np.ndarray:
    """
    根据历史日内成交量分布 profile (U型曲线) 生成精准的 VWAP 分时报单计划
    
    参数:
    ----------
    total_shares_to_buy : int 目标总购买股数
    historical_volume_profile : np.ndarray, 长度为 intervals 的历史成交量占比
    intervals : int 日内时间切片数 (如 A 股 4 小时 = 240 分钟，每 5 分钟一片即 48 片)
    
    返回:
    ----------
    np.ndarray : 每个时间切片所应执行的目标股数 (整手对齐)
    """
    assert len(historical_volume_profile) == intervals
    # 归一化权重曲线 (早尾盘权重高，盘中清淡)
    normalized_weights = historical_volume_profile / np.sum(historical_volume_profile)
    
    # 计算理论各分片分配量
    raw_shares = total_shares_to_buy * normalized_weights
    
    # 按照 100 股 (1 手) 进行整手向下取整
    scheduled_shares = np.floor(raw_shares / 100.0) * 100.0
    
    # 处理因整手截断导致的尾数差额
    residual_shares = total_shares_to_buy - np.sum(scheduled_shares)
    
    if residual_shares > 0:
        # 将剩余散单优先分配到全天成交量最大的高峰切片中
        top_volume_indices = np.argsort(normalized_weights)[::-1]
        for idx in top_volume_indices:
            if residual_shares <= 0:
                break
            add_amount = min(residual_shares, 100.0)
            scheduled_shares[idx] += add_amount
            residual_shares -= add_amount
            
    return scheduled_shares.astype(int)
```

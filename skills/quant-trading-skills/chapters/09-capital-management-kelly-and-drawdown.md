# 09 - 资金管理、凯利公式与动态回撤控制

> 本模块系统阐述量化长青的生命线：**资金与杠杆管理 (Money Management)**。推导经典凯利公式（Kelly Criterion）、解析“全凯利自杀陷阱”、确立半凯利（Half-Kelly）实战铁律，并给出动态回撤截断与 CVaR 极端风险管理模型。

---

## 1. 为什么资金管理决定量化团队的生死？

90% 的量化爆仓并不是因为选股因子失效或买卖信号错误，而是死于**过度杠杆与错误的头寸管理**。
* **不对称亏损陷阱**：亏损 10% 需要上涨 11% 回本；亏损 50% 需要上涨 100% 回本；亏损 90% 则需要上涨 900% 才能回本。
* **破产概率 (Risk of Ruin)**：即使一个策略长期预期收益为正，如果不恰当地放大了杠杆，在有限资本条件下遭遇一次极端肥尾连续回撤，就会在黎明到来前彻底出局。

---

## 2. 凯利公式 (Kelly Criterion) 数学推导

凯利公式的唯一目标是：**在假定无限期复利再投资的前提下，最大化资本的长期几何复合增长率 $E[\ln(W_T)]$**。

### 2.1 离散交易模型
设单次交易胜率为 $p$，亏损概率为 $q = 1 - p$，盈利时的盈亏比为 $b$（即赢时赚 $b$ 倍，输时输 $1$ 倍）：
$$f^* = \frac{p \cdot b - q}{b} = p - \frac{1 - p}{b}$$
* $f^*$ 为单笔交易所应动用的最优资金比例（包含杠杆）。

---

### 2.2 连续收益与算法交易模型 (Ernest Chan 推导)
在连续交易中，资产价格遵循对数正态扩散过程，年化预期超额收益为 $\mu - r$，年化波动率为 $\sigma$。求解最优杠杆倍数 $f^*$：
$$\max_f E[\ln(1 + R)] \approx \max_f \left( r + f(\mu - r) - \frac{1}{2} f^2 \sigma^2 \right)$$
对 $f$ 求一阶导并令其等于零：
$$\frac{d}{df} = (\mu - r) - f \sigma^2 = 0 \implies \mathbf{f^* = \frac{\mu - r}{\sigma^2} = \frac{\text{Sharpe}}{\sigma}}$$

* **核心结论**：
  - 最优持仓杠杆倍数正比于**夏普比率 (Sharpe)**，反比于**资产波动率 ($\sigma$)**；
  - 波动率越大，所允许的杠杆倍数必须以平方速度急剧削减！

---

## 3. “全凯利自杀陷阱”与半凯利 (Half-Kelly) 铁律

```
复合年化增长率 g(f)
        ▲
        │               全凯利峰值 f* (理论最大，但回撤巨大)
        │                 ▼
        │              ╭─────╮
        │            ╭─╯     ╰─╮
        │          ╭─╯         ╰─╮
        │        ╭─╯             ╰─╮
        │      ╭─╯                 ╰─╮
        │    ╭─╯                     ╰─╮
        │  ╭─╯                         ╰─╮  过度杠杆自杀区: 增长率跌入负值
        │╭─╯                             ╰──────────────────────────►
        └─────────────────────────────────────────────── 杠杆倍数 f
               ▲               ▲
          半凯利 0.5f*      全凯利 f*
          (75% 收益率,       (50% 巨幅回撤,
           回撤降低50%)       参数过估即爆仓)
```

### 3.1 为什么实盘绝不能使用全凯利？
1. **参数估计误差是致命的**：回测中估计出的 $\mu$ 和 $\sigma$ 是历史样本，未来极易衰减。如果实际夏普比率比估计值低 30%，按照估计的全凯利下注，杠杆就会直接越过顶点冲进右侧的**“负收益自杀区”**！
2. **毁灭性的心理与净值回撤**：在全凯利下，资本回撤超过 50% 的概率高达 1/3。对于基金管理人而言，50% 的回撤足以触发客户挤兑、清盘强平与职业生涯终结。

### 3.2 实战铁律：必须且只能使用半凯利 (Half-Kelly)
**在任何实盘配置中，杠杆比例严格取理论全凯利的 $50\%$（或 $25\%$）：**
$$f_{\text{practical}} = 0.5 \times f^* = \frac{1}{2} \cdot \frac{\mu - r}{\sigma^2}$$
* **权衡优势**：
  - 保留了全凯利 **$75\%$** 的长期几何复合增长速度；
  - 将投资组合的方差与回撤降低了整整 **$50\%$**；
  - 赋予系统对抗参数估计误差和极端流动性冲击的超强安全边际。

---

## 4. 生产级动态回撤阶梯控制与保护机制

为了确保账户整体净值绝不突破投资人允许的最大回撤红线（如 MaxDD $\le 10\%$），必须建立动态降仓状态机：

```python
import numpy as np

class DynamicDrawdownManager:
    """生产级动态回撤监控与仓位阶梯截断控制器"""
    def __init__(self, 
                 soft_warning_dd: float = 0.04,   # 4% 软预警线
                 hard_cut_dd: float = 0.07,       # 7% 硬削减线
                 kill_switch_dd: float = 0.10):   # 10% 熔断平仓线
        self.soft_warning_dd = soft_warning_dd
        self.hard_cut_dd = hard_cut_dd
        self.kill_switch_dd = kill_switch_dd
        self.peak_nav = 1.0
        
    def evaluate_position_multiplier(self, current_nav: float) -> float:
        """
        根据当前最新累计净值，动态返回持仓缩放系数 (0.0 ~ 1.0)
        """
        if current_nav > self.peak_nav:
            self.peak_nav = current_nav
            
        current_dd = (self.peak_nav - current_nav) / self.peak_nav
        
        # 1. 触发极端熔断线 -> 清空所有持仓，锁定风险
        if current_dd >= self.kill_switch_dd:
            return 0.0
            
        # 2. 触发硬削减线 -> 仓位强制压缩至 30%
        elif current_dd >= self.hard_cut_dd:
            return 0.3
            
        # 3. 触发软预警线 -> 仓位阶梯削减至 60%
        elif current_dd >= self.soft_warning_dd:
            # 线性插值平滑削减
            progress = (current_dd - self.soft_warning_dd) / (self.hard_cut_dd - self.soft_warning_dd)
            return float(0.6 - 0.3 * progress)
            
        # 4. 正常状态 -> 允许正常按策略执行 (100% 建议仓位)
        return 1.0
```

---

## 5. 超越 VaR：条件在险价值 (CVaR / Expected Shortfall)

金融时间序列的收益分布具有极其严重的“厚尾”和“左偏”（黑天鹅事件频发）。
* **传统 VaR (Value-at-Risk) 的欺骗性**：$99\%$ 置信度下的 1 日 VaR 仅告诉你“在 $99\%$ 的日子里，亏损不会超过 3%”，但完全无法告诉你那 $1\%$ 最糟糕的极端崩盘日会亏损 5%、20% 还是 100%！
* **CVaR (Expected Shortfall)**：度量当损失超过 VaR 门槛时，极端尾部损失的**条件期望值**：
  $$\text{CVaR}_\alpha = E[L \mid L > \text{VaR}_\alpha]$$
* **风控准则**：在优化组合时，使用 CVaR 替代样本方差作为风险惩罚项，能够大幅压低极值肥尾风险，有效避免微盘踩踏或单日闪崩穿仓。

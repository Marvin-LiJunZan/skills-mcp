# 08 - 均值回归、协整检验与卡尔曼滤波动态对冲

> 本模块系统拆解欧内斯特·陈 (Ernest P. Chan) 最具标志性的核心策略体系：**统计套利均值回归 (Mean Reversion)**、**ADF 与协整检验 (Cointegration)**、**OU 过程半衰期测算 (Half-life)** 以及 **卡尔曼滤波 (Kalman Filter) 动态对冲比率**。

---

## 1. 均值回归的数学底层：从平稳性到协整

金融资产的单边价格绝大多数是具有非平稳趋势的“随机游走”序列（单位根过程 $I(1)$）。若直接对两个非平稳价格做配对交易，必然陷入“伪回归 (Spurious Regression)”的毁灭性陷阱。

### 1.1 增强迪基-富勒平稳性检验 (ADF Test)
检验价格序列或价差 $S_t$ 是否具有均值回归特性：
$$\Delta S_t = \alpha + \beta t + \gamma S_{t-1} + \sum_{p=1}^P \delta_p \Delta S_{t-p} + \epsilon_t$$
* **原假设 $H_0: \gamma = 0$**（序列存在单位根，非平稳，不具有均值回归性）；
* **备择假设 $H_1: \gamma < 0$**（序列平稳，具有向历史中枢靠拢的均值回归力）；
* **判定标准**：当 ADF 检验的 p-value $< 0.05$（或 t 统计量显著小于临界值）时，方能确认价差是平稳的。

---

### 1.2 协整 (Cointegration)：寻找永不走散的孪生序列
设资产 $A$ 的对数价格为 $P_A \sim I(1)$，资产 $B$ 的对数价格为 $P_B \sim I(1)$。若存在常数 $\beta$（对冲比例 Hedge Ratio），使得它们的线性组合：
$$S_t = P_{A,t} - \beta \cdot P_{B,t}$$
满足 $S_t \sim I(0)$（平稳过程），则称资产 $A$ 与 $B$ 存在**协整关系**。

* **经济学直觉（遛狗理论）**：主人（资产 A）和小狗（资产 B）各自在公园里漫无目的地随机走动（非平稳），但只要中间有一根弹性牵引绳（协整约束，如相同的上游原材料、可互换的替代产品、母子公司股权关系），一旦两者距离拉大，绳子的拉力就会迫使它们重新靠拢。
* **Engle-Granger 两步法**：
  1. 对 $P_{A,t} = \alpha + \beta P_{B,t} + \epsilon_t$ 执行 OLS 回归，求得残差序列 $\hat{\epsilon}_t$；
  2. 对残差 $\hat{\epsilon}_t$ 进行 ADF 检验。若残差拒绝单位根，则协整关系成立。

---

## 2. Ornstein-Uhlenbeck (OU) 过程与均值回归半衰期 (Half-life)

平稳并不代表就能赚钱。如果一个价差序列需要 3 年才能回归均值一次，资金的时间成本会彻底击垮策略。必须定量测算**均值回归半衰期**。

### 2.1 OU 连续时间过程与离散化
连续时间下的均值回归 Ornstein-Uhlenbeck 模型：
$$dS_t = \lambda (\mu - S_t) dt + \sigma dW_t$$
* $\mu$：长期均衡中枢；
* $\lambda$：均值回归速度系数（$\lambda > 0$ 表示拉回均值，$0$ 为随机游走）。

离散化为 AR(1) 形式：
$$\Delta S_t = S_t - S_{t-1} = \theta + \gamma S_{t-1} + \epsilon_t$$
其中 $\gamma = -\lambda \Delta t$。

### 2.2 半衰期数学公式与交易周期确定
价差偏离中枢后，衰减一半所需要的特征期望时间：
$$\text{Half-life} = -\frac{\ln(2)}{\gamma}$$

| 半衰期范围 | 策略判定与操作法则 |
| :--- | :--- |
| **$< 1$ 天** | 超高频微观结构噪声，滑点与双边印花税将吃尽所有利润，非低延迟做市商不可行。 |
| **$5 \sim 30$ 天** | **绝佳波段套利区间**。布林带（Bollinger Bands）或 Z-Score 均值回归策略的最佳试验田。 |
| **$> 90$ 天** | 资金周转极慢，且极其容易遭遇基本面断裂引发的“协整破裂（单边离散）”，应直接放弃。 |

```python
import numpy as np
import statsmodels.api as sm

def calculate_half_life(spread: np.ndarray) -> float:
    """计算价差序列的 Ornstein-Uhlenbeck 均值回归半衰期"""
    spread_lag = spread[:-1]
    spread_diff = spread[1:] - spread_lag
    
    # 回归: spread_diff = alpha + gamma * spread_lag
    X = sm.add_constant(spread_lag)
    model = sm.OLS(spread_diff, X).fit()
    gamma = model.params[1]
    
    if gamma >= 0:
        return np.inf  # 不具有均值回归特性
    return float(-np.log(2.0) / gamma)
```

---

## 3. 卡尔曼滤波 (Kalman Filter) 动态自适应对冲比率

传统 OLS 回归假定对冲比例 $\beta$ 在全历史周期恒定不变。然而在真实宏观经济与产业链变迁中，两只股票的真实对冲比例是**随时间动态漂移 (Time-varying)** 的。静态 OLS 必然在结构突变点爆发巨额亏损。

卡尔曼滤波将对冲比例视为一个不可直接观测的“隐状态 (Hidden State)”，并随每个最新 Tick/Bar 的到来做最优在线自适应更新。

### 3.1 状态空间方程构建
1. **状态方程（State Equation - 真实的对冲比率随机游走漂移）**：
   $$\begin{bmatrix} \alpha_t \\ \beta_t \end{bmatrix} = \begin{bmatrix} \alpha_{t-1} \\ \beta_{t-1} \end{bmatrix} + w_t, \quad w_t \sim \mathcal{N}(0, Q)$$
   其中 $Q = \delta / (1-\delta) \cdot I$ 为过程噪声协方差，$\delta \approx 0.0001$ 为自适应更新学习率。
2. **观测方程（Measurement Equation - 资产 A 与资产 B 的实时价格）**：
   $$y_t = [1, \quad x_t] \begin{bmatrix} \alpha_t \\ \beta_t \end{bmatrix} + v_t, \quad v_t \sim \mathcal{N}(0, R)$$
   其中 $y_t$ 为资产 A 价格，$x_t$ 为资产 B 价格，$v_t$ 为即时观测噪声。

### 3.2 完整卡尔曼滤波 Python 实战实现

```python
import numpy as np
import pandas as pd

class KalmanPairsHedge:
    """基于卡尔曼滤波在线估计两资产动态对冲比率与实时价差"""
    def __init__(self, delta: float = 1e-4, R: float = 1e-3):
        self.delta = delta
        self.R = R
        self.Vw = self.delta / (1.0 - self.delta) * np.eye(2)
        self.beta = np.zeros((2, 1))          # [intercept, slope]
        self.P = np.zeros((2, 2))             # 估计误差协方差
        
    def step(self, y_price: float, x_price: float) -> tuple:
        """
        输入最新截面的 y_price (资产A) 和 x_price (资产B)
        返回: (当前动态对冲比率 beta_t, 当前对冲残差 spread_t, 残差方差 Q_t)
        """
        # 1. 状态外推预测
        x_obs = np.array([[1.0], [x_price]])
        self.P = self.P + self.Vw
        
        # 2. 观测残差与方差
        y_pred = float(x_obs.T @ self.beta)
        error = y_price - y_pred
        Q_variance = float(x_obs.T @ self.P @ x_obs) + self.R
        
        # 3. 计算卡尔曼增益 K
        K = (self.P @ x_obs) / Q_variance
        
        # 4. 状态后验更新
        self.beta = self.beta + K * error
        self.P = self.P - K @ (x_obs.T @ self.P)
        
        hedge_ratio = float(self.beta[1, 0])
        current_spread = error
        return hedge_ratio, current_spread, np.sqrt(Q_variance)
```

---

## 4. 均值回归实盘交易触发与硬性止损规则

有了动态对冲比率 $\beta_t$ 和平稳价差 $S_t$，制定交易规则：
1. **标准化 Z-Score 信号**：
   $$Z_t = \frac{S_t - \mu_{S, \text{lookback}}}{\sigma_{S, \text{lookback}}}$$
   其中移动窗口通常设为 $1 \sim 1.5$ 倍的半衰期 $\text{Half-life}$。
2. **进场阈值**：
   - 当 $Z_t < -1.5$ 时：做多价差（买入资产 A，按 $\beta_t$ 比例做空资产 B）；
   - 当 $Z_t > +1.5$ 时：做空价差（做空资产 A，按 $\beta_t$ 比例做多资产 B）。
3. **出场中枢离场**：
   - 当 $Z_t$ 回归至 $[-0.2, +0.2]$ 区间时平仓获利了结。
4. **灾难性止损（Catastrophic Stop-loss）**：
   - **铁律**：如果 $|Z_t| > 3.5$ 且持续 2 个半衰期未修复，**无条件平仓割肉！** 这意味着原本的协整经济学纽带已经永久性断裂（如其中一家公司爆发财务造假或技术颠覆），死扛均值回归必然导致单边穿仓。

# 06 - 组合优化、Barra 风险模型与交易成本冲击控制

> 本模块讲解将多因子预测打分转化为实际持仓权重的工业级核心引擎：**结构化多因子风险模型 (Barra 体系)**、**二次规划组合优化 (QP)** 以及 **Almgren-Chriss 市场冲击成本控制**。

---

## 1. 结构化多因子风险模型 (Barra 体系)

在股票池有 $N=4000$ 只股票时，直接计算全样本资产协方差矩阵 $\Sigma$ 需要估计 $\frac{N(N+1)}{2} \approx 800$ 万个参数！在时间序列长度 $T < N$ 的真实环境中，样本协方差矩阵必然不可逆（奇异阵），导致均值-方差优化彻底失控。

Barra 结构化风险模型通过将风险分解到低维风格因子上，彻底解决了该维数灾难。

### 1.1 Barra 结构化线性模型
在任意时间点 $t$：
$$r = X f + u$$
* $r$：$N \times 1$ 的个股超额收益向量；
* $X$：$N \times K$ 的已知因子暴露矩阵（涵盖行业哑变量 + 风格因子，如 Beta、Size、Value、Momentum、Volatility 等），$K \ll N$（通常 $K \approx 40$）；
* $f$：$K \times 1$ 的因子收益率向量；
* $u$：$N \times 1$ 的特质收益率（残差），假设与因子收益不相关，且各股票之间特质风险相互独立。

### 1.2 协方差矩阵的结构化降维分解
根据上述模型，资产收益的协方差矩阵被精确解构为两部分：
$$\Sigma = X F X^T + \Delta$$
* $F = \text{Cov}(f)$：$K \times K$ 的因子协方差矩阵（仅需估计数百个参数，数值极其稳健）；
* $\Delta = \text{diag}(\sigma_{u,1}^2, \dots, \sigma_{u,N}^2)$：$N \times N$ 的对角阵，代表各股票特质风险方差。

**工程优势**：
1. **保证正定可逆**：只要 $F$ 正定且特质方差 $\sigma_{u,i}^2 > 0$，求得的 $\Sigma$ 严格正定；
2. **极速矩阵求逆**：利用 Woodbury 矩阵恒等式，计算时间复杂度从 $O(N^3)$ 锐降为 $O(N K^2)$。

---

## 2. 现代组合优化二次规划模型 (Quadratic Programming)

不能简单将因子得分高的股票等权买入，因为这会导致行业严重倾斜、非目标风格（如微盘或高贝塔）暴露过载，承担大量毫无回报的非系统性风险。必须采用**受约束的二次规划 (QP)**。

### 2.1 优化目标函数与惩罚项
设目标持仓权重为 $w$（$N \times 1$），基准指数权重为 $w_b$（如沪深300或中证500），主动权重为 $h = w - w_b$：

$$\max_{w} \underbrace{w^T \alpha}_{\text{预期 Alpha 收益}} - \underbrace{\frac{\lambda}{2} h^T \Sigma h}_{\text{跟踪误差风险惩罚}} - \underbrace{\tau \cdot \sum_{i=1}^N |w_i - w_{0,i}|}_{\text{换手率与交易成本惩罚}}$$

其中：
* $\alpha$：由多因子模型预测的个股超额收益向量；
* $\lambda$：风险厌恶系数（控制组合的主动跟踪误差 Tracking Error）；
* $w_0$：上期期末的实际持仓权重（用于抑制过度换手）；
* $\tau$：单位换手交易摩擦成本估计。

### 2.2 生产级工程约束条件集
1. **预算与多头约束**：
   $$\sum_{i=1}^N w_i = 1, \quad 0 \le w_i \le w_{\max} \quad (\text{如单票权重上限 } 2\% \sim 5\%)$$
2. **行业中性 / 相对基准容忍度约束**：
   $$|h^T D_{\text{ind}, j}| \le \delta_{\text{ind}} \quad (\text{如行业主动偏离不超过 } \pm 1\%)$$
3. **风格因子暴露约束**：
   $$|h^T X_{\text{style}, k}| \le \delta_{\text{style}} \quad (\text{例如要求对 Size 或 Beta 相对基准零暴露})$$
4. **单次换手率硬上限**：
   $$\frac{1}{2} \sum_{i=1}^N |w_i - w_{0,i}| \le \text{MaxTurnover} \quad (\text{例如单期双边换手 } \le 20\%)$$

---

## 3. 基于 CVXPY 的生产级组合优化器实现

```python
import numpy as np
import cvxpy as cp

def optimize_portfolio(alpha: np.ndarray,
                       w_benchmark: np.ndarray,
                       w_initial: np.ndarray,
                       X_factor: np.ndarray,
                       F_cov: np.ndarray,
                       delta_specific_var: np.ndarray,
                       risk_aversion: float = 1.0,
                       max_stock_weight: float = 0.03,
                       turnover_limit: float = 0.25,
                       industry_matrix: np.ndarray = None,
                       ind_tolerance: float = 0.01) -> np.ndarray:
    """
    基于 Barra 因子风险模型与二次规划的生产级多因子组合优化器
    
    参数:
    ----------
    alpha : np.ndarray, (N,) 预期超额收益
    w_benchmark : np.ndarray, (N,) 基准成分股权重
    w_initial : np.ndarray, (N,) 当前现有持仓权重
    X_factor : np.ndarray, (N, K) 因子暴露矩阵
    F_cov : np.ndarray, (K, K) 因子协方差矩阵
    delta_specific_var : np.ndarray, (N,) 个股特质方差
    """
    N = len(alpha)
    w = cp.Variable(N)
    h = w - w_benchmark  # 主动权重
    
    # 构造因子风险项: h.T @ (X @ F @ X.T + Delta) @ h
    # = (X.T @ h).T @ F @ (X.T @ h) + sum(delta * h^2)
    factor_active_exp = X_factor.T @ h
    factor_risk = cp.quad_form(factor_active_exp, F_cov)
    specific_risk = cp.sum(cp.multiply(delta_specific_var, cp.square(h)))
    total_active_risk = factor_risk + specific_risk
    
    # 目标函数: 最大化 Alpha 减去 风险惩罚
    objective = cp.Maximize(alpha.T @ w - (risk_aversion / 2.0) * total_active_risk)
    
    constraints = [
        cp.sum(w) == 1.0,               # 资金完全配置
        w >= 0.0,                       # 纯多头约束
        w <= max_stock_weight,          # 单票上限
        cp.sum(cp.abs(w - w_initial)) <= 2.0 * turnover_limit  # 换手率约束
    ]
    
    # 行业硬约束
    if industry_matrix is not None:
        # industry_matrix 形状为 (N, M_ind)
        active_ind_exp = industry_matrix.T @ h
        constraints.append(active_ind_exp <= ind_tolerance)
        constraints.append(active_ind_exp >= -ind_tolerance)
        
    problem = cp.Problem(objective, constraints)
    problem.solve(solver=cp.OSQP, verbose=False)
    
    if problem.status not in ["optimal", "optimal_inaccurate"]:
        raise ValueError(f"优化求解失败，状态: {problem.status}")
        
    return np.clip(w.value, 0.0, 1.0)
```

---

## 4. 市场流动性冲击模型 (Almgren-Chriss)

在大资金规模（几亿至几十亿）下，真实交易产生的滑点绝不是固定的几个基点，而是取决于订单占全市场成交量的比例（Participation Rate）。

### 4.1 瞬时冲击与永久冲击
* **永久市场冲击 (Permanent Impact)**：大单买入改变了市场的供求均衡，导致价格不可逆地上移：
  $$I_{\text{perm}} = \gamma \cdot \frac{Q}{V} \cdot \sigma$$
  其中 $Q$ 为交易股数，$V$ 为全天成交量，$\sigma$ 为日波动率。
* **瞬时市场冲击 (Temporary Impact)**：大单在撮合瞬间吃尽盘口流动性引发的临时滑点，在成交后部分恢复：
  $$I_{\text{temp}} = \eta \cdot \left(\frac{q_t}{v_t}\right)^\alpha$$
  通常 $\alpha \approx 0.5$（经典的**平方根定律 Square-root Law**）。

### 4.2 组合优化中的容量瓶颈
任何追求超高 IC 的高频换手策略，其 Alpha 衰减收益在资金量突破一定规模时，都会被非线性的市场冲击彻底吞噬。因此，在生成组合权重时，**必须将个股的成交额占比（ADV%）作为硬性惩罚项纳入目标函数**，限制单日调仓量不得超过目标股过去 20 日平均成交额（ADV）的 1%~3%。

# 04 - 多因子定价模型体系与 GRS 联合假设检验

> 本模块系统梳理现代实证资产定价领域的基石模型（FF3、Carhart4、FF5、q-Factor），并详细推导评估资产定价模型优劣的黄金标准——**GRS (Gibbons-Ross-Shanken) 联合假设检验**，附带可直接执行的 Python 计算实现。

---

## 1. 经典多因子资产定价模型全景

资产定价模型的核心使命是用尽可能精简的系统性风险因子，解释全市场资产的截面预期收益，使得截距项（定价误差 $\alpha_i$）尽可能收敛到零。

### 1.1 Fama-French 三因子模型 (FF3, 1993)
$$R_{i,t} - R_{f,t} = \alpha_i + \beta_{i,M} MKT_t + \beta_{i,S} SMB_t + \beta_{i,V} HML_t + \epsilon_{i,t}$$
* **MKT (Market)**：全市场超额收益。
* **SMB (Small Minus Big)**：按规模分组构建的多空小市值因子。
* **HML (High Minus Low)**：按账面市值比（B/M）构建的价值溢价因子。
* **局限**：无法解释动量效应（Jegadeesh-Titman 1993）及高盈利、低投资公司的超额收益。

---

### 1.2 Carhart 四因子模型 (1997)
$$R_{i,t} - R_{f,t} = \alpha_i + \beta_{i,M} MKT_t + \beta_{i,S} SMB_t + \beta_{i,V} HML_t + \beta_{i,U} UMD_t + \epsilon_{i,t}$$
* **UMD (Up Minus Down)**：基于过去 2~12 个月累计收益构建的截面动量因子。
* **应用场景**：公募基金业绩归因评价的标准模型（判定基金经理获取的是真实选股能力还是动量/风格暴露）。

---

### 1.3 Fama-French 五因子模型 (FF5, 2015)
$$R_{i,t} - R_{f,t} = \alpha_i + \beta_{i,M} MKT_t + \beta_{i,S} SMB_t + \beta_{i,V} HML_t + \beta_{i,R} RMW_t + \beta_{i,C} CMA_t + \epsilon_{i,t}$$
* **RMW (Robust Minus Weak)**：高营业利润率减低营业利润率股票的多空组合（盈利因子）。
* **CMA (Conservative Minus Aggressive)**：低资产增长率（投资稳健）减高资产增长率股票的多空组合（投资因子）。
* **关键发现**：在美股市场加入 RMW 和 CMA 之后，传统价值因子 HML 的解释力几乎被完全吸收（冗余因子）；但**在 A 股市场，价值因子具有独立性，无法被 RMW 和 CMA 取代**。

---

### 1.4 Hou-Xue-Zhang q-Factor 模型 (2015)
基于企业投资理论（Q 理论）而非传统的贴现现金流模型：
$$R_{i,t} - R_{f,t} = \alpha_i + \beta_{i,M} MKT_t + \beta_{i,ME} r_{ME,t} + \beta_{i,IA} r_{I/A,t} + \beta_{i,ROE} r_{ROE,t} + \epsilon_{i,t}$$
* $r_{ME}$：市值因子（Market Equity）；
* $r_{I/A}$：投资与资产比率变动（Investment-to-Assets）；
* $r_{ROE}$：净资产收益率（Return on Equity）。
* **理论优势**：模型参数直接源自企业最优投资一阶条件，对异象资产组合的定价拟合优度常常超越 FF5。

---

## 2. GRS (Gibbons-Ross-Shanken 1989) 联合假设检验

当使用一个多因子模型对 $N$ 个测试资产（例如 25 个规模-价值双重排序组合）进行时间序列回归时，单个资产的 t 检验只能说明该资产是否被定价。为了评估**模型整体是否成立**，必须检验所有资产的定价误差 $\alpha_1, \alpha_2, \dots, \alpha_N$ 是否**联合为零**：

$$H_0: \alpha_1 = \alpha_2 = \cdots = \alpha_N = 0$$

### 2.1 GRS 统计量数学公式
设样本长度为 $T$，测试资产数量为 $N$，模型因子数量为 $K$。
- $\hat{\alpha} = [\hat{\alpha}_1, \dots, \hat{\alpha}_N]'$ 为 $N \times 1$ 的估计定价误差向量；
- $\hat{\Sigma}_\epsilon = \frac{1}{T-K-1} \sum_{t=1}^T \hat{\epsilon}_t \hat{\epsilon}_t'$ 为回归残差的 $N \times N$ 样本协方差矩阵；
- $\bar{f} = \frac{1}{T} \sum_{t=1}^T f_t$ 为 $K \times 1$ 的因子样本时序均值向量；
- $\hat{\Sigma}_f = \frac{1}{T-1} \sum_{t=1}^T (f_t - \bar{f})(f_t - \bar{f})'$ 为因子收益率的 $K \times K$ 协方差矩阵。

GRS 统计量定义为：
$$GRS = \frac{T - N - K}{N} \cdot \left(1 + \bar{f}' \hat{\Sigma}_f^{-1} \bar{f}\right)^{-1} \cdot \left(\hat{\alpha}' \hat{\Sigma}_\epsilon^{-1} \hat{\alpha}\right)$$

在正态性假设下，该统计量在原假设 $H_0$ 下严格服从 **F 分布**：
$$GRS \sim F(N, T - N - K)$$

### 2.2 几何直观与经济学含义
式中：
* $\bar{f}' \hat{\Sigma}_f^{-1} \bar{f} = \theta_f^2$ 为因子本身构成的切点组合的平方夏普比率；
* $\hat{\alpha}' \hat{\Sigma}_\epsilon^{-1} \hat{\alpha}$ 为测试资产 Alpha 的相对波动率大小；
* **本质**：GRS 检验在比较“仅由因子构成的有效前沿”与“加入测试资产后的全市场有效前沿”是否存在统计学显著的差异。如果测试资产无法显著提升总有效前沿的夏普比率，则 GRS 接受原假设（模型成功定价）。

---

## 3. GRS 检验算法的 Python 实现

```python
import numpy as np
import scipy.stats as stats

def grs_test(returns: np.ndarray, factors: np.ndarray) -> dict:
    """
    Gibbons, Ross, and Shanken (1989) 联合定价误差检验
    
    参数:
    ----------
    returns : np.ndarray, 形状为 (T, N)
        T 个时间期，N 个测试资产的超额收益矩阵
    factors : np.ndarray, 形状为 (T, K)
        T 个时间期，K 个风险因子的收益率矩阵
        
    返回:
    ----------
    dict 包含:
        - grs_stat: GRS F统计量
        - p_value: 统计显著性 p 值 (p > 0.05 则不能拒绝 H0，说明模型定价良好)
        - avg_abs_alpha: 平均绝对定价误差 (越小越好)
    """
    T, N = returns.shape
    _, K = factors.shape
    
    # 构造设计矩阵 (包含常数项截距)
    X = np.column_stack([np.ones(T), factors])
    
    # 逐资产执行 OLS 回归: returns = X * B + E
    # B 矩阵形状为 (K+1, N), 第一行为 alpha
    B = np.linalg.lstsq(X, returns, rcond=None)[0]
    alphas = B[0, :]
    residuals = returns - X @ B
    
    # 计算残差协方差矩阵 Sigma_e
    sigma_e = (residuals.T @ residuals) / (T - K - 1)
    sigma_e_inv = np.linalg.inv(sigma_e)
    
    # 因子均值向量与协方差矩阵
    f_mean = np.mean(factors, axis=0)
    sigma_f = np.cov(factors, rowvar=False)
    if K == 1:
        sigma_f_inv = 1.0 / sigma_f
        factor_sharpe_sq = (f_mean ** 2) * sigma_f_inv
    else:
        sigma_f_inv = np.linalg.inv(sigma_f)
        factor_sharpe_sq = f_mean.T @ sigma_f_inv @ f_mean
        
    # 计算 GRS 统计量
    alpha_term = alphas.T @ sigma_e_inv @ alphas
    c_factor = 1.0 / (1.0 + factor_sharpe_sq)
    d_f = (T - N - K) / N
    
    grs_stat = d_f * c_factor * alpha_term
    
    # F 分布 p 值 (自由度 N, T - N - K)
    p_value = 1.0 - stats.f.cdf(grs_stat, N, T - N - K)
    avg_abs_alpha = np.mean(np.abs(alphas))
    
    return {
        "grs_stat": float(grs_stat),
        "p_value": float(p_value),
        "avg_abs_alpha": float(avg_abs_alpha)
    }
```

---

## 4. 模型优劣评估的三大多元辅助指标

在实际大样本检验中（尤其 $T$ 很大时），GRS 统计量因检验功效极强，往往极易拒绝原假设。因此实务中需结合以下辅助指标进行横向模型对比：

1. **平均绝对定价误差 $A|\alpha|$**：
   $$A|\alpha| = \frac{1}{N} \sum_{i=1}^N |\hat{\alpha}_i|$$
   值越小，说明模型对各类组合的未解释残差越少，定价越精准。
2. **平均相对定价误差比率**：
   $$\frac{A|\alpha|}{A|\bar{R}|} = \frac{\frac{1}{N} \sum |\hat{\alpha}_i|}{\frac{1}{N} \sum |\bar{R}_i|}$$
   衡量定价误差占测试资产原始均值收益的相对比例。
3. **Alpha 波动提升率**：
   通过比较不同因子模型加入后残差协方差的对角线缩减程度，检验新因子是否有效降低了组合无法解释的特质风险。

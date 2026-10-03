# 量化交易核心决策树与公式速查手册 (Cheatsheet)

---

## 1. 核心量化投研决策树

### 1.1 因子有效性与准入决策树
```
           [ 原始输入数据: 财务指标 / 量价特征 ]
                           │
                           ▼
          [ 检查是否存在向前看偏差 / 幸存者偏差? ]
              ├── 存在 ──> 立即修正数据时间戳与股票池
              └── 通过
                           │
                           ▼
          [ 数据清洗三部曲: MAD去极值 -> Z-Score标准化 -> 行业/市值中性化 ]
                           │
                           ▼
          [ 投资组合排序检验: 5分位分层回测 ]
              ├── 各组年化收益是否单调? ── 否 ──> 剔除 (非稳健因子)
              └── 是
                           │
                           ▼
          [ IC / Rank IC 评价 ]
              ├── |Mean(Rank IC)| >= 0.03 且 IR >= 0.5? ── 否 ──> 剔除
              └── 是
                           │
                           ▼
          [ Fama-MacBeth 截面回归 (含 Newey-West HAC 调整) ]
              ├── t 统计量是否达到多重测试门槛 (|t| > 3.0)? ── 否 ──> 疑似 p-hacking, 淘汰
              └── 是
                           │
                           ▼
          [ GRS 联合定价误差检验 ]
              ├── 新因子能否显著降低已有定价模型 (如 FF5) 的定价误差? ── 否 ──> 冗余因子
              └── 是
                           │
                           ▼
                 ★ 纳入量化因子候选库 ★
```

---

### 1.2 均值回归配对交易决策树 (Ernest Chan 体系)
```
          [ 两只潜在配对资产的对数价格序列 PA, PB ]
                           │
                           ▼
          [ ADF 检验 PA 与 PB 单独的平稳性 ]
              ├── 两者均为 I(0) 平稳序列? ── 是 ──> 直接交易单个平稳资产
              └── 均为 I(1) 单位根序列?
                           │
                           ▼
          [ Engle-Granger / Johansen 协整检验 ]
              ├── 线性组合残差序列是否拒绝单位根 (p < 0.05)? ── 否 ──> 不存在协整, 放弃
              └── 是 (两者存在协整纽带)
                           │
                           ▼
          [ 拟合 OU 过程测算半衰期 (Half-life) ]
              ├── Half-life < 1天? ──> 交易摩擦过高, 放弃
              ├── Half-life > 60天? ──> 资金占用成本高且易断裂, 放弃
              └── 5天 <= Half-life <= 30天 (黄金区间)
                           │
                           ▼
          [ 启动卡尔曼滤波在线跟踪动态时变对冲比率 beta_t ]
                           │
                           ▼
          [ 计算标准化 Z-Score 信号 ]
              ├── Z_t < -1.5 ──> 买入A, 卖空 beta_t 数量的 B (做多价差)
              ├── Z_t > +1.5 ──> 卖空A, 买入 beta_t 数量的 B (做空价差)
              ├── |Z_t| <= 0.2 ──> 均值回归到位, 平仓止盈
              └── |Z_t| > 3.5 持续超过 2 个半衰期 ──> 协整破裂, 触发灾难性硬止损!
```

---

## 2. 核心数学模型公式卡片

| 模块 | 核心指标 / 公式 | 关键参数说明与实务取值 |
| :--- | :--- | :--- |
| **MAD 去极值** | $M \pm 3 \times 1.4826 \times \text{Median}(\|X - M\|)$ | 软缩尾（Winsorization）处理，不剔除样本。 |
| **中性化残差** | $y_i = \sum \beta_{\text{ind}} D_{i,j} + \beta_{\text{size}} \ln(\text{Cap}_i) + \epsilon_i$ | $\epsilon_i$ 为剥离行业与市值后的纯净风格值。 |
| **信息比率 (IR)** | $\text{IR} = \frac{\text{Mean}(\text{Rank IC})}{\text{Std}(\text{Rank IC})}$ | 实操及格线 $\ge 0.5$；优秀 $\ge 0.8$。 |
| **Newey-West 滞后** | $L = \text{round}\left(4 \cdot (T / 100)^{2/9}\right)$ | 截面 FMB 回归必须启用的 HAC 滞后阶数。 |
| **GRS 统计量** | $\frac{T-N-K}{N} (1 + \bar{f}' \hat{\Sigma}_f^{-1} \bar{f})^{-1} (\hat{\alpha}' \hat{\Sigma}_\epsilon^{-1} \hat{\alpha}) \sim F$ | 联合检验多因子定价误差是否全为零。 |
| **Harvey 多重门槛** | $\|t\| \ge 3.0$（甚至 $3.39$） | 考虑了因子动物园多重测试后的真实显著门槛。 |
| **Barra 协方差** | $\Sigma = X F X^T + \Delta$ | 降维协方差估计，保证矩阵对称正定可逆。 |
| **OU 半衰期** | $\text{Half-life} = -\frac{\ln 2}{\lambda}$ | $\Delta S_t = \lambda S_{t-1} + \epsilon$ 回归求得 $\lambda$。 |
| **半凯利公式** | $f_{\text{half}} = \frac{1}{2} \cdot \frac{\mu - r}{\sigma^2} = \frac{1}{2} \cdot \frac{\text{Sharpe}}{\sigma}$ | 杠杆倍数减半，防范参数估计误差与暴跌爆仓。 |
| **股指期货基差** | $\text{Basis}_t = S_t - F_t$ | 现货高于期货为贴水，注意对冲滚仓年化折价成本。 |
| **VWAP 分配量** | $V_i = V_{\text{total}} \cdot \frac{\text{HistVol}_i}{\sum \text{HistVol}}$ | 按历史日内成交量 U 型分布动态拆单执行。 |

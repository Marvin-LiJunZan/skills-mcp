# 05 - 数据挖掘、多重假设检验与 p-hacking 防伪军规

> 本模块直击量化投研界最大的“伪科学陷阱”——**过度拟合与数据挖掘 (Data Snooping / p-hacking)**。系统梳理 Harvey, Liu, and Zhu (2016) 的划时代检验标准，给出控制假发现率 (FDR) 的完整数学工具与投研防伪军规。

---

## 1. “因子动物园”与资产定价的假阳性危机

在金融学术界和工业界过去数十年的发展中，被各类文献报道具有“显著超额收益”的因子超过 400 个（被称为 **Factor Zoo，因子动物园**，Cochrane 2011）。

### 1.1 为什么回测完美的策略实盘必亏？
1. **研究者的自由度（p-hacking）**：
   - 尝试 20 种不同的行业分类标准；
   - 切换 5 种不同的去极值与中性化方式；
   - 调整不同的排序分位数（5分位、10分位、20分位）；
   - 人为截取某段特定的“黄金牛市”回测区间。
   如果研究员尝试了 100 种参数组合，即使这些数据全是纯随机白噪声，依据经典统计学 $\alpha = 0.05$ 的门槛，**也会纯粹因为运气产生 5 个在统计上看似“极其显著”的假因子！**
2. **出版偏倚 (Publication Bias)**：
   学术期刊和投研报告只倾向于发表“成功发现异象”的结果，而对“检验失效”的数千个负结果保持沉默，造成市场对因子强度的严重虚假乐观。

---

## 2. 统计检验门槛的革命：Harvey, Liu, and Zhu (2016)

Harvey, Liu, and Zhu (2016) 在金融学顶刊 *The Journal of Finance* 发表里程碑论文 **《...and the Cross-Section of Expected Returns》**，正式宣告传统经典统计学门槛在多因子领域的破产。

### 2.1 传统门槛的崩溃
* **传统标准**：基于单个假设检验，临界值 $|t| > 1.96$（约 2.0），对应双尾检验显著性水平 $p = 0.05$。
* **致命缺陷**：经典 t 检验仅在“**只做了一次独立检验**”的前提下成立。而在实证资产定价中，历史已经被数以千计的学者和量化机构反复挖掘。

### 2.2 现代多重测试基准
考虑已经测试过的海量因子背景，新因子要想证明自身不是纯粹的随机巧合，其统计显著性门槛必须随着测试次数动态攀升：
* **新因子合格门槛**：必须达到 **$|t| > 3.0$**（甚至 3.39，对应原始 p 值 $< 0.001$）。
* **结论**：凡是历史回测 t 统计量介于 $2.0 \sim 2.8$ 之间的因子，有超过一半是纯粹数据挖掘产生的虚假副产品，实盘必死！

---

## 3. 多重假设检验校正数学模型

面对同时检验的一组候选因子 $\{F_1, F_2, \dots, F_M\}$ 及其对应的原始 p 值 $\{p_1, p_2, \dots, p_M\}$，必须进行多重比较校正。

### 3.1 Bonferroni 极值校正（控制 FWER）
* **目标**：严格控制“至少发生一次假阳性错误”的概率（Family-Wise Error Rate, FWER）。
* **公式**：
  $$p_i^{\text{adjusted}} = \min(M \cdot p_i, 1.0)$$
* **评价**：极其保守。在因子之间存在高度相关性时，会过度惩罚真实有效的因子。

---

### 3.2 Benjamini-Hochberg (BH) 错误发现率控制 (FDR)
* **核心思想**：放弃对“绝不犯一次错误”的过度苛求，转而控制**“被我们宣称显著的发现中，假阳性所占的期望比例（FDR）不超过 $q$（如 5%）”**。
* **执行步骤**：
  1. 将所有 $M$ 个因子的原始 p 值升序排列：$p_{(1)} \le p_{(2)} \le \dots \le p_{(M)}$；
  2. 寻找最大的索引 $k$，满足：
     $$p_{(k)} \le \frac{k}{M} \cdot q$$
  3. 拒绝所有对应的原假设 $H_{(1)}, \dots, H_{(k)}$，认为前 $k$ 个因子真实有效。

```python
import numpy as np

def bh_fdr_correction(p_values: np.ndarray, fdr_target: float = 0.05) -> tuple:
    """
    Benjamini-Hochberg (1995) 错误发现率 (FDR) 校正
    
    返回:
    ----------
    significant_flags : np.ndarray (bool)
        各因子是否通过 FDR 显著性检验
    adjusted_p_values : np.ndarray
        校正后的 q-values
    """
    p_vals = np.asarray(p_values)
    M = len(p_vals)
    sorted_indices = np.argsort(p_vals)
    sorted_p = p_vals[sorted_indices]
    
    # 临界阈值阶梯
    thresholds = (np.arange(1, M + 1) / M) * fdr_target
    
    # 寻找满足条件的最大 k
    passed = sorted_p <= thresholds
    if np.any(passed):
        max_k = np.max(np.where(passed)[0])
        significant_sorted = np.zeros(M, dtype=bool)
        significant_sorted[:max_k + 1] = True
    else:
        significant_sorted = np.zeros(M, dtype=bool)
        
    significant_flags = np.zeros(M, dtype=bool)
    significant_flags[sorted_indices] = significant_sorted
    
    # 计算调整后 q-value
    adjusted_p = np.zeros(M)
    cummin_term = sorted_p * M / np.arange(1, M + 1)
    cummin_val = np.minimum.accumulate(cummin_term[::-1])[::-1]
    adjusted_p[sorted_indices] = np.clip(cummin_val, 0.0, 1.0)
    
    return significant_flags, adjusted_p
```

---

## 4. 工业级量化投研防伪“军规五条”

1. **经济学与财务常识第一原则**：
   - 任何因子在敲入第一行代码前，必须能用两句话在白板上讲清楚其**经济学因果逻辑**（是承担了哪种未分散风险？还是捕捉了哪类投资者的非理性心理偏误？）。
   - 禁止在没有任何商业逻辑的前提下，利用遗传算法或复杂公式符号穷举海量 Alpha。
2. **全生命周期样本外测试 (OOS, Out-of-Sample)**：
   - 训练样本（In-Sample）与测试样本（Out-of-Sample）必须物理隔离；
   - 严禁在看到测试集表现差之后，返回训练集重新修改因子构造（这实际上将测试集变成了训练集）。
3. **参数稳健性邻域检验 (Sensitivity Plateau)**：
   - 如果某个动量突破策略在参数为 20 日时夏普比率高达 2.5，但微调为 19 日或 21 日时夏普比率暴跌至 0.8，这属于典型的“孤岛过拟合”；
   - 优质因子的表现必须在参数邻域内呈现平缓的高原分布（Plateau）。
4. **子样本时序断代一致性**：
   - 将样本历史划分为两个不重叠的时段（如 2010-2017 与 2018-2024），因子在两个不同市场环境下的收益方向必须保持一致。
5. **换手衰减与交易摩擦真实惩罚**：
   - 回测必须加入真实的冲击成本和滑点模型；若一个因子的毛收益年化 25%，但在扣除 0.15% 双边滑点与印花税后变成负收益，该因子属于“纸面黄金”。

"""组合级绩效指标。"""

from __future__ import annotations

from typing import Dict

import numpy as np
import pandas as pd


def annualized_return(nav_series: pd.Series, periods_per_year: int = 250) -> float:
    if len(nav_series) < 2:
        return 0.0
    total = nav_series.iloc[-1] / nav_series.iloc[0]
    years = (len(nav_series) - 1) / periods_per_year
    if years <= 0:
        return 0.0
    return float(total ** (1.0 / years) - 1.0)


def annualized_volatility(returns: pd.Series, periods_per_year: int = 250) -> float:
    if returns.empty:
        return 0.0
    return float(returns.std(ddof=1) * np.sqrt(periods_per_year))


def max_drawdown(nav_series: pd.Series) -> float:
    if nav_series.empty:
        return 0.0
    peak = nav_series.cummax()
    dd = nav_series / peak - 1.0
    return float(dd.min())


def sharpe(returns: pd.Series, periods_per_year: int = 250, rf: float = 0.0) -> float:
    if returns.empty or returns.std(ddof=1) == 0:
        return 0.0
    excess = returns - rf / periods_per_year
    return float(excess.mean() / returns.std(ddof=1) * np.sqrt(periods_per_year))


def calmar(nav_series: pd.Series, periods_per_year: int = 250) -> float:
    ann = annualized_return(nav_series, periods_per_year)
    mdd = abs(max_drawdown(nav_series))
    if mdd == 0:
        return 0.0
    return float(ann / mdd)


def xirr(cashflows: list, rate_lo: float = -0.9, rate_hi: float = 10.0) -> float:
    if not cashflows:
        return 0.0
    dates = pd.to_datetime([c[0] for c in cashflows])
    days = (dates - dates[0]).days.astype(float)
    amounts = np.array([c[1] for c in cashflows], dtype=float)

    def npv(rate):
        return float(np.sum(amounts / (1.0 + rate) ** (days / 365.0)))

    lo, hi = rate_lo, rate_hi
    if npv(lo) * npv(hi) > 0:
        return 0.0
    for _ in range(80):
        mid = (lo + hi) / 2.0
        if npv(mid) > 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


def summary(nav_series: pd.Series, periods_per_year: int = 250) -> Dict:
    nav_series = nav_series.dropna()
    ret = nav_series.pct_change().dropna()
    total_return = float(nav_series.iloc[-1] / nav_series.iloc[0] - 1.0) if len(nav_series) >= 2 else 0.0
    return {
        "总收益": total_return,
        "年化收益": annualized_return(nav_series, periods_per_year),
        "年化波动率": annualized_volatility(ret, periods_per_year),
        "最大回撤": max_drawdown(nav_series),
        "夏普比率": sharpe(ret, periods_per_year),
        "卡玛比率": calmar(nav_series, periods_per_year),
    }


def analyze_metrics(metrics: Dict) -> tuple:
    """基于回测指标给出分析结论与参数修改建议。"""
    lines = []
    advice = []
    xirr_value = metrics.get("XIRR")
    if xirr_value is None:
        xirr_value = metrics.get("年化收益", 0.0)
    mdd = metrics.get("最大回撤", 0.0)
    avg_cash = metrics.get("平均现金占比", None)
    end_cash = metrics.get("期末现金占比", None)
    wr = metrics.get("胜率", 0.0)
    n = metrics.get("交易次数", 0)
    empty = metrics.get("最长空仓天数", 0)
    insuff = metrics.get("资金不足买入周数", 0)
    excess = metrics.get("超额收益", None)

    if xirr_value <= 0:
        lines.append("按实际投入节奏折算的年化收益率 %.2f%%，策略未实现正收益。" % (xirr_value * 100.0))
        advice.append("考虑收紧买入条件或降低每期仓位。")
    else:
        lines.append("按实际投入节奏折算的年化收益率 %.2f%%，为正收益。" % (xirr_value * 100.0))
    if excess is not None:
        if excess < 0:
            lines.append("比一直持有少赚 %.2f 个百分点。" % (abs(excess) * 100.0))
            advice.append("考虑改进择时规则，或回归买入持有。")
        else:
            lines.append("比一直持有多赚 %.2f 个百分点。" % (excess * 100.0))
    if mdd < -0.20:
        lines.append("最大回撤 %.2f%%，回撤偏大。" % (mdd * 100.0))
        advice.append("可增加止损/止盈规则或降低每期仓位。")
    if avg_cash is not None and avg_cash > 0.40:
        lines.append("平均现金占比 %.2f%%，现金拖累明显。" % (avg_cash * 100.0))
        advice.append("可提高买入力度或降低止盈频率。")
    if end_cash is not None and end_cash > 0.30:
        lines.append("期末现金占比 %.2f%%，仍有较多资金闲置。" % (end_cash * 100.0))
        advice.append("可考虑提高每期仓位或降低卖出阈值。")
    if 0 < wr < 0.4:
        lines.append("胜率 %.2f%%，偏低。" % (wr * 100.0))
        advice.append("检查卖出规则是否过早或过晚。")
    if n > 300:
        lines.append("交易次数 %d，换手偏高。" % n)
        advice.append("可延长调仓间隔或减少止盈触发。")
    if empty and empty > 250:
        lines.append("最长空仓天数 %d，资金闲置时间较长。" % empty)
        advice.append("可开启最久空仓期强制回补。")
    if insuff > 0:
        lines.append("回测中有 %d 个调仓期因现金不足未能全额买入。" % insuff)
        advice.append("可提高初始资金或定期新增金额。")
    if not lines:
        lines.append("当前参数组合表现均衡。")
    if not advice:
        advice.append("保持当前参数继续观察。")
    return "\n".join(lines), "；".join(advice)

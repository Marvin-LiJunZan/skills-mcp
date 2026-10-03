"""回测可视化：收益曲线、买卖点、回撤、指标表。"""

from __future__ import annotations

from pathlib import Path
from typing import Dict

import matplotlib

matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd

from font_config import configure_chinese_font

configure_chinese_font(plt)


def _naive_date(value):
    ts = pd.Timestamp(value)
    if ts.tzinfo is not None:
        ts = ts.tz_localize(None)
    return ts.normalize()


def extract_markers(trades, eq_index):
    """把 trades 中落在 eq_index 内的成交日提取为画点数据。"""
    if trades is None or trades.empty:
        return pd.DataFrame(columns=["date", "side"])
    eq_dates = {_naive_date(v) for v in eq_index}
    rows = []
    for _, row in trades.iterrows():
        d = _naive_date(row["date"])
        if d in eq_dates:
            rows.append({"date": d, "side": row["side"]})
    return pd.DataFrame(rows, columns=["date", "side"])


def plot_backtest(
    equity: pd.Series,
    benchmark: pd.Series,
    metrics: Dict,
    title: str,
    out_path: Path,
    trades=None,
    show_trade_markers: bool = True,
    benchmark_label: str = "基准（买入持有）",
) -> Path:
    eq = (equity / equity.iloc[0] * 100.0).copy()
    eq.index = pd.to_datetime(eq.index)

    bm = benchmark.reindex(equity.index).ffill()
    bm = bm / bm.iloc[0] * 100.0
    bm.index = pd.to_datetime(bm.index)

    fig, (ax1, ax2) = plt.subplots(
        2, 1, figsize=(12, 8), sharex=True, gridspec_kw={"height_ratios": [3, 1]}
    )

    ax1.plot(eq.index, eq.values, label="策略", linewidth=1.8, color="#1f77b4")
    ax1.plot(bm.index, bm.values, label=benchmark_label, linewidth=1.3, color="#9e9e9e", alpha=0.85)

    ax1.set_title(title)
    if show_trade_markers and trades is not None and not trades.empty:
        markers = extract_markers(trades, eq.index)
        for side, color, label in (
            ("buy", "#d62728", "买入"),
            ("sell", "#2ca02c", "卖出"),
        ):
            sub = markers[markers["side"] == side]
            if sub.empty:
                continue
            dates = pd.to_datetime(sub["date"].values)
            vals = [eq.loc[pd.Timestamp(d)] for d in dates]
            ax1.scatter(
                dates,
                vals,
                color=color,
                s=36,
                zorder=5,
                label=label,
                edgecolors="white",
                linewidths=0.5,
            )
    ax1.legend(loc="upper left", fontsize=9)
    ax1.grid(True, alpha=0.25)
    ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    plt.setp(ax1.get_xticklabels(), rotation=45, ha="right")

    dd = eq / eq.cummax() - 1.0
    ax2.fill_between(dd.index, dd.values, 0, color="#ef5350", alpha=0.5)
    ax2.set_ylabel("回撤")
    ax2.grid(True, alpha=0.25)

    metric_lines = [
        f"按实际投入节奏折算的年化收益率 {metrics.get('XIRR', 0):.2%}",
        f"最大回撤 {metrics.get('最大回撤', 0):.2%}",
        f"平均现金 {metrics.get('平均现金占比', 0):.2%}",
        f"期末现金 {metrics.get('期末现金占比', 0):.2%}",
        f"期末资产 {metrics.get('期末资产', 0):,.0f}",
        f"累计盈利 {metrics.get('累计盈利', 0):,.0f}",
        f"夏普 {metrics.get('夏普比率', 0):.2f}",
        f"胜率 {metrics.get('胜率', 0):.2%}",
        f"申购周 {metrics.get('申购周数', 0)}",
        f"赎回周 {metrics.get('赎回周数', 0)}",
        f"交易 {metrics.get('交易次数', 0)}",
    ]
    ax1.text(
        0.99,
        0.03,
        "    ".join(metric_lines),
        transform=ax1.transAxes,
        ha="right",
        va="bottom",
        fontsize=8,
        bbox={"facecolor": "white", "alpha": 0.8, "edgecolor": "#cccccc"},
    )

    fig.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=130, bbox_inches="tight")
    plt.close(fig)
    return out_path

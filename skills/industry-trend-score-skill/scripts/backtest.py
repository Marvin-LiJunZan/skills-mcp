"""本地回测引擎：统一消费「目标仓位」，叠加分批建仓 / 分批止盈 / 费率。"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List

import pandas as pd


DEFAULT_FEE = {
    "purchase_rate": 0.0015,
    "redeem_ladder": [
        {"hold_days": 7, "rate": 0.015},
        {"hold_days": 365, "rate": 0.005},
        {"hold_days": 99999, "rate": 0.0},
    ],
}
EXTRA_FREQ_MODES = {
    "每周": "weekly",
    "每月": "monthly",
    "每季": "quarterly",
    "每年": "annual",
}


def _extra_period_key(t, mode: str):
    t = pd.Timestamp(t)
    if mode == "weekly":
        return (t.year, t.week)
    if mode == "monthly":
        return (t.year, t.month)
    if mode == "quarterly":
        return (t.year, (t.month - 1) // 3 + 1)
    return (t.year,)


def _redeem_rate(hold_days: int, ladder: List[Dict]) -> float:
    for step in ladder:
        if hold_days < step["hold_days"]:
            return float(step["rate"])
    return float(ladder[-1]["rate"])


def _date_to_days(date: str) -> int:
    return (pd.Timestamp(date) - pd.Timestamp("1970-01-01")).days


@dataclass
class BacktestResult:
    equity: pd.Series = field(default_factory=pd.Series)
    returns: pd.Series = field(default_factory=pd.Series)
    trades: pd.DataFrame = field(default_factory=pd.DataFrame)
    positions: pd.DataFrame = field(default_factory=pd.DataFrame)
    metrics: Dict = field(default_factory=dict)


def run_backtest(
    target_weights: pd.DataFrame,
    nav_map: Dict[str, pd.DataFrame],
    position_cfg: Dict,
    fee_cfg: Dict = None,
    forced_buys: pd.DataFrame = None,
) -> BacktestResult:
    fee = {**DEFAULT_FEE, **(fee_cfg or {})}
    purchase_rate = float(fee["purchase_rate"])
    redeem_ladder = fee["redeem_ladder"]
    entry_tranche_ratio = float(position_cfg.get("entry_tranche_ratio", 1.0))
    buy_mode = str(position_cfg.get("buy_mode", "固定金额"))
    buy_amount_fixed = float(position_cfg.get("buy_amount", 5000.0))
    buy_ratio = float(position_cfg.get("buy_ratio", entry_tranche_ratio))
    exit_mode = position_cfg.get("exit_mode", "all")
    exit_ratio = float(position_cfg.get("exit_ratio", 1.0))
    rebalance_days = int(position_cfg.get("rebalance_days", 1))
    rebalance_mode = position_cfg.get("rebalance_mode", "days")
    take_profit_step = position_cfg.get("take_profit_step")
    take_profit_ratio = float(position_cfg.get("take_profit_ratio", 0.5))
    trailing_stop = position_cfg.get("trailing_stop")
    initial_capital = float(position_cfg.get("initial_capital", 1_000_000.0))
    extra_amount = float(position_cfg.get("extra_contribution_amount", 0.0))
    extra_freq = str(position_cfg.get("extra_contribution_freq", "每年"))
    extra_mode = EXTRA_FREQ_MODES.get(extra_freq, "annual")

    funds = list(target_weights.columns)
    is_single_fund = len(funds) == 1
    navs = pd.DataFrame({f: nav_map[f]["adj_nav"] for f in funds})
    navs = navs.reindex(target_weights.index)

    # 信号 T-1 日计算，T 日净值成交，避免未来函数。
    target = target_weights.shift(1).fillna(0.0)
    if forced_buys is not None and not forced_buys.empty:
        forced = forced_buys.reindex(target_weights.index).fillna(0.0).shift(1).fillna(0.0)
    else:
        forced = None
    from strategies import compute_rebalance_mask

    rebalance_mask = compute_rebalance_mask(target.index, rebalance_mode, rebalance_days)

    cash = initial_capital
    contributed = initial_capital
    extra_count = 0
    last_extra_key = None
    cashflows = [(target.index[0], -initial_capital)]
    cash_ratios = []
    strategy_index = 100.0
    prev_value = initial_capital
    first_period = True
    lots: List[Dict] = []  # {fund, date, shares, cost_amount}
    peak = {f: None for f in funds}
    tp_ref = {f: None for f in funds}

    def shares_of(fund: str) -> float:
        return sum(lt["shares"] for lt in lots if lt["fund"] == fund)

    equity_rows = {}
    asset_rows = {}
    pos_rows = {}
    trade_rows: List[Dict] = []

    dates = list(target.index)
    for idx, t in enumerate(dates):
        nav_t = navs.loc[t]
        value_pre = cash + sum(
            lt["shares"] * nav_t[lt["fund"]] for lt in lots if lt["shares"] > 0
        )
        if first_period:
            first_period = False
        else:
            strategy_index *= (value_pre / prev_value) if prev_value > 0 else 1.0

        if extra_amount > 0:
            extra_key = _extra_period_key(t, extra_mode)
            if last_extra_key is not None and extra_key != last_extra_key:
                cash += extra_amount
                contributed += extra_amount
                extra_count += 1
                cashflows.append((t, -extra_amount))
            last_extra_key = extra_key
        value = cash + sum(
            lt["shares"] * nav_t[lt["fund"]] for lt in lots if lt["shares"] > 0
        )
        cur_w = {
            f: (shares_of(f) * nav_t[f] / value if value > 0 else 0.0) for f in funds
        }
        des_w = {f: float(target.loc[t, f]) for f in funds}

        if rebalance_mask[idx]:
            for f in funds:
                if des_w[f] < cur_w[f] - 1e-8:
                    cur_shares = shares_of(f)
                    if cur_shares <= 0:
                        continue
                    if exit_mode == "partial":
                        sell_shares = cur_shares * exit_ratio
                    else:
                        target_value = des_w[f] * value
                        sell_shares = max(0.0, cur_shares - target_value / nav_t[f])
                    if sell_shares <= 0:
                        continue
                    sell_shares = min(sell_shares, cur_shares)
                    cash, pnl, fee_total = _sell_fifo(
                        lots, f, sell_shares, nav_t[f], t, redeem_ladder, cash
                    )
                    trade_rows.append(
                        {
                            "date": t,
                            "fund": f,
                            "side": "sell",
                            "amount": sell_shares * nav_t[f],
                            "fee": fee_total,
                            "pnl": pnl,
                        }
                    )

            for f in funds:
                if des_w[f] > cur_w[f] + 1e-8:
                    gap = des_w[f] - cur_w[f]
                    if is_single_fund:
                        per_buy = buy_amount_fixed if buy_mode in ("固定金额", "fixed") else buy_ratio * value
                    else:
                        per_buy = entry_tranche_ratio * value
                    buy_amount = min(per_buy, gap * value)
                    buy_amount = min(buy_amount, cash)
                    if buy_amount <= 0:
                        continue
                    net = buy_amount / (1.0 + purchase_rate)
                    fee_cost = buy_amount - net
                    shares_bought = net / nav_t[f]
                    cash -= buy_amount
                    lots.append(
                        {
                            "fund": f,
                            "date": t,
                            "shares": shares_bought,
                            "cost_amount": net,
                        }
                    )
                    trade_rows.append(
                        {
                            "date": t,
                            "fund": f,
                            "side": "buy",
                            "amount": buy_amount,
                            "fee": fee_cost,
                            "pnl": 0.0,
                        }
                    )

        if forced is not None:
            for f in funds:
                frac = float(forced.loc[t, f]) if f in forced.columns else 0.0
                if frac <= 0:
                    continue
                per_buy = buy_amount_fixed if buy_mode in ("固定金额", "fixed") else buy_ratio * value
                buy_amount = min(per_buy, cash)
                if buy_amount <= 0:
                    continue
                net = buy_amount / (1.0 + purchase_rate)
                fee_cost = buy_amount - net
                shares_bought = net / nav_t[f]
                cash -= buy_amount
                lots.append(
                    {
                        "fund": f,
                        "date": t,
                        "shares": shares_bought,
                        "cost_amount": net,
                    }
                )
                trade_rows.append(
                    {
                        "date": t,
                        "fund": f,
                        "side": "buy",
                        "amount": buy_amount,
                        "fee": fee_cost,
                        "pnl": 0.0,
                        "forced": 1,
                    }
                )

        if take_profit_step is not None:
            for f in funds:
                cur_shares = shares_of(f)
                if cur_shares <= 0:
                    tp_ref[f] = None
                    continue
                cost = sum(
                    lt["cost_amount"]
                    for lt in lots
                    if lt["fund"] == f and lt["shares"] > 0
                )
                if cost <= 0:
                    continue
                avg_entry = cost / cur_shares
                # 止盈参考价：首次建仓取平均成本，触发止盈后重置为当日净值，
                # 避免同一波上涨被连续每日“减半”卖出。
                if tp_ref[f] is None:
                    tp_ref[f] = avg_entry
                if nav_t[f] / tp_ref[f] - 1.0 >= take_profit_step:
                    sell_shares = cur_shares * take_profit_ratio
                    if sell_shares <= 0:
                        continue
                    cash, pnl, fee_total = _sell_fifo(
                        lots, f, sell_shares, nav_t[f], t, redeem_ladder, cash
                    )
                    trade_rows.append(
                        {
                            "date": t,
                            "fund": f,
                            "side": "sell",
                            "amount": sell_shares * nav_t[f],
                            "fee": fee_total,
                            "pnl": pnl,
                        }
                    )
                    tp_ref[f] = nav_t[f]

        if trailing_stop:
            for f in funds:
                cur_shares = shares_of(f)
                if cur_shares <= 0:
                    peak[f] = None
                    continue
                nav_f = nav_t[f]
                if peak[f] is None or nav_f > peak[f]:
                    peak[f] = nav_f
                if nav_f / peak[f] - 1.0 <= -trailing_stop:
                    cash, pnl, fee_total = _sell_fifo(
                        lots, f, cur_shares, nav_f, t, redeem_ladder, cash
                    )
                    trade_rows.append(
                        {
                            "date": t,
                            "fund": f,
                            "side": "sell",
                            "amount": cur_shares * nav_f,
                            "fee": fee_total,
                            "pnl": pnl,
                        }
                    )
                    peak[f] = None

        nav_value = cash + sum(
            lt["shares"] * nav_t[lt["fund"]] for lt in lots if lt["shares"] > 0
        )
        cash_ratios.append(cash / nav_value if nav_value > 0 else 1.0)
        equity_rows[t] = strategy_index
        asset_rows[t] = nav_value
        pos_rows[t] = {
            f: (shares_of(f) * nav_t[f] / nav_value if nav_value > 0 else 0.0)
            for f in funds
        }
        prev_value = nav_value

    equity = pd.Series(equity_rows)
    returns = equity.pct_change().fillna(0.0)
    positions = pd.DataFrame(pos_rows).T
    trades = pd.DataFrame(trade_rows)

    from metrics import max_drawdown, sharpe, xirr

    final_asset = float(pd.Series(asset_rows).iloc[-1]) if asset_rows else initial_capital
    cashflows.append((equity.index[-1], final_asset))
    mdd = max_drawdown(equity)
    xirr_value = xirr(cashflows)
    avg_cash = float(pd.Series(cash_ratios).mean()) if cash_ratios else 0.0
    end_cash = float(cash_ratios[-1]) if cash_ratios else 0.0
    profit = final_asset - contributed

    # 买入持有基准：只使用初始资金做一次性满仓买入，不把定期新增资金算进基准。
    if len(funds) == 1:
        bench_nav = navs[funds[0]]
    else:
        bench_nav = navs.mean(axis=1)
    bench_nav = bench_nav.reindex(equity.index).ffill().bfill()
    initial_cash = -float(cashflows[0][1])
    bench_start = float(bench_nav.iloc[0])
    bench_end = float(bench_nav.iloc[-1])
    bench_shares = initial_cash / bench_start if bench_start > 0 else 0.0
    bench_final = bench_shares * bench_end
    bench_xirr = xirr(
        [(bench_nav.index[0], -initial_cash), (bench_nav.index[-1], bench_final)]
    )

    pos_sum = positions.sum(axis=1)
    streak = 0
    best = 0
    for v in pos_sum:
        if v <= 1e-9:
            streak += 1
            if streak > best:
                best = streak
        else:
            streak = 0
    metrics = {
        "回测区间": "%s ~ %s" % (
            pd.to_datetime(equity.index[0]).date(),
            pd.to_datetime(equity.index[-1]).date(),
        ),
        "XIRR": xirr_value,
        "最大回撤": mdd,
        "夏普比率": sharpe(returns),
        "期末资产": final_asset,
        "累计投入": contributed,
        "累计盈利": profit,
        "平均现金占比": avg_cash,
        "期末现金占比": end_cash,
        "最长空仓天数": best,
        "交易次数": int(len(trades)),
        "基准XIRR": bench_xirr,
        "超额收益": xirr_value - bench_xirr,
    }
    sell_trades = trades[trades["side"] == "sell"] if not trades.empty else trades
    if not sell_trades.empty and "pnl" in sell_trades.columns:
        metrics["胜率"] = float((sell_trades["pnl"] > 0).mean())
    else:
        metrics["胜率"] = 0.0
    if trades.empty:
        metrics["申购周数"] = 0
        metrics["赎回周数"] = 0
    else:
        cal = pd.to_datetime(trades["date"]).dt.isocalendar()
        weekkey = cal["year"].astype(str) + "-" + cal["week"].astype(str)
        metrics["申购周数"] = int(weekkey[trades["side"] == "buy"].nunique())
        metrics["赎回周数"] = int(weekkey[trades["side"] == "sell"].nunique())

    return BacktestResult(
        equity=equity,
        returns=returns,
        trades=trades,
        positions=positions,
        metrics=metrics,
    )


def _sell_fifo(lots, fund, sell_shares, nav, date, ladder, cash):
    """按 FIFO 卖出份额，返回 (更新后 cash, 本次实现盈亏, 本次赎回费)。"""
    remaining = sell_shares
    pnl = 0.0
    fee_total = 0.0
    for lt in lots:
        if lt["fund"] != fund or lt["shares"] <= 0:
            continue
        take = min(remaining, lt["shares"])
        hold_days = _date_to_days(date) - _date_to_days(lt["date"])
        rate = _redeem_rate(hold_days, ladder)
        gross = take * nav
        fee = gross * rate
        net = gross - fee
        fee_total += fee
        cost_share = lt["cost_amount"] / lt["shares"] if lt["shares"] > 0 else 0.0
        pnl += net - cost_share * take
        cash += net
        lt["shares"] -= take
        lt["cost_amount"] -= cost_share * take
        remaining -= take
        if remaining <= 0:
            break
    return cash, pnl, fee_total

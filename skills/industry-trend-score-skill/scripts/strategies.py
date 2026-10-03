"""策略定义与目标仓位计算。

两类策略统一输出一个「每日目标仓位」DataFrame：
- 单基金择时：单列，目标权重 0/1（是否持有）。
- 行业轮动：多列，每个行业的目标权重（Top K 等权）。
回测引擎只消费这个目标仓位，再叠加分批建仓 / 分批止盈 / 费率。
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

import numpy as np
import pandas as pd


WEIGHT_SCHEME_LABELS = {
    "equal": "等权",
    "rank": "排名加权",
    "score": "评分加权",
    "vol": "风险平价",
    "score_vol": "评分·波动率",
}


def _trend_ribbon(nav, fast_windows, slow_windows):
    fast = pd.DataFrame({f"f{w}": nav.rolling(w).mean() for w in fast_windows})
    slow = pd.DataFrame({f"s{w}": nav.rolling(w).mean() for w in slow_windows})
    return (
        (fast.gt(nav, axis=0) & fast.gt(slow.min(axis=1), axis=0))
        .all(axis=1)
        .astype(float)
    )


def _ma_slope(nav, window, slope_window):
    ma = nav.rolling(window).mean()
    return ma.pct_change(slope_window)


def _bollinger_state(nav, window, num_std):
    ma = nav.rolling(window).mean()
    std = nav.rolling(window).std(ddof=0)
    upper = ma + num_std * std
    lower = ma - num_std * std
    percent_b = (nav - lower) / (upper - lower).replace(0, np.nan)
    return pd.DataFrame({"lower": lower, "upper": upper, "percent_b": percent_b})


def _rolling_percentile(nav, window):
    return nav.rolling(window).apply(lambda x: (x[-1] >= x).mean(), raw=True)


def _drawdown_from_peak(nav):
    peak = nav.rolling(len(nav), min_periods=1).max()
    return nav / peak - 1.0


def _rsi_slope(rsi, window):
    return rsi.diff(window)


def _single_fund_target(df: pd.DataFrame, cfg: Dict, market: pd.Series | None = None) -> pd.Series:
    nav = df["adj_nav"]
    signal = cfg.get("signal", "valuation")
    out = pd.Series(0.0, index=df.index)

    if signal == "valuation":
        buy = cfg.get("buy_threshold", 30)
        sell = cfg.get("sell_threshold", 70)
        pct = df["pe_ttm_5y_pct"]
        state = 0
        for i in range(len(df)):
            p = pct.iloc[i]
            if pd.isna(p):
                out.iloc[i] = state
                continue
            if p < buy:
                state = 1
            elif p > sell:
                state = 0
            out.iloc[i] = state

    elif signal == "ma_trend":
        ma_fast = nav.rolling(cfg.get("ma_fast", 20)).mean()
        ma_slow = nav.rolling(cfg.get("ma_slow", 60)).mean()
        out = (ma_fast > ma_slow).astype(float).fillna(0.0)

    elif signal == "valuation_momentum":
        buy = cfg.get("buy_threshold", 30)
        sell = cfg.get("sell_threshold", 70)
        ma20 = nav.rolling(20).mean()
        pct = df["pe_ttm_5y_pct"]
        hold = (pct < buy) & (nav > ma20)
        exit_ = (pct > sell) | (nav < ma20)
        state = 0
        for i in range(len(df)):
            if bool(hold.iloc[i]):
                state = 1
            if bool(exit_.iloc[i]):
                state = 0
            out.iloc[i] = state

    elif signal == "momentum":
        lookback = cfg.get("lookback", 60)
        out = (nav / nav.shift(lookback) - 1.0 > 0).astype(float).fillna(0.0)

    elif signal == "ma_price":
        n = cfg.get("ma", 60)
        out = (nav > nav.rolling(n).mean()).astype(float).fillna(0.0)

    elif signal == "hold":
        out = pd.Series(1.0, index=df.index)

    elif signal == "rsi":
        buy = cfg.get("buy_threshold", 30)
        sell = cfg.get("sell_threshold", 70)
        rsi = df["rsi_pct"]
        state = 0
        for i in range(len(df)):
            r = rsi.iloc[i]
            if pd.isna(r):
                out.iloc[i] = state
                continue
            if r < buy:
                state = 1
            elif r > sell:
                state = 0
            out.iloc[i] = state

    elif signal == "donchian":
        threshold = cfg.get("threshold", 0)
        out = (df["donchian_channel"] > threshold).astype(float).fillna(0.0)

    elif signal == "trend_ribbon":
        fast = cfg.get("ma_fast", 20)
        slow = cfg.get("ma_slow", 120)
        out = _trend_ribbon(nav, [fast], [slow])

    elif signal == "trend_slope":
        n = cfg.get("ma", 60)
        slope_window = cfg.get("slope_window", 5)
        price_ok = (nav > nav.rolling(n).mean()).astype(float)
        slope_ok = (_ma_slope(nav, n, slope_window) > 0).astype(float)
        out = (price_ok * slope_ok).fillna(0.0)

    elif signal == "donchian_trend":
        threshold = cfg.get("threshold", 0.0)
        out = ((df.get("donchian_channel", 0.0) > threshold)).astype(float).fillna(0.0)

    elif signal == "vol_scaled_momentum":
        lookback = cfg.get("lookback", 120)
        vol_window = cfg.get("vol_window", 20)
        mom = nav.pct_change(lookback)
        vol = nav.pct_change().rolling(vol_window).std(ddof=0)
        raw = mom / vol.replace(0, np.nan)
        out = (raw > cfg.get("momentum_threshold", 0.0)).astype(float).fillna(0.0)

    elif signal == "rsi_reversal":
        rsi = df["rsi_pct"]
        low = cfg.get("rsi_low", 35)
        high = cfg.get("rsi_high", 65)
        rising = _rsi_slope(rsi, cfg.get("rsi_slope_window", 3)) > 0
        state = 0
        for i in range(len(df)):
            r = rsi.iloc[i]
            if pd.isna(r):
                out.iloc[i] = state
            elif r < low and bool(rising.iloc[i]):
                state = 1
            elif r > high:
                state = 0
            out.iloc[i] = state

    elif signal == "bollinger_mean_reversion":
        bb = _bollinger_state(nav, cfg.get("bb_window", 20), cfg.get("bb_std", 2.0))
        buy = bb["percent_b"] < cfg.get("buy_pct", 0.0)
        sell = bb["percent_b"] > cfg.get("sell_pct", 0.8)
        state = 0
        for i in range(len(df)):
            if bool(buy.iloc[i]):
                state = 1
            if bool(sell.iloc[i]):
                state = 0
            out.iloc[i] = state

    elif signal == "price_percentile":
        pct = _rolling_percentile(nav, cfg.get("window", 60))
        buy = cfg.get("buy_pct", 0.2)
        sell = cfg.get("sell_pct", 0.8)
        state = 0
        for i in range(len(df)):
            p = pct.iloc[i]
            if pd.isna(p):
                out.iloc[i] = state
            elif p < buy:
                state = 1
            elif p > sell:
                state = 0
            out.iloc[i] = state

    elif signal == "drawdown_reversal":
        dd = _drawdown_from_peak(nav)
        rsi = df["rsi_pct"]
        threshold = cfg.get("dd_threshold", 0.15)
        rising = _rsi_slope(rsi, cfg.get("rsi_slope_window", 3)) > 0
        state = 0
        for i in range(len(df)):
            if bool(dd.iloc[i] <= -threshold and rising.iloc[i]):
                state = 1
            elif bool(dd.iloc[i] > -cfg.get("recover_threshold", 0.03)):
                state = 0
            out.iloc[i] = state

    else:
        raise ValueError(f"unknown single-fund signal: {signal}")

    if market is not None and cfg.get("market_filter"):
        mkt_ok = (market > market.rolling(cfg.get("market_ma", 200)).mean()).reindex(df.index).ffill().fillna(False).astype(bool)
        out = out.where(mkt_ok, 0.0)
    if cfg.get("max_empty"):
        mode, days, periods = _max_empty_limits(cfg)
        if mode == "target" and (days > 0 or periods > 0):
            rb = compute_rebalance_mask(
                df.index, cfg.get("rebalance_mode", "days"), cfg.get("rebalance_days", 20)
            )
            for i in _empty_trigger_positions((out == 0).tolist(), cfg, rb):
                out.iloc[i] = 1.0
                j = i + 1
                while j < len(df) and not rb[j]:
                    out.iloc[j] = 1.0
                    j += 1
    return out


def _compute_weights(scores: pd.Series, vols: pd.Series, scheme: str) -> dict:
    n = len(scores)
    if n == 0:
        return {}
    if scheme == "equal":
        return {nm: 1.0 / n for nm in scores.index}
    if scheme == "rank":
        ranks = scores.rank(ascending=False, method="first")
        w = (n + 1 - ranks).astype(float)
        return (w / w.sum()).to_dict()
    if scheme == "score":
        s = scores - scores.min()
        if s.sum() <= 0:
            return {nm: 1.0 / n for nm in scores.index}
        return (s / s.sum()).to_dict()
    if scheme == "vol":
        inv = 1.0 / vols.replace(0, np.nan)
        inv = inv.fillna(0.0)
        if inv.sum() <= 0:
            return {nm: 1.0 / n for nm in scores.index}
        return (inv / inv.sum()).to_dict()
    if scheme == "score_vol":
        s = (scores - scores.min()).clip(lower=0.0)
        inv = 1.0 / vols.replace(0, np.nan).fillna(1e9)
        sw = s * inv
        if sw.sum() <= 0:
            return {nm: 1.0 / n for nm in scores.index}
        return (sw / sw.sum()).to_dict()
    raise ValueError(f"unknown weight_scheme: {scheme}")


def zcross(x: pd.DataFrame) -> pd.DataFrame:
    """按行（每个交易日）做截面 z-score，用于跨行业打分。"""
    return x.sub(x.mean(axis=1), axis=0).div(x.std(axis=1), axis=0)


def compute_rebalance_mask(index, mode: str = "days", days: int = 20) -> list:
    """返回与 index 等长的布尔列表，标记调仓日。

    mode: days（每 N 个交易日）/ weekly（每 5 个交易日）/ monthly（每月首个交易日）/
          semimonthly（每月首个交易日 + 每月 15 日后的首个交易日）/
          quarterly（每季首个交易日）。
    """
    n = len(index)
    mask = [False] * n
    if mode == "days":
        mask = [i % days == 0 for i in range(n)]
    elif mode == "weekly":
        mask = [i % 5 == 0 for i in range(n)]
    elif mode == "monthly":
        ym = pd.to_datetime(index).strftime("%Y-%m")
        mask = [i == 0 or ym[i] != ym[i - 1] for i in range(n)]
    elif mode == "semimonthly":
        dt = pd.to_datetime(index)
        ym = dt.strftime("%Y-%m")
        half = (dt.day > 15).astype(str)
        key = (ym + "-" + half).tolist()
        mask = [i == 0 or key[i] != key[i - 1] for i in range(n)]
    elif mode == "quarterly":
        dt = pd.to_datetime(index)
        key = [(t.year, (t.month - 1) // 3) for t in dt]
        mask = [i == 0 or key[i] != key[i - 1] for i in range(n)]
    else:
        raise ValueError(f"unknown rebalance_mode: {mode}")
    return mask


def _max_empty_limits(cfg):
    me = cfg.get("max_empty") or {}
    mode = me.get("mode", "target")
    days = int(me.get("days", 0) or 0)
    periods = int(me.get("periods", 0) or 0)
    return mode, days, periods


def _empty_trigger_positions(empty_flags, cfg, rebalance_flags=None):
    mode, days, periods = _max_empty_limits(cfg)
    out = []
    if periods > 0 and rebalance_flags is not None:
        streak = 0
        for i, empty in enumerate(empty_flags):
            if not rebalance_flags[i]:
                continue
            if empty:
                streak += 1
                if streak >= periods:
                    out.append(i)
                    streak = 0
            else:
                streak = 0
    else:
        streak = 0
        for i, empty in enumerate(empty_flags):
            if empty:
                streak += 1
                if days > 0 and streak >= days:
                    out.append(i)
                    streak = 0
            else:
                streak = 0
    return out


def build_forced_buys(cfg, data_map, market=None):
    """tranche 模式的强制买入日期（每天买入一份的占位 1.0）。"""
    category = cfg.get("category", "single_fund_timing")
    if category != "single_fund_timing":
        return pd.DataFrame()
    mode, days, periods = _max_empty_limits(cfg)
    if mode != "tranche" or (days <= 0 and periods <= 0):
        return pd.DataFrame()
    name = cfg["fund_pool"][0]
    df = data_map[name]
    target = _single_fund_target(df, cfg, market)
    rb = compute_rebalance_mask(
        df.index, cfg.get("rebalance_mode", "days"), cfg.get("rebalance_days", 20)
    )
    idx = [
        df.index[i]
        for i in _empty_trigger_positions((target == 0).tolist(), cfg, rb)
    ]
    if not idx:
        return pd.DataFrame()
    return pd.DataFrame(1.0, index=idx, columns=[name])


def _rotation_target(data_map: Dict[str, pd.DataFrame], cfg: Dict, market: pd.Series | None = None) -> pd.DataFrame:
    names = list(cfg["fund_pool"])
    lookback = cfg.get("lookback", 20)
    top_k = cfg.get("top_k", 3)
    rebalance_days = cfg.get("rebalance_days", 20)
    signal = cfg.get("signal", "momentum")
    weight_scheme = cfg.get("weight_scheme", "equal")
    rebalance_mode = cfg.get("rebalance_mode", "days")

    nav_df = pd.DataFrame({n: data_map[n]["adj_nav"] for n in names})
    pe_df = pd.DataFrame({
        n: data_map[n].get(
            "pe_ttm_5y_pct",
            pd.Series(np.nan, index=data_map[n].index),
        )
        for n in names
    })
    first = nav_df.bfill().iloc[0]
    mom = nav_df / nav_df.shift(lookback).fillna(first) - 1.0
    vol_df = nav_df.pct_change().rolling(cfg.get("vol_window", 20)).std()
    rsi_df = pd.DataFrame({n: data_map[n].get("rsi_pct", np.nan) for n in names})

    if signal == "momentum":
        score = mom
    elif signal == "valuation":
        mv = cfg.get("valuation_momentum_weight", 0.5)
        score = zcross(-pe_df) + mv * zcross(mom)
    elif signal == "rsi":
        score = -rsi_df.shift(cfg.get("rsi_lag", 5))
    elif signal == "equal":
        target = pd.DataFrame(np.nan, index=nav_df.index, columns=names)
        mask = compute_rebalance_mask(nav_df.index, rebalance_mode, rebalance_days)
        for i in range(len(nav_df)):
            if not mask[i]:
                continue
            target.iloc[i, :] = 0.0
            scores = mom.iloc[i]
            vols = vol_df.loc[vol_df.index[i], names]
            weights = _compute_weights(scores, vols, weight_scheme)
            for nm, w in weights.items():
                target.loc[target.index[i], nm] = w
        target = target.ffill().fillna(0.0)
        if market is not None and cfg.get("market_filter"):
            mkt_ok = (market > market.rolling(cfg.get("market_ma", 200)).mean()).reindex(target.index).ffill().fillna(False).astype(bool)
            target = target.where(mkt_ok, 0.0)
        return target
    elif signal == "score":
        params = cfg.get("params") or {}
        wm = float(cfg.get("momentum_weight", params.get("momentum_weight", 0.5)))
        wv = float(cfg.get("valuation_weight", params.get("valuation_weight", 0.5)))
        if wm + wv <= 0:
            ratio = 0.5
        else:
            ratio = wm / (wm + wv)
        # 避免权重退化为单因子打分，保留两个因子都参与。
        ratio = min(max(ratio, 0.1), 0.9)
        score = ratio * zcross(mom) + (1.0 - ratio) * zcross(-pe_df)
    elif signal == "trend_score":
        ma_fast = cfg.get("ma_fast", 20)
        ma_slow = cfg.get("ma_slow", 60)
        trend = pd.DataFrame({
            n: (data_map[n]["adj_nav"].rolling(ma_fast).mean()
                - data_map[n]["adj_nav"].rolling(ma_slow).mean())
            for n in names
        })
        score = zcross(trend) + zcross(mom)
    elif signal == "momentum_vol":
        vol_window = cfg.get("vol_window", 20)
        vol = nav_df.pct_change().rolling(vol_window).std(ddof=0).replace(0, np.nan)
        score = zcross(mom / vol)
    elif signal == "donchian_rotation":
        channel = pd.DataFrame({
            n: data_map[n].get(
                "donchian_channel",
                pd.Series(np.nan, index=data_map[n].index),
            )
            for n in names
        })
        score = zcross(channel.fillna(0.0))
    elif signal == "relative_strength_rotation":
        ma = cfg.get("ma", 60)
        abs_ok = pd.DataFrame({
            n: data_map[n]["adj_nav"] > data_map[n]["adj_nav"].rolling(ma).mean()
            for n in names
        })
        score = zcross(mom).where(abs_ok, -np.inf)
    elif signal == "rsi_reversal_rotation":
        lag = cfg.get("rsi_lag", 5)
        slope = rsi_df.diff(lag)
        score = zcross(-rsi_df) + zcross(slope)
    elif signal == "mean_reversion_rotation":
        window = cfg.get("window", 60)
        pct = pd.DataFrame({
            n: _rolling_percentile(nav_df[n], window)
            for n in names
        })
        gate = (mom > 0).astype(float)
        score = -zcross(pct) + cfg.get("momentum_gate", 0.5) * gate
    elif signal == "drawdown_rotation":
        dd = nav_df.apply(lambda c: c / c.expanding().max() - 1.0)
        score = -zcross(dd) + cfg.get("reversal_weight", 0.5) * zcross(rsi_df.diff(cfg.get("rsi_lag", 5)))
    else:
        raise ValueError(f"unknown rotation signal: {signal}")

    if cfg.get("vol_filter"):
        vol_rank = vol_df.rank(axis=1, pct=True)
        score = score.where(vol_rank <= cfg.get("vol_threshold", 0.8))

    target = pd.DataFrame(np.nan, index=nav_df.index, columns=names)
    mask = compute_rebalance_mask(nav_df.index, rebalance_mode, rebalance_days)
    for i in range(len(nav_df)):
        if not mask[i]:
            continue
        row = score.iloc[i].dropna()
        if row.empty:
            continue
        top = row.sort_values(ascending=False).head(top_k)
        if top.empty:
            continue
        target.iloc[i, :] = 0.0
        weights = _compute_weights(top, vol_df.loc[vol_df.index[i], top.index], weight_scheme)
        for nm, w in weights.items():
            target.loc[target.index[i], nm] = w

    target = target.ffill().fillna(0.0)

    # 市场趋势过滤：大盘指数在 MA 之下时整体空仓
    if market is not None and cfg.get("market_filter"):
        mkt_ok = (market > market.rolling(cfg.get("market_ma", 200)).mean()).reindex(target.index).ffill().fillna(False).astype(bool)
        target = target.where(mkt_ok, 0.0)

    # 大盘回撤止损：指数从 250 日高点回撤超过阈值时整体空仓。
    market_dd_stop = cfg.get("market_dd_stop")
    if market is not None and market_dd_stop:
        peak = market.rolling(250, min_periods=1).max()
        dd = (market / peak - 1.0).reindex(target.index).ffill()
        target = target.where(dd > -float(market_dd_stop), 0.0)

    if cfg.get("max_empty"):
        mode, days, periods = _max_empty_limits(cfg)
        if mode == "target" and (days > 0 or periods > 0):
            rb = compute_rebalance_mask(
                target.index,
                cfg.get("rebalance_mode", "days"),
                cfg.get("rebalance_days", 20),
            )
            empty = (target.sum(axis=1) <= 0).tolist()
            for i in _empty_trigger_positions(empty, cfg, rb):
                row = score.iloc[i].dropna()
                if row.empty:
                    continue
                top = row.sort_values(ascending=False).head(cfg.get("top_k", 3))
                if top.empty:
                    continue
                weights = _compute_weights(
                    top,
                    vol_df.loc[vol_df.index[i], top.index],
                    cfg.get("weight_scheme", "equal"),
                )
                target.iloc[i, :] = 0.0
                for nm, w in weights.items():
                    target.loc[target.index[i], nm] = w
                j = i + 1
                while j < len(target) and not rb[j]:
                    target.iloc[j, :] = target.iloc[i, :]
                    j += 1
    return target


def load_preset(path=None):
    p = Path(path) if path else Path(__file__).resolve().parents[1] / "config" / "strategies_preset.json"
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def expand_single_fund_strategies(preset: Dict) -> List[Dict]:
    out = []
    for idea in preset.get("ideas", []):
        for s in idea.get("strategies", []):
            if s.get("category") != "single_fund_timing":
                continue
            for fund in s.get("funds", []):
                cfg = {
                    "category": "single_fund_timing",
                    "fund": fund,
                    "fund_pool": [fund],
                    "strategy_id": s["strategy_id"],
                    "name": s["name"],
                    "signal": s.get("signal", ""),
                    "idea": idea["idea"],
                    "idea_id": idea["idea_id"],
                    "description": idea.get("description", ""),
                    "explanation": s.get("explanation", {}),
                    "tunable_params": s.get("tunable_params", []),
                    "max_empty": dict(s.get("max_empty", {})),
                    "fund_overrides": s.get("fund_overrides", {}),
                }
                cfg.update(s.get("default_params", {}))
                cfg.update(preset.get("cashflow", {}) or {})
                cfg.update(s.get("cashflow") or {})
                cfg.update(s.get("fund_overrides", {}).get(fund, {}))
                cfg["fund_params"] = preset.get("fund_params") or s.get("fund_params") or []
                for p in s.get("tunable_params", []):
                    cfg.setdefault(p["key"], p.get("default"))
                out.append(cfg)
    return out


def expand_rotation_strategies(preset: Dict) -> List[Dict]:
    out = []
    for idea in preset.get("ideas", []):
        for s in idea.get("strategies", []):
            if s.get("category") != "industry_rotation":
                continue
            cfg = {
                "category": "industry_rotation",
                "strategy_id": s["strategy_id"],
                "name": s["name"],
                "signal": s.get("signal", ""),
                "idea": idea["idea"],
                "idea_id": idea["idea_id"],
                "description": idea.get("description", ""),
                "explanation": s.get("explanation", {}),
                "tunable_params": s.get("tunable_params", []),
                "max_empty": dict(s.get("max_empty", {})),
            }
            cfg.update(s.get("default_params", {}))
            cfg.update(preset.get("cashflow", {}) or {})
            cfg.update(s.get("cashflow") or {})
            base = preset.get("fund_params") or s.get("fund_params") or []
            rotation = preset.get("rotation_fund_params") or []
            cfg["fund_params"] = list(base) + list(rotation)
            out.append(cfg)
    return out


def flatten_preset(preset: Dict) -> Dict:
    return {
        "single_fund_timing": expand_single_fund_strategies(preset),
        "industry_rotation": expand_rotation_strategies(preset),
    }


def flatten_config(cfg: Dict) -> Dict:
    """兼容双层 preset 与单条策略配置。"""
    if "ideas" in cfg:
        return flatten_preset(cfg)
    category = cfg.get("category", "single_fund_timing")
    if category == "single_fund_timing":
        single = dict(cfg)
        single.update(cfg.get("position") or {})
        if "fund_pool" not in single:
            single["fund_pool"] = [single["fund"]]
        single.setdefault("fund", single["fund_pool"][0])
        return {"single_fund_timing": [single], "industry_rotation": []}
    rotation = dict(cfg)
    rotation.update(cfg.get("position") or {})
    return {"single_fund_timing": [], "industry_rotation": [rotation]}


def resolve_rotation_pool(cfg: Dict, all_names, available=None) -> list:
    """自定义轮动池优先；预设展开时才回退到全量行业。"""
    avail = set(available if available is not None else all_names)
    pool = [n for n in (cfg.get("fund_pool") or []) if n in avail]
    return pool or list(all_names)


def filter_pool_by_names(pool: Dict, names) -> Dict:
    """只保留 fund_pool 中出现的基金池条目，用于单策略 config 定向取数。"""
    want = set(names)
    return {
        cat: [it for it in items if it.get("subcategory") in want]
        for cat, items in pool.items()
        if any(it.get("subcategory") in want for it in items)
    }


def position_cfg(cfg: Dict) -> Dict:
    pos = dict(cfg.get("position") or {})
    return {
        "entry_tranche_ratio": pos.get("entry_tranche_ratio", cfg.get("entry_tranche_ratio", 1.0)),
        "buy_mode": pos.get("buy_mode", cfg.get("buy_mode", "固定金额")),
        "buy_amount": pos.get("buy_amount", cfg.get("buy_amount", 5000.0)),
        "buy_ratio": pos.get("buy_ratio", cfg.get("buy_ratio", cfg.get("entry_tranche_ratio", 0.25))),
        "exit_mode": pos.get("exit_mode", cfg.get("exit_mode", "all")),
        "exit_ratio": pos.get("exit_ratio", cfg.get("exit_ratio", 1.0)),
        "rebalance_days": pos.get("rebalance_days", cfg.get("rebalance_days", 5)),
        "rebalance_mode": pos.get("rebalance_mode", cfg.get("rebalance_mode", "weekly")),
        "take_profit_step": pos.get("take_profit_step", cfg.get("take_profit_step")),
        "take_profit_ratio": pos.get("take_profit_ratio", cfg.get("take_profit_ratio", 0.5)),
        "trailing_stop": pos.get("trailing_stop", cfg.get("trailing_stop")) or None,
        "initial_capital": cfg.get("initial_capital", 1_000_000.0),
        "extra_contribution_amount": cfg.get("extra_contribution_amount", 0.0),
        "extra_contribution_freq": cfg.get("extra_contribution_freq", "每年"),
    }


def build_target_weights(cfg: Dict, data_map: Dict[str, pd.DataFrame], market: pd.Series | None = None) -> pd.DataFrame:
    category = cfg.get("category", "single_fund_timing")
    if category == "single_fund_timing":
        name = cfg["fund_pool"][0]
        ser = _single_fund_target(data_map[name], cfg, market)
        return ser.to_frame(name)
    if category == "industry_rotation":
        return _rotation_target(data_map, cfg, market)
    raise ValueError(f"unknown category: {category}")


def explain_strategy(cfg) -> str:
    expl = cfg.get("explanation")
    if isinstance(expl, str):
        return expl
    expl = expl or {}
    idea = expl.get("idea") or cfg.get("idea", "")
    rules = expl.get("rules", "")
    position = expl.get("position", "")
    tunable = cfg.get("tunable_params", [])
    params = (
        "、".join(p.get("label", p.get("key", "")) for p in tunable)
        if tunable
        else "无（使用默认参数）"
    )
    lines = [
        "策略目的：%s" % idea,
        "怎么选行业：%s" % rules,
        "资金怎么分：%s" % position,
        "可以调整：%s" % params,
    ]
    fund_params = cfg.get("fund_params") or []
    if fund_params:
        fund_labels = "、".join(p.get("label", p.get("key", "")) for p in fund_params)
        lines.append("资金相关设置：%s" % fund_labels)
    return "\n".join(lines)


def _current_value(cfg, p):
    key = p["key"]
    if key == "max_empty_days":
        days = (cfg.get("max_empty") or {}).get("days")
        return p.get("default", 0) if days is None else days
    if key == "rebalance_interval":
        mode = cfg.get("rebalance_mode", "days")
        days = cfg.get("rebalance_days", 20)
        if mode == "monthly":
            return "每月"
        if mode == "weekly":
            return "每周"
        if mode == "semimonthly":
            return "每半月"
        if days == 1:
            return "每日"
        if days == 5:
            return "每周"
        if days == 10:
            return "每两周"
        return "每%d天" % days
    if key == "momentum_weight":
        return (cfg.get("params") or {}).get(
            "momentum_weight",
            cfg.get("momentum_weight", p.get("default", 0.5)),
        )
    if key == "valuation_weight":
        return (cfg.get("params") or {}).get(
            "valuation_weight",
            cfg.get("valuation_weight", p.get("default", 0.5)),
        )
    if key == "buy_mode":
        return cfg.get("buy_mode", p.get("default", "固定金额"))
    if key == "buy_ratio":
        return cfg.get("buy_ratio", cfg.get("entry_tranche_ratio", p.get("default", 0.25)))
    if key == "weight_scheme":
        raw = cfg.get("weight_scheme", p.get("default", "equal"))
        return WEIGHT_SCHEME_LABELS.get(raw, raw)
    if key == "fund_pool":
        return "、".join(cfg.get("fund_pool") or []) or p.get("default", "")
    return cfg.get(key, p.get("default", ""))


def format_tunable_params(cfg) -> str:
    parts = []
    for p in cfg.get("tunable_params", []):
        key = p["key"]
        label = p.get("label", key)
        current = _current_value(cfg, p)
        if "min" in p and "max" in p:
            rng = "%s~%s" % (p["min"], p["max"])
        elif "choices" in p:
            rng = "/".join(str(c) for c in p["choices"])
        else:
            rng = ""
        unit = p.get("unit", "")
        display = ("%s%%" % current) if unit == "%" else str(current)
        suffix = ("（范围 %s）" % rng) if rng else ""
        if unit and unit != "%":
            display = "%s%s" % (display, unit)
        parts.append("%s：%s%s" % (label, display, suffix))
    return "；".join(parts)

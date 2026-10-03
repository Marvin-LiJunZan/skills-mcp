"""端到端：取数 → 目标仓位 → 回测 → 指标 → 图表 → 汇总。"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(__file__))

import pandas as pd

from data_client import DataClient
from strategies import (
    build_forced_buys,
    build_target_weights,
    explain_strategy,
    filter_pool_by_names,
    flatten_config,
    format_tunable_params,
    position_cfg,
    resolve_rotation_pool,
)
from backtest import run_backtest
from metrics import analyze_metrics
from report import plot_backtest


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config"
REPORTS = ROOT / "reports"


def load_json(path: Path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def strategy_label(tpl: dict) -> str:
    """Use the user-facing Chinese name in reports while keeping config name ASCII."""
    return str(tpl.get("display_name") or tpl.get("name") or "策略")


def fetch_pool(client: DataClient, pool: dict, years: int = 5) -> dict:
    data_map = {}
    meta = {}
    for category, items in pool.items():
        for it in items:
            name = it["subcategory"]
            thscode = it["thscode"]
            print(f"fetch {category}/{name} {thscode} ...", flush=True)
            df = client.fetch_series(thscode, it.get("fund_type", "otc"), years=years)
            if df.empty:
                print(f"  WARN empty {thscode}")
                continue
            df = df.set_index("date")
            data_map[name] = df
            meta[name] = it
    return data_map, meta


def single_fund_benchmark(nav: pd.Series) -> pd.Series:
    return nav.dropna()


def rotation_benchmark(data_map: dict, names: list) -> pd.Series:
    navs = pd.DataFrame({n: data_map[n]["adj_nav"] for n in names})
    norm = navs.apply(lambda c: c / c.dropna().iloc[0])
    return norm.mean(axis=1)


def common_range(data_map: dict, names: list) -> tuple:
    lo = max(data_map[n].index.min() for n in names)
    hi = min(data_map[n].index.max() for n in names)
    return lo, hi


def save_trades(trades: pd.DataFrame, tag: str, strategy: str, out_dir=None) -> None:
    if trades is None or trades.empty:
        return
    t = trades.copy()
    t.insert(0, "策略", strategy)
    out_dir = out_dir or REPORTS
    out = out_dir / "trades" / f"{tag}_trades.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    t.to_csv(out, index=False, encoding="utf-8-sig")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", type=Path, default=CONFIG / "strategies_preset.json")
    ap.add_argument("--out-dir", type=Path, default=REPORTS)
    args = ap.parse_args()
    preset = load_json(args.config)
    flat = flatten_config(preset)
    if "ideas" not in preset:
        if preset.get("category") == "single_fund_timing" and preset.get("fund_thscode"):
            pool = {
                "宽基": [
                    {
                        "subcategory": preset["fund"],
                        "thscode": preset["fund_thscode"],
                        "fund_type": preset.get("fund_type", "otc"),
                    }
                ]
            }
        else:
            pool = load_json(CONFIG / "fund_pool.json")
            need = []
            for tpl in flat["single_fund_timing"]:
                need.extend(tpl.get("fund_pool") or [])
            for tpl in flat["industry_rotation"]:
                need.extend(tpl.get("fund_pool") or [])
            pool = filter_pool_by_names(pool, need)
    else:
        pool = load_json(CONFIG / "fund_pool.json")
    client = DataClient(skill_action="backtest")

    years = int((preset.get("cashflow") or {}).get("years") or preset.get("years") or 5)
    warmup_years = int(preset.get("warmup_years") or 0)
    fetch_years = max(years, warmup_years)
    data_map, meta = fetch_pool(client, pool, years=fetch_years)
    need_market = bool(flat["industry_rotation"]) or any(
        tpl.get("market_filter") or tpl.get("market_dd_stop")
        for tpl in flat["single_fund_timing"]
    )
    market = None
    if need_market:
        market = client.fetch_index("000300.SH", years=fetch_years).set_index("date")["close"]

    results = []

    for tpl in flat["single_fund_timing"]:
        name = tpl["fund"]
        if name not in data_map:
            continue
        cfg = dict(tpl)
        cfg["fund_pool"] = [name]
        print("\n" + "=" * 60)
        label = strategy_label(tpl)
        print(label + " · " + name)
        print(explain_strategy(cfg))
        print(format_tunable_params(cfg))
        try:
            target = build_target_weights(cfg, data_map, market)
            forced = build_forced_buys(cfg, data_map, market)
            pos_cfg = position_cfg(tpl)
            res = run_backtest(target, data_map, pos_cfg, fee_cfg=tpl.get("fee"), forced_buys=forced)
            analysis, advice = analyze_metrics(res.metrics)
            print("分析：" + analysis)
            print("修改建议：" + advice)
            benchmark = single_fund_benchmark(data_map[name]["adj_nav"])
            title = f"{name} · {label}"
            png = plot_backtest(
                res.equity,
                benchmark,
                res.metrics,
                title,
                args.out_dir / f"{name}_{label}.png",
                trades=res.trades,
                show_trade_markers=True,
            )
            save_trades(res.trades, f"{name}_{label}", title, args.out_dir)
            results.append(
                {
                    "类别": "单基金择时",
                    "理念": tpl.get("idea", ""),
                    "基金": name,
                    "策略": label,
                    "规则摘要": (tpl.get("explanation") or {}).get("rules", ""),
                    "可调参数": format_tunable_params(cfg),
                    "分析": analysis,
                    "修改建议": advice,
                    **{k: v for k, v in res.metrics.items() if k != "交易次数"},
                    "交易次数": res.metrics["交易次数"],
                    "图": png.name,
                }
            )
        except Exception as exc:
            print(f"ERROR single {name}/{label}: {exc}")

    # 行业轮动
    ind_names = [it["subcategory"] for it in pool.get("行业", []) if it["subcategory"] in data_map]
    if len(ind_names) >= 3:
        for tpl in flat["industry_rotation"]:
            cfg = dict(tpl)
            cfg["fund_pool"] = resolve_rotation_pool(cfg, ind_names, ind_names)
            pool_names = cfg["fund_pool"]
            lo, hi = common_range(data_map, pool_names)
            rot_data_map = {
                n: data_map[n].loc[lo:hi].copy()
                for n in pool_names
            }
            print("\n" + "=" * 60)
            label = strategy_label(tpl)
            print(label)
            print(explain_strategy(cfg))
            print(format_tunable_params(cfg))
            try:
                target = build_target_weights(cfg, rot_data_map, market)
                if warmup_years > years:
                    backtest_start = pd.Timestamp(hi) - pd.DateOffset(years=years)
                    target = target.loc[backtest_start:hi]
                    rot_data_map = {
                        n: df.loc[backtest_start:hi].copy()
                        for n, df in rot_data_map.items()
                    }
                forced = build_forced_buys(cfg, rot_data_map, market)
                pos_cfg = position_cfg(tpl)
                res = run_backtest(target, rot_data_map, pos_cfg, fee_cfg=tpl.get("fee"), forced_buys=forced)
                analysis, advice = analyze_metrics(res.metrics)
                print("分析：" + analysis)
                print("修改建议：" + advice)
                benchmark = market
                title = f"行业轮动 · {label}"
                png = plot_backtest(
                    res.equity,
                    benchmark,
                    res.metrics,
                    title,
                args.out_dir / f"轮动_{label}.png",
                trades=res.trades,
                show_trade_markers=False,
                benchmark_label="基准（沪深300买入持有）",
            )
                save_trades(res.trades, f"轮动_{label}", title, args.out_dir)
                results.append(
                    {
                        "类别": "行业轮动",
                        "理念": tpl.get("idea", ""),
                        "基金": "/".join(pool_names),
                        "策略": label,
                        "规则摘要": (tpl.get("explanation") or {}).get("rules", ""),
                        "可调参数": format_tunable_params(cfg),
                        "分析": analysis,
                        "修改建议": advice,
                        **{k: v for k, v in res.metrics.items() if k != "交易次数"},
                        "交易次数": res.metrics["交易次数"],
                        "图": png.name,
                    }
                )
            except Exception as exc:
                print(f"ERROR rotation {label}: {exc}")

    df = pd.DataFrame(results)
    if df.empty:
        print("no results")
        return

    sort_cols = ["类别", "XIRR"]
    df = df.sort_values(sort_cols, ascending=[True, False])
    display_names = {
        "XIRR": "按实际投入节奏折算的年化收益率",
        "基准XIRR": "一直持有基准的年化收益率",
        "超额收益": "比一直持有多赚/少赚",
    }
    display_df = df.rename(columns=display_names)
    out_csv = args.out_dir / "summary.csv"
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    display_df.to_csv(out_csv, index=False, encoding="utf-8-sig")

    print("\n===== 回测汇总 =====")
    show_cols = ["类别", "理念", "基金", "策略", "回测区间", "按实际投入节奏折算的年化收益率", "一直持有基准的年化收益率", "比一直持有多赚/少赚", "最大回撤", "平均现金占比", "期末现金占比", "期末资产", "累计投入", "累计盈利", "申购周数", "赎回周数", "胜率", "最长空仓天数", "交易次数"]
    print(display_df[show_cols].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print(f"\n详细结果与图：{out_csv}")
    print("\n风险提示：历史回测结果基于历史数据与既定规则模拟，不代表未来收益；市场有风险，投资需谨慎。本 skill 输出仅为决策参考，不构成投资建议。")


if __name__ == "__main__":
    main()

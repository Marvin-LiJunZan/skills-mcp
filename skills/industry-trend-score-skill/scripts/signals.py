"""当日买卖信号生成：对指定策略/基金池，用最新数据计算目标仓位与动作。"""

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
    resolve_rotation_pool,
)


ROOT = Path(__file__).resolve().parents[1]


def load_json(path: Path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def strategy_label(tpl: dict) -> str:
    """Use the user-facing Chinese name in signal output while keeping config name ASCII."""
    return str(tpl.get("display_name") or tpl.get("name") or "策略")


def fetch_data(client: DataClient, pool: dict, years: int = 5) -> dict:
    data_map = {}
    for category, items in pool.items():
        for it in items:
            df = client.fetch_series(it["thscode"], it.get("fund_type", "otc"), years=years)
            if not df.empty:
                data_map[it["subcategory"]] = df.set_index("date")
    return data_map


def latest_signal(cfg: dict, data_map: dict, market=None, forced_buys=None) -> dict:
    target = build_target_weights(cfg, data_map, market)
    last = target.iloc[-1]
    data_date = str(target.index[-1].date())
    if cfg.get("category") == "single_fund_timing":
        name = cfg["fund_pool"][0]
        w = float(last[name])
        action = "买入/持有" if w > 0.5 else "卖出/空仓"
        if forced_buys is not None and not forced_buys.empty:
            fbd = forced_buys.reindex(target.index).dropna()
            if not fbd.empty and fbd.index[-1] == target.index[-1]:
                action = "买入（空仓N天/期，强制回补）"
        return {"数据日期": data_date, "类型": "单基金", "基金": name, "目标仓位": w, "动作": action}
    held = [n for n in target.columns if float(last[n]) > 0]
    return {"数据日期": data_date, "类型": "轮动", "目标行业": held, "动作": "空仓" if not held else "持有这些行业"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", type=Path, default=ROOT / "config" / "strategies_preset.json")
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
            pool = load_json(ROOT / "config" / "fund_pool.json")
            need = []
            for tpl in flat["single_fund_timing"]:
                need.extend(tpl.get("fund_pool") or [])
            for tpl in flat["industry_rotation"]:
                need.extend(tpl.get("fund_pool") or [])
            pool = filter_pool_by_names(pool, need)
    else:
        pool = load_json(ROOT / "config" / "fund_pool.json")
    client = DataClient(skill_action="signal")
    years = int((preset.get("cashflow") or {}).get("years") or preset.get("years") or 5)
    data_map = fetch_data(client, pool, years=years)
    market = client.fetch_index("000300.SH", years=years + 1).set_index("date")["close"]

    rows = []
    for tpl in flat["single_fund_timing"]:
        name = tpl["fund"]
        if name not in data_map:
            continue
        cfg = dict(tpl)
        cfg["fund_pool"] = [name]
        forced = build_forced_buys(cfg, data_map, market)
        sig = latest_signal(cfg, data_map, market, forced)
        print("\n" + "=" * 60)
        label = strategy_label(tpl)
        print(label + " · " + name)
        print(explain_strategy(cfg))
        print(format_tunable_params(cfg))
        rows.append({"类别": "单基金", "策略": label, **sig})

    ind_names = [it["subcategory"] for it in pool.get("行业", []) if it["subcategory"] in data_map]
    for tpl in flat["industry_rotation"]:
        cfg = dict(tpl)
        cfg["fund_pool"] = resolve_rotation_pool(cfg, ind_names, ind_names)
        sig = latest_signal(cfg, data_map, market)
        print("\n" + "=" * 60)
        label = strategy_label(tpl)
        print(label)
        print(explain_strategy(cfg))
        print(format_tunable_params(cfg))
        rows.append({"类别": "行业轮动", "策略": label, **sig})

    df = pd.DataFrame(rows)
    print("\n===== 当日信号 =====")
    print(df.to_string(index=False))
    print("\n风险提示：历史回测结果基于历史数据与既定规则模拟，不代表未来收益；市场有风险，投资需谨慎。本 skill 输出仅为决策参考，不构成投资建议。")


if __name__ == "__main__":
    main()

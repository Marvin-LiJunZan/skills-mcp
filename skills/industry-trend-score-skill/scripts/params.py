"""策略参数：NL 修改、校验与说明。"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


INTERVAL_ALIASES = {
    "每日": ("days", 1),
    "每天": ("days", 1),
    "每周": ("weekly", 5),
    "每两周": ("days", 10),
    "每半月": ("semimonthly", 15),
    "每月": ("monthly", 1),
}
EXTRA_FREQ_CHOICES = ["每周", "每月", "每季", "每年"]


def load_cfg(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_cfg(path, cfg):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)


def tunable_params(cfg):
    return cfg.get("tunable_params", [])


def all_params(cfg):
    return list(cfg.get("tunable_params", [])) + list(cfg.get("fund_params", []))


def _value_from_text(text, param, other_tokens=()):
    label = param.get("label", param.get("key"))
    key = param.get("key", label)
    clause = text
    for sep in ["，", ",", "；", ";", "。", "、"]:
        parts = text.split(sep)
        hit = [p for p in parts if label in p or key in p]
        if hit:
            clause = hit[0]
            break
    pos = clause.find(label)
    if pos >= 0:
        token = label
    else:
        pos = clause.find(key)
        token = key
    segment = clause[pos + len(token):] if pos >= 0 else clause
    stops = [
        segment.find(t) for t in other_tokens
        if t and segment.find(t) >= 0
    ]
    if stops:
        segment = segment[: min(stops)]
    m = re.search(r"(\d+(?:\.\d+)?)", segment)
    if not m:
        return None, "没有识别到数值"
    raw = float(m.group(1))
    if "%" in segment and param.get("max", 1) <= 1:
        raw = raw / 100.0
    elif param.get("unit") == "%" and param.get("max", 1) <= 1:
        raw = raw / 100.0
    return raw, None


def _validate(param, value):
    label = param.get("label", param.get("key"))
    if "min" in param and value < param["min"]:
        return False, "%s 最小值为 %s" % (label, param["min"])
    if "max" in param and value > param["max"]:
        return False, "%s 最大值为 %s" % (label, param["max"])
    return True, None


def apply_param_updates(text, cfg, params=None):
    params = params if params is not None else all_params(cfg)
    other_tokens = [q.get("label", q.get("key")) for q in params]
    messages = []
    matched_any = False
    if not any(q.get("key") == "max_empty_days" for q in params) and (
        "最久空仓期" in text or "max_empty_days" in text
    ):
        matched_any = True
        m = re.search(r"(\d+(?:\.\d+)?)", text)
        if not m:
            messages.append("最久空仓期：没有识别到数值")
        else:
            value = float(m.group(1))
            if 0 <= value <= 250:
                cfg.setdefault("max_empty", {})["days"] = int(value)
                messages.append("最久空仓期 -> %d" % int(value))
            else:
                messages.append("超出范围：最久空仓期 最大值为 250")
    has_fund = bool(cfg.get("fund_params"))
    if has_fund:
        freq_hit = [a for a in EXTRA_FREQ_CHOICES if a in text]
        if freq_hit and any(k in text for k in ("新增", "资金频率", "频率", "extra_contribution_freq")):
            matched_any = True
            cfg["extra_contribution_freq"] = freq_hit[-1]
            messages.append("定期新增频率 -> %s" % freq_hit[-1])
        if "新增" in text and "定期新增金额" not in text and "新增金额" not in text:
            m = re.search(r"新增[^\d]*(\d+(?:\.\d+)?)", text)
            if m:
                matched_any = True
                cfg["extra_contribution_amount"] = float(m.group(1))
                messages.append("定期新增金额 -> %s" % m.group(1))
    if "固定金额" in text or "固定比例" in text:
        matched_any = True
        cfg["buy_mode"] = "固定金额" if "固定金额" in text else "固定比例"
        messages.append("买入方式 -> %s" % cfg["buy_mode"])
    for p in params:
        label = p.get("label", p.get("key"))
        if label not in text and p.get("key") not in text:
            continue
        matched_any = True
        key = p["key"]
        if key == "fund_pool":
            choices = p.get("choices") or []
            hit = [c for c in choices if c in text]
            if not hit:
                messages.append(label + "：没有识别到行业")
            elif any(k in text for k in ("去掉", "删除", "移除", "剔除")):
                cfg["fund_pool"] = [x for x in (cfg.get("fund_pool") or []) if x not in hit]
                messages.append("%s -> 去掉 %s" % (label, "、".join(hit)))
            elif any(k in text for k in ("加入", "加上", "增加", "添加")):
                pool = list(cfg.get("fund_pool") or [])
                added = [x for x in hit if x not in pool]
                pool.extend(added)
                cfg["fund_pool"] = pool
                messages.append("%s -> 加入 %s" % (label, "、".join(added) if added else "无新增"))
            else:
                cfg["fund_pool"] = list(hit)
                messages.append("%s -> %s" % (label, "、".join(hit)))
            continue
        if key == "weight_scheme" or ("choices" in p and "values" in p):
            for choice, val in zip(p.get("choices") or [], p.get("values") or []):
                if choice in text:
                    cfg[key] = val
                    messages.append("%s -> %s" % (label, choice))
                    break
            else:
                messages.append(label + "：没有识别到选项")
            continue
        if key == "extra_contribution_freq":
            continue
        if key == "buy_mode":
            continue
        if key == "rebalance_interval":
            for alias, (mode, days) in INTERVAL_ALIASES.items():
                if alias in text:
                    cfg["rebalance_mode"] = mode
                    cfg["rebalance_days"] = days
                    messages.append("%s -> %s" % (label, alias))
                    break
            else:
                m = re.search(r"每\s*(\d+)\s*天", text)
                if m:
                    days = int(m.group(1))
                    if days < 1:
                        messages.append("超出范围：%s 最小值为 1 天" % label)
                    else:
                        cfg["rebalance_mode"] = "days"
                        cfg["rebalance_days"] = days
                        messages.append("%s -> 每%d天" % (label, cfg["rebalance_days"]))
            continue
        if key == "max_empty_days":
            value, err = _value_from_text(text, p, other_tokens)
            if err is not None:
                messages.append(label + "：" + err)
            else:
                ok, msg = _validate(p, value)
                if ok:
                    cfg.setdefault("max_empty", {})["days"] = int(value)
                    messages.append("%s -> %d" % (label, int(value)))
                else:
                    messages.append("超出范围：" + msg)
            continue
        if key in ("momentum_weight", "valuation_weight"):
            value, err = _value_from_text(text, p, other_tokens)
            if err is not None:
                messages.append(label + "：" + err)
            else:
                ok, msg = _validate(p, value)
                if ok:
                    cfg[key] = value
                    cfg.setdefault("params", {})[key] = value
                    messages.append("%s -> %s" % (label, value))
                else:
                    messages.append("超出范围：" + msg)
            continue
        value, err = _value_from_text(text, p, other_tokens)
        if err is not None:
            messages.append(label + "：" + err)
            continue
        ok, msg = _validate(p, value)
        if not ok:
            messages.append("超出范围：" + msg)
            continue
        cfg[key] = value
        messages.append("%s -> %s" % (label, value))
    if not matched_any and any(k in text for k in ("改成", "调整", "调参")):
        candidates = "、".join(q.get("label", q.get("key")) for q in params) or "无"
        messages.append("没有识别到可调参数，候选参数：" + candidates)
    return cfg, messages


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True, type=Path)
    ap.add_argument("--set", action="append", required=True)
    args = ap.parse_args()
    cfg = load_cfg(args.config)
    for s in args.set:
        cfg, msgs = apply_param_updates(s, cfg)
        for m in msgs:
            print(m)
    save_cfg(args.config, cfg)


if __name__ == "__main__":
    main()

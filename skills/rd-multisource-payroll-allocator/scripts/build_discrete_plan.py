# -*- coding: utf-8 -*-
"""
生成全生命周期 52 个月份严格离散工时率（0.25, 0.20, 0.15, 0.10）的排布方案
"""
import os, sys, random, json
sys.path.append(r"C:\JunzanLi_project\skills_mcp\skills\rd-multisource-payroll-allocator\scripts")
from generate_19b03_all_52_months import get_monthly_finance_data, all_periods, GRAND_TOTAL_TARGET, monthly_targets

discrete_rates = [0.25, 0.20, 0.15, 0.10]
random.seed(20261015)

core_names = ['陈前', '徐加兵', '梁兴朴', '周智', '肖云', '魏章俊', '喻国军']

# 第一步：构建各月初始参研团队与离散档位
month_plans = {}
for y, m in all_periods:
    tgt = monthly_targets[(y, m)]
    p_data = get_monthly_finance_data(y, m)
    
    # 规模根据当月费用预算适配 (10 ~ 15人)
    if tgt < 46000: k = 9
    elif tgt < 54000: k = 11
    elif tgt < 63000: k = 13
    else: k = 15
    
    cq = [p for p in p_data if p['name'] == '陈前']
    core = [p for p in p_data if p['name'] in core_names and p['name'] != '陈前']
    others = [p for p in p_data if p['name'] not in core_names]
    
    chosen = cq + core[:min(len(core), k//2)]
    needed = k - len(chosen)
    if needed > 0 and len(others) >= needed:
        chosen += random.sample(others, needed)
    elif needed > 0:
        chosen += others
        
    rates = {}
    for p in chosen:
        nm = p['name']
        if nm == '陈前':
            rates[nm] = 0.25 if tgt > 56000 else 0.20
        elif nm in core_names:
            rates[nm] = 0.20 if tgt > 64000 else 0.15
        else:
            rates[nm] = 0.15 if tgt > 62000 else 0.10
            
    tot = sum(p['base_fee'] * rates[p['name']] for p in chosen)
    month_plans[(y, m)] = {
        'team_names': [p['name'] for p in chosen],
        'rates': rates,
        'tot': tot,
        'tgt': tgt
    }

# 第二步：全局微调离散档位，使全生命周期总和与 3,113,798.60 的差距压缩到极微小
current_grand = sum(cfg['tot'] for cfg in month_plans.values())
diff = current_grand - GRAND_TOTAL_TARGET
print(f"初始离散总额: {current_grand:,.2f} 元, 全局差距: {diff:+,.2f} 元")

periods_list = list(all_periods)
for _ in range(10000):
    if abs(diff) < 15.0: break
    p_ym = random.choice(periods_list)
    cfg = month_plans[p_ym]
    y, m = p_ym
    p_data = {p['name']: p for p in get_monthly_finance_data(y, m)}
    
    nm = random.choice(cfg['team_names'])
    curr_r = cfg['rates'][nm]
    b_fee = p_data[nm]['base_fee']
    
    if diff > 0:
        lower = [r for r in discrete_rates if r < curr_r]
        if lower:
            next_r = max(lower)
            change = b_fee * (next_r - curr_r)
            if abs(diff + change) < abs(diff):
                cfg['rates'][nm] = next_r
                cfg['tot'] += change
                diff += change
    else:
        higher = [r for r in discrete_rates if r > curr_r]
        if higher:
            next_r = min(higher)
            change = b_fee * (next_r - curr_r)
            if abs(diff + change) < abs(diff):
                cfg['rates'][nm] = next_r
                cfg['tot'] += change
                diff += change

final_grand = sum(cfg['tot'] for cfg in month_plans.values())
print(f"优化后离散总额: {final_grand:,.2f} 元, 全局差距: {final_grand - GRAND_TOTAL_TARGET:+.2f} 元")

# 第三步：各月根据实际计算额与月度目标的极微小偏差，计算陈前的微调补偿 (平均仅几块钱)
export_data = {}
for p_ym in all_periods:
    cfg = month_plans[p_ym]
    y, m = p_ym
    p_data = {p['name']: p for p in get_monthly_finance_data(y, m)}
    # 理论小计之和
    calc_sum = sum(p_data[nm]['base_fee'] * cfg['rates'][nm] for nm in cfg['team_names'])
    m_diff = round(cfg['tgt'] - calc_sum, 2)
    
    export_data[f"{y}_{m}"] = {
        'team_names': cfg['team_names'],
        'rates': cfg['rates'],
        'comp': m_diff,
        'tgt': cfg['tgt'],
        'calc_sum': calc_sum
    }

# 保存为 json 供生成器直接读取
out_json = r"C:\JunzanLi_project\skills_mcp\skills\rd-multisource-payroll-allocator\scripts\discrete_plan_52m.json"
with open(out_json, "w", encoding="utf-8") as f:
    json.dump(export_data, f, ensure_ascii=False, indent=2)

print(f"-> 离散规划方案保存成功: {out_json}")

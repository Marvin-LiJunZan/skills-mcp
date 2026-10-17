# -*- coding: utf-8 -*-
import os, sys, random
sys.path.append(r"C:\JunzanLi_project\skills_mcp\skills\rd-multisource-payroll-allocator\scripts")
from generate_19b03_all_52_months import get_monthly_finance_data, all_periods, GRAND_TOTAL_TARGET, monthly_targets

discrete_rates = [0.25, 0.20, 0.15, 0.10]
random.seed(42)

months_info = []
core_names = ['陈前', '徐加兵', '梁兴朴', '周智', '肖云', '魏章俊', '喻国军']

for y, m in all_periods:
    tgt = monthly_targets[(y, m)]
    p_data = get_monthly_finance_data(y, m)
    months_info.append({'period': (y, m), 'tgt': tgt, 'p_data': p_data})

month_configs = []
for minfo in months_info:
    tgt = minfo['tgt']
    p_data = minfo['p_data']
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
    month_configs.append({'team': chosen, 'rates': rates, 'tot': tot, 'tgt': tgt})

current_grand = sum(cfg['tot'] for cfg in month_configs)
diff = current_grand - GRAND_TOTAL_TARGET
print('Starting grand total:', round(current_grand, 2), 'diff:', round(diff, 2))

for _ in range(5000):
    if abs(diff) < 20.0: break
    m_idx = random.randint(0, len(month_configs)-1)
    cfg = month_configs[m_idx]
    team = cfg['team']
    p = random.choice(team)
    nm = p['name']
    curr_r = cfg['rates'][nm]
    
    if diff > 0:
        lower = [r for r in discrete_rates if r < curr_r]
        if lower:
            next_r = max(lower)
            change = p['base_fee'] * (next_r - curr_r)
            if abs(diff + change) < abs(diff):
                cfg['rates'][nm] = next_r
                cfg['tot'] += change
                diff += change
    else:
        higher = [r for r in discrete_rates if r > curr_r]
        if higher:
            next_r = min(higher)
            change = p['base_fee'] * (next_r - curr_r)
            if abs(diff + change) < abs(diff):
                cfg['rates'][nm] = next_r
                cfg['tot'] += change
                diff += change

final_grand = sum(cfg['tot'] for cfg in month_configs)
print('Final grand total:', round(final_grand, 2), 'diff:', round(final_grand - GRAND_TOTAL_TARGET, 2))
print('Sample 5 months final:')
for i in range(5):
    cfg = month_configs[i]
    r_dist = {r: list(cfg['rates'].values()).count(r) for r in discrete_rates}
    print('  Month', i+1, ':', len(cfg['team']), 'persons, Tot=', round(cfg['tot'], 2), '|', r_dist)

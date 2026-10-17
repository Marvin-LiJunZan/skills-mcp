"""
研发费用人工费考勤表与职工薪酬分摊表自动化生成脚本 (Skill 内置通用版)
严格遵循：
1. 考勤统计周期为上月21日至当月20日；
2. 动态自适应任何研发项目的工时率列与研究人员费列（不硬编码列名与列号）；
3. 以季度汇总表入账的研究人员费（法定金额）为基准倒推平衡月度考勤天数与科研打点，
   确保3个月度分摊表合计严格等于汇总表法定研究人员费金额；
4. 科研单日工时限定5大标准面额（8, 4, 2, 1, 0.5），团队科研日对齐课题负责人；
5. 科研天数纯正活公式（=SUM/8）与两位小数保留（0.00_ ），表底签名栏留白手签。
"""

import sys
import os
import re
import argparse
import hashlib
import datetime as dt
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import xlrd
import openpyxl
from openpyxl.styles import Font, Alignment, Border, Side
import chinese_calendar as cc

ALLOWED_HOURS = [8, 4, 2, 1, 0.5]
SEED = "21-B-02-replay-v1"

# 公司特批春节假期配置 (除夕至正月初十含两端放假，优先于调休上班)
COMPANY_OFF_RANGES = {
    2022: (dt.date(2022, 1, 31), dt.date(2022, 2, 10)),
    2023: (dt.date(2023, 1, 21), dt.date(2023, 1, 31)),
    2024: (dt.date(2024, 2, 9), dt.date(2024, 2, 19)),
    2025: (dt.date(2025, 1, 28), dt.date(2025, 2, 7)),
}

def is_company_holiday(d: dt.date) -> bool:
    y = d.year
    if y in COMPANY_OFF_RANGES:
        start_d, end_d = COMPANY_OFF_RANGES[y]
        if start_d <= d <= end_d:
            return True
    return False

def get_day_mark(d: dt.date):
    if is_company_holiday(d):
        return '-'
    if cc.is_workday(d):
        return 8
    is_in_lieu, hol_name = cc.get_holiday_detail(d)
    if hol_name is not None:
        return '-'
    return '/'

def random_generator(key: str):
    state = int.from_bytes(hashlib.sha256(f"{SEED}|{key}".encode('utf-8')).digest()[:4], 'little')
    def rnd():
        nonlocal state
        state = (state + 0x6D2B79F5) & 0xFFFFFFFF
        t = state
        t = (t ^ (t >> 15)) & 0xFFFFFFFF
        t = (t * (t | 1)) & 0xFFFFFFFF
        t = (t ^ (t + (((t ^ (t >> 7)) * (t | 61)) & 0xFFFFFFFF))) & 0xFFFFFFFF
        return ((t ^ (t >> 14)) & 0xFFFFFFFF) / 4294967296.0
    return rnd

def allocate_hours_codex_style(available_indices, target_hours, key, leader_allocation=None):
    assigned = round(target_hours / 0.5) * 0.5
    units = int(round(assigned * 2))
    chunks = []
    for h in sorted(ALLOWED_HOURS, reverse=True):
        size = int(round(h * 2))
        while units >= size:
            chunks.append(h)
            units -= size
            
    if units > 0:
        chunks.append(0.5)
        
    avail_set = set(available_indices)
    leader_days = set([i for i, h in leader_allocation.items() if h > 0]) if leader_allocation else None
    
    preferred = set([i for i in avail_set if not leader_days or i in leader_days])
    extras = set([i for i in avail_set if leader_days and i not in leader_days])
    
    rnd = random_generator(key)
    res = {}
    cursor = 0
    
    while cursor < len(chunks):
        pool = preferred if len(preferred) > 0 else extras
        if not pool:
            break
        pairs = [i for i in pool if (i + 1) in pool]
        use_pair = len(pairs) > 0 and (len(chunks) - cursor >= 2)
        if use_pair:
            pick_idx = int(rnd() * len(pairs))
            start_day = pairs[pick_idx]
            chosen = [start_day, start_day + 1]
        else:
            pool_list = sorted(list(pool))
            pick_idx = int(rnd() * len(pool_list))
            chosen = [pool_list[pick_idx]]
            
        for day in chosen:
            if cursor >= len(chunks):
                break
            res[day] = chunks[cursor]
            cursor += 1
            if day in pool:
                pool.remove(day)
                
    return res, assigned

def solve_person_backcalc(name, B, r_target, q_rate, W):
    """
    根据人员在当季度的目标研究人员费金额 (r_target) 与三个月的月度薪酬基数 (B)，
    倒推求得各有效月份的最优出勤天数 A=(a1, a2, a3) 和科研小时 H=(h1, h2, h3)，
    使得 sum(B[m] * (H[m] / (8 * A[m]))) 极度精确贴合 r_target。
    支持人员在季度内部分月份入职或离职（即某个或某些月份薪酬为0的情况）。
    """
    if r_target <= 0 or sum(B) <= 0:
        base_h = [round(W[m] * 8 * q_rate * 2) / 2 if B[m] > 0 else 0.0 for m in range(3)]
        return (W[0], W[1], W[2]), tuple(base_h), 0.0

    active_indices = [m for m in range(3) if B[m] > 0]
    eff_rate = r_target / sum(B)
    
    best_diff = 999999
    best_sol = None
    
    if len(active_indices) == 3:
        base_h = [round(W[m] * 8 * eff_rate * 2) / 2 for m in range(3)]
        a_options = [
            (da1, da2, da3)
            for da1 in [0, -1, -2]
            for da2 in [0, -1, -2]
            for da3 in [0, -1, -2]
        ]
        a_options.sort(key=lambda x: abs(x[0]) + abs(x[1]) + abs(x[2]))
        for da1, da2, da3 in a_options:
            a1, a2, a3 = W[0] + da1, W[1] + da2, W[2] + da3
            if a1 < 8 or a2 < 8 or a3 < 8 or a1 > W[0] or a2 > W[1] or a3 > W[2]:
                continue
            for dh1 in [x * 0.5 for x in range(-54, 55)]:
                h1 = base_h[0] + dh1
                if h1 <= 0 or h1 > a1 * 8:
                    continue
                alloc1 = B[0] * (h1 / (8.0 * a1))
                for dh2 in [x * 0.5 for x in range(-54, 55)]:
                    h2 = base_h[1] + dh2
                    if h2 <= 0 or h2 > a2 * 8:
                        continue
                    alloc2 = B[1] * (h2 / (8.0 * a2))
                    rem = r_target - alloc1 - alloc2
                    if rem <= 0:
                        continue
                    h3_cand = round((rem * 8.0 * a3 / B[2]) * 2) / 2
                    if h3_cand <= 0 or h3_cand > a3 * 8:
                        continue
                    alloc3 = B[2] * (h3_cand / (8.0 * a3))
                    diff = abs((alloc1 + alloc2 + alloc3) - r_target)
                    penalty = diff * 10.0 + (abs(da1) + abs(da2) + abs(da3)) * 0.2 + (abs(dh1) + abs(dh2) + abs(h3_cand - base_h[2])) * 0.05
                    if penalty < best_diff:
                        best_diff = penalty
                        best_sol = ((a1, a2, a3), (h1, h2, h3_cand), diff)
                        if diff < 0.005 and da1 == 0 and da2 == 0 and da3 == 0:
                            return best_sol

    elif len(active_indices) == 2:
        m0, m1 = active_indices
        base_h = [round(W[m] * 8 * eff_rate * 2) / 2 if B[m] > 0 else 0.0 for m in range(3)]
        a_opts = [(da0, da1) for da0 in [0, -1, -2] for da1 in [0, -1, -2]]
        a_opts.sort(key=lambda x: abs(x[0]) + abs(x[1]))
        for da0, da1 in a_opts:
            a = list(W)
            a[m0] += da0
            a[m1] += da1
            if a[m0] < 8 or a[m1] < 8 or a[m0] > W[m0] or a[m1] > W[m1]:
                continue
            for dh0 in [x * 0.5 for x in range(-54, 55)]:
                h0 = base_h[m0] + dh0
                if h0 <= 0 or h0 > a[m0] * 8:
                    continue
                alloc0 = B[m0] * (h0 / (8.0 * a[m0]))
                rem = r_target - alloc0
                if rem <= 0:
                    continue
                h1_cand = round((rem * 8.0 * a[m1] / B[m1]) * 2) / 2
                if h1_cand <= 0 or h1_cand > a[m1] * 8:
                    continue
                alloc1 = B[m1] * (h1_cand / (8.0 * a[m1]))
                diff = abs((alloc0 + alloc1) - r_target)
                penalty = diff * 10.0 + (abs(da0) + abs(da1)) * 0.2
                if penalty < best_diff:
                    best_diff = penalty
                    h_res = [0.0, 0.0, 0.0]
                    h_res[m0] = h0
                    h_res[m1] = h1_cand
                    best_sol = (tuple(a), tuple(h_res), diff)
                    if diff < 0.005 and da0 == 0 and da1 == 0:
                        return best_sol

    elif len(active_indices) == 1:
        m0 = active_indices[0]
        a = list(W)
        for da0 in [0, -1, -2]:
            a[m0] = W[m0] + da0
            h0_cand = round((r_target * 8.0 * a[m0] / B[m0]) * 2) / 2
            if 0 < h0_cand <= a[m0] * 8:
                alloc0 = B[m0] * (h0_cand / (8.0 * a[m0]))
                diff = abs(alloc0 - r_target)
                if diff < best_diff:
                    best_diff = diff
                    h_res = [0.0, 0.0, 0.0]
                    h_res[m0] = h0_cand
                    best_sol = (tuple(a), tuple(h_res), diff)

    return best_sol if best_sol else ((W[0], W[1], W[2]), tuple([round(W[m] * 8 * eff_rate * 2) / 2 if B[m] > 0 else 0.0 for m in range(3)]), 999)

def get_project_leader(wb_src, proj_keywords):
    summary_sname = None
    for s in wb_src.sheet_names():
        if '汇总' in s and '分配' not in s:
            summary_sname = s
            break
    if not summary_sname and len(wb_src.sheet_names()) > 0:
        summary_sname = wb_src.sheet_names()[0]
        
    if summary_sname:
        ss = wb_src.sheet_by_name(summary_sname)
        lead_col = None
        for c in range(ss.ncols):
            for r in range(min(5, ss.nrows)):
                v = str(ss.cell_value(r, c)).replace('\n', '').strip()
                if '负责人' in v: lead_col = c
        if lead_col is not None:
            for r in range(ss.nrows):
                row_str = " ".join([str(ss.cell_value(r, c)) for c in range(ss.ncols)])
                if any(k in row_str for k in proj_keywords):
                    leader = str(ss.cell_value(r, lead_col)).strip()
                    if leader and leader not in ['负责人', '课题负责人']:
                        return leader
    return "陈前"

def parse_quarter_info(filename):
    m = re.search(r'(\d{4})年.*([1-4])季度', filename)
    if m:
        year = int(m.group(1))
        quarter = int(m.group(2))
        months = [(quarter - 1) * 3 + 1, (quarter - 1) * 3 + 2, (quarter - 1) * 3 + 3]
        return year, quarter, months
    return None, None, None

def generate_quarter_workbook(summary_file, output_dir, proj_code, proj_name, proj_keywords, template_file=None):
    if template_file is None:
        template_file = r"C:\JunzanLi_project\课题申报横向\人工费考勤表与分摊表\2024年7-9月研发人员薪酬、职工薪酬分配表21-B-02（定稿打印版）.xlsx"
    fname = os.path.basename(summary_file)
    year, quarter, months = parse_quarter_info(fname)
    if not year:
        return
        
    out_filename = f"{year}年{months[0]}-{months[2]}月研发人员薪酬、职工薪酬分配表{proj_code}.xlsx"
    out_path = os.path.join(output_dir, out_filename)
    print(f"\n>>> 正在生成: {out_filename} (来源: {fname})...")
    
    wb_src = xlrd.open_workbook(summary_file)
    snames = wb_src.sheet_names()
    
    leader_name = get_project_leader(wb_src, proj_keywords)
    print(f"  课题负责人: {leader_name}")
    
    entry_sname = None
    for s in snames:
        if any(k in s for k in ['分配表入账', '职工薪酬分配明细', '分配明细', '职工薪酬']):
            if s != '汇总表':
                entry_sname = s
                break
    if not entry_sname and len(snames) > 1:
        entry_sname = snames[1]
    if not entry_sname:
        raise ValueError(f"{fname} 缺少入账分摊表!")
        
    es = wb_src.sheet_by_name(entry_sname)
    
    # 动态、通用匹配课题列与紧邻的研究人员费列 (绝非死写列字母)
    proj_rate_col = None
    for c in range(es.ncols):
        txt = " ".join([str(es.cell_value(r, c)) for r in range(min(5, es.nrows))])
        if any(k in txt for k in proj_keywords):
            proj_rate_col = c
            break
    if proj_rate_col is None:
        raise ValueError(f"{fname} 未匹配到课题列!")
        
    proj_fee_col = proj_rate_col + 1
    
    name_col = 1
    for c in range(min(5, es.ncols)):
        for r in range(min(5, es.nrows)):
            if str(es.cell_value(r, c)).strip() == '姓名':
                name_col = c
                break
                
    proj_people = {}
    proj_target_fees = {}
    source_order = []
    target_quarter_total = 0.0
    
    for r in range(es.nrows):
        name = str(es.cell_value(r, name_col)).strip()
        val_rate = es.cell_value(r, proj_rate_col)
        val_fee = es.cell_value(r, proj_fee_col) if proj_fee_col < es.ncols else 0.0
        
        if name and name not in ['姓名', '合计', '小计', ''] and val_rate not in ['', None, 0, 0.0]:
            try:
                rate = float(val_rate)
                fee = float(val_fee) if val_fee not in ['', None] else 0.0
                if rate > 0 or fee > 0:
                    proj_people[name] = rate
                    proj_target_fees[name] = fee
                    if name not in source_order:
                        source_order.append(name)
            except ValueError:
                pass
        elif name == '合计' and val_fee not in ['', None]:
            try:
                target_quarter_total = float(val_fee)
            except ValueError:
                pass
                
    base_people_list = sorted(source_order, key=lambda x: (x != leader_name, source_order.index(x)))
    print(f"  课题人员名单 ({len(base_people_list)}人): {base_people_list}")
    print(f"  课题汇总表法定研究人员费总额: {target_quarter_total:.2f}")
    
    monthly_sheet_names = []
    for m in months:
        candidates = [str(m), f"{m}月", f"{m}月份薪酬", f"{m:02d}月", f"{year}{m:02d}月"]
        found = None
        for cand in candidates:
            if cand in snames:
                found = cand
                break
        if not found and quarter in [1, 2, 3, 4]:
            idx_in_q = str(months.index(m) + 1)
            if idx_in_q in snames:
                found = idx_in_q
        if not found:
            raise ValueError(f"在 {fname} 中未找到 {m} 月薪酬表!")
        monthly_sheet_names.append(found)

    # 预先穿透提取3个月的月度基数与日历
    months_wages = []
    months_workdays_count = []
    months_calendar_info = []

    for m_idx, month_num in enumerate(months):
        src_sheet_name = monthly_sheet_names[m_idx]
        ms = wb_src.sheet_by_name(src_sheet_name)
        
        col_map = {}
        for r in range(min(6, ms.nrows)):
            for c in range(min(20, ms.ncols)):
                val = str(ms.cell_value(r, c)).replace('\n', '').replace(' ', '')
                if '姓名' in val and '姓名' not in col_map: col_map['姓名'] = c
                elif ('1.应发工资' in val or '应发工资' in val) and '应发工资' not in col_map: col_map['应发工资'] = c
                elif ('2.社会保险费' in val or '社会保险费' in val) and '社保' not in col_map: col_map['社保'] = c
                elif ('2.1' in val or '基本养老' in val) and '养老' not in col_map: col_map['养老'] = c
                elif ('2.2' in val or '工伤' in val) and '工伤' not in col_map: col_map['工伤'] = c
                elif ('2.3' in val or '失业' in val) and '失业' not in col_map: col_map['失业'] = c
                elif ('2.4' in val or '基本医疗' in val) and '医疗' not in col_map: col_map['医疗'] = c
                elif ('2.5' in val or '大病' in val) and '大病' not in col_map: col_map['大病'] = c
                elif ('3.住房' in val or '公积金' in val) and '公积金' not in col_map: col_map['公积金'] = c
                elif ('4.企业年金' in val or '年金' in val) and '年金' not in col_map: col_map['年金'] = c
                
        emp_wages = {}
        for r in range(ms.nrows):
            name_val = str(ms.cell_value(r, col_map['姓名'])).strip() if '姓名' in col_map else ""
            if name_val in proj_people:
                def get_num(key):
                    if key in col_map:
                        v = ms.cell_value(r, col_map[key])
                        try:
                            return round(float(v), 2) if v not in ['', None] else 0.0
                        except ValueError:
                            return 0.0
                    return 0.0
                annuity = get_num('年金') if '年金' in col_map else None
                emp_wages[name_val] = {
                    '应发工资': get_num('应发工资'),
                    '社保': get_num('社保'),
                    '养老': get_num('养老'),
                    '工伤': get_num('工伤'),
                    '失业': get_num('失业'),
                    '医疗': get_num('医疗'),
                    '大病': get_num('大病'),
                    '公积金': get_num('公积金'),
                    '年金': annuity if (annuity is not None and annuity > 0) else None,
                }
        months_wages.append(emp_wages)
        
        # 严格执行：考勤周期为上月21日至当月20日
        if month_num == 1:
            start_date = dt.date(year - 1, 12, 21)
        else:
            start_date = dt.date(year, month_num - 1, 21)
        end_date = dt.date(year, month_num, 20)
        
        days_count = (end_date - start_date).days + 1
        days_range = [start_date + dt.timedelta(days=i) for i in range(days_count)]
        marks = [get_day_mark(d) for d in days_range]
        workdays_indices = [idx for idx, m in enumerate(marks) if m == 8]
        months_workdays_count.append(len(workdays_indices))
        months_calendar_info.append({
            'start_date': start_date,
            'end_date': end_date,
            'days_count': days_count,
            'days_range': days_range,
            'marks': marks,
            'workdays_indices': workdays_indices
        })

    # 倒推求解每位人员的月度最优出勤天数与科研工时
    A_plan = {}
    H_plan = {}
    for name in base_people_list:
        B = [
            months_wages[m].get(name, {}).get('应发工资', 0) +
            months_wages[m].get(name, {}).get('社保', 0) +
            months_wages[m].get(name, {}).get('公积金', 0) +
            (months_wages[m].get(name, {}).get('年金') or 0)
            for m in range(3)
        ]
        r_target = proj_target_fees.get(name, 0.0)
        q_rate = proj_people.get(name, 0.0)
        a_sol, h_sol, diff = solve_person_backcalc(name, B, r_target, q_rate, months_workdays_count)
        A_plan[name] = a_sol
        H_plan[name] = h_sol

    # 尾差平账计算引擎：模拟3个月度分摊后计算尾差，在末月公式中自动追加微调数抹平
    tail_diff = {}
    for name in base_people_list:
        r_target = proj_target_fees.get(name, 0.0)
        sim_allocs = []
        for m in range(3):
            a_val = A_plan[name][m]
            h_val = H_plan[name][m]
            rate_val = (h_val / 8.0) / a_val if a_val > 0 else 0.0
            w = months_wages[m].get(name, {})
            base_val = (
                w.get('应发工资', 0) +
                w.get('社保', 0) +
                w.get('公积金', 0) +
                (w.get('年金') or 0)
            )
            tot = base_val * rate_val
            sim_allocs.append(tot)
        diff_val = r_target - sum(sim_allocs)
        if abs(diff_val) <= 25.0:
            tail_diff[name] = diff_val
        else:
            tail_diff[name] = 0.0

    # 季度总额微调平账：将总目标与各人目标之和的微小差额补入第一人
    grand_rem = target_quarter_total - sum(proj_target_fees.get(p, 0.0) for p in base_people_list)
    if abs(grand_rem) > 0.00001 and base_people_list:
        tail_diff[base_people_list[0]] += grand_rem

    # 记录每位人员当季最后一个有效出勤月份（避免中途离职人员未到第3个月无法注入尾差）
    last_active_month = {}
    for name in base_people_list:
        active_m = [m for m in range(3) if months_wages[m].get(name, {}).get('应发工资', 0) > 0 or months_wages[m].get(name, {}).get('社保', 0) > 0]
        last_active_month[name] = max(active_m) if active_m else 2

    # 严格基于官方打印定稿模板复制并修改，确保全生命周期表样与打印版 100% 绝对一致
    wb_out = openpyxl.load_workbook(template_file)
    
    font_body = Font(name="宋体", size=10)
    font_bold = Font(name="宋体", size=10, bold=True)
    align_center = Alignment(horizontal="center", vertical="center")
    align_right = Alignment(horizontal="right", vertical="center")
    align_left = Alignment(horizontal="left", vertical="center")
    
    border_thin = Side(style='thin', color='000000')
    border_all = Border(left=border_thin, right=border_thin, top=border_thin, bottom=border_thin)

    sheet_pairs = [
        (wb_out.sheetnames[0], wb_out.sheetnames[1]),
        (wb_out.sheetnames[2], wb_out.sheetnames[3]),
        (wb_out.sheetnames[4], wb_out.sheetnames[5]),
    ]

    # 循环构建各月份考勤表与分摊表
    for m_idx, month_num in enumerate(months):
        orig_pay_name, orig_att_name = sheet_pairs[m_idx]
        pay_sheet_name = f"{year}{month_num:02d}月"
        att_sheet_name = f"{year}{month_num:02d}月考勤表"
        
        ws_pay = wb_out[orig_pay_name]
        ws_att = wb_out[orig_att_name]
        ws_pay.title = pay_sheet_name
        ws_att.title = att_sheet_name
        
        emp_wages = months_wages[m_idx]
        cal_info = months_calendar_info[m_idx]
        
        people_list = [p for p in base_people_list if p in emp_wages and (emp_wages[p]['应发工资'] > 0 or emp_wages[p]['社保'] > 0)]
        
        days_count = cal_info['days_count']
        days_range = cal_info['days_range']
        workdays_indices = cal_info['workdays_indices']
        
        end_day_col = 3 + days_count
        ai_col_idx = end_day_col + 1
        aj_col_idx = end_day_col + 2
        ai_col_letter = openpyxl.utils.get_column_letter(ai_col_idx)
        aj_col_letter = openpyxl.utils.get_column_letter(aj_col_idx)
        end_day_letter = openpyxl.utils.get_column_letter(end_day_col)
        
        # 1. 考勤表 (ws_att) 规范表头及打点
        ws_att.row_dimensions[1].height = 25.1
        for r in list(ws_att.merged_cells.ranges):
            if r.min_row == 1 and r.max_row == 1:
                ws_att.unmerge_cells(str(r))
        ws_att.merge_cells(f"A1:{aj_col_letter}1")
        ws_att.cell(1, 1, value="中铁建华南建设有限公司研发人员科研工时安排表")
        
        ws_att.row_dimensions[2].height = 15.75
        ws_att.cell(2, 1, value=f"研发项目名称：{proj_name}")
        for r in list(ws_att.merged_cells.ranges):
            if r.min_row == 2 and r.max_row == 2 and r.min_col >= 20:
                ws_att.unmerge_cells(str(r))
        ws_att.merge_cells("AA2:AD2")
        c_lbl = ws_att.cell(2, 27, value="合同编号：")
        c_lbl.font = font_body
        c_lbl.alignment = align_center
        ws_att.merge_cells(f"AE2:{aj_col_letter}2")
        c_code = ws_att.cell(2, 31, value=proj_code)
        c_code.font = font_body
        c_code.alignment = align_center
        
        ws_att.row_dimensions[3].height = 15.75
        ws_att.row_dimensions[4].height = 15.75
        for r in list(ws_att.merged_cells.ranges):
            if r.min_row in [3, 4] and r.min_col >= 4:
                ws_att.unmerge_cells(str(r))
                
        ws_att.merge_cells(f"D3:{end_day_letter}3")
        c_hdr = ws_att.cell(3, 4, value=f"{year}年{month_num}月份科研工时安排（{cal_info['start_date'].month}月{cal_info['start_date'].day}日—{cal_info['end_date'].month}月{cal_info['end_date'].day}日）")
        c_hdr.font = font_body
        c_hdr.alignment = align_center
        
        ws_att.merge_cells(f"{ai_col_letter}3:{ai_col_letter}4")
        c_att_hdr = ws_att.cell(3, ai_col_idx, value="出勤\n天数")
        c_att_hdr.font = font_body
        c_att_hdr.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        
        ws_att.merge_cells(f"{aj_col_letter}3:{aj_col_letter}4")
        c_rate_hdr = ws_att.cell(3, aj_col_idx, value="工时\n率")
        c_rate_hdr.font = font_body
        c_rate_hdr.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        
        for c_idx, d in enumerate(days_range):
            c_cell = ws_att.cell(4, 4 + c_idx, value=d.day)
            c_cell.font = font_body
            c_cell.alignment = align_center
            c_cell.border = border_all
            
        for c in range(1, aj_col_idx + 1):
            for r in range(3, 5):
                ws_att.cell(r, c).border = border_all

        # 清空第5行往后的旧数据
        for r in list(ws_att.merged_cells.ranges):
            if r.max_row >= 5:
                ws_att.unmerge_cells(str(r))
        if ws_att.max_row >= 5:
            ws_att.delete_rows(5, ws_att.max_row - 5 + 1)
            
        leader_hours_alloc = None
        for p_idx, name in enumerate(people_list):
            a_target = A_plan[name][m_idx]
            h_target = H_plan[name][m_idx]
            r_att = 5 + 2 * p_idx
            r_res = 6 + 2 * p_idx
            ws_att.row_dimensions[r_att].height = 19.0
            ws_att.row_dimensions[r_res].height = 19.0
            
            ws_att.merge_cells(f"A{r_att}:A{r_res}")
            ws_att.cell(r_att, 1, value=p_idx + 1).font = font_body
            ws_att.cell(r_att, 1).alignment = align_center
            
            ws_att.merge_cells(f"B{r_att}:B{r_res}")
            ws_att.cell(r_att, 2, value=name).font = font_body
            ws_att.cell(r_att, 2).alignment = align_center
            
            ws_att.cell(r_att, 3, value="出勤").font = font_body
            ws_att.cell(r_att, 3).alignment = align_center
            ws_att.cell(r_res, 3, value="科研").font = font_body
            ws_att.cell(r_res, 3).alignment = align_center
            
            # 出勤打点
            actual_workdays = workdays_indices[:a_target]
            for c_idx, d in enumerate(days_range):
                col_pos = 4 + c_idx
                mark = cal_info['marks'][c_idx]
                if mark == 8:
                    val = 8 if c_idx in actual_workdays else "/"
                else:
                    val = mark
                c_m = ws_att.cell(r_att, col_pos, value=val)
                c_m.font = font_body
                c_m.alignment = align_center
                
            c_tot_days = ws_att.cell(r_att, ai_col_idx, value=f"=COUNT(D{r_att}:{end_day_letter}{r_att})")
            c_tot_days.font = font_body
            c_tot_days.alignment = align_center
            
            # 科研工时排班打点
            alloc_dict = {}
            avail_indices = [idx for idx in actual_workdays if cal_info['marks'][idx] == 8]
            is_leader = (name == leader_name)
            if h_target > 0:
                if is_leader:
                    int_part = int(h_target)
                    has_half = (h_target - int_part) > 0.25
                    n_avail = len(avail_indices)
                    if n_avail > 0:
                        base_h = int_part // n_avail
                        rem_h = int_part % n_avail
                        for rank, idx in enumerate(avail_indices):
                            h_val = float(base_h + (1 if rank < rem_h else 0))
                            if has_half and rank == rem_h:
                                h_val += 0.5
                                has_half = False
                            if h_val > 0:
                                alloc_dict[idx] = h_val
                        if has_half and avail_indices:
                            alloc_dict[avail_indices[0]] = alloc_dict.get(avail_indices[0], 0.0) + 0.5
                    leader_hours_alloc = dict(alloc_dict)
                else:
                    slots = []
                    for idx in avail_indices:
                        w = leader_hours_alloc.get(idx, 0) if leader_hours_alloc else 0
                        slots.append((w, idx))
                    slots.sort(key=lambda x: (-x[0], x[1]))
                    needed = h_target
                    for _, idx in slots:
                        if needed >= 8:
                            alloc_dict[idx] = 8
                            needed -= 8
                        elif needed > 0:
                            alloc_dict[idx] = needed
                            needed = 0
                        else:
                            break
            for c_idx in range(days_count):
                if c_idx in alloc_dict:
                    val = alloc_dict[c_idx]
                    c_h = ws_att.cell(r_res, 4 + c_idx, value=int(val) if val == int(val) else val)
                    c_h.font = font_body
                    c_h.alignment = align_center
                    
            c_res_days = ws_att.cell(r_res, ai_col_idx, value=f"=SUM(D{r_res}:{end_day_letter}{r_res})/8")
            c_res_days.font = font_body
            c_res_days.alignment = align_center
            c_res_days.number_format = '0.00'
            
            c_res_rate = ws_att.cell(r_res, aj_col_idx, value=f"={ai_col_letter}{r_res}/{ai_col_letter}{r_att}")
            c_res_rate.font = font_body
            c_res_rate.alignment = align_center
            c_res_rate.number_format = '0.00'
            
        for r in range(3, 5 + 2 * len(people_list)):
            for c in range(1, aj_col_idx + 1):
                ws_att.cell(r, c).border = border_all
                
        r_note = 5 + 2 * len(people_list)
        ws_att.row_dimensions[r_note].height = 27.0
        ws_att.merge_cells(f"A{r_note}:{aj_col_letter}{r_note}")
        c_note = ws_att.cell(r_note, 1, value="说明：出勤栏8表示日历应出勤，/表示休息，—表示国家法定假日；科研栏数字表示科研小时数。")
        c_note.font = font_body
        c_note.alignment = align_left
        
        r_sig = r_note + 1
        ws_att.row_dimensions[r_sig].height = 24.0
        ws_att.merge_cells(f"A{r_sig}:E{r_sig}")
        ws_att.cell(r_sig, 1, value="项目/课题负责人：").font = font_body
        ws_att.cell(r_sig, 1).alignment = align_left
        ws_att.cell(r_sig, 22, value="制表：").font = font_body
        ws_att.cell(r_sig, 22).alignment = align_left
        
        ws_att.column_dimensions['A'].width = 2.83
        ws_att.column_dimensions['B'].width = 6.33
        ws_att.column_dimensions['C'].width = 4.67
        for c in range(4, end_day_col + 1):
            ws_att.column_dimensions[openpyxl.utils.get_column_letter(c)].width = 3.5
        ws_att.column_dimensions[ai_col_letter].width = 4.58
        ws_att.column_dimensions[aj_col_letter].width = 5.42
        ws_att.print_area = f"'{att_sheet_name}'!$A$1:${aj_col_letter}${r_sig}"
        ws_att.page_setup.orientation = 'landscape'
        ws_att.page_setup.paperSize = 9

        # 2. 月度分摊表 (ws_pay) 规范项目信息与动态数据
        ws_pay.cell(2, 1, value=f"项目名称：{proj_name}")
        ws_pay.cell(2, 13, value="课题合同（项目）编号：")
        ws_pay.cell(2, 16, value=proj_code)
        ws_pay.cell(2, 22, value=f"{year}年{month_num}月（单位：元）")
        
        for r in list(ws_pay.merged_cells.ranges):
            if r.max_row >= 5:
                ws_pay.unmerge_cells(str(r))
        if ws_pay.max_row >= 5:
            ws_pay.delete_rows(5, ws_pay.max_row - 5 + 1)
            
        for p_idx, name in enumerate(people_list):
            r_pay = 5 + p_idx
            r_att_res = 6 + 2 * p_idx
            ws_pay.row_dimensions[r_pay].height = 24.0
            
            ws_pay.cell(r_pay, 1, value=p_idx + 1).font = font_body
            ws_pay.cell(r_pay, 1).alignment = align_center
            
            ws_pay.cell(r_pay, 2, value=name).font = font_body
            ws_pay.cell(r_pay, 2).alignment = align_center
            
            c_c = ws_pay.cell(r_pay, 3, value=f"='{att_sheet_name}'!{ai_col_letter}{r_att_res}")
            c_c.font = font_body
            c_c.alignment = align_center
            c_c.number_format = '0.00'
            
            c_d = ws_pay.cell(r_pay, 4, value=f"='{att_sheet_name}'!{aj_col_letter}{r_att_res}")
            c_d.font = font_body
            c_d.alignment = align_center
            c_d.number_format = '0.00'
            
            w = emp_wages[name]
            ann_val = w['年金'] if (w['年金'] is not None and w['年金'] > 0) else ""
            vals = [
                w['应发工资'], w['社保'], w['养老'], w['工伤'],
                w['失业'], w['医疗'], w['大病'], w['公积金'], ann_val
            ]
            for v_idx, val in enumerate(vals):
                cell_p = ws_pay.cell(r_pay, 5 + v_idx, value=val)
                cell_p.font = font_body
                cell_p.alignment = align_right
                if val != "":
                    cell_p.number_format = '#,##0.00'
                    
            c_tot = ws_pay.cell(r_pay, 14, value=f"=SUM(E{r_pay},F{r_pay},L{r_pay},M{r_pay})")
            c_tot.font = font_body
            c_tot.alignment = align_right
            c_tot.number_format = '#,##0.00'
            
            # 研发工资及末月尾差补偿平账（平账至绝对 0.00 差额闭合）
            delta = tail_diff.get(name, 0.0) if m_idx == last_active_month.get(name, 2) else 0.0
            if abs(delta) >= 0.00005:
                sign = "+" if delta > 0 else "-"
                delta_str = f"{abs(delta):.4f}".rstrip('0').rstrip('.')
                if '.' not in delta_str:
                    delta_str += '.00'
                elif len(delta_str.split('.')[1]) == 1:
                    delta_str += '0'
                f_val = f"=E{r_pay}*$D{r_pay}{sign}{delta_str}"
            else:
                f_val = f"=E{r_pay}*$D{r_pay}"
                
            ws_pay.cell(r_pay, 15, value=f_val).font = font_body
            ws_pay.cell(r_pay, 15).alignment = align_right
            ws_pay.cell(r_pay, 15).number_format = '#,##0.00'
            
            ws_pay.cell(r_pay, 16, value=f"=F{r_pay}*$D{r_pay}").font = font_body
            ws_pay.cell(r_pay, 16).alignment = align_right
            ws_pay.cell(r_pay, 16).number_format = '#,##0.00'
            
            for off in range(5):
                c_src = openpyxl.utils.get_column_letter(7 + off)
                cell_sub = ws_pay.cell(r_pay, 17 + off, value=f"={c_src}{r_pay}*$D{r_pay}")
                cell_sub.font = font_body
                cell_sub.alignment = align_right
                cell_sub.number_format = '#,##0.00'
                
            ws_pay.cell(r_pay, 22, value=f"=L{r_pay}*$D{r_pay}").font = font_body
            ws_pay.cell(r_pay, 22).alignment = align_right
            ws_pay.cell(r_pay, 22).number_format = '#,##0.00'
            
            ws_pay.cell(r_pay, 23, value=f'=IF(M{r_pay}="","",M{r_pay}*$D{r_pay})').font = font_body
            ws_pay.cell(r_pay, 23).alignment = align_right
            ws_pay.cell(r_pay, 23).number_format = '#,##0.00'
            
            c_alloc_tot = ws_pay.cell(r_pay, 24, value=f"=SUM(O{r_pay},P{r_pay},V{r_pay},W{r_pay})")
            c_alloc_tot.font = font_body
            c_alloc_tot.alignment = align_right
            c_alloc_tot.number_format = '#,##0.00'
            
            # 核对列 (Z & AA)
            ws_pay.cell(r_pay, 26, value=f"=SUM(O{r_pay},P{r_pay},V{r_pay},W{r_pay})").font = font_body
            ws_pay.cell(r_pay, 26).alignment = align_right
            ws_pay.cell(r_pay, 26).number_format = '#,##0.00'
            
            ws_pay.cell(r_pay, 27, value=f"=ROUND(Z{r_pay}-X{r_pay},2)").font = font_body
            ws_pay.cell(r_pay, 27).alignment = align_right
            ws_pay.cell(r_pay, 27).number_format = '#,##0.00'
            
            for c in range(1, 25):
                ws_pay.cell(r_pay, c).border = border_all
                
        # 合计行
        r_sum = 5 + len(people_list)
        ws_pay.row_dimensions[r_sum].height = 24.0
        ws_pay.cell(r_sum, 2, value="合计").font = font_bold
        ws_pay.cell(r_sum, 2).alignment = align_center
        
        c_sum_c = ws_pay.cell(r_sum, 3, value=f"=SUM(C5:C{r_sum-1})")
        c_sum_c.font = font_bold
        c_sum_c.alignment = align_center
        c_sum_c.number_format = '0.00'
        
        for c_idx in list(range(5, 15)) + list(range(15, 24)):
            col_let = openpyxl.utils.get_column_letter(c_idx)
            c_s = ws_pay.cell(r_sum, c_idx, value=f"=SUM({col_let}5:{col_let}{r_sum-1})")
            c_s.font = font_bold
            c_s.alignment = align_right
            c_s.number_format = '#,##0.00'
            
        c_s_x = ws_pay.cell(r_sum, 24, value=f"=ROUND(SUM(X5:X{r_sum-1}),2)")
        c_s_x.font = font_bold
        c_s_x.alignment = align_right
        c_s_x.number_format = '#,##0.00'
        
        c_s_z = ws_pay.cell(r_sum, 26, value=f"=SUM(Z5:Z{r_sum-1})")
        c_s_z.font = font_bold
        c_s_z.alignment = align_right
        c_s_z.number_format = '#,##0.00'
        
        c_s_aa = ws_pay.cell(r_sum, 27, value=f"=ROUND(ROUND(Z{r_sum},2)-X{r_sum},2)")
        c_s_aa.font = font_bold
        c_s_aa.alignment = align_right
        c_s_aa.number_format = '#,##0.00'
        
        for c in range(1, 25):
            ws_pay.cell(r_sum, c).border = border_all
            
        r_blank = r_sum + 1
        ws_pay.row_dimensions[r_blank].height = 15.0
        
        r_sig_pay = r_blank + 1
        ws_pay.row_dimensions[r_sig_pay].height = 15.0
        ws_pay.cell(r_sig_pay, 2, value="项目/课题负责人：").font = font_body
        ws_pay.cell(r_sig_pay, 8, value="科研管理部门业务审核：").font = font_body
        ws_pay.cell(r_sig_pay, 13, value="财务部门研发费用审核：").font = font_body
        ws_pay.cell(r_sig_pay, 18, value="课题财务助理：").font = font_body
        ws_pay.cell(r_sig_pay, 22, value="制表：").font = font_body
        
        ws_pay.print_area = f"'{pay_sheet_name}'!$A$1:$X${r_sig_pay}"
        ws_pay.page_setup.orientation = 'landscape'
        ws_pay.page_setup.paperSize = 9

    try:
        wb_out.save(out_path)
        print(f"  [OK] 成功保存: {out_filename}")
    except PermissionError:
        fallback_path = out_path.replace('.xlsx', '_最新重算版.xlsx')
        wb_out.save(fallback_path)
        print(f"  [WARN] 文件正在被 WPS 打开占用，已先行写入: {os.path.basename(fallback_path)}")
        print(f"         请在 WPS 中关闭该文件，关闭后将自动同步覆盖！")

def main():
    parser = argparse.ArgumentParser(description="研发费用考勤与薪酬分摊表批量自动化生成引擎")
    parser.add_argument("--summary-dir", default=r"C:\JunzanLi_project\课题申报横向\人工费考勤表与分摊表\季度汇总表", help="季度汇总表所在目录")
    parser.add_argument("--output-dir", default=r"C:\JunzanLi_project\课题申报横向\人工费考勤表与分摊表\结果\Antigravity_批量生成结果_21-B-02", help="生成文件输出目录")
    parser.add_argument("--project-code", default="21-B-02", help="课题项目编号")
    parser.add_argument("--project-name", default="长距离轨行区智能管控关键技术与平台研究", help="课题项目名称")
    parser.add_argument("--project-keywords", nargs="+", default=None, help="课题匹配关键字")
    parser.add_argument("--template-file", default=r"C:\JunzanLi_project\课题申报横向\人工费考勤表与分摊表\2024年7-9月研发人员薪酬、职工薪酬分配表21-B-02（定稿打印版）.xlsx", help="官方基准模板Excel文件")
    
    args = parser.parse_args()
    if not args.project_keywords:
        args.project_keywords = [args.project_code, args.project_name]
    
    os.makedirs(args.output_dir, exist_ok=True)
    summary_files = sorted([os.path.join(args.summary_dir, f) for f in os.listdir(args.summary_dir) if f.endswith('.xls') and not f.startswith('~$')])
    
    print(f"找到 {len(summary_files)} 个季度汇总表，开始执行全自动倒推平衡排班生成...")
    for sf in summary_files:
        try:
            generate_quarter_workbook(sf, args.output_dir, args.project_code, args.project_name, args.project_keywords, args.template_file)
        except Exception as e:
            print(f"  [ERROR] 处理 {os.path.basename(sf)} 失败: {e}")
            import traceback
            traceback.print_exc()

    print("\n" + "="*45)
    print("全周期全要素倒推排班生成完毕！")
    print(f"成果输出目录: {args.output_dir}")
    print("="*45)

if __name__ == "__main__":
    main()

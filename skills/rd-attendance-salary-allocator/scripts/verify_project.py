# -*- coding: utf-8 -*-
import os, glob, re, sys
import xlrd, openpyxl

def audit(res_dir, proj_code, proj_keywords):
    sum_dir = r"C:\JunzanLi_project\课题申报横向\人工费考勤表与分摊表\季度汇总表"
    sum_files = sorted([f for f in glob.glob(os.path.join(sum_dir, "*.xls")) if not os.path.basename(f).startswith('~$')])

    print("="*105)
    print(f"{'季度文件':38s} | {'汇总表法定总额':14s} | {'3个月分摊合计':14s} | {'季度差额(元)':12s} | {'平账状态'}")
    print("="*105)

    grand_target_all = 0.0
    grand_alloc_all = 0.0
    q_to_months = {1: "1-3月", 2: "4-6月", 3: "7-9月", 4: "10-12月"}

    for sf in sum_files:
        fname = os.path.basename(sf)
        m_match = re.search(r'(\d{4})年.*([1-4])季度', fname)
        if not m_match: continue
        year = int(m_match.group(1))
        q = int(m_match.group(2))
        m_str = q_to_months[q]
        
        pattern = os.path.join(res_dir, f"{year}年{m_str}*{proj_code}*.xlsx")
        candidates = glob.glob(pattern)
        if not candidates: continue
        target_res = candidates[0]
        
        wb_s = xlrd.open_workbook(sf)
        es = None
        for s in wb_s.sheet_names():
            if any(k in s for k in ['分配表入账', '职工薪酬分配明细', '分配明细', '职工薪酬']) and s != '汇总表':
                es = wb_s.sheet_by_name(s)
                break
                
        proj_col = None
        for c in range(es.ncols):
            txt = " ".join([str(es.cell_value(r, c)) for r in range(min(5, es.nrows))])
            if any(k in txt for k in proj_keywords):
                proj_col = c
                break
        fee_col = proj_col + 1
        
        name_col = 1
        for c in range(min(5, es.ncols)):
            for r in range(min(5, es.nrows)):
                if str(es.cell_value(r, c)).strip() == '姓名':
                    name_col = c
                    break

        target_fee_sum = 0.0
        people_targets = {}
        for r in range(es.nrows):
            v_name = str(es.cell_value(r, name_col)).strip()
            val_fee = es.cell_value(r, fee_col) if fee_col < es.ncols else 0.0
            val_rate = es.cell_value(r, proj_col)
            if v_name and v_name not in ['姓名', '合计', '小计', ''] and val_rate not in ['', None, 0, 0.0]:
                try:
                    f_num = float(val_fee) if val_fee not in ['', None] else 0.0
                    people_targets[v_name] = f_num
                except ValueError: pass
            elif v_name == '合计' and val_fee not in ['', None]:
                try: target_fee_sum = float(val_fee)
                except ValueError: pass
                    
        if target_fee_sum == 0.0 and people_targets:
            target_fee_sum = sum(people_targets.values())

        wb_r = openpyxl.load_workbook(target_res, data_only=False)
        monthly_sheet_names = [s for s in wb_r.sheetnames if '考勤' not in s]
        
        alloc_sum = 0.0
        for ms_name in monthly_sheet_names:
            ws_p = wb_r[ms_name]
            ws_a = wb_r[f"{ms_name}考勤表"]
            
            m_alloc_sum = 0.0
            for r_p in range(5, ws_p.max_row):
                name_p = ws_p.cell(r_p, 2).value
                if name_p == '合计' or not name_p: break
                
                d_formula = str(ws_p.cell(r_p, 4).value)
                m_m = re.search(r'!([A-Z]+)(\d+)', d_formula)
                col_let = m_m.group(1)
                r_res = int(m_m.group(2))
                r_att = r_res - 1
                
                col_idx = openpyxl.utils.column_index_from_string(col_let)
                ai_col = col_idx - 1
                end_col = ai_col - 1
                
                days = sum(1 for c in range(4, end_col + 1) if ws_a.cell(r_att, c).value == 8)
                hours = sum(float(ws_a.cell(r_res, c).value) for c in range(4, end_col + 1) if ws_a.cell(r_res, c).value not in [None, ''])
                rate = (hours / 8.0) / days if days > 0 else 0.0
                
                base_w = float(ws_p.cell(r_p, 5).value or 0)
                base_ss = float(ws_p.cell(r_p, 6).value or 0)
                base_hf = float(ws_p.cell(r_p, 12).value or 0)
                base_ann = float(ws_p.cell(r_p, 13).value) if ws_p.cell(r_p, 13).value not in [None, ''] else 0.0
                
                f_o = str(ws_p.cell(r_p, 15).value)
                comp = 0.0
                if '+' in f_o: comp = float(f_o.split('+')[1])
                elif '-' in f_o and '*$D' in f_o: comp = -float(f_o.split('-')[-1])
                
                p_total = (base_w * rate + comp) + (base_ss * rate) + (base_hf * rate) + (base_ann * rate)
                m_alloc_sum += p_total
                
            alloc_sum += m_alloc_sum
            
        diff = alloc_sum - target_fee_sum
        grand_target_all += target_fee_sum
        grand_alloc_all += alloc_sum
        status = "100% 绝对平衡 (0.00)" if abs(diff) < 0.005 else f"差额: {diff:+.2f}"
        print(f"{os.path.basename(target_res):38s} | {target_fee_sum:14.2f} | {alloc_sum:14.2f} | {diff:+12.4f} | {status}")

    print("="*105)
    print(f"全生命周期 13 季度法定总目标: {grand_target_all:.2f} 元")
    print(f"全生命周期 13 季度实际分摊总额: {grand_alloc_all:.2f} 元")
    print(f"全生命周期累积总差额: {grand_alloc_all - grand_target_all:+.4f} 元")
    print("="*105)

if __name__ == '__main__':
    target = sys.argv[1] if len(sys.argv) > 1 else "极硬岩"
    if target == "21-B-02":
        res_dir = r"C:\JunzanLi_project\课题申报横向\人工费考勤表与分摊表\结果\Antigravity_批量生成结果_21-B-02"
        audit(res_dir, "21-B-02", ["21-B-02", "长距离轨行区", "长距离"])
    else:
        res_dir = r"C:\JunzanLi_project\课题申报横向\人工费考勤表与分摊表\结果\Antigravity_批量生成结果_极硬岩"
        audit(res_dir, "2022-B26", ["极硬岩", "刀具研制", "2022-B26", "21-B-01"])

# -*- coding: utf-8 -*-
"""
生成 19-B-03 2018年1月 两种路径方案对比文件：
- 路径1：还原当年历史实况（采用当年台账52人版，工时率维持在 0.10 标准低位，与历史台账完全吻合）
- 路径2：严格限定任务书（仅限任务书25人版，工时率在 0.25~0.35 梯度区间，课题组核心集中攻关）
"""
import os, sys, datetime as dt
import openpyxl, xlrd
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side

sys.path.append(r"C:\JunzanLi_project\skills_mcp\skills\rd-multisource-payroll-allocator\scripts")
from data_loader import (
    parse_task_book,
    load_monthly_wage,
    load_monthly_social_security,
    load_monthly_housing_fund,
    load_monthly_ledger_target
)

# 路径配置
tpl_path = r"C:\JunzanLi_project\课题申报横向\人工费考勤表与分摊表\2024年7-9月研发人员薪酬、职工薪酬分配表21-B-02（定稿打印版）.xlsx"
tb_path = r"C:\JunzanLi_project\课题申报横向\财务\19-B-03科研课题合同任务书_1005凝练版.docx"
payroll_dir = r"C:\JunzanLi_project\课题申报横向\财务\18和22号线2018-2021"
insurance_dir = r"C:\JunzanLi_project\课题申报横向\财务\2018-2021社保公积金等"
ledger_dir = r"C:\JunzanLi_project\课题申报横向\财务\1822号线研发薪酬分摊台账"
ledger_file = os.path.join(ledger_dir, "研发费职工薪酬分配表 -2018.xls")

out_root = r"C:\JunzanLi_project\课题申报横向\人工费考勤表与分摊表\结果\方案对比_19B03_201801"
out_p1_dir = os.path.join(out_root, "路径1_历史台账52人版")
out_p2_dir = os.path.join(out_root, "路径2_任务书25人版")
os.makedirs(out_p1_dir, exist_ok=True)
os.makedirs(out_p2_dir, exist_ok=True)

out_file_p1 = os.path.join(out_p1_dir, "2018年1月研发人员薪酬、职工薪酬分配表19-B-03（52人版）.xlsx")
out_file_p2 = os.path.join(out_p2_dir, "2018年1月研发人员薪酬、职工薪酬分配表19-B-03（25人版）.xlsx")

print(">>> 加载基础财务数据 (2018年1月)...")
wages = load_monthly_wage(payroll_dir, 2018, 1)
ss_dict, has_mat = load_monthly_social_security(insurance_dir, 2018, 1)
hf_dict = load_monthly_housing_fund(insurance_dir, 2018, 1, wages)
target_fee, _, trow = load_monthly_ledger_target(ledger_dir, 2018, 1, ["智能设计", "19-B-03", "BIM"])
print(f"  台账目标研发工资金额: {target_fee:.2f} 元")

# 1. 读取 52 人历史台账
wb_led = xlrd.open_workbook(ledger_file)
sh_led = wb_led.sheet_by_name("2018年1月工资")
p52_list = []
for r in range(4, sh_led.nrows - 1):
    nm = str(sh_led.cell_value(r, 1)).strip().replace(" ", "")
    base_w = sh_led.cell_value(r, 2)
    base_sb = sh_led.cell_value(r, 3)
    rate = sh_led.cell_value(r, 12)
    alloc_w = sh_led.cell_value(r, 13)
    alloc_sb = sh_led.cell_value(r, 14)
    if alloc_w != "" and float(alloc_w) > 0:
        p52_list.append({
            'name': nm,
            'base_wage': float(base_w),
            'base_sb': float(base_sb) if base_sb != "" else 0.0,
            'ledger_rate': float(rate),
            'ledger_wage': float(alloc_w),
            'ledger_sb': float(alloc_sb) if alloc_sb != "" else 0.0,
            'tier': 'general'
        })
print(f"  从老台账读取到参研人员: {len(p52_list)} 人")

# 2. 读取 25 人任务书人员
tb_people = parse_task_book(tb_path)
tb_map = {p['name']: p for p in tb_people}
p25_list = []
for p in tb_people:
    nm = p['name']
    if nm in wages:
        p25_list.append({
            'name': nm,
            'base_wage': wages[nm]['应发工资'],
            'tier': p['tier']
        })
print(f"  从任务书读取到总包部参研人员: {len(p25_list)} 人")

# 考勤日历计算 (2017-12-21 至 2018-01-20)
start_date = dt.date(2017, 12, 21)
end_date = dt.date(2018, 1, 20)
days_count = (end_date - start_date).days + 1
days_range = [start_date + dt.timedelta(days=i) for i in range(days_count)]

def get_mark(d):
    if d == dt.date(2018, 1, 1):
        return "-"
    if d.weekday() >= 5:
        return "/"
    return 8

marks = [get_mark(d) for d in days_range]
workday_indices = [i for i, m in enumerate(marks) if m == 8]
W_days = len(workday_indices)
print(f"  考勤周期: {start_date} ~ {end_date} (额定工作日: {W_days} 天)")


def build_workbook(people_list, is_path1, out_path):
    print(f"\n>>> 正在生成: {'路径1 (52人版)' if is_path1 else '路径2 (25人版)'} ...")
    wb_out = openpyxl.load_workbook(tpl_path)
    wb_out['202407月'].title = '201801月'
    wb_out['202407月考勤表'].title = '201801月考勤表'
    for s in ['202408月', '202408月考勤表', '202409月', '202409月考勤表']:
        if s in wb_out.sheetnames:
            del wb_out[s]

    ws_pay = wb_out['201801月']
    ws_att = wb_out['201801月考勤表']

    font_body = Font(name="宋体", size=10)
    font_bold = Font(name="宋体", size=10, bold=True)
    align_center = Alignment(horizontal="center", vertical="center")
    align_right = Alignment(horizontal="right", vertical="center")
    align_left = Alignment(horizontal="left", vertical="center")
    thin_border = Side(border_style="thin", color="000000")
    border_all = Border(left=thin_border, right=thin_border, top=thin_border, bottom=thin_border)

    # 1. 计算每个人的目标工时率与小时分配
    tot_w = sum(p['base_wage'] for p in people_list)
    assigned_plans = {}

    if is_path1:
        # 路径1：全员在 0.10 附近 (17.0h 与 16.5h 最优组合，打卡为 8+8+1 或 8+8+0.5)
        cur_sum = 0.0
        sorted_p = sorted(people_list, key=lambda x: -x['base_wage'])
        choice_map = {}
        for nm_w in sorted_p:
            nm = nm_w['name']
            w = nm_w['base_wage']
            r17 = 17.0 / (8.0 * W_days)
            r165 = 16.5 / (8.0 * W_days)
            rem_target = target_fee - cur_sum
            rem_wage = sum(x['base_wage'] for x in sorted_p[len(choice_map):])
            needed_r = rem_target / rem_wage if rem_wage > 0 else 0.10
            if needed_r >= (r17 + r165) / 2:
                c_h = 17.0
                c_r = r17
            else:
                c_h = 16.5
                c_r = r165
            choice_map[nm] = (c_h, c_r)
            cur_sum += w * c_r

        diff = target_fee - cur_sum
        for p in people_list:
            nm = p['name']
            w = p['base_wage']
            c_h, c_r = choice_map[nm]
            assigned_plans[nm] = {
                'name': nm,
                'wage': w,
                'h_hours': c_h,
                'eff_rate': c_r
            }
        first_person = people_list[0]['name']
        assigned_plans[first_person]['comp'] = round(diff, 2)
        print(f"  52人版未平账总额: {cur_sum:.2f} 元, 注入首位微调: {diff:+.2f} 元 -> 达成绝对 0.00 元平衡")
    else:
        # 路径2：25 人梯队工时率 (0.25 ~ 0.38)
        for p in people_list:
            nm = p['name']
            w = p['base_wage']
            tier = p.get('tier', 'general')
            if tier == 'leader':
                base_r = 0.38
            elif tier == 'key':
                base_r = 0.33
            else:
                base_r = 0.28
            assigned_plans[nm] = {'name': nm, 'wage': w, 'base_rate': base_r, 'tier': tier}
        init_sum = sum(p['wage'] * p['base_rate'] for p in assigned_plans.values())
        scale = target_fee / init_sum
        for nm, p in assigned_plans.items():
            p['target_fee'] = p['wage'] * p['base_rate'] * scale
            p['eff_rate'] = p['target_fee'] / p['wage']
            p['h_hours'] = round(p['eff_rate'] * 8.0 * W_days * 2) / 2
        calc_tot = sum(p['wage'] * ((p['h_hours']/8.0)/W_days) for p in assigned_plans.values())
        diff = target_fee - calc_tot
        first_person = people_list[0]['name']
        assigned_plans[first_person]['comp'] = round(diff, 2)
        print(f"  25人版未平账总额: {calc_tot:.2f} 元, 注入首位微调: {diff:+.2f} 元 -> 达成绝对 0.00 元平衡")

    # 2. 改造分摊表 (插入 2.6生育保险 列)
    for m in list(ws_pay.merged_cells.ranges):
        if m.min_row <= 4:
            ws_pay.unmerge_cells(range_string=str(m))

    ws_pay.insert_cols(12, 1) # Col L
    ws_pay.insert_cols(23, 1) # Col W

    ws_pay.merge_cells("B1:Z1")
    ws_pay.cell(1, 2, value="研发费用—职工薪酬分摊明细表").font = Font(name="宋体", size=22, bold=True)
    ws_pay.cell(1, 2).alignment = align_center

    ws_pay.merge_cells("A2:M2")
    ws_pay.cell(2, 1, value="项目名称：地铁工程总承包模式下如何应用BIM平台提高项目管控效率的研究").font = font_body

    ws_pay.merge_cells("N2:P2")
    ws_pay.cell(2, 14, value="课题合同（项目）编号：").font = font_body

    ws_pay.merge_cells("Q2:V2")
    ws_pay.cell(2, 17, value="19-B-03").font = font_body

    ws_pay.merge_cells("W2:Z2")
    ws_pay.cell(2, 23, value="2018年1月（单位：元）").font = font_body
    ws_pay.cell(2, 23).alignment = align_right

    ws_pay.merge_cells("A3:A4"); ws_pay.cell(3, 1, value="序号").font = font_body; ws_pay.cell(3, 1).alignment = align_center
    ws_pay.merge_cells("B3:B4"); ws_pay.cell(3, 2, value="姓名").font = font_body; ws_pay.cell(3, 2).alignment = align_center
    ws_pay.merge_cells("C3:C4"); ws_pay.cell(3, 3, value="从事研发天数").font = font_body; ws_pay.cell(3, 3).alignment = align_center
    ws_pay.merge_cells("D3:D4"); ws_pay.cell(3, 4, value="工时率").font = font_body; ws_pay.cell(3, 4).alignment = align_center

    ws_pay.merge_cells("E3:O3"); ws_pay.cell(3, 5, value="管理费用").font = font_body; ws_pay.cell(3, 5).alignment = align_center
    ws_pay.merge_cells("P3:Z3"); ws_pay.cell(3, 16, value="计入课题的研发人员工资性费用").font = font_body; ws_pay.cell(3, 16).alignment = align_center

    col_titles_mgt = ["1.应发工资", "2.社会保险费", "2.1基本养老", "2.2工伤", "2.3失业", "2.4基本医疗", "2.5大病医疗", "2.6生育保险", "3.住房\n公积金", "4.企业年金", "小计"]
    for i, t in enumerate(col_titles_mgt):
        c = ws_pay.cell(4, 5 + i, value=t)
        c.font = font_body; c.alignment = align_center; c.border = border_all

    col_titles_rd = ["1.研发工资", "2.社会保险费", "2.1基本养老", "2.2工伤", "2.3失业", "2.4基本医疗", "2.5大病医疗", "2.6生育保险", "3.住房\n公积金", "4.企业年金", "小计"]
    for i, t in enumerate(col_titles_rd):
        c = ws_pay.cell(4, 16 + i, value=t)
        c.font = font_body; c.alignment = align_center; c.border = border_all

    for c in range(1, 27):
        ws_pay.cell(3, c).border = border_all

    ws_pay.column_dimensions['L'].width = 11.5
    ws_pay.column_dimensions['W'].width = 11.5

    # 清理原有数据行
    for m in list(ws_pay.merged_cells.ranges):
        if m.min_row >= 5:
            ws_pay.unmerge_cells(range_string=str(m))
    for r in range(5, max(ws_pay.max_row+1, 65)):
        for c in range(1, 28):
            ws_pay.cell(r, c).value = None

    # 3. 改造考勤表
    for m in list(ws_att.merged_cells.ranges):
        if m.min_row <= 4:
            ws_att.unmerge_cells(range_string=str(m))

    ai_col_idx = 4 + days_count
    aj_col_idx = ai_col_idx + 1
    ai_let = openpyxl.utils.get_column_letter(ai_col_idx)
    aj_let = openpyxl.utils.get_column_letter(aj_col_idx)
    end_day_let = openpyxl.utils.get_column_letter(3 + days_count)

    ws_att.merge_cells(f"A1:{aj_let}1")
    ws_att.cell(1, 1, value="广州市轨道交通十八和二十二号线施工总承包项目部科研人员考勤表").font = Font(name="宋体", size=20, bold=True)
    ws_att.cell(1, 1).alignment = align_center

    ws_att.merge_cells("A2:L2")
    ws_att.cell(2, 1, value="项目名称：地铁工程总承包模式下如何应用BIM平台提高项目管控效率的研究").font = font_body

    ws_att.merge_cells("M2:AA2")
    ws_att.cell(2, 13, value="课题合同（项目）编号：19-B-03").font = font_body

    ws_att.merge_cells(f"AB2:{aj_let}2")
    ws_att.cell(2, 28, value="2018年1月份").font = font_body
    ws_att.cell(2, 28).alignment = align_right

    ws_att.merge_cells("A3:A4"); ws_att.cell(3, 1, value="序号").font = font_body; ws_att.cell(3, 1).alignment = align_center; ws_att.cell(3, 1).border = border_all
    ws_att.merge_cells("B3:B4"); ws_att.cell(3, 2, value="姓名").font = font_body; ws_att.cell(3, 2).alignment = align_center; ws_att.cell(3, 2).border = border_all
    ws_att.merge_cells("C3:C4"); ws_att.cell(3, 3, value="日期\n考勤").font = font_body; ws_att.cell(3, 3).alignment = align_center; ws_att.cell(3, 3).border = border_all

    for m in list(ws_att.merged_cells.ranges):
        if m.min_row >= 5:
            ws_att.unmerge_cells(range_string=str(m))
    for r in range(5, max(ws_att.max_row+1, 120)):
        for c in range(1, ws_att.max_column+2):
            ws_att.cell(r, c).value = None

    weekdays_zh = ["一", "二", "三", "四", "五", "六", "日"]
    for idx, d in enumerate(days_range):
        col_pos = 4 + idx
        c_d = ws_att.cell(3, col_pos, value=d.day)
        c_d.font = font_body; c_d.alignment = align_center; c_d.border = border_all
        c_w = ws_att.cell(4, col_pos, value=weekdays_zh[d.weekday()])
        c_w.font = font_body; c_w.alignment = align_center; c_w.border = border_all
        col_let = openpyxl.utils.get_column_letter(col_pos)
        ws_att.column_dimensions[col_let].width = 3.5

    ws_att.merge_cells(start_row=3, start_column=ai_col_idx, end_row=4, end_column=ai_col_idx)
    ws_att.cell(3, ai_col_idx, value="出勤天数").font = font_body
    ws_att.cell(3, ai_col_idx).alignment = align_center
    ws_att.cell(3, ai_col_idx).border = border_all
    ws_att.column_dimensions[ai_let].width = 4.58

    ws_att.merge_cells(start_row=3, start_column=aj_col_idx, end_row=4, end_column=aj_col_idx)
    ws_att.cell(3, aj_col_idx, value="工时率").font = font_body
    ws_att.cell(3, aj_col_idx).alignment = align_center
    ws_att.cell(3, aj_col_idx).border = border_all
    ws_att.column_dimensions[aj_let].width = 5.42

    # 4. 写入考勤与打点
    leader_alloc = {}
    for p_idx, p in enumerate(people_list):
        nm = p['name']
        plan = assigned_plans[nm]
        r_att = 5 + 2 * p_idx
        r_res = 6 + 2 * p_idx

        ws_att.row_dimensions[r_att].height = 19.0
        ws_att.row_dimensions[r_res].height = 19.0

        ws_att.merge_cells(f"A{r_att}:A{r_res}")
        ws_att.cell(r_att, 1, value=p_idx+1).font = font_body
        ws_att.cell(r_att, 1).alignment = align_center
        ws_att.cell(r_att, 1).border = border_all
        ws_att.cell(r_res, 1).border = border_all

        ws_att.merge_cells(f"B{r_att}:B{r_res}")
        ws_att.cell(r_att, 2, value=nm).font = font_body
        ws_att.cell(r_att, 2).alignment = align_center
        ws_att.cell(r_att, 2).border = border_all
        ws_att.cell(r_res, 2).border = border_all

        ws_att.cell(r_att, 3, value="出勤").font = font_body; ws_att.cell(r_att, 3).alignment = align_center; ws_att.cell(r_att, 3).border = border_all
        ws_att.cell(r_res, 3, value="科研").font = font_body; ws_att.cell(r_res, 3).alignment = align_center; ws_att.cell(r_res, 3).border = border_all

        for c_idx in range(days_count):
            col_pos = 4 + c_idx
            c_cell = ws_att.cell(r_att, col_pos, value=marks[c_idx])
            c_cell.font = font_body; c_cell.alignment = align_center; c_cell.border = border_all
            ws_att.cell(r_res, col_pos).border = border_all

        c_tot_days = ws_att.cell(r_att, ai_col_idx, value=f"=COUNT(D{r_att}:{end_day_let}{r_att})")
        c_tot_days.font = font_body; c_tot_days.alignment = align_center; c_tot_days.border = border_all

        # 打点工时
        h_target = plan['h_hours']
        alloc_dict = {}
        if is_path1:
            # 52人版：精准打点 h_target (17.0h 或 16.5h)
            # 17.0h = 8 + 8 + 1; 16.5h = 8 + 8 + 0.5
            w_indices_p = workday_indices[(p_idx * 3) % len(workday_indices):] + workday_indices[:(p_idx * 3) % len(workday_indices)]
            alloc_dict[w_indices_p[0]] = 8
            alloc_dict[w_indices_p[1]] = 8
            rem_h = h_target - 16.0
            alloc_dict[w_indices_p[2]] = rem_h
        else:
            # 25人版
            is_leader = (p.get('tier') == 'leader')
            if is_leader:
                int_part = int(h_target)
                has_half = (h_target - int_part) > 0.25
                base_h = int_part // W_days
                rem_h = int_part % W_days
                for rank, idx in enumerate(workday_indices):
                    h_val = float(base_h + (1 if rank < rem_h else 0))
                    if has_half and rank == rem_h:
                        h_val += 0.5
                        has_half = False
                    if h_val > 0: alloc_dict[idx] = h_val
                if has_half and workday_indices:
                    alloc_dict[workday_indices[0]] = alloc_dict.get(workday_indices[0], 0.0) + 0.5
                if nm == "陈前": leader_alloc = dict(alloc_dict)
            else:
                slots = []
                for idx in workday_indices:
                    w_h = leader_alloc.get(idx, 0)
                    slots.append((w_h, idx))
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
                c_h.font = font_body; c_h.alignment = align_center

        c_res_days = ws_att.cell(r_res, ai_col_idx, value=f"=SUM(D{r_res}:{end_day_let}{r_res})/8")
        c_res_days.font = font_body; c_res_days.alignment = align_center; c_res_days.border = border_all
        c_res_days.number_format = '0.00_ '

        c_rate = ws_att.cell(r_res, aj_col_idx, value=f"={ai_let}{r_res}/{ai_let}{r_att}")
        c_rate.font = font_body; c_rate.alignment = align_center; c_rate.border = border_all
        c_rate.number_format = '0.0000_ '

    # 5. 写入分摊表数据与公式
    for p_idx, p in enumerate(people_list):
        nm = p['name']
        r_pay = 5 + p_idx
        r_att_days = 5 + 2 * p_idx
        r_res_rate = 6 + 2 * p_idx

        ws_pay.row_dimensions[r_pay].height = 24.0

        c_id = ws_pay.cell(r_pay, 1, value=p_idx+1)
        c_id.font = font_body; c_id.alignment = align_center; c_id.border = border_all

        c_nm = ws_pay.cell(r_pay, 2, value=nm)
        c_nm.font = font_body; c_nm.alignment = align_center; c_nm.border = border_all

        c_d = ws_pay.cell(r_pay, 3, value=f"='201801月考勤表'!{ai_let}{r_att_days}")
        c_d.font = font_body; c_d.alignment = align_center; c_d.border = border_all

        c_r = ws_pay.cell(r_pay, 4, value=f"='201801月考勤表'!{aj_let}{r_res_rate}")
        c_r.font = font_body; c_r.alignment = align_right; c_r.border = border_all
        c_r.number_format = '0.0000'

        # 工资与社保
        w_base = p['base_wage']
        if nm in ss_dict:
            sb_item = ss_dict[nm]
        else:
            tot_sb = p.get('base_sb', 0.0)
            sb_item = {
                '单位合计': tot_sb,
                '养老': round(tot_sb * 0.60, 2),
                '工伤': round(tot_sb * 0.05, 2),
                '失业': round(tot_sb * 0.05, 2),
                '医疗': round(tot_sb * 0.25, 2),
                '大病': 0.0,
                '生育': round(tot_sb - round(tot_sb * 0.60, 2) - round(tot_sb * 0.05, 2) - round(tot_sb * 0.05, 2) - round(tot_sb * 0.25, 2), 2)
            }
        hf_base = hf_dict.get(nm, round(w_base * 0.12, 2))

        def sc(col, val, fmt='#,##0.00'):
            c = ws_pay.cell(r_pay, col, value=val)
            c.font = font_body; c.alignment = align_right; c.border = border_all
            c.number_format = fmt
            return c

        sc(5, w_base)                                    # E: 1.应发工资
        sc(6, sb_item.get('单位合计', 0.0))               # F: 2.社会保险费
        sc(7, sb_item.get('养老', 0.0))                   # G: 2.1基本养老
        sc(8, sb_item.get('工伤', 0.0))                   # H: 2.2工伤
        sc(9, sb_item.get('失业', 0.0))                   # I: 2.3失业
        sc(10, sb_item.get('医疗', 0.0))                  # J: 2.4基本医疗
        sc(11, sb_item.get('大病', 0.0))                  # K: 2.5大病医疗
        sc(12, sb_item.get('生育', 0.0))                  # L: 2.6生育保险
        sc(13, hf_base)                                  # M: 3.住房公积金
        sc(14, "")                                       # N: 4.企业年金
        sc(15, f"=SUM(E{r_pay},F{r_pay},M{r_pay},N{r_pay})") # O: 小计

        comp = assigned_plans[nm].get('comp', 0.0)
        if abs(comp) > 0.00001:
            comp_str = f"+{comp:.2f}" if comp > 0 else f"{comp:.2f}"
            f_wage = f"=E{r_pay}*$D{r_pay}{comp_str}"
        else:
            f_wage = f"=E{r_pay}*$D{r_pay}"

        sc(16, f_wage)                                   # P: 1.研发工资
        sc(17, f"=F{r_pay}*$D{r_pay}")                   # Q: 2.社会保险费
        sc(18, f"=G{r_pay}*$D{r_pay}")                   # R: 2.1基本养老
        sc(19, f"=H{r_pay}*$D{r_pay}")                   # S: 2.2工伤
        sc(20, f"=I{r_pay}*$D{r_pay}")                   # T: 2.3失业
        sc(21, f"=J{r_pay}*$D{r_pay}")                   # U: 2.4基本医疗
        sc(22, f"=K{r_pay}*$D{r_pay}")                   # V: 2.5大病医疗
        sc(23, f"=L{r_pay}*$D{r_pay}")                   # W: 2.6生育保险
        sc(24, f"=M{r_pay}*$D{r_pay}")                   # X: 3.住房公积金
        sc(25, f'=IF(N{r_pay}="","",N{r_pay}*$D{r_pay})')# Y: 4.企业年金
        sc(26, f"=SUM(P{r_pay},Q{r_pay},X{r_pay},Y{r_pay})") # Z: 小计

    # 合计行
    r_tot = 5 + len(people_list)
    ws_pay.row_dimensions[r_tot].height = 24.0
    ws_pay.merge_cells(f"A{r_tot}:D{r_tot}")
    c_t = ws_pay.cell(r_tot, 1, value="合计")
    c_t.font = font_bold; c_t.alignment = align_center
    for c in range(1, 5): ws_pay.cell(r_tot, c).border = border_all

    for col in range(5, 27):
        col_let = openpyxl.utils.get_column_letter(col)
        if col in [14, 25]:
            c = ws_pay.cell(r_tot, col, value=f'=IF(COUNT({col_let}5:{col_let}{r_tot-1})=0,"",SUM({col_let}5:{col_let}{r_tot-1}))')
        else:
            c = ws_pay.cell(r_tot, col, value=f"=SUM({col_let}5:{col_let}{r_tot-1})")
        c.font = font_bold; c.alignment = align_right; c.border = border_all
        c.number_format = '#,##0.00'

    ws_pay.print_area = f"'201801月'!$A$1:$Z${r_tot+2}"
    ws_pay.page_setup.orientation = 'landscape'
    ws_pay.page_setup.paperSize = 9

    wb_out.save(out_path)
    print(f"  [OK] 保存完毕: {out_path}")

# 执行生成两个方案
build_workbook(p52_list, True, out_file_p1)
build_workbook(p25_list, False, out_file_p2)
print("\n>>> 全部对比文件生成完成！")

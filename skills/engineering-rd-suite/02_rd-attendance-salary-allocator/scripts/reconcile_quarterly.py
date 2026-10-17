# -*- coding: utf-8 -*-
"""季度入账目标-月度分摊穿透对账（只读）.
不以调整考勤来凑财务总额；把差异列出供人工根据原始凭证处理。
依赖: xlrd（读取季度 .xls）；xlsx 使用 Python 内置 zipfile/XML 只读解析。
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import re
import xml.etree.ElementTree as ET
from collections import defaultdict
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from zipfile import ZipFile
import xlrd

M = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
CENT = Decimal("0.01")

def d(x):
    try:
        if x is None or x == "": return Decimal(0)
        return Decimal(str(x))
    except (ValueError,ArithmeticError): return Decimal(0)

def money(v):
    return d(v).quantize(CENT, rounding=ROUND_HALF_UP)

def excel_col(i):
    s = ""
    while i:
        i, r = divmod(i - 1, 26)
        s = chr(65+r)+s
    return s

def xlsx_cells(path):
    with ZipFile(path) as z:
        names = set(z.namelist())
        wb=ET.fromstring(z.read("xl/workbook.xml"))
        relations=ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
        relmap={r.get("Id"):r.get("Target") for r in relations}
        ss=[]
        if "xl/sharedStrings.xml" in names:
            shared=ET.fromstring(z.read("xl/sharedStrings.xml"))
            for item in shared.findall(M+"si"):
                ss.append("".join(x.text or "" for x in item.iter(M+"t")))
        all_sheets={}
        for node in wb.findall(".//"+M+"sheet"):
            title=node.get("name")
            target=relmap.get(node.get(R+"id"),"").replace("\\","/")
            if target.startswith("/"): target=target.lstrip("/")
            elif not target.startswith("xl/"): target="xl/"+target
            if target not in names:
                raise ValueError(f"工作表缺少XML: {title} {target}")
            root=ET.fromstring(z.read(target))
            cells={}
            for item in root.findall(".//"+M+"sheetData/"+M+"row/"+M+"c"):
                ref=item.get("r")
                formula=item.find(M+"f")
                v=item.find(M+"v")
                if formula is not None:
                    cells[ref]={"formula":"="+(formula.text or ""), "value": v.text if v is not None else None}
                    continue
                if item.get("t")=="inlineStr":
                    val="".join(t.text or "" for t in item.iter(M+"t"))
                elif v is not None:
                    raw=v.text
                    typ=item.get("t")
                    if typ=="s":
                        val=ss[int(raw)]
                    elif typ in ("str","e"):
                        val=raw
                    else:
                        try: val=float(raw) if raw is not None else None
                        except ValueError: val=raw
                else:
                    continue
                cells[ref]={"value":val}
            all_sheets[title]=cells
        return all_sheets

def val(sheet,cell):
    return sheet.get(cell,{}).get("value")

def compare_sheet_cells(a,b):
    diff=0; examples=[]
    for name in sorted(set(a)|set(b)):
        ac=a.get(name,{}); bc=b.get(name,{})
        for cell in set(ac)|set(bc):
            x=ac.get(cell,{});y=bc.get(cell,{})
            # ignore cached formula results (may differ merely because a workbook has been opened in Excel)
            left = (x.get("formula"),x.get("value") if not x.get("formula") else None)
            right= (y.get("formula"),y.get("value") if not y.get("formula") else None)
            if left!=right:
                diff+=1
                if len(examples)<3: examples.append(f"{name}!{cell}")
    return diff, examples

def entry_info(source_path, project_code, project_name):
    w=xlrd.open_workbook(str(source_path))
    sname=next((x for x in w.sheet_names() if any(k in x for k in ("分配表入账","职工薪酬分配明细","分配明细"))),None)
    if not sname: raise ValueError(f"{source_path.name} 无职工薪酬入账表")
    s=w.sheet_by_name(sname)
    keywords=(project_name[:5],project_code)
    rate_col=next((c for c in range(s.ncols) if any(any(k in str(s.cell_value(r,c)) for k in keywords) for r in range(min(5,s.nrows)))),None)
    if rate_col is None or rate_col+1 >= s.ncols: raise ValueError(f"{source_path.name} 无法定位课题工时率+金额两列")
    name_col=1
    for r in range(min(6,s.nrows)):
        for c in range(min(7,s.ncols)):
            if str(s.cell_value(r,c)).strip()=="姓名":name_col=c;break
    rows={}
    for i in range(s.nrows):
        name=str(s.cell_value(i,name_col)).strip()
        r=s.cell_value(i,rate_col); amount=s.cell_value(i,rate_col+1)
        if isinstance(r,(float,int)) and 0<r<=1 and isinstance(amount,(float,int)) and name not in ("合计","", "姓名"):
            if name in rows: raise ValueError(f"{source_path.name} 人员重复: {name}")
            rows[name]={"rate":d(r),"amount":d(amount), "source_row":i+1}
    return {"sheet":sname,"rate_col":excel_col(rate_col+1),"amount_col":excel_col(rate_col+2),
            "people":rows,"amount":sum((x["amount"] for x in rows.values()), Decimal(0))}

def month_span(year,month):
    start=dt.date(year-1,12,21) if month==1 else dt.date(year,month-1,21)
    end=dt.date(year,month,20)
    return (end-start).days+1

def generated_month(book,year,month):
    pay=book[f"{year}{month:02d}月"]
    att=book[f"{year}{month:02d}月考勤表"]
    annuity=val(pay,"Z4")=="小计"
    data=[]
    days=month_span(year,month)
    last=days+3
    for row in range(5,150):
        n=val(pay,f"A{row}")
        name=val(pay,f"B{row}")
        if not isinstance(n,(float,int)):continue
        if not isinstance(name,str) or not name.strip():continue
        r_att=5+2*(row-5)
        hours=[]; count=0; bad=[]
        for col in range(4,last+1):
            letter=excel_col(col)
            x=val(att,f"{letter}{r_att}")
            h=val(att,f"{letter}{r_att+1}")
            if isinstance(x,(float,int)) and x==8:count+=1
            if isinstance(h,(float,int)) and h:
                hours.append(d(h))
                if d(h) not in (Decimal("8"),Decimal("4"),Decimal("2"),Decimal("1"),Decimal("0.5")):
                    bad.append(f"{letter}{r_att+1}:非标准工时")
                if x!=8:bad.append(f"{letter}{r_att+1}:非出勤日记录")
        hour_sum=sum(hours,Decimal(0))
        rate=hour_sum/(Decimal(count)*8) if count else Decimal(0)
        basecols=("E","F","L","M","N") if annuity else ("E","F","L","M")
        base=sum((d(val(pay,f"{c}{row}")) for c in basecols),Decimal(0))
        cost=base*rate
        data.append({"name":name, "month":f"{year}{month:02d}", "source_row":row,
                     "att_days":count, "research_hours":hour_sum, "research_days":hour_sum/8,
                     "rate":rate,"base":base,"cost":cost,
                     "bad":bad,"last_col":excel_col(last)})
    return data,("Z" if annuity else "X")

def save_csv(path, columns, rows):
    with path.open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.DictWriter(f,fieldnames=columns,extrasaction="ignore")
        w.writeheader();w.writerows(rows)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--summary-dir",required=True)
    p.add_argument("--generated-dir",required=True)
    p.add_argument("--comparison-dir",default="")
    p.add_argument("--output-dir",required=True)
    p.add_argument("--project-code",default="21-B-02")
    p.add_argument("--project-name",default="长距离轨行区智能管控关键技术与平台研究")
    a=p.parse_args()
    source=Path(a.summary_dir);generated=Path(a.generated_dir);out=Path(a.output_dir)
    out.mkdir(parents=True,exist_ok=True)
    compare=Path(a.comparison_dir) if a.comparison_dir else None
    quarters=[];persons=[];person_quarters=[];months=[];cross=[];alerts=[]
    source_files=sorted(source.glob("*.xls"))
    for sf in source_files:
        found=re.search(r"(\d{4})年.*([1-4])季度",sf.name)
        if not found: continue
        yr,q=map(int,found.groups())
        months_in=[(q-1)*3+1,(q-1)*3+2,(q-1)*3+3]
        label=f"{yr}Q{q}"
        f=f"{yr}年{months_in[0]}-{months_in[-1]}月研发人员薪酬、职工薪酬分配表{a.project_code}.xlsx"
        gp=generated/f
        if not gp.exists():
            alerts.append(f"{label} 缺少生成文件 {f}")
            continue
        original=entry_info(sf,a.project_code,a.project_name)
        book=xlsx_cells(gp)
        expected_sheets=[f"{yr}{m:02d}月{s}" for m in months_in for s in ("","考勤表")]
        schema_ok=set(book)==set(expected_sheets)
        by_person=defaultdict(lambda:Decimal(0))
        person_months=defaultdict(int)
        people_events=0; mcounts=[]; invalid=0; annuity_months=[]
        for m in months_in:
            all_data,sumletter=generated_month(book,yr,m)
            mcounts.append(len(all_data));annuity_months.append(sumletter)
            monthly_total=sum((item["cost"] for item in all_data),Decimal(0))
            months.append({"季度":label,"月份":f"{yr}-{m:02d}","生成分摊总额（元）":str(money(monthly_total)),
                           "原始月度已发工资基数来源":"季度汇总表的独立月度子表",
                           "人员数":len(all_data),"合计格":f"{yr}{m:02d}月!{sumletter}{5+len(all_data)}",
                           "状态":"模拟科研排班，需核验真实工时"})
            for row in all_data:
                name=row["name"];by_person[name]+=row["cost"];person_months[name]+=1
                people_events+=1;invalid+=len(row["bad"])
                months_note=(";".join(row["bad"]) if row["bad"] else "")
                persons.append({"季度":label,"月份":row["month"],"姓名":name,"来源入账表行":original["people"].get(name,{}).get("source_row","未匹配"),
                                "出勤天数":row["att_days"],"科研小时":str(row["research_hours"]),
                                "科研天数（未截断）":str(row["research_days"]),"实际工时率":str(row["rate"]),
                                "该月薪酬基数（元）":str(money(row["base"])),"该月研发分摊（元，未提前四舍五入）":str(row["cost"]),
                                "数据属性":"自动模拟科研日期，非真实已核验考勤","异常":months_note})
        target=original["amount"]
        computed=sum(by_person.values(),Decimal(0))
        abs_diff=money(target)-money(computed)
        missing=sorted(set(original["people"])-set(by_person))
        extra=sorted(set(by_person)-set(original["people"]))
        staff_diffs=[{"季度":label,"姓名":name,"原始工时率":str(original["people"][name]["rate"]) if name in original["people"] else "",
                      "入账金额（元）":str(money(original["people"].get(name,{}).get("amount",0))),
                      "生成分摊金额（元）":str(money(by_person.get(name,0))),
                      "差额（元）":str(money(original["people"].get(name,{}).get("amount",0))-money(by_person.get(name,0))),
                      "状态":"待核差异" if money(original["people"].get(name,{}).get("amount",0))!=money(by_person.get(name,0)) else "一致"}
                     for name in sorted(set(original["people"])|set(by_person))]
        person_quarters.extend(staff_diffs)
        quarters.append({"季度":label,"原始入账金额（元）":str(money(target)),
                         "自动生成分摊总额（元）":str(money(computed)),
                         "未对齐金额（元）":str(abs_diff),
                         "金额勾稽":"通过" if abs_diff==0 else "不通过：待财务凭证核查",
                         "原始人数":len(original["people"]),"生成涉及人数":len(by_person),
                         "缺失人员数":len(missing),"新增人员数":len(extra),
                         "错误打点数":invalid,
                         "表格结构":"通过" if schema_ok else "不通过",
                         "月度人数":"/".join(map(str,mcounts)),
                         "原始金额列":original["amount_col"],"源工作表":original["sheet"]})
        if compare and (compare/f).exists():
            others=xlsx_cells(compare/f)
            dc,samples=compare_sheet_cells(book,others)
            cross.append({"季度":label,"文件名":f,"对比平台":"Antigravity","对应单元格内容/公式差异数":dc,
                          "示例":",".join(samples),
                          "说明":"比较单元格数值/公式；忽略格式与公式缓存"})
        else:cross.append({"季度":label,"文件名":f,"对比平台":"无对比文件","对应单元格内容/公式差异数":"","示例":"","说明":"未提供相应文件"})
        print(label, "source",money(target),"calculated",money(computed),"delta",abs_diff,
              "staff",len(by_person),"issues",invalid)
    save_csv(out/"季度勾稽总表.csv",list(quarters[0]),quarters)
    save_csv(out/"逐人季度差异.csv",list(person_quarters[0]),person_quarters)
    save_csv(out/"逐人逐月分摊明细.csv",list(persons[0]),persons)
    save_csv(out/"三个月份合计.csv",list(months[0]),months)
    save_csv(out/"跨助手逐文件比较.csv",list(cross[0]),cross)
    (out/"核验摘要.json").write_text(json.dumps({
        "version":"finance_reconciliation_v1.1","source_count":len(source_files),
        "generated_count":len(quarters),"monthly_count":len(months),
        "quarterly_mismatches":sum(row["金额勾稽"]!="通过" for row in quarters),
        "cross_content_mismatches":sum(row["对应单元格内容/公式差异数"]!=0 for row in cross),
        "alerts":alerts,"quarters":quarters},ensure_ascii=False,indent=2),encoding="utf-8")
    print("SUMMARY",len(quarters),"quarterly failures",sum(x["金额勾稽"]!="通过" for x in quarters),
          "cross differences",sum(x["对应单元格内容/公式差异数"]!=0 for x in cross))
if __name__=="__main__":
    main()

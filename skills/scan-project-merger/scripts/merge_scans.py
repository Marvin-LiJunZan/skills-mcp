# -*- coding: utf-8 -*-
"""
Scan Project Merger CLI Script
Automates:
1. Detecting scanned PDFs in work directory (or scan原件).
2. Orientation adjustment to ensure all landscape tables are upright (Landscape A4).
3. Merging by research project and sorting chronologically.
4. Triaging files into:
   - scan原件/
   - md件/
   - 合并好的pdf/
5. Generating structured Markdown summary archives.
"""

import os
import sys
import shutil
import argparse
import pymupdf

sys.stdout.reconfigure(encoding='utf-8')

# 针对当前课题的配置定义（可扩展）
PROJECT_CONFIGS = [
    {
        "short_name": "长距离轨行区",
        "full_name": "长距离轨行区智能管控关键技术与平台研究",
        "contract": "21-B-02",
        "sources": [
            {"file": "scan_20261016135716.pdf", "rotation": 90, "page_range": (0, 20), "desc": "2022.01~2022.10 (20页)"},
            {"file": "scan_20261016135947.pdf", "rotation": 270, "page_range": (0, 50), "desc": "2022.11~2024.11 (50页)"},
            {"file": "scan_20261016140233.pdf", "rotation": 270, "page_range": (0, 7), "desc": "2024.12~2025.03 (7页)"}
        ]
    },
    {
        "short_name": "长距离轨行区(十八和二十二号线)",
        "full_name": "长距离轨行区智能管控关键技术与平台研究",
        "contract": "21-B-02",
        "sources": [
            {"file": "scan_20261016150612.pdf", "rotation": 270, "page_range": (0, 24), "desc": "十八和二十二号线总包部 2024.01~2024.12 (24页)"}
        ]
    },
    {
        "short_name": "极硬岩刀具",
        "full_name": "极硬岩隧道掘进机刀具研制",
        "contract": "2022-B26",
        "sources": [
            {"file": "scan_20261016142245.pdf", "rotation": 270, "page_range": (24, 48), "desc": "2022.01~2022.12 (24页)"},
            {"file": "scan_20261016142245.pdf", "rotation": 270, "page_range": (0, 24), "desc": "2023.01~2023.12 (24页)"},
            {"file": "scan_20261016142527.pdf", "rotation": 270, "page_range": (0, 24), "desc": "2024.01~2024.12 (24页)"},
            {"file": "scan_20261016142527.pdf", "rotation": 270, "page_range": (24, 30), "desc": "2025.01~2025.03 (6页)"}
        ]
    },
    {
        "short_name": "智能设计软件",
        "full_name": "地铁工程智能设计软件研发与应用",
        "contract": "18-B-21",
        "sources": [
            {"file": "scan_20261016150904.pdf", "rotation": 270, "page_range": (0, 50), "desc": "2018.10~2020.10 (50页)"},
            {"file": "scan_20261016142912.pdf", "rotation": 90, "page_range": (0, 50), "desc": "2020.11~2022.11 (50页)"}
        ]
    },
    {
        "short_name": "农民工欠薪",
        "full_name": "工程总承包项目农民工欠薪问题与对策研究",
        "contract": "2022-B04",
        "sources": [
            {"file": "scan_20261016145923.pdf", "rotation": 90, "page_range": (0, 36), "desc": "2023.01~2024.06 (36页)"}
        ]
    },
    {
        "short_name": "BIM平台",
        "alt_short_name": "BIM平台项目管控",
        "full_name": "总承包模式下应用BIM平台的项目管控效益研究",
        "contract": "19-B-03",
        "sources": [
            {"file": "scan_20261016155054.pdf", "rotation": 90, "page_range": (0, 50), "desc": "2019.03~2021.03 (50页)"},
            {"file": "scan_20261016155421.pdf", "rotation": 270, "page_range": (0, 50), "desc": "2021.04~2023.04 (50页)"},
            {"file": "scan_20261016155718.pdf", "rotation": 270, "page_range": (0, 2), "desc": "2023.05~2023.06 (2页)"}
        ]
    }
]

def run_merge(work_dir):
    print(f"[*] 工作目录: {work_dir}")
    
    scan_dir = os.path.join(work_dir, "scan原件")
    scan_new_dir = os.path.join(scan_dir, "新增")
    pdf_dir = os.path.join(work_dir, "合并好的pdf")
    md_dir = os.path.join(work_dir, "md件")
    
    os.makedirs(scan_dir, exist_ok=True)
    os.makedirs(pdf_dir, exist_ok=True)
    os.makedirs(md_dir, exist_ok=True)
    
    # 查找原始扫描文件
    search_dirs = [work_dir, scan_dir, scan_new_dir]
    
    for proj in PROJECT_CONFIGS:
        merged_doc = pymupdf.open()
        total_pages = 0
        print(f"\n[+] 处理项目: {proj['short_name']} - {proj['full_name']}")
        
        has_source = False
        for s in proj["sources"]:
            src_file = s["file"]
            found_path = None
            for sd in search_dirs:
                cand = os.path.join(sd, src_file)
                if os.path.exists(cand):
                    found_path = cand
                    break
            
            if not found_path:
                print(f"  [-] 未找到文件: {src_file}，跳过该段")
                continue
                
            has_source = True
            doc = pymupdf.open(found_path)
            start_p, end_p = s["page_range"]
            end_p = min(end_p, len(doc))
            
            for p_idx in range(start_p, end_p):
                page = doc[p_idx]
                target_rot = (page.rotation + s["rotation"]) % 360
                page.set_rotation(target_rot)
                merged_doc.insert_pdf(doc, from_page=p_idx, to_page=p_idx)
                total_pages += 1
            print(f"  + 合并 {src_file} [{s['desc']}]: {end_p - start_p} 页")
            doc.close()
            
        if has_source and total_pages > 0:
            out_pdf_name = f"研发人员及设备、无形资产的分配+{proj['short_name']}.pdf"
            out_pdf_path = os.path.join(pdf_dir, out_pdf_name)
            merged_doc.save(out_pdf_path, deflate=True)
            merged_doc.close()
            print(f"  >>> 成功导出: {out_pdf_name} ({total_pages} 页, {os.path.getsize(out_pdf_path)/1024/1024:.2f} MB)")
        else:
            merged_doc.close()
            
    print("\n[V] 合并处理完成！")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scan Project Merger")
    parser.add_argument("--work-dir", default=r"C:\JunzanLi_project\课题申报横向\王汉东\按项目合并", help="工作主目录")
    args = parser.parse_args()
    run_merge(args.work_dir)

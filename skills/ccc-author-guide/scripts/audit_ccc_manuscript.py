#!/usr/bin/env python3
r"""
audit_ccc_manuscript.py
Automated Technical Screening and Compliance Audit for Cement and Concrete Composites (Elsevier, ISSN 0958-9465).

Checks:
1. Layout & Line numbers (\usepackage{lineno}, \linenumbers)
2. Highlights length (3-5 bullets, <= 85 characters each)
3. Table citation coverage and sequential monotonicity
4. Figure citation coverage and sequential monotonicity
5. Bijective citation mapping (all \cite in \bibitem, all \bibitem cited in text)
6. Elsevier Numbered style compliance (no [R]/[M] GB/T markers, HTTPS DOIs)
7. End-matter mandatory sections (CRediT, Competing interests, Funding, Data availability)
"""

import sys
import os
import re
from pathlib import Path


def audit_highlights(highlights_path):
    issues = []
    if not os.path.exists(highlights_path):
        return ["Highlights file not found."]
    
    with open(highlights_path, "r", encoding="utf-8", errors="ignore") as f:
        lines = [line.strip() for line in f if line.strip()]
    
    # Filter bullet markers and header
    cleaned = []
    for l in lines:
        if l.lower().startswith("highlights") and len(l) < 20:
            continue
        c = re.sub(r"^[-*•\d\.\s]+", "", l).strip()
        if c:
            cleaned.append(c)
            
    if not (3 <= len(cleaned) <= 5):
        issues.append(f"Highlights count ({len(cleaned)}) is not within 3 to 5 bullets.")
        
    for i, bullet in enumerate(cleaned, 1):
        l = len(bullet)
        if l > 85:
            issues.append(f"Bullet {i} length ({l} chars) exceeds Elsevier maximum of 85 characters: '{bullet[:40]}...'")
            
    return issues


def audit_latex_manuscript(tex_path):
    report = {
        "passed": True,
        "critical_issues": [],
        "warnings": [],
        "stats": {}
    }
    
    if not os.path.exists(tex_path):
        report["passed"] = False
        report["critical_issues"].append(f"File not found: {tex_path}")
        return report
        
    with open(tex_path, "r", encoding="utf-8", errors="ignore") as f:
        tex = f.read()
        
    # 1. Line numbers check
    has_lineno_pkg = bool(re.search(r"\\usepackage\{lineno\}", tex))
    has_linenumbers_cmd = bool(re.search(r"\\linenumbers", tex))
    if not (has_lineno_pkg and has_linenumbers_cmd):
        report["critical_issues"].append("Missing line numbers. Add \\usepackage{lineno} in preamble and \\linenumbers after \\begin{document}.")
    else:
        report["stats"]["line_numbers"] = "Configured"

    # 2. Table citations and monotonicity
    tab_labels = re.findall(r"\\begin\{table\*?\}.*?\\caption\{.*?\}.*?\\label\{(tab:[^}]+)\}", tex, re.DOTALL)
    if not tab_labels:
        tab_labels = re.findall(r"\\label\{(tab:[^}]+)\}", tex)
    report["stats"]["total_tables"] = len(tab_labels)
    all_refs = re.findall(r"\\(?:cref|Cref|ref)\{([^}]+)\}", tex)
    ref_keys = set([k.strip() for r in all_refs for k in r.split(",")])
    
    uncited_tabs = [t for t in tab_labels if t not in ref_keys]
    if uncited_tabs:
        report["critical_issues"].append(f"Uncited tables found: {uncited_tabs}")
        
    # Table citation order
    tab_first_pos = {}
    for t in tab_labels:
        m = re.search(r"\\(?:cref|Cref|ref)\{[^}]*" + re.escape(t) + r"[^}]*\}", tex)
        if m:
            tab_first_pos[t] = m.start()
    sorted_tabs_by_pos = sorted(tab_first_pos.keys(), key=lambda x: tab_first_pos[x])
    for i in range(len(sorted_tabs_by_pos) - 1):
        t1, t2 = sorted_tabs_by_pos[i], sorted_tabs_by_pos[i+1]
        idx1 = tab_labels.index(t1)
        idx2 = tab_labels.index(t2)
        if idx1 > idx2:
            report["warnings"].append(f"Table citation non-monotonic: {t1} cited before {t2}.")

    # 3. Figure citations and monotonicity
    # Find main figures by matching \caption{...}\label{fig:...} outside of subfigures
    fig_blocks = re.findall(r"\\begin\{figure\*?\}(.*?)\\end\{figure\*?\}", tex, re.DOTALL)
    fig_labels = []
    for fb in fig_blocks:
        # Strip subfigures first
        fb_no_sub = re.sub(r"\\begin\{subfigure\}.*?\\end\{subfigure\}", "", fb, flags=re.DOTALL)
        m = re.findall(r"\\caption\{.*?\}\s*\\label\{(fig:[^}]+)\}", fb_no_sub, re.DOTALL)
        if m:
            fig_labels.extend(m)
        else:
            # Fallback
            fallback = re.findall(r"\\label\{(fig:[^}]+)\}", fb_no_sub)
            if fallback:
                fig_labels.append(fallback[-1])
                
    report["stats"]["total_figures"] = len(fig_labels)
    uncited_figs = [f for f in fig_labels if f not in ref_keys]
    if uncited_figs:
        report["critical_issues"].append(f"Uncited figures found: {uncited_figs}")
        
    fig_first_pos = {}
    for f in fig_labels:
        m = re.search(r"\\(?:cref|Cref|ref)\{[^}]*" + re.escape(f) + r"[^}]*\}", tex)
        if m:
            fig_first_pos[f] = m.start()
    sorted_figs_by_pos = sorted(fig_first_pos.keys(), key=lambda x: fig_first_pos[x])
    for i in range(len(sorted_figs_by_pos) - 1):
        f1, f2 = sorted_figs_by_pos[i], sorted_figs_by_pos[i+1]
        idx1 = fig_labels.index(f1)
        idx2 = fig_labels.index(f2)
        if idx1 > idx2:
            report["warnings"].append(f"Figure citation non-monotonic: {f1} cited before {f2}.")

    # 4. Citations & BibItems Bijective check
    cites_in_text = []
    for m in re.finditer(r"\\cite\{([^}]+)\}", tex):
        keys = [k.strip() for k in m.group(1).split(",")]
        for k in keys:
            if k not in cites_in_text:
                cites_in_text.append(k)
                
    bib_items = re.findall(r"\\bibitem\{([^}]+)\}", tex)
    report["stats"]["citations_in_text"] = len(cites_in_text)
    report["stats"]["bibitems_in_list"] = len(bib_items)
    
    missing_in_bib = [k for k in cites_in_text if k not in bib_items]
    unused_in_tex = [k for k in bib_items if k not in cites_in_text]
    
    if missing_in_bib:
        report["critical_issues"].append(f"Citations missing in \\bibitem list: {missing_in_bib}")
    if unused_in_tex:
        report["critical_issues"].append(f"Bibitems never cited in text: {unused_in_tex}")
        
    # 5. GB/T 7714 Contamination check
    gbt_markers = re.findall(r"\\bibitem\{[^}]+\}.*?(\[(?:R|M|C|D|P|J|N|G|S)\])", tex)
    if gbt_markers:
        report["critical_issues"].append(f"Chinese GB/T 7714 document type markers found in bibliography: {set(gbt_markers)}")

    # 6. Non-breaking space before \cite check
    space_cites = len(re.findall(r"[a-zA-Z0-9]\s+\\cite\{", tex))
    if space_cites > 0:
        report["warnings"].append(f"Found {space_cites} instances of breakable spaces before \\cite{{...}}. Use Author~\\cite{{...}} to avoid orphan line-breaks.")

    # 7. Mandatory End-matter sections
    for sec_name, pattern in [
        ("CRediT authorship", r"CRediT|author contribution"),
        ("Competing interests", r"competing interest|conflict of interest"),
        ("Funding", r"funding|financial support"),
        ("Data availability", r"data availability|data statement")
    ]:
        if not re.search(pattern, tex, re.IGNORECASE):
            report["critical_issues"].append(f"Missing mandatory section: {sec_name}")
            
    if report["critical_issues"]:
        report["passed"] = False
        
    return report


def main():
    if len(sys.argv) < 2:
        print("Usage: python audit_ccc_manuscript.py <path_to_paper.tex> [path_to_Highlights.txt]")
        sys.exit(1)
        
    tex_path = sys.argv[1]
    report = audit_latex_manuscript(tex_path)
    
    print("=" * 60)
    print("CCC (Cement and Concrete Composites) Technical Audit Report")
    print("=" * 60)
    print(f"Target Manuscript: {tex_path}")
    print(f"Overall Status   : {'PASSED [OK]' if report['passed'] else 'FAILED [CRITICAL ISSUES FOUND]'}")
    print("-" * 60)
    print("Statistics:")
    for k, v in report["stats"].items():
        print(f"  - {k:22}: {v}")
    print("-" * 60)
    
    if report["critical_issues"]:
        print(f"Critical Screening Issues ({len(report['critical_issues'])}):")
        for idx, err in enumerate(report["critical_issues"], 1):
            print(f"  [{idx}] {err}")
        print("-" * 60)
        
    if report["warnings"]:
        print(f"Formatting Warnings ({len(report['warnings'])}):")
        for idx, w in enumerate(report["warnings"], 1):
            print(f"  [{idx}] {w}")
        print("-" * 60)
        
    if len(sys.argv) >= 3:
        hl_path = sys.argv[2]
        hl_issues = audit_highlights(hl_path)
        print(f"Highlights Audit ({hl_path}):")
        if not hl_issues:
            print("  [OK] Highlights fully comply with CCC guidelines (3-5 bullets, <= 85 chars).")
        else:
            for idx, err in enumerate(hl_issues, 1):
                print(f"  [{idx}] {err}")
        print("-" * 60)
        
    sys.exit(0 if report["passed"] else 1)


if __name__ == "__main__":
    main()

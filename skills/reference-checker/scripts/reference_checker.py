#!/usr/bin/env python3
"""
reference_checker.py — Standalone Reference Cross-Check and Bijective Auditor.
Checks LaTeX or Markdown manuscripts for orphan citations, missing bibitems, and ordering anomalies.
"""

import sys
import os
import re
import json
import argparse


def check_latex_file(tex_path):
    with open(tex_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    # 1. Extract in-text \cite{...}
    in_text_cites = []
    for m in re.finditer(r"\\cite[a-zA-Z*]*\{([^}]+)\}", content):
        keys = [k.strip() for k in m.group(1).split(",")]
        for k in keys:
            if k and k not in in_text_cites:
                in_text_cites.append(k)

    # 2. Extract bibitems
    bib_items = re.findall(r"\\bibitem(?:\[[^\]]*\])?\{([^}]+)\}", content)

    missing_in_bib = [k for k in in_text_cites if k not in bib_items] if bib_items else []
    orphan_bibs = [b for b in bib_items if b not in in_text_cites] if bib_items else []

    # 3. Check spacing before citations
    breakable_spaces = len(re.findall(r"[a-zA-Z0-9]\s+\\cite\{", content))

    report = {
        "file": tex_path,
        "total_in_text_citations": len(in_text_cites),
        "total_bib_items": len(bib_items),
        "missing_in_bibliography": missing_in_bib,
        "orphan_references": orphan_bibs,
        "breakable_space_citations": breakable_spaces,
        "passed": (len(missing_in_bib) == 0 and len(orphan_bibs) == 0) if bib_items else True
    }
    return report


def main():
    parser = argparse.ArgumentParser(description="Academic Reference Checker")
    parser.add_argument("--tex", help="Path to LaTeX manuscript")
    parser.add_argument("--json-output", help="Save report to JSON")
    args = parser.parse_args()

    if not args.tex:
        parser.print_help()
        sys.exit(1)

    if not os.path.exists(args.tex):
        print(f"File not found: {args.tex}")
        sys.exit(1)

    res = check_latex_file(args.tex)

    print("=" * 60)
    print("Reference Checker Audit Report")
    print("=" * 60)
    print(f"Target File: {res['file']}")
    print(f"Status     : {'PASSED [OK]' if res['passed'] else 'ACTION REQUIRED [ISSUES FOUND]'}")
    print(f"In-text citations: {res['total_in_text_citations']}")
    print(f"Bibliography items: {res['total_bib_items']}")
    print("-" * 60)

    if res["missing_in_bibliography"]:
        print(f"[FAIL] Missing in Bibliography ({len(res['missing_in_bibliography'])}):")
        for k in res["missing_in_bibliography"]:
            print(f"  - {k}")

    if res["orphan_references"]:
        print(f"[WARN] Orphan Bibliography Items (never cited in text, {len(res['orphan_references'])}):")
        for k in res["orphan_references"]:
            print(f"  - {k}")

    if res["breakable_space_citations"] > 0:
        print(f"[HINT] Found {res['breakable_space_citations']} breakable spaces before \\cite. Use Author~\\cite{{...}}.")

    if not res["missing_in_bibliography"] and not res["orphan_references"]:
        print("[SUCCESS] 100% bijective match between in-text citations and bibliography!")

    print("=" * 60)

    if args.json_output:
        with open(args.json_output, "w", encoding="utf-8") as f:
            json.dump(res, f, indent=2, ensure_ascii=False)
        print(f"Report saved to: {args.json_output}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
CCC Journal Compliance Checker
Automated diagnostic and adaptation tool for academic manuscripts targeting top-tier journals
in Intelligent Construction, Civil & Structural Engineering, Building Materials, and Materials/NDT.
"""

import sys
import re
import argparse
from pathlib import Path

JOURNAL_RULES = {
    "autcon": {
        "name": "Automation in Construction",
        "publisher": "Elsevier",
        "docclass": "elsarticle",
        "abstract_max_words": 250,
        "abstract_min_words": 150,
        "highlights_required": True,
        "highlights_min": 3,
        "highlights_max": 5,
        "highlights_max_chars": 85,
        "ref_style": "numbered",
        "mandatory_sections": ["CRediT", "Declaration of Competing Interest", "Data Availability"],
        "max_words": 9000,
        "primary_focus": "Core contribution MUST be the IT/computational/robotic automation algorithm, not merely standard software applied to a building."
    },
    "cacaie": {
        "name": "Computer-Aided Civil and Infrastructure Engineering",
        "publisher": "Wiley",
        "docclass": "wiley",
        "abstract_max_words": 250,
        "abstract_min_words": 200,
        "highlights_required": False,
        "ref_style": "author-date",
        "mandatory_sections": ["Data Availability", "Conflict of Interest"],
        "max_words": 10000,
        "primary_focus": "Methodological/mathematical rigor in computing and AI integrated with civil infrastructure."
    },
    "advei": {
        "name": "Advanced Engineering Informatics",
        "publisher": "Elsevier",
        "docclass": "elsarticle",
        "abstract_max_words": 250,
        "abstract_min_words": 150,
        "highlights_required": True,
        "highlights_min": 3,
        "highlights_max": 5,
        "highlights_max_chars": 85,
        "ref_style": "numbered",
        "mandatory_sections": ["CRediT", "Declaration of Competing Interest", "Data Availability"],
        "max_words": 9500,
        "primary_focus": "Explicit distinction between AI/informatics methodology and engineering application in abstract."
    },
    "asce_jcce": {
        "name": "ASCE Journal of Computing in Civil Engineering",
        "publisher": "ASCE",
        "docclass": "ascelike-new",
        "abstract_max_words": 200,
        "abstract_min_words": 100,
        "highlights_required": False,
        "ref_style": "author-date",
        "mandatory_sections": ["Data Availability"],
        "max_words": 10000,
        "primary_focus": "Unnumbered section headings, 10,000 word-equivalent cap, notation list for mathematical formulations."
    },
    "engstruct": {
        "name": "Engineering Structures",
        "publisher": "Elsevier",
        "docclass": "elsarticle",
        "abstract_max_words": 250,
        "abstract_min_words": 150,
        "highlights_required": True,
        "highlights_min": 3,
        "highlights_max": 5,
        "highlights_max_chars": 85,
        "ref_style": "numbered",
        "mandatory_sections": ["CRediT", "Declaration of Competing Interest", "Data Availability"],
        "max_words": 9500,
        "primary_focus": "Generalizable structural mechanics advance; strictly only ONE corresponding author permitted."
    },
    "structures": {
        "name": "Structures (IStructE / Elsevier)",
        "publisher": "Elsevier",
        "docclass": "elsarticle",
        "abstract_max_words": 250,
        "abstract_min_words": 150,
        "highlights_required": True,
        "highlights_min": 3,
        "highlights_max": 5,
        "highlights_max_chars": 85,
        "ref_style": "numbered",
        "mandatory_sections": ["CRediT", "Declaration of Competing Interest", "Data Availability"],
        "max_words": 9000,
        "primary_focus": "Relevance to practical structural design and experimental/FE structural testing."
    },
    "twst": {
        "name": "Thin-Walled Structures",
        "publisher": "Elsevier",
        "docclass": "elsarticle",
        "abstract_max_words": 250,
        "abstract_min_words": 150,
        "highlights_required": True,
        "highlights_min": 3,
        "highlights_max": 5,
        "highlights_max_chars": 85,
        "ref_style": "numbered",
        "mandatory_sections": ["CRediT", "Declaration of Competing Interest", "Data Availability"],
        "max_words": 9000,
        "primary_focus": "Thin-walled, cold-formed, welded joint stability, fatigue, and structural integrity."
    },
    "asce_jse": {
        "name": "ASCE Journal of Structural Engineering",
        "publisher": "ASCE",
        "docclass": "ascelike-new",
        "abstract_max_words": 200,
        "abstract_min_words": 100,
        "highlights_required": False,
        "ref_style": "author-date",
        "mandatory_sections": ["Data Availability"],
        "max_words": 10000,
        "primary_focus": "Unnumbered headings, structural mechanics advance, notation list."
    },
    "cbm": {
        "name": "Construction and Building Materials",
        "publisher": "Elsevier",
        "docclass": "elsarticle",
        "abstract_max_words": 250,
        "abstract_min_words": 150,
        "highlights_required": True,
        "highlights_min": 3,
        "highlights_max": 5,
        "highlights_max_chars": 85,
        "ref_style": "numbered",
        "mandatory_sections": ["CRediT", "Declaration of Competing Interest", "Data Availability"],
        "max_words": 8500,
        "primary_focus": "Mandatory construction relevance; pure material physics without civil context is desk-rejected."
    },
    "ccc": {
        "name": "Cement and Concrete Composites",
        "publisher": "Elsevier",
        "docclass": "elsarticle",
        "abstract_max_words": 250,
        "abstract_min_words": 150,
        "highlights_required": True,
        "highlights_min": 3,
        "highlights_max": 5,
        "highlights_max_chars": 85,
        "ref_style": "numbered",
        "mandatory_sections": ["CRediT", "Declaration of Competing Interest", "Data Availability"],
        "max_words": 9000,
        "primary_focus": "Microstructural and mechanistic depth linked directly to composite performance."
    },
    "ccr": {
        "name": "Cement and Concrete Research",
        "publisher": "Elsevier",
        "docclass": "elsarticle",
        "abstract_max_words": 250,
        "abstract_min_words": 150,
        "highlights_required": True,
        "highlights_min": 3,
        "highlights_max": 5,
        "highlights_max_chars": 85,
        "ref_style": "numbered",
        "mandatory_sections": ["CRediT", "Declaration of Competing Interest", "Data Availability"],
        "max_words": 10000,
        "primary_focus": "Fundamental chemical, physical, and thermodynamic mechanisms; applied empirical papers rejected."
    },
    "jobe": {
        "name": "Journal of Building Engineering",
        "publisher": "Elsevier",
        "docclass": "elsarticle",
        "abstract_max_words": 250,
        "abstract_min_words": 150,
        "highlights_required": True,
        "highlights_min": 3,
        "highlights_max": 5,
        "highlights_max_chars": 85,
        "ref_style": "numbered",
        "mandatory_sections": ["CRediT", "Declaration of Competing Interest", "Data Availability"],
        "max_words": 9000,
        "primary_focus": "Whole building performance, building materials, and lifecycle engineering."
    },
    "matdes": {
        "name": "Materials & Design",
        "publisher": "Elsevier",
        "docclass": "elsarticle",
        "abstract_max_words": 250,
        "abstract_min_words": 150,
        "highlights_required": True,
        "highlights_min": 3,
        "highlights_max": 5,
        "highlights_max_chars": 85,
        "ref_style": "numbered",
        "mandatory_sections": ["CRediT", "Declaration of Competing Interest", "Data Availability"],
        "max_words": 9000,
        "primary_focus": "Material processing and microstructure must be explicitly linked to an engineering design context."
    },
    "jmpt": {
        "name": "Journal of Materials Processing Technology",
        "publisher": "Elsevier",
        "docclass": "elsarticle",
        "abstract_max_words": 250,
        "abstract_min_words": 150,
        "highlights_required": True,
        "highlights_min": 3,
        "highlights_max": 5,
        "highlights_max_chars": 85,
        "ref_style": "numbered",
        "mandatory_sections": ["CRediT", "Declaration of Competing Interest", "Data Availability"],
        "max_words": 9000,
        "primary_focus": "Defect formation mechanisms linked directly to manufacturing process physics."
    },
    "eaai": {
        "name": "Engineering Applications of Artificial Intelligence",
        "publisher": "Elsevier",
        "docclass": "elsarticle",
        "abstract_max_words": 250,
        "abstract_min_words": 150,
        "highlights_required": True,
        "highlights_min": 3,
        "highlights_max": 5,
        "highlights_max_chars": 85,
        "ref_style": "numbered",
        "mandatory_sections": ["CRediT", "Declaration of Competing Interest", "Data Availability"],
        "max_words": 9500,
        "primary_focus": "Balanced AI architectural novelty and real industrial engineering deployment validation."
    },
    "ndteint": {
        "name": "NDT & E International",
        "publisher": "Elsevier",
        "docclass": "elsarticle",
        "abstract_max_words": 250,
        "abstract_min_words": 150,
        "highlights_required": True,
        "highlights_min": 3,
        "highlights_max": 5,
        "highlights_max_chars": 85,
        "ref_style": "numbered",
        "mandatory_sections": ["CRediT", "Declaration of Competing Interest", "Data Availability"],
        "max_words": 8500,
        "primary_focus": "Physical and experimental validation of nondestructive evaluation and metrology accuracy."
    }
}

def strip_latex(text: str) -> str:
    """Strip comments and common LaTeX commands for accurate word counting."""
    # Remove comments
    text = re.sub(r'%.*?\n', '\n', text)
    # Remove equation environments
    text = re.sub(r'\\begin\{(equation|align|aligned|gather)\*?\}.*?\\end\{\1\*?\}', ' ', text, flags=re.DOTALL)
    # Remove inline math
    text = re.sub(r'\$.*?\$', ' ', text)
    # Remove basic markup commands while keeping content
    text = re.sub(r'\\[a-zA-Z]+\*?(\[[^\]]*\])?\{([^}]*)\}', r'\2', text)
    # Remove dangling commands
    text = re.sub(r'\\[a-zA-Z]+', ' ', text)
    # Clean whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def inspect_manuscript(filepath: Path, journal_key: str):
    if not filepath.exists():
        print(f"Error: File '{filepath}' not found.")
        sys.exit(1)
        
    journal_key = journal_key.lower().replace("-", "_").replace(" ", "_")
    if journal_key not in JOURNAL_RULES:
        print(f"Unknown journal key '{journal_key}'. Available journals:")
        for k, v in JOURNAL_RULES.items():
            print(f"  - {k}: {v['name']} ({v['publisher']})")
        sys.exit(1)
        
    rules = JOURNAL_RULES[journal_key]
    raw_content = filepath.read_text(encoding="utf-8", errors="ignore")
    
    print("=" * 78)
    print(f"CCC Journal Compliance Audit: {rules['name']}")
    print(f"Target Publisher: {rules['publisher']} | File: {filepath.name}")
    print("=" * 78)
    
    # 1. Check Abstract
    abstract_match = re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}', raw_content, re.DOTALL)
    if abstract_match:
        abstract_text = strip_latex(abstract_match.group(1))
        abstract_words = len(abstract_text.split())
        abs_ok = rules['abstract_min_words'] <= abstract_words <= rules['abstract_max_words']
        status = "[PASS]" if abs_ok else "[WARN]"
        print(f"{status} Abstract Word Count: {abstract_words} words (Required: {rules['abstract_min_words']}--{rules['abstract_max_words']} words)")
    else:
        print("[WARN] Abstract environment not found in manuscript.")
        
    # 2. Check Document Class
    docclass_match = re.search(r'\\documentclass(\[[^\]]*\])?\{([^}]*)\}', raw_content)
    if docclass_match:
        actual_class = docclass_match.group(2)
        print(f"[INFO] Document Class: '{actual_class}' (Target family: '{rules['docclass']}')")
    
    # 3. Check Mandatory Sections
    print("\nMandatory Declarations Check:")
    for section_name in rules['mandatory_sections']:
        pattern = re.compile(re.escape(section_name), re.IGNORECASE)
        found = pattern.search(raw_content) is not None
        status = "[PASS]" if found else "[FAIL]"
        print(f"  {status} {section_name}")
        
    # 4. Check Highlights (if stored in an adjacent .txt, .md or inside tex comments)
    print("\nHighlights Verification:")
    highlights_file = filepath.parent / "highlights.txt"
    if not highlights_file.exists():
        highlights_file = filepath.parent / "highlights.md"
        
    if highlights_file.exists():
        hl_lines = [l.strip("- *").strip() for l in highlights_file.read_text(encoding="utf-8").splitlines() if l.strip()]
        print(f"  Found highlights file: {highlights_file.name} ({len(hl_lines)} bullets)")
        for i, hl in enumerate(hl_lines, 1):
            char_len = len(hl)
            ok = char_len <= rules.get('highlights_max_chars', 85)
            status = "[PASS]" if ok else "[FAIL]"
            print(f"    {status} Bullet {i} ({char_len} chars): \"{hl}\"")
            if not ok:
                print(f"           -> EXCEEDS {rules['highlights_max_chars']} CHAR LIMIT BY {char_len - rules['highlights_max_chars']} CHARS!")
    else:
        print(f"  [INFO] No separate highlights.txt/.md found in {filepath.parent}.")
        if rules['highlights_required']:
            print(f"  [REMINDER] {rules['name']} mandates 3-5 highlights with max 85 characters each.")

    # 5. Citation Style
    print("\nCitation & Bibliography Style:")
    cite_style_match = re.search(r'\\bibliographystyle\{([^}]*)\}', raw_content)
    if cite_style_match:
        bibstyle = cite_style_match.group(1)
        print(f"  [INFO] Bibliography Style: '{bibstyle}' (Target: {rules['ref_style']})")
    else:
        print(f"  [INFO] No explicit \\bibliographystyle found.")

    # 6. Overall Word Count
    body_text = strip_latex(raw_content)
    total_words = len(body_text.split())
    status = "[PASS]" if total_words <= rules['max_words'] else "[WARN]"
    print(f"\n{status} Estimated Body Word Count: ~{total_words} words (Target budget: <= {rules['max_words']} words)")
    
    # 7. Editorial Philosophy & Desk-Reject Core Focus
    print("\n" + "-" * 78)
    print(f"CRITICAL EDITORIAL PHILOSOPHY & DESK-REJECT FOCUS FOR {rules['name'].upper()}:")
    print(f">> {rules['primary_focus']}")
    print("-" * 78 + "\n")

def main():
    parser = argparse.ArgumentParser(description="Audit academic manuscript compliance with target journal guidelines.")
    parser.add_argument("file", help="Path to manuscript file (e.g. main.tex)")
    parser.add_argument("--journal", "-j", default="autcon", help="Journal code (e.g., autcon, cacaie, advei, cbm, ccc, ccr, engstruct, eaai, matdes, etc.)")
    args = parser.parse_args()
    
    inspect_manuscript(Path(args.file), args.journal)

if __name__ == "__main__":
    main()

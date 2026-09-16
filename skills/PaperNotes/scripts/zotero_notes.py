#!/usr/bin/env python3
"""
zotero_notes.py — Converts BibTeX and Zotero entries into structured atomic research notes.
Pure Python standard library.
"""

import sys
import os
import re
import json
import argparse
from datetime import datetime


def create_note_template(key, title, authors, year, doi="", abstract=""):
    note = f"""---
citekey: "{key}"
title: "{title}"
authors: "{authors}"
year: {year or "Unknown"}
doi: "{doi}"
date_imported: "{datetime.now().strftime('%Y-%m-%d')}"
tags:
  - literature-note
  - research
---

# {title}

- **Authors**: {authors}
- **Year**: {year}
- **DOI / URL**: {f'[{doi}](https://doi.org/{doi})' if doi else 'N/A'}

## 🎯 One-Sentence Takeaway
> [Write the primary contribution or insight of this paper here]

## 🔬 Core Methodology & Approach
- **Key Formulation**: 
- **Datasets / Materials**: 
- **Experimental Protocol**: 

## 📊 Key Results & Evidence
- [Anchor to critical figure or table data]

## ⚠️ Limitations & Open Questions
- 

## 💡 Connections to My Research
- 
"""
    return note


def main():
    parser = argparse.ArgumentParser(description="PaperNotes note generator")
    parser.add_argument("--citekey", help="Citation key")
    parser.add_argument("--title", default="Untitled Paper", help="Paper title")
    parser.add_argument("--authors", default="Author et al.", help="Authors string")
    parser.add_argument("--year", default="2024", help="Publication year")
    parser.add_argument("--doi", default="", help="DOI string")
    parser.add_argument("--output", default=".", help="Output directory for notes")
    args = parser.parse_args()

    key = args.citekey or re.sub(r"[^a-zA-Z0-9]", "", args.title)[:15].lower()
    content = create_note_template(key, args.title, args.authors, args.year, args.doi)

    os.makedirs(args.output, exist_ok=True)
    out_file = os.path.join(args.output, f"{key}.md")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Created PaperNote card at: {out_file}")


if __name__ == "__main__":
    main()

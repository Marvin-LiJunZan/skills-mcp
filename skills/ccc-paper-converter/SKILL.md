---
name: ccc-paper-converter
description: Specialized academic PDF to Markdown converter and experimental data extractor for the CCC skills ecosystem. Integrates with ccc-literature-scout BibTeX/CSV libraries, leverages RTX 5070 Ti GPU acceleration with MinerU/Docling/Native multi-engines, restores LaTeX formulas and tables, and aggregates experimental data into comparison matrices for paper writing.
---

# CCC Paper Converter & Experimental Data Extractor

A specialized academic converter designed for the **CCC Skills Ecosystem**.
Converts scientific literature PDFs to publication-grade Markdown (with LaTeX formulas and tables), binds metadata with `ccc-literature-scout` reference libraries, and automatically extracts experimental data tables into unified comparison matrices for paper writing.

---

## 🌟 Ecosystem Integration Architecture

```
┌─────────────────────────────────────────────────────────────┐
│ 1. ccc-literature-scout (Literature Retrieval & BibTeX)     │
│    Outputs: master_unified_references.bib, matrix.csv       │
└──────────────────────────────┬──────────────────────────────┘
                               │ (PDFs + BibTeX / CSV Metadata)
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. ccc-paper-converter (Batch Conversion & Data Mining)     │
│                                                             │
│ ├── Engine A: MinerU (Magic-PDF) [LaTeX Formulas & 2-Column]│
│ ├── Engine B: IBM Docling [Multi-page Tables & RAG]         │
│ └── Engine C: Native Engine (PyMuPDF + pdfplumber Fallback) │
│                                                             │
│ Output Artifacts:                                           │
│ ├── <BibKey>.md (Clean Markdown with injected YAML header)  │
│ ├── master_extracted_tables.md (All tables aggregated)      │
│ └── master_extracted_data.csv (Excel-ready data matrix)     │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. Writing Phase (Results & Discussion / Comparison Tables) │
└─────────────────────────────────────────────────────────────┘
```

---

## 🛠️ CLI Quick Start & Commands

The tool is located at:
`skills/ccc-paper-converter/ccc_converter_tool.py`

### 1. System & GPU Diagnostics

Check your GPU status (e.g. RTX 5070 Ti), PyTorch CUDA, and available engines:

```bash
python skills/ccc-paper-converter/ccc_converter_tool.py check-env
```

### 2. Full End-to-End Pipeline (Convert + Bind Metadata + Extract Data)

Batch converts downloaded PDFs, links them to `ccc-literature-scout` BibTeX metadata, and extracts all experimental tables into a summary report:

```bash
python skills/ccc-paper-converter/ccc_converter_tool.py pipeline \
  -i ./downloaded_pdfs \
  -o ./converted_corpus \
  --bib ./literature_project/master_unified_references.bib \
  --engine auto \
  --extract-tables
```

### 3. Step-by-Step Commands

#### A. Batch Convert PDFs to Markdown
```bash
# Auto mode (prefers MinerU/Docling if installed, falls back to Native PyMuPDF)
python skills/ccc-paper-converter/ccc_converter_tool.py convert \
  -i ./downloaded_pdfs \
  -o ./converted_mds \
  --engine auto

# Specific engine selection:
# --engine mineru   (Requires: pip install magic-pdf[full])
# --engine docling  (Requires: pip install docling)
# --engine native   (Zero extra installation, uses PyMuPDF)
```

#### B. Bind Metadata from `ccc-literature-scout`
Automatically renames markdown files to their `BibKey` and injects YAML frontmatter (Title, Authors, Year, DOI, Abstract):
```bash
python skills/ccc-paper-converter/ccc_converter_tool.py bind-metadata \
  --md-dir ./converted_mds \
  --bib ./literature_project/master_unified_references.bib
```

#### C. Extract Experimental Tables & Parameters
Scans all converted papers, extracts every table, and generates a unified summary:
```bash
python skills/ccc-paper-converter/ccc_converter_tool.py extract-tables \
  --md-dir ./converted_mds \
  --output-file ./converted_mds/master_extracted_tables.md \
  --output-csv ./converted_mds/master_extracted_data.csv
```

---

## 📂 Output Artifacts Structure

```
converted_corpus/
├── Zhang2024Hierarchical.md          (Standardized with YAML frontmatter)
├── Wang2023Porous.md
├── Liu2025Multiscale.md
├── master_extracted_tables.md        (Unified catalog of all experimental tables)
└── master_extracted_data.csv         (Excel-ready flattened data matrix)
```

---
name: ccc-literature-scout
description: Automated massive-scale academic literature search (up to 1000 papers per keyword), per-keyword BibTeX generation with full abstracts, Web of Science & OpenAlex multi-source integration, cross-corpus deduplication & matrix synthesis, and 5-stage publication-grade LaTeX/Markdown Introduction drafting.
---

# CCC Literature Scout & Introduction Synthesizer (V2.0 - Massive Scale)

A specialized academic skill for **large-scale literature retrieval (up to 1000 papers per keyword)**, **per-keyword `.bib` generation with full abstracts**, **multi-bib deduplication and synthesis**, and **publication-grade 5-stage Introduction drafting** (Nature / Elsevier / IEEE style).

---

## 🌟 Two-Stage Systematic Architecture

```
[User Keywords: KW1, KW2, KW3...]
               │
               ▼
┌────────────────────────────────────────────────────────────────────────┐
│ STAGE 1: Massive-Scale Multi-Source Literature Retrieval               │
│ - OpenAlex (250M+ Works, Inverted-Index Abstract Reconstruction)       │
│ - Web of Science Clarivate API (Starter / Expanded API)                │
│ - Campus WoS Batch Exports (.ciw, .txt, .bib, .ris folder)             │
│ - arXiv & Crossref API Enrichment                                      │
│                                                                        │
│ OUTPUT per Keyword:                                                    │
│ ├── bib_by_keyword/01_<keyword1>.bib (up to 1000 entries with abstracts)│
│ ├── bib_by_keyword/01_<keyword1>_matrix.csv                            │
│ ├── bib_by_keyword/02_<keyword2>.bib (up to 1000 entries with abstracts)│
│ └── bib_by_keyword/02_<keyword2>_matrix.csv                            │
└────────────────────────────────────────────────────────────────────────┘
               │
               ▼
┌────────────────────────────────────────────────────────────────────────┐
│ STAGE 2: Deep Cross-Corpus Synthesis & Introduction Generation         │
│ - Ingest all keyword bib files into a unified corpus                   │
│ - Multi-level deduplication (DOI, Title cosine, arXiv mapping)         │
│ - Timeline evolution & Landmark citation ranking                       │
│ - Thematic clustering into methodological streams                      │
│                                                                        │
│ OUTPUT Master Artifacts:                                               │
│ ├── master_unified_references.bib (Clean, deduplicated master library) │
│ ├── master_literature_matrix.csv (Excel-ready analysis spreadsheet)   │
│ ├── master_literature_synthesis.md (Trend report & landmark ranking)   │
│ ├── introduction_draft.tex (Publication-grade LaTeX with \cite{...})   │
│ └── introduction_draft.md (Markdown draft for fast reading)            │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ CLI Quick Start & Commands

The tool is located at:
`c:/JunzanLi_project/skills_mcp/skills/ccc-literature-scout/ccc_literature_tool.py`

### 1. Full End-to-End Pipeline (Stage 1 + Stage 2)

Downloads up to 1000 papers with abstracts for each keyword, exports separate keyword bib files, and generates the unified introduction:

```bash
# English journal mode (Elsevier / Nature / IEEE)
python c:/JunzanLi_project/skills_mcp/skills/ccc-literature-scout/ccc_literature_tool.py pipeline \
  --keywords "implicit neural representations microstructure" "porous media transport permeability" "multigrid defect correction" \
  --topic "Implicit Neural Microstructure Representation for Multiscale Transport" \
  --method-name "the proposed hierarchical implicit framework" \
  --limit 1000 \
  --output-dir ./literature_project \
  --lang en
```

```bash
# Chinese manuscript mode (中文期刊 / 博士论文引言)
python c:/JunzanLi_project/skills_mcp/skills/ccc-literature-scout/ccc_literature_tool.py pipeline \
  --keywords "水泥基材料 微观结构 传输性能" "隐式神经表征 偏微分方程求解" \
  --topic "基于分层隐式神经表征的水泥基材料多尺度传输建模" \
  --method-name "分层隐式连续表征与缺陷修正物理求解器" \
  --limit 1000 \
  --output-dir ./literature_project_zh \
  --lang zh
```

### 2. Stage 1 ONLY: Batch Retrieval (1 Bib per Keyword)

```bash
python c:/JunzanLi_project/skills_mcp/skills/ccc-literature-scout/ccc_literature_tool.py stage1-fetch \
  --keywords "deep learning fluid dynamics" "physics informed neural networks" \
  --limit 1000 \
  --output-dir ./stage1_data
```

### 3. Stage 2 ONLY: Synthesize Existing `.bib` Directory into Introduction

```bash
python c:/JunzanLi_project/skills_mcp/skills/ccc-literature-scout/ccc_literature_tool.py stage2-synthesize \
  --bib-dir ./stage1_data/bib_by_keyword \
  --topic "Physics-informed neural networks for fluid dynamics" \
  --method-name "our conservative PINN architecture" \
  --output-dir ./stage2_output \
  --lang en
```

### 4. Direct Web of Science Clarivate API or Campus Export Ingestion

* **If you have a Web of Science API Key**:
  ```bash
  python ccc_literature_tool.py pipeline --keywords "..." --topic "..." --wos-api-key "YOUR_KEY"
  ```
* **If you have a folder of exported `.ciw`, `.txt`, `.bib` files from campus WoS**:
  ```bash
  python ccc_literature_tool.py pipeline --keywords "..." --topic "..." --wos-dir ./campus_wos_downloads
  ```

---

## 📂 Output Artifacts Directory Structure

```
literature_project/
├── bib_by_keyword/
│   ├── 01_implicit_neural_representations_microstructure.bib      (1000 entries with abstracts)
│   ├── 01_implicit_neural_representations_microstructure_matrix.csv
│   ├── 02_porous_media_transport_permeability.bib                 (1000 entries with abstracts)
│   ├── 02_porous_media_transport_permeability_matrix.csv
│   ├── 03_multigrid_defect_correction.bib                         (1000 entries with abstracts)
│   └── 03_multigrid_defect_correction_matrix.csv
├── master_unified_references.bib                                  (Deduplicated master bib)
├── master_literature_matrix.csv                                   (Excel-ready master matrix)
├── master_literature_corpus.json                                  (Structured JSON corpus)
├── master_literature_synthesis.md                                 (Timeline & landmark report)
├── introduction_draft.tex                                         (5-stage publication LaTeX)
└── introduction_draft.md                                          (Markdown preview)
```

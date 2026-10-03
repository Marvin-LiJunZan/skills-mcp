---
name: ccc-literature-scout
description: Automated massive-scale academic literature search across 25+ databases (Web of Science, OpenAlex, Semantic Scholar, Crossref, arXiv, PubMed, PMC, Europe PMC, bioRxiv, ChemRxiv, DBLP, CORE, DOAJ, OpenAIRE, Chinese CJK academic sources), per-keyword BibTeX generation with full abstracts, cross-corpus deduplication & matrix synthesis, open-access PDF downloading for ccc-paper-converter, and 5-stage publication-grade LaTeX/Markdown Introduction drafting.
---

# CCC Literature Scout & Introduction Synthesizer (V3.0 - Multi-Source Omnichannel)

A specialized academic skill for **large-scale multi-database literature retrieval (up to 1000 papers per keyword)**, **per-keyword `.bib` generation with full abstracts**, **multi-bib deduplication and synthesis**, **open-access PDF batch downloading**, and **publication-grade 5-stage Introduction drafting** (Nature / Elsevier / IEEE / CCC style).

---

## 🌟 Multi-Source Omnichannel Architecture

```
[User Keywords: KW1, KW2, KW3... (English or Chinese)]
               │
               ▼
┌────────────────────────────────────────────────────────────────────────┐
│ STAGE 1: Massive Multi-Source Academic Retrieval (25+ Databases)       │
│ - Commercial & Citation: Web of Science (Clarivate API / Campus files) │
│ - AI & High-Impact Graph: Semantic Scholar (TLDR + Citation Graph)     │
│ - Open Knowledge Graph: OpenAlex (250M+ catalog, reconstructed abs)    │
│ - Official DOIs & Metadata: Crossref                                   │
│ - Preprints: arXiv, bioRxiv, medRxiv, ChemRxiv, IACR                   │
│ - Biomedical & Life Sciences: PubMed, PMC, Europe PMC                  │
│ - Open Repositories & OA: CORE, DOAJ, OpenAIRE, BASE, Zenodo, HAL, SSRN│
│ - Chinese Academic Routing: OpenAlex (CJK), Crossref (CN), NSSD, yiigle│
│ - Optional Key-Activated: IEEE Xplore, ACM Digital Library             │
│ - Optional OA PDF Pipeline: Auto-download PDFs for ccc-paper-converter │
│                                                                        │
│ OUTPUT per Keyword:                                                    │
│ ├── bib_by_keyword/01_<keyword1>.bib (up to 1000 entries with abstracts)│
│ ├── bib_by_keyword/01_<keyword1>_matrix.csv (with Citations, DOI, PDF) │
│ └── pdfs/01_<keyword1>/<BibKey>.pdf (Downloaded OA PDFs)               │
└────────────────────────────────────────────────────────────────────────┘
               │
               ▼
┌────────────────────────────────────────────────────────────────────────┐
│ STAGE 2: Deep Cross-Corpus Synthesis & Introduction Generation         │
│ - Ingest all keyword bib files into a unified corpus                   │
│ - Multi-level deduplication (DOI, Title normalization, arXiv mapping)  │
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

```bash
# English journal mode with multi-source retrieval
python c:/JunzanLi_project/skills_mcp/skills/ccc-literature-scout/ccc_literature_tool.py pipeline \
  --keywords "implicit neural representations microstructure" "porous media transport permeability" \
  --topic "Implicit Neural Microstructure Representation for Multiscale Transport" \
  --method-name "the proposed hierarchical implicit framework" \
  --sources all \
  --limit 500 \
  --output-dir ./literature_project \
  --lang en
```

```bash
# Chinese manuscript mode (自动路由中文数据库与 CJK 索引)
python c:/JunzanLi_project/skills_mcp/skills/ccc-literature-scout/ccc_literature_tool.py pipeline \
  --keywords "水泥基材料 微观结构 传输性能" "隐式神经表征 偏微分方程求解" \
  --topic "基于分层隐式神经表征的水泥基材料多尺度传输建模" \
  --method-name "分层隐式连续表征与缺陷修正物理求解器" \
  --sources chinese \
  --limit 500 \
  --output-dir ./literature_project_zh \
  --lang zh
```

### 2. Stage 1 ONLY: Multi-Source Batch Retrieval

```bash
# Retrieve across CS preset (Semantic Scholar, DBLP, arXiv, OpenAlex, WoS)
python c:/JunzanLi_project/skills_mcp/skills/ccc-literature-scout/ccc_literature_tool.py stage1-fetch \
  --keywords "deep learning fluid dynamics" "physics informed neural networks" \
  --sources cs \
  --limit 200 \
  --output-dir ./stage1_data
```

```bash
# Automatically download open-access PDFs for ccc-paper-converter
python c:/JunzanLi_project/skills_mcp/skills/ccc-literature-scout/ccc_literature_tool.py stage1-fetch \
  --keywords "geopolymer concrete rheology" \
  --sources materials \
  --download-oa-pdfs \
  --max-pdfs 30 \
  --output-dir ./stage1_materials
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

### 4. Source Presets & Custom Selection

- `--sources all`: All 25+ integrated databases.
- `--sources default`: Balanced tier (WoS, OpenAlex, Semantic Scholar, arXiv, Crossref, PubMed, DBLP).
- `--sources cs`: Semantic Scholar, DBLP, arXiv, OpenAlex, Crossref, WoS, IEEE, ACM.
- `--sources biomedical`: PubMed, PMC, Europe PMC, bioRxiv, medRxiv, OpenAlex, Crossref, WoS.
- `--sources materials`: WoS, OpenAlex, ChemRxiv, Crossref, arXiv, CORE, DOAJ.
- `--sources chinese`: OpenAlex (CJK), Crossref (CJK), NSSD, WoS.
- Or comma-separated: `--sources wos,semantic,arxiv,pubmed`.

### 5. API Key Configuration

All API keys can be passed as CLI flags or environment variables:
- **Web of Science**: `--wos-api-key "KEY"` or `$env:WOS_API_KEY = "KEY"`
- **Semantic Scholar**: `--semantic-key "KEY"` or `$env:SEMANTIC_SCHOLAR_API_KEY = "KEY"`
- **IEEE Xplore**: `$env:IEEE_API_KEY = "KEY"`
- **ACM DL**: `$env:ACM_API_KEY = "KEY"`
- **Campus WoS export folder**: `--wos-dir ./campus_wos_downloads` (.ciw, .txt, .bib, .ris)

---

## 📂 Output Artifacts Directory Structure

```
literature_project/
├── bib_by_keyword/
│   ├── 01_<keyword1>.bib                                          (1000 entries with abstracts)
│   ├── 01_<keyword1>_matrix.csv                                   (with Citations, DOI, PdfURL)
│   ├── 02_<keyword2>.bib                                          (1000 entries with abstracts)
│   └── 02_<keyword2>_matrix.csv
├── pdfs/                                                          (When --download-oa-pdfs is enabled)
│   ├── 01_<keyword1>/
│   │   ├── Author2025Title.pdf                                    (Ready for ccc-paper-converter)
│   │   └── ...
├── master_unified_references.bib                                  (Deduplicated master bib)
├── master_literature_matrix.csv                                   (Excel-ready master matrix)
├── master_literature_corpus.json                                  (Structured JSON corpus)
├── master_literature_synthesis.md                                 (Timeline & landmark report)
├── introduction_draft.tex                                         (5-stage publication LaTeX)
└── introduction_draft.md                                          (Markdown preview)
```

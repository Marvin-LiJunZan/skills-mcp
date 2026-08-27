---
name: ccc-literature-scout
description: Automated academic literature search, Web of Science & multi-source metadata retrieval, clean BibTeX generator with full abstracts, deduplication, literature matrix synthesis, and 5-stage publication-grade LaTeX/Markdown Introduction drafting. Use when the user wants to batch search papers by keywords, export/parse Web of Science bib entries, analyze literature trends/gaps, or draft an academic paper Introduction with real citation anchors.
---

# CCC Literature Scout & Introduction Synthesizer

A specialized academic skill for **batch literature retrieval**, **abstract-enriched BibTeX generation**, **corpus matrix analysis**, and **publication-grade Introduction drafting** (Nature / Elsevier / IEEE style).

---

## 🌟 Core Highlights & Capabilities

1. **Zero-Friction Multi-Source Retrieval**:
   - Automatically queries **OpenAlex** (250M+ open catalog, reconstructs full abstracts from inverted index), **arXiv** (native preprints & IDs), and **Crossref** (official DOIs & publisher metadata).
   - Requires **no login / no VPN / no browser automation**; runs stably in seconds.

2. **Web of Science (WoS) / EndNote / RIS Parser**:
   - Supports ingesting `.ciw`, `.txt`, `.bib`, and `.ris` files exported from your campus network WoS.
   - Automatically cleans missing fields, extracts abstracts, standardizes keys, and deduplicates.

3. **Publication-Grade BibTeX with Full Abstracts**:
   - Generates standardized keys: `FirstAuthorYearKeyword` (e.g. `Muller2022Instant`, `Sitzmann2020Implicit`).
   - Escapes special LaTeX characters (`&` $\to$ `\&`, `%` $\to$ `\%`, etc.).
   - Standardizes `abstract = {...}` for all entries so you never need to copy-paste abstracts manually.

4. **Corpus Matrix & Synthesis Report**:
   - Outputs `literature_matrix.csv` (for Excel / Pandas viewing with title, authors, year, journal, citations, abstract).
   - Outputs `literature_synthesis.md` (timeline distribution, landmark works ranking, emerging frontier papers).

5. **5-Stage Publication-Grade Introduction Drafting (English & 中文)**:
   - Follows top-tier journal logic chain:
     1. **Broad Background & Practical Relevance** (宏观背景与工程意义)
     2. **Categorized SOTA & Methodological Paradigms** (主流方法分类综述与文献簇引用)
     3. **Critical Bottlenecks & Fundamental Research Gap** (关键瓶颈与尚未解决的科学问题)
     4. **Proposed Framework & Theoretical Insights** (本文提出的核心方法与机制)
     5. **Key Technical Contributions & Article Roadmap** (3-4 点具体学术贡献与论文结构)
   - Directly embeds valid `\cite{...}` keys from the generated `.bib`.

---

## 🛠️ CLI Quick Start & Commands

The CLI tool is located at:
`c:/JunzanLi_project/skills_mcp/skills/ccc-literature-scout/ccc_literature_tool.py`

### 1. One-Click End-to-End Pipeline (Search $\to$ BibTeX $\to$ Analysis $\to$ Introduction)

```bash
python ccc_literature_tool.py pipeline \
  --keywords "implicit neural representations microstructure" "multiscale transport porous media" "cementitious pore network" \
  --topic "Implicit Neural Microstructure Representation for Multiscale Transport" \
  --method-name "the proposed hierarchical implicit framework" \
  --limit 15 \
  --output-dir ./literature_output \
  --lang en
```

*For Chinese manuscript output:*
```bash
python ccc_literature_tool.py pipeline \
  --keywords "微观孔隙结构 传输性能" "隐式神经表征 偏微分方程" \
  --topic "基于分层隐式神经表征的水泥基材料多尺度传输建模" \
  --method-name "分层隐式连续表征与缺陷修正物理求解器" \
  --output-dir ./literature_output_zh \
  --lang zh
```

### 2. Ingest Campus Web of Science Export (.ciw / .txt / .bib)

If you have downloaded an export file from Web of Science (e.g. `savedrecs.ciw` or `savedrecs.txt`):

```bash
python ccc_literature_tool.py parse-wos \
  --input ./savedrecs.ciw \
  --output-dir ./wos_output
```

### 3. Generate Introduction from an Existing `.bib` File

```bash
python ccc_literature_tool.py write-intro \
  --bib ./my_references.bib \
  --topic "Neural implicit representations for microstructural fluid dynamics" \
  --output-dir ./intro_output \
  --lang en
```

---

## 📂 Output Artifacts Structure

When executed, the tool generates the following artifacts in your target folder:

| File Name | Purpose & Content |
| :--- | :--- |
| **`references.bib`** | Clean, deduplicated BibTeX file with full `abstract = {...}`, DOIs, and formatted keys. |
| **`literature_matrix.csv`** | Excel-ready spreadsheet of all papers, citations, journals, DOIs, and abstracts. |
| **`literature_corpus.json`** | Structured JSON database for programmatic access. |
| **`literature_synthesis.md`** | Chronological timeline, citation ranking, landmark papers, and thematic clusters. |
| **`introduction_draft.tex`** | Top-tier 5-stage LaTeX Introduction ready to insert into your `.tex` manuscript. |
| **`introduction_draft.md`** | Markdown draft for fast reading, reviewing, and editing. |

---

## 🎯 Best Practices for Prompting the Agent

When you want the agent to conduct literature reviews or write introductions:
1. Provide 3–5 specific keyword phrases (e.g., `"implicit neural representations"`, `"porous media permeability"`, `"multigrid defect correction"`).
2. State the key innovation of your paper (e.g., `"2-level PCG solver with sub-voxel feature correction"`).
3. The agent will run `ccc_literature_tool.py`, retrieve all matching literature with abstracts into a `.bib`, and generate a publication-grade Introduction where every statement is backed by real `\cite{...}` citation anchors.

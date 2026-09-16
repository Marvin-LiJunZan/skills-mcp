---
name: arxiv-digest
description: "Daily arXiv literature tracking & digest: queries latest arXiv preprints by subject category or keywords, extracts core innovations, and synthesizes an executive Chinese daily digest."
metadata:
  short-description: "arXiv daily literature tracker & Chinese executive digest generator"
---

# arXiv Digest — Daily Literature Tracker & Chinese Executive Brief

Transforms the overwhelming flood of daily arXiv submissions into a structured, highly readable, and actionable Chinese research briefing.

---

## Capabilities

1. **Category & Keyword Filtering**:
   - Monitors primary categories (e.g., `cs.AI`, `cs.LG`, `cs.CV`, `cond-mat.mtrl-sci`).
   - Filters by custom keyword expressions (e.g., `"concrete" OR "cement" OR "topology optimization"`).

2. **Automated Chinese Executive Brief**:
   - Each paper entry is formatted as a 3-bullet insight card:
     - **一句话解决的核心问题 (Problem Solved)**
     - **核心方法与创新机制 (Method Innovation)**
     - **关键实验结果与收益 (Quantitative Gain)**

3. **BibTeX & Citation Ready**:
   - Auto-generates clean, standard BibTeX entries for any paper worth bookmarking.

---

## Usage

```powershell
# Fetch top 5 recent papers in AI/ML materials science
python scripts/fetch_arxiv_digest.py --category "cs.AI" --query "materials" --max_results 5

# Custom keyword search
python scripts/fetch_arxiv_digest.py --query "topology optimization" --max_results 5
```

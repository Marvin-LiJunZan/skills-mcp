---
name: literature-review-workflow
description: "End-to-end literature review workflow: search strategy design, full-text PDF acquisition, structured deep reading, cross-paper evidence matrix compilation, and publication-ready review drafting."
metadata:
  short-description: "End-to-end 5-step literature review & evidence matrix pipeline"
---

# Literature Review Workflow — End-to-End Scientific Synthesis

A systematic 5-stage protocol transforming research queries into a publication-grade literature review section with an airtight evidence chain.

---

## The 5-Step Pipeline

```text
[1. 找文献] ──> [2. 下文献] ──> [3. 读文献] ──> [4. 做证据表] ──> [5. 写综述]
   Search         Fetch          Analyze         Synthesize        Write
```

### Step 1: 找文献 (Search Strategy & Boolean Expansion)
- Construct structured boolean search queries across Web of Science, Scopus, arXiv, and Google Scholar.
- Example query: `("alkali-activated" OR "geopolymer") AND ("rheology" OR "yield stress") AND ("temperature" OR "curing")`.

### Step 2: 下文献 (PDF Acquisition & Metadata Normalization)
- Fetch open-access PDFs via Unpaywall, OpenAlex, or arXiv.
- Store systematically with standardized naming: `[Year]_[FirstAuthor]_[ShortTitle].pdf`.
- Maintain a bijective BibTeX file with matching cite-keys.

### Step 3: 读文献 (Structured Deep Reading & Extraction)
Extract 5 mandatory data fields per paper:
1. **Core Problem**: What exact bottleneck does the study target?
2. **Experimental/Numerical Setup**: Materials, sample dimensions, testing protocol, software/model architecture.
3. **Key Parameters**: Independent and dependent variables.
4. **Quantitative Finding**: Exact numbers, percentage increases, $R^2$, RMSE.
5. **Limitations & Gaps**: What did the authors fail to test or explain?

### Step 4: 做证据表 (Cross-Paper Evidence Matrix)
Synthesize the extracted data into a unified comparative table:

| Citation Key | Material / System | Method / Model | Primary Metric | Quantitative Outcome | Stated Limitation |
|---|---|---|---|---|---|
| Zhang2023 | BFS Slag Paste | PINN + Rheometer | Yield Stress | $\pm 4.2\%$ error | Tested only at $25^\circ\text{C}$ |
| Wang2024 | Fly Ash Mortar | LightGBM | Compressive Str. | $R^2 = 0.94$ | Limited to curing $<28$d |

### Step 5: 写综述 (Narrative Synthesis & Section Drafting)
- Never write a laundry list (*"A did X. B did Y. C did Z."*).
- Group papers by **mechanism and scientific debate**:
  > *"While initial models (Zhang et al., 2023) demonstrated high accuracy under ambient conditions, they falter when thermal activation alters hydration kinetics, a limitation partially addressed by Wang et al. (2024)..."*

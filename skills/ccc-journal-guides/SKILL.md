---
name: ccc-journal-guides
description: Comprehensive Guide for Authors, submission specifications, and automated manuscript adaptation rules for premier journals in Intelligent Construction, Civil & Structural Engineering, Building Materials, and Advanced Materials/Defect Inspection (Automation in Construction, CACAIE, ADVEI, ASCE JCCE, Engineering Structures, Structures, Thin-Walled Structures, ASCE JSE, Construction and Building Materials, Cement and Concrete Composites, Cement and Concrete Research, Journal of Building Engineering, Materials & Design, JMPT, EAAI, NDT & E International).
---

# CCC Journal Guides & Automated Manuscript Adaptation Standards

This skill provides verified, publication-grade **Guides for Authors** and an **Automated Manuscript Adaptation Protocol** for premier academic journals in **Intelligent Construction**, **Civil & Structural Engineering**, **Building Materials & Concrete**, and **Advanced Materials & Manufacturing/Inspection**.

When authoring, revising, or re-targeting an academic paper (LaTeX or Markdown), this skill enables the agent to automatically reconfigure the manuscript to comply with the exact editorial philosophy, length budgets, citation style, and front/back-matter declarations of the target journal.

---

## 1. Master Journal Specification Matrix

| Domain | Journal Name | Publisher | JCR / IF | Main Text Words | Abstract Limit | Highlights Rule | Citation Style |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Intelligent Construction** | *Automation in Construction* (AUTCON) | Elsevier | Q1 / 10.3 | 6,000–9,000 | 150–250 w | Mandatory (3–5, $\le 85$ c) | Numbered `[1]` |
| | *Computer-Aided Civil & Infra. Eng.* (CACAIE) | Wiley | Q1 / 10.0 | 7,000–10,000 | $\le 250$ w | Not required (use GA) | Author-Date (APA) |
| | *Advanced Engineering Informatics* (ADVEI) | Elsevier | Q1 / 8.8 | 6,500–9,500 | 150–250 w | Mandatory (3–5, $\le 85$ c) | Numbered `[1]` |
| | *ASCE J. of Computing in Civil Eng.* (JCCE) | ASCE | Q1/Q2 / 4.6 | $\le 10,000$ equiv | $\le 200$ w | None (Notation list) | Author-Date |
| **Civil & Structural** | *Engineering Structures* (ENGSTRUCT) | Elsevier | Q1 / 5.7 | 6,000–9,500 | 150–250 w | Mandatory (3–5, $\le 85$ c) | Numbered `[1]` |
| | *Structures* | Elsevier / IStructE | Q2 / 4.1 | 6,000–9,000 | 150–250 w | Mandatory (3–5, $\le 85$ c) | Numbered `[1]` |
| | *ASCE J. of Structural Engineering* (JSE) | ASCE | Q1/Q2 / 3.8 | $\le 10,000$ equiv | $\le 200$ w | None (Notation list) | Author-Date |
| | *Thin-Walled Structures* (TWST) | Elsevier | Q1 / 6.4 | 6,000–9,000 | 150–250 w | Mandatory (3–5, $\le 85$ c) | Numbered `[1]` |
| **Building Materials** | *Construction and Building Materials* (CBM) | Elsevier | Q1 / 7.4 | 7,000–8,500 | 150–250 w | Mandatory (3–5, $\le 85$ c) | Numbered `[1]` |
| | *Cement and Concrete Composites* (CCC) | Elsevier | Q1 / 10.8 | 7,000–9,000 | 150–250 w | Mandatory (3–5, $\le 85$ c) | Numbered `[1]` |
| | *Cement and Concrete Research* (CCR) | Elsevier | Q1 / 11.4 | 7,000–10,000 | 150–250 w | Mandatory (3–5, $\le 85$ c) | Numbered `[1]` |
| | *Journal of Building Engineering* (JOBE) | Elsevier | Q1 / 6.4 | 6,500–9,000 | 150–250 w | Mandatory (3–5, $\le 85$ c) | Numbered `[1]` |
| **Materials & Manufacturing** | *Materials & Design* (MATDES) | Elsevier | Q1 / 8.4 | 6,500–9,000 | 150–250 w | Mandatory (3–5, $\le 85$ c) | Numbered `[1]` |
| | *J. of Materials Processing Technology* (JMPT) | Elsevier | Q1 / 6.3 | 6,500–9,000 | 150–250 w | Mandatory (3–5, $\le 85$ c) | Numbered `[1]` |
| | *Eng. Applications of AI* (EAAI) | Elsevier | Q1 / 8.0 | 6,500–9,500 | 150–250 w | Mandatory (3–5, $\le 85$ c) | Numbered `[1]` |
| | *NDT & E International* (NDTEINT) | Elsevier | Q1 / 4.2 | 6,000–8,500 | 150–250 w | Mandatory (3–5, $\le 85$ c) | Numbered `[1]` |

---

## 2. Directory Structure of Official Author Guides

Full-text, detailed guides covering specific editorial red lines, reviewer expectations, and submission instructions are indexed in `guides/`:

- **Intelligent Construction**:
  - `guides/automation-in-construction.md`
  - `guides/computer-aided-civil-and-infrastructure-engineering.md`
  - `guides/advanced-engineering-informatics.md`
  - `guides/asce-journal-of-computing-in-civil-engineering.md`
- **Civil & Structural Engineering**:
  - `guides/engineering-structures.md`
  - `guides/structures.md`
  - `guides/asce-journal-of-structural-engineering.md`
  - `guides/thin-walled-structures.md`
- **Building Materials & Cement/Concrete**:
  - `guides/construction-and-building-materials.md`
  - `guides/cement-and-concrete-composites.md`
  - `guides/cement-and-concrete-research.md`
  - `guides/journal-of-building-engineering.md`
- **Materials, Manufacturing & Defect Metrology**:
  - `guides/materials-and-design.md`
  - `guides/journal-of-materials-processing-technology.md`
  - `guides/engineering-applications-of-artificial-intelligence.md`
  - `guides/ndt-and-e-international.md`

---

## 3. Seven-Stage Automated Manuscript Adaptation Protocol

When adapting a manuscript to a specified target journal, execute the following systematic procedure:

### Stage 1: Narrative Angle & Scope Realignment
- **If target is *Automation in Construction***: Emphasize the IT/computational/robotic contribution (FastWeld-YOLO algorithm, directional attention, real-time edge latency, ISO compliance engine). De-emphasize purely passive material testing.
- **If target is *Construction and Building Materials***: Highlight the physical material system (structural steel grades, weld bead microstructure, heat-affected zone ripples) and practical construction quality assurance.
- **If target is *Engineering Structures* or *Structures***: Emphasize the effect of detected weld defects on structural load-carrying capacity, joint fatigue performance, and design standards (Eurocode 3, AISC).
- **If target is *Materials & Design***: Frame the visual detection output as an input for design tolerance decisions and structural integrity evaluation.
- **If target is *NDT & E International***: Highlight calibrated physical metrology (mm/pixel accuracy, skeletonization length, hydraulic diameter) and non-destructive optical inspection physics.

### Stage 2: Document Class & Typography Reconfiguration
- **Elsevier Journals** (*AUTCON, CBM, ENGSTRUCT, EAAI, CCC, etc.*):
  ```latex
  \documentclass[review,12pt]{elsarticle} % Initial submission
  % or
  \documentclass[5p,times,twocolumn]{elsarticle} % Final layout
  ```
- **Wiley Journals** (*CACAIE*):
  - Single-column, double-spaced with continuous line numbers (`\linenumbers`).
- **ASCE Journals** (*JCCE, JSE*):
  ```latex
  \documentclass[Journal]{ascelike-new}
  ```
  - **Remove all section numbers** (ASCE strictly uses unnumbered section headings).

### Stage 3: Title & Abstract Precision
- Ensure abstract word count strictly respects the journal's upper threshold (typically 250 words; 200 words for ASCE).
- Remove any undefined acronyms, equations, or citations from the abstract.
- Write in a single continuous scholarly paragraph (no bullet points).

### Stage 4: Highlights Generation (The Strict 85-Character Law)
- For all Elsevier journals requiring Highlights, generate exactly 3 to 5 bullet points.
- **Every single bullet must be $\le 85$ characters (including spaces and punctuation)**.
- Store highlights in `highlights.txt` or `highlights.md` for one-click submission.

### Stage 5: Equations, Tables & Figures Standardization
- Tables must strictly follow the three-line `booktabs` format (`\toprule`, `\midrule`, `\bottomrule`) with zero vertical rules.
- Figure dimensions: single-column ($90\text{ mm}$), $1.5$-column ($140\text{ mm}$), or double-column ($190\text{ mm}$).
- Ensure vector graphics (TikZ/EPS/PDF) are used for architectures and plots; $\ge 300\text{ dpi}$ for photographic halftones.

### Stage 6: Citation & Reference Re-styling
- **Numbered Style** (*Elsevier journals*):
  - In-text: `[1]`, `[2,3]`, `[4--6]`.
  - LaTeX BibTeX: `\bibliographystyle{elsarticle-num}`.
- **Author-Date Style** (*ASCE, Wiley CACAIE*):
  - In-text: `(Li and Wang 2024)`.
  - LaTeX BibTeX: `\bibliographystyle{ascelike-new}` or `\bibliographystyle{apacite}`.

### Stage 7: Mandatory Back Matter & Declarations
Inject the mandatory declarations before references:
1. `\section*{CRediT Authorship Contribution Statement}` (standardized 14 CRediT roles).
2. `\section*{Declaration of Competing Interest}` (mandatory statement).
3. `\section*{Data Availability}` (explicit repository/access statement).
4. `\section*{Declaration of Generative AI and AI-Assisted Technologies}` (Elsevier standard AI disclosure).

---

## 4. Automated Compliance Inspection Tool

The skill includes a dedicated command-line verification script:
`skills/ccc-journal-guides/scripts/journal_compliance_checker.py`

### Usage Example:
```bash
# Audit a paper for Automation in Construction
python scripts/journal_compliance_checker.py path/to/main.tex --journal autcon

# Audit for Construction and Building Materials
python scripts/journal_compliance_checker.py path/to/main.tex --journal cbm

# Audit for Engineering Structures
python scripts/journal_compliance_checker.py path/to/main.tex --journal engstruct
```

The script automatically:
- Computes abstract word count and flags deviations.
- Verifies character lengths of each bullet in `highlights.txt` against the 85-character limit.
- Checks for presence of all mandatory declarations (CRediT, Data Availability, Competing Interests).
- Validates document class and citation style.
- Outputs the journal's core editorial red lines to prevent desk rejection.

---

## 5. Absolute Writing Quality Rule (Strict Zero-Listicle Policy)

> [!CAUTION]
> **STRICT ACADEMIC PROSE RULE (严禁“AI味”机械列点)**
> - In all journals covered by this skill, the main body (Introduction, Methodology, Results, Discussion, Conclusion) must consist of **fluent, continuous academic paragraphs**.
> - **Never** overuse bullet points (`itemize`) or numbered lists (`enumerate`) to describe contributions, bottlenecks, or experimental observations. Such listicle patterns are perceived by editors as superficial AI-generated text and lead to immediate rejection.

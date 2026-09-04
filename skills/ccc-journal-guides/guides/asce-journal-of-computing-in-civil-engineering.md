# ASCE Journal of Computing in Civil Engineering (JCCE) - Guide for Authors & Adaptation Rules

## 1. Journal Profile & Editorial Philosophy

- **Official Name**: *Journal of Computing in Civil Engineering*
- **Publisher**: American Society of Civil Engineers (ASCE) | **ISSN**: 0887-3801
- **Indexing & Metrics**: JCR Q1/Q2, Impact Factor: 4.6 (5-Year IF ~5.2)
- **Subject Category**: Engineering, Civil | Computer Science, Interdisciplinary Applications
- **Aims & Scope**: Computing in Civil Engineering publishes research on innovative applications of computing, algorithms, information science, and artificial intelligence in all branches of civil engineering.
- **Core Editorial Philosophy**:
  - Requires clear formulation of computing principles and algorithms integrated with civil engineering mechanics, systems, or structures.
  - Emphasis on reproducibility, rigorous verification, and clear potential for practical professional civil engineering adoption.

---

## 2. Article Types & Word-Equivalent Limits

ASCE calculates manuscript length using a **Word-Equivalent Sizing Worksheet** where text, equations, figures, and tables contribute to total word equivalents.

| Article Type | Word-Equivalent Limit | Abstract Limit | Heading Style | Citation Style |
| :--- | :--- | :--- | :--- | :--- |
| **Technical Paper** | Max 10,000 word-equivalents | Max 200 words | Unnumbered | Author-Date |
| **Technical Note** | Max 3,500 word-equivalents | Max 150 words | Unnumbered | Author-Date |

> [!WARNING]
> ASCE strictly enforces the 10,000 word-equivalent cap. Manuscripts that grossly exceed this threshold are returned without review.

---

## 3. Mandatory ASCE Formatting Rules

### 3.1 Unnumbered Headings (Strict ASCE Rule)
- **Headings must NOT be numbered**. Do not use `1. Introduction` or `2.1 WeldDSA`. Use text-only headings:
  ```latex
  \section*{Introduction}
  \subsection*{Proposed Vision Pipeline}
  ```
- Major headings: Title Case, centered or bold.
- Second-level headings: Bold, left-aligned.
- Third-level headings: Italic, run-in with paragraph text.

### 3.2 Notation List
- If the paper introduces more than a few mathematical symbols, ASCE mandates a **Notation** list placed at the end of the manuscript immediately preceding the References.

### 3.3 Abstract
- Strictly $\le 200$ words.
- Single continuous paragraph without citations or undefined abbreviations.

---

## 4. Citations & Reference Style (Author-Date)

- **In-Text Citation**: Author-Date format:
  - Single author: `(Li 2024)` or `Li (2024)`
  - Two authors: `(Li and Wang 2024)`
  - Three or more: `(Li et al. 2024)`
- **Bibliography Ordering**: Alphabetical by primary author's surname.
- **No Traditional Page Numbers**: ASCE uses Content Identifiers (CIDs) for online articles.
- **LaTeX Template**:
  ```latex
  \documentclass[Journal]{ascelike-new}
  \bibliographystyle{ascelike-new}
  ```

---

## 5. Mandatory Disclosures & Back Matter

- **Data Availability Statement**: Must select from standard ASCE data availability categories (e.g., *Some or all data, models, or code that support the findings of this study are available from the corresponding author upon reasonable request.*)
- **Acknowledgments & Disclaimers**: Disclose any commercial affiliations or patent applications.

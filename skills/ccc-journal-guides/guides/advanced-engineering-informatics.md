# Advanced Engineering Informatics (ADVEI) - Guide for Authors & Adaptation Rules

## 1. Journal Profile & Editorial Philosophy

- **Official Name**: *Advanced Engineering Informatics*
- **Publisher**: Elsevier | **ISSN**: 1474-0346
- **Indexing & Metrics**: JCR Q1, Impact Factor: 8.8 (CiteScore ~16.2)
- **Subject Category**: Engineering, Multidisciplinary | Computer Science, Artificial Intelligence
- **Aims & Scope**: ADVEI focuses on research that supports engineering decision-making through **engineering informatics**, **knowledge acquisition**, **reasoning**, **ontologies**, **cognitive systems**, and **artificial intelligence** applied to complex engineering domains.
- **Core Editorial Philosophy (Crucial for Acceptance)**:
  - **Distinction Between AI Method and Engineering Application**: The editorial policy mandates that the abstract and introduction must clearly demarcate the **informatics/computational knowledge contribution** from the engineering domain application.
  - Submissions that treat AI as a mere black-box prediction tool without modeling engineering logic, semantic reasoning, or domain knowledge representation will be desk-rejected.

---

## 2. Article Types & Word Count Budgets

| Article Type | Main Text Word Limit | Abstract Limit | Highlights Requirement | Keywords Count |
| :--- | :--- | :--- | :--- | :--- |
| **Research Paper** | 6,500 – 9,500 words | 150 – 250 words | Mandatory (3–5 bullets) | 4 – 7 terms |
| **Review Paper** | 9,000 – 14,000 words | 200 – 300 words | Mandatory (3–5 bullets) | 4 – 7 terms |

---

## 3. Mandatory Front Matter Requirements

### 3.1 Highlights (Strict 85-Character Rule)
- 3 to 5 bullet points, each $\le 85$ characters (including spaces).
- Must capture both the informatics/computational breakthrough and the validated engineering outcome.

### 3.2 Abstract
- **Length**: 150 – 250 words.
- **Strict Rule**: Undefined acronyms are forbidden in the title and abstract. Must state:
  1. Engineering problem and knowledge gap.
  2. Computational architecture / reasoning mechanism.
  3. Experimental validation findings.
  4. Decision-support utility in engineering.

### 3.3 Single-Column Initial Review Requirement
- ADVEI requires manuscripts to be formatted in **single-column format** during initial peer review for reviewer annotation.

---

## 4. Manuscript Structure & Narrative Flow

1. **Introduction**:
   - Engineering decision-making context.
   - Comprehensive review of existing AI and informatics methodologies.
   - Distinct definition of knowledge representation and engineering reasoning gaps.
   - Research objectives and core methodological contributions.
2. **Methodological Architecture & Knowledge Modeling**:
   - Explicit formalization of algorithms, data representation schemas, and decision pipelines.
   - Decoupled explanation of visual perception and deterministic engineering standards.
3. **Implementation & Empirical Validation**:
   - Software and hardware implementation architecture.
   - Quantitative performance metrics and ablation evaluations.
4. **Engineering Case Study & Decision Evaluation**:
   - Deployment on real-world engineering artifacts (e.g., welded joint inspection).
   - Traceability, explainability, and regulatory compliance (e.g., ISO/GB standards).
5. **Discussion**:
   - Knowledge scalability, generalizability, and engineering constraints.
6. **Conclusion**:
   - Summary of findings, informatics implications, and future challenges.

---

## 5. Citations, Reference Style & LaTeX Formatting

- **LaTeX Class**:
  ```latex
  \documentclass[review,12pt]{elsarticle}
  ```
- **Reference Style**: Elsevier Numbered format (`[1]`, `[2--4]`).
  ```latex
  \bibliographystyle{elsarticle-num}
  \bibliography{references}
  ```
- **Declarations**: CRediT authorship statement, declaration of interests, data availability statement, and generative AI disclosure clause.

# Engineering Applications of Artificial Intelligence (EAAI) - Guide for Authors & Adaptation Rules

## 1. Journal Profile & Editorial Philosophy

- **Official Name**: *Engineering Applications of Artificial Intelligence*
- **Publisher**: Elsevier | **ISSN**: 0952-1976
- **Indexing & Metrics**: JCR Q1, Impact Factor: 8.0 (5-Year IF ~8.2, CiteScore ~14.5)
- **Subject Category**: Engineering, Multidisciplinary | Computer Science, Artificial Intelligence | Automation & Control Systems
- **Aims & Scope**: Focuses on the application of AI methodologies (machine learning, deep learning, computer vision, evolutionary algorithms, knowledge engineering, fuzzy systems) to solve real-world engineering problems across manufacturing, robotics, civil infrastructure, aerospace, and energy systems.
- **Core Editorial Philosophy (Crucial for Acceptance)**:
  - **Balanced AI Innovation and Real Engineering Utility**: EAAI insists on both **methodological algorithmic novelty** (custom network backbones, attention mechanisms, loss formulations, or re-parameterization pipelines) and **real-world engineering validation** on industrial datasets or physical testbeds.
  - Papers that apply vanilla models without engineering adaptations or domain-informed priors are rejected.

---

## 2. Article Types & Word Count Budgets

| Article Type | Main Text Word Limit | Abstract Limit | Highlights Requirement | Keywords Count |
| :--- | :--- | :--- | :--- | :--- |
| **Research Paper** | 6,500 – 9,500 words | 150 – 250 words | Mandatory (3–5 bullets, $\le 85$ chars) | 4 – 7 terms |
| **Review Article** | 10,000 – 16,000 words | 250 words | Mandatory (3–5 bullets, $\le 85$ chars) | 4 – 7 terms |
| **Short Communication** | 3,000 – 4,500 words | 100 – 150 words | Mandatory (3–5 bullets, $\le 85$ chars) | 3 – 5 terms |

---

## 3. Mandatory Front Matter Requirements

### 3.1 Highlights (Strict 85-Character Constraint)
- 3 to 5 bullet points.
- Maximum 85 characters per bullet including spaces.
- Must articulate AI architecture contribution, efficiency gains, and engineering deployment validation.

### 3.2 Abstract
- 150 – 250 words. Continuous single paragraph without citations.
- Explicitly state: engineering challenge, AI architecture innovation, quantitative benchmark metrics, and practical deployment efficacy.

### 3.3 Graphical Abstract
- Highly recommended. Clean illustration of the end-to-end intelligent engineering pipeline.

---

## 4. Manuscript Structure & Academic Standards

1. **Introduction**:
   - Industrial engineering problem and limitations of conventional non-AI or basic AI methods.
   - Comprehensive review of current machine learning and deep learning applications in the domain.
   - Distinct definition of methodological gap and architectural innovations.
   - Continuous prose summary of scientific contributions.
2. **Proposed AI Methodology & Architecture**:
   - Complete mathematical definitions of operators, loss formulations, and computational flows.
   - Clean vector diagrams of the deep learning architecture.
3. **Experimental Setup & Benchmark Evaluation**:
   - Dataset acquisition parameters, resolution, lighting conditions, and split proportions.
   - Comprehensive ablation study demonstrating the isolated impact of each component.
   - Direct quantitative comparison against modern state-of-the-art architectures.
4. **Hardware Deployment & Real-Time Performance**:
   - Physical execution profiling (GPU/CPU latency, batch size one inference, FPS, parameter count, GFLOPs).
   - Integration into practical engineering platforms or decision-support pipelines.
5. **Conclusion**:
   - Synthesis of verified gains, industrial applicability, and future algorithmic developments.

---

## 5. Citations, Reference Style & LaTeX Formatting

- **LaTeX Template**:
  ```latex
  \documentclass[review,12pt]{elsarticle}
  \bibliographystyle{elsarticle-num}
  \bibliography{references}
  ```
- **In-Text Citations**: Numbered style in brackets (`[1]`, `[2,3]`).
- **Tables & Figures**: Standard `booktabs` layout; high-resolution vector and raster figures.
- **Mandatory Statements**: CRediT authorship statement, declaration of interests, and data availability statement.

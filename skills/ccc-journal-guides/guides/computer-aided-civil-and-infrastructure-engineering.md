# Computer-Aided Civil and Infrastructure Engineering (CACAIE) - Guide for Authors & Adaptation Rules

## 1. Journal Profile & Editorial Philosophy

- **Official Name**: *Computer-Aided Civil and Infrastructure Engineering*
- **Publisher**: Wiley | **ISSN**: 1093-9687 (Print), 1467-8667 (Online)
- **Indexing & Metrics**: JCR Q1 (Top 1%), Impact Factor: 10.0 (5-Year IF ~10.8)
- **Subject Category**: Engineering, Civil | Computer Science, Interdisciplinary Applications | Transportation Science & Technology
- **Aims & Scope**: CACAIE is a scholarly journal devoted to novel computational methodologies and artificial intelligence in bridge, building, environmental, highway, geotechnical, infrastructure, and transportation engineering.
- **Core Editorial Philosophy (Crucial for Acceptance)**:
  - **Methodological Rigor**: CACAIE requires a significant, mathematically rigorous computational advance. Mere empirical applications of standard deep learning algorithms without foundational algorithmic development or rigorous analytical validation are systematically rejected.
  - **Bridge / Infrastructure Repercussions**: The proposed method must clearly demonstrate transformative potential in real-world civil infrastructure systems.

---

## 2. Article Types & Word Count Budgets

| Article Type | Main Text Word Limit | Abstract Limit | Highlights | Keywords |
| :--- | :--- | :--- | :--- | :--- |
| **Research Article** | 7,000 – 10,000 words | 200 – 250 words | Not required (use Graphical Abstract) | 4 – 6 terms |
| **Review Article** | 10,000 – 15,000 words | 250 words | Optional | 4 – 6 terms |

> [!NOTE]
> Wiley encourages double-spaced single-column submissions during the peer review stage, formatted with 12 pt font and continuous line numbering.

---

## 3. Mandatory Front Matter Requirements

### 3.1 Abstract
- **Word Limit**: Strictly $\le 250$ words.
- **Structure**: Unstructured single paragraph. Must explicitly articulate:
  1. The specific civil/infrastructure challenge.
  2. The novel computational/algorithmic formulation.
  3. Quantitative benchmark verification results.
  4. Real-world engineering applicability.
- **Rules**: Absolutely no undefined acronyms, no mathematical symbols in the title, and no literature citations.

### 3.2 Keywords
- Provide 4 to 6 keywords representative of both the computational technique and the civil engineering application (e.g., `Structural health monitoring; Deep neural networks; Directional attention; Weld defect detection; Computer vision`).

### 3.3 Graphical Abstract
- Highly recommended for online indexation. Should visually encapsulate the algorithm-to-infrastructure workflow.

---

## 4. Manuscript Structure & Narrative Conventions

1. **Introduction**:
   - Establish the infrastructure safety/reliability challenge.
   - Critique existing computational and vision-based techniques.
   - Formulate the mathematical and physical gaps in present approaches.
   - Summarize the original methodological contributions without bullet points.
2. **Computational Methodology**:
   - Rigorous mathematical formulation (tensor representations, convergence properties, loss topologies).
   - Clear vector architecture diagrams showing data flow and dimensional transformations.
3. **Experimental / Field Infrastructure Verification**:
   - Verification using genuine structural inspection data or calibrated testbeds.
   - Comprehensive comparative evaluations with recent state-of-the-art methods.
   - Statistical confidence intervals and error distribution analyses.
4. **Engineering Discussion & Computational Complexity**:
   - Floating-point complexity ($O(N)$ vs $O(N^2)$), edge memory requirements, and inference throughput.
   - Robustness under real-world noise (vibration, dust, variable lighting, weather).
5. **Conclusions**:
   - Theoretical contributions and practical deployment takeaways for infrastructure maintenance.

---

## 5. Figures, Tables & Typography

- **Figures**: High-resolution vector graphics (EPS/PDF) or $\ge 600\text{ dpi}$ TIFF. Arial or Times font across all diagrams.
- **Tables**: Clean horizontal lines (`\toprule`, `\midrule`, `\bottomrule`), strictly no vertical lines.
- **Line Numbers**: Mandatory continuous line numbers throughout the entire initial submission.

---

## 6. Citations & Reference Style

- **Reference Style**: Wiley APA Author-Date format.
  - *In-text*: `(Smith, 2023)` or `Smith (2023)` for single author; `(Smith & Jones, 2023)` for two authors; `(Smith et al., 2024)` for three or more authors.
  - *BibTeX Style*:
    ```latex
    \bibliographystyle{apacite} % or natbib with \citep and \citet
    ```
- **Bibliography Alphabetization**: Alphabetical by the surname of the first author.

---

## 7. Mandatory Disclosures

- **Data Availability Statement**: Mandatory declaration of data and code accessibility.
- **Conflict of Interest**: Clear declaration of financial or personal interests.
- **Funding Acknowledgments**: Project grant numbers and funding agencies.

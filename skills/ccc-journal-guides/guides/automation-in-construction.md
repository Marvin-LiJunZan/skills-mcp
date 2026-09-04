# Automation in Construction (AUTCON) - Guide for Authors & Adaptation Rules

## 1. Journal Profile & Editorial Philosophy

- **Official Name**: *Automation in Construction*
- **Publisher**: Elsevier | **ISSN**: 0926-5805
- **Indexing & Metrics**: JCR Q1 (Top 1%), Impact Factor: 10.3 (CiteScore ~18.5)
- **Subject Category**: Engineering, Civil | Construction & Building Technology | Computer Science, Interdisciplinary Applications
- **Aims & Scope**: The journal is the leading international venue focusing on **Information Technologies (IT)**, **computational intelligence**, **robotics**, **digital twins**, **computer vision**, and **automated sensing** across the entire lifecycle of civil and constructed facilities (planning, design, engineering, fabrication, inspection, maintenance, and deconstruction).
- **Core Editorial Philosophy (Crucial for Acceptance)**:
  - **IT / Automation Contribution as Primary Focus**: The editorial board enforces a strict requirement that the core novel contribution must be the **computational method, automation mechanism, robotic framework, or sensing algorithm**, rather than merely a standard case study or routine application of off-the-shelf software to a civil structure.
  - Submissions that only apply existing tools (e.g., standard YOLOv8 or commercial photogrammetry software without architectural, algorithmic, or domain-specific mathematical innovation) will face **immediate desk rejection**.

---

## 2. Article Types & Word Count Budgets

| Article Type | Main Text Word Limit | Abstract Limit | Highlights Requirement | Keywords Count |
| :--- | :--- | :--- | :--- | :--- |
| **Research Paper** | 6,000 – 9,000 words | 150 – 250 words | Mandatory (3–5 bullets) | 1 – 7 terms |
| **Review Paper** | 8,000 – 12,000 words | 200 – 300 words | Mandatory (3–5 bullets) | 1 – 7 terms |
| **Short Communication** | 3,000 – 4,500 words | 100 – 150 words | Mandatory (3–5 bullets) | 1 – 5 terms |

> [!IMPORTANT]
> The main text word count excludes the Title Page, Abstract, Highlights, Keywords, Acknowledgments, References, and Appendices. Concise, dense prose is strongly favored over verbose narrative.

---

## 3. Mandatory Front Matter Requirements

### 3.1 Highlights (Strict 85-Character Constraint)
- **Quantity**: Exactly 3 to 5 bullet points.
- **Length Constraint**: **Maximum 85 characters (including spaces and punctuation)** per bullet point. Exceeding 85 characters triggers automated submission rejection by the editorial portal.
- **Example Compliant Highlights for Weld/Civil Defect Detection**:
  - `FastWeld-YOLO achieves 95.54% mAP@0.5 with only 2.48M parameters.` (61 chars)
  - `Partial convolution reduces redundant backbone FLOPs and memory latency.` (72 chars)
  - `WeldDSA directional strip-pooling captures high-aspect-ratio seam cracks.` (72 chars)
  - `Structural re-parameterization delivers 6.97 ms latency on an RTX GPU.` (69 chars)
  - `WeldVision platform evaluates ISO 5817 compliance deterministically.` (67 chars)

### 3.2 Abstract
- **Word Limit**: 150 – 250 words.
- **Structure**: Single continuous scholarly paragraph.
- **Content Requirements**:
  1. Industrial context and core engineering dilemma.
  2. Proposed algorithmic/hardware innovation.
  3. Key quantitative benchmark findings (mAP, latency, FPS, parameter count).
  4. Real-world validation and significance to construction automation.
- **Restrictions**: Strictly no citations, no undefined abbreviations or acronyms, and no bullet points.

### 3.3 Keywords
- Provide 1 to 7 specific indexing terms.
- Use title case or lower case consistently, separated by semicolons.
- *Recommended Terms*: `Construction automation`; `Weld defect detection`; `Computer vision`; `Deep learning`; `Structural inspection`; `Edge deployment`; `ISO 5817 compliance`.

### 3.4 Graphical Abstract (GA)
- Highly recommended and prominently featured online.
- **Dimensions**: Minimum $531 \times 1328$ pixels (aspect ratio approx. $5:3$ or $16:9$), minimum resolution 300 dpi.
- **Format**: TIFF, EPS, PDF, or JPEG.
- **Content**: Clean visual overview illustrating the workflow from raw construction/sensor input through the proposed computational core to physical inspection/metrology output.

---

## 4. Manuscript Structure & Narrative Conventions

1. **Introduction**:
   - Establish the high-stakes construction or manufacturing challenge.
   - Review recent related literature in construction automation, sensing, and AI.
   - Explicitly highlight the methodological gap in current solutions.
   - Summarize the novel scientific contributions in a continuous, cohesive paragraph (no mechanical listicles).
2. **Methodology / System Architecture**:
   - Provide complete mathematical definitions, network topology, and loss functions.
   - Include high-quality vector architectural diagrams (TikZ or vector SVG/PDF).
   - Detail directional attention, sparse operations, or re-parameterization formulations.
3. **Experimental Validation & Benchmarking**:
   - Dataset acquisition details, sensor configurations, and physical testbeds.
   - Quantitative evaluation across standard metrics (Precision, Recall, mAP@0.5, mAP@0.5:0.95, FPS, FLOPs, Latency).
   - Stepwise ablation studies demonstrating the isolated effect of each component.
   - Quantitative comparison against state-of-the-art published baselines.
4. **Industrial Case Study & Hardware Deployment**:
   - Demonstration on physical hardware (edge devices, robotic platforms, or inspection rigs).
   - Frame latency, memory footprint, and real-time operational feasibility under batch-size-one constraints.
   - Engineering rule evaluation (e.g., ISO 5817, AWS D1.1, GB/T standards).
5. **Discussion**:
   - Computational bottlenecks, sensitivity to illumination/specular reflections, false-alarm suppression.
   - Generalizability to other construction scenarios (bridges, pipelines, steel frames).
6. **Conclusion**:
   - Synthesis of verified findings, practical implications, and future research directions.

---

## 5. Figures, Tables & Mathematical Typesetting

### 5.1 Figure Standards
- **Vector Formats**: EPS or PDF is mandatory for line art, architecture graphs, and plots.
- **Raster Formats**: TIFF or high-quality JPEG for photographs and raw micrographs/inspection imagery.
- **Resolution**:
  - Color / Grayscale photographs: $\ge 300\text{ dpi}$.
  - Line art and diagrams: $\ge 1000\text{ dpi}$.
  - Combination halftone + line art: $\ge 500\text{ dpi}$.
- **Sizing**:
  - Single column: $90\text{ mm}$ ($3.5\text{ in}$).
  - $1.5$-column: $140\text{ mm}$ ($5.5\text{ in}$).
  - Double column: $190\text{ mm}$ ($7.5\text{ in}$).
- **Typography in Figures**: Consistent sans-serif font (Arial or Helvetica), font size $8\text{--}10\text{ pt}$.

### 5.2 Table Standards
- Use the formal three-line table layout (`booktabs` package in LaTeX).
- Only horizontal lines (`\toprule`, `\midrule`, `\bottomrule`). **Vertical lines are strictly prohibited**.
- Align numerical columns using decimal point alignment (`S` column in `siunitx` or `r`).
- Table caption must be placed **above** the table.

### 5.3 Mathematical Notations
- Variables: italicized ($x, y, z$).
- Vectors and matrices: boldface ($\mathbf{x}, \mathbf{W}$).
- Functions and operators: upright roman ($\operatorname{SiLU}, \min, \max, \exp$).

---

## 6. Citations, Reference Style & LaTeX Template

- **Submission LaTeX Class**:
  ```latex
  \documentclass[review,12pt]{elsarticle} % Initial single-column review
  % or
  \documentclass[5p,times,twocolumn]{elsarticle} % Final Elsevier layout
  ```
- **In-Text Citations**: Numbered style in square brackets, e.g., `[1]`, `[2,3]`, `[4--7]`.
- **BibTeX Style**:
  ```latex
  \bibliographystyle{elsarticle-num}
  \bibliography{references}
  ```
- **Reference Entry Essentials**: Every entry must include full author list, full article title, standardized journal abbreviation, volume, year, page range/article number, and DOI.

---

## 7. Mandatory Disclosures & Back Matter

1. **CRediT Authorship Contribution Statement**:
   - Use standard CRediT roles: `Conceptualization`, `Methodology`, `Software`, `Validation`, `Formal analysis`, `Investigation`, `Data curation`, `Writing - original draft`, `Writing - review & editing`, `Visualization`, `Supervision`, `Project administration`, `Funding acquisition`.
2. **Declaration of Competing Interest**:
   - `The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.`
3. **Data Availability Statement**:
   - Explicit declaration detailing where raw data, benchmark images, or model weights are accessible (e.g., repository URL, Zenodo DOI, or upon reasonable request).
4. **Declaration of Generative AI in Scientific Writing**:
   - If AI tools (e.g., LLMs) were utilized for drafting, proofreading, or coding assistance, insert the formal Elsevier AI disclosure clause prior to the references.
5. **Funding Acknowledgments**:
   - Formal grant numbers and sponsoring organizations.

---

## 8. Common Desk-Reject Pitfalls in AUTCON

1. **Lack of IT / Algorithmic Innovation**: Treating standard commercial software or out-of-the-box deep learning models as a "contribution" without novel architectural or mathematical developments.
2. **Highlights Violation**: Writing highlights longer than 85 characters (causes automated rejection at submission).
3. **AI Listicle Style**: Overusing bullet points, colon-lists, or mechanical enumerate sequences in the Introduction and Discussion.
4. **Weak Physical / Field Validation**: Validating solely on synthetic or toy datasets without industrial-scale data or practical hardware runtime measurement.
5. **Missing Standard Elsevier Declarations**: Omitting CRediT, Data Availability, or Competing Interest statements.

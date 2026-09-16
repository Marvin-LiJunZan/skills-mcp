---
name: PaperSpine
description: "Reverse-engineer, deconstruct, and extract the spine of academic papers: thesis statements, logical argument graphs, experimental evidence backbones, and replication recipes."
metadata:
  short-description: "Academic paper deconstruction and spine extraction"
---

# PaperSpine — Academic Paper Deconstruction Engine

PaperSpine breaks down academic papers into their structural and logical components, revealing how top-tier authors construct arguments, frame novel contributions, and connect empirical data to claims.

## Core Deconstruction Dimensions

1. **Problem Framing (The Hook)**:
   - What real-world/theoretical deadlock is exposed?
   - How is previous work synthesized to highlight the precise gap?

2. **The Spine (Logical Argument Chain)**:
   - Premise $\rightarrow$ Mechanism $\rightarrow$ Validation $\rightarrow$ Boundary Conditions.
   - Identifying the single load-bearing claim of the entire paper.

3. **Evidence Matrix Extraction**:
   - Mapping each claim directly to a specific figure, table, or ablation experiment.
   - Auditing whether the data strictly support the claim or overreach.

4. **Replication & Adaptation Blueprint**:
   - Decomposing the methodology into modular components for implementation or adaptation in related projects.

## Output Format: The 5-Point Spine Summary

When executing PaperSpine on a target paper (PDF or text):
```markdown
### 1. The Core Research Question & Non-Triviality
- [What is the exact question? Why could prior methods not answer it?]

### 2. The Primary Thesis / Key Insight
- [The central intellectual contribution in 1-2 sentences]

### 3. Argument Architecture (The Spine)
- Stage 1: [Hypothesis/Foundation]
- Stage 2: [Technical Mechanism]
- Stage 3: [Empirical Proof]

### 4. Critical Evidence Anchors
- Claim 1 -> Supported by Figure X (Key trend / metric)
- Claim 2 -> Supported by Table Y (Comparative baseline superiority)

### 5. Transferable Methodology Takeaways
- [Techniques, narrative framing tricks, or experimental designs worth adopting]
```

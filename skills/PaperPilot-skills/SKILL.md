---
name: PaperPilot-skills
description: "All-in-one research copilot: guides researcher from initial topic exploration through paper retrieval, automated downloading, structured deep-reading, novelty synthesis, and research proposal generation."
metadata:
  short-description: "PaperPilot: Search -> Download -> Deep-Read -> Novelty -> Proposal"
---

# PaperPilot — Autonomous Research Navigator

PaperPilot navigates the entire early-stage research lifecycle: from a vague topic interest to an airtight, experiment-ready research proposal and methodology blueprint.

---

## The 5 Navigation Stages

```text
[Stage 1: 找论文] ──> [Stage 2: 下论文] ──> [Stage 3: 精读论文] ──> [Stage 4: 提炼创新] ──> [Stage 5: 研究方案]
  Paper Search          PDF Fetch            Deep Reading          Novelty Mining       Proposal Blueprint
```

### Stage 1: 找论文 (Precision Reconnaissance)
- Pinpoints 10–20 landmark papers across classic foundation works, latest SOTA, and survey anchors.
- Identifies the author lineages and core research groups in the field.

### Stage 2: 下论文 (Automated Archive & Library Setup)
- Coordinates with local literature databases, arXiv MCP, or Web tools to retrieve full texts.
- Establishes a local `references/` directory and `.bib` registry.

### Stage 3: 精读论文 (Structural Reverse-Engineering)
- Executes deep dissection across the 4 key sections:
  1. Assumptions made in the mathematical formulation.
  2. Dataset characteristics and unstated sampling biases.
  3. Experimental controls and ablation validity.
  4. Unresolved failure cases reported in the appendix or discussion.

### Stage 4: 提炼创新点 (Opportunity Discovery)
- Synthesizes recurring failure modes in current literature into candidate research angles.
- Evaluates feasibility, computational cost, and publication potential.

### Stage 5: 形成研究方案 (Research Blueprint & Protocol)
- Generates a full Research Protocol document:
  - **Title & Working Hypothesis**
  - **Proposed Architecture / Mechanism**
  - **Experimental Design & Baseline Comparisons**
  - **Evaluation Metrics & Verification Criteria**
  - **Timeline & Milestones**

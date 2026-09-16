---
name: survey-builder
description: "Architect and synthesize comprehensive academic literature surveys, review papers, taxonomy trees, chronological evolution maps, and comparative matrices."
metadata:
  short-description: "Comprehensive literature review & survey paper synthesizer"
---

# Survey Builder — Literature Review & Taxonomy Synthesizer

Survey Builder orchestrates the creation of high-impact review and survey papers, transforming disorganized paper lists into thematic taxonomies, comparative matrices, and chronological research trajectories.

---

## The 5-Pillar Survey Structure

Every survey generated under this skill follows the canonical top-tier review architecture:

1. **Motivation & Scope Definition**:
   - Why is a survey needed *now*? (e.g., emergence of LLMs in materials science, multimodal fusion, recent standardization).
   - Inclusion and exclusion criteria (PRISMA framework alignment).

2. **Taxonomy & Conceptual Categorization**:
   - Multi-level classification tree of existing methods/theories.
   - Orthogonal categorization (by input data type, modeling paradigm, application domain, physical scale).

3. **In-Depth Thematic Analysis & Comparison Matrix**:
   - Comprehensive cross-method tables (Strengths, Weaknesses, Computational Complexity, Empirical Benchmarks).
   - Side-by-side comparative matrices rather than isolated paper summaries.

4. **Evolutionary Timeline & Milestones**:
   - Tracing paradigm shifts: *Handcrafted heuristics $\rightarrow$ Classical ML $\rightarrow$ Deep Learning $\rightarrow$ Foundation Models*.

5. **Open Challenges & Future Roadmaps**:
   - Actionable research gaps (Data scarcity, interpretability, real-world deployment, physical consistency).

---

## Quick Usage

```powershell
# Synthesize a comparative matrix from parsed literature
python scripts/build_survey.py --input "literature_corpus.json" --output "survey_draft.md"
```

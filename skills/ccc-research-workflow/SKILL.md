---
name: ccc-research-workflow
description: Coordinate reproducible computational research for the CCC Skills ecosystem, from literature and data provenance through controlled experiments, audits, publication figures, manuscript synchronization, and CCC submission delivery.
metadata:
  short-description: CCC research lifecycle and evidence-chain workflow
---

# CCC Research Workflow

Use this skill when a Cement and Concrete Composites-oriented project contains linked sources, datasets, computational methods, experiments, results, figures, manuscripts, or review/submission packages. It is the lifecycle coordinator for the CCC skills ecosystem; route specialized work to `ccc-literature-scout`, `ccc-paper-converter`, `ccc-author-guide`, or `ccc-journal-guides` when those skills are available.

## Evidence-chain principle

Treat the project as an auditable chain:

`claim → method → data → executable code → saved result → figure/table → manuscript statement`

Before changing a claim, locate its supporting result and provenance. Before changing a result, preserve the prior artifact and record configuration, timestamp, and code revision where practical.

## Lifecycle

1. **Reconnaissance**: inspect README/CONTEXT/status documents, Git state, recent activity, and canonical paths. Separate active, canonical, exploratory, legacy, and generated artifacts.
2. **Evidence contract**: define the question, hypotheses, target claims, baselines, primary metrics, controls, and acceptance criteria. State what each dataset can and cannot support.
3. **Literature and data provenance**: preserve raw/source data, record source identifiers and transformations, and audit units, identity, duplicates, missingness, ranges, leakage, and semantics before modeling.
4. **Executable experiments**: build the smallest canonical pipeline from preprocessing to saved metrics. Keep controls comparable and include baselines, ablations, sensitivity/robustness checks, and held-out or external validation as justified.
5. **Verification**: check domain-appropriate physical/numerical invariants, convergence, gradients or implementation details, mesh/parameter independence, and reproducibility. Recompute key tables from numerical outputs.
6. **Result freeze**: designate the canonical result set and freeze its configuration/code revision. Retain failed, non-converged, and negative-transfer cases.
7. **CCC publication synchronization**: generate figures and tables from frozen results; synchronize LaTeX/Word manuscripts, bibliography, captions, highlights, supplements, declarations, and reviewer responses. Use `ccc-author-guide` for venue compliance audits.
8. **Delivery**: build a clean reproducible package with README, environment requirements, run instructions, source/data manifest, audit reports, manuscript files, and a limitations/known-gaps record.

## Default project layout

Adapt to an existing repository. For a new project, prefer:

```text
project/
├── README.md / CONTEXT.md / RESEARCH_PROTOCOL.md
├── sources/ or references/
├── data/ or dataset/
├── code/
├── experiments/ or benchmarks/
├── results/ or outputs/
├── figures/ or paper/figures/
├── paper/
├── tests/
└── archive/ / backup/ / scratch/
```

## Guardrails

- Do not claim temporal, causal, or external validation when the data only support static or in-domain evaluation.
- Do not mix exploratory outputs with canonical publication results.
- Do not hand-enter quantitative table values when they can be regenerated.
- Do not delete failed runs or unfavorable results; log them and explain their status.
- Do not trust stale README, figure, or manuscript text over current executable evidence.
- If provenance is incomplete, downgrade the claim and state the missing evidence.

For recurring repository patterns and failure modes, read [project-patterns.md](references/project-patterns.md).

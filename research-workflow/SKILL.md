---
name: research-workflow
description: Organize, execute, audit, and package computational research projects from literature and data intake through reproducible experiments, figures, manuscripts, and submission-ready delivery.
metadata:
  short-description: Reproducible computational research workflow
---

# Research workflow

Use this skill when a research project contains multiple linked artifacts—sources, datasets, code, experiments, results, figures, manuscripts, or review/submission packages—and the user wants to advance or audit the work.

## Operating principle

Treat the project as an evidence chain, not a collection of scripts:

`claim → method → data → executable code → saved result → figure/table → manuscript statement`

Before changing a claim, locate the supporting result and its provenance. Before changing a result, preserve the prior artifact and record the new configuration, timestamp, and code revision where practical.

## Workflow

1. **Reconnaissance**
   - Inspect the root, README/CONTEXT/status documents, Git state, and recent activity.
   - Identify canonical paths for raw data, processed data, code, results, figures, paper sources, and archives.
   - Separate active, canonical, exploratory, legacy, and generated artifacts; do not silently merge them.

2. **Research question and evidence contract**
   - State the question, hypotheses, target claims, primary metrics, comparison baselines, and stopping/acceptance criteria.
   - Record what each dataset can and cannot support (for example, static snapshots cannot validate a temporal model).
   - Mark unsupported, uncertain, or exploratory claims explicitly.

3. **Source and data audit**
   - Preserve raw public/source data as immutable inputs.
   - Generate processed data through scripts, retaining source identifiers, transformations, units, exclusions, hashes, and provenance.
   - Check identity, duplicates, missingness, ranges, leakage, train/test separation, and semantic consistency before modeling.

4. **Executable experiment loop**
   - Implement the smallest canonical pipeline: preprocessing → model/solver → evaluation → saved metrics.
   - Keep baselines, controls, seeds, splits, meshes, physical parameters, and convergence criteria comparable.
   - Run ablations, sensitivity/robustness checks, and external or held-out validation when the evidence contract requires them.
   - Retain failed, non-converged, or negative-transfer cases; never remove unfavorable results to improve a summary.

5. **Verification and audit**
   - Verify numerical invariants appropriate to the domain: data integrity, dimensional/physical constraints, solver convergence, gradient or implementation checks, mesh/parameter independence, and reproducibility.
   - Recompute key tables from saved numerical outputs rather than hand-entering values.
   - Distinguish diagnostic evidence from publication-grade evidence and downgrade claims when provenance is incomplete.

6. **Result freeze and communication**
   - Designate a canonical result set and freeze its configuration/code revision.
   - Generate publication figures and tables from that result set, with stable names and source-data links.
   - Synchronize English/Chinese manuscripts, references, captions, highlights, supplementary material, and review responses from the same evidence.
   - Run a final consistency check: every quantitative manuscript claim must resolve to a result, and every reported result must be reproducible.

7. **Delivery**
   - Build a clean package containing README, environment requirements, run instructions, source/data manifest, audit reports, and the manuscript artifacts required by the target venue.
   - Keep backups/archives clearly separated from active canonical files.
   - Report remaining limitations, known provenance gaps, and the exact next action.

## Preferred project layout

Adapt to the existing repository; do not reorganize merely for aesthetics. When a new project has no established convention, prefer:

```text
project/
├── README.md / CONTEXT.md / RESEARCH_PROTOCOL.md
├── sources/ or references/       # literature and source metadata
├── data/                         # raw/processed data with provenance
├── code/                         # reusable methods and pipeline runners
├── experiments/ or benchmarks/   # controlled experiment entry points
├── results/                      # metrics, configs, logs, audits
├── figures/ or paper/figures/    # generated publication assets
├── paper/                        # manuscript, bibliography, supplements
├── tests/                        # invariants and regression checks
└── archive/ / scratch/           # explicitly non-canonical material
```

## Required response style when using this skill

Lead with the current evidence status. Name assumptions and limitations. For changes, state the success criteria, make surgical edits, run proportionate verification, and link the resulting files. Do not claim a result is verified when only the code or a draft figure exists.

For detailed audit questions, consult [project-patterns.md](references/project-patterns.md), which summarizes the recurring structures observed in the user's research repositories.

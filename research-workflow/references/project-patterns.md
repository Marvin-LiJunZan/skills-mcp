# Observed project patterns

The following patterns were observed across active computational research repositories under `C:\JunzanLi_project` and are useful as conventions, not rigid requirements.

## Repeated artifact groups

- `code/`: domain methods, training/solver scripts, figure generators, audits, and pipeline runners.
- `data/` or `dataset/`: source workbooks, imported literature data, processed datasets, and metadata/audit JSON.
- `results/` or `outputs/`: metrics, checkpoints, plots, logs, submission gates, and integrity reports.
- `paper/`: LaTeX sources, bibliography, compiled PDFs, figures, supplements, and compile logs.
- `docs/`, `对话记录/`, or root status files: decisions, current status, review responses, and handoff context.
- `archive/`, `backup/`, `scratch/`, and temporary folders: non-canonical or historical material that must be labeled.

## Strong recurring workflow signals

1. Literature collection is coupled to data extraction and bibliography construction.
2. Data cleaning and semantic verification are increasingly scripted and audited.
3. Experiments include baselines, ablations, transfer/OOD tests, sensitivity studies, or cross-model evaluation.
4. Figures are regenerated from numerical outputs and then synchronized into manuscripts.
5. Publication work includes journal-format checks, reviewer-response matrices, truth/integrity audits, and clean delivery packages.
6. Project history frequently contains claim corrections; the current canonical claim must override stale README, figure, or manuscript text.

## Common failure modes to guard against

- README and code report different models or validation strategies.
- Static external data are used to imply temporal or causal validation.
- Processed data or manually typed table values lack provenance.
- Exploratory and canonical results are mixed in the same summary.
- Failed runs, non-convergence, or negative transfer are deleted instead of logged.
- Figures, English/Chinese papers, and supplementary files drift out of sync.
- Generated build artifacts and temporary files obscure the actual active structure.

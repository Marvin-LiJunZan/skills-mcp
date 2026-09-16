# CCC project patterns

Across active computational research repositories, the recurring artifact groups are:

- `sources/`, `参考文献/`, or `背景资料/`: literature, standards, and source metadata.
- `data/` or `dataset/`: raw workbooks, imported literature data, processed datasets, and provenance/audit JSON.
- `code/`: domain methods, training/solver scripts, figure generators, audits, and pipeline runners.
- `results/` or `outputs/`: metrics, checkpoints, plots, logs, submission gates, and integrity reports.
- `paper/`: LaTeX sources, bibliography, compiled PDFs, figures, supplements, and compile logs.
- `docs/`, `对话记录/`, or root status files: decisions, current status, review responses, and handoff context.
- `archive/`, `backup/`, and `scratch/`: explicitly non-canonical material.

Common lifecycle signals include literature-to-dataset extraction, scripted semantic audits, baselines and ablations, transfer/OOD or sensitivity studies, figure regeneration from numerical outputs, and final manuscript/submission audits.

Common failure modes are mismatched README/code claims, unsupported temporal or causal interpretations, untraceable processed data, hand-entered result tables, deletion of negative results, and drift between figures, bilingual manuscripts, supplements, and review packages.

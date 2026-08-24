---
name: nature-figure
description: >-
  Publication-ready matplotlib figures for Nature/high-impact journals and academic papers.
  Covers bar charts, grouped bars, heatmaps, line/trend plots, radar plots, and multi-panel
  layouts with Nature-style typography (Arial/sans-serif), semantic color palettes, and
  PDF/PNG export conventions. Use when creating scientific figures that must match Nature
  publication standards. Do NOT use for interactive dashboards (Plotly, Bokeh) or
  Illustrator/Figma-first infographic workflows.
---

# Nature Figure Making Skill

A complete guide for producing publication-quality matplotlib figures matching Nature journal standards.
Derived from the [figures4papers](https://github.com/ChenLiu-1996/figures4papers) repository
(papers published in *Nature Machine Intelligence* and top ML venues).

## Quick-start: Mandatory rcParams

Always apply these at the top of every script:

```python
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial']
plt.rcParams['svg.fonttype'] = 'none'          # editable text in SVG/PDF
plt.rcParams['font.size'] = 16                 # 24 for large bar panels
plt.rcParams['axes.spines.right'] = False
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.linewidth'] = 2.5           # 3 for big bars, 2 for compact
plt.rcParams['legend.frameon'] = False
```

Use `text.usetex = True` only when LaTeX is installed and math-rich labels are required.

## When to load this skill

- Matplotlib figures for **papers, slides, or reports** targeting Nature, NeurIPS, ICLR, or similar venues.
- Requests involving **grouped bars, trend lines, heatmaps, radar plots, multi-panel grids**, or **PDF/SVG/high-DPI** output.
- Any mention of "Nature style", "publication figure", "paper figure", or "high-quality scientific plot".

## When NOT to load

- Plotly, Altair, Bokeh, or other interactive/web-first plotting.
- EDA-only plots without a publication target.
- Primary workflow is 3D, GIS, or non-matplotlib tooling.
- Illustrator / Figma–first layout.

## Related files

| File | Open when |
|------|-----------|
| [references/design-theory.md](references/design-theory.md) | Typography, color theory, layout rationale, export policy |
| [references/api.md](references/api.md) | PALETTE, helper function signatures, validation rules |
| [references/common-patterns.md](references/common-patterns.md) | Ultra-wide panels, legend-only axes, print-safe bars |
| [references/tutorials.md](references/tutorials.md) | End-to-end walkthroughs: bars, trends, heatmaps |
| [references/chart-types.md](references/chart-types.md) | Radar, 3D sphere, fill_between, scatter patterns |

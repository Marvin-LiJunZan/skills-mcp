# Common Patterns — Nature Figure Making

Reusable layout and encoding patterns used across publication-grade scripts.

---

## Pattern 1: Ultra-wide multi-metric bar panel

For 3–4 metrics compared across many methods, use a wide canvas so bars and labels don't crowd.

```python
fig = plt.figure(figsize=(45, 12))   # or (28, 6) for fewer metrics
gs = gridspec.GridSpec(1, n_metrics)

for i, metric in enumerate(metrics):
    ax = fig.add_subplot(gs[i])
    ax.bar(x, values[metric], color=colors, ...)
    ax.set_ylabel(metric, fontsize=54, labelpad=12)
    ax.set_xticks([])

# Last panel: legend only
ax_leg = fig.add_subplot(gs[-1])
ax_leg.legend(handles, labels, fontsize=38, loc='center', frameon=False)
ax_leg.set_axis_off()

fig.tight_layout(pad=2)
```

**Rule**: Width often 3–4× height. Allows left-to-right narrative scanning.

---

## Pattern 2: Dedicated legend panel

When the legend is large, give it its own axis so data panels stay clean.

```python
fig, axes = plt.subplots(1, n_data + 1, figsize=(...))

for i, ax in enumerate(axes[:-1]):
    bars = ax.bar(...)
    if i == 0:
        handles, labels = ax.get_legend_handles_labels()

# Legend-only panel
axes[-1].legend(handles, labels, fontsize=28, loc='center', frameon=False)
axes[-1].set_axis_off()
```

---

## Pattern 3: Categorical bars without x-tick labels

When methods are named in the legend, hide x-ticks entirely.

```python
ax.set_xticks([])        # removes ticks and labels
# Alternatively:
ax.set_xticklabels([])   # keeps tick marks, removes labels
```

---

## Pattern 4: Dynamic y-axis tightening

Never use 0–100 when all values are in 80–95.

```python
margin = (values.max() - values.min()) * 0.1   # 10% padding
ax.set_ylim([values.min() - margin, values.max() + margin])

# Manual ticks at clean round numbers
ax.set_yticks([0.75, 0.80, 0.85, 0.90])
ax.tick_params(axis='y', labelsize=36, length=10, width=2)
```

---

## Pattern 5: Alpha-graduated ablation bars (same color, varying opacity)

```python
import numpy as np

blue_rgb = (0.215686, 0.458824, 0.729412)   # #3775BA as float tuple
n_ablations = len(ablation_configs)
alphas = np.linspace(0.2, 1.0, n_ablations)
colors = [(blue_rgb[0], blue_rgb[1], blue_rgb[2], a) for a in alphas]
# Full method → alpha=1.0, most ablated → alpha=0.2
```

---

## Pattern 6: Hatch encoding for print-safe grayscale

Add hatching so bars remain distinct when printed in black-and-white.

```python
hatches = ['/', '\\\\', '.', 'x', 'o', '+']
for bar_container, hatch in zip(grouped_bars, hatches):
    for patch in bar_container:
        patch.set_hatch(hatch)
        patch.set_edgecolor('black')
        patch.set_linewidth(1.5)
```

---

## Pattern 7: Semantic color mapping

Always map colors consistently across all panels in a figure:

```python
method_colors = {
    'Ours':        '#0F4D92',   # blue_main — hero
    'Baseline A':  '#8BCF8B',   # green_3
    'Baseline B':  '#E9A6A1',   # red_2
    'Reference':   '#CFCECE',   # neutral_light
}
colors = [method_colors[m] for m in methods]
```

---

## Pattern 8: In-bar text with luminance-aware color

```python
def annotate_bars(ax, bars, colors, fmt='{:.2f}', fontsize=32, offset=-0.10):
    for bar, color in zip(bars, colors):
        c = color.lstrip('#')
        r, g, b = int(c[0:2],16)/255, int(c[2:4],16)/255, int(c[4:6],16)/255
        lum = 0.299*r + 0.587*g + 0.114*b
        textcolor = 'white' if lum < 0.5 else 'black'
        value = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2,
                value + offset,
                fmt.format(value),
                ha='center', va='bottom',
                fontsize=fontsize, color=textcolor)
```

---

## Pattern 9: Fill-between trend with hatch (print-safe)

```python
ax.fill_between(x, 0, cumsum_series,
                color=fill_color,
                hatch='\\\\\\',   # triple backslash for dense hatch
                edgecolor='black',
                label=label_name)
# Visually erase the border artifacts:
ax.fill_between(x, 0, cumsum_series,
                facecolor='none',
                edgecolor='white',
                linewidth=2)
```

---

## Pattern 10: Annotate events on trend lines

```python
def mark_events(ax, x_labels, y_cumsum, events_dict, dy_fraction=0.1):
    """Add labeled arrows at event dates on a trend line."""
    x_index = {label: i for i, label in enumerate(x_labels)}
    y_lo, y_hi = ax.get_ylim()
    dy = dy_fraction * (y_hi - y_lo)
    for date, label in events_dict.items():
        if date not in x_index:
            continue
        i = x_index[date]
        stars = label.count('*')
        clean_label = label.replace('*', '')
        y_data = y_cumsum[i]
        ax.annotate(
            clean_label,
            xy=(i, y_data),
            xytext=(i, y_data + (1 + 0.8 * stars) * dy),
            ha='center', va='bottom', fontsize=11,
            arrowprops=dict(arrowstyle='-|>', lw=1.3, color='black',
                            shrinkA=0, shrinkB=0, mutation_scale=15)
        )
```

---

## Pattern 11: Grouped bars across multiple datasets (grouped-within-grouped)

```python
num_methods = len(methods)
xtick_positions = []

for dataset_idx, dataset_name in enumerate(datasets):
    x_start = dataset_idx * (num_methods + 1)   # gap of 1 between groups
    ax.bar(
        np.arange(num_methods) + x_start,
        values[dataset_name],
        color=method_colors,
        label=methods if dataset_idx == 0 else ['_nolegend_'] * num_methods,
    )
    xtick_positions.append(np.mean(np.arange(num_methods)) + x_start)

ax.set_xticks(xtick_positions)
ax.set_xticklabels(datasets)
```

---

## Related files

- [skill.md](../skill.md) — When to use this skill
- [api.md](api.md) — Helper function signatures and PALETTE
- [design-theory.md](design-theory.md) — Rationale behind every pattern above
- [tutorials.md](tutorials.md) — End-to-end walkthroughs
- [chart-types.md](chart-types.md) — Radar, 3D, scatter patterns

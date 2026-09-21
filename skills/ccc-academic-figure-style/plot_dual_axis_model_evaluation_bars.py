# -*- coding: utf-8 -*-
"""
CCC & Nature-grade Plotting Template:
Dual Y-Axis Multi-Metric Model Evaluation Bar Chart (双Y轴多指标模型综合评估柱状图)
================================================================================
Design Features (strictly matching Nature/Elsevier reference):
- Dual Y-axes:
    - Left Y-axis: Primary error metrics (MAE, RMSE, MAPE)
    - Right Y-axis: Coefficient of determination (R2) highlighted in distinct dark blue
- Groups along X-axis: Data partitions (e.g., 'Training Set', 'Testing Set')
- Paired bars per metric comparing multiple model architectures (e.g., Model A vs Model B)
- Publication gradient fill on bars:
    - MAE: Teal/Aquamarine to white gradient with crisp dark boundary
    - RMSE: Sky blue to white gradient
    - MAPE: Peach/Orange to white gradient
    - R2: Coral red to white gradient
- Metric values annotated on top of bars (dark blue for R2, black for error metrics)
- Model names rotated 90 degrees vertically at the inside base of each bar
- Top-left boxed legend with 2x2 grid layout
- STRICT RULE: Inward ticks only; Main axis has NO top ticks and NO right ticks;
               Twinx axis has NO top ticks and NO left ticks.

Author: Antigravity CCC Skills Suite
"""

import os
import argparse
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import Rectangle, Patch

# -------------------------------------------------------------------------
# Publication Styling Configuration
# -------------------------------------------------------------------------
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif']
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['xtick.top'] = False       # STRICT: NO top ticks
plt.rcParams['ytick.right'] = False     # STRICT: NO right ticks
plt.rcParams['axes.edgecolor'] = '#222222'
plt.rcParams['axes.linewidth'] = 1.0
plt.rcParams['axes.unicode_minus'] = False

# Gradient top base colors
COLOR_MAE = '#48cae4'   # Teal / Aquamarine
COLOR_RMSE = '#0096c7'  # Azure / Sky Blue
COLOR_MAPE = '#f4a261'  # Peach / Sandy Orange
COLOR_R2 = '#ef5350'    # Coral / Crimson Red
R2_THEME_COLOR = '#0d47a1' # Royal Blue for R2 axis and values


def draw_gradient_bar(ax, x, y, width, height, top_color, n_slices=80):
    """
    Simulates a publication-grade vertical linear gradient fill for a bar
    transitioning smoothly from `top_color` at the top to near-white at the base.
    """
    if height <= 0:
        return
    rgb_top = np.array(mcolors.to_rgb(top_color))
    rgb_base = np.array([0.98, 0.98, 0.98])  # Soft white base

    y_steps = np.linspace(y, y + height, n_slices + 1)
    slice_h = height / n_slices

    for i in range(n_slices):
        t = i / float(n_slices)
        # Power curve for subtle gradient falloff
        color = (1.0 - t**0.75) * rgb_base + (t**0.75) * rgb_top
        rect = Rectangle((x, y_steps[i]), width, slice_h,
                         facecolor=color, edgecolor='none', zorder=3)
        ax.add_patch(rect)

    # Clean enclosing boundary frame
    frame = Rectangle((x, y), width, height,
                      facecolor='none', edgecolor='#222222', linewidth=0.85, zorder=4)
    ax.add_patch(frame)


def plot_dual_axis_model_evaluation_bars(
    eval_dict=None,
    model_names=("TL", "MLP"),
    metric_names=("MAE", "RMSE", "MAPE", "R$^2$"),
    dataset_partitions=("Training Set", "Testing Set"),
    metric_scales=None,
    title="Fig. 12. Quantitative evaluation scores for the TL and MLP models.",
    output_prefix="dual_axis_model_evaluation_bars_standard",
    figsize=(9.2, 6.2),
    dpi=300
):
    """
    Generate publication-grade dual y-axis multi-metric model evaluation bar chart.
    """
    if eval_dict is None:
        # Default representative data matching reference Fig. 12
        eval_dict = {
            "Training Set": {
                "MAE":  {"TL": 0.0023, "MLP": 0.0026},
                "RMSE": {"TL": 0.0037, "MLP": 0.0043},
                "MAPE": {"TL": 0.23,   "MLP": 0.35},
                "R$^2$": {"TL": 0.89,   "MLP": 0.83},
            },
            "Testing Set": {
                "MAE":  {"TL": 0.0026, "MLP": 0.0034},
                "RMSE": {"TL": 0.0040, "MLP": 0.0062},
                "MAPE": {"TL": 0.44,   "MLP": 0.67},
                "R$^2$": {"TL": 0.91,   "MLP": 0.77},
            }
        }

    if metric_scales is None:
        # Default: scale MAPE (percentage/fraction) by 0.006 to sit nicely alongside 0.002-0.006 MAE
        metric_scales = {"MAE": 1.0, "RMSE": 1.0, "MAPE": 0.0065, "R$^2$": 1.0}

    fig, ax_left = plt.subplots(figsize=figsize, dpi=dpi)
    ax_right = ax_left.twinx()

    # Determine scaling factors and limits
    left_plot_vals = []
    for part in dataset_partitions:
        for m in metric_names[:-1]:
            scale = metric_scales.get(m, 1.0)
            for mdl in model_names:
                left_plot_vals.append(eval_dict[part][m][mdl] * scale)

    max_left = max(left_plot_vals) if left_plot_vals else 0.008
    ax_left.set_ylim(0, max_left * 1.32)
    ax_right.set_ylim(0, 1.25)

    # Metric colors mapping
    metric_colors = [COLOR_MAE, COLOR_RMSE, COLOR_MAPE, COLOR_R2]

    # Bar layout geometry
    bar_width = 0.46
    intra_pair_gap = 0.02
    inter_metric_gap = 0.18
    inter_partition_gap = 0.85

    current_x = 0.5
    partition_centers = []

    for part_idx, part_name in enumerate(dataset_partitions):
        part_start_x = current_x
        for m_idx, m_name in enumerate(metric_names):
            color = metric_colors[m_idx % len(metric_colors)]
            is_r2 = (m_idx == len(metric_names) - 1)
            target_ax = ax_right if is_r2 else ax_left
            scale = metric_scales.get(m_name, 1.0) if not is_r2 else 1.0

            for mdl_idx, mdl_name in enumerate(model_names):
                raw_val = eval_dict[part_name][m_name][mdl_name]
                plot_height = raw_val if is_r2 else raw_val * scale
                bx = current_x

                # Draw gradient bar
                draw_gradient_bar(target_ax, bx, 0, bar_width, plot_height, color)

                # Label on top of bar (shows true raw value)
                val_text = f"{raw_val:g}" if isinstance(raw_val, (int, float)) else str(raw_val)
                txt_color = R2_THEME_COLOR if is_r2 else ('#6a1b9a' if m_name == 'MAPE' else '#222222')
                target_ax.text(bx + bar_width / 2.0, plot_height + (0.018 if is_r2 else max_left * 0.018),
                               val_text, ha='center', va='bottom', fontsize=9.5,
                               color=txt_color, zorder=6)

                # Vertical model label at base of bar
                target_ax.text(bx + bar_width / 2.0, (0.02 if is_r2 else max_left * 0.02),
                               mdl_name, ha='center', va='bottom', rotation=90,
                               fontsize=10.0, color='#111111', zorder=7)

                current_x += bar_width + intra_pair_gap

            current_x += inter_metric_gap

        part_end_x = current_x - inter_metric_gap
        partition_centers.append((part_start_x + part_end_x) / 2.0)
        current_x += inter_partition_gap

    total_x_span = current_x - inter_partition_gap + 0.5
    ax_left.set_xlim(0, total_x_span)
    ax_right.set_xlim(0, total_x_span)

    # Set Partition labels on bottom X-axis
    ax_left.set_xticks(partition_centers)
    ax_left.set_xticklabels(dataset_partitions, fontsize=12.0)
    ax_left.tick_params(axis='x', which='both', length=0, pad=9)  # Hide bottom x tick marks

    # Configure Left Y-Axis
    ax_left.set_ylabel('Evaluation', fontsize=12.0, labelpad=7)
    ax_left.tick_params(axis='y', which='major', direction='in', length=5.0, width=0.9,
                        top=False, right=False, labelsize=11.0)
    ax_left.grid(True, linestyle='--', color='#e0e0e0', linewidth=0.75, alpha=0.75, zorder=1)

    # Configure Right Y-Axis (R2 axis in distinct blue)
    ax_right.set_ylabel(r'$R^2$', fontsize=12.0, color=R2_THEME_COLOR, labelpad=9)
    ax_right.spines['right'].set_color(R2_THEME_COLOR)
    ax_right.spines['right'].set_linewidth(1.1)
    ax_right.spines['top'].set_visible(False)
    ax_left.spines['top'].set_visible(False)
    ax_right.spines['left'].set_visible(False)
    ax_right.tick_params(axis='y', which='major', direction='in', length=5.0, width=1.0,
                         colors=R2_THEME_COLOR, top=False, left=False, labelsize=11.0)
    ax_right.set_yticks([0.0, 0.3, 0.6, 0.9, 1.2])

    # STRICT: Check tick rules
    ax_left.tick_params(top=False, right=False)
    ax_right.tick_params(top=False, left=False)

    # Legend in top-left: 2 columns x 2 rows
    legend_patches = [
        Patch(facecolor=COLOR_MAE, edgecolor='#222222', label='MAE'),
        Patch(facecolor=COLOR_MAPE, edgecolor='#222222', label='MAPE'),
        Patch(facecolor=COLOR_RMSE, edgecolor='#222222', label='RMSE'),
        Patch(facecolor=COLOR_R2, edgecolor='#222222', label=r'R$^2$'),
    ]
    ax_left.legend(handles=legend_patches, loc='upper left', ncol=2,
                   frameon=True, facecolor='#ffffff', edgecolor='#222222',
                   framealpha=0.98, fontsize=11.0, handlelength=2.0, handleheight=1.0,
                   columnspacing=1.8, borderpad=0.55)

    # Bottom Caption
    if title:
        plt.figtext(0.5, 0.012, title, ha='center', fontsize=11.5, fontweight='bold')

    plt.tight_layout(rect=[0.02, 0.04, 0.98, 0.98])

    out_png = f"{output_prefix}.png"
    out_pdf = f"{output_prefix}.pdf"
    fig.savefig(out_png, dpi=dpi, bbox_inches='tight')
    fig.savefig(out_pdf, bbox_inches='tight')
    plt.close(fig)
    print(f"[Dual-Axis Model Bars] Figure saved to:\n  {os.path.abspath(out_png)}\n  {os.path.abspath(out_pdf)}")
    return out_png, out_pdf


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate dual y-axis multi-metric model evaluation bar chart.")
    parser.add_argument('--output', type=str, default='dual_axis_model_evaluation_bars_standard', help='Output prefix')
    args = parser.parse_args()

    print("Generating demo Dual-Axis Model Evaluation Bar chart matching reference...")
    plot_dual_axis_model_evaluation_bars(
        title="Fig. 12. Quantitative evaluation scores for the TL and MLP models.",
        output_prefix=args.output
    )

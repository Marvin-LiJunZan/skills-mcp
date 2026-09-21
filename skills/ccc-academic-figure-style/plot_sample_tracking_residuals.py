# -*- coding: utf-8 -*-
"""
CCC & Nature-grade Plotting Template:
Sample-Wise Prediction Tracking & Residual Distribution Plot (逐样本预测跟踪与残差分布图)
================================================================================
Design Features (strictly matching Nature/Elsevier reference):
- Top curves:
    - Cyan solid line: Ground truth experimental values ('Experiment')
    - Deep blue solid line: Model predictions ('Model prediction')
- Divider: Vertical dashed line separating 'Training Set' and 'Testing Set'
- Bottom curve:
    - Coral red line with circular markers: Prediction error / residual ('Error')
    - Horizontal dashed gray envelope lines for maximum and minimum error bounds
    - Exact error bounds annotated on the right margin outside the axes
    - 'Training Set' and 'Testing Set' labels positioned cleanly in free space below lower bound
- STRICT RULE: Inward ticks on Left and Bottom axes only; Absolutely NO top ticks and NO right ticks.

Author: Antigravity CCC Skills Suite
"""

import os
import argparse
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

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


def generate_mock_tracking_data(n_train=200, n_test=50, target_type='strength', random_state=42):
    """Generate realistic synthetic sequences for training and testing tracking."""
    rng = np.random.RandomState(random_state)
    n_tot = n_train + n_test
    if target_type == 'strength':
        # True fluctuating values
        base = rng.uniform(20.0, 110.0, size=n_tot)
        # Training residuals (very small)
        res_tr = rng.normal(0.0, 0.4, size=n_train)
        # Testing residuals (slightly larger with a couple of peaks)
        res_te = rng.normal(0.0, 2.5, size=n_test)
        res_te[int(n_test * 0.4)] = 8.5
        res_te[int(n_test * 0.75)] = -11.2
        unit = 'MPa'
        name = 'Compressive strength'
    else:
        base = rng.uniform(120.0, 350.0, size=n_tot)
        res_tr = rng.normal(0.0, 1.8, size=n_train)
        res_te = rng.normal(0.0, 12.0, size=n_test)
        res_te[int(n_test * 0.5)] = -45.0
        res_te[int(n_test * 0.8)] = 28.0
        unit = 'mm'
        name = 'Fresh fluidity'

    y_tr = base[:n_train]
    p_tr = y_tr + res_tr
    y_te = base[n_train:]
    p_te = y_te + res_te
    return y_tr, p_tr, y_te, p_te, name, unit


def plot_tracking_panel(ax, y_tr, p_tr, y_te, p_te, target_name, unit, model_label="Model",
                        panel_title="", x_label="Number"):
    """
    Plots a single sample-wise prediction tracking and residual panel on `ax`.
    """
    n_tr = len(y_tr)
    n_te = len(y_te)
    n_tot = n_tr + n_te

    # Concatenate training and testing sequences
    y_all = np.concatenate([y_tr, y_te])
    p_all = np.concatenate([p_tr, p_te])
    err_all = p_all - y_all
    x_idx = np.arange(1, n_tot + 1)

    # Maximum and minimum error bounds (envelope)
    bound_pos = float(np.round(np.max(err_all), 1 if unit in ['MPa', 'mm'] else 3))
    bound_neg = float(np.round(np.min(err_all), 1 if unit in ['MPa', 'mm'] else 3))

    # Grid (subtle)
    ax.grid(True, linestyle='--', color='#f0f0f0', linewidth=0.7, alpha=0.9, zorder=1)

    # 1. Experiment curve (Cyan line)
    line_exp, = ax.plot(x_idx, y_all, color='#00b4d8', linewidth=1.15, alpha=0.95, zorder=3, label='Experiment')

    # 2. Model Prediction curve (Deep blue line)
    line_pred, = ax.plot(x_idx, p_all, color='#1565c0', linewidth=1.05, alpha=0.90, zorder=4, label=f'{model_label} prediction')

    # 3. Error curve (Red line with circular markers)
    line_err, = ax.plot(x_idx, err_all, color='#e53935', linewidth=0.85, marker='o', markersize=2.8,
                        markerfacecolor='#ef5350', markeredgecolor='#b71c1c', markeredgewidth=0.5,
                        alpha=0.85, zorder=5, label='Error')

    # 4. Zero reference line for error
    ax.axhline(0, color='#9e9e9e', linestyle=':', linewidth=0.8, alpha=0.75, zorder=2)

    # 5. Horizontal error bound dashed lines
    ax.axhline(bound_pos, color='#9e9e9e', linestyle='--', linewidth=0.85, alpha=0.85, zorder=2)
    ax.axhline(bound_neg, color='#9e9e9e', linestyle='--', linewidth=0.85, alpha=0.85, zorder=2)

    # Annotate error bound numbers on the right side outside axes
    ax.text(1.01, bound_pos, f"{bound_pos:+g}", transform=ax.get_yaxis_transform(),
            color='#222222', fontsize=9.5, va='center', ha='left', clip_on=False, zorder=6)
    ax.text(1.01, bound_neg, f"{bound_neg:+g}", transform=ax.get_yaxis_transform(),
            color='#222222', fontsize=9.5, va='center', ha='left', clip_on=False, zorder=6)

    # 6. Vertical divider between Training Set and Testing Set
    divider_x = n_tr + 0.5
    ax.axvline(divider_x, color='#424242', linestyle='--', linewidth=1.1, zorder=4)

    # 7. Set clean y limits to leave ample space at bottom for labels below the lower dashed line
    y_raw_min, y_raw_max = ax.get_ylim()
    y_lower = bound_neg - max(abs(bound_neg) * 0.65, 12.0)
    y_upper = y_raw_max + (y_raw_max - y_lower) * 0.08
    ax.set_ylim(y_lower, y_upper)

    # Labels for Training Set and Testing Set at bottom in clear free space well below dashed line
    y_text_pos = y_lower + (bound_neg - y_lower) * 0.45
    ax.text(divider_x * 0.025, y_text_pos, 'Training Set', color='#757575', fontsize=10.5,
            fontweight='normal', ha='left', va='center', zorder=6)
    ax.text(divider_x + 8, y_text_pos, 'Testing Set', color='#757575', fontsize=10.5,
            fontweight='normal', ha='left', va='center', zorder=6)

    # 8. Legend at the top (Experiment, Model prediction, Error)
    ax.legend(handles=[line_exp, line_pred, line_err], loc='upper left', ncol=3,
              frameon=False, fontsize=10.5, handlelength=2.2, columnspacing=1.8)

    # 9. Axis labels and limits
    ax.set_xlabel(x_label, fontsize=11.5, labelpad=5)
    ax.set_ylabel(f'{target_name} ({unit})', fontsize=11.5, labelpad=6)
    ax.set_xlim(0, n_tot + 1)

    # 10. STRICT TICK FORMATTING: No top ticks, no right ticks!
    ax.tick_params(axis='both', which='major', direction='in', length=5, width=0.9,
                   top=False, right=False, labelsize=10.5)
    ax.tick_params(axis='both', which='minor', direction='in', length=2.5, width=0.7,
                   top=False, right=False)

    # Subplot caption text
    if panel_title:
        ax.text(0.5, -0.22, panel_title, transform=ax.transAxes,
                fontsize=11.5, ha='center', va='top')


def plot_sample_tracking_residuals(y_tr_list, p_tr_list, y_te_list, p_te_list,
                                   target_names, units, model_labels, titles=None,
                                   output_prefix="sample_tracking_residuals_standard",
                                   figsize=(10.5, 8.8), dpi=300):
    """
    Generate stacked 2-row x 1-column publication prediction tracking & residual plot.
    """
    n_panels = len(y_tr_list)
    fig, axes = plt.subplots(n_panels, 1, figsize=figsize, dpi=dpi)
    if n_panels == 1:
        axes = [axes]
    plt.subplots_adjust(hspace=0.38, left=0.08, right=0.93, top=0.96, bottom=0.08)

    for i in range(n_panels):
        t_title = titles[i] if titles and i < len(titles) else f"({chr(97+i)}) Accuracy of the {model_labels[i]} model predictions and residual tracking"
        plot_tracking_panel(
            ax=axes[i],
            y_tr=np.asarray(y_tr_list[i]),
            p_tr=np.asarray(p_tr_list[i]),
            y_te=np.asarray(y_te_list[i]),
            p_te=np.asarray(p_te_list[i]),
            target_name=target_names[i],
            unit=units[i],
            model_label=model_labels[i],
            panel_title=t_title
        )

    out_png = f"{output_prefix}.png"
    out_pdf = f"{output_prefix}.pdf"
    fig.savefig(out_png, dpi=dpi, bbox_inches='tight')
    fig.savefig(out_pdf, bbox_inches='tight')
    plt.close(fig)
    print(f"[Sample Tracking] Figure saved to:\n  {os.path.abspath(out_png)}\n  {os.path.abspath(out_pdf)}")
    return out_png, out_pdf


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate sample-wise prediction tracking and residual distribution plot.")
    parser.add_argument('--output', type=str, default='sample_tracking_residuals_standard', help='Output prefix')
    args = parser.parse_args()

    print("Generating demo Sample-Wise Prediction Tracking & Residual plot...")
    y_tr1, p_tr1, y_te1, p_te1, name1, unit1 = generate_mock_tracking_data(n_train=480, n_test=120, target_type='strength', random_state=42)
    y_tr2, p_tr2, y_te2, p_te2, name2, unit2 = generate_mock_tracking_data(n_train=224, n_test=57, target_type='fluidity', random_state=101)

    plot_sample_tracking_residuals(
        y_tr_list=[y_tr1, y_tr2],
        p_tr_list=[p_tr1, p_tr2],
        y_te_list=[y_te1, y_te2],
        p_te_list=[p_te1, p_te2],
        target_names=[name1, name2],
        units=[unit1, unit2],
        model_labels=['ExtraTrees', 'TabPFN v2 + ResBoost'],
        titles=[
            '(a) Accuracy of the ExtraTrees model predictions and residual tracking',
            '(b) Accuracy of the TabPFN v2 + CatBoost ResBoost model predictions and residual tracking'
        ],
        output_prefix=args.output
    )

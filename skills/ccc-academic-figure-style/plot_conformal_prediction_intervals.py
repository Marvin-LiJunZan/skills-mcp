# -*- coding: utf-8 -*-
"""
CCC & Nature-grade Plotting Template:
Conformal Prediction Interval Coverage Plot (置信预测区间覆盖图)
================================================================================
Design Features:
- Split conformal quantile computation under 1 - alpha nominal confidence (e.g., 95%)
- Test samples sorted in ascending order of true targets to form a smooth benchmark curve
- Light blue shaded prediction interval band (y_pred +/- q_conformal)
- Open blue diamonds for point predictions with optional whisker bars
- Open red circles for ground truth experiment targets
- Highlighted markers (red cross / markers) for uncovered out-of-interval samples
- Standard publication summary metrics box (Empirical Coverage EC, Mean Interval Width MIW, R2, RMSE)
- STRICT RULE: Inward ticks on Left and Bottom axes only; Absolutely NO top ticks and NO right ticks.

Author: Antigravity CCC Skills Suite
"""

import os
import argparse
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

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


def generate_mock_uq_data(n_samples=120, target_type='strength', random_state=42):
    """Generate realistic synthetic regression test data with heteroscedastic noise."""
    rng = np.random.RandomState(random_state)
    if target_type == 'strength':
        y_true = np.sort(rng.uniform(5.0, 130.0, size=n_samples))
        noise = rng.normal(0.0, 2.5 + 0.03 * y_true, size=n_samples)
        # Add 2-3 outlier failure points
        noise[int(n_samples * 0.85)] += 14.5
        noise[int(n_samples * 0.15)] -= 9.2
        y_pred = y_true + noise
        unit = 'MPa'
        name = 'Compressive Strength'
    else:
        y_true = np.sort(rng.uniform(80.0, 360.0, size=n_samples))
        noise = rng.normal(0.0, 10.0 + 0.02 * y_true, size=n_samples)
        noise[int(n_samples * 0.90)] += 42.0
        y_pred = y_true + noise
        unit = 'mm'
        name = 'Fresh Fluidity Flow'
    return y_true, y_pred, name, unit


def plot_conformal_panel(ax, y_true, y_pred, target_name, unit, model_label="Regression Model",
                         confidence=0.95, panel_title=""):
    """
    Plots a single conformal prediction interval coverage panel on `ax`.
    """
    # 1. Sort samples by true target values
    order = np.argsort(y_true)
    y_true_sorted = y_true[order]
    y_pred_sorted = y_pred[order]
    n_samples = len(y_true)
    x = np.arange(n_samples)

    # 2. Conformal quantile computation (finite-sample correction)
    res = np.abs(y_true - y_pred)
    res_sorted = np.abs(y_true_sorted - y_pred_sorted)
    q_level = np.ceil((n_samples + 1) * confidence) / n_samples
    q_level = min(1.0, max(0.0, q_level))
    q_val = np.percentile(res, q_level * 100.0)

    # Interval bounds
    lo = y_pred_sorted - q_val
    hi = y_pred_sorted + q_val

    # Coverage metrics
    covered = res_sorted <= q_val
    uncovered = ~covered
    n_covered = np.sum(covered)
    ec = n_covered / n_samples
    miw = 2.0 * q_val
    ss_tot = np.sum((y_true - np.mean(y_true))**2)
    ss_res = np.sum((y_true - y_pred)**2)
    r2 = 1.0 - (ss_res / ss_tot) if ss_tot > 0 else 0.0
    rmse = np.sqrt(np.mean(res**2))

    # 3. Grid
    ax.grid(True, linestyle='--', color='#ececec', linewidth=0.75, alpha=0.85, zorder=1)

    # 4. Shaded interval envelope
    ax.fill_between(x, lo, hi, color='#90caf9', alpha=0.52, zorder=2, label=f'{int(confidence*100)}% Interval Band')
    ax.plot(x, lo, color='#42a5f5', linewidth=0.85, alpha=0.9, zorder=2)
    ax.plot(x, hi, color='#42a5f5', linewidth=0.85, alpha=0.9, zorder=2)

    # 5. Point predictions (Open blue diamonds with error stems)
    ax.vlines(x, lo, hi, color='#64b5f6', linewidth=0.45, alpha=0.4, zorder=2)
    ax.scatter(x, y_pred_sorted, marker='d', s=34, facecolor='#ffffff', edgecolor='#1976d2',
               linewidth=1.1, zorder=4, label=f'Predicted {target_name}')

    # 6. True experimental targets (Open red circles)
    ax.scatter(x, y_true_sorted, marker='o', s=24, facecolor='#ffffff', edgecolor='#e53935',
               linewidth=1.0, zorder=5, label=f'True {target_name}')

    # 7. Highlight uncovered failure samples
    if np.any(uncovered):
        ax.scatter(x[uncovered], y_true_sorted[uncovered], marker='x', s=42, color='#b71c1c',
                   linewidth=1.6, zorder=6, label='Uncovered Failure')

    # 8. Metrics annotation box
    metrics_str = (
        f"$\\mathbf{{EC}} = {ec:.3f}$ ({n_covered}/{n_samples})\n"
        f"$\\mathbf{{MIW}} = {miw:.2f}$ {unit}\n"
        f"$R^2 = {r2:.4f}$\n"
        f"$\\mathrm{{RMSE}} = {rmse:.2f}$ {unit}"
    )
    ax.text(0.70, 0.28, metrics_str, transform=ax.transAxes, fontsize=9.5,
            verticalalignment='top', horizontalalignment='left',
            bbox=dict(boxstyle='square,pad=0.55', facecolor='#ffffff', edgecolor='#777777',
                      linewidth=0.75, alpha=0.96),
            zorder=7)

    # 9. Legend
    handles, labels = ax.get_legend_handles_labels()
    patch_cov = Patch(facecolor='#90caf9', edgecolor='#42a5f5', alpha=0.6, label='Covered')
    patch_unc = Patch(facecolor='#ffcdd2', edgecolor='#e53935', alpha=0.8, label='Uncovered')
    all_handles = [
        Line2D([0], [0], marker='d', color='w', markeredgecolor='#1976d2', markerfacecolor='w', markersize=6.5, label=f'Predicted {target_name}'),
        Line2D([0], [0], marker='o', color='w', markeredgecolor='#e53935', markerfacecolor='w', markersize=5.5, label=f'True {target_name}'),
        Patch(facecolor='#90caf9', edgecolor='#42a5f5', alpha=0.52, label=f'{int(confidence*100)}% Interval Band'),
        patch_cov,
        patch_unc
    ]
    ax.legend(handles=all_handles, loc='upper left', frameon=True, facecolor='#ffffff',
              edgecolor='#333333', framealpha=0.95, fontsize=8.5, handlelength=1.6)

    # 10. Labels and axes formatting
    ax.set_xlabel('Test Samples (sorted by True target values)', fontsize=10.5, labelpad=5)
    ax.set_ylabel(f'{target_name} ({unit})', fontsize=10.5, labelpad=6)
    ax.set_xlim(-1, n_samples)
    y_min, y_max = ax.get_ylim()
    ax.set_ylim(min(0, y_min), y_max + 0.05 * (y_max - y_min))

    # STRICT: INWARD TICKS ONLY ON LEFT AND BOTTOM
    ax.tick_params(axis='both', which='major', direction='in', length=4.5, width=0.85,
                   top=False, right=False, labelsize=9.5)
    ax.tick_params(axis='both', which='minor', direction='in', length=2.5, width=0.6,
                   top=False, right=False)

    if panel_title:
        ax.set_title(panel_title, fontsize=11, fontweight='bold', pad=8)


def plot_conformal_prediction_intervals(y_true_list, y_pred_list, target_names, units, model_labels,
                                        titles=None, output_prefix="conformal_uq_standard",
                                        figsize=(11.0, 8.8), dpi=300):
    """
    Generate stacked 2-row x 1-column publication conformal uncertainty figure.
    """
    n_panels = len(y_true_list)
    fig, axes = plt.subplots(n_panels, 1, figsize=figsize, dpi=dpi)
    if n_panels == 1:
        axes = [axes]
    plt.subplots_adjust(hspace=0.38, left=0.08, right=0.96, top=0.95, bottom=0.08)

    for i in range(n_panels):
        t_title = titles[i] if titles and i < len(titles) else f"({chr(97+i)}) {target_names[i]} ({model_labels[i]})"
        plot_conformal_panel(
            ax=axes[i],
            y_true=np.asarray(y_true_list[i]),
            y_pred=np.asarray(y_pred_list[i]),
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
    print(f"[Conformal UQ] Figure saved to:\n  {os.path.abspath(out_png)}\n  {os.path.abspath(out_pdf)}")
    return out_png, out_pdf


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate publication conformal prediction interval coverage plot.")
    parser.add_argument('--output', type=str, default='conformal_uq_standard', help='Output file prefix (without extension)')
    args = parser.parse_args()

    # Demo execution with synthetic datasets
    print("Generating demo Conformal Prediction Interval plot...")
    y_true1, y_pred1, name1, unit1 = generate_mock_uq_data(n_samples=120, target_type='strength', random_state=42)
    y_true2, y_pred2, name2, unit2 = generate_mock_uq_data(n_samples=57, target_type='fluidity', random_state=101)

    plot_conformal_prediction_intervals(
        y_true_list=[y_true1, y_true2],
        y_pred_list=[y_pred1, y_pred2],
        target_names=[name1, name2],
        units=[unit1, unit2],
        model_labels=['ExtraTrees', 'TabPFN v2 + ResBoost'],
        titles=[
            '(a) Compressive Strength (ExtraTrees, Hold-out N=120)',
            '(b) Fresh Fluidity Flow (TabPFN v2 + CatBoost ResBoost, Hold-out N=57)'
        ],
        output_prefix=args.output
    )

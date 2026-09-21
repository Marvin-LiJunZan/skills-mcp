# -*- coding: utf-8 -*-
"""
Joint Parity Plot with Marginal Distributions & Golden Drop Shadow Legend
Conforming strictly to Nature/Elsevier/CCC journal standards & user reference (media_1789993872280.png & media_1789994060601.png):
- Calibrated Modern Color Palette (lowered 1 notch, vibrant & fresh):
  * Train: Vibrant Coral Vermilion (#E53935)
  * Test: Crisp Cyan Ocean Blue (#0097A7)
- Legend with Golden-Yellow Drop Shadow (#FFA000) at bottom-right
- Central 1:1 Parity Scatter: Experimental vs Predicted (y = x, +-15% error envelope)
- Top Marginal Axis: Density distribution (KDE, alpha=0.18) of Experimental ground truth
- Right Marginal Axis: Density distribution (horizontal KDE, alpha=0.18) of Model predictions
- Strict Times New Roman typography, inward ticks, boxed spines, no top/right ticks on main axis.
"""

import argparse
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
import matplotlib.patheffects as pe
import seaborn as sns

# CCC Universal Styling & Typography
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif', 'serif']
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['font.size'] = 9.0
plt.rcParams['axes.edgecolor'] = '#222222'
plt.rcParams['axes.linewidth'] = 0.85
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['xtick.top'] = False
plt.rcParams['ytick.right'] = False

# CCC Calibrated Red-Blue Palette & Signature Bright Yellow Shadow
COLOR_TRAIN = '#E63939'   # CCC Classic Crimson / Red (Training set)
COLOR_TEST = '#2F6AB9'    # CCC Classic Sapphire Blue (Test set)
SHADOW_YELLOW = '#FEC211' # CCC Signature Bright Yellow (#FEC211)


def generate_synthetic_parity_data(n_train=480, n_test=120):
    """Generates synthetic parity predictions for demonstration."""
    np.random.seed(42)
    y_tr = np.concatenate([np.random.normal(25, 10, int(n_train * 0.4)),
                           np.random.normal(65, 20, int(n_train * 0.6))])
    y_tr = np.clip(y_tr, 2, 145)

    y_te = np.concatenate([np.random.normal(25, 10, int(n_test * 0.4)),
                           np.random.normal(65, 20, int(n_test * 0.6))])
    y_te = np.clip(y_te, 2, 145)

    p_tr = y_tr + np.random.normal(0, 1.2 + 0.02 * y_tr)
    p_te = y_te + np.random.normal(0, 2.5 + 0.04 * y_te)
    return y_tr, p_tr, y_te, p_te

def apply_shadow_to_legend(leg, offset=(2.8, -2.8), color=SHADOW_YELLOW):
    """Applies a crisp golden-yellow 3D drop shadow to the legend box."""
    frame = leg.get_frame()
    frame.set_facecolor('#ffffff')
    frame.set_edgecolor('#222222')
    frame.set_linewidth(1.05)
    frame.set_alpha(1.0)
    frame.set_path_effects([
        pe.SimplePatchShadow(offset=offset, shadow_rgbFace=color, alpha=1.0),
        pe.Normal()
    ])

def plot_single_joint_parity(y_tr, p_tr, y_te, p_te,
                             xlabel="Experimental CS (MPa)", ylabel="Predicted CS (MPa)",
                             caption="(c) XGBoost", lims=(0, 160),
                             output_prefix="parity_with_marginals_standard"):
    fig = plt.figure(figsize=(5.4, 5.4), dpi=300)
    gs = fig.add_gridspec(2, 2, width_ratios=(4.5, 1.0), height_ratios=(1.0, 4.5),
                          left=0.15, right=0.92, bottom=0.14, top=0.92,
                          wspace=0.04, hspace=0.04)

    ax_main = fig.add_subplot(gs[1, 0])
    ax_top = fig.add_subplot(gs[0, 0], sharex=ax_main)
    ax_right = fig.add_subplot(gs[1, 1], sharey=ax_main)

    # 1. Central Parity Plot
    rel_err_te = np.abs(y_te - p_te) / np.maximum(y_te, 1e-3)
    pct_in_15 = np.mean(rel_err_te <= 0.15) * 100

    ax_main.plot(lims, lims, 'k-', lw=1.2, label=r'$y=x$', zorder=2)
    ax_main.plot(lims, [l * 1.15 for l in lims], 'k--', lw=0.9, zorder=2,
                 label=rf'$\pm 15\%$ line ({pct_in_15:.1f}% points included)')
    ax_main.plot(lims, [l * 0.85 for l in lims], 'k--', lw=0.9, zorder=2)

    ax_main.scatter(y_tr, p_tr, facecolors='none', edgecolors=COLOR_TRAIN, s=26,
                    linewidths=0.95, alpha=0.85, zorder=3, label=f'Training set ($N={len(y_tr)}$)')
    ax_main.scatter(y_te, p_te, facecolors='none', edgecolors=COLOR_TEST, s=28, marker='s',
                    linewidths=1.05, alpha=0.90, zorder=4, label=f'Test set ($N={len(y_te)}$)')

    ax_main.set_xlim(lims)
    ax_main.set_ylim(lims)
    ax_main.set_xlabel(xlabel, fontsize=9.8, fontname='Times New Roman')
    ax_main.set_ylabel(ylabel, fontsize=9.8, fontname='Times New Roman')

    ax_main.tick_params(top=False, right=False, direction='in', length=3.0, width=0.85)
    ax_main.xaxis.set_minor_locator(AutoMinorLocator(2))
    ax_main.yaxis.set_minor_locator(AutoMinorLocator(2))
    ax_main.tick_params(which='minor', length=0, bottom=False, left=False, top=False, right=False)
    ax_main.grid(False, which='major')
    ax_main.grid(True, which='minor', linestyle=':', color='#E2E8F0', linewidth=0.6, alpha=0.9)

    # Legend with yellow shadow
    leg = ax_main.legend(loc='upper left', frameon=True, fontsize=7.6,
                         borderpad=0.45, labelspacing=0.35)
    apply_shadow_to_legend(leg, offset=(2.8, -2.8), color=SHADOW_YELLOW)

    ax_main.text(0.5, -0.22, caption, transform=ax_main.transAxes, ha='center', va='top',
                 fontsize=10.0, fontweight='bold', fontname='Times New Roman')

    # 2. Top Marginal Distribution (Ground Truth)
    sns.kdeplot(y_tr, ax=ax_top, color=COLOR_TRAIN, fill=True, alpha=0.18, lw=1.2, bw_adjust=0.85)
    sns.kdeplot(y_te, ax=ax_top, color=COLOR_TEST, fill=True, alpha=0.18, lw=1.2, bw_adjust=0.85)
    ax_top.tick_params(axis='x', which='both', bottom=False, labelbottom=False, top=False)
    ax_top.tick_params(axis='y', which='both', left=False, labelleft=False, right=False)
    for spine in ['top', 'right', 'left']:
        ax_top.spines[spine].set_visible(False)
    ax_top.spines['bottom'].set_color('#222222')
    ax_top.spines['bottom'].set_linewidth(0.85)
    ax_top.set_ylabel('')
    ax_top.set_xlabel('')

    # 3. Right Marginal Distribution (Predicted)
    sns.kdeplot(y=p_tr, ax=ax_right, color=COLOR_TRAIN, fill=True, alpha=0.18, lw=1.2, bw_adjust=0.85)
    sns.kdeplot(y=p_te, ax=ax_right, color=COLOR_TEST, fill=True, alpha=0.18, lw=1.2, bw_adjust=0.85)
    ax_right.tick_params(axis='y', which='both', left=False, labelleft=False, right=False)
    ax_right.tick_params(axis='x', which='both', bottom=False, labelbottom=False, top=False)
    for spine in ['top', 'right', 'bottom']:
        ax_right.spines[spine].set_visible(False)
    ax_right.spines['left'].set_color('#222222')
    ax_right.spines['left'].set_linewidth(0.85)
    ax_right.set_xlabel('')
    ax_right.set_ylabel('')

    out_png = f"{output_prefix}.png"
    out_pdf = f"{output_prefix}.pdf"
    fig.savefig(out_png, dpi=300, bbox_inches='tight')
    fig.savefig(out_pdf, bbox_inches='tight')
    plt.close(fig)
    print(f"[SUCCESS] Exported Joint Parity Plot with Marginals: {out_png} and {out_pdf}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate Joint Parity Plot with Top and Right Marginal Distributions")
    parser.add_argument('--output', type=str, default="parity_with_marginals_standard", help="Output file prefix")
    args = parser.parse_args()

    y_tr, p_tr, y_te, p_te = generate_synthetic_parity_data()
    plot_single_joint_parity(y_tr, p_tr, y_te, p_te, output_prefix=args.output)

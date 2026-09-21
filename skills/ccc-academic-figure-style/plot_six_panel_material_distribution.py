# -*- coding: utf-8 -*-
"""
6-Panel Composite Material and Property Distribution Plot
Conforming strictly to CCC (Elsevier) journal standards & Nature/Elsevier guidelines:
- Panel (a): Primary Mix Proportions (W/B and S/B, Violin + Boxplot + Jittered Scatter)
- Panel (b): Binder Composition (Portland cement fraction wt%, KDE + Soft Blue Fill + Rug ticks)
- Panel (c): Chemical Admixtures (PCE, Defoamer, VMA, Jittered Scatter + Red Diamond Mean +- SD)
- Panel (d): Geopolymer Precursors & SCMs (Fly ash, Slag, Silica fume overlapping histograms)
- Panel (e): Compressive Strength Evolution (1d, 3d, 7d, 28d Multi-age Violin + Boxplot + Jittered Scatter)
- Panel (f): Fresh-State Fluidity Distribution (Histogram + KDE curve + Median & Target lines)

Strict Times New Roman typography, inward ticks, boxed spines, no top/right ticks.
"""

import argparse
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

# Configure strict Times New Roman & CCC academic standards
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif', 'serif']
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['font.size'] = 9.0
plt.rcParams['axes.labelsize'] = 9.0
plt.rcParams['xtick.labelsize'] = 8.5
plt.rcParams['ytick.labelsize'] = 8.5
plt.rcParams['axes.edgecolor'] = '#222222'
plt.rcParams['axes.linewidth'] = 0.85
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['xtick.top'] = False
plt.rcParams['ytick.right'] = False

# CCC Palette
COLOR_BLUE_DARK = '#2F6AB9'
COLOR_BLUE_MED = '#69AADB'
COLOR_BLUE_LIGHT = '#97C6E6'
COLOR_RED = '#F14040'
COLOR_YELLOW = '#FEC211'

def generate_synthetic_data():
    """Generates synthetic material dataset for standalone demonstration."""
    np.random.seed(42)
    n = 300
    wb = np.clip(np.random.normal(0.28, 0.08, n), 0.15, 0.75)
    sb = np.clip(np.random.normal(0.85, 0.25, n), 0.30, 1.80)
    cement = np.clip(np.random.beta(5, 2, n) * 100, 30, 100)
    fa = np.clip(np.random.exponential(15, n), 0, 60)
    slag = np.clip(np.random.exponential(12, n), 0, 50)
    sf = np.clip(np.random.exponential(5, n), 0, 25)
    pce = np.clip(np.random.normal(0.45, 0.20, n), 0.05, 1.8)
    defamer = np.clip(np.random.normal(0.08, 0.03, n), 0.01, 0.25)
    vma = np.clip(np.random.normal(0.05, 0.02, n), 0.01, 0.15)
    flow = np.clip(np.random.normal(305, 35, n), 180, 380)

    # Multi-age strengths
    s1 = np.clip(np.random.normal(32, 8, n), 10, 65)
    s3 = np.clip(s1 * 1.35 + np.random.normal(0, 4, n), 20, 85)
    s7 = np.clip(s3 * 1.25 + np.random.normal(0, 5, n), 30, 110)
    s28 = np.clip(s7 * 1.20 + np.random.normal(0, 6, n), 40, 140)

    return {
        'wb': wb, 'sb': sb, 'cement': cement,
        'fa': fa[fa > 0], 'slag': slag[slag > 0], 'sf': sf[sf > 0],
        'pce': pce, 'defamer': defamer, 'vma': vma,
        's1': s1, 's3': s3, 's7': s7, 's28': s28,
        'flow': flow
    }

def plot_six_panel_distribution(data, output_prefix="distribution_6panel_standard"):
    fig, axs = plt.subplots(2, 3, figsize=(11.8, 7.6), dpi=300)

    # (a) Primary Mix Proportions (W/B, S/B)
    ax = axs[0, 0]
    wb, sb = data['wb'], data['sb']
    parts = ax.violinplot([wb, sb], positions=[1, 2], widths=0.48, showmeans=False, showmedians=False, showextrema=False)
    for pc in parts['bodies']:
        pc.set_facecolor(COLOR_BLUE_MED)
        pc.set_alpha(0.45)
        pc.set_edgecolor(COLOR_BLUE_DARK)
        pc.set_linewidth(1.2)

    ax.boxplot([wb, sb], positions=[1, 2], widths=0.18, patch_artist=True,
               boxprops=dict(facecolor='white', edgecolor='#222222', lw=1.1),
               medianprops=dict(color=COLOR_RED, lw=1.6),
               whiskerprops=dict(color='#222222', lw=1.0),
               capprops=dict(color='#222222', lw=1.0), showfliers=False)

    np.random.seed(42)
    ax.scatter(np.random.normal(1 - 0.20, 0.035, len(wb)), wb, s=12, color=COLOR_BLUE_DARK, alpha=0.45, edgecolors='none')
    ax.scatter(np.random.normal(2 - 0.20, 0.035, len(sb)), sb, s=12, color=COLOR_BLUE_DARK, alpha=0.45, edgecolors='none')
    ax.set_xticks([1, 2])
    ax.set_xticklabels(['$W/B$', '$S/B$'], fontsize=9.5)
    ax.set_ylabel('Mass ratio (--)')
    ax.tick_params(direction='in', top=False, right=False)
    ax.grid(axis='y', alpha=0.25, linestyle=':')
    ax.set_title('(a) Primary Mix Proportions', loc='left', fontsize=9.5, fontweight='bold')

    # (b) Binder Composition
    ax = axs[0, 1]
    c_frac = data['cement']
    sns.kdeplot(c_frac, ax=ax, color=COLOR_BLUE_DARK, lw=2.2, fill=True, alpha=0.25, bw_adjust=0.85)
    rug_y = ax.get_ylim()[1] * 0.03
    ax.scatter(c_frac, np.zeros_like(c_frac) + rug_y * 0.15, color=COLOR_RED, s=16, alpha=0.55, marker='|', lw=1.1)
    ax.set_xlabel('Portland cement fraction (wt%)')
    ax.set_ylabel('Probability density')
    ax.tick_params(direction='in', top=False, right=False)
    ax.grid(axis='y', alpha=0.25, linestyle=':')
    ax.set_title('(b) Binder Composition', loc='left', fontsize=9.5, fontweight='bold')

    # (c) Chemical Admixtures
    ax = axs[0, 2]
    admix_data = [data['pce'], data['defamer'], data['vma']]
    admix_labels = ['PCE', 'Defoamer', 'VMA']
    pos = [1, 2, 3]
    cols = [COLOR_BLUE_DARK, COLOR_BLUE_MED, COLOR_BLUE_LIGHT]
    for p, d, c in zip(pos, admix_data, cols):
        jitter = np.random.normal(0, 0.045, len(d))
        ax.scatter(p + jitter, d, s=18, color=c, alpha=0.55, edgecolors='#222222', lw=0.4, zorder=2)
        m_val, s_val = np.mean(d), np.std(d)
        ax.errorbar(p, m_val, yerr=s_val, fmt='D', color=COLOR_RED, markersize=5.5,
                    capsize=4, capthick=1.2, elinewidth=1.6, zorder=4,
                    label='Mean $\\pm$ SD' if p == 1 else "")
    ax.set_xticks(pos)
    ax.set_xticklabels(admix_labels, fontsize=9.5)
    ax.set_ylabel('Dosage (wt% of binder)')
    ax.tick_params(direction='in', top=False, right=False)
    ax.legend(frameon=True, edgecolor='#cccccc', fontsize=8.0, loc='upper right')
    ax.grid(axis='y', alpha=0.25, linestyle=':')
    ax.set_title('(c) Chemical Admixtures', loc='left', fontsize=9.5, fontweight='bold')

    # (d) Precursors & SCMs
    ax = axs[1, 0]
    bins = np.linspace(0, 80, 17)
    ax.hist(data['fa'], bins=bins, label='Fly ash (FA)', facecolor=COLOR_BLUE_DARK, edgecolor='#1C3F73', lw=1.0, alpha=0.65)
    ax.hist(data['slag'], bins=bins, label='Slag (GGBS)', facecolor=COLOR_RED, edgecolor='#A82020', lw=1.0, alpha=0.60)
    ax.hist(data['sf'], bins=bins, label='Silica fume (SF)', facecolor=COLOR_YELLOW, edgecolor='#B58900', lw=1.0, alpha=0.75)
    ax.set_xlabel('Precursor / SCM fraction (wt%)')
    ax.set_ylabel('Mixture count')
    ax.tick_params(direction='in', top=False, right=False)
    ax.legend(frameon=True, edgecolor='#cccccc', fontsize=8.0, loc='upper right')
    ax.grid(axis='y', alpha=0.25, linestyle=':')
    ax.set_title('(d) Geopolymer Precursors & SCMs', loc='left', fontsize=9.5, fontweight='bold')

    # (e) Compressive Strength Evolution
    ax = axs[1, 1]
    strengths = [data['s1'], data['s3'], data['s7'], data['s28']]
    age_labels = ['1 day', '3 days', '7 days', '28 days']
    pos_e = [1, 2, 3, 4]
    cols_e = ['#97C6E6', '#69AADB', '#2F6AB9', '#1C3F73']
    parts = ax.violinplot(strengths, positions=pos_e, widths=0.55, showmeans=False, showmedians=False, showextrema=False)
    for pc, col in zip(parts['bodies'], cols_e):
        pc.set_facecolor(col)
        pc.set_alpha(0.50)
        pc.set_edgecolor('#222222')
        pc.set_linewidth(1.0)
    ax.boxplot(strengths, positions=pos_e, widths=0.20, patch_artist=True,
               boxprops=dict(facecolor='white', edgecolor='#222222', lw=1.1),
               medianprops=dict(color=COLOR_RED, lw=1.6),
               whiskerprops=dict(color='#222222', lw=1.0),
               capprops=dict(color='#222222', lw=1.0), showfliers=False)
    for p, s, c in zip(pos_e, strengths, cols_e):
        jitter = np.random.normal(p - 0.20, 0.035, len(s))
        ax.scatter(jitter, s, s=10, color=c, alpha=0.50, edgecolors='none')
    ax.set_xticks(pos_e)
    ax.set_xticklabels(age_labels, fontsize=9.0)
    ax.set_ylabel('Compressive strength (MPa)')
    ax.tick_params(direction='in', top=False, right=False)
    ax.grid(axis='y', alpha=0.25, linestyle=':')
    ax.set_title('(e) Compressive Strength Evolution', loc='left', fontsize=9.5, fontweight='bold')

    # (f) Fresh Fluidity Distribution
    ax = axs[1, 2]
    flow = data['flow']
    ax.hist(flow, bins=14, facecolor=COLOR_BLUE_MED, edgecolor=COLOR_BLUE_DARK, lw=1.1, alpha=0.60, density=True)
    sns.kdeplot(flow, ax=ax, color=COLOR_BLUE_DARK, lw=2.0)
    median_flow = float(np.median(flow))
    ax.axvline(median_flow, color=COLOR_RED, lw=1.6, linestyle='--', label=f'Median: {median_flow:.0f} mm')
    ax.axvline(300, color=COLOR_YELLOW, lw=1.8, linestyle=':', label='Design target: 300 mm')
    ax.set_xlabel('Initial fluidity spread $F_0$ (mm)')
    ax.set_ylabel('Probability density')
    ax.tick_params(direction='in', top=False, right=False)
    ax.legend(frameon=True, edgecolor='#cccccc', fontsize=8.0, loc='upper left')
    ax.grid(axis='y', alpha=0.25, linestyle=':')
    ax.set_title('(f) Fresh-State Fluidity Distribution', loc='left', fontsize=9.5, fontweight='bold')

    plt.tight_layout()
    plt.subplots_adjust(hspace=0.28, wspace=0.26)

    out_png = f"{output_prefix}.png"
    out_pdf = f"{output_prefix}.pdf"
    fig.savefig(out_png, dpi=300, bbox_inches='tight')
    fig.savefig(out_pdf, bbox_inches='tight')
    plt.close(fig)
    print(f"[SUCCESS] Exported 6-panel distribution figures: {out_png} and {out_pdf}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate CCC Standard 6-Panel Composite Material Distribution Plot")
    parser.add_argument('--output', type=str, default="distribution_6panel_standard", help="Output file prefix")
    args = parser.parse_args()

    data = generate_synthetic_data()
    plot_six_panel_distribution(data, output_prefix=args.output)

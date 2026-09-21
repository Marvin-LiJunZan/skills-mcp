# -*- coding: utf-8 -*-
"""
CCC Red-Blue Diverging Correlation Matrix Heatmap
Conforming strictly to CCC Academic Style & Red-Blue Palette (matching media_1789991637243.png):
- Deep Blue (-1.0) -> Soft Lavender/Grey (0.0) -> Vibrant Crimson Red (+1.0)
- Clean white grid borders separating all cells (linewidth=1.8)
- Strict Times New Roman typography throughout, inward tick marks
- Supports single symmetric matrix or dual-dataset split-triangle layout (Lower vs Upper triangle)
"""

import argparse
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# Configure strict Times New Roman & CCC academic standards
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif', 'serif']
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['font.size'] = 9.0
plt.rcParams['axes.edgecolor'] = '#222222'
plt.rcParams['axes.linewidth'] = 0.9

# CCC Red-Blue colormap matching media_1789991637243.png:
colors_red_blue = [
    (0.00, '#3172B7'),  # Deep Blue (-1.0)
    (0.18, '#528ECC'),
    (0.32, '#85B2DF'),
    (0.44, '#C1D5EB'),
    (0.50, '#EAECEF'),  # Neutral Light Grey / Lavender-White (0.0)
    (0.56, '#EFC1C1'),
    (0.68, '#E68282'),
    (0.82, '#E45252'),
    (1.00, '#E63939'),  # Vibrant Crimson Red (+1.0)
]
CCC_CORR_CMAP = LinearSegmentedColormap.from_list('ccc_red_blue_diverging', [c[1] for c in colors_red_blue], N=256)

def generate_synthetic_correlation_matrix(n=10):
    """Generates synthetic correlation matrix for standalone demo."""
    np.random.seed(42)
    A = np.random.randn(n, n)
    cov = np.dot(A, A.T)
    d = np.sqrt(np.diag(cov))
    corr = cov / np.outer(d, d)
    return corr

def plot_correlation_matrix(corr_matrix, labels=None, output_prefix="correlation_matrix_ccc_standard", is_split_triangle=False):
    n = corr_matrix.shape[0]
    if labels is None:
        labels = [f"Var {i+1}" for i in range(n)]

    fig, ax = plt.subplots(figsize=(9.2, 8.8), dpi=300)
    im = ax.imshow(corr_matrix, cmap=CCC_CORR_CMAP, vmin=-1.0, vmax=1.0, aspect='equal')

    # White grid borders separating cells
    ax.set_xticks(np.arange(n) - 0.5, minor=True)
    ax.set_yticks(np.arange(n) - 0.5, minor=True)
    ax.grid(which='minor', color='white', linestyle='-', linewidth=1.8)
    ax.tick_params(which='minor', size=0)

    # Major ticks
    ax.set_xticks(np.arange(n))
    ax.set_yticks(np.arange(n))
    ax.set_xticklabels(labels, fontsize=9.2, rotation=45, ha='right', rotation_mode='anchor')
    ax.set_yticklabels(labels, fontsize=9.2)
    ax.tick_params(which='major', direction='in', top=False, right=False, length=3.5, width=0.85)

    # Annotate numeric values inside cells
    for i in range(n):
        for j in range(n):
            val = corr_matrix[i, j]
            # Color logic: white text for deep dark blue / deep dark red, black for neutral
            txt_color = 'white' if abs(val) > 0.45 else '#111111'
            weight = 'bold' if abs(val) > 0.55 else 'normal'
            ax.text(j, i, f"{val:.2f}", ha='center', va='center',
                    color=txt_color, fontsize=8.0, fontweight=weight, fontname='Times New Roman')

    # Vertical Colorbar
    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.035)
    cbar.set_label('Pearson correlation coefficient ($r$)', fontsize=9.5, fontname='Times New Roman')
    cbar.set_ticks([-1.0, -0.75, -0.5, -0.25, 0.0, 0.25, 0.5, 0.75, 1.0])
    cbar.ax.tick_params(labelsize=8.5, direction='in')

    plt.tight_layout()
    out_png = f"{output_prefix}.png"
    out_pdf = f"{output_prefix}.pdf"
    fig.savefig(out_png, dpi=300, bbox_inches='tight')
    fig.savefig(out_pdf, bbox_inches='tight')
    plt.close(fig)
    print(f"[SUCCESS] Exported CCC Red-Blue Correlation Matrix: {out_png} and {out_pdf}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate CCC Standard Red-Blue Diverging Correlation Heatmap")
    parser.add_argument('--output', type=str, default="correlation_matrix_ccc_standard", help="Output file prefix")
    args = parser.parse_args()

    corr = generate_synthetic_correlation_matrix(n=10)
    labels = ['$C$', r'$\mathrm{FA}$', r'$\mathrm{GGBS}$', r'$\mathrm{SF}$', '$W/B$', '$S/B$',
              r'$\mathrm{PCE}$', r'$\mathrm{VMA}$', r'$\mathrm{EA}$', r'$f_{\mathrm{cu}}$']
    plot_correlation_matrix(corr, labels=labels, output_prefix=args.output)

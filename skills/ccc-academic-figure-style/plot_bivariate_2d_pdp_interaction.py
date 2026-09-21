# -*- coding: utf-8 -*-
"""
Bivariate 2D Partial Dependence Plots (PDP) Interaction Surfaces
Conforming strictly to CCC (Elsevier) journal standards & user reference (media_1789991692513.png):
- CCC Red-Blue diverging colormap: Deep Blue (Low) -> Lavender-White (Neutral) -> Vibrant Crimson Red (High)
- Clear white contour lines with inline level annotations (clabel)
- Strict Times New Roman font throughout, inward tick marks, no top/right ticks
- Individual flush colorbars on the right of each subplot
- Multi-panel grid (e.g., 2x4 for dual target properties or custom 1x2, 2x2 layouts)
"""

import argparse
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from mpl_toolkits.axes_grid1 import make_axes_locatable

# CCC Universal Styling & Typography
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif', 'serif']
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['axes.edgecolor'] = '#222222'
plt.rcParams['axes.linewidth'] = 0.85
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['xtick.top'] = False
plt.rcParams['ytick.right'] = False

# CCC Red-Blue colormap matching media_1789991692513.png:
colors_red_blue = [
    (0.00, '#2F6AB9'),  # Deep Blue (Minimum response)
    (0.20, '#5894D3'),
    (0.35, '#8CBBE8'),
    (0.45, '#C6D9EE'),
    (0.50, '#EAECEF'),  # Neutral Light Lavender-White
    (0.55, '#F1C7C7'),
    (0.65, '#E88B8B'),
    (0.80, '#E65656'),
    (1.00, '#E63939'),  # Vibrant Crimson Red (Maximum response)
]
CCC_DIVERGING_CMAP = mcolors.LinearSegmentedColormap.from_list(
    "ccc_red_blue_diverging", [c[1] for c in colors_red_blue], N=256
)

def create_synthetic_surfaces():
    """Generates synthetic 2D nonlinear response surfaces for 2x4 demo."""
    x = np.linspace(0.2, 0.8, 50)
    y = np.linspace(0.4, 1.6, 50)
    X, Y = np.meshgrid(x, y)

    # 4 surfaces for target 1 (e.g. Strength)
    Z1_a = 45 - 35 * X + 15 * np.log10(1 + 28 * Y)
    Z1_b = 65 - 40 * np.maximum(0, X - 0.2)**1.2 - 15 * np.maximum(0, Y - 0.4)**1.1
    Z1_c = 40 + 25 * np.sin(X * np.pi) * np.cos(Y * 1.5)
    Z1_d = 30 + 30 * np.exp(-((X - 0.4)**2 + (Y - 0.9)**2) / 0.15)

    # 4 surfaces for target 2 (e.g. Fluidity)
    Z2_a = 280 + 90 * X - 70 * Y + 30 * X * Y
    Z2_b = 310 - 60 * (Y - 0.4)**2 + 45 * X
    Z2_c = 260 + 120 * (1 / (1 + np.exp(-6 * (X - 0.5)))) - 40 * Y
    Z2_d = 295 - 50 * np.sqrt(np.abs(X - Y)) + 20 * np.sin(X * 4)

    panels = [
        # Target 1: Hardened Strength
        {'title': '(a) Age $\\times$ $W/B$', 'xlabel': 'Curing age $t$ (d)', 'ylabel': 'Water-to-binder ratio ($W/B$)',
         'x_range': (1, 28), 'y_range': (0.2, 0.6), 'Z': Z1_a, 'cbar_label': '$f_{\\mathrm{cu}}$ (MPa)', 'fmt': '%.0f'},
        {'title': '(b) $W/B \\times S/B$', 'xlabel': 'Water-to-binder ratio ($W/B$)', 'ylabel': 'Sand-to-binder ratio ($S/B$)',
         'x_range': (0.2, 0.6), 'y_range': (0.4, 1.6), 'Z': Z1_b, 'cbar_label': '$f_{\\mathrm{cu}}$ (MPa)', 'fmt': '%.0f'},
        {'title': '(c) Defoamer $\\times$ PCE', 'xlabel': 'Defoamer dosage (wt%)', 'ylabel': 'PCE dosage (wt%)',
         'x_range': (0.02, 0.20), 'y_range': (0.2, 1.4), 'Z': Z1_c, 'cbar_label': '$f_{\\mathrm{cu}}$ (MPa)', 'fmt': '%.0f'},
        {'title': '(d) SF $\\times$ $W/B$', 'xlabel': 'Silica fume dosage (wt%)', 'ylabel': 'Water-to-binder ratio ($W/B$)',
         'x_range': (0, 20), 'y_range': (0.2, 0.6), 'Z': Z1_d, 'cbar_label': '$f_{\\mathrm{cu}}$ (MPa)', 'fmt': '%.0f'},
        # Target 2: Fresh Fluidity
        {'title': '(e) $W/B \\times S/B$', 'xlabel': 'Water-to-binder ratio ($W/B$)', 'ylabel': 'Sand-to-binder ratio ($S/B$)',
         'x_range': (0.2, 0.5), 'y_range': (0.6, 1.5), 'Z': Z2_a, 'cbar_label': '$\\mathrm{Flow}$ (mm)', 'fmt': '%.0f'},
        {'title': '(f) $S/B \\times \\mathrm{PCE}$', 'xlabel': 'Sand-to-binder ratio ($S/B$)', 'ylabel': 'PCE dosage (wt%)',
         'x_range': (0.6, 1.5), 'y_range': (0.2, 1.4), 'Z': Z2_b, 'cbar_label': '$\\mathrm{Flow}$ (mm)', 'fmt': '%.0f'},
        {'title': '(g) $W/B \\times \\mathrm{PCE}$', 'xlabel': 'Water-to-binder ratio ($W/B$)', 'ylabel': 'PCE dosage (wt%)',
         'x_range': (0.2, 0.5), 'y_range': (0.2, 1.4), 'Z': Z2_c, 'cbar_label': '$\\mathrm{Flow}$ (mm)', 'fmt': '%.0f'},
        {'title': '(h) $\\mathrm{PCE} \\times \\mathrm{Defoamer}$', 'xlabel': 'PCE dosage (wt%)', 'ylabel': 'Defoamer dosage (wt%)',
         'x_range': (0.2, 1.4), 'y_range': (0.02, 0.20), 'Z': Z2_d, 'cbar_label': '$\\mathrm{Flow}$ (mm)', 'fmt': '%.0f'},
    ]
    return panels

def plot_bivariate_pdp_grid(panels, nrows=2, ncols=4, figsize=(16.5, 7.6), output_prefix="pdp_2d_bivariate_standard"):
    fig, axes = plt.subplots(nrows, ncols, figsize=figsize, dpi=300)
    axes_flat = axes.flatten()

    for idx, p in enumerate(panels):
        ax = axes_flat[idx]
        x_min, x_max = p['x_range']
        y_min, y_max = p['y_range']
        Z = p['Z']

        xx = np.linspace(x_min, x_max, Z.shape[1])
        yy = np.linspace(y_min, y_max, Z.shape[0])
        XX, YY = np.meshgrid(xx, yy)

        # Filled contour
        cf = ax.contourf(XX, YY, Z, levels=22, cmap=CCC_DIVERGING_CMAP)

        # Clean white contour lines with labels
        cs = ax.contour(XX, YY, Z, levels=9, colors='white', linewidths=0.85, alpha=0.90)
        ax.clabel(cs, inline=True, fontsize=7.0, fmt=p.get('fmt', '%.0f'), colors='white')

        ax.set_title(p['title'], loc='left', fontsize=9.5, fontweight='bold')
        ax.set_xlabel(p['xlabel'], fontsize=8.8)
        ax.set_ylabel(p['ylabel'], fontsize=8.8)
        ax.tick_params(labelsize=8.2, direction='in', top=False, right=False)

        # Right flush colorbar
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5.5%", pad=0.08)
        cb = fig.colorbar(cf, cax=cax)
        cb.set_label(p['cbar_label'], fontsize=8.5, fontname='Times New Roman')
        cb.ax.tick_params(labelsize=7.8, direction='in')

    plt.tight_layout()
    plt.subplots_adjust(hspace=0.28, wspace=0.38)

    out_png = f"{output_prefix}.png"
    out_pdf = f"{output_prefix}.pdf"
    fig.savefig(out_png, dpi=300, bbox_inches='tight')
    fig.savefig(out_pdf, bbox_inches='tight')
    plt.close(fig)
    print(f"[SUCCESS] Exported Bivariate 2D PDP figures: {out_png} and {out_pdf}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate CCC Standard Bivariate 2D PDP Interaction Surfaces")
    parser.add_argument('--output', type=str, default="pdp_2d_bivariate_standard", help="Output file prefix")
    args = parser.parse_args()

    panels = create_synthetic_surfaces()
    plot_bivariate_pdp_grid(panels, nrows=2, ncols=4, output_prefix=args.output)

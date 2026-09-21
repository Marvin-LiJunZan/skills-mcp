# -*- coding: utf-8 -*-
"""
CCC & Nature-grade Plotting Template:
Multi-Variable Feature Distribution Horizontal Stacked Bar Chart (多变量区间分布堆叠柱状图)
================================================================================
Design Features (strictly matching Nature/Elsevier reference):
- Displays multi-dimensional feature distributions as aligned horizontal segmented bars.
- Each bar represents a distinct input parameter, partitioned into discrete physical intervals.
- The width of each segment represents the specimen count in that specific interval.
- Threshold cutoff numbers are printed directly above each partition boundary.
- Sub-sample counts are printed centered inside each colored box.
- Left y-axis displays the parameter name (with units) and a subordinate 'Counts' indicator.
- Bottom x-axis displays the total specimen scale ('Number of specimens').
- Academic pastel palette: Peach, Sage green, Lavender, Butter yellow, Sky blue, Soft rose.
- STRICT RULE: Inward ticks on Bottom axis only; Absolutely NO top ticks and NO right ticks.

Author: Antigravity CCC Skills Suite
"""

import os
import argparse
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

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

# Standard academic soft pastel color palette (cyclical)
PASTEL_COLORS = [
    '#fbc4ab',  # Soft peach / apricot
    '#b7e4c7',  # Soft sage green
    '#d8b4e2',  # Lavender / muted purple
    '#fff1b8',  # Soft butter yellow
    '#bde0fe',  # Pastel sky blue
    '#ffcad4',  # Soft rose / muted pink
    '#c8d6e5',  # Pastel slate
    '#ffdfba',  # Muted melon
]


def auto_discretize_feature(series, n_bins=5, custom_cutoffs=None):
    """
    Discretize a numeric series into bins with formatted thresholds and counts.
    """
    clean = pd.to_numeric(series, errors='coerce').dropna().values
    if len(clean) == 0:
        return [0], [0.0, 1.0]

    if custom_cutoffs is not None:
        cutoffs = sorted(list(set(custom_cutoffs)))
        # Ensure min and max wrap the data
        if cutoffs[0] > clean.min():
            cutoffs.insert(0, float(np.round(clean.min(), 2)))
        if cutoffs[-1] < clean.max():
            cutoffs.append(float(np.round(clean.max(), 2)))
    else:
        # Quantile or pretty linspace bins
        q = np.linspace(0, 100, n_bins + 1)
        cutoffs = np.percentile(clean, q)
        cutoffs = np.unique(np.round(cutoffs, 2))
        if len(cutoffs) < 3:
            cutoffs = np.linspace(clean.min(), clean.max(), n_bins + 1)
            cutoffs = np.round(cutoffs, 2)

    counts = []
    for i in range(len(cutoffs) - 1):
        lo, hi = cutoffs[i], cutoffs[i + 1]
        if i == len(cutoffs) - 2:
            c = np.sum((clean >= lo) & (clean <= hi))
        else:
            c = np.sum((clean >= lo) & (clean < hi))
        counts.append(int(c))

    return counts, list(cutoffs)


def plot_feature_distribution_bars(feature_data_dict, total_samples=None,
                                   title="Distribution of input parameters.",
                                   output_prefix="feature_distribution_bars_standard",
                                   figsize=None, dpi=300):
    """
    Plots horizontal segmented bars for multi-variable distributions.

    Parameters
    ----------
    feature_data_dict : dict
        Keys: Feature display labels, e.g., 'd (mm)', 'h (mm)', 'W/B'.
        Values: Either:
            1. A 1D numeric array/Series (auto-binned).
            2. A tuple: (counts_list, cutoffs_list), e.g., ([26, 9, 69, 77, 21, 26], [50, 100, 150, 200, 250, 300, 350]).
    total_samples : int, optional
        Scale for total specimens. Defaults to sum of counts or max length.
    """
    n_features = len(feature_data_dict)
    if figsize is None:
        figsize = (10.0, max(6.0, 0.65 * n_features + 2.0))

    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)

    # Calculate total samples if not provided
    processed_data = []
    max_counts_sum = 0
    for feat_name, val in feature_data_dict.items():
        if isinstance(val, (tuple, list)) and len(val) == 2 and isinstance(val[0], list):
            counts, cutoffs = val
        else:
            counts, cutoffs = auto_discretize_feature(val)
        processed_data.append((feat_name, counts, cutoffs))
        max_counts_sum = max(max_counts_sum, sum(counts))

    if total_samples is None:
        total_samples = max_counts_sum

    bar_height = 0.52
    y_positions = np.arange(n_features)[::-1]  # Top to bottom

    # Subtle horizontal dotted guidelines
    for y in y_positions:
        ax.axhline(y, color='#e0e0e0', linestyle=':', linewidth=0.75, zorder=1)

    for idx, (feat_name, counts, cutoffs) in enumerate(processed_data):
        y = y_positions[idx]
        current_x = 0

        # Draw segmented rectangles
        for b_idx, count in enumerate(counts):
            if count <= 0:
                continue
            color = PASTEL_COLORS[b_idx % len(PASTEL_COLORS)]
            rect = Rectangle((current_x, y - bar_height / 2), count, bar_height,
                             facecolor=color, edgecolor='#333333', linewidth=0.85, zorder=3)
            ax.add_patch(rect)

            # Inside label: count
            center_x = current_x + count / 2.0
            ax.text(center_x, y, str(count), ha='center', va='center',
                    fontsize=9.5, color='#111111', zorder=4)

            # Cutoff number above boundary line
            cutoff_num = cutoffs[b_idx]
            num_str = f"{cutoff_num:g}" if isinstance(cutoff_num, (int, float)) else str(cutoff_num)
            ax.text(current_x, y + bar_height / 2 + 0.08, num_str,
                    ha='center', va='bottom', fontsize=8.5, color='#222222', zorder=5)

            current_x += count

        # Last cutoff number above right edge
        if len(cutoffs) > 0:
            last_cutoff = cutoffs[-1]
            last_str = f"{last_cutoff:g}" if isinstance(last_cutoff, (int, float)) else str(last_cutoff)
            ax.text(current_x, y + bar_height / 2 + 0.08, last_str,
                    ha='center', va='bottom', fontsize=8.5, color='#222222', zorder=5)

    # Configure Y-axis labels with dual lines: Parameter on top, 'Counts' below
    ax.set_yticks(y_positions)
    # Use formatted plain labels with newlines
    y_tick_labels = [f"{item[0]}\nCounts" for item in processed_data]
    ax.set_yticklabels(y_tick_labels, fontsize=9.5)

    # Configure X-axis
    ax.set_xlim(-0.5, total_samples + 0.5)
    ax.set_ylim(-0.8, n_features - 0.2)
    ax.set_xlabel('Number of specimens', fontsize=11.0, labelpad=8)

    # Formatting: Hide top, right, and left spines to create the minimalist open look
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_linewidth(1.0)
    ax.spines['bottom'].set_color('#222222')

    # STRICT: Ticks only on bottom, inward
    ax.tick_params(axis='y', which='both', left=False, right=False)  # No y ticks
    ax.tick_params(axis='x', which='major', direction='in', length=5.0, width=0.9,
                   top=False, right=False, labelsize=9.5)
    ax.set_xticks([0, total_samples])
    ax.set_xticklabels(['0', str(total_samples)], fontsize=10.0)

    # Caption at bottom
    if title:
        plt.figtext(0.5, 0.012, title, ha='center', fontsize=11.0, fontweight='bold')

    plt.tight_layout(rect=[0.02, 0.04, 0.98, 0.98])

    out_png = f"{output_prefix}.png"
    out_pdf = f"{output_prefix}.pdf"
    fig.savefig(out_png, dpi=dpi, bbox_inches='tight')
    fig.savefig(out_pdf, bbox_inches='tight')
    plt.close(fig)
    print(f"[Feature Distribution Bars] Figure saved to:\n  {os.path.abspath(out_png)}\n  {os.path.abspath(out_pdf)}")
    return out_png, out_pdf


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate multi-variable feature distribution horizontal stacked bar chart.")
    parser.add_argument('--output', type=str, default='feature_distribution_bars_standard', help='Output prefix')
    args = parser.parse_args()

    print("Generating demo Multi-Variable Feature Distribution Bar chart matching reference...")
    demo_data = {
        r"d\text{ (mm)}": ([26, 9, 69, 77, 21, 26], [50, 100, 150, 200, 250, 300, 350]),
        r"h\text{ (mm)}": ([31, 69, 4, 28, 41, 55], [100, 250, 400, 550, 700, 850, 1050]),
        r"t\text{ (mm)}": ([104, 70, 28, 2, 12, 12], [0, 6, 12, 18, 24, 30, 40]),
        r"\lambda_{\mathrm{f}}": ([63, 41, 110, 10, 4], [0, 0.5, 1, 1.5, 2, 2.6]),
        r"E_{\mathrm{c}}\text{ (GPa)}": ([87, 87, 33, 21], [39.5, 45, 50, 55, 59.3]),
        r"f_{\mathrm{co}}\text{ (MPa)}": ([36, 47, 50, 50, 25, 20], [71.7, 100, 125, 150, 175, 200, 227]),
        r"\varepsilon_{\mathrm{co}}\text{ (\%)}": ([35, 68, 55, 39, 12, 19], [0.18, 0.24, 0.3, 0.36, 0.42, 0.48, 0.57]),
        r"\rho_{\mathrm{l}}\text{ (\%)}": ([58, 85, 24, 10], [0.64, 2.0, 4.0, 6.0, 12.32]),
        r"f_{\mathrm{yl}}\text{ (MPa)}": ([41, 23, 35, 8, 70], [425.8, 480, 540, 600, 660, 850]),
        r"\rho_{\mathrm{h}}\text{ (\%)}": ([126, 61, 13, 10], [0.25, 2.5, 5, 7.5, 16.45]),
        r"f_{\mathrm{yh}}\text{ (MPa)}": ([103, 29, 43, 35], [360, 500, 650, 800, 1400]),
        r"k_{\mathrm{e}}": ([18, 6, 9, 32, 71, 92], [0, 0.15, 0.3, 0.45, 0.6, 0.75, 1.0]),
        r"I_{\mathrm{e}}": ([71, 95, 54, 8], [0, 0.05, 0.1, 0.15, 0.26]),
        r"f_{\mathrm{cc}}\text{ (MPa)}": ([13, 52, 65, 57, 32, 9], [62.3, 100, 135, 170, 205, 240, 284.6]),
        r"\varepsilon_{\mathrm{cc}}\text{ (\%)}": ([108, 95, 19, 6], [0.2, 0.45, 0.7, 0.95, 1.94])
    }

    plot_feature_distribution_bars(
        feature_data_dict=demo_data,
        total_samples=228,
        title="Fig. 4. Distribution of input parameters.",
        output_prefix=args.output
    )

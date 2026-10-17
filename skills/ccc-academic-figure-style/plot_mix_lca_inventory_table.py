#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CCC Standard Template: Concrete Mix Inverse Design & LCA Inventory Breakdown
=============================================================================
Stacked bar chart with an integrated, precisely aligned constituent data table
under each subpanel, featuring embedded mini-swatch icons, Times New Roman typography,
inward tick marks, and publication-grade spacing.

Ideal for:
- Concrete mix proportion inverse design / multi-objective optimization (Pareto candidates)
- Life Cycle Assessment (LCA) environmental benchmarking: Embodied Carbon & Embodied Energy
- Constituent inventory contribution & economic cost breakdown
"""

import os
import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ==============================================================================
# Global Publication Typography & Spine Standards (CCC Persona)
# ==============================================================================
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif', 'serif']
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.linewidth'] = 0.9
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['xtick.top'] = False
plt.rcParams['ytick.right'] = False
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42

# Default candidate mix designations (13 representative mixes)
DEFAULT_MIX_IDS = [
    "Control", "K-1", "J-1", "S-1", "R-1", "B-1", "C-1",
    "K-2", "J-2", "S-2", "R-2", "B-2", "C-2"
]

DEFAULT_CONSTITUENTS = [
    "OPC",
    "Fly Ash",
    "RCA",
    "Natural Sand",
    "Natural CA",
    "SP",
    "Fiber"
]

# (a) Embodied Carbon Data (kg CO2-eq/m³)
DEFAULT_CARBON_DATA = {
    "OPC":          [365.0] * 13,
    "Fly Ash":      [0.1] * 13,
    "RCA":          [0.0, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2],
    "Natural Sand": [0.8] * 13,
    "Natural CA":   [5.3] * 13,
    "SP":           [5.3] + [9.3] * 12,
    "Fiber":        [0.0, 12.9, 12.7, 12.1, 34.6, 11.6, 4.6, 12.9, 12.7, 12.1, 34.6, 11.6, 4.6]
}

# (b) Embodied Energy Data (MJ/m³)
DEFAULT_ENERGY_DATA = {
    "OPC":          [2475.0] * 13,
    "Fly Ash":      [2.0] * 13,
    "RCA":          [0.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0],
    "Natural Sand": [15.3] * 13,
    "Natural CA":   [550.0] * 13,
    "SP":           [132.3] + [231.6] * 12,
    "Fiber":        [0.0, 149.8, 92.2, 115.3, 69.2, 80.7, 17.3, 149.8, 92.2, 115.3, 69.2, 80.7, 17.3]
}

# CCC-Compliant Blue-to-Red Scientific Palette with distinct textures
SCIENTIFIC_PALETTE = {
    "OPC":          {"face": "#2F6AB9", "edge": "#1A3B66", "hatch": ""},
    "Fly Ash":      {"face": "#69AADB", "edge": "#2C5B82", "hatch": "///"},
    "RCA":          {"face": "#97C6E6", "edge": "#3B6E96", "hatch": "xxx"},
    "Natural Sand": {"face": "#D5E8F7", "edge": "#688FA8", "hatch": "..."},
    "Natural CA":   {"face": "#F6B7B2", "edge": "#A84C46", "hatch": "\\\\\\"},
    "SP":           {"face": "#EA7B7D", "edge": "#912A2C", "hatch": "+++"},
    "Fiber":        {"face": "#F14040", "edge": "#780A0A", "hatch": "***"},
}


def plot_mix_lca_inventory_table(
    mix_ids=None,
    carbon_dict=None,
    energy_dict=None,
    palette=None,
    output_prefix="mix_lca_inventory_standard"
):
    """
    Renders publication-grade 2-panel stacked bar chart with aligned data tables.
    """
    mix_ids = mix_ids or DEFAULT_MIX_IDS
    carbon_dict = carbon_dict or DEFAULT_CARBON_DATA
    energy_dict = energy_dict or DEFAULT_ENERGY_DATA
    palette = palette or SCIENTIFIC_PALETTE

    constituents = [c for c in DEFAULT_CONSTITUENTS if c in carbon_dict]

    fig = plt.figure(figsize=(7.5, 12.8), dpi=300)

    # Geometry: well-separated axes ensuring the integrated table and sublabels breathe freely
    ax1 = fig.add_axes([0.16, 0.66, 0.80, 0.29])
    ax2 = fig.add_axes([0.16, 0.17, 0.80, 0.29])

    bar_width = 0.56
    x_indices = np.arange(len(mix_ids))

    def _render_panel(ax, data_dict, y_max, y_label, sublabel):
        bottoms = np.zeros(len(mix_ids))

        # 1. Stacked bars (from bottom OPC to top Fiber)
        for name in constituents:
            values = np.array(data_dict[name], dtype=float)
            cfg = palette.get(name, {"face": "#777777", "edge": "#333333", "hatch": ""})
            ax.bar(
                x_indices,
                values,
                bottom=bottoms,
                width=bar_width,
                color=cfg["face"],
                edgecolor=cfg["edge"],
                hatch=cfg["hatch"],
                linewidth=0.75,
                zorder=3
            )
            bottoms += values

        # 2. Spines, ticks & grid
        ax.set_xlim(-0.7, len(mix_ids) - 0.3)
        ax.set_ylim(0, y_max)
        ax.set_ylabel(y_label, fontsize=10.5, fontweight="bold", labelpad=8)
        ax.tick_params(axis='y', labelsize=9.0, length=3.5, width=0.8)
        ax.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
        ax.grid(axis='y', linestyle=':', alpha=0.45, zorder=0)

        # 3. Aligned Data Table
        table_rows = list(reversed(constituents))  # Fiber on top down to OPC at bottom
        cell_text = []
        for name in table_rows:
            row = [f"{val:.1f}" for val in data_dict[name]]
            cell_text.append(row)

        table = ax.table(
            cellText=cell_text,
            rowLabels=table_rows,
            colLabels=mix_ids,
            cellLoc='center',
            rowLoc='left',
            loc='bottom',
            bbox=[0.0, -0.44, 1.0, 0.42]
        )

        table.auto_set_font_size(False)
        table.set_fontsize(8.2)

        # 4. Table cell styling
        cells = table.get_celld()
        for (r, c), cell in cells.items():
            cell.set_linewidth(0.6)
            cell.set_edgecolor("#555555")
            if r == 0:
                cell.set_facecolor("#EDF2F7")
                cell.set_text_props(fontweight='bold', fontsize=8.2)
                cell.set_height(0.055)
            elif c == -1:
                # Row header: indent text slightly to leave room for the swatch icon
                cell.set_facecolor("#F7FAFC")
                cell.set_text_props(fontweight='bold', fontsize=7.8, ha='left')
                orig_text = cell.get_text().get_text()
                cell.get_text().set_text("   " + orig_text)
            else:
                cell.set_facecolor("white")
                cell.set_height(0.048)

        # 5. Draw mini-legend swatch icons inside each row header cell
        fig.canvas.draw()
        for idx, name in enumerate(table_rows, start=1):
            cell = cells[(idx, -1)]
            bbox = cell.get_bbox()
            swatch_w = bbox.width * 0.10
            swatch_h = bbox.height * 0.48
            swatch_x = bbox.x0 + bbox.width * 0.04
            swatch_y = bbox.y0 + (bbox.height - swatch_h) / 2.0

            cfg = palette.get(name, {"face": "#777777", "edge": "#333333", "hatch": ""})
            rect = mpatches.Rectangle(
                (swatch_x, swatch_y),
                swatch_w, swatch_h,
                transform=ax.transAxes,
                facecolor=cfg["face"],
                edgecolor=cfg["edge"],
                hatch=cfg["hatch"],
                linewidth=0.6,
                zorder=10,
                clip_on=False
            )
            ax.add_patch(rect)

        # 6. Subpanel label centered below table
        ax.text(
            0.5, -0.52, sublabel,
            transform=ax.transAxes,
            ha='center', va='top',
            fontsize=12.0, fontweight='bold',
            color='#000000'
        )

    # Render Panel (a) Embodied Carbon
    _render_panel(
        ax1, carbon_dict, y_max=460,
        y_label=r"$\mathbf{Embodied\ carbon\ (kg\ CO_2\text{-}eq/m^3)}$",
        sublabel="(a)"
    )

    # Render Panel (b) Embodied Energy
    _render_panel(
        ax2, energy_dict, y_max=4200,
        y_label=r"$\mathbf{Embodied\ energy\ (MJ/m^3)}$",
        sublabel="(b)"
    )

    png_out = f"{output_prefix}.png"
    pdf_out = f"{output_prefix}.pdf"

    plt.savefig(png_out, dpi=300, bbox_inches='tight')
    plt.savefig(pdf_out, dpi=600, bbox_inches='tight')
    plt.close()

    print(f"[+] Output PNG: {png_out}")
    print(f"[+] Output PDF: {pdf_out}")
    return png_out, pdf_out


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CCC Mix LCA Inventory Breakdown Plotter")
    parser.add_argument("--output", "-o", default="mix_lca_inventory_standard", help="Output prefix name")
    args = parser.parse_args()

    plot_mix_lca_inventory_table(output_prefix=args.output)

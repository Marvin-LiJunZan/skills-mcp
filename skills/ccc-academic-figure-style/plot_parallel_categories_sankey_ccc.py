"""
Publication-Grade Parallel Categories / Multilevel Sankey Diagram Generator
STRICT CCC SIGNATURE PALETTE EDITION:
- District (Extreme High / Highlighted cohort): #F14040 (CCC Crimson Vivid Red)
- Building (Baseline / Bulk cohort):            #2F6AB9 (CCC Dark Sapphire Blue)
- City     (Special Highlighted trend):         #FEC211 (CCC Signature Highlight Yellow)

Author: CCC Academic Skills Ecosystem
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path

# --- CCC Universal Typography & Rendering Standards ---
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif', 'serif']
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42

# --- CCC Canonical Blue-Red 6-Step Palette & Golden Highlight ---
# District: #F14040 (Level 6: Crimson Vivid Red)
# Building: #2F6AB9 (Level 1: Dark Sapphire Blue)
# City:     #FEC211 (Signature Highlight Yellow)
COLOR_MAP_CCC = {
    "District": "#F14040",   # 阶6: 绯红强色 (Crimson Vivid Red)
    "Building": "#2F6AB9",   # 阶1: 深海蓝 (Dark Sapphire Blue)
    "City":     "#FEC211"    # 专属特别高亮/趋势线亮黄色
}

# Node blocks styling (Pure academic clean look)
NODE_FACE = "#F8FAFC"        # Crisp, light slate off-white
NODE_EDGE = "#94A3B8"        # Subtle slate border
NODE_LW = 0.85

def draw_bezier_flow(ax, x0, y0_b, y0_t, x1, y1_b, y1_t, color, alpha=0.68):
    """Draw smooth S-curve cubic Bezier polygon between stage x0 and stage x1."""
    dx = (x1 - x0) * 0.48
    verts = [
        (x0, y0_b),
        (x0 + dx, y0_b), (x1 - dx, y1_b), (x1, y1_b),
        (x1, y1_t),
        (x1 - dx, y1_t), (x0 + dx, y0_t), (x0, y0_t),
        (x0, y0_b)
    ]
    codes = [
        Path.MOVETO,
        Path.CURVE4, Path.CURVE4, Path.CURVE4,
        Path.LINETO,
        Path.CURVE4, Path.CURVE4, Path.CURVE4,
        Path.CLOSEPOLY
    ]
    patch = patches.PathPatch(
        Path(verts, codes),
        facecolor=color,
        edgecolor="none",
        alpha=alpha,
        zorder=2
    )
    ax.add_patch(patch)

def plot_parallel_categories_ccc_style(df, output_prefix="parallel_categories_sankey_ccc_standard"):
    """
    Renders the parallel categories diagram with strict CCC Signature Palette.
    """
    fig, ax = plt.subplots(figsize=(13.0, 5.8), dpi=300)
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")

    # Dimensions / Columns
    dimensions = [
        "Spatial scale",
        "Temporal regime",
        "Data regime",
        "Calibration methods",
        "SA",
        "Sampling",
        "Metamodel"
    ]
    
    # Category ordering per dimension (matching top-to-bottom layout of reference figure)
    dim_orders = {
        "Spatial scale": ["District", "Building", "City"],
        "Temporal regime": ["Static", "Quasi-dynamic", "Dynamic"],
        "Data regime": ["Data-mixed", "Data-scarce", "Data-rich"],
        "Calibration methods": ["Bayesian", "Manual", "Optimization", "ML"],
        "SA": ["No", "SA"],
        "Sampling": ["No", "Sampling"],
        "Metamodel": ["No", "Metamodel"]
    }

    n_stages = len(dimensions)
    
    TOTAL_HEIGHT = 100.0
    NODE_WIDTH = 0.22
    GAP = 2.0  # Gap between categories in the same column
    
    # X-coordinates for the 7 stages
    stage_x = [0.2 + i * 1.05 for i in range(n_stages)]
    
    # Compute node positions for each stage
    node_positions = {}
    for col_idx, col in enumerate(dimensions):
        node_positions[col] = {}
        cats = dim_orders[col]
        
        counts = df[col].value_counts()
        total_counts = sum(counts.get(c, 0) for c in cats)
        
        n_cats = len(cats)
        avail_h = TOTAL_HEIGHT - (n_cats - 1) * GAP
        
        cur_top = TOTAL_HEIGHT
        for cat in cats:
            cnt = counts.get(cat, 0)
            h = (cnt / total_counts) * avail_h if total_counts > 0 else 0
            b = cur_top - h
            node_positions[col][cat] = {
                'bottom': b,
                'height': h,
                'top': cur_top,
                'count': cnt,
                'cur_y_out': cur_top,
                'cur_y_in': cur_top
            }
            cur_top = b - GAP

    # Sort DataFrame rows
    df_sorted = df.sort_values(by=dimensions, ascending=[True] * len(dimensions)).copy()

    # Draw ribbons between adjacent stages
    for i in range(n_stages - 1):
        col0 = dimensions[i]
        col1 = dimensions[i + 1]
        x0 = stage_x[i] + NODE_WIDTH
        x1 = stage_x[i + 1]
        
        group_cols = ["Spatial scale"]
        if col0 not in group_cols:
            group_cols.append(col0)
        if col1 not in group_cols:
            group_cols.append(col1)
            
        flow_groups = df_sorted.groupby(group_cols, sort=False).size().reset_index(name='count')
        
        for _, row in flow_groups.iterrows():
            origin_scale = row["Spatial scale"]
            cat0 = row[col0]
            cat1 = row[col1]
            cnt = row['count']
            
            # Using CCC Canonical Colors
            color = COLOR_MAP_CCC.get(origin_scale, "#2F6AB9")
            
            # Height of this flow in col0 and col1
            h0 = (cnt / df[col0].value_counts()[cat0]) * node_positions[col0][cat0]['height']
            h1 = (cnt / df[col1].value_counts()[cat1]) * node_positions[col1][cat1]['height']
            
            y0_top = node_positions[col0][cat0]['cur_y_out']
            y0_bot = y0_top - h0
            node_positions[col0][cat0]['cur_y_out'] = y0_bot
            
            y1_top = node_positions[col1][cat1]['cur_y_in']
            y1_bot = y1_top - h1
            node_positions[col1][cat1]['cur_y_in'] = y1_bot
            
            # Alpha slightly lighter (0.65) for dark sapphire blue and crimson to avoid over-dark overlaps
            draw_bezier_flow(ax, x0, y0_bot, y0_top, x1, y1_bot, y1_top, color, alpha=0.65)

    # Draw Node Rectangles and Category Text Labels
    for i, col in enumerate(dimensions):
        x = stage_x[i]
        for cat in dim_orders[col]:
            pos = node_positions[col][cat]
            b = pos['bottom']
            h = pos['height']
            
            rect = patches.Rectangle(
                (x, b), NODE_WIDTH, h,
                facecolor=NODE_FACE,
                edgecolor=NODE_EDGE,
                linewidth=NODE_LW,
                zorder=4
            )
            ax.add_patch(rect)
            
            fontsize = 9.0 if h >= 12 else (8.0 if h >= 6 else 6.8)
            ax.text(
                x + NODE_WIDTH / 2.0, b + h / 2.0, cat,
                ha='center', va='center',
                fontsize=fontsize,
                fontweight='normal',
                color='#0F172A',
                fontfamily='Times New Roman',
                zorder=5
            )

    # Draw Stage Headers (Bottom Axis)
    stage_headers = [
        "Spatial\nscale",
        "Temporal\nregime",
        "Data\nregime",
        "Calibration\nmethods",
        "SA",
        "Sampling",
        "Metamodel"
    ]
    for i, title in enumerate(stage_headers):
        x = stage_x[i] + NODE_WIDTH / 2.0
        ax.text(
            x, -5.5, title,
            ha='center', va='top',
            fontsize=10.5,
            fontweight='bold',
            color='#1E293B',
            fontfamily='Times New Roman',
            linespacing=1.05
        )

    # Draw "Accelerating techniques" bottom grouping bracket
    bracket_x0 = stage_x[4]
    bracket_x1 = stage_x[6] + NODE_WIDTH
    bracket_y = -12.5
    tick_len = 1.2
    
    ax.plot([bracket_x0, bracket_x1], [bracket_y, bracket_y], color="#334155", lw=1.1, clip_on=False)
    ax.plot([bracket_x0, bracket_x0], [bracket_y, bracket_y + tick_len], color="#334155", lw=1.1, clip_on=False)
    ax.plot([bracket_x1, bracket_x1], [bracket_y, bracket_y + tick_len], color="#334155", lw=1.1, clip_on=False)

    ax.text(
        (bracket_x0 + bracket_x1) / 2.0, -14.2, "Accelerating techniques",
        ha='center', va='top',
        fontsize=11.0,
        fontweight='bold',
        color='#1E293B',
        fontfamily='Times New Roman'
    )

    ax.set_xlim(-0.05, stage_x[-1] + NODE_WIDTH + 0.3)
    ax.set_ylim(-18.0, 102.0)
    ax.axis('off')

    plt.subplots_adjust(left=0.02, right=0.98, top=0.97, bottom=0.18)

    # Export
    png_file = f"{output_prefix}.png"
    pdf_file = f"{output_prefix}.pdf"
    svg_file = f"{output_prefix}.svg"
    plt.savefig(png_file, dpi=300, facecolor='#FFFFFF', edgecolor='none')
    plt.savefig(pdf_file, dpi=600, facecolor='#FFFFFF', edgecolor='none')
    plt.savefig(svg_file, facecolor='#FFFFFF', edgecolor='none')
    plt.close()
    
    print(f"[Done] Generated CCC Standard Palette edition: {png_file}, {pdf_file}, and {svg_file}")
    return png_file, pdf_file

if __name__ == "__main__":
    data_csv = r"c:\JunzanLi_project\skills_mcp\skills\ccc-academic-figure-style\calibration_survey_dataset.csv"
    df_in = pd.read_csv(data_csv)
        
    out_dir = r"c:\JunzanLi_project\skills_mcp\skills\ccc-academic-figure-style"
    plot_parallel_categories_ccc_style(df_in, output_prefix=os.path.join(out_dir, "parallel_categories_sankey_ccc_standard"))

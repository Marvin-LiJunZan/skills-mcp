"""
Publication-Grade Model Evaluation Heatmap Table Generator (CCC Academic Standard)
Matches exact reference style of media_1789981969299.png:
- Dual-block layout: 'Train' and 'Test' sets side-by-side
- Deep teal header cells (#00897B) with bold white text (MAE, RMSE, MAPE, R^2)
- Cyan gradient shading where darker cells represent proximity to 'ideal value'
- Best R^2 values on Test set highlighted in bold red font
- Bottom legend: 4 horizontal gradient colorbars indicating metric convergence to 'ideal value'
- Strict CCC axis rules: no top/right ticks, crisp white cell borders, Times New Roman typography

Author: CCC Academic Figure Skills Ecosystem
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.colors import LinearSegmentedColormap

# --- Typography & Export Standards ---
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif', 'serif']
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42
plt.rcParams['xtick.top'] = False
plt.rcParams['ytick.right'] = False

# --- CCC Mandatory Academic Red-Blue Palette ---
# Exact CCC Standard Colors from SKILL.md:
# BLUE_RED_6: ["#2F6AB9", "#69AADB", "#97C6E6", "#F6B7B2", "#EA7B7D", "#F14040"]
# HIGHLIGHT_YELLOW: "#FEC211"

COLOR_CCC_BLUE = '#2F6AB9'    # CCC 阶1: 深海蓝 (Dark Sapphire Blue)
COLOR_CCC_RED = '#E63939'     # CCC 阶6: 绯红强色 (Crimson Vivid Red)
HIGHLIGHT_YELLOW = '#FEC211'  # CCC Signature Bright Yellow (#FEC211)

# Train Colormap: CCC Sapphire Blue gradient (white -> soft ice blue #97C6E6 -> light sky blue #69AADB -> CCC blue #2F6AB9)
CCC_BLUE_CMAP = LinearSegmentedColormap.from_list(
    'ccc_eval_blue',
    ['#FFFFFF', '#F0F6FC', '#D6E7F8', '#97C6E6', '#69AADB', '#4689D2', '#2F6AB9'],
    N=256
)

# Test Colormap: CCC Crimson Red gradient (white -> soft peach #F6B7B2 -> coral #EA7B7D -> CCC red #E63939)
CCC_RED_CMAP = LinearSegmentedColormap.from_list(
    'ccc_eval_red',
    ['#FFFFFF', '#FDF3F3', '#FCD7DA', '#F6B7B2', '#EA7B7D', '#E85B5F', '#E63939'],
    N=256
)

HEADER_BG_TRAIN = COLOR_CCC_BLUE  # CCC Standard Sapphire Blue (#2F6AB9)
HEADER_BG_TEST = COLOR_CCC_RED    # CCC Standard Crimson Red (#E63939)
CELL_EDGE = '#FFFFFF'             # Crisp white separator between cells
NORMAL_TEXT_COLOR = '#0F172A'     # Deep slate black for numbers


def plot_evaluation_heatmap_table(models_data, output_path="model_evaluation_heatmap_table.png"):
    """
    Renders the publication evaluation heatmap matrix table with CCC Red-Blue dual palette.
    """
    fig, ax = plt.subplots(figsize=(10.5, 5.9), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')
    
    cols = ['MAE', 'RMSE', 'MAPE', 'R2']
    col_labels = ['MAE', 'RMSE', 'MAPE', r'$\mathbf{R^2}$']
    
    # Calculate normalization min/max per task for fair shading
    tasks = list(dict.fromkeys([d['task'] for d in models_data]))
    norm_ranges = {}
    for task in tasks:
        task_rows = [d for d in models_data if d['task'] == task]
        norm_ranges[task] = {}
        for m in cols:
            tr_vals = [r['train'][m] for r in task_rows]
            te_vals = [r['test'][m] for r in task_rows]
            all_vals = tr_vals + te_vals
            if m == 'R2':
                norm_ranges[task][m] = (min(0.50, min(all_vals)), 1.0)
            else:
                norm_ranges[task][m] = (0.0, max(all_vals) * 1.08)

    def get_cell_color(val, task, m, split='train'):
        v_min, v_max = norm_ranges[task][m]
        if m == 'R2':
            score = (val - v_min) / (v_max - v_min + 1e-9)
            score = max(0.60, score)
        else:
            score = 1.0 - (val - v_min) / (v_max - v_min + 1e-9)
        score = np.clip(score * 0.80, 0.02, 0.80)
        cmap = CCC_BLUE_CMAP if split == 'train' else CCC_RED_CMAP
        return cmap(score)

    def get_text_color(col_rgb, split='train'):
        """Perceived luminance according to ITU-R BT.601: returns white for dark/saturated cells, slate for light."""
        lum = 0.299 * col_rgb[0] + 0.587 * col_rgb[1] + 0.114 * col_rgb[2]
        threshold = 0.80 if split == 'train' else 0.70
        return '#FFFFFF' if lum < threshold else '#0F172A'

    # Layout geometry
    cell_w = 0.95
    label_w = 2.45
    train_x0 = label_w
    test_x0 = train_x0 + 4 * cell_w + 0.35
    
    row_h = 0.48
    header_h = 0.50
    table_top = 4.8
    
    # 1. Block Titles: "Train" (CCC Blue #2F6AB9) and "Test" (CCC Red #E63939)
    train_center_x = train_x0 + 2 * cell_w
    test_center_x = test_x0 + 2 * cell_w
    title_y = table_top + 0.16
    
    ax.text(train_center_x, title_y, 'Train', ha='center', va='bottom',
            fontsize=13.0, fontweight='bold', fontfamily='Times New Roman', color=COLOR_CCC_BLUE)
    ax.text(test_center_x, title_y, 'Test', ha='center', va='bottom',
            fontsize=13.0, fontweight='bold', fontfamily='Times New Roman', color=COLOR_CCC_RED)
    
    # 2. Header Row: Train (CCC Sapphire Blue) & Test (CCC Crimson Red)
    hdr_y = table_top - header_h
    for j, m_lbl in enumerate(col_labels):
        x = train_x0 + j * cell_w
        rect = patches.Rectangle((x, hdr_y), cell_w, header_h,
                                 facecolor=HEADER_BG_TRAIN, edgecolor=CELL_EDGE, linewidth=1.2, zorder=2)
        ax.add_patch(rect)
        ax.text(x + cell_w / 2.0, hdr_y + header_h / 2.0, m_lbl,
                ha='center', va='center', fontsize=11.5, fontweight='bold',
                fontfamily='Times New Roman', color='#FFFFFF', zorder=3)
        
    for j, m_lbl in enumerate(col_labels):
        x = test_x0 + j * cell_w
        rect = patches.Rectangle((x, hdr_y), cell_w, header_h,
                                 facecolor=HEADER_BG_TEST, edgecolor=CELL_EDGE, linewidth=1.2, zorder=2)
        ax.add_patch(rect)
        ax.text(x + cell_w / 2.0, hdr_y + header_h / 2.0, m_lbl,
                ha='center', va='center', fontsize=11.5, fontweight='bold',
                fontfamily='Times New Roman', color='#FFFFFF', zorder=3)

        
    # 3. Model Data Rows
    cur_y = hdr_y
    prev_task = None
    for i, row in enumerate(models_data):
        task = row['task']
        name = row['name']
        
        # Add slight task separation gap between CS and FF
        if prev_task is not None and task != prev_task:
            cur_y -= 0.08
        prev_task = task
        
        cur_y -= row_h
        
        # Row label on left
        ax.text(train_x0 - 0.15, cur_y + row_h / 2.0, name,
                ha='right', va='center', fontsize=10.5, fontweight='bold',
                fontfamily='Times New Roman', color='#0F172A', zorder=3)
        
        # Train cells (Blue)
        for j, m in enumerate(cols):
            x = train_x0 + j * cell_w
            val = row['train'][m]
            col_rgb = get_cell_color(val, task, m, split='train')
            rect = patches.Rectangle((x, cur_y), cell_w, row_h,
                                     facecolor=col_rgb, edgecolor=CELL_EDGE, linewidth=1.2, zorder=2)
            ax.add_patch(rect)
            
            if m == 'R2':
                val_txt = f"{val:.3f}" if val < 0.999 else "1.00"
            elif m == 'MAPE':
                val_txt = f"{val:.3f}" if val < 0.1 else f"{val:.2f}"
            elif m in ['MAE', 'RMSE']:
                val_txt = f"{val:.3f}" if val < 0.01 else (f"{val:.2f}" if val < 10 else f"{val:.1f}")
                
            txt_color = get_text_color(col_rgb, split='train')
            ax.text(x + cell_w / 2.0, cur_y + row_h / 2.0, val_txt,
                    ha='center', va='center', fontsize=10.0,
                    fontfamily='Times New Roman', color=txt_color, zorder=3)
            
        # Test cells (Red)
        for j, m in enumerate(cols):
            x = test_x0 + j * cell_w
            val = row['test'][m]
            col_rgb = get_cell_color(val, task, m, split='test')
            rect = patches.Rectangle((x, cur_y), cell_w, row_h,
                                     facecolor=col_rgb, edgecolor=CELL_EDGE, linewidth=1.2, zorder=2)
            ax.add_patch(rect)
            
            is_best_r2 = (m == 'R2' and row.get('is_best_test_r2', False))
            if m == 'R2':
                txt_color = '#FFFFFF'
                if is_best_r2:
                    best_box = patches.Rectangle((x, cur_y), cell_w, row_h,
                                                 fill=False, edgecolor=HIGHLIGHT_YELLOW, linewidth=2.0, zorder=4)
                    ax.add_patch(best_box)
                    fweight = 'bold'
                else:
                    fweight = 'normal'
            else:
                txt_color = get_text_color(col_rgb, split='test')
                fweight = 'normal'
            
            if m == 'R2':
                val_txt = f"{val:.3f}" if val < 0.999 else "1.00"
            elif m == 'MAPE':
                val_txt = f"{val:.3f}" if val < 0.1 else f"{val:.2f}"
            elif m in ['MAE', 'RMSE']:
                val_txt = f"{val:.3f}" if val < 0.01 else (f"{val:.2f}" if val < 10 else f"{val:.1f}")
                
            ax.text(x + cell_w / 2.0, cur_y + row_h / 2.0, val_txt,
                    ha='center', va='center', fontsize=10.0, fontweight=fweight,
                    fontfamily='Times New Roman', color=txt_color, zorder=3)

    # 4. Bottom Legend: 4 Horizontal Gradient Colorbars (Train in Blue, Test in Red)
    legend_top = cur_y - 0.48
    bar_w = 2.25
    bar_h = 0.14
    
    cbar_left_x = train_x0 + 1.10
    cbar_right_x = test_x0 + 1.10
    
    def draw_gradient_bar(x, y, w, h, left_composite_label, ideal_txt, cmap, show_ideal_title=False):
        grad = np.linspace(0.02, 0.85, 256).reshape(1, -1)
        ax.imshow(grad, extent=[x, x + w, y, y + h], aspect='auto', cmap=cmap, zorder=2)
        rect = patches.Rectangle((x, y), w, h, fill=False, edgecolor='#333333', linewidth=0.8, zorder=3)
        ax.add_patch(rect)
        
        # Composite text to the left
        ax.text(x - 0.08, y + h / 2.0, left_composite_label, ha='right', va='center',
                fontsize=9.2, fontfamily='Times New Roman', color='#0F172A')
        # Ideal value label to the right
        ax.text(x + w + 0.08, y + h / 2.0, ideal_txt, ha='left', va='center',
                fontsize=9.5, fontfamily='Times New Roman', color='#0F172A')
        # "ideal value" text above the right side
        if show_ideal_title:
            ax.text(x + w + 0.08, y + h + 0.06, 'ideal value', ha='center', va='bottom',
                    fontsize=9.2, fontfamily='Times New Roman', color='#0F172A')

    # Row 1: Train Error (Blue, left) and Test Error (Red, right)
    draw_gradient_bar(cbar_left_x, legend_top, bar_w, bar_h, 'Train Error', '0', CCC_BLUE_CMAP, show_ideal_title=True)
    draw_gradient_bar(cbar_right_x, legend_top, bar_w, bar_h, 'Test Error', '0', CCC_RED_CMAP, show_ideal_title=True)
    
    # Row 2: Train R^2 (Blue, left) and Test R^2 (Red, right)
    draw_gradient_bar(cbar_left_x, legend_top - 0.34, bar_w, bar_h, r'Train $\mathrm{R^2}$ 0.5', '1', CCC_BLUE_CMAP, show_ideal_title=False)
    draw_gradient_bar(cbar_right_x, legend_top - 0.34, bar_w, bar_h, r'Test $\mathrm{R^2}$ 0.5', '1', CCC_RED_CMAP, show_ideal_title=False)

    # 5. Caption at the bottom
    caption_y = legend_top - 0.75
    ax.text((train_x0 + test_x0 + 4 * cell_w) / 2.0, caption_y,

            'Fig. 4. Evaluation indexes for the predictive models on compressive strength and fresh fluidity.',
            ha='center', va='top', fontsize=10.5, fontfamily='Times New Roman', color='#0F172A')

    ax.set_xlim(0.0, test_x0 + 4 * cell_w + 0.5)
    ax.set_ylim(caption_y - 0.35, table_top + 0.7)
    ax.axis('off')
    
    plt.subplots_adjust(left=0.01, right=0.99, top=0.98, bottom=0.02)
    
    base, _ = os.path.splitext(output_path)
    png_out = f"{base}.png"
    pdf_out = f"{base}.pdf"
    plt.savefig(png_out, dpi=300, bbox_inches='tight', facecolor='#FFFFFF', edgecolor='none')
    plt.savefig(pdf_out, dpi=600, bbox_inches='tight', facecolor='#FFFFFF', edgecolor='none')
    artifact_png = os.path.join(r"C:\Users\12830\.gemini\antigravity\brain\36a320c1-f064-4608-bded-3c20cecff9d2", "fig4_model_evaluation_heatmap_table.png")
    plt.savefig(artifact_png, dpi=300, bbox_inches='tight', facecolor='#FFFFFF', edgecolor='none')
    plt.close()

    print(f"[Done] Generated Model Evaluation Heatmap Table: {png_out}, {pdf_out}")
    return png_out, pdf_out

if __name__ == '__main__':
    demo_models = [
        {
            'task': 'Compressive Strength',
            'name': r'$\mathbf{CS}$-$\mathrm{ExtraTrees}$',
            'train': {'MAE': 0.121, 'RMSE': 0.694, 'MAPE': 0.016, 'R2': 0.9995},
            'test':  {'MAE': 2.057, 'RMSE': 3.353, 'MAPE': 0.105, 'R2': 0.9866},
            'is_best_test_r2': True
        },
        {
            'task': 'Compressive Strength',
            'name': r'$\mathbf{CS}$-$\mathrm{CatBoost}$',
            'train': {'MAE': 1.466, 'RMSE': 2.070, 'MAPE': 0.285, 'R2': 0.9956},
            'test':  {'MAE': 2.691, 'RMSE': 3.975, 'MAPE': 0.694, 'R2': 0.9812},
            'is_best_test_r2': False
        },
        {
            'task': 'Compressive Strength',
            'name': r'$\mathbf{CS}$-$\mathrm{XGBoost}$',
            'train': {'MAE': 0.683, 'RMSE': 1.080, 'MAPE': 0.063, 'R2': 0.9988},
            'test':  {'MAE': 2.621, 'RMSE': 4.074, 'MAPE': 0.224, 'R2': 0.9802},
            'is_best_test_r2': False
        },
        {
            'task': 'Compressive Strength',
            'name': r'$\mathbf{CS}$-$\mathrm{RandomForest}$',
            'train': {'MAE': 1.613, 'RMSE': 2.450, 'MAPE': 0.070, 'R2': 0.9938},
            'test':  {'MAE': 4.112, 'RMSE': 6.424, 'MAPE': 0.146, 'R2': 0.9508},
            'is_best_test_r2': False
        },
        {
            'task': 'Fresh Fluidity',
            'name': r'$\mathbf{FF}$-$\mathrm{TabPFN+ResBoost}$',
            'train': {'MAE': 2.900, 'RMSE': 4.554, 'MAPE': 0.013, 'R2': 0.9957},
            'test':  {'MAE': 11.060, 'RMSE': 17.678, 'MAPE': 0.047, 'R2': 0.9022},
            'is_best_test_r2': True
        },
        {
            'task': 'Fresh Fluidity',
            'name': r'$\mathbf{FF}$-$\mathrm{TabPFN\ v2}$',
            'train': {'MAE': 7.150, 'RMSE': 9.850, 'MAPE': 0.031, 'R2': 0.9802},
            'test':  {'MAE': 12.120, 'RMSE': 18.992, 'MAPE': 0.052, 'R2': 0.8871},
            'is_best_test_r2': False
        },
        {
            'task': 'Fresh Fluidity',
            'name': r'$\mathbf{FF}$-$\mathrm{CatBoost}$',
            'train': {'MAE': 4.860, 'RMSE': 6.840, 'MAPE': 0.021, 'R2': 0.9901},
            'test':  {'MAE': 14.648, 'RMSE': 22.588, 'MAPE': 0.063, 'R2': 0.8403},
            'is_best_test_r2': False
        },
        {
            'task': 'Fresh Fluidity',
            'name': r'$\mathbf{FF}$-$\mathrm{ExtraTrees}$',
            'train': {'MAE': 2.350, 'RMSE': 3.650, 'MAPE': 0.010, 'R2': 0.9972},
            'test':  {'MAE': 14.241, 'RMSE': 23.550, 'MAPE': 0.061, 'R2': 0.8264},
            'is_best_test_r2': False
        },
    ]
    
    out_file = os.path.join(r"c:\JunzanLi_project\灌浆材料\paper\figures", "fig4_model_evaluation_heatmap_table.png")
    plot_evaluation_heatmap_table(demo_models, output_path=out_file)

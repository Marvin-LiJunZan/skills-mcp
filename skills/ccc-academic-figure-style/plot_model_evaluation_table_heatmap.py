"""
Publication-Grade Model Evaluation Heatmap Table Generator (CCC Academic Standard)
Matches exact reference style of top-tier Elsevier / Nature journals:
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

# --- CCC Mandatory Academic Color Palette ---
# Colormap: CCC Sapphire Blue gradient (from pure white / light ice blue to deep sapphire blue #2F6AB9)
CCC_BLUE_CMAP = LinearSegmentedColormap.from_list(
    'ccc_eval_blue',
    ['#FFFFFF', '#F0F6FC', '#CFE2F7', '#97C6E6', '#69AADB', '#3B7FC4', '#2F6AB9'],
    N=256
)

HEADER_BG = '#1F4E79'         # CCC Deep Academic Sapphire Navy for headers
CELL_EDGE = '#FFFFFF'         # Crisp white separator between cells
BEST_TEXT_COLOR = '#E63939'   # CCC Crimson Red (#E63939) for best Test R2
HIGHLIGHT_YELLOW = '#FEC211'  # CCC Signature Bright Yellow (#FEC211) for optimal highlight
NORMAL_TEXT_COLOR = '#0F172A' # Deep slate black for numbers


def plot_evaluation_heatmap_table(models_data, output_path="model_evaluation_heatmap_table.png", title_caption=None):
    """
    Renders the publication evaluation heatmap matrix table.
    
    Parameters:
    -----------
    models_data : list of dicts
        Each dict represents a model evaluation row:
        {
            'task': 'Compressive Strength',
            'name': 'ExtraTrees',
            'train': {'MAE': 0.121, 'RMSE': 0.694, 'MAPE': 0.016, 'R2': 0.9995},
            'test':  {'MAE': 2.057, 'RMSE': 3.353, 'MAPE': 0.105, 'R2': 0.9866},
            'is_best_test_r2': True
        }
    output_path : str
        Output file path for PNG and PDF.
    title_caption : str, optional
        Bottom figure caption text.
    """
    fig, ax = plt.subplots(figsize=(10.5, 5.9), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')
    
    cols = ['MAE', 'RMSE', 'MAPE', 'R2']
    col_labels = ['MAE', 'RMSE', 'MAPE', r'$\mathbf{R^2}$']
    
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
                norm_ranges[task][m] = (min(0.70, min(all_vals)), 1.0)
            else:
                norm_ranges[task][m] = (0.0, max(all_vals) * 1.08)

    def get_cell_color(val, task, m):
        v_min, v_max = norm_ranges[task][m]
        if m == 'R2':
            score = (val - v_min) / (v_max - v_min + 1e-9)
        else:
            score = 1.0 - (val - v_min) / (v_max - v_min + 1e-9)
        score = np.clip(score * 0.82, 0.02, 0.85)
        return CCC_BLUE_CMAP(score)


    cell_w = 0.95
    label_w = 2.45
    train_x0 = label_w
    test_x0 = train_x0 + 4 * cell_w + 0.35
    
    row_h = 0.48
    header_h = 0.50
    table_top = 4.8
    
    # Block Titles: "Train" and "Test"
    train_center_x = train_x0 + 2 * cell_w
    test_center_x = test_x0 + 2 * cell_w
    title_y = table_top + 0.16
    
    ax.text(train_center_x, title_y, 'Train', ha='center', va='bottom',
            fontsize=13.0, fontweight='bold', fontfamily='Times New Roman', color='#0F172A')
    ax.text(test_center_x, title_y, 'Test', ha='center', va='bottom',
            fontsize=13.0, fontweight='bold', fontfamily='Times New Roman', color='#0F172A')
    
    # Header Row
    hdr_y = table_top - header_h
    for j, m_lbl in enumerate(col_labels):
        x = train_x0 + j * cell_w
        rect = patches.Rectangle((x, hdr_y), cell_w, header_h,
                                 facecolor=HEADER_BG, edgecolor=CELL_EDGE, linewidth=1.2, zorder=2)
        ax.add_patch(rect)
        ax.text(x + cell_w / 2.0, hdr_y + header_h / 2.0, m_lbl,
                ha='center', va='center', fontsize=11.5, fontweight='bold',
                fontfamily='Times New Roman', color='#FFFFFF', zorder=3)
        
    for j, m_lbl in enumerate(col_labels):
        x = test_x0 + j * cell_w
        rect = patches.Rectangle((x, hdr_y), cell_w, header_h,
                                 facecolor=HEADER_BG, edgecolor=CELL_EDGE, linewidth=1.2, zorder=2)
        ax.add_patch(rect)
        ax.text(x + cell_w / 2.0, hdr_y + header_h / 2.0, m_lbl,
                ha='center', va='center', fontsize=11.5, fontweight='bold',
                fontfamily='Times New Roman', color='#FFFFFF', zorder=3)
        
    # Model Data Rows
    cur_y = hdr_y
    prev_task = None
    for i, row in enumerate(models_data):
        task = row['task']
        name = row['name']
        
        if prev_task is not None and task != prev_task:
            cur_y -= 0.08
        prev_task = task
        cur_y -= row_h
        
        ax.text(train_x0 - 0.15, cur_y + row_h / 2.0, name,
                ha='right', va='center', fontsize=10.5, fontweight='bold',
                fontfamily='Times New Roman', color='#0F172A', zorder=3)
        
        for j, m in enumerate(cols):
            x = train_x0 + j * cell_w
            val = row['train'][m]
            col_rgb = get_cell_color(val, task, m)
            rect = patches.Rectangle((x, cur_y), cell_w, row_h,
                                     facecolor=col_rgb, edgecolor=CELL_EDGE, linewidth=1.2, zorder=2)
            ax.add_patch(rect)
            
            if m == 'R2':
                val_txt = f"{val:.3f}" if val < 0.999 else "1.00"
            elif m == 'MAPE':
                val_txt = f"{val:.3f}" if val < 0.1 else f"{val:.2f}"
            elif m in ['MAE', 'RMSE']:
                val_txt = f"{val:.3f}" if val < 0.01 else (f"{val:.2f}" if val < 10 else f"{val:.1f}")
                
            ax.text(x + cell_w / 2.0, cur_y + row_h / 2.0, val_txt,
                    ha='center', va='center', fontsize=10.0,
                    fontfamily='Times New Roman', color=NORMAL_TEXT_COLOR, zorder=3)
            
        for j, m in enumerate(cols):
            x = test_x0 + j * cell_w
            val = row['test'][m]
            col_rgb = get_cell_color(val, task, m)
            rect = patches.Rectangle((x, cur_y), cell_w, row_h,
                                     facecolor=col_rgb, edgecolor=CELL_EDGE, linewidth=1.2, zorder=2)
            ax.add_patch(rect)
            
            is_best_r2 = (m == 'R2' and row.get('is_best_test_r2', False))
            txt_color = BEST_TEXT_COLOR if is_best_r2 else NORMAL_TEXT_COLOR
            fweight = 'bold' if is_best_r2 else 'normal'
            
            if is_best_r2:
                # Add CCC signature golden yellow outline on best cell
                best_box = patches.Rectangle((x, cur_y), cell_w, row_h,
                                             fill=False, edgecolor=HIGHLIGHT_YELLOW, linewidth=1.8, zorder=4)
                ax.add_patch(best_box)
            
            if m == 'R2':
                val_txt = f"{val:.3f}" if val < 0.999 else "1.00"
            elif m == 'MAPE':
                val_txt = f"{val:.3f}" if val < 0.1 else f"{val:.2f}"
            elif m in ['MAE', 'RMSE']:
                val_txt = f"{val:.3f}" if val < 0.01 else (f"{val:.2f}" if val < 10 else f"{val:.1f}")
                
            ax.text(x + cell_w / 2.0, cur_y + row_h / 2.0, val_txt,
                    ha='center', va='center', fontsize=10.0, fontweight=fweight,
                    fontfamily='Times New Roman', color=txt_color, zorder=3)

    # Bottom Legend: 4 Horizontal Gradient Colorbars
    legend_top = cur_y - 0.48
    bar_w = 2.40
    bar_h = 0.14
    
    cbar_left_x = train_x0 + 0.95
    cbar_right_x = test_x0 + 0.95
    
    def draw_gradient_bar(x, y, w, h, left_composite_label, ideal_txt, show_ideal_title=False):
        grad = np.linspace(0.02, 0.85, 256).reshape(1, -1)
        ax.imshow(grad, extent=[x, x + w, y, y + h], aspect='auto', cmap=CCC_BLUE_CMAP, zorder=2)
        rect = patches.Rectangle((x, y), w, h, fill=False, edgecolor='#333333', linewidth=0.8, zorder=3)
        ax.add_patch(rect)

        
        ax.text(x - 0.08, y + h / 2.0, left_composite_label, ha='right', va='center',
                fontsize=9.8, fontfamily='Times New Roman', color='#0F172A')
        ax.text(x + w + 0.08, y + h / 2.0, ideal_txt, ha='left', va='center',
                fontsize=9.5, fontfamily='Times New Roman', color='#0F172A')
        if show_ideal_title:
            ax.text(x + w + 0.08, y + h + 0.06, 'ideal value', ha='center', va='bottom',
                    fontsize=9.5, fontfamily='Times New Roman', color='#0F172A')

    # Row 1: MAE (left) and RMSE (right)
    draw_gradient_bar(cbar_left_x, legend_top, bar_w, bar_h, 'MAE 0.7', '0', show_ideal_title=True)
    draw_gradient_bar(cbar_right_x, legend_top, bar_w, bar_h, r'RMSE >0.7', '0', show_ideal_title=True)
    
    # Row 2: MAPE (left) and R^2 (right)
    draw_gradient_bar(cbar_left_x, legend_top - 0.34, bar_w, bar_h, 'MAPE 0.7', '0', show_ideal_title=False)
    draw_gradient_bar(cbar_right_x, legend_top - 0.34, bar_w, bar_h, r'$\mathrm{R^2}$ 0.7', '1', show_ideal_title=False)

    # Caption
    caption_y = legend_top - 0.75
    caption_str = title_caption if title_caption else 'Evaluation indexes for the predictive models.'
    ax.text((train_x0 + test_x0 + 4 * cell_w) / 2.0, caption_y,
            caption_str, ha='center', va='top', fontsize=10.5, fontfamily='Times New Roman', color='#0F172A')

    ax.set_xlim(0.0, test_x0 + 4 * cell_w + 0.5)
    ax.set_ylim(caption_y - 0.35, table_top + 0.7)
    ax.axis('off')
    
    plt.subplots_adjust(left=0.01, right=0.99, top=0.98, bottom=0.02)
    
    base, _ = os.path.splitext(output_path)
    png_out = f"{base}.png"
    pdf_out = f"{base}.pdf"
    plt.savefig(png_out, dpi=300, bbox_inches='tight', facecolor='#FFFFFF', edgecolor='none')
    plt.savefig(pdf_out, dpi=600, bbox_inches='tight', facecolor='#FFFFFF', edgecolor='none')
    plt.close()
    print(f"[Done] Generated Model Evaluation Heatmap Table: {png_out}, {pdf_out}")
    return png_out, pdf_out

if __name__ == '__main__':
    demo_models = [
        {
            'task': 'Task A',
            'name': 'Model_TL',
            'train': {'MAE': 0.0023, 'RMSE': 0.0037, 'MAPE': 0.23, 'R2': 0.89},
            'test':  {'MAE': 0.0026, 'RMSE': 0.0040, 'MAPE': 0.44, 'R2': 0.91},
            'is_best_test_r2': True
        },
        {
            'task': 'Task A',
            'name': 'Model_MLP1',
            'train': {'MAE': 0.0026, 'RMSE': 0.0043, 'MAPE': 0.35, 'R2': 0.83},
            'test':  {'MAE': 0.0034, 'RMSE': 0.0062, 'MAPE': 0.67, 'R2': 0.77},
            'is_best_test_r2': False
        },
        {
            'task': 'Task B',
            'name': 'Model_NLP_TL',
            'train': {'MAE': 0.40, 'RMSE': 0.64, 'MAPE': 0.039, 'R2': 0.98},
            'test':  {'MAE': 0.66, 'RMSE': 1.35, 'MAPE': 0.064, 'R2': 0.90},
            'is_best_test_r2': True
        },
        {
            'task': 'Task B',
            'name': 'Model_MLP2',
            'train': {'MAE': 0.34, 'RMSE': 0.53, 'MAPE': 0.050, 'R2': 0.99},
            'test':  {'MAE': 0.69, 'RMSE': 1.52, 'MAPE': 0.050, 'R2': 0.85},
            'is_best_test_r2': False
        }
    ]
    plot_evaluation_heatmap_table(demo_models, output_path="plot_model_evaluation_heatmap_table_demo.png")

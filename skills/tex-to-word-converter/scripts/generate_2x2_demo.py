import os
import matplotlib.pyplot as plt
import numpy as np
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

out_dir = r"C:\JunzanLi_project\skills_mcp\skills\tex-to-word-converter\demo_output"
os.makedirs(out_dir, exist_ok=True)

# 1. Generate 4 publication-grade academic subplots (Nature/Elsevier style)
plt.style.use('seaborn-v0_8-paper' if 'seaborn-v0_8-paper' in plt.style.available else 'default')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial']
plt.rcParams['axes.edgecolor'] = '#333333'
plt.rcParams['axes.linewidth'] = 0.8

# Subplot (a): Stress-Strain Curve (Geotechnical / Concrete)
fig, ax = plt.subplots(figsize=(3.4, 2.5), dpi=300)
strain = np.linspace(0, 0.05, 100)
for p, col, label in [(100, '#1f77b4', r'$\sigma_3 = 100\ \mathrm{kPa}$'), 
                      (200, '#ff7f0e', r'$\sigma_3 = 200\ \mathrm{kPa}$'),
                      (300, '#2ca02c', r'$\sigma_3 = 300\ \mathrm{kPa}$')]:
    q = (strain / (0.005 + 0.001 * strain)) * (p / 100)**0.5
    ax.plot(strain * 100, q, color=col, lw=1.8, label=label)
ax.set_xlabel('Axial Strain $\\varepsilon_a$ (%)', fontsize=9)
ax.set_ylabel('Deviatoric Stress $q$ (kPa)', fontsize=9)
ax.legend(fontsize=7, frameon=False)
ax.grid(True, ls='--', alpha=0.4)
fig.tight_layout()
fig_a = os.path.join(out_dir, "sub_a.png")
fig.savefig(fig_a, dpi=300)
plt.close(fig)

# Subplot (b): Pore Water Pressure
fig, ax = plt.subplots(figsize=(3.4, 2.5), dpi=300)
u = 80 * (1 - np.exp(-strain * 60))
ax.plot(strain * 100, u, color='#d62728', lw=1.8, label='Measured $u$')
ax.plot(strain * 100, u * 0.92, color='#9467bd', ls='--', lw=1.8, label='FEM Prediction')
ax.set_xlabel('Axial Strain $\\varepsilon_a$ (%)', fontsize=9)
ax.set_ylabel('Excess Pore Pressure $\\Delta u$ (kPa)', fontsize=9)
ax.legend(fontsize=7, frameon=False)
ax.grid(True, ls='--', alpha=0.4)
fig.tight_layout()
fig_b = os.path.join(out_dir, "sub_b.png")
fig.savefig(fig_b, dpi=300)
plt.close(fig)

# Subplot (c): Yield Surface Evolution
fig, ax = plt.subplots(figsize=(3.4, 2.5), dpi=300)
p_vals = np.linspace(0, 400, 100)
for r, col, ls in [(1.0, '#333333', '-'), (1.2, '#1f77b4', '--'), (1.4, '#2ca02c', ':')]:
    q_yield = 1.1 * p_vals * (1 - (p_vals / (350 * r))**0.8)
    q_yield[q_yield < 0] = 0
    ax.plot(p_vals, q_yield, color=col, ls=ls, lw=1.8, label=f'Hardening $\\alpha={r}$')
ax.set_xlabel('Mean Effective Stress $p\'$ (kPa)', fontsize=9)
ax.set_ylabel('Deviatoric Stress $q$ (kPa)', fontsize=9)
ax.legend(fontsize=7, frameon=False)
ax.grid(True, ls='--', alpha=0.4)
fig.tight_layout()
fig_c = os.path.join(out_dir, "sub_c.png")
fig.savefig(fig_c, dpi=300)
plt.close(fig)

# Subplot (d): Field Monitoring Displacement
fig, ax = plt.subplots(figsize=(3.4, 2.5), dpi=300)
time_days = np.arange(1, 31)
disp = 15 * np.log10(time_days) + np.random.normal(0, 0.4, 30)
ax.scatter(time_days, disp, color='#e377c2', s=18, label='Sensor S-01')
ax.plot(time_days, 15 * np.log10(time_days), color='#17becf', lw=1.8, label='Digital Twin Fit')
ax.set_xlabel('Elapsed Time (Days)', fontsize=9)
ax.set_ylabel('Cumulative Displacement (mm)', fontsize=9)
ax.legend(fontsize=7, frameon=False)
ax.grid(True, ls='--', alpha=0.4)
fig.tight_layout()
fig_d = os.path.join(out_dir, "sub_d.png")
fig.savefig(fig_d, dpi=300)
plt.close(fig)

print("[OK] 4 Subplots generated successfully.")

# 2. Build Publication-grade Word Document with 2x2 Subfigure Table
doc = Document()

# Set standard margins (1 inch)
for section in doc.sections:
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.left_margin = Inches(1.0)
    section.right_margin = Inches(1.0)

# Title & Headings
title_p = doc.add_paragraph()
r_title = title_p.add_run("Demonstration of Publication-Grade 2×2 Subfigure Layout in Word")
r_title.font.name = "Times New Roman"
r_title.font.size = Pt(16)
r_title.font.bold = True
title_p.paragraph_format.space_after = Pt(12)

sec_p = doc.add_paragraph()
r_sec = sec_p.add_run("1. Experimental & Numerical Verification")
r_sec.font.name = "Times New Roman"
r_sec.font.size = Pt(13)
r_sec.font.bold = True
sec_p.paragraph_format.space_before = Pt(8)
sec_p.paragraph_format.space_after = Pt(6)

body_p = doc.add_paragraph()
r_body = body_p.add_run(
    "To validate the constitutive response and field adaptability of the proposed framework, "
    "triaxial shear behaviors under different confining pressures, excess pore pressure dissipation, "
    "yield surface evolution, and long-term digital twin monitoring data were comprehensively evaluated. "
    "As illustrated in Figure 1, the numerical simulations show strict monotonicity and excellent consistency with physical measurements."
)
r_body.font.name = "Times New Roman"
r_body.font.size = Pt(10.5)
body_p.paragraph_format.line_spacing = 1.25
body_p.paragraph_format.space_after = Pt(10)
body_p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

# 3. Create Borderless 2x2 Grid Table for Subfigures
# We use 4 rows: Row 0 = [Img A, Img B], Row 1 = [Label A, Label B], Row 2 = [Img C, Img D], Row 3 = [Label C, Label D]
table = doc.add_table(rows=4, cols=2)
table.alignment = WD_TABLE_ALIGNMENT.CENTER

def remove_borders(cell):
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(r'''
        <w:tcBorders xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
            <w:top w:val="none"/>
            <w:left w:val="none"/>
            <w:bottom w:val="none"/>
            <w:right w:val="none"/>
            <w:insideH w:val="none"/>
            <w:insideV w:val="none"/>
        </w:tcBorders>
    ''')
    tcPr.append(tcBorders)

# Width: each column ~3.15 inches (total 6.3 inches fits standard 6.5 inch text width)
col_widths = [Inches(3.15), Inches(3.15)]
for row in table.rows:
    for idx, width in enumerate(col_widths):
        row.cells[idx].width = width
        remove_borders(row.cells[idx])

# Cell (0, 0): Img A
p00 = table.rows[0].cells[0].paragraphs[0]
p00.alignment = WD_ALIGN_PARAGRAPH.CENTER
p00.paragraph_format.space_after = Pt(2)
p00.add_run().add_picture(fig_a, width=Inches(3.05))

# Cell (0, 1): Img B
p01 = table.rows[0].cells[1].paragraphs[0]
p01.alignment = WD_ALIGN_PARAGRAPH.CENTER
p01.paragraph_format.space_after = Pt(2)
p01.add_run().add_picture(fig_b, width=Inches(3.05))

# Cell (1, 0): Label A
p10 = table.rows[1].cells[0].paragraphs[0]
p10.alignment = WD_ALIGN_PARAGRAPH.CENTER
p10.paragraph_format.space_before = Pt(2)
p10.paragraph_format.space_after = Pt(8)
r_la = p10.add_run("(a) Stress-strain response at different confining stresses")
r_la.font.name = "Times New Roman"
r_la.font.size = Pt(9.5)
r_la.font.italic = False

# Cell (1, 1): Label B
p11 = table.rows[1].cells[1].paragraphs[0]
p11.alignment = WD_ALIGN_PARAGRAPH.CENTER
p11.paragraph_format.space_before = Pt(2)
p11.paragraph_format.space_after = Pt(8)
r_lb = p11.add_run("(b) Excess pore pressure generation and dissipation")
r_lb.font.name = "Times New Roman"
r_lb.font.size = Pt(9.5)

# Cell (2, 0): Img C
p20 = table.rows[2].cells[0].paragraphs[0]
p20.alignment = WD_ALIGN_PARAGRAPH.CENTER
p20.paragraph_format.space_after = Pt(2)
p20.add_run().add_picture(fig_c, width=Inches(3.05))

# Cell (2, 1): Img D
p21 = table.rows[2].cells[1].paragraphs[0]
p21.alignment = WD_ALIGN_PARAGRAPH.CENTER
p21.paragraph_format.space_after = Pt(2)
p21.add_run().add_picture(fig_d, width=Inches(3.05))

# Cell (3, 0): Label C
p30 = table.rows[3].cells[0].paragraphs[0]
p30.alignment = WD_ALIGN_PARAGRAPH.CENTER
p30.paragraph_format.space_before = Pt(2)
p30.paragraph_format.space_after = Pt(6)
r_lc = p30.add_run("(c) Kinematic yield surface contraction and expansion")
r_lc.font.name = "Times New Roman"
r_lc.font.size = Pt(9.5)

# Cell (3, 1): Label D
p31 = table.rows[3].cells[1].paragraphs[0]
p31.alignment = WD_ALIGN_PARAGRAPH.CENTER
p31.paragraph_format.space_before = Pt(2)
p31.paragraph_format.space_after = Pt(6)
r_ld = p31.add_run("(d) Real-time displacement tracking from digital twin sensor")
r_ld.font.name = "Times New Roman"
r_ld.font.size = Pt(9.5)

# 4. Main Figure Caption
cap_p = doc.add_paragraph()
cap_p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
cap_p.paragraph_format.space_before = Pt(6)
cap_p.paragraph_format.space_after = Pt(12)

r_fig_bold = cap_p.add_run("Fig. 1. ")
r_fig_bold.font.name = "Times New Roman"
r_fig_bold.font.size = Pt(9.5)
r_fig_bold.font.bold = True

r_fig_text = cap_p.add_run(
    "Multi-dimensional experimental and numerical validation of geotechnical behavior: "
    "(a) Deviatoric stress vs. axial strain curves; "
    "(b) Comparison between measured and predicted excess pore water pressures; "
    "(c) Yield surface locus under different hardening stages; "
    "(d) Field sensor displacement evolution versus digital twin predictions."
)
r_fig_text.font.name = "Times New Roman"
r_fig_text.font.size = Pt(9.5)

# Save Document
doc_path = os.path.join(out_dir, "Publication_Grade_2x2_Subfigures_Demo.docx")
doc.save(doc_path)
print(f"[SUCCESS] Demo Word document generated at: {doc_path}")

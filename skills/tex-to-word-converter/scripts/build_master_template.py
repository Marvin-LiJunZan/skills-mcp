"""
Generate Master Publication-Grade Word Template & Comprehensive Showcase Document.
Injects real active Zotero CSL fields, perfect bookmark scopes, three-line tables, and 2x2 subfigures.
"""
import os
import json
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

out_dir = r"C:\JunzanLi_project\skills_mcp\skills\tex-to-word-converter\demo_output"
os.makedirs(out_dir, exist_ok=True)
master_doc_path = os.path.join(out_dir, "Publication_Grade_Master_Template.docx")

doc = Document()

# Page Margins: Standard 1 inch (2.54 cm)
for section in doc.sections:
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.left_margin = Inches(1.0)
    section.right_margin = Inches(1.0)

# 1. Styles
styles = doc.styles
def get_or_add_style(name, style_type):
    if name in styles: return styles[name]
    return styles.add_style(name, style_type)

normal = styles['Normal']
normal.font.name = 'Times New Roman'
normal.font.size = Pt(10.5)
normal.font.color.rgb = RGBColor(0, 0, 0)
normal.paragraph_format.line_spacing = 1.25
normal.paragraph_format.space_after = Pt(6)
normal.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

s_title = get_or_add_style('Paper Title', WD_STYLE_TYPE.PARAGRAPH)
s_title.font.name = 'Times New Roman'
s_title.font.size = Pt(18)
s_title.font.bold = True
s_title.paragraph_format.space_after = Pt(12)

s_author = get_or_add_style('Paper Author', WD_STYLE_TYPE.PARAGRAPH)
s_author.font.name = 'Times New Roman'
s_author.font.size = Pt(11)
s_author.paragraph_format.space_after = Pt(4)

s_affil = get_or_add_style('Paper Affiliation', WD_STYLE_TYPE.PARAGRAPH)
s_affil.font.name = 'Times New Roman'
s_affil.font.size = Pt(9.0)
s_affil.font.italic = True
s_affil.paragraph_format.space_after = Pt(12)

s_h1 = get_or_add_style('Heading 1', WD_STYLE_TYPE.PARAGRAPH)
s_h1.font.name = 'Times New Roman'
s_h1.font.size = Pt(13)
s_h1.font.bold = True
s_h1.paragraph_format.space_before = Pt(12)
s_h1.paragraph_format.space_after = Pt(4)

s_h2 = get_or_add_style('Heading 2', WD_STYLE_TYPE.PARAGRAPH)
s_h2.font.name = 'Times New Roman'
s_h2.font.size = Pt(11.5)
s_h2.font.bold = True
s_h2.font.italic = True
s_h2.paragraph_format.space_before = Pt(8)
s_h2.paragraph_format.space_after = Pt(3)

s_thdr = get_or_add_style('Table Header', WD_STYLE_TYPE.PARAGRAPH)
s_thdr.font.name = 'Times New Roman'
s_thdr.font.size = Pt(9.5)
s_thdr.font.bold = False
s_thdr.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
s_thdr.paragraph_format.space_before = Pt(3)
s_thdr.paragraph_format.space_after = Pt(3)
s_thdr.paragraph_format.line_spacing = 1.05

s_tbdy = get_or_add_style('Table Body', WD_STYLE_TYPE.PARAGRAPH)
s_tbdy.font.name = 'Times New Roman'
s_tbdy.font.size = Pt(9.0)
s_tbdy.font.bold = False
s_tbdy.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
s_tbdy.paragraph_format.space_before = Pt(2.5)
s_tbdy.paragraph_format.space_after = Pt(2.5)
s_tbdy.paragraph_format.line_spacing = 1.0

s_tnote = get_or_add_style('Table Note', WD_STYLE_TYPE.PARAGRAPH)
s_tnote.font.name = 'Times New Roman'
s_tnote.font.size = Pt(8.5)
s_tnote.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
s_tnote.paragraph_format.space_before = Pt(3)
s_tnote.paragraph_format.space_after = Pt(10)

def add_xml_run(paragraph, text, italic=False, sub=False, sup=False, bold=False, font_size=21):
    rPr = [f'<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:sz w:val="{font_size}"/>']
    if bold: rPr.append('<w:b/>')
    if italic: rPr.append('<w:i/>')
    if sub: rPr.append('<w:vertAlign w:val="subscript"/>')
    elif sup: rPr.append('<w:vertAlign w:val="superscript"/>')
    rPr_str = "".join(rPr)
    r_elm = parse_xml(f'<w:r {nsdecls("w")}><w:rPr>{rPr_str}</w:rPr><w:t xml:space="preserve">{text}</w:t></w:r>')
    paragraph._p.append(r_elm)

def add_field(paragraph, instr_text, display_text, font_size=21, bold=False):
    fld = parse_xml(f'<w:fldSimple {nsdecls("w")} w:instr="{instr_text}"/>')
    b_xml = '<w:b/>' if bold else ''
    r = parse_xml(f'<w:r {nsdecls("w")}><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>{b_xml}<w:sz w:val="{font_size}"/></w:rPr><w:t>{display_text}</w:t></w:r>')
    fld.append(r)
    paragraph._p.append(fld)

def add_zotero_csl_citation(paragraph, num, key="ITEM"):
    # Escape quotes inside XML attribute
    csl_dict = {
        "citationID": f"csl_{num}",
        "properties": {"formattedCitation": f"[{num}]", "plainCitation": f"[{num}]"},
        "citationItems": [{"id": f"ref_{num}", "uris": [f"http://zotero.org/users/local/items/{key}_{num}"]}]
    }
    json_str = json.dumps(csl_dict).replace('"', '&quot;')
    instr = f"ADDIN ZOTERO_ITEM CSL_CITATION {json_str}"
    fld = parse_xml(f'<w:fldSimple {nsdecls("w")} w:instr="{instr}"/>')
    r = parse_xml(f'<w:r {nsdecls("w")}><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:sz w:val="21"/></w:rPr><w:t>[{num}]</w:t></w:r>')
    fld.append(r)
    paragraph._p.append(fld)

def set_cell_border(cell, **kwargs):
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = tcPr.first_child_found_in("w:tcBorders")
    if tcBorders is None:
        tcBorders = OxmlElement('w:tcBorders')
        tcPr.append(tcBorders)
    for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        edge_data = kwargs.get(edge)
        if edge_data:
            tag = f'w:{edge}'
            element = tcBorders.find(qn(tag))
            if element is None:
                element = OxmlElement(tag)
                tcBorders.append(element)
            for key, val in edge_data.items():
                element.set(qn(f'w:{key}'), str(val))

# Title & Authors
p_title = doc.add_paragraph(style='Paper Title')
p_title.add_run("Deep Learning-Driven Digital Twin and Multi-Scale Constitutive Modeling for Geomaterials and Structural Infrastructure")

p_author = doc.add_paragraph(style='Paper Author')
p_author.add_run("Junzan Li")
add_xml_run(p_author, "a,b,*", sup=True)
p_author.add_run(", Senior Academician")
add_xml_run(p_author, "a", sup=True)

p_affil = doc.add_paragraph(style='Paper Affiliation')
add_xml_run(p_affil, "a ", sup=True)
p_affil.add_run("School of Civil and Transportation Engineering, China\n")
add_xml_run(p_affil, "b ", sup=True)
p_affil.add_run("State Key Laboratory for Disaster Prevention and Smart Infrastructure, China\n* Corresponding author.")

p_abs = doc.add_paragraph()
r_abs_t = p_abs.add_run("Abstract: ")
r_abs_t.bold = True
p_abs.add_run(
    "Accurate prediction of progressive deformation in complex geomaterials remains an open scientific challenge. "
    "This master template establishes the international standard for automated LaTeX-to-Word academic publishing. "
    "We rigorously demonstrate the isolation of physical variables from Office Math boxes, the seamless invocation of MathType OLE objects, "
    "the generation of unbolded publication three-line tables with anti-split pagination defense, and the physical caption-fused 2×2 subfigure alignment. "
    "Dynamic cross-referencing via Word SEQ and REF fields is embedded to guarantee deterministic number re-indexing."
)

p_kw = doc.add_paragraph()
r_kw_t = p_kw.add_run("Keywords: ")
r_kw_t.bold = True
p_kw.add_run("Digital twin; Three-line table; Constitutive modeling; MathType equation; Subfigure layout; Geomechanics")
p_kw.paragraph_format.space_after = Pt(16)

# Section 1: Intro with 26 Zotero CSL citations
p_s1 = doc.add_paragraph("1. Mathematical Formulation & Literature Background", style='Heading 1')

p_txt1 = doc.add_paragraph()
p_txt1.add_run("Geotechnical infrastructure failure monitoring has advanced rapidly over the past decade ")
add_zotero_csl_citation(p_txt1, 1)
p_txt1.add_run(", with slope deformation and landslide stabilization studied through diverse numerical approaches ")
add_zotero_csl_citation(p_txt1, 2)
p_txt1.add_run(". Classical limit equilibrium and finite-element formulations have been extensively validated across field sites ")
for i in range(3, 10):
    add_zotero_csl_citation(p_txt1, i)
    p_txt1.add_run(" ")

p_txt1_b = doc.add_paragraph()
p_txt1_b.add_run("Constitutive developments in multi-scale geomechanics and unsaturated soil mechanics have provided essential physical baselines ")
for i in range(10, 18):
    add_zotero_csl_citation(p_txt1_b, i)
    p_txt1_b.add_run(" ")

p_txt1_c = doc.add_paragraph()
p_txt1_c.add_run("According to the ISO 80000-2 and IUPAP international conventions, physical variables must be italicized while units and chemical formulas remain upright. Under initial consolidation, the vertical effective stress is denoted by ")
add_xml_run(p_txt1_c, "σ", italic=True)
add_xml_run(p_txt1_c, "v0", sub=True)
add_xml_run(p_txt1_c, "′", sup=True)
p_txt1_c.add_run(", volumetric strain is ")
add_xml_run(p_txt1_c, "ε", italic=True)
add_xml_run(p_txt1_c, "vol", sub=True)
p_txt1_c.add_run(", and coefficient of earth pressure is ")
add_xml_run(p_txt1_c, "K", italic=True)
add_xml_run(p_txt1_c, "0,nc", sub=True)
p_txt1_c.add_run(". During multi-stage triaxial shear loading, the major principal stress satisfies ")
add_xml_run(p_txt1_c, "σ", italic=True)
add_xml_run(p_txt1_c, "1", sub=True)
add_xml_run(p_txt1_c, "2", sup=True)
p_txt1_c.add_run(" = 450 kPa")
add_xml_run(p_txt1_c, "2", sup=True)
p_txt1_c.add_run(", undrained shear strength achieves ")
add_xml_run(p_txt1_c, "c", italic=True)
add_xml_run(p_txt1_c, "u", sub=True)
add_xml_run(p_txt1_c, "(t)", sup=True)
p_txt1_c.add_run(", and the slope factor of safety reaches ")
add_xml_run(p_txt1_c, "F", italic=True)
add_xml_run(p_txt1_c, "s", italic=True, sub=True)
add_xml_run(p_txt1_c, "min", sup=True)
p_txt1_c.add_run(" = 1.34 at an ambient temperature of 20 °C. The specimen contains Fe")
add_xml_run(p_txt1_c, "2", sub=True)
p_txt1_c.add_run("O")
add_xml_run(p_txt1_c, "3", sub=True)
p_txt1_c.add_run(" with dry density of 1.95 g/cm")
add_xml_run(p_txt1_c, "3", sup=True)
p_txt1_c.add_run(", matching empirical observations in recent literature ")
for i in range(18, 27):
    add_zotero_csl_citation(p_txt1_c, i)
    p_txt1_c.add_run(" ")

# Display Equation with SEQ Equation
p_eq = doc.add_paragraph()
p_eq.paragraph_format.space_before = Pt(6)
p_eq.paragraph_format.space_after = Pt(6)
p_eq.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
r_eq_body = p_eq.add_run("                                          τf = c′ + (σn − u) tan φ′                                            ")
r_eq_body.font.name = "Times New Roman"
r_eq_body.font.italic = True
p_eq.add_run("(")
add_field(p_eq, "SEQ Equation \\* ARABIC", "1")
p_eq.add_run(")")

# Section 2: Table
p_s2 = doc.add_paragraph("2. Calibrated Physical Properties & Three-Line Table", style='Heading 1')

p_txt2 = doc.add_paragraph()
p_txt2.add_run("The physical state parameters and calibrated constitutive variables are summarized in ")
add_field(p_txt2, "REF _RefTable1 \\h", "Table 1")
p_txt2.add_run(". The table adheres to the strict booktabs criteria: 1.5 pt top/bottom rules, 0.75 pt mid rule, unbolded header text, dedicated styles, and pagination cantSplit defenses.")

# Table Caption with ISOLATED Bookmark Scope (wraps label & number only)
p_tcap = doc.add_paragraph()
p_tcap.paragraph_format.space_before = Pt(8)
p_tcap.paragraph_format.space_after = Pt(4)
p_tcap._p.append(parse_xml(f'<w:bookmarkStart {nsdecls("w")} w:id="201" w:name="_RefTable1"/>'))
p_tcap.add_run("Table ").bold = True
add_field(p_tcap, "SEQ Table \\* ARABIC", "1", bold=True)
p_tcap._p.append(parse_xml(f'<w:bookmarkEnd {nsdecls("w")} w:id="201"/>'))
p_tcap.add_run(". Calibrated geotechnical physical and mechanical properties of engineered soil specimens.").bold = True

headers = [
    "Specimen ID", "Moisture w\n(%)", "Dry Density ρd\n(g/cm³)", 
    "Cohesion c′\n(kPa)", "Friction Angle φ′\n(°)", "Modulus E0\n(MPa)", "Permeability k\n(×10⁻⁷ cm/s)"
]
data = [
    ["SP-01", "12.4 ± 0.3", "1.78", "28.5 ± 1.2", "24.2 ± 0.5", "45.8 ± 2.1", "3.42 ± 0.15"],
    ["SP-02", "11.8 ± 0.2", "1.85", "34.2 ± 1.5", "28.7 ± 0.6", "68.4 ± 3.4", "2.85 ± 0.11"],
    ["SP-03", "10.5 ± 0.4", "1.96", "42.8 ± 1.8", "33.5 ± 0.8", "112.6 ± 5.2", "1.96 ± 0.08"],
    ["SP-04", "9.2 ± 0.3", "2.08", "51.6 ± 2.1", "38.9 ± 1.1", "185.3 ± 7.8", "1.24 ± 0.06"],
    ["SP-05", "8.1 ± 0.2", "2.19", "46.3 ± 2.4", "43.2 ± 1.3", "264.0 ± 9.5", "0.88 ± 0.04"],
]

tbl = doc.add_table(rows=len(data) + 1, cols=len(headers))
tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
tbl.rows[0]._tr.get_or_add_trPr().append(OxmlElement('w:tblHeader'))

for c_idx, h_text in enumerate(headers):
    cell = tbl.rows[0].cells[c_idx]
    p = cell.paragraphs[0]
    p.style = doc.styles['Table Header']
    p.add_run(h_text)
    set_cell_border(cell,
                    top={'val': 'single', 'sz': '12', 'color': '000000'},
                    bottom={'val': 'single', 'sz': '6', 'color': '000000'},
                    left={'val': 'none'}, right={'val': 'none'},
                    insideH={'val': 'none'}, insideV={'val': 'none'})

for r_idx, r_data in enumerate(data, start=1):
    row = tbl.rows[r_idx]
    row._tr.get_or_add_trPr().append(OxmlElement('w:cantSplit'))
    is_last = (r_idx == len(data))
    for c_idx, val in enumerate(r_data):
        cell = row.cells[c_idx]
        p = cell.paragraphs[0]
        p.style = doc.styles['Table Body']
        p.add_run(val)
        if is_last:
            set_cell_border(cell,
                            top={'val': 'none'},
                            bottom={'val': 'single', 'sz': '12', 'color': '000000'},
                            left={'val': 'none'}, right={'val': 'none'},
                            insideH={'val': 'none'}, insideV={'val': 'none'})
        else:
            set_cell_border(cell,
                            top={'val': 'none'}, bottom={'val': 'none'},
                            left={'val': 'none'}, right={'val': 'none'},
                            insideH={'val': 'none'}, insideV={'val': 'none'})

p_tnote = doc.add_paragraph(style='Table Note')
r_nl = p_tnote.add_run("Note: ")
r_nl.font.italic = True
p_tnote.add_run("Values indicate mean ± standard deviation from triaxial shear experiments; all shear strength parameters are determined at peak deviatoric stress.")

# Section 3: Subfigures
p_s3 = doc.add_paragraph("3. Multi-Panel Experimental Results (2×2 Subfigures)", style='Heading 1')

p_txt3 = doc.add_paragraph()
p_txt3.add_run("Figure 1 demonstrates the multi-scale physical and numerical verification. As referenced in ")
add_field(p_txt3, "REF _RefFig1 \\h", "Fig. 1")
p_txt3.add_run(", all four sub-panels are aligned within a borderless container, and the caption is fused into the bottom merged cell.")

fig_a = os.path.join(out_dir, "sub_a.png")
fig_b = os.path.join(out_dir, "sub_b.png")
fig_c = os.path.join(out_dir, "sub_c.png")
fig_d = os.path.join(out_dir, "sub_d.png")

t_fig = doc.add_table(rows=5, cols=2)
t_fig.alignment = WD_TABLE_ALIGNMENT.CENTER

def remove_borders(cell):
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(f'''
        <w:tcBorders {nsdecls("w")}>
            <w:top w:val="none"/><w:left w:val="none"/><w:bottom w:val="none"/><w:right w:val="none"/>
            <w:insideH w:val="none"/><w:insideV w:val="none"/>
        </w:tcBorders>
    ''')
    tcPr.append(tcBorders)

for row in t_fig.rows:
    for c in row.cells:
        remove_borders(c)

col_w = Inches(3.15)
for row in t_fig.rows:
    row.cells[0].width = col_w
    row.cells[1].width = col_w

if os.path.exists(fig_a):
    t_fig.rows[0].cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    t_fig.rows[0].cells[0].paragraphs[0].add_run().add_picture(fig_a, width=Inches(3.05))
if os.path.exists(fig_b):
    t_fig.rows[0].cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    t_fig.rows[0].cells[1].paragraphs[0].add_run().add_picture(fig_b, width=Inches(3.05))

p_la = t_fig.rows[1].cells[0].paragraphs[0]
p_la.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_la.paragraph_format.space_before = Pt(2)
p_la.paragraph_format.space_after = Pt(8)
r_la = p_la.add_run("(a) Triaxial deviatoric stress response curves")
r_la.font.name = "Times New Roman"
r_la.font.size = Pt(9.5)

p_lb = t_fig.rows[1].cells[1].paragraphs[0]
p_lb.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_lb.paragraph_format.space_before = Pt(2)
p_lb.paragraph_format.space_after = Pt(8)
r_lb = p_lb.add_run("(b) Excess pore water pressure evolution")
r_lb.font.name = "Times New Roman"
r_lb.font.size = Pt(9.5)

if os.path.exists(fig_c):
    t_fig.rows[2].cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    t_fig.rows[2].cells[0].paragraphs[0].add_run().add_picture(fig_c, width=Inches(3.05))
if os.path.exists(fig_d):
    t_fig.rows[2].cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    t_fig.rows[2].cells[1].paragraphs[0].add_run().add_picture(fig_d, width=Inches(3.05))

p_lc = t_fig.rows[3].cells[0].paragraphs[0]
p_lc.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_lc.paragraph_format.space_before = Pt(2)
p_lc.paragraph_format.space_after = Pt(6)
r_lc = p_lc.add_run("(c) Yield surface locus under hardening stages")
r_lc.font.name = "Times New Roman"
r_lc.font.size = Pt(9.5)

p_ld = t_fig.rows[3].cells[1].paragraphs[0]
p_ld.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_ld.paragraph_format.space_before = Pt(2)
p_ld.paragraph_format.space_after = Pt(6)
r_ld = p_ld.add_run("(d) Real-time digital twin displacement tracking")
r_ld.font.name = "Times New Roman"
r_ld.font.size = Pt(9.5)

# Fused Caption with ISOLATED Bookmark Scope
cell_cap = t_fig.rows[4].cells[0]
tcPr_cap = cell_cap._tc.get_or_add_tcPr()
tcPr_cap.append(parse_xml(f'<w:gridSpan {nsdecls("w")} w:val="2"/>'))
p_fcap = cell_cap.paragraphs[0]
p_fcap.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
p_fcap.paragraph_format.space_before = Pt(6)
p_fcap.paragraph_format.space_after = Pt(12)

# Bookmark _RefFig1 strictly wraps 'Fig. 1' only
p_fcap._p.append(parse_xml(f'<w:bookmarkStart {nsdecls("w")} w:id="301" w:name="_RefFig1"/>'))
p_fcap.add_run("Fig. ").bold = True
add_field(p_fcap, "SEQ Fig. \\* ARABIC", "1", font_size=19, bold=True)
p_fcap._p.append(parse_xml(f'<w:bookmarkEnd {nsdecls("w")} w:id="301"/>'))

r_fcap_t = p_fcap.add_run(". Multi-dimensional constitutive experimental and numerical validation of geotechnical behavior: (a) Deviatoric stress vs. axial strain curves; (b) Measured and predicted excess pore water pressures; (c) Yield locus expansion; (d) Sensor displacement evolution.")
r_fcap_t.font.name = "Times New Roman"
r_fcap_t.font.size = Pt(9.5)

# References Section
p_s4 = doc.add_paragraph("References", style='Heading 1')

for i in range(1, 27):
    p_ref = doc.add_paragraph()
    p_ref.paragraph_format.line_spacing = 1.15
    p_ref.paragraph_format.space_after = Pt(4)
    p_ref.paragraph_format.left_indent = Inches(0.25)
    p_ref.paragraph_format.first_line_indent = Inches(-0.25)
    p_ref.add_run(f"[{i}] Author, A., Coauthor, B. (2024). Groundbreaking geotechnical and constitutive modeling investigations in top-tier civil journals. Computers and Geotechnics, 168: 106{i:03d}. https://doi.org/10.1016/j.compgeo.2024.106{i:03d}")

doc.save(master_doc_path)
print(f"[SUCCESS] Re-generated master template with 26 active Zotero CSL fields: {master_doc_path}")


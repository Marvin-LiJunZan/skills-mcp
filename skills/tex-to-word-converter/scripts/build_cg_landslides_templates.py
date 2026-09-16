"""
Generate specialized DOCX templates for:
1. computers_and_geotechnics.docx (Elsevier, 1.5 line spacing, Times New Roman 10.5pt, line numbers friendly)
2. landslides.docx (Springer, 1.5 line spacing, Times New Roman 11pt, Author-Date friendly)
"""
import os
import docx
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

def configure_journal_doc(base_path, out_path, font_name="Times New Roman", line_spacing=1.5, body_pt=11.0):
    doc = Document(base_path)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
    styles = doc.styles
    normal = styles['Normal']
    normal.font.name = font_name
    normal.font.size = Pt(body_pt)
    normal.font.color.rgb = RGBColor(0, 0, 0)
    normal.paragraph_format.line_spacing = line_spacing
    normal.paragraph_format.space_after = Pt(4)
    normal.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    if 'Heading 1' in styles:
        h1 = styles['Heading 1']
        h1.font.name = font_name
        h1.font.size = Pt(13)
        h1.font.bold = True
        h1.font.color.rgb = RGBColor(0, 0, 0)
        h1.paragraph_format.space_before = Pt(12)
        h1.paragraph_format.space_after = Pt(4)

    if 'Heading 2' in styles:
        h2 = styles['Heading 2']
        h2.font.name = font_name
        h2.font.size = Pt(11.5)
        h2.font.bold = True
        h2.font.italic = True
        h2.font.color.rgb = RGBColor(0, 0, 0)
        h2.paragraph_format.space_before = Pt(8)
        h2.paragraph_format.space_after = Pt(3)

    if 'Caption' in styles:
        cap = styles['Caption']
        cap.font.name = font_name
        cap.font.size = Pt(9.5)
        cap.font.bold = True
        cap.font.color.rgb = RGBColor(0, 0, 0)
        cap.paragraph_format.space_before = Pt(6)
        cap.paragraph_format.space_after = Pt(6)
        cap.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.save(out_path)
    print(f"[OK] Saved: {out_path}")

base = r"C:\JunzanLi_project\skills_mcp\skills\tex-to-word-converter\templates\default_reference.docx"
t_dir = r"C:\JunzanLi_project\skills_mcp\skills\tex-to-word-converter\templates"

configure_journal_doc(base, os.path.join(t_dir, "computers_and_geotechnics.docx"), font_name="Times New Roman", line_spacing=1.5, body_pt=10.5)
configure_journal_doc(base, os.path.join(t_dir, "landslides.docx"), font_name="Times New Roman", line_spacing=1.5, body_pt=11.0)

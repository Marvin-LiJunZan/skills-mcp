"""
Generate specialized journal reference DOCX templates:
1. elsevier_standard.docx (Cement & Concrete, AUTCON, CBM)
2. asce_journal.docx (Civil / Structural / Computing)
3. ieee_transactions.docx (Digital Twin / Smart Infrastructure)
4. springer_nature.docx (Materials & Structures)
5. chinese_core_journal.docx (土木工程学报/建筑材料学报)
"""
import os
import shutil
import docx
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def configure_styles(doc, font_name="Times New Roman", cn_font="SimSun", line_spacing=1.15, body_pt=10.5):
    # Set document margins (1 inch standard)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
    styles = doc.styles
    
    # Normal / Body Text
    normal = styles['Normal']
    normal.font.name = font_name
    normal.font.size = Pt(body_pt)
    normal.font.color.rgb = RGBColor(0, 0, 0)
    normal.paragraph_format.line_spacing = line_spacing
    normal.paragraph_format.space_after = Pt(4)
    normal.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    # Heading 1
    if 'Heading 1' in styles:
        h1 = styles['Heading 1']
        h1.font.name = font_name
        h1.font.size = Pt(13)
        h1.font.bold = True
        h1.font.color.rgb = RGBColor(0, 0, 0)
        h1.paragraph_format.space_before = Pt(12)
        h1.paragraph_format.space_after = Pt(4)

    # Heading 2
    if 'Heading 2' in styles:
        h2 = styles['Heading 2']
        h2.font.name = font_name
        h2.font.size = Pt(11.5)
        h2.font.bold = True
        h2.font.italic = True
        h2.font.color.rgb = RGBColor(0, 0, 0)
        h2.paragraph_format.space_before = Pt(8)
        h2.paragraph_format.space_after = Pt(3)

    # Caption
    if 'Caption' in styles:
        cap = styles['Caption']
        cap.font.name = font_name
        cap.font.size = Pt(9.5)
        cap.font.bold = True
        cap.font.color.rgb = RGBColor(0, 0, 0)
        cap.paragraph_format.space_before = Pt(6)
        cap.paragraph_format.space_after = Pt(6)
        cap.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER

base_ref = r"C:\JunzanLi_project\skills_mcp\skills\tex-to-word-converter\templates\default_reference.docx"
target_dir = r"C:\JunzanLi_project\skills_mcp\skills\tex-to-word-converter\templates"

# 1. Elsevier (CCC, AUTCON, CBM)
doc1 = Document(base_ref)
configure_styles(doc1, font_name="Times New Roman", line_spacing=1.5, body_pt=10.5)
doc1.save(os.path.join(target_dir, "elsevier_standard.docx"))

# 2. ASCE (Journal of Structural Eng, Computing in Civil Eng)
doc2 = Document(base_ref)
configure_styles(doc2, font_name="Times New Roman", line_spacing=2.0, body_pt=12.0)
doc2.save(os.path.join(target_dir, "asce_journal.docx"))

# 3. IEEE Transactions (Digital Twin / Smart Infra)
doc3 = Document(base_ref)
configure_styles(doc3, font_name="Times New Roman", line_spacing=1.05, body_pt=10.0)
doc3.save(os.path.join(target_dir, "ieee_transactions.docx"))

# 4. Springer / Nature (Materials and Structures)
doc4 = Document(base_ref)
configure_styles(doc4, font_name="Arial", line_spacing=1.2, body_pt=10.0)
doc4.save(os.path.join(target_dir, "springer_nature.docx"))

# 5. Chinese Core (土木工程学报 / 建筑材料学报)
doc5 = Document(base_ref)
configure_styles(doc5, font_name="Times New Roman", cn_font="SimSun", line_spacing=1.25, body_pt=10.5)
doc5.save(os.path.join(target_dir, "chinese_core_journal.docx"))

print("[OK] Generated all 5 journal reference DOCX templates.")

"""
Subfigure Insertion Tool: Template-Referenced Table Cloning.
Solves the core problem:
Word composite figure layouts (subfigures) cannot be reliably generated from prompts alone.
Instead, this tool physically references and clones the canonical subfigure table
directly from the journal template docx (templates/subfigure_template.docx or templates/ccc_standard.docx).
Ensures:
1. Borderless cell grid with exact column widths (3.15 inches for 2 cols).
2. Sub-labels (a), (b)... centered beneath each panel.
3. Fused bottom caption using <w:gridSpan w:val="2"/> to prevent cross-page splitting.
4. Bookmark scope strictly wrapping ONLY 'Fig. {num}' (zero caption leakage).
5. Dynamic SEQ Fig. \\* ARABIC field codes.
"""
import os
import sys
import argparse
from copy import deepcopy
import docx
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls, qn

DEFAULT_TEMPLATE_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "templates", "subfigure_template.docx")
)
if not os.path.exists(DEFAULT_TEMPLATE_PATH):
    DEFAULT_TEMPLATE_PATH = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "templates", "ccc_standard.docx")
    )

def add_field(paragraph, instr_text, display_text, font_size=19, bold=True):
    fld = parse_xml(f'<w:fldSimple {nsdecls("w")} w:instr="{instr_text}"/>')
    b_xml = '<w:b/>' if bold else ''
    r = parse_xml(f'<w:r {nsdecls("w")}><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>{b_xml}<w:sz w:val="{font_size}"/></w:rPr><w:t>{display_text}</w:t></w:r>')
    fld.append(r)
    paragraph._p.append(fld)

def find_template_table(template_doc, layout="2x2"):
    """
    Locates the appropriate subfigure template table from the template document.
    """
    target_rows = 5 if layout == "2x2" else 3
    for t in template_doc.tables:
        t_xml = t._tbl.xml
        if '<w:gridSpan' in t_xml and ('SEQ Fig' in t_xml or 'Fig.' in t_xml):
            if len(t.rows) == target_rows:
                return t
    # Fallback to any table with gridSpan and SEQ Fig
    for t in template_doc.tables:
        t_xml = t._tbl.xml
        if '<w:gridSpan' in t_xml and ('SEQ Fig' in t_xml or 'Fig.' in t_xml):
            return t
    raise ValueError(f"No canonical subfigure template table found for layout {layout} in template doc.")

def insert_subfigure_from_template(target_doc, 
                                   template_path=None, 
                                   layout="2x2", 
                                   images=None, 
                                   labels=None, 
                                   fig_num=1, 
                                   caption_text="", 
                                   insert_after_p=None,
                                   img_width_in=3.05):
    """
    Clones the canonical subfigure table from the reference Word template
    and populates it with the specified images, labels, and caption.
    """
    if template_path is None or not os.path.exists(template_path):
        template_path = DEFAULT_TEMPLATE_PATH
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Subfigure reference template not found at: {template_path}")

    template_doc = Document(template_path)
    ref_table = find_template_table(template_doc, layout=layout)
    
    # Deepcopy the canonical XML table
    cloned_tbl_elem = deepcopy(ref_table._tbl)

    # Insert into target document
    if insert_after_p is not None:
        insert_after_p._p.addnext(cloned_tbl_elem)
    else:
        target_doc._body._element.append(cloned_tbl_elem)

    # Wrap as python-docx Table object
    table = docx.table.Table(cloned_tbl_elem, target_doc)

    images = images or []
    labels = labels or []

    # Mapping rows based on layout
    if layout == "2x2":
        panel_map = [
            {"img_row": 0, "img_col": 0, "lbl_row": 1, "lbl_col": 0, "default_lbl": "(a)"},
            {"img_row": 0, "img_col": 1, "lbl_row": 1, "lbl_col": 1, "default_lbl": "(b)"},
            {"img_row": 2, "img_col": 0, "lbl_row": 3, "lbl_col": 0, "default_lbl": "(c)"},
            {"img_row": 2, "img_col": 1, "lbl_row": 3, "lbl_col": 1, "default_lbl": "(d)"},
        ]
        cap_row_idx = 4
    else: # 1x2
        panel_map = [
            {"img_row": 0, "img_col": 0, "lbl_row": 1, "lbl_col": 0, "default_lbl": "(a)"},
            {"img_row": 0, "img_col": 1, "lbl_row": 1, "lbl_col": 1, "default_lbl": "(b)"},
        ]
        cap_row_idx = 2

    # Populate Panels
    for idx, panel in enumerate(panel_map):
        img_cell = table.rows[panel["img_row"]].cells[panel["img_col"]]
        lbl_cell = table.rows[panel["lbl_row"]].cells[panel["lbl_col"]]

        # Insert / Replace image
        img_p = img_cell.paragraphs[0]
        img_p.text = "" # Clear previous text/runs
        img_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        img_p.paragraph_format.space_after = Pt(2)
        if idx < len(images) and images[idx] and os.path.exists(images[idx]):
            img_p.add_run().add_picture(images[idx], width=Inches(img_width_in))

        # Insert / Replace sub-label
        lbl_p = lbl_cell.paragraphs[0]
        lbl_p.text = ""
        lbl_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        lbl_p.paragraph_format.space_before = Pt(2)
        lbl_p.paragraph_format.space_after = Pt(8)
        lbl_text = labels[idx] if idx < len(labels) and labels[idx] else panel["default_lbl"]
        r_lbl = lbl_p.add_run(lbl_text)
        r_lbl.font.name = "Times New Roman"
        r_lbl.font.size = Pt(9.5)

    # Populate Caption Row
    cap_cell = table.rows[cap_row_idx].cells[0]
    cap_p = cap_cell.paragraphs[0]
    cap_p.text = ""
    cap_p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    cap_p.paragraph_format.space_before = Pt(6)
    cap_p.paragraph_format.space_after = Pt(12)

    # Isolated Bookmark wrapping ONLY 'Fig. {fig_num}'
    bm_id = str(600 + fig_num)
    bm_name = f"_RefFig{fig_num}"
    cap_p._p.append(parse_xml(f'<w:bookmarkStart {nsdecls("w")} w:id="{bm_id}" w:name="{bm_name}"/>'))
    r_fig = cap_p.add_run("Fig. ")
    r_fig.font.name = "Times New Roman"
    r_fig.font.size = Pt(9.5)
    r_fig.font.bold = True

    add_field(cap_p, "SEQ Fig. \\* ARABIC", str(fig_num), font_size=19, bold=True)
    cap_p._p.append(parse_xml(f'<w:bookmarkEnd {nsdecls("w")} w:id="{bm_id}"/>'))

    # Rest of caption text
    if not caption_text.startswith("."):
        caption_text = ". " + caption_text.lstrip()
    r_txt = cap_p.add_run(caption_text)
    r_txt.font.name = "Times New Roman"
    r_txt.font.size = Pt(9.5)

    return table

def main():
    parser = argparse.ArgumentParser(description="Insert publication-grade subfigures into Word by cloning reference template.")
    parser.add_argument("--docx", required=True, help="Target DOCX document to modify")
    parser.add_argument("--template", default=None, help="Reference template containing canonical subfigure table")
    parser.add_argument("--layout", choices=["1x2", "2x2"], default="2x2", help="Subfigure layout grid")
    parser.add_argument("--images", nargs="+", required=True, help="Image file paths for subfigures")
    parser.add_argument("--labels", nargs="+", default=[], help="Labels for subfigures e.g. '(a) ...' '(b) ...'")
    parser.add_argument("--fig-num", type=int, default=1, help="Figure number (for SEQ Fig and bookmark)")
    parser.add_argument("--caption", default="Subfigure comparison.", help="Main figure caption text")
    parser.add_argument("--output", default=None, help="Output docx file (default overwrites target)")

    args = parser.parse_args()

    doc = Document(args.docx)
    insert_subfigure_from_template(
        target_doc=doc,
        template_path=args.template,
        layout=args.layout,
        images=args.images,
        labels=args.labels,
        fig_num=args.fig_num,
        caption_text=args.caption
    )

    out_file = args.output or args.docx
    doc.save(out_file)
    print(f"[SUCCESS] Inserted {args.layout} subfigure panel referencing template into: {out_file}")

if __name__ == "__main__":
    main()

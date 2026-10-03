import os
import win32com.client
import fitz
from PIL import Image

out_dir = r"C:\JunzanLi_project\skills_mcp\skills\tex-to-word-converter\demo_output"
docx_path = os.path.abspath(os.path.join(out_dir, "Publication_Grade_CCC_Template.docx"))
pdf_path = os.path.abspath(os.path.join(out_dir, "Publication_Grade_CCC_Template.pdf"))

word = win32com.client.Dispatch("Word.Application")
word.Visible = False
doc = word.Documents.Open(docx_path)
doc.SaveAs(pdf_path, FileFormat=17) # wdFormatPDF = 17
doc.Close()
word.Quit()
print("[OK] Converted CCC docx to PDF.")

doc_pdf = fitz.open(pdf_path)
images = []
for p_num in range(min(2, len(doc_pdf))):
    page = doc_pdf[p_num]
    pix = page.get_pixmap(dpi=150)
    p_path = os.path.join(out_dir, f"ccc_template_page_{p_num+1}.png")
    pix.save(p_path)
    images.append(Image.open(p_path))

if len(images) == 2:
    w, h = images[0].size
    gap = 30
    comb = Image.new("RGB", (w * 2 + gap, h), (230, 230, 230))
    comb.paste(images[0], (0, 0))
    comb.paste(images[1], (w + gap, 0))
    comb_path = os.path.join(out_dir, "ccc_template_preview_twopage.png")
    comb.save(comb_path)
    print(f"[SUCCESS] Saved CCC side-by-side preview: {comb_path}")
